"""
Disease routes.

Endpoints:
  GET    /diseases                - search/paginate diseases (public)
  GET    /diseases/categories     - distinct categories (public)
  GET    /diseases/{id}           - one disease (public)
  POST   /diseases                - create disease (admin)
  PATCH  /diseases/{id}           - update disease (admin)
  DELETE /diseases/{id}           - delete disease (admin)
"""

from fastapi import APIRouter, Depends

from app.database import Database
from app.dependencies.auth_deps import get_current_admin
from app.dependencies.db_deps import get_db
from app.dependencies.pagination_deps import get_pagination
from app.schemas.common import Message, Page
from app.schemas.disease import DiseaseCreate, DiseaseOut, DiseaseUpdate
from app.schemas.user import UserOut
from app.services.disease_service import DiseaseService

router = APIRouter(prefix="/diseases", tags=["Diseases"])


def get_disease_service(db: Database = Depends(get_db)) -> DiseaseService:
    """FastAPI dependency providing a DiseaseService bound to the collection."""
    return DiseaseService(db.plant_diseases)


@router.get(
    "",
    response_model=Page[DiseaseOut],
    summary="Search diseases",
    description="Search diseases by name/description/symptoms with pagination and category filter.",
)
async def search_diseases(
    q: str | None = None,
    category: str | None = None,
    pagination: tuple[int, int] = Depends(get_pagination),
    service: DiseaseService = Depends(get_disease_service),
):
    """Search and paginate diseases."""
    page, page_size = pagination
    items, total = await service.search(q, category, page, page_size)
    return Page[DiseaseOut].build([DiseaseOut.model_validate(i) for i in items], total, page, page_size)


@router.get(
    "/categories",
    response_model=list[str],
    summary="List categories",
    description="Return all distinct disease categories.",
)
async def list_categories(service: DiseaseService = Depends(get_disease_service)):
    """List distinct disease categories."""
    return await service.categories()


@router.get(
    "/{disease_id}",
    response_model=DiseaseOut,
    summary="Get one disease",
    description="Fetch a single disease record by id.",
)
async def get_disease(
    disease_id: str,
    service: DiseaseService = Depends(get_disease_service),
):
    """Return a single disease."""
    doc = await service.get(disease_id)
    return DiseaseOut.model_validate(doc)


@router.post(
    "",
    response_model=DiseaseOut,
    status_code=201,
    summary="Create disease (admin)",
    description="Admin-only: add a new disease to the knowledge base.",
)
async def create_disease(
    payload: DiseaseCreate,
    service: DiseaseService = Depends(get_disease_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Create a new disease record."""
    doc = await service.create(payload)
    return DiseaseOut.model_validate(doc)


@router.patch(
    "/{disease_id}",
    response_model=DiseaseOut,
    summary="Update disease (admin)",
    description="Admin-only: partially update a disease record.",
)
async def update_disease(
    disease_id: str,
    payload: DiseaseUpdate,
    service: DiseaseService = Depends(get_disease_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Update a disease record."""
    doc = await service.update(disease_id, payload)
    return DiseaseOut.model_validate(doc)


@router.delete(
    "/{disease_id}",
    response_model=Message,
    summary="Delete disease (admin)",
    description="Admin-only: delete a disease record.",
)
async def delete_disease(
    disease_id: str,
    service: DiseaseService = Depends(get_disease_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Delete a disease record."""
    await service.delete(disease_id)
    return Message(detail="Disease deleted")
