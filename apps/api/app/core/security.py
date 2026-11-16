import hmac
import time

from fastapi import Header, HTTPException

from app.core.config import settings

_last_run = 0.0


def admin_only(x_admin_key: str = Header(default="")):
    # constant-time compare; an empty configured key disables the endpoint entirely
    if not settings.api_admin_key or not hmac.compare_digest(x_admin_key, settings.api_admin_key):
        raise HTTPException(401, "admin key required")


def cooldown():
    """Run-now starts billable compute, so it is rate limited."""
    global _last_run
    wait = settings.run_now_cooldown_seconds - (time.time() - _last_run)
    if wait > 0:
        raise HTTPException(429, f"try again in {int(wait)} seconds")
    _last_run = time.time()
