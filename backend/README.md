# MyTruyen Query Service

Natural-language, read-only database query service for MyTruyen.

## Setup

```powershell
uv sync
Copy-Item .env.example .env
uv run uvicorn app.main:app --reload --port 8001
```

Use a PostgreSQL account that has only `SELECT` permission on the approved
tables. Gemini generates PostgreSQL SQL, then `sqlglot` parses it, validates
its tables and columns against the catalog, and enforces a result limit.

Preview endpoint:

```text
POST /api/v1/nl-query/preview
```

This endpoint returns validated SQL without executing it.

Execute endpoint:

```text
POST /api/v1/nl-query/execute
```

It generates and validates SQL, then executes it inside a read-only transaction
with a database statement timeout.
