"""
Admin schemas.

Request/response models for the admin dashboard: user management, platform
statistics and detection-record listings.

Every payload here is only reachable through endpoints guarded by
`get_current_admin`, and `AdminUserUpdate` refuses to change anything except the
explicitly allowed fields (`extra="forbid"`).
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.user import UserOut


class AdminUserUpdate(BaseModel):
    """
    Payload for PATCH /admin/users/{id}.

    Admins may rename an account, change its role and enable/disable it. They may
    not touch the username, email or password through this endpoint — those are
    changed by the account owner or by the `scripts/create_admin.py` CLI so that
    privilege changes always have a single, auditable path.
    """

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, max_length=100)
    role: Literal["user", "admin"] | None = None
    is_active: bool | None = None

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = " ".join(value.split())
        return value or None


class AdminUserOut(UserOut):
    """A user row in the admin table — same fields, documented separately."""

    updated_at: datetime | None = None


class AdminStats(BaseModel):
    """Headline counters for the admin dashboard overview."""

    total_users: int
    active_users: int
    disabled_users: int
    total_admins: int
    new_users_7d: int
    total_diseases: int
    total_predictions: int
    total_feedback: int
    average_rating: float
    detections_7d: int


class DetectionOut(BaseModel):
    """One row in the admin detections table."""

    id: str
    user_id: str
    username: str | None = None
    disease_name: str
    confidence: float
    severity: str | None = None
    plant: str | None = None
    status: str
    symptoms: list[str] = Field(default_factory=list)
    predicted_at: datetime


class CategoryCount(BaseModel):
    """A label/value pair used for the simple bar charts on the overview."""

    label: str
    count: int


class ActivityOut(BaseModel):
    """A single entry in the overview's recent-activity feed."""

    kind: Literal["user", "detection"]
    title: str
    detail: str | None = None
    at: datetime
