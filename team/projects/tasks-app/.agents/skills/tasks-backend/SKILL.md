---
name: tasks-backend
description: Add or change a backend route, model or migration in the tasks app. Use for any backend work in the tasks-app repository.
---

# Tasks backend

## Before you write code

1. Read "Rules for changes" in `docs/development.md`.
2. Write the test first in `backend/tests/` and see it fail for the right reason.
   Cover the denied paths: no session, another user's task.

## Routes

- Put routes in a router module under `backend/app/` and include it in `app/main.py`.
- Take the user from the `CurrentUser` dependency in `app/auth.py`. Never take a user
  ID from the request body or the path.
- Load tasks with `owner_id == user.id` in the query itself. Answer `404` for a task that
  is missing or belongs to someone else.
- Validate input with a `SQLModel` class that has field limits.

## Models and migrations

- Change `app/models.py`, then add a migration in `backend/alembic/versions/`.
- Check it from an empty database: `alembic upgrade head`, `alembic check`,
  `alembic downgrade base`, `alembic upgrade head`.
- Send the migration to `database_reviewer` through the orchestrator.

## Finish

Run `ruff check . && ruff format --check . && pytest` in `backend/`. Report the files
changed, the results and anything you could not run.
