# Tasks

A task list where each person signs in and manages only their own tasks.

| Part | Stack |
|---|---|
| `backend/` | Python, FastAPI, SQLModel, Alembic, PostgreSQL |
| `webapp/` | React, TypeScript, Vite |
| Containers | Docker Compose for development, tests and a production-like stack |

## Run it

Development, with both servers reloading on change:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Open <http://localhost:5173>, create an account and add a task.

Tests:

```bash
docker compose -f docker-compose.test.yml up --build \
  --abort-on-container-exit --exit-code-from backend-tests
docker compose -f docker-compose.test.yml run --rm --build webapp-tests
```

Production-like stack on <http://localhost:8080>:

```bash
cp .env.example .env    # then fill in the values
docker compose up --build -d
```

See [`docs/development.md`](docs/development.md) for working without Docker, the
project layout and the rules for changes.

## API

| Method | Path | Session | Does |
|---|---|---|---|
| `POST` | `/api/auth/register` | No | Creates an account and signs in |
| `POST` | `/api/auth/login` | No | Signs in |
| `POST` | `/api/auth/logout` | No | Signs out |
| `GET` | `/api/auth/me` | Yes | The signed-in user |
| `GET` | `/api/tasks` | Yes | The user's tasks |
| `POST` | `/api/tasks` | Yes | Adds a task |
| `PATCH` | `/api/tasks/{id}` | Yes | Renames a task or marks it done |
| `DELETE` | `/api/tasks/{id}` | Yes | Deletes a task |
| `GET` | `/api/health` | No | Health check |

In development, the interactive documentation is at <http://localhost:5173/api/docs>.
It is off unless `TASKS_API_DOCS=true`.
