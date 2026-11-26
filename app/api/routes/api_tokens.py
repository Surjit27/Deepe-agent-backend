from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_internal_key
from app.db.session import get_db
from app.providers.catalog import API_TOKEN_PROVIDER_TYPES
from app.services import api_token_providers as svc

router = APIRouter(tags=["api-tokens"], dependencies=[Depends(require_internal_key)])


@router.get("/settings/api-token-types")
def list_types() -> dict:
    return {"types": API_TOKEN_PROVIDER_TYPES, "storageSchema": "ai", "storageTable": "api_token_providers"}


@router.get("/settings/api-tokens")
def list_tokens(db: Session = Depends(get_db)) -> dict:
    return {"providers": svc.list_providers(db)}


@router.post("/settings/api-tokens", status_code=201)
def create_token(body: dict, db: Session = Depends(get_db)) -> dict:
    try:
        return {"provider": svc.create_provider(db, body)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/settings/api-tokens/{provider_id}")
def get_token(provider_id: str, db: Session = Depends(get_db)) -> dict:
    row = svc.get_provider(db, provider_id)
    if not row:
        raise HTTPException(status_code=404, detail="API token provider not found")
    return {"provider": svc.to_public(row)}


@router.patch("/settings/api-tokens/{provider_id}")
def patch_token(provider_id: str, body: dict, db: Session = Depends(get_db)) -> dict:
    try:
        return {"provider": svc.patch_provider(db, provider_id, body)}
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/settings/api-tokens/{provider_id}")
def delete_token(provider_id: str, db: Session = Depends(get_db)) -> dict:
    try:
        svc.delete_provider(db, provider_id)
        return {"ok": True}
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc