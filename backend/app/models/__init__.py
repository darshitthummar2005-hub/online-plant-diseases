"""
Domain models package.

Pydantic models mirroring MongoDB documents. They give type safety and
validation without requiring an ODM (we use Motor directly for queries).
"""

from app.models.base import MongoModel  # noqa: F401
