"""
JWT helpers.

Create and validate HS256 access tokens. Tokens carry the user id (`sub`), the
role, a unique token id (`jti`) and an expiry so that:

  - role checks do not require a database hit, and
  - a token can be individually revoked on logout (see `app.auth.session`).
"""

import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
_settings = get_settings()


def create_access_token(subject: str, role: str) -> tuple[str, int, str]:
    """
    Create a signed JWT.

    Returns ``(token, expires_in_seconds, jti)``. The caller stores the ``jti``
    inside the token so `app.auth.session` can revoke it on logout.
    """
    now = datetime.now(timezone.utc)
    expires_in = _settings.access_token_expire_minutes * 60
    jti = uuid.uuid4().hex
    payload = {
        "sub": subject,
        "role": role,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
    }
    token = jwt.encode(payload, _settings.secret_key, algorithm=_settings.jwt_algorithm)
    return token, expires_in, jti


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT.

    Raises jwt.PyJWTError on invalid/expired tokens so the auth dependency can
    translate it into a clean 401.
    """
    return jwt.decode(
        token,
        _settings.secret_key,
        algorithms=[_settings.jwt_algorithm],
    )
