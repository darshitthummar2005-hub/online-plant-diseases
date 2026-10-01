"""
Detection routes (AI Plant Doctor).

Endpoints:
  POST /detect - public disease diagnosis returning a full report
"""

from fastapi import APIRouter, Depends

from app.database import Database
from app.dependencies.db_deps import get_db
from app.schemas.detection import DetectRequest, DetectResponse
from app.services.detect_service import DetectService

router = APIRouter(prefix="/detect", tags=["Detection"])


def get_detect_service(db: Database = Depends(get_db)) -> DetectService:
    """FastAPI dependency providing a DetectService bound to the collection."""
    return DetectService(db.plant_diseases)


@router.post(
    "",
    response_model=DetectResponse,
    summary="Run AI Plant Doctor detection",
    description=(
        "Submit symptom keywords (and optionally an image) to receive a complete "
        "diagnosis report: confidence, severity, treatment plans, prevention tips, "
        "fertilizer and weather guidance."
    ),
)
async def run_detection(
    payload: DetectRequest,
    service: DetectService = Depends(get_detect_service),
):
    """Run the diagnosis pipeline and return the full report."""
    return await service.detect(payload)
