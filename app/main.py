import structlog
from fastapi import FastAPI

from app.api.routes import health, jobs
from app.config import get_settings

structlog.configure(processors=[structlog.processors.JSONRenderer()])

settings = get_settings()

app = FastAPI(
    title="aazhi-python-backend",
    description="AI indexing and decode worker (internal API)",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(jobs.router, prefix="/v1")


@app.on_event("startup")
def startup() -> None:
    log = structlog.get_logger()
    log.info("startup", env=settings.env, postgres_schema=settings.postgres_schema)
