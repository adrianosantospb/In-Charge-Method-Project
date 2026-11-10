---
title: <key>
type: repository
permalink: projects/<project>/repos/<key>
---

# Repository: <repository>

<What it is.> Rules, layout and commands: `docs/development.md` in the repository.

| Agent | Folders | Read first |
|---|---|---|
| `backend_engineer` | `<path>/` | `<skill or document>` |
| `frontend_engineer` | `<path>/` | `<skill or document>` |
| `platform_engineer` | `<Docker, proxy, CI and deploy files>` | `<skill or document>` |
| `qa_engineer` | `<test folders>` | `<skill or document>` |
| `security_reviewer` | Whole repository | `<project security skill, if any>` |
| `database_reviewer` | `<models, migrations, SQL and seed data>` | `<database rules>` |
| `docs_maintainer` | `<docs/, README.md>` | `<documentation rules>` |
| `fixer`, `code_mapper` | Files named in the task / whole repository | `docs/development.md` |

- **Checks:** <where the commands are>.
- **API contract:** <file, if any>.
- **Migrations:** <how and when they run in each environment>.
- **Never open:** <files with credentials beyond `.env`>.
- **Feature files:** <folder and template, or "not used">.

## Relations

- part_of [[<project>]]
