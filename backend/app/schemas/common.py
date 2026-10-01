"""
Common schemas.

Shared response wrappers (message, pagination) used across endpoints.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Message(BaseModel):
    """Simple success/error message body."""

    detail: str


class Page(BaseModel, Generic[T]):
    """
    Generic paginated response.

    Usage: Page[UserOut], Page[DiseaseOut], ...
    """

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int, page_size: int) -> "Page[T]":
        """Create a Page instance computing the total number of pages."""
        pages = (total + page_size - 1) // page_size if page_size else 0
        return cls(items=items, total=total, page=page, page_size=page_size, pages=pages)
