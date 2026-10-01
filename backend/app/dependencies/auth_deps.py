"""
Authentication & authorization dependencies.

`get_current_user` decodes the JWT, rejects revoked tokens, reloads the user from
MongoDB and returns a UserOut.
`get_current_admin` additionally requires role == "admin".

The role is always read from the *database*, never from the token claim, so a
client cannot escalate privileges by crafting a token. Admin APIs are protected
by these dependencies server-side — hiding the UI is only a convenience.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt

from app.auth import session
from app.auth.security import decode_token
from app.database import Database
from app.dependencies.db_deps import get_db
from app.models.user import User
from app.schemas.user import UserOut
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Auto-documents the `Authorization: Bearer <token>` header in OpenAPI.
_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Database = Depends(get_db),
) -> UserOut:
    """
    Resolve the authenticated user from the JWT.

    Raises 401 when the token is missing, invalid, expired, revoked, or the user
    no longer exists / is disabled.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if session.is_revoked(payload.get("jti")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ended, please sign in again",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    user_doc = await db.users.find_one({"_id": __oid(user_id)}) if user_id else None
    if not user_doc:
        raise HTTPException(status_code=401, detail="User not found")

    user = User.from_doc(user_doc)
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    return UserOut.from_user(user)


async def get_current_admin(user: UserOut = Depends(get_current_user)) -> UserOut:
    """
    Require the current user to be an admin.

    Depends on `get_current_user`, so the identity is already proven against the
    database; only the stored role is checked here.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user


def __oid(value: str):
    """Convert a string id to a bson ObjectId, tolerating malformed input."""
    from bson import ObjectId

    try:
        return ObjectId(value)
    except Exception:
        return value
