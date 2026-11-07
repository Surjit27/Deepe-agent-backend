from fastapi import Header, HTTPException

from app.config import get_settings


def require_internal_key(x_internal_key: str | None = Header(default=None, alias="X-Internal-Key")) -> None:
    expected = get_settings().internal_api_key
    if not x_internal_key or x_internal_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Internal-Key")
