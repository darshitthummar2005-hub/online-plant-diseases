"""
User document model.

Stored in the `users` collection. Only the hashed password is persisted - the
raw password is never stored or returned by the API.
"""

from typing import Literal

from pydantic import EmailStr, Field

from app.models.base import MongoModel


class User(MongoModel):
    """A registered user of the portal."""

    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    hashed_password: str
    full_name: str | None = None
    role: Literal["user", "admin"] = "user"
    is_active: bool = True
