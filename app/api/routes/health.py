from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    s = get_settings()
    return {"ok": True, "service": "aazhi-python-backend", "postgres_schema": s.postgres_schema}
