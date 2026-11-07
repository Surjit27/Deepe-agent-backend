from typing import Literal

from pydantic import BaseModel, Field

from app.contracts.graph import GraphSnapshot


class IndexJobRequest(BaseModel):
    index_run_id: str
    client_user_id: str
    backend_id: str
    repository: str
    branch: str = "main"
    commit_sha: str | None = None
    clone_url: str | None = None
    architecture: str = "node-express"


class IndexJobResponse(BaseModel):
    job_id: str
    status: str
    graph: GraphSnapshot


class DecodeJobRequest(BaseModel):
    index_run_id: str
    client_user_id: str
    backend_id: str
    provider: Literal["openai", "gemini"] = "openai"
    model: str | None = None
    openai_api_key: str | None = None
    google_api_key: str | None = None


class SymbolSummary(BaseModel):
    node_id: str
    summary: str


class DecodeJobResponse(BaseModel):
    job_id: str
    status: str
    summaries: list[SymbolSummary] = Field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0
