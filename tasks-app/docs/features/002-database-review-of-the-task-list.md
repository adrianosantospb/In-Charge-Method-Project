# 002: Database review of the task list

Plan approved: 2026-11-10 16:14 UTC

## Status

Delivered. Waiting for the user's manual tests.

## Goal

Give the schema, migration, queries and development data of activity 001 the database review it planned but never received.

## Scope

- Read-only review with the `database-review` skill: the migration `0001`, the models, the queries in the backend, how and where migrations run, and the test and development data.
- The findings go to the user, who decides what is fixed, what stays open and what goes into the book.

## Out of scope

- Changing code before the user decides on the findings.
- Security of data access, which belongs to the security review of activity 001.

## Findings

No high or medium findings. Four low findings:

1. Whitespace-only task titles are stored as empty strings: `min_length` is checked before `.strip()` (`app/models.py`, `app/tasks.py`).
2. The test setup runs `TRUNCATE tasks, users CASCADE` on whatever `TASKS_DATABASE_URL` names, with no guard on the database name (`tests/conftest.py`).
3. Email uniqueness regardless of case relies only on `_normalize` in `app/auth.py`; the unique index is case-sensitive.
4. `GET /api/tasks` has no limit, sorts by `created_at` only, and has no index for that sort (`app/tasks.py`).

Info notes: models match the migration; time zones, lengths and keys fit the data; the cascade is deliberate; there are no database defaults; the downgrade drops all data by design; migrations run in one transaction at every start, with no `lock_timeout` yet; `env.py` needs `TASKS_JWT_SECRET` to migrate; no constraint naming convention; no development data can reach production.

## Decisions

- Findings 1 and 2 were fixed in this activity. Findings 3 and 4 stay open (see below).
- Fix 1: `TaskCreate` and `TaskUpdate` strip the title before the length check, so a title of only spaces is refused with `422` on create and on update.
- Fix 2: the tests refuse to run unless the database name ends in `_test`, checked twice: in `TASKS_DATABASE_URL` when the tests start, and with `SELECT current_database()` before the first migration or `TRUNCATE`, because a `dbname` query parameter can make the URL name one database and connect to another. `docs/development.md` says so.

## Verification

- Read-only review with the `database-review` skill, by a reviewer who did not write the code.
- On a throwaway PostgreSQL 16: `alembic upgrade head`, `alembic check`, `downgrade base`, `upgrade head`, all passing; the tables match the models; hand inserts confirmed finding 3, the cascade and the NOT NULL columns.
- Fixes, test first: the whitespace test failed (`201`, expected `422`) before the fix. After the fixes, 32 backend tests pass on PostgreSQL 16 (`tasks_test`); the tests stop before any change on a database named `tasks_dev`, and on a URL with `dbname=keepme` (a marker row in `keepme` stayed). `ruff check` and `ruff format --check` pass.
- The database reviewer reviewed the fixes twice: approved with notes (the `dbname` gap and the docs line, both fixed), then approved.
- One write of this feature file reported success but left the old version on disk; the read-back caught it and the file was written again.

## Open items

- Finding 3: a unique index on `lower(email)`, so the database enforces what `_normalize` does today.
- Finding 4: a limit or pagination on `GET /api/tasks`, `ORDER BY created_at, id`, and an index on `(owner_id, created_at, id)` when volumes justify it.
- A title made only of zero-width characters is still accepted; cosmetic.
- The `.strip()` calls in `app/tasks.py` are now redundant.
- The Docker test stack was not run in this activity. Run it before the commit.

## Not verified

- Production-sized data: how many tasks the heaviest users have (finding 4), whether existing rows already break findings 1 and 3, and lock waits once a later migration alters populated tables. The review assumed thousands of users and a few hundred tasks per user, with one backend replica.
