"""
Base model.

Every stored document extends MongoModel so that:
  - `_id` from MongoDB maps to the `id` field.
  - conversion to/from MongoDB documents is centralised.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MongoModel(BaseModel):
    """Base Pydantic model for MongoDB documents."""

    # Map MongoDB's `_id` onto our `id` field while allowing `id` by name too.
    id: str | None = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )

    @field_validator("id", mode="before")
    @classmethod
    def _coerce_object_id(cls, value: Any) -> Any:
        """Convert bson ObjectId to str so documents validate cleanly."""
        if value is not None:
            try:
                from bson import ObjectId

                if isinstance(value, ObjectId):
                    return str(value)
            except ImportError:  # pragma: no cover
                pass
        return value

    @classmethod
    def from_doc(cls, doc: dict[str, Any] | None) -> "MongoModel | None":
        """Build a model instance from a raw MongoDB document."""
        if doc is None:
            return None
        return cls(**doc)

    def to_doc(self, exclude_unset: bool = False) -> dict[str, Any]:
        """
        Serialize to a MongoDB-ready document.

        Converts the string `id` back into an ObjectId when present, and strips
        the None id so MongoDB can generate it.
        """
        from bson import ObjectId
        from pydantic import TypeAdapter

        data = self.model_dump(exclude={"id"}, exclude_unset=exclude_unset)
        if self.id:
            data["_id"] = TypeAdapter(ObjectId).validate_python(self.id)
        return data
