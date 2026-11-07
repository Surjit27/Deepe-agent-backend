"""LLM decode stub — wire OpenAI / Gemini using per-job keys from Node."""

from dataclasses import dataclass

from app.contracts.jobs import DecodeJobRequest, SymbolSummary


@dataclass
class DecodeResult:
    summaries: list[SymbolSummary]
    prompt_tokens: int
    completion_tokens: int


def run_decode_stub(body: DecodeJobRequest) -> DecodeResult:
    if body.provider == "openai" and not (body.openai_api_key or _env_openai()):
        pass
    if body.provider == "gemini" and not (body.google_api_key or _env_google()):
        pass

    return DecodeResult(
        summaries=[
            SymbolSummary(
                node_id=f"{body.backend_id}:health",
                summary="Public health probe; no auth. (stub — connect LLM next.)",
            )
        ],
        prompt_tokens=0,
        completion_tokens=0,
    )


def _env_openai() -> bool:
    from app.config import get_settings

    return bool(get_settings().openai_api_key)


def _env_google() -> bool:
    from app.config import get_settings

    return bool(get_settings().google_api_key)
