"""
Prediction document model.

Stored in the `predictions` collection. Records every disease diagnosis made
for a user so they can view their history.
"""

from datetime import datetime

from pydantic import Field

from app.models.base import MongoModel


class Prediction(MongoModel):
    """A single disease prediction result."""

    user_id: str
    image_id: str | None = None
    disease_id: str | None = None
    disease_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    status: str = Field(default="completed")  # pending | completed | failed
    model_version: str = Field(default="rule-demo-v1")
    symptoms: list[str] = Field(default_factory=list)
    predicted_at: datetime = Field(default_factory=datetime.utcnow)
