"""
Pagination dependencies.

Expose `page` and `page_size` query parameters to routes as a tuple.
"""

from fastapi import Query

from app.utils.pagination import DEFAULT_PAGE_SIZE


async def get_pagination(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=100, description="Items per page"),
) -> tuple[int, int]:
    """Return validated (page, page_size)."""
    return page, page_size
