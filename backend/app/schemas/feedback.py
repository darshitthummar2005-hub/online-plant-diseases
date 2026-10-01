"""
Feedback schemas.

Request/response models for the feedback system.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    """Payload for POST /feedback."""

    rating: int = Field(ge=1, le=5)
    message: str | None = Field(default=None, max_length=2000)
    prediction_id: str | None = None


class FeedbackOut(BaseModel):
    """Feedback record response."""

    id: str
    rating: int
    message: str | None = None
    prediction_id: str | None = None
    submitted_at: datetime
