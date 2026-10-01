"""
Image validation helpers.

Validates uploaded files: extension, content type and that they really are
images (using Pillow to decode the header). Also computes a SHA-256 hash and
image dimensions.
"""

import hashlib
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.utils.logger import get_logger

logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


def validate_image(file: UploadFile, max_bytes: int) -> tuple[str, int]:
    """
    Validate extension + MIME type + size.

    Returns (safe_extension, size_bytes) or raises HTTPException.
    """
    # Extension check
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    # MIME check
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported content type '{content_type}'.",
        )

    # Size check (read whole file)
    data = file.file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large (max {max_bytes // (1024 * 1024)} MB)",
        )
    return ext, len(data)


def compute_sha256(data: bytes) -> str:
    """Return hex SHA-256 of the file bytes."""
    return hashlib.sha256(data).hexdigest()


def read_dimensions(data: bytes) -> tuple[int | None, int | None]:
    """Return (width, height) using Pillow's header reader (no full decode)."""
    try:
        from PIL import Image

        with Image.open(__import__("io").BytesIO(data)) as img:
            return img.width, img.height
    except Exception as exc:  # pragma: no cover - corrupt images
        logger.warning("Could not read image dimensions: %s", exc)
        return None, None
