"""
Configuration module.

Centralises all runtime settings (server, CORS, MongoDB, JWT, uploads) loaded
from environment variables / the `.env` file. Uses Pydantic Settings so values
are validated and typed at startup, failing fast on misconfiguration.
"""

import json
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Typed application settings, read from environment variables."""

    # --- Server ---
    app_name: str = "GreenRoot API"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # --- CORS ---
    # Comma separated list parsed into a list by a property below.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- MongoDB ---
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "greenroot_db"

    # --- JWT ---
    secret_key: str = "change-me-to-a-long-random-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # --- File uploads ---
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 5

    # --- Optional default admin (created on first boot by app/seed.py) ---
    admin_username: str = ""
    admin_email: str = ""
    admin_password: str = ""

    # --- Optional extra admin accounts, as a JSON array string ---
    # Lets the deployment own more than one administrator without code changes.
    # Credentials stay in `.env` (git-ignored) instead of living in source.
    # Example:
    #   ADMIN_ACCOUNTS=[{"username":"nilesh","email":"nilesh@x.dev","password":"..."}]
    admin_accounts: str = ""

    # Locations of .env files to read (highest priority = current dir).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse the comma-separated CORS string into a Python list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def admin_accounts_list(self) -> list[dict[str, str]]:
        """
        Parse ADMIN_ACCOUNTS into a list of admin account dicts.

        Never raises: a malformed value is logged and ignored so a typo in
        `.env` cannot stop the API from booting.
        """
        raw = (self.admin_accounts or "").strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            logger.error("ADMIN_ACCOUNTS is not valid JSON; ignoring it")
            return []
        if not isinstance(parsed, list):
            logger.error("ADMIN_ACCOUNTS must be a JSON array; ignoring it")
            return []
        return [item for item in parsed if isinstance(item, dict)]

    @property
    def max_upload_size_bytes(self) -> int:
        """Upload limit expressed in bytes."""
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Cached so that every module shares the same settings object (and the .env
    file is only parsed once per process).
    """
    return Settings()
