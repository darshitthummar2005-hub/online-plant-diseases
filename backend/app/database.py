"""
Database module.

Establishes a lazy, async connection to MongoDB using Motor (the async driver).
MongoDB collections used by the application are exposed as typed attributes so
routes/services can do ``await db.users.find_one(...)`` without importing the
driver directly.

Connection lifecycle:
  - The client is created lazily on first access.
  - ``ping_db()`` verifies connectivity at application startup.
  - ``close_db()`` is called on application shutdown to release resources.
"""

import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import get_settings

logger = logging.getLogger(__name__)

_settings = get_settings()

# Lazily-created shared client (None until first access).
_client: AsyncIOMotorClient | None = None


class Database:
    """
    Thin wrapper around the Motor database exposing named collections.

    Each attribute returns the corresponding MongoDB collection so the rest of
    the codebase can rely on consistent collection names.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    # --- Collections (single source of truth for collection names) ---
    @property
    def users(self):
        return self._db["users"]

    @property
    def plant_diseases(self):
        return self._db["plant_diseases"]

    @property
    def predictions(self):
        return self._db["predictions"]

    @property
    def uploaded_images(self):
        return self._db["uploaded_images"]

    @property
    def feedback(self):
        return self._db["feedback"]

    @property
    def raw(self) -> AsyncIOMotorDatabase:
        """Access the raw database object when needed (indexes, etc.)."""
        return self._db


def get_client() -> AsyncIOMotorClient:
    """Create (once) and return the async MongoDB client."""
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(_settings.mongo_uri, serverSelectionTimeoutMS=5000)
        logger.info("Created MongoDB client for %s", _settings.mongo_uri)
    return _client


def get_database() -> Database:
    """Return the application Database wrapper (creates the client if needed)."""
    client = get_client()
    return Database(client[_settings.mongo_db_name])


async def ping_db() -> bool:
    """
    Check MongoDB connectivity.

    Sends a ping command and returns True on success. Logs and re-raises any
    connection error so startup can fail fast with a clear message.
    """
    client = get_client()
    try:
        await client.admin.command("ping")
        logger.info("MongoDB ping OK")
        return True
    except Exception as exc:  # pragma: no cover - depends on external service
        logger.error("MongoDB ping failed: %s", exc)
        raise


async def close_db() -> None:
    """Close the shared MongoDB client during application shutdown."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        logger.info("Closed MongoDB client")


async def ensure_indexes() -> None:
    """
    Create the indexes required by the application.

    Called once at startup. Indexes speed up logins, searches and history
    lookups, and the unique index on user email enforces duplicate prevention.
    """
    db = get_database()

    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)

    await db.plant_diseases.create_index([("name", 1)], unique=True)
    await db.plant_diseases.create_index([("category", 1)])

    await db.predictions.create_index([("user_id", 1), ("created_at", -1)])
    await db.predictions.create_index([("disease_id", 1)])

    await db.uploaded_images.create_index([("user_id", 1), ("uploaded_at", -1)])

    await db.feedback.create_index([("user_id", 1), ("created_at", -1)])
    await db.feedback.create_index([("rating", 1)])

    logger.info("MongoDB indexes ensured")
