"""
Prediction service layer.

Runs the disease detection pipeline. A real ML model would plug in here; the
current implementation is a transparent rule-based matcher that scores diseases
against the uploaded image presence + user-selected symptom keywords, then
persists the result in MongoDB.

Endpoints use this service for: create prediction, list history, get one.
"""

import re
from datetime import datetime

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate, PredictionOut
from app.utils.logger import get_logger
from app.utils.pagination import paginate_async

logger = get_logger(__name__)


class PredictionService:
    """Creates, lists and retrieves disease predictions."""

    def __init__(
        self,
        predictions: AsyncIOMotorCollection,
        diseases: AsyncIOMotorCollection,
    ) -> None:
        self.predictions = predictions
        self.diseases = diseases

    # ---------- Core prediction ----------
    async def predict(self, user_id: str, payload: PredictionCreate) -> PredictionOut:
        """Create a prediction for the given symptoms (optionally linked image)."""
        symptoms = [s.strip().lower() for s in payload.symptoms if s.strip()]

        # Gather every known disease.
        disease_docs = await self.diseases.find({}).to_list(length=10000)

        # Score each disease by keyword overlap with the chosen symptoms.
        scored = [
            (self._score_disease(doc, symptoms), doc)
            for doc in disease_docs
        ]
        scored.sort(key=lambda pair: pair[0], reverse=True)

        best_score, best_doc = scored[0] if scored else (0.0, None)

        disease_id = None
        disease_name = "Unknown"
        confidence = 0.0
        disease_payload = None

        if best_doc:
            disease_id = str(best_doc["_id"])
            disease_name = best_doc["name"]
            # Heuristic confidence: starts at 0.35 when an image is present, grows
            # with symptom overlap. Caps at 0.97.
            confidence = round(min(0.97, 0.35 + best_score * 0.12), 3)
            disease_payload = self._disease_to_dict(best_doc)

        record = Prediction(
            user_id=user_id,
            image_id=payload.image_id,
            disease_id=disease_id,
            disease_name=disease_name,
            confidence=confidence,
            status="completed",
            model_version=payload.model_version or "rule-demo-v1",
            symptoms=symptoms,
        )
        doc = record.to_doc()
        result = await self.predictions.insert_one(doc)

        logger.info("Prediction %s for user %s -> %s (%.2f)", result.inserted_id, user_id, disease_name, confidence)

        out = self._to_out(doc, result.inserted_id, disease_payload)
        return out

    # ---------- History ----------
    async def history(self, user_id: str, page: int, page_size: int):
        """Paginated prediction history for a user (newest first)."""
        items, total = await paginate_async(
            self.predictions,
            {"user_id": user_id},
            page,
            page_size,
            sort=[("predicted_at", -1)],
        )
        # Attach disease summaries for each prediction in the page.
        disease_ids = [doc.get("disease_id") for doc in items if doc.get("disease_id")]
        disease_map: dict = {}
        if disease_ids:
            from bson import ObjectId

            oids = [ObjectId(did) for did in disease_ids if __is_valid_oid(did)]
            if oids:
                for d in await self.diseases.find({"_id": {"$in": oids}}).to_list(length=1000):
                    disease_map[str(d["_id"])] = self._disease_to_dict(d)

        outs = [
            self._to_out(doc, doc["_id"], disease_map.get(str(doc.get("disease_id"))))
            for doc in items
        ]
        return outs, total

    async def get(self, user_id: str, prediction_id: str) -> PredictionOut:
        """Fetch one prediction, verifying ownership."""
        doc = await self.predictions.find_one({"_id": __oid(prediction_id), "user_id": user_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Prediction not found")

        disease_payload = None
        if doc.get("disease_id"):
            disease_doc = await self.diseases.find_one({"_id": __oid(doc["disease_id"])})
            if disease_doc:
                disease_payload = self._disease_to_dict(disease_doc)

        return self._to_out(doc, doc["_id"], disease_payload)

    # ---------- Helpers ----------
    @staticmethod
    def _score_disease(doc: dict, symptoms: list[str]) -> int:
        """Count how many chosen symptoms appear in a disease record's text."""
        if not symptoms:
            return 0
        haystack = " ".join(
            [
                str(doc.get("name", "")),
                str(doc.get("description", "")),
                " ".join(doc.get("symptoms", [])),
                " ".join(doc.get("causes", [])),
            ]
        ).lower()
        return sum(1 for s in symptoms if s in haystack)

    @staticmethod
    def _disease_to_dict(doc: dict) -> dict:
        """Public dictionary projection of a disease document."""
        return {
            "id": str(doc.get("_id")),
            "name": doc.get("name"),
            "category": doc.get("category"),
            "scientific_name": doc.get("scientific_name"),
            "severity": doc.get("severity"),
            "description": doc.get("description"),
            "symptoms": doc.get("symptoms", []),
            "causes": doc.get("causes", []),
            "treatment": doc.get("treatment", []),
            "prevention": doc.get("prevention", []),
            "affected_plants": doc.get("affected_plants", []),
        }

    @staticmethod
    def _to_out(doc: dict, oid, disease_payload: dict | None) -> PredictionOut:
        """Serialize a stored prediction into the response schema."""
        return PredictionOut(
            id=str(oid),
            disease_id=str(doc["disease_id"]) if doc.get("disease_id") else None,
            disease_name=doc.get("disease_name", "Unknown"),
            confidence=doc.get("confidence", 0.0),
            status=doc.get("status", "completed"),
            model_version=doc.get("model_version", "rule-demo-v1"),
            symptoms=doc.get("symptoms", []),
            image_id=str(doc["image_id"]) if doc.get("image_id") else None,
            predicted_at=doc.get("predicted_at", datetime.utcnow()),
            disease=disease_payload,
        )


def __oid(value: str):
    """Convert a string id to a bson ObjectId."""
    from bson import ObjectId

    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")


def __is_valid_oid(value: str) -> bool:
    """Return True if the string is a valid ObjectId hex value."""
    from bson import ObjectId

    try:
        ObjectId(value)
        return True
    except Exception:
        return False
