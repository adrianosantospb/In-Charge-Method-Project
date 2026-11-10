# In Charge: the example

The complete example from the book *In Charge: a team of agents, with me in charge*, by
Adriano Araujo Santos. The book describes the In-Charge Method: building software with a
permanent team of AI agents in Codex, while a person keeps every decision.

This repository has the code the book refers to. The book itself is sold separately.

## What is here

```text
team/        a complete team repository: agents, rules, skills, memory and metrics
tasks-app/   the example product: FastAPI, React, PostgreSQL and Docker Compose
```

In real use, `team/` and `tasks-app/` are two separate repositories. They sit together
here so the book can refer to both. The product holds no information about AI agents; the
team's context for it lives in `team/projects/tasks-app/`.

## Start here

- To run the application and its tests, see [`tasks-app/README.md`](tasks-app/README.md).
  You need Docker with Compose.
- To use the team, see [`team/README.md`](team/README.md). You need Codex. Copy `team/`
  to its own repository, set your models and the path of the product repository, and
  start a session with `bin/work tasks-app`.

The history of the example is in the repository itself:
`tasks-app/docs/features/` has the activities the book follows, and
`team/metrics/dashboard.html` shows where their errors were caught.

## License

The code in this repository is released under the MIT License. See [`LICENSE`](LICENSE).
The book is not part of this repository and is not covered by this license.
