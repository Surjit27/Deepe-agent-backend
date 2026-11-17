from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import ApiTokenProvider
from app.lib.secret_box import decrypt_secret, encrypt_secret
from app.providers.catalog import API_TOKEN_PROVIDER_TYPES, PROVIDER_IDS


def _env_key_for(provider: str) -> str:
    row = next((t for t in API_TOKEN_PROVIDER_TYPES if t["id"] == provider), None)
    if not row:
        return ""
    return getattr(get_settings(), f"{provider}_api_key", "") or get_settings().model_dump().get(row["env_key"].lower(), "")


def _resolved_key(row: ApiTokenProvider) -> tuple[str, str]:
    saved = decrypt_secret(row.api_key_cipher)
    if saved:
        return saved, "saved"
    settings = get_settings()
    env_map = {
        "openai": settings.openai_api_key,
        "gemini": settings.google_api_key,
        "anthropic": settings.anthropic_api_key,
        "cursor": settings.cursor_api_key,
        "cerebras": settings.cerebras_api_key,
        "groq": settings.groq_api_key,
        "mistral": settings.mistral_api_key,
        "openrouter": settings.openrouter_api_key,
    }
    env_val = env_map.get(row.provider, "")
    if env_val:
        return env_val, "env"
    return "", "none"


def _mask_key(api_key: str) -> str | None:
    if not api_key:
        return None
    if len(api_key) <= 8:
        return "•" * len(api_key)
    return f"{'•' * 12}{api_key[-4:]}"


def to_public(row: ApiTokenProvider) -> dict[str, Any]:
    meta = next((t for t in API_TOKEN_PROVIDER_TYPES if t["id"] == row.provider), None)
    key, source = _resolved_key(row)
    return {
        "id": str(row.id),
        "provider": row.provider,
        "providerLabel": meta["label"] if meta else row.provider,
        "freeAllowance": meta["free_allowance"] if meta else "",
        "bestFor": meta["best_for"] if meta else "",
        "name": row.name,
        "status": row.status,
        "baseUrl": row.base_url,
        "isDefault": row.is_default,
        "apiKeySet": source != "none",
        "apiKeySource": source,
        "apiKeyMasked": _mask_key(key),
        "apiKeySavedInDatabase": bool(row.api_key_cipher),
        "storageSchema": "ai",
        "storageTable": "api_token_providers",
        "updatedAt": row.updated_at.isoformat() if row.updated_at else None,
        "createdAt": row.created_at.isoformat() if row.created_at else None,
    }


def list_providers(db: Session) -> list[dict[str, Any]]:
    rows = db.query(ApiTokenProvider).order_by(ApiTokenProvider.provider, ApiTokenProvider.is_default.desc()).all()
    return [to_public(r) for r in rows]


def get_provider(db: Session, provider_id: str) -> ApiTokenProvider | None:
    return db.get(ApiTokenProvider, provider_id)


def create_provider(db: Session, body: dict[str, Any]) -> dict[str, Any]:
    provider = str(body.get("provider", "")).strip().lower()
    if provider not in PROVIDER_IDS:
        raise ValueError("Unsupported provider")
    meta = next(t for t in API_TOKEN_PROVIDER_TYPES if t["id"] == provider)
    name = str(body.get("name", "")).strip() or meta["label"]
    status = "active" if body.get("status") == "active" else "inactive"
    is_default = bool(body.get("isDefault"))
    if is_default:
        db.query(ApiTokenProvider).filter(ApiTokenProvider.provider == provider).update({"is_default": False})
    row = ApiTokenProvider(
        provider=provider,
        name=name,
        status=status,
        base_url=str(body.get("baseUrl", "")).strip(),
        is_default=is_default or db.query(ApiTokenProvider).filter(ApiTokenProvider.provider == provider).count() == 0,
    )
    api_key = str(body.get("apiKey", "")).strip()
    if api_key:
        row.api_key_cipher = encrypt_secret(api_key)
    db.add(row)
    db.commit()
    db.refresh(row)
    return to_public(row)


def patch_provider(db: Session, provider_id: str, body: dict[str, Any]) -> dict[str, Any]:
    row = get_provider(db, provider_id)
    if not row:
        raise LookupError("API token provider not found")
    if body.get("name") is not None:
        row.name = str(body["name"]).strip()
    if body.get("status") is not None:
        row.status = "active" if body["status"] == "active" else "inactive"
    if body.get("baseUrl") is not None:
        row.base_url = str(body["baseUrl"]).strip()
    if body.get("isDefault") is True:
        db.query(ApiTokenProvider).filter(ApiTokenProvider.provider == row.provider).update({"is_default": False})
        row.is_default = True
    if body.get("apiKey") is not None:
        api_key = str(body["apiKey"]).strip()
        if api_key:
            row.api_key_cipher = encrypt_secret(api_key)
    db.commit()
    db.refresh(row)
    return to_public(row)


def delete_provider(db: Session, provider_id: str) -> None:
    row = get_provider(db, provider_id)
    if not row:
        raise LookupError("API token provider not found")
    db.delete(row)
    db.commit()