# Development guide

## Layout

```text
backend/
  app/            # FastAPI application: config, db, models, security, auth, tasks
  alembic/        # Database migrations
  tests/          # pytest, against a real PostgreSQL database
webapp/
  src/            # React components, the API client and their tests
  nginx.conf      # Production web server: static files and /api forwarding
docs/
  features/       # One file per piece of work: scope, plan, verification, open items
  adr/            # Decision records
```

## Without Docker

You need Python 3.12 or later, Node 22 and a PostgreSQL 16 server.

```bash
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-test.txt
export TASKS_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@localhost:5432/tasks_dev"
export TASKS_JWT_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
export TASKS_COOKIE_SECURE=false TASKS_API_DOCS=true
alembic upgrade head
uvicorn app.main:app --reload
```

The tests need their own, empty database. They empty every table, so its name must end in
`_test`; the tests refuse to run otherwise.

```bash
TASKS_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@localhost:5432/tasks_test" pytest
ruff check . && ruff format --check .
```

In another terminal:

```bash
cd webapp
npm ci
npm run dev        # http://localhost:5173, /api goes to http://localhost:8000
npm run typecheck && npm test
```

## Settings

| Variable | Required | Meaning |
|---|---|---|
| `TASKS_DATABASE_URL` | Yes | SQLAlchemy URL of the PostgreSQL database |
| `TASKS_JWT_SECRET` | Yes | Signs the session tokens. At least 32 characters, generated |
| `TASKS_ACCESS_TOKEN_MINUTES` | No | Session length, 30 by default |
| `TASKS_COOKIE_SECURE` | No | `true` by default. Set to `false` only on plain HTTP in development |
| `TASKS_API_DOCS` | No | `false` by default. `true` serves the API documentation at `/api/docs` |

Never commit `.env` files or real secrets.

## Rules for changes

- Every change starts from a feature file in `docs/features/`, named
  `<number>-<short-name>.md`, and a branch named `feature/<number>-<short-name>`.
- Write the test first and see it fail for the right reason.
- Requests that change data must be `application/json`; the API answers `415` otherwise.
- Every query on tasks filters by the signed-in user. A task of another user answers
  `404`, the same as a task that does not exist.
- Schema changes need an Alembic migration that runs from an empty database and back.
- Changes to sign-in, sessions or secrets need a security review before they are done.
- Before you finish: backend tests and lint, webapp type check and tests, and the
  documentation that the change made false.
