"""
Feedback routes.

Endpoints:
  POST /feedback         - submit a rating/message (protected)
  GET  /feedback         - list all feedback (admin)
  GET  /feedback/average - overall average rating (public)
"""

from fastapi import APIRouter, Depends

from app.database import Database
from app.dependencies.auth_deps import get_current_admin, get_current_user
from app.dependencies.db_deps import get_db
from app.dependencies.pagination_deps import get_pagination
from app.schemas.common import Page
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.schemas.user import UserOut
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["Feedback"])


def get_feedback_service(db: Database = Depends(get_db)) -> FeedbackService:
    """FastAPI dependency providing a FeedbackService bound to the collection."""
    return FeedbackService(db.feedback)


@router.post(
    "",
    response_model=FeedbackOut,
    status_code=201,
    summary="Submit feedback",
    description="Authenticated users can rate the portal 1-5 and leave a message.",
)
async def create_feedback(
    payload: FeedbackCreate,
    user: UserOut = Depends(get_current_user),
    service: FeedbackService = Depends(get_feedback_service),
):
    """Store feedback for the authenticated user."""
    return await service.create(user.id, payload)


@router.get(
    "/average",
    response_model=dict,
    summary="Average rating",
    description="Public endpoint returning the overall average feedback rating.",
)
async def average_rating(service: FeedbackService = Depends(get_feedback_service)):
    """Return the average rating across all feedback."""
    return {"average_rating": await service.average_rating()}


@router.get(
    "",
    response_model=Page[FeedbackOut],
    summary="List feedback (admin)",
    description="Admin-only: paginated list of all feedback.",
)
async def list_feedback(
    pagination: tuple[int, int] = Depends(get_pagination),
    service: FeedbackService = Depends(get_feedback_service),
    admin: UserOut = Depends(get_current_admin),
):
    """List all feedback (admin)."""
    page, page_size = pagination
    items, total = await service.list_all(page, page_size)
    return Page[FeedbackOut].build(items, total, page, page_size)
