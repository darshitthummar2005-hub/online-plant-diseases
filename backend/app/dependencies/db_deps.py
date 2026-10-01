"""
Database dependency.

Yields the shared Database wrapper for request handlers. FastAPI calls this per
request; because the underlying Motor client is cached, no new connections are
created.
"""

from typing import AsyncGenerator

from app.database import Database, get_database


async def get_db() -> AsyncGenerator[Database, None]:
    """Provide the application database wrapper to route handlers."""
    yield get_database()
