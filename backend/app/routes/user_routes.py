"""
User routes.

Endpoints:
  GET    /users/me       - current user profile (protected)
  PATCH  /users/me       - update current user profile (protected)
  DELETE /users/me       - delete current user account (protected)
"""

from fastapi import APIRouter, Depends, status

from app.database import Database
from app.dependencies.auth_deps import get_current_user
from app.dependencies.db_deps import get_db
from app.schemas.common import Message
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Database = Depends(get_db)) -> UserService:
    """FastAPI dependency providing a UserService bound to the users collection."""
    return UserService(db.users)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get profile",
    description="Return the authenticated user's profile.",
)
async def get_me(user: UserOut = Depends(get_current_user)):
    """Return the current user's profile."""
    return user


@router.patch(
    "/me",
    response_model=UserOut,
    summary="Update profile",
    description="Update full name, password or active status of the current user.",
)
async def update_me(
    payload: UserUpdate,
    user: UserOut = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Update the current user's profile."""
    return await service.update_profile(user.id, payload)


@router.delete(
    "/me",
    response_model=Message,
    summary="Delete account",
    description="Permanently delete the current user's account.",
)
async def delete_me(
    user: UserOut = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Delete the current user's account."""
    await service.delete_user(user.id)
    return Message(detail="Account deleted")
