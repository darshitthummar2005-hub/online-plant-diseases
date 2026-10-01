"""
Upload routes.

Endpoints:
  POST /uploads        - upload an image (protected, multipart/form-data)
  GET  /uploads/{id}   - metadata for one upload (protected, owner only)
"""

from fastapi import APIRouter, Depends, File, UploadFile

from app.database import Database
from app.dependencies.auth_deps import get_current_user
from app.dependencies.db_deps import get_db
from app.schemas.upload import UploadResponse
from app.schemas.user import UserOut
from app.services.image_service import ImageService

router = APIRouter(prefix="/uploads", tags=["Uploads"])


def get_image_service(db: Database = Depends(get_db)) -> ImageService:
    """FastAPI dependency providing an ImageService bound to the collection."""
    return ImageService(db.uploaded_images)


@router.post(
    "",
    response_model=UploadResponse,
    status_code=201,
    summary="Upload a leaf image",
    description="Upload an image (jpg/png/webp, max 5 MB). Returns metadata + public URL.",
)
async def upload_image(
    file: UploadFile = File(..., description="Image file"),
    user: UserOut = Depends(get_current_user),
    service: ImageService = Depends(get_image_service),
):
    """Upload and index an image for the authenticated user."""
    return await service.save_upload(user.id, file)


@router.get(
    "/{image_id}",
    response_model=UploadResponse,
    summary="Get upload metadata",
    description="Return metadata for one of the user's uploads.",
)
async def get_upload(
    image_id: str,
    user: UserOut = Depends(get_current_user),
    service: ImageService = Depends(get_image_service),
):
    """Return metadata for a single upload owned by the user."""
    record = await service.get_upload(user.id, image_id)
    return UploadResponse(
        image_id=record.id,
        filename=record.filename,
        content_type=record.content_type,
        size_bytes=record.size_bytes,
        url=f"/uploads/{user.id}/{record.filename}",
        sha256=record.sha256,
        width=record.width,
        height=record.height,
        uploaded_at=record.uploaded_at,
    )
