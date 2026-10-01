"""
Uploaded image document model.

Stored in the `uploaded_images` collection. Tracks each file stored on disk
(under `uploads/`) together with metadata and a SHA-256 hash for integrity.
"""

from datetime import datetime

from pydantic import Field

from app.models.base import MongoModel


class UploadedImage(MongoModel):
    """Metadata for an image a user uploaded for analysis."""

    user_id: str
    filename: str
    content_type: str
    size_bytes: int
    path: str  # relative path inside UPLOAD_DIR
    sha256: str
    width: int | None = None
    height: int | None = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
