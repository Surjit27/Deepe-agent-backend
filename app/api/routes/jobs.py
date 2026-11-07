import structlog
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_internal_key
from app.contracts.jobs import DecodeJobRequest, DecodeJobResponse, IndexJobRequest, IndexJobResponse
from app.db.models import DecodeJob, IndexJob
from app.db.session import get_db
from app.services.indexer import run_static_index
from app.services.llm_decode import run_decode_stub

router = APIRouter(tags=["jobs"], dependencies=[Depends(require_internal_key)])
log = structlog.get_logger()


@router.post("/jobs/index", response_model=IndexJobResponse)
def create_index_job(body: IndexJobRequest, db: Session = Depends(get_db)) -> IndexJobResponse:
    row = IndexJob(
        index_run_id=body.index_run_id,
        client_user_id=body.client_user_id,
        backend_id=body.backend_id,
        repository=body.repository,
        branch=body.branch,
        commit_sha=body.commit_sha or "",
        status="running",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    log.info("index_job_started", index_run_id=body.index_run_id, backend_id=body.backend_id)
    snapshot = run_static_index(body)
    row.status = "succeeded"
    row.node_count = len(snapshot.nodes)
    row.edge_count = len(snapshot.edges)
    db.commit()

    return IndexJobResponse(job_id=str(row.id), status=row.status, graph=snapshot)


@router.post("/jobs/decode", response_model=DecodeJobResponse)
def create_decode_job(body: DecodeJobRequest, db: Session = Depends(get_db)) -> DecodeJobResponse:
    row = DecodeJob(
        index_run_id=body.index_run_id,
        client_user_id=body.client_user_id,
        backend_id=body.backend_id,
        provider=body.provider,
        status="running",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    result = run_decode_stub(body)
    row.status = "succeeded"
    row.prompt_tokens = result.prompt_tokens
    row.completion_tokens = result.completion_tokens
    db.commit()

    return DecodeJobResponse(
        job_id=str(row.id),
        status=row.status,
        summaries=result.summaries,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
    )
