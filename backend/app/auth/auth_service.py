"""
Auth service layer.

Business logic for registration and login. Kept out of the route handler so it
can be unit-tested and reused (e.g. admin-created users).

Security properties enforced here:
  - Passwords are bcrypt-hashed on the way in and compared with
    `bcrypt.checkpw` on the way in — plaintext is never persisted or logged.
  - The `role` of a self-registered account is hard-coded to `"user"`. A role
    coming from the request body is rejected by the schema *and* ignored here.
  - Login failures are generic ("Invalid credentials") so the endpoint cannot be
    used to enumerate accounts, and repeated failures from the same identifier
    are throttled to slow down brute-force attempts.
"""

import threading
import time
from collections import defaultdict

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.auth.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.utils.logger import get_logger

logger = get_logger(__name__)

# --- Brute-force throttling -------------------------------------------------
_MAX_FAILURES = 8
_LOCKOUT_SECONDS = 60
_FAILURES: dict[str, list[float]] = defaultdict(list)
_fail_lock = threading.Lock()


def _too_many_failures(identifier: str) -> bool:
    """True when `identifier` has failed `_MAX_FAILURES` times recently."""
    now = time.time()
    with _fail_lock:
        attempts = [t for t in _FAILURES[identifier.lower()] if now - t < _LOCKOUT_SECONDS]
        _FAILURES[identifier.lower()] = attempts
        return len(attempts) >= _MAX_FAILURES


def _record_failure(identifier: str) -> None:
    with _fail_lock:
        _FAILURES[identifier.lower()].append(time.time())


def _clear_failures(identifier: str) -> None:
    with _fail_lock:
        _FAILURES.pop(identifier.lower(), None)


class AuthService:
    """Handles user registration, login and account lookup."""

    def __init__(self, users: AsyncIOMotorCollection) -> None:
        self.users = users

    async def register(self, payload: UserCreate) -> UserOut:
        """Create a new user account. The role is always `user`."""
        username = (payload.username or "").strip()
        email = str(payload.email or "").strip().lower()

        # Duplicate checks (unique index is the final safety net).
        clash = await self.users.find_one(
            {"$or": [{"email": email}, {"username": username}]}
        )
        if clash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already registered",
            )

        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            role="user",  # never taken from the request
            is_active=True,
        )
        doc = user.to_doc()
        try:
            result = await self.users.insert_one(doc)
        except Exception as exc:
            # The unique indexes on username/email are the real guard against
            # two simultaneous registrations of the same account.
            if "DuplicateKeyError" in type(exc).__name__:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username or email already registered",
                ) from exc
            raise

        user.id = str(result.inserted_id)

        logger.info("New user registered: %s", user.username)
        return UserOut.from_user(user)

    async def login(self, payload: UserLogin) -> Token:
        """Authenticate by username/email + password and issue a JWT."""
        identifier = payload.identifier.strip()
        if not identifier:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if _too_many_failures(identifier):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed attempts. Please wait a minute and try again.",
            )

        user_doc = await self.users.find_one(
            {
                "$or": [
                    {"email": identifier.lower()},
                    {"username": identifier},
                    {"username": {"$regex": f"^{_escape_regex(identifier)}$", "$options": "i"}},
                ]
            }
        )
        if not user_doc:
            _record_failure(identifier)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        user = User.from_doc(user_doc)
        # Hash even when the account is missing a hash, so a malformed document
        # costs the attacker the same time as a wrong password.
        stored_hash = user.hashed_password if user else ""
        if not user or not verify_password(payload.password, stored_hash):
            _record_failure(identifier)
            logger.info("Failed login attempt for identifier: %s", identifier[:64])
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not user.is_active:
            _record_failure(identifier)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled. Contact an administrator.",
            )

        _clear_failures(identifier)

        from app.utils.jwt_token import create_access_token

        token, expires_in, _jti = create_access_token(user.id, user.role)
        logger.info("User logged in: %s (role=%s)", user.username, user.role)
        return Token(
            access_token=token,
            expires_in=expires_in,
            user=UserOut.from_user(user),
        )


def _escape_regex(value: str) -> str:
    """Escape regex metacharacters so a username is matched literally."""
    import re

    return re.escape(value)
