"""
Upload schemas.

Response models for image upload endpoints.
"""

from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response after a successful image upload."""

    image_id: str
    filename: str
    content_type: str
    size_bytes: int
    url: str  # public URL to view/download the image
    sha256: str
    width: int | None = None
    height: int | None = None
    uploaded_at: datetime
