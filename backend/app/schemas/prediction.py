"""
Prediction schemas.

Request/response models for the disease prediction endpoints and history.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PredictionCreate(BaseModel):
    """
    Payload for POST /predictions.

    When an image was uploaded first, `image_id` links the prediction to it.
    `symptoms` may carry user-selected symptom keywords to help the matcher.
    """

    image_id: str | None = None
    symptoms: list[str] = Field(default_factory=list, max_length=20)
    model_version: str | None = None


class PredictionOut(BaseModel):
    """A single prediction response."""

    id: str
    disease_id: str | None = None
    disease_name: str
    confidence: float
    status: Literal["pending", "completed", "failed"]
    model_version: str
    symptoms: list[str]
    image_id: str | None = None
    predicted_at: datetime
    # Convenience: full disease details when a match was found.
    disease: dict | None = None
