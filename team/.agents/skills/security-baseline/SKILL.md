---
name: security-baseline
description: Baseline security checklist for reviewing authentication, authorization, sessions, tokens, secrets and data exposure in any project. Use with the project's own security skill, if it has one.
---

# Security baseline

Use this list when the project has no security skill, and as a floor when it has one.
The project's own rules and contracts always come first.

## Access

- [ ] Every entry point that needs authentication enforces it on the server.
- [ ] Authorization checks the object, not only the route, so one user cannot reach
      another user's data by changing an ID.
- [ ] Privileged and ordinary access paths stay separate as the project requires.
- [ ] Interface guards are treated as navigation only, never as protection.

## Sessions and tokens

- [ ] Tokens are verified for signature, algorithm, issuer, audience and expiry.
- [ ] Refresh, logout and password changes revoke what they must.
- [ ] Concurrent requests cannot reuse a token or bypass a check.
- [ ] Access tokens and temporary passwords are not kept in browser storage.

## Input and output

- [ ] External input is validated before use. Queries use parameters, never string
      building.
- [ ] Errors and logs do not leak secrets, tokens, passwords or personal data.
- [ ] CORS, cookies and security headers are as strict as the project allows.

## Secrets

- [ ] No secret is committed, printed, logged or baked into an image.
- [ ] Keys and credentials are readable only by the process that needs them.

## Report

List only real findings, most severe first, each with a path and line, a severity, the
failure scenario and the fix. Then list what you checked.
