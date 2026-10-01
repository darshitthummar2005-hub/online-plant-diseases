"""
Prediction routes.

Endpoints:
  POST /predictions        - run detection and save the result (protected)
  GET  /predictions        - paginated prediction history (protected)
  GET  /predictions/{id}   - one prediction (protected, owner only)
"""

from fastapi import APIRouter, Depends

from app.database import Database
from app.dependencies.auth_deps import get_current_user
from app.dependencies.db_deps import get_db
from app.dependencies.pagination_deps import get_pagination
from app.schemas.common import Page
from app.schemas.prediction import PredictionCreate, PredictionOut
from app.schemas.user import UserOut
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions", tags=["Predictions"])


def get_prediction_service(db: Database = Depends(get_db)) -> PredictionService:
    """FastAPI dependency providing a PredictionService bound to the collections."""
    return PredictionService(db.predictions, db.plant_diseases)


@router.post(
    "",
    response_model=PredictionOut,
    status_code=201,
    summary="Run disease detection",
    description="Submit symptoms (and/or a previously uploaded image id) to get a prediction.",
)
async def create_prediction(
    payload: PredictionCreate,
    user: UserOut = Depends(get_current_user),
    service: PredictionService = Depends(get_prediction_service),
):
    """Run detection and persist the prediction."""
    return await service.predict(user.id, payload)


@router.get(
    "",
    response_model=Page[PredictionOut],
    summary="Prediction history",
    description="Paginated list of the user's past predictions (newest first).",
)
async def list_predictions(
    pagination: tuple[int, int] = Depends(get_pagination),
    user: UserOut = Depends(get_current_user),
    service: PredictionService = Depends(get_prediction_service),
):
    """Return the user's prediction history."""
    page, page_size = pagination
    items, total = await service.history(user.id, page, page_size)
    return Page[PredictionOut].build(items, total, page, page_size)


@router.get(
    "/{prediction_id}",
    response_model=PredictionOut,
    summary="Get one prediction",
    description="Return a single prediction owned by the user, with disease details.",
)
async def get_prediction(
    prediction_id: str,
    user: UserOut = Depends(get_current_user),
    service: PredictionService = Depends(get_prediction_service),
):
    """Return one of the user's predictions."""
    return await service.get(user.id, prediction_id)
