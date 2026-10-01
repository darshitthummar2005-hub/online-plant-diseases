"""
Admin routes.

Endpoints (all admin-only, guarded by `get_current_admin`):
  GET    /admin/stats              - dashboard counters
  GET    /admin/overview           - counters + charts + recent activity
  GET    /admin/users              - paginated user list (search / role filter)
  PATCH  /admin/users/{id}         - rename / change role / enable-disable
  DELETE /admin/users/{id}         - delete an account
  GET    /admin/detections         - paginated disease-detection records
  GET    /admin/admins             - list the administrator accounts

Authorisation is enforced here on the server, so typing an admin URL (or calling
the API directly) as a normal user is rejected with 403 regardless of what the
frontend does.
"""

from fastapi import APIRouter, Depends, Query

from app.dependencies.auth_deps import get_current_admin
from app.dependencies.db_deps import get_db
from app.database import Database
from app.schemas.admin import (
    ActivityOut,
    AdminStats,
    AdminUserOut,
    AdminUserUpdate,
    CategoryCount,
    DetectionOut,
)
from app.schemas.common import Message, Page
from app.schemas.user import UserOut
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_service(db: Database = Depends(get_db)) -> AdminService:
    """FastAPI dependency providing an AdminService bound to the database."""
    return AdminService(db.raw)


@router.get(
    "/stats",
    response_model=AdminStats,
    summary="Dashboard statistics (admin)",
    description="Headline counters for the admin dashboard overview.",
)
async def get_stats(
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Return the aggregate platform counters."""
    return await service.stats()


@router.get(
    "/overview",
    summary="Dashboard overview (admin)",
    description="Counters, disease-category breakdown and the recent-activity feed.",
)
async def get_overview(
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Return everything the overview page needs in a single round trip."""
    stats = await service.stats()
    categories = await service.disease_categories()
    activity = await service.recent_activity()
    return {
        "stats": stats,
        "disease_categories": categories,
        "recent_activity": activity,
    }


@router.get(
    "/users",
    response_model=Page[AdminUserOut],
    summary="List users (admin)",
    description="Paginated list of every account, with optional search and role filter.",
)
async def list_users(
    q: str | None = Query(None, max_length=120, description="Search username/email/name"),
    role: str | None = Query(None, pattern="^(user|admin)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """List registered users."""
    items, total = await service.list_users(page, page_size, q, role)
    return Page[AdminUserOut].build(items, total, page, page_size)


@router.patch(
    "/users/{user_id}",
    response_model=AdminUserOut,
    summary="Update user (admin)",
    description="Change an account's display name, role or active status.",
)
async def update_user(
    user_id: str,
    payload: AdminUserUpdate,
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Apply an admin change to a user account."""
    return await service.update_user(user_id, payload, admin)


@router.delete(
    "/users/{user_id}",
    response_model=Message,
    summary="Delete user (admin)",
    description="Permanently remove a user account.",
)
async def delete_user(
    user_id: str,
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Delete a user account."""
    await service.delete_user(user_id, admin)
    return Message(detail="User deleted")


@router.get(
    "/detections",
    response_model=Page[DetectionOut],
    summary="List detection records (admin)",
    description="Paginated history of every disease detection performed on the portal.",
)
async def list_detections(
    q: str | None = Query(None, max_length=120, description="Search disease name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """List the disease-detection records."""
    items, total = await service.list_detections(page, page_size, q)
    return Page[DetectionOut].build(items, total, page, page_size)


@router.get(
    "/admins",
    response_model=list[AdminUserOut],
    summary="List admin accounts (admin)",
    description="Every active administrator account. Never returns credentials.",
)
async def list_admins(
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """List the administrator accounts."""
    items, _total = await service.list_users(1, 100, None, "admin")
    return [u for u in items if u.is_active]


@router.get(
    "/activity",
    response_model=list[ActivityOut],
    summary="Recent activity (admin)",
    description="The latest registrations and detections, newest first.",
)
async def recent_activity(
    limit: int = Query(8, ge=1, le=25),
    service: AdminService = Depends(get_admin_service),
    admin: UserOut = Depends(get_current_admin),
):
    """Return the recent-activity feed."""
    return await service.recent_activity(limit)
