"""Static index stub — replace with git clone + tree-sitter / route parsers."""

from app.contracts.graph import GraphEdge, GraphEdgeKind, GraphNode, GraphNodeKind, GraphSnapshot
from app.contracts.jobs import IndexJobRequest


def run_static_index(req: IndexJobRequest) -> GraphSnapshot:
    """Placeholder graph so Node can integrate before real parsers land."""
    entry = GraphNode(
        id=f"{req.backend_id}:health",
        kind=GraphNodeKind.endpoint,
        label="GET /api/health",
        file="src/routes/health.routes.js",
        line=1,
        method="GET",
        path="/api/health",
        description="Placeholder endpoint from Python indexer stub.",
    )
    handler = GraphNode(
        id=f"{req.backend_id}:health-handler",
        kind=GraphNodeKind.function,
        label="healthCheck",
        file="src/routes/health.routes.js",
        line=5,
        description="Handler stub for integration testing.",
    )
    edge = GraphEdge(
        id=f"{req.backend_id}:e1",
        kind=GraphEdgeKind.calls,
        source_id=entry.id,
        target_id=handler.id,
        label="dispatches",
    )
    return GraphSnapshot(
        backend_id=req.backend_id,
        client_user_id=req.client_user_id,
        commit_sha=req.commit_sha or "",
        nodes=[entry, handler],
        edges=[edge],
    )
