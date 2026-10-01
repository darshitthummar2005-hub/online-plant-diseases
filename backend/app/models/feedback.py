"""
Feedback document model.

Stored in the `feedback` collection. Users can rate the portal and leave
messages, optionally linked to a specific prediction they received.
"""

from datetime import datetime

from pydantic import Field

from app.models.base import MongoModel


class Feedback(MongoModel):
    """User feedback/rating for a prediction or the portal in general."""

    user_id: str
    rating: int = Field(ge=1, le=5)
    message: str | None = Field(default=None, max_length=2000)
    prediction_id: str | None = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
