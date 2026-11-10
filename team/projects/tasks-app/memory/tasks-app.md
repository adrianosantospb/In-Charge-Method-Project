---
title: tasks-app
type: project-memory
permalink: projects/tasks-app/memory/tasks-app
---

# Tasks app memory

Facts learned about this project. Newest first.

## Environment

- [fact] Development runs at `http://localhost:5173` and the production-like stack at `http://localhost:8080`. #environment ([[001]], [[tasks]])
- [fact] The backend tests need an empty PostgreSQL database in `TASKS_DATABASE_URL`; they empty the tables before each test. #testing ([[001]], [[tasks]])

## Database

- [fact] Email uniqueness regardless of case is enforced only by `_normalize` in `auth.py`; the unique index in the database is case-sensitive. #schema ([[002]], [[tasks]])
- [fact] Backend tests empty the tables with `TRUNCATE`; since 002 they refuse any database whose name does not end in `_test`, both in the URL and in `current_database()`. #testing ([[002]], [[tasks]])
- [fact] Migrations run in one transaction at every backend start; a failure rolls back cleanly, then the container restarts in a loop. There is no `lock_timeout` yet. #migrations ([[002]], [[tasks]])

## Pending work

- [pending] Rate limiting of sign-in attempts. #security ([[001]], [[tasks]])
