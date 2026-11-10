# Python-backend (Aazhi AI worker)

FastAPI service for **git indexing**, **static graph extraction**, and **LLM decode** (OpenAI / Gemini). It does **not** handle portal login or JWT — the Node `backend/` orchestrates jobs and persists the canonical portal graph.

## Layout

| Path | Purpose |
|------|---------|
| `app/` | FastAPI app, workers, indexers (stubs for now) |
| `app/contracts/` | **API contract** (Pydantic) shared with Node via HTTP JSON |
| `app/db/` | SQLAlchemy models in Postgres schema `ai` |
| `alembic/` | Migrations for schema `ai` only |
| `docs/SCHEMA_ARCHITECTURE.md` | How `public` vs `ai` vs `client_*` schemas fit together |

## Quick start

```bash
cd Python-backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Postgres from backend/: docker compose up -d postgres mongo
alembic upgrade head
uvicorn app.main:app --reload --port 4100
```

- Health: http://localhost:4100/health  
- OpenAPI: http://localhost:4100/docs  

Call internal routes with header `X-Internal-Key: <INTERNAL_API_KEY>`.

## Docker

```bash
docker compose up --build
```

Runs on port **4100** and expects Postgres/Mongo/Redis from the Node stack:

```bash
cd ../backend && docker compose up -d postgres mongo redis
```

## Node integration (summary)

1. Node creates a backend row + `IndexRun` in **`public`** (Prisma).
2. BullMQ job `index-backend` → HTTP `POST /v1/jobs/index` to this service.
3. Python writes progress to **`ai.index_jobs`**, artifacts to **Mongo**, returns `GraphSnapshot` JSON.
4. Node merges snapshot into portal tables (future Prisma models) and updates UI.

See [docs/SCHEMA_ARCHITECTURE.md](docs/SCHEMA_ARCHITECTURE.md) for the full database split.
