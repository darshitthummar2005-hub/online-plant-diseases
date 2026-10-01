"""
Password hashing helpers.

Wraps bcrypt so password security logic lives in one place. bcrypt's 72-byte
limit is respected by truncating to 72 bytes before hashing.
"""

import bcrypt

from app.utils.logger import get_logger

logger = get_logger(__name__)


def hash_password(password: str) -> str:
    """Return a bcrypt hash for the given plaintext password."""
    password_bytes = password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Returns False (instead of raising) on any mismatch or malformed hash.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72],
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError) as exc:
        logger.warning("Password verification failed: %s", exc)
        return False
