"""
User & auth schemas.

Request/response models for registration, login, profile management and tokens.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.models.user import User

# A username may only contain letters, digits and underscores.
USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"


# ---------- Request bodies ----------
class UserCreate(BaseModel):
    """
    Payload for POST /auth/register.

    The sign-up form collects a full name, *either* a username or an email (or
    both) and a password. The missing identifier is derived from the other one
    so the stored document always has a unique username + email pair.

    `extra="forbid"` is deliberate: it means a client cannot smuggle a `role`
    field (or any other unexpected key) into the payload. Role assignment is a
    server-side decision only — see `AuthService.register`.
    """

    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=USERNAME_PATTERN,
        description="Optional unique username. Derived from the email when omitted.",
    )
    email: EmailStr | None = Field(
        default=None,
        description="Optional unique email. Derived from the username when omitted.",
    )
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=100)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        """Enforce a minimum password strength rule."""
        if not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one uppercase letter and one digit")
        return value

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str | None) -> str | None:
        """Collapse surrounding whitespace; treat blank as absent."""
        if value is None:
            return None
        value = " ".join(value.split())
        return value or None

    @model_validator(mode="after")
    def fill_missing_identifier(self) -> "UserCreate":
        """
        Require at least one identifier and derive the other from it.

        A username that is already an email address is promoted to the email
        field, so `{"username": "a@b.com"}` works just like
        `{"email": "a@b.com"}`.
        """
        if self.username and not self.email and "@" in self.username:
            # `username` looks like an email -> treat it as the email.
            self.email, self.username = self.username, None
            return self

        if not self.username and not self.email:
            raise ValueError("Provide a username or an email address")

        if not self.username and self.email:
            derived = self.email.split("@")[0]
            # Strip characters the username pattern disallows, then pad/trim
            # so the 3..30 length rule still holds.
            derived = "".join(c for c in derived if c.isalnum() or c == "_")[:30]
            if len(derived) < 3:
                derived = f"user{derived}"
            self.username = derived

        if not self.email and self.username:
            self.email = f"{self.username.lower()}@users.onlineplantdiseases.local"

        return self


class UserLogin(BaseModel):
    """Payload for POST /auth/login (username or email + password)."""

    model_config = ConfigDict(extra="forbid")

    identifier: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=128)


class UserUpdate(BaseModel):
    """Payload for PATCH /users/me."""

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = " ".join(value.split())
        return value or None

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str | None) -> str | None:
        """Mirror the registration rule for self-service password changes."""
        if value is None:
            return None
        if not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one uppercase letter and one digit")
        return value


# ---------- Responses ----------
class UserOut(BaseModel):
    """Public user profile (never exposes password)."""

    id: str
    username: str
    email: EmailStr
    full_name: str | None = None
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserOut":
        """Build from a User model."""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )


class Token(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut


class TokenPayload(BaseModel):
    """Decoded JWT payload shape."""

    sub: str  # user id
    role: str
    exp: int
