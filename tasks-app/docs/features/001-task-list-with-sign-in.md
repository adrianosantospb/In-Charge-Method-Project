# 001 Task list with sign-in

## Scope

- People create an account with email and password, sign in and sign out.
- Each person adds, completes and deletes their own tasks. The API can also rename a
  task; the webapp does not offer it yet.
- Nobody sees or changes another person's tasks.
- Development, test and production-like Docker Compose stacks.

Out of scope: password reset, email verification, rate limiting of sign-in attempts.

## Plan

| Step | Status |
|---|---|
| 1. Backend: models, migration, password hashing and session cookie | Done |
| 2. Backend: task routes filtered by owner | Done |
| 3. Backend tests, including denied paths | Done |
| 4. Webapp: sign-in form and task list, with tests | Done |
| 5. Docker Compose for development, tests and production | Done |
| 6. Security review of sign-in and sessions | Done, findings fixed or listed below |
| 7. Documentation check | Done |

## Decisions

- The session is a short JWT in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie
  limited to `/api`. See [ADR 0001](../adr/0001-keep-the-session-in-an-http-only-cookie.md).
- Passwords are hashed with Argon2. At sign-in, a wrong password and an unknown email get
  the same answer and take about the same time. Registration still says when an email is
  taken; that trade-off is accepted for this app.
- Requests that change data must be `application/json`, as a second guard against
  cross-site requests.
- The API documentation is off unless `TASKS_API_DOCS=true`, as in development.
- Another user's task answers `404`, so its existence is not revealed.

## Verification

- Backend: 25 tests against PostgreSQL 16, Ruff lint and format.
- Migration: upgrade from an empty database, `alembic check`, downgrade and upgrade again.
- Webapp: 10 tests, TypeScript type check and production build.
- Docker: the test stack ran on a developer machine, with 25 backend and 10 webapp tests
  passing in containers. That run found two problems the local tests could not: the
  webapp tests stopped the shared test database early, and the test user could not
  create its caches in `/app`. Both are fixed.
- Browser: sign up, add and complete tasks, reload, sign out, a second user sees no
  tasks, and a wrong password shows the error.

## Open items

- Rate limiting of sign-in attempts belongs in the reverse proxy or a later feature.
- Signing out removes the cookie, but a copied token stays valid until it expires.
- Only direct Python dependencies are pinned. A lock file with hashes would make builds
  reproducible.
