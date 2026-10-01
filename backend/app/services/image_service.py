"""
Image service layer.

Persists uploaded images to disk, records metadata in MongoDB, and serves them
back via a public URL.
"""

import secrets
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.config import get_settings
from app.models.uploaded_image import UploadedImage
from app.schemas.upload import UploadResponse
from app.utils.image_validator import (
    compute_sha256,
    read_dimensions,
    validate_image,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)
_settings = get_settings()


class ImageService:
    """Handles saving and indexing uploaded leaf images."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def save_upload(self, user_id: str, file: UploadFile) -> UploadResponse:
        """
        Validate and store an image.

        Flow: validate -> generate safe filename -> write to disk -> record
        metadata in MongoDB -> return public response.
        """
        ext, size = validate_image(file, _settings.max_upload_size_bytes)
        data = file.file.read()

        # Directory: uploads/<user_id>/
        user_dir = Path(_settings.upload_dir) / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        # Collision-proof, non-user-controlled filename.
        filename = f"{uuid.uuid4().hex}{ext}"
        path = user_dir / filename
        path.write_bytes(data)

        width, height = read_dimensions(data)
        record = UploadedImage(
            user_id=user_id,
            filename=filename,
            content_type=file.content_type or "application/octet-stream",
            size_bytes=size,
            path=str(path.as_posix()),
            sha256=compute_sha256(data),
            width=width,
            height=height,
        )
        doc = record.to_doc()
        result = await self.collection.insert_one(doc)

        logger.info("Uploaded image %s (%d bytes) for user %s", filename, size, user_id)
        return UploadResponse(
            image_id=str(result.inserted_id),
            filename=filename,
            content_type=record.content_type,
            size_bytes=size,
            url=f"/uploads/{user_id}/{filename}",
            sha256=record.sha256,
            width=width,
            height=height,
            uploaded_at=record.uploaded_at,
        )

    async def get_upload(self, user_id: str, image_id: str) -> UploadedImage:
        """Fetch an upload, ensuring it belongs to the requesting user."""
        doc = await self.collection.find_one({"_id": __oid(image_id), "user_id": user_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Image not found")
        return UploadedImage.from_doc(doc)


def __oid(value: str):
    """Convert a string id to a bson ObjectId."""
    from bson import ObjectId

    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image id")
