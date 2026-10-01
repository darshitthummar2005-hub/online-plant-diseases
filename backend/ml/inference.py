"""
Real image classification for the AI Plant Doctor.

This module is **optional**. The website works without it (the rule-based
symptom matcher takes over), which keeps the normal deployment small. Install
the extra dependencies and train a model to switch on real inference:

    pip install -r backend/requirements-ml.txt
    python -m ml.train --data backend/ml/data/PlantVillage

At runtime the classifier is used automatically when all three hold:

  1. TensorFlow is importable
  2. The trained model file exists (ML_MODEL_PATH, or ml/models/... )
  3. The image decodes successfully

Anything missing degrades to `None` and the caller falls back, so a broken or
absent model can never take the API down.
"""

from __future__ import annotations

import base64
import binascii
import io
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

IMAGE_SIZE = (224, 224)
#: Below this probability a prediction is treated as "not confident enough".
DEFAULT_MIN_CONFIDENCE = float(os.getenv("ML_MIN_CONFIDENCE", "55"))

MODEL_PATH = Path(
    os.getenv(
        "ML_MODEL_PATH",
        str(Path(__file__).resolve().parent / "models" / "plant_disease_mobilenetv2.h5"),
    )
)
LABELS_PATH = Path(
    os.getenv(
        "ML_LABELS_PATH",
        str(Path(__file__).resolve().parent / "models" / "labels.json"),
    )
)

#: PlantVillage folder name -> disease name used by the knowledge base.
#: Keys are the raw PlantVillage class directory names.
CLASS_LABEL_MAP: dict[str, str] = {
    "Apple___Apple_scab": "Apple Scab",
    "Apple___Black_rot": "Apple Black Rot",
    "Apple___Cedar_apple_rust": "Apple Cedar Apple Rust",
    "Apple___healthy": "Apple Healthy Foliage",
    "Blueberry___healthy": "Blueberry Healthy Foliage",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry Powdery Mildew",
    "Cherry_(including_sour)___healthy": "Cherry Healthy Foliage",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn Gray Leaf Spot",
    "Corn_(maize)___Common_rust_": "Corn Common Rust",
    "Corn_(maize)___Northern_Leaf_Blight": "Corn Northern Leaf Blight",
    "Corn_(maize)___healthy": "Corn Healthy Foliage",
    "Grape___Black_rot": "Grape Black Rot",
    "Grape___Esca_(Black_Measles)": "Grape Esca (Black Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape Leaf Blight (Isariopsis)",
    "Grape___healthy": "Grape Healthy Foliage",
    "Orange___Haunglongbing_(Citrus_greening)": "Orange Haunglongbing Leaf Symptom Reference",
    "Peach___Bacterial_spot": "Peach Bacterial Spot",
    "Peach___healthy": "Peach Healthy Foliage",
    "Pepper,_bell___Bacterial_spot": "Pepper Bell Bacterial Spot",
    "Pepper,_bell___healthy": "Pepper Bell Healthy Foliage",
    "Potato___Early_blight": "Potato Early Blight",
    "Potato___Late_blight": "Potato Late Blight",
    "Potato___healthy": "Potato Healthy Foliage",
    "Raspberry___healthy": "Raspberry Healthy Foliage",
    "Soybean___healthy": "Soybean Healthy Foliage",
    "Squash___Powdery_mildew": "Squash Powdery Mildew",
    "Strawberry___Leaf_scorch": "Strawberry Leaf Scorch",
    "Strawberry___healthy": "Strawberry Healthy Foliage",
    "Tomato___Bacterial_spot": "Tomato Bacterial Spot",
    "Tomato___Early_blight": "Tomato Early Blight",
    "Tomato___Late_blight": "Tomato Late Blight",
    "Tomato___Leaf_Mold": "Tomato Leaf Mold",
    "Tomato___Septoria_leaf_spot": "Tomato Septoria Leaf Spot",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato Spider Mites (Two-spotted)",
    "Tomato___Target_Spot": "Tomato Target Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato Yellow Leaf Curl Virus",
    "Tomato___Tomato_mosaic_virus": "Tomato Mosaic Virus",
    "Tomato___healthy": "Tomato Healthy Foliage",
}

#: Species each label belongs to, used to sanity-check a user-selected plant.
CROP_OF_LABEL: dict[str, str] = {
    "Apple": "apple",
    "Blueberry": "blueberry",
    "Cherry": "cherry",
    "Corn": "corn",
    "Grape": "grape",
    "Orange": "orange",
    "Peach": "peach",
    "Pepper": "pepper",
    "Potato": "potato",
    "Raspberry": "raspberry",
    "Soybean": "soybean",
    "Squash": "squash",
    "Strawberry": "strawberry",
    "Tomato": "tomato",
}


@dataclass
class Prediction:
    """One classified result, ready to be merged into a diagnosis report."""

    raw_label: str
    disease_name: str
    confidence: float
    is_healthy: bool = False
    crop: str = ""
    alternatives: list[tuple[str, float]] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "disease_name": self.disease_name,
            "confidence": round(self.confidence, 2),
            "is_healthy": self.is_healthy,
            "crop": self.crop,
            "raw_label": self.raw_label,
        }


def _healthy_label(raw_label: str) -> bool:
    return "healthy" in raw_label.lower()


def _crop_for(raw_label: str) -> str:
    species = raw_label.split("___", 1)[0].split("_", 1)[0]
    return CROP_OF_LABEL.get(species, species.lower())


def _load_labels() -> list[str]:
    """Return class labels, preferring the sidecar JSON written by training."""
    if LABELS_PATH.is_file():
        try:
            data = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return [str(x) for x in data]
            if isinstance(data, dict) and data.get("labels"):
                return [str(x) for x in data["labels"]]
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not read %s (%s); using built-in labels", LABELS_PATH, exc)
    return list(CLASS_LABEL_MAP.keys())


class PlantDiseaseClassifier:
    """Thin, lazily-initialised wrapper around the trained Keras model."""

    def __init__(self) -> None:
        self._model = None
        self._labels: list[str] | None = None
        self._load_failed = False

    @property
    def available(self) -> bool:
        """True when a model file is present and TensorFlow can be imported."""
        if self._load_failed:
            return False
        if self._model is not None:
            return True
        return MODEL_PATH.is_file()

    def load(self) -> bool:
        """Load the model once. Returns False if unavailable; never raises."""
        if self._model is not None:
            return True
        if self._load_failed:
            return False

        if not MODEL_PATH.is_file():
            logger.info(
                "ML model not found at %s. Symptom-based detection stays active. "
                "Train one with: python -m ml.train --data ml/data/PlantVillage",
                MODEL_PATH,
            )
            return False

        try:
            import tensorflow as tf  # noqa: PLC0415 - deliberately lazy and optional
        except ImportError as exc:
            logger.info(
                "TensorFlow is not installed (%s). Install requirements-ml.txt to "
                "enable image classification.",
                exc,
            )
            return False

        try:
            self._model = tf.keras.models.load_model(MODEL_PATH)
            self._labels = _load_labels()
            logger.info("Loaded plant disease model from %s", MODEL_PATH)
            return True
        except Exception as exc:  # noqa: BLE001 - a bad model must not break the API
            self._load_failed = True
            logger.error("Failed to load ML model %s: %s", MODEL_PATH, exc)
            return False

    def predict(self, image_bytes: bytes, top_k: int = 3) -> Prediction | None:
        """Classify raw image bytes. Returns None when the model is unusable."""
        if not image_bytes or not self.load():
            return None

        try:
            import numpy as np  # noqa: PLC0415
            from PIL import Image  # noqa: PLC0415

            img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(IMAGE_SIZE)
            arr = np.expand_dims(np.asarray(img, dtype="float32") / 255.0, axis=0)

            probs = np.asarray(self._model.predict(arr, verbose=0))[0]
            labels = self._labels or _load_labels()
            if len(labels) != probs.shape[-1]:
                logger.warning(
                    "Model outputs %s classes but %s labels are known; skipping "
                    "image prediction.",
                    probs.shape[-1],
                    len(labels),
                )
                return None

            order = np.argsort(probs)[::-1][:top_k]
            ranked = [(labels[int(i)], float(probs[int(i)])) for i in order]
        except (binascii.Error, OSError, ValueError) as exc:
            logger.warning("Could not analyse image: %s", exc)
            return None
        except Exception as exc:  # noqa: BLE001 - never let inference kill the request
            logger.error("Unexpected image inference error: %s", exc)
            return None

        raw_label, top_conf = ranked[0]
        if top_conf * 100.0 < DEFAULT_MIN_CONFIDENCE:
            logger.info(
                "Top image prediction %.1f%% below threshold %.1f%%; deferring to "
                "symptom matching.",
                top_conf * 100.0,
                DEFAULT_MIN_CONFIDENCE,
            )
            return None

        return Prediction(
            raw_label=raw_label,
            disease_name=CLASS_LABEL_MAP.get(raw_label, raw_label.replace("_", " ").replace("___", " ")),
            confidence=top_conf * 100.0,
            is_healthy=_healthy_label(raw_label),
            crop=_crop_for(raw_label),
            alternatives=[(CLASS_LABEL_MAP.get(lbl, lbl), conf * 100.0) for lbl, conf in ranked[1:]],
        )


#: Process-wide singleton; the model is loaded at most once.
classifier = PlantDiseaseClassifier()


def decode_data_url(image_data: str) -> bytes | None:
    """Decode a `data:image/...;base64,...` string (or bare base64) to bytes."""
    if not image_data:
        return None
    payload = image_data.split(",", 1)[1] if "," in image_data else image_data
    try:
        return base64.b64decode(payload, validate=False)
    except (binascii.Error, ValueError) as exc:
        logger.warning("Invalid base64 image payload: %s", exc)
        return None


def classify_image(image_data: str) -> Prediction | None:
    """
    Classify a data-URL image. Returns None when the ML path is unavailable,
    letting the caller fall back to symptom matching.
    """
    raw = decode_data_url(image_data)
    if raw is None:
        return None
    return classifier.predict(raw)