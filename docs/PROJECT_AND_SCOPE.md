# Deepe (Aazhi) — project & scope

**Deepe** is a multi-portal product for understanding and operating connected software backends: Git-linked **repo indexing**, **static graph extraction**, and **LLM-assisted decode**. The public name is **Deepe**; GitHub repositories use the **Aazhi** naming prefix.

This document describes the **whole system** and the **scope of this repository** (the FastAPI **internal** AI worker).

## Three repositories (no parent git repo)

The product is split across three independent repos. On disk they often live as siblings under a local folder (for example `Personal projects/Aazhi/`); there is **no** umbrella git repository—clone and version each repo separately.

| Repository | GitHub | Runtime | Default port |
|------------|--------|---------|--------------|
| **Frontend** | [Surjit27/Aazhi](https://github.com/Surjit27/Aazhi) | React 18 + Vite | 5173 |
| **Node backend** | [Surjit27/Aazhi-js-backend](https://github.com/Surjit27/Aazhi-js-backend) | Express + Prisma | 4000 |
| **Python backend** (this repo) | [Surjit27/Deepe-agent-backend](https://github.com/Surjit27/Deepe-agent-backend) | FastAPI (internal) | 4100 |

Related docs in the other repos:

- Frontend: `Frontend/docs/PROJECT_AND_SCOPE.md`
- Node: `backend/docs/PROJECT_AND_SCOPE.md` and `backend/README.md`
- Database split (detail): [SCHEMA_ARCHITECTURE.md](./SCHEMA_ARCHITECTURE.md)

## System architecture (high level)

```text
                    ┌─────────────────────────────────────┐
                    │  Browsers (hostname-based portals)   │
                    │  home · client · admin @ :5173      │
                    └──────────────────┬──────────────────┘
                                       │ JWT to Node only
                                       ▼
                    ┌─────────────────────────────────────┐
                    │  Node API                           │
                    │  Creates index_run / backend IDs      │
                    └──────────┬──────────────────────────┘
                               │ POST /v1/jobs/* + X-Internal-Key
                               ▼
                    ┌─────────────────────────────────────┐
                    │  Python-backend (this repo)         │
                    │  Clone · index · graph · LLM decode │
                    │  ai schema · Mongo ai_* artifacts   │
                    └─────────────────────────────────────┘
```

Browsers and the Frontend **never** call this service directly in production shape; only **Node** (or operators via curl) use the internal API.

## This repo: Python backend — responsibilities

### In scope

- **FastAPI** app on port **4100**: health, **`/v1/jobs/index`** (and decode routes as added).
- **Pydantic contracts** in `app/contracts/` (`GraphSnapshot`, job request/response) — versioned HTTP JSON shared with Node.
- **PostgreSQL `ai` schema** via **Alembic** (`index_jobs`, `decode_jobs`, `llm_usage`, …).
- **MongoDB** collections prefixed `ai_` (repo snapshots, symbol snippets for RAG).
- **Workers**: git indexing, static graph extraction, optional **OpenAI / Gemini** decode passes.
- **structlog** JSON logging; configuration via `.env` / `app/config.py`.
- Docker image that expects Postgres/Mongo/Redis from the Node stack’s Compose file.

### Out of scope

- Portal **login**, JWT, user management → **Node**.
- **Prisma** or migrations on **`public`** / **`client_*`** → **Node**.
- Rendering UI or serving the client SPA → **Frontend**.
- Inventing `backendId` / `indexRunId` — Node assigns IDs; Python only processes them.

### Security model

- Requests authenticated with **`X-Internal-Key`** (`INTERNAL_API_KEY`), not end-user JWT.
- **LLM API keys** are not stored in `ai` tables; Node passes short-lived keys per job or omits them to skip LLM steps.

### Local dev (this repo)

```bash
cd Python-backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
cd ../backend && docker compose up -d postgres mongo redis
cd ../Python-backend && alembic upgrade head
uvicorn app.main:app --reload --port 4100
```

OpenAPI: http://localhost:4100/docs

## Product scope (cross-cutting)

### Currently implemented / active themes

- Service **scaffold**: health, jobs router, DB models, Alembic bootstrap for `ai` schema.
- Documented **Node ↔ Python** handoff and identity fields (see [SCHEMA_ARCHITECTURE.md](./SCHEMA_ARCHITECTURE.md)).
- Provider hooks under `app/providers/` for future OpenAI/Gemini usage.

### Planned / in progress

- Full **clone + static index** pipeline and durable progress in `ai.index_jobs`.
- Returning production-quality **`GraphSnapshot`** payloads for Node to persist in `public`.
- **Decode** jobs and token accounting in `llm_usage`.

### Explicit non-goals (for now)

- Public-facing OAuth or CORS for browser clients.
- Owning canonical graph rows the UI reads (Node merges into `public`).
- Alembic changes outside schema **`ai`**.

## How to work across repos

1. Change a job payload → edit `app/contracts/`, bump handler, update Node HTTP client, then Frontend if exposed.
2. New `ai` table → Alembic revision here only.
3. New portal-visible entity → Node Prisma/SQL + API; Python only references IDs.

## Documentation map

| Document | Where |
|----------|--------|
| **Project & scope** (this file) | `docs/PROJECT_AND_SCOPE.md` in each of the three repos |
| **Postgres / Mongo split, job handoff** | [SCHEMA_ARCHITECTURE.md](./SCHEMA_ARCHITECTURE.md) |
| **Runbooks** | Each repo’s `README.md` |

When system scope changes, update the matching sections in **all three** `PROJECT_AND_SCOPE.md` copies and bump the *Last updated* line below.

## Local Git identity (Aazhi clones only)

The three repos are often siblings under one folder (for example `Personal projects/Aazhi/`). Use **repo-local** Git config in each clone so other folders on the machine keep their own `user.name` / `user.email`:

```bash
cd Python-backend   # repeat in Frontend/ and backend/
git config user.name "Surjit27"
git config user.email "billionfolds@gmail.com"
```

This does **not** modify global Git configuration.

---

*Last updated: 2026-11-25 — keep in sync with sibling copies in `Frontend/docs/` and `backend/docs/` when system scope changes.*