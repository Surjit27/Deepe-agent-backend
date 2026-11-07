from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GraphNodeKind(str, Enum):
    endpoint = "endpoint"
    middleware = "middleware"
    controller = "controller"
    service = "service"
    function = "function"
    module = "module"
    external = "external"


class GraphEdgeKind(str, Enum):
    calls = "CALLS"
    imports = "IMPORTS"
    http_to = "HTTP_TO"
    reads_db = "READS_DB"
    publishes = "PUBLISHES"
    consumes = "CONSUMES"


class GraphNode(BaseModel):
    id: str
    kind: GraphNodeKind
    label: str
    file: str | None = None
    line: int | None = None
    method: str | None = None
    path: str | None = None
    description: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    kind: GraphEdgeKind
    source_id: str
    target_id: str
    label: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphSnapshot(BaseModel):
    """Returned to Node after index; Node persists to public graph tables."""

    backend_id: str
    client_user_id: str
    commit_sha: str = ""
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
