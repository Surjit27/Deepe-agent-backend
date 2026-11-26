# Python backend troubleshooting

Internal FastAPI worker (port **4100**).

## Alembic / `ai` schema errors

1. Ensure Postgres is up from `backend/docker compose up -d postgres`.
2. `alembic upgrade head` from this repo—revisions create schema **`ai`** if missing.
3. `DATABASE_URL` should allow `search_path` or explicit `ai` usage per `app/config.py`.

## `401` on `/v1/jobs/*`

All internal routes require header:

```http
X-Internal-Key: <INTERNAL_API_KEY>
```

Match the value in Node `.env` and this repo’s `.env`.

## Health OK but jobs hang

1. Check `ai.index_jobs` row status in Postgres.
2. Confirm git clone credentials / repo URL in the job body from Node.
3. Mongo connection required for snapshot snippets—verify `MONGO_URI` matches the Node stack.

## OpenAPI drift with Node

Regenerate or hand-sync types from http://localhost:4100/openapi.json when `app/contracts/` changes. See [SCHEMA_ARCHITECTURE.md](./SCHEMA_ARCHITECTURE.md) for identity fields.

## Related docs

- [PROJECT_AND_SCOPE.md](./PROJECT_AND_SCOPE.md)
- [../README.md](../README.md)

*Last updated: 2026-11-26*