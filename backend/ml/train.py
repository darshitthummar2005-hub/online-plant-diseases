"""
Train the AI Plant Doctor image classifier on the PlantVillage dataset.

Usage
-----
    pip install -r requirements-ml.txt

    # 1. Download PlantVillage and extract it so that you have:
    #      ml/data/PlantVillage/<Class_Name>__<Disease_Name>/*.jpg
    #    (https://www.kaggle.com/datasets/emmarex/plantdisease)

    # 2. Train:
    python -m ml.train --data ml/data/PlantVillage

    # Optional flags:
    python -m ml.train --data ml/data/PlantVillage --epochs 25 --batch 32
    python -m ml.train --data ml/data/PlantVillage --weights mobilenetv2

What it does
------------
Fine-tunes a pre-trained backbone (ImageNet weights) as a 38-class classifier.
A frozen-backbone first stage then a fine-tuning stage gives good accuracy in a
few epochs on CPU. The trained model and its label list are written to
`ml/models/`, where `ml.inference` picks them up automatically.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ml.inference import CLASS_LABEL_MAP, IMAGE_SIZE, LABELS_PATH, MODEL_PATH

DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data" / "PlantVillage"
MODELS_DIR = Path(__file__).resolve().parent / "models"

BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
SEED = 42


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_DIR, help="Dataset root")
    parser.add_argument("--epochs", type=int, default=15, help="Fine-tune epochs")
    parser.add_argument("--batch", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument(
        "--weights",
        default="mobilenetv2",
        choices=["mobilenetv2", "efficientnetb0", "resnet50"],
        help="Backbone to fine-tune",
    )
    parser.add_argument("--out", type=Path, default=MODELS_DIR, help="Where to save the model")
    return parser.parse_args()


def discover_classes(data_dir: Path) -> list[str]:
    """Return sorted class directory names that contain images."""
    if not data_dir.is_dir():
        raise SystemExit(
            f"Dataset directory not found: {data_dir}\n"
            "Download PlantVillage and extract it there, or pass --data <path>."
        )
    classes = sorted(
        d.name
        for d in data_dir.iterdir()
        if d.is_dir() and any(p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"} for p in d.iterdir())
    )
    if not classes:
        raise SystemExit(f"No class folders with images inside {data_dir}")
    return classes


def build_model(weights: str, num_classes: int):
    """Build and compile the requested backbone as a transfer-learning model."""
    import tensorflow as tf
    from tensorflow.keras import layers, models

    if weights == "mobilenetv2":
        base = tf.keras.applications.MobileNetV2(
            input_shape=(*IMAGE_SIZE, 3), include_top=False, weights="imagenet"
        )
        base.trainable = False
        x = layers.Conv2D(128, 3, padding="same", activation="relu")(base.output)
    elif weights == "efficientnetb0":
        base = tf.keras.applications.EfficientNetB0(
            input_shape=(*IMAGE_SIZE, 3), include_top=False, weights="imagenet"
        )
        base.trainable = False
        x = base.output
    else:
        base = tf.keras.applications.ResNet50(
            input_shape=(*IMAGE_SIZE, 3), include_top=False, weights="imagenet"
        )
        base.trainable = False
        x = layers.Conv2D(256, 3, padding="same", activation="relu")(base.output)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    out = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = models.Model(base.input, out, name=f"plant_disease_{weights}")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return base, model


def main() -> int:
    args = parse_args()

    try:
        import tensorflow as tf
    except ImportError:
        print(
            "TensorFlow is not installed.\n"
            "Run: pip install -r requirements-ml.txt",
            file=sys.stderr,
        )
        return 1

    tf.random.set_seed(SEED)

    classes = discover_classes(args.data)
    print(f"Found {len(classes)} classes in {args.data}")
    if len(classes) != len(CLASS_LABEL_MAP):
        unknown = [c for c in classes if c not in CLASS_LABEL_MAP]
        if unknown:
            print(
                "Warning: these classes are not in CLASS_LABEL_MAP, so their "
                "predictions will be shown with a cleaned-up folder name:",
            )
            for name in unknown:
                print(f"  - {name}")

    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
        args.data,
        labels="inferred",
        label_mode="categorical",
        batch_size=args.batch,
        image_size=IMAGE_SIZE,
        validation_split=VALIDATION_SPLIT,
        seed=SEED,
    )

    augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.1),
        ],
        name="augmentation",
    )
    train_ds = train_ds.map(
        lambda x, y: (augmentation(x, training=True), y),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    base, model = build_model(args.weights, len(classes))
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=4, restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=2, min_lr=1e-5
        ),
    ]

    print("\nStage 1/2: training the classifier head (backbone frozen)")
    model.fit(train_ds, validation_data=val_ds, epochs=max(2, args.epochs // 3), callbacks=callbacks)

    print("\nStage 2/2: fine-tuning the backbone")
    base.trainable = True
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)

    args.out.mkdir(parents=True, exist_ok=True)
    model.save(args.out / MODEL_PATH.name)
    LABELS_PATH.write_text(json.dumps(classes, indent=2), encoding="utf-8")

    print(f"\nSaved model   -> {args.out / MODEL_PATH.name}")
    print(f"Saved labels  -> {LABELS_PATH}")
    print("Restart the API; image classification is picked up automatically.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())