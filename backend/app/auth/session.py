"""
Session revocation store.

Access tokens are JWTs, so by default they stay valid until they expire. To make
logout meaningful ("after logout, protected pages are no longer accessible") each
token carries a unique `jti`; logging out adds that `jti` to the denylist below
and `app.dependencies.auth_deps.get_current_user` refuses it.

Design notes:
  - Entries are keyed by `jti` and hold the token's own expiry timestamp, so the
    store can never grow without bound: expired entries are swept on write.
  - The store is in-process. For a multi-worker / multi-instance deployment
    swap `revoke` / `is_revoked` for a Redis-backed implementation — the rest of
    the codebase only depends on those two functions.
"""

import threading
import time

_lock = threading.Lock()
_revoked: dict[str, float] = {}  # jti -> unix timestamp at which it expires


def revoke(jti: str, expires_at: float) -> None:
    """Block `jti` until its natural expiry (`expires_at` is a unix timestamp)."""
    if not jti or float(expires_at) <= time.time():
        return
    with _lock:
        _sweep_locked()
        _revoked[jti] = float(expires_at)


def is_revoked(jti: str | None) -> bool:
    """Return True when the token id has been revoked and has not yet expired."""
    if not jti:
        # Tokens issued before this feature existed carry no `jti`; they are
        # still signature- and expiry-validated, so they are accepted.
        return False
    with _lock:
        _sweep_locked()
        return jti in _revoked


def _sweep_locked() -> None:
    """Remove entries whose token has expired. Caller must hold the lock."""
    now = time.time()
    for jti, exp in list(_revoked.items()):
        if exp <= now:
            del _revoked[jti]


def clear() -> None:
    """Forget every revocation. Used by tests."""
    with _lock:
        _revoked.clear()
