"""
Pagination helpers.

Shared logic for clamping page/page_size and paginating a list of documents.
"""

from typing import Any

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def validate_page_params(page: int, page_size: int) -> tuple[int, int]:
    """Clamp page and page_size to safe, positive bounds."""
    page = max(1, page)
    page_size = min(max(1, page_size), MAX_PAGE_SIZE)
    return page, page_size


async def paginate_async(collection, query: dict[str, Any], page: int, page_size: int, sort: list | None = None):
    """
    Query a Mongo collection with pagination.

    Returns (items, total). sort is a list like [("created_at", -1)].
    """
    page, page_size = validate_page_params(page, page_size)
    cursor = collection.find(query)
    if sort:
        cursor = cursor.sort(sort)
    items = await cursor.skip((page - 1) * page_size).limit(page_size).to_list(length=page_size)
    total = await collection.count_documents(query)
    return items, total
