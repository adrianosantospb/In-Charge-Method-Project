# Project: tasks-app

A task list where each person signs in and manages only their own tasks. One repository
holds the backend, the webapp and the Docker Compose files.

The repositories are listed in `repos.toml`. Each one has a context file in `repos/`.
Each repository's own rules are in its `docs/development.md` or `README.md`.

## Repositories

| Key | Repository | What it is | Context |
|---|---|---|---|
| `tasks` | `tasks-app` | FastAPI backend, React webapp, PostgreSQL, Docker Compose | `repos/tasks.md` |

## How the parts connect

- The browser talks to one origin. `/api` goes to the backend: Vite forwards it in
  development and nginx in production.
- The session is a JWT in an `HttpOnly` cookie limited to `/api`. The webapp never reads
  the token. See `docs/adr/0001-keep-the-session-in-an-http-only-cookie.md`.

## Rules for this project

- Activities use the user's work item number: branch `feature/<number>-<name>` and
  feature file `docs/features/<number>-<name>.md`.
- Every task query filters by the signed-in user. Another user's task answers `404`.
- Never open `.env` files. `.env.example` holds the names only.

## Memory

Project memory is in `memory/tasks-app.md` and `memory/activities/`.
