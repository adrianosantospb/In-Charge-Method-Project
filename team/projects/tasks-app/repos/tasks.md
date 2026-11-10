---
title: tasks
type: repository
permalink: projects/tasks-app/repos/tasks
---

# Repository: tasks-app

Backend, webapp and Docker Compose files of the tasks app. Rules, layout and commands:
`docs/development.md` and `README.md` in the repository.

| Agent | Folders | Read first |
|---|---|---|
| `backend_engineer` | `backend/app/`, `backend/alembic/` | `tasks-backend` skill, "Rules for changes" in `docs/development.md` |
| `frontend_engineer` | `webapp/src/` | "Rules for changes" in `docs/development.md` |
| `platform_engineer` | `backend/Dockerfile`, `webapp/Dockerfile`, `webapp/nginx.conf`, `docker-compose*.yml`, `.env.example` | `README.md` |
| `qa_engineer` | `backend/tests/`, `webapp/src/*.test.tsx` | "Rules for changes" in `docs/development.md` |
| `security_reviewer` | Whole repository | `security-baseline`, `docs/adr/` |
| `database_reviewer` | `backend/app/models.py`, `backend/alembic/` | `database-review` |
| `docs_maintainer` | `README.md`, `docs/` | `documentation-check` |
| `fixer`, `code_mapper` | Files named in the task / whole repository | `docs/development.md` |

- **Checks:** backend `ruff check . && ruff format --check . && pytest`; webapp
  `npm run typecheck && npm test && npm run build`; or `docker-compose.test.yml`.
- **API contract:** the API table in `README.md` and `/api/docs`.
- **Migrations:** Alembic, in `backend/alembic/versions/`. The backend runs
  `alembic upgrade head` each time it starts, so a failing migration stops it.
- **Never open:** `.env`.
- **Feature files:** `docs/features/`, decision records in `docs/adr/`.

## Relations

- part_of [[tasks-app]]
