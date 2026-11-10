# 0001 Keep the session in an HttpOnly cookie

## Status

Accepted

## Context

The webapp needs to stay signed in across page loads. A token kept in `localStorage`
is readable by any script on the page, so one injected script could steal it.

## Decision

The backend sets a signed JWT in a cookie that is `HttpOnly`, `Secure`,
`SameSite=Strict` and limited to the path `/api`. The webapp never reads the token.
The webapp and the API share one origin: Vite forwards `/api` in development, and
nginx does it in production.

## Consequences

- Scripts on the page cannot read the session.
- Cross-site requests are blocked twice, so no CSRF token is needed while the API has no
  CORS. `SameSite=Strict` keeps the cookie off requests from other sites, and the API
  refuses any request that changes data unless it is `application/json` (`415`), which
  another origin cannot send without a CORS preflight. The second check also covers
  sibling subdomains, which count as the same site.
- The API and the webapp must stay on the same site. Serving them from different
  domains needs a new decision.
- Tokens are not stored on the server, so signing out cannot revoke a copied token
  before it expires. Sessions are kept short (30 minutes) for that reason.
