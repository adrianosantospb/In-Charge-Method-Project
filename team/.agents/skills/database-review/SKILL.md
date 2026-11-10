---
name: database-review
description: Review a schema, migration, hand-written SQL, seed data or heavy query for data loss, locks, reversibility, integrity and performance. Use when planning or reviewing any database change, in any project.
---

# Database review

Read-only. Review the plan before code exists, and the code before delivery.

## Gather

- The project context (`projects/<project>/AGENTS.md` and `repos/`): where models, migrations, SQL and seed data live, and
  how and when migrations run in each environment.
- The diff of every migration, model and query in the activity.
- Whether models live in another repository, such as a shared module.

## Migrations

- [ ] Each schema change has a migration, and the models match it.
- [ ] Nothing drops or rewrites data without an explicit, approved plan.
- [ ] New `NOT NULL` columns on existing tables have a default or a backfill.
- [ ] Large backfills run in batches or outside the deploy.
- [ ] Table rewrites and long locks are avoided, or the downtime is stated. For
      PostgreSQL, prefer `CREATE INDEX CONCURRENTLY` and constraints added `NOT VALID`
      and validated later, when the migration tool allows it.
- [ ] The downgrade works, or the migration says it cannot be undone and why.
- [ ] The migration runs from an empty database and from the current production schema.
- [ ] Migrations that run automatically at startup cannot leave the service unable to
      start on a partial failure.

## Integrity

- [ ] Primary keys, foreign keys, unique and check constraints protect the rules that
      must never break, not only application code.
- [ ] Deletion behavior (`CASCADE`, `RESTRICT`, soft delete) is deliberate.
- [ ] Time zones, numeric precision and text lengths fit the data.

## Queries

- [ ] Filters, joins and sorts used by frequent queries have suitable indexes.
- [ ] No N+1 queries and no unbounded result sets on user-facing paths.
- [ ] Transactions are short and hold no lock across network calls.

## Development data

- [ ] Seed and test data load only in development and tests, never through a production
      migration, image or configuration.

## Report

List findings most severe first, each with a path and line, a severity, the failure
scenario and the fix. State the data volumes you assumed and what only a production-sized
copy could confirm. Leave access control and injection to `security_reviewer`, unless you
found something concrete.
