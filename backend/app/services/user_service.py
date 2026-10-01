"""
User service layer.

Profile management for the authenticated user (read, update, delete).
"""

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.auth.security import hash_password
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UserService:
    """Operations on the current user's profile."""

    def __init__(self, users: AsyncIOMotorCollection) -> None:
        self.users = users

    async def get_user(self, user_id: str) -> User:
        """Fetch a user by id or raise 404."""
        from bson import ObjectId

        try:
            user_doc = await self.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            user_doc = None
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        return User.from_doc(user_doc)

    async def update_profile(self, user_id: str, payload: UserUpdate) -> UserOut:
        """Apply non-null fields of UserUpdate to the user's profile."""
        updates: dict = {}
        if payload.full_name is not None:
            updates["full_name"] = payload.full_name
        if payload.is_active is not None:
            updates["is_active"] = payload.is_active
        if payload.password is not None:
            updates["hashed_password"] = hash_password(payload.password)

        if updates:
            updates["updated_at"] = __import__("datetime").datetime.utcnow()
            await self.users.update_one(
                {"_id": __oid(user_id)},
                {"$set": updates},
            )

        user = await self.get_user(user_id)
        logger.info("Updated profile for user %s", user_id)
        return UserOut.from_user(user)

    async def delete_user(self, user_id: str) -> None:
        """Permanently remove a user account."""
        result = await self.users.delete_one({"_id": __oid(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("Deleted user %s", user_id)


def __oid(value: str):
    """Convert a string id to a bson ObjectId."""
    from bson import ObjectId

    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user id")
