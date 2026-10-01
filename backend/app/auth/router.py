"""
Auth routes.

Endpoints:
  POST   /auth/register   - create an account (role is always `user`)
  POST   /auth/login      - authenticate and receive a JWT
  GET    /auth/me         - current user profile (protected)
  POST   /auth/logout     - revoke the current token (protected)
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth import session
from app.auth.auth_service import AuthService
from app.auth.security import decode_token
from app.dependencies.auth_deps import get_current_user
from app.dependencies.db_deps import get_db
from app.database import Database
from app.schemas.common import Message
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

_bearer = HTTPBearer(auto_error=True, description="JWT returned by POST /auth/login")


def get_auth_service(db: Database = Depends(get_db)) -> AuthService:
    """FastAPI dependency providing an AuthService bound to the users collection."""
    return AuthService(db.users)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Create a user account with a full name, a username and/or email and a "
        "password. New accounts always receive the `user` role."
    ),
)
async def register(payload: UserCreate, service: AuthService = Depends(get_auth_service)):
    """Create a new user account."""
    return await service.register(payload)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate with username/email and password. Returns a JWT.",
)
async def login(payload: UserLogin, service: AuthService = Depends(get_auth_service)):
    """Login and receive an access token."""
    return await service.login(payload)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    description="Return the profile of the authenticated user.",
)
async def me(user: UserOut = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return user


@router.post(
    "/logout",
    response_model=Message,
    summary="Logout",
    description="Revoke the access token used for this request so it cannot be reused.",
)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    """
    Revoke the presented access token.

    The `jti` is added to the denylist until its natural expiry, so any copy of
    this token stops working immediately — a real server-side logout rather than
    a client-side token delete.
    """
    payload = decode_token(credentials.credentials)
    session.revoke(payload.get("jti", ""), payload.get("exp", 0))
    logger.info("Token revoked for user: %s", payload.get("sub"))
    return Message(detail="Signed out successfully")
