---
title: Memory guide
type: guide
permalink: memory/readme
---

# Memory

What the team learned by working. Rules, project context and decision records say what
must be done; memory says what was learned doing it.

| Memory | Files | Read by | Limit |
|---|---|---|---|
| Individual | `agents/<agent>.md`, named after the agent's role | That agent | 60 lines |
| Team | `team/lessons.md` | Every agent | 150 lines |
| Project | `../projects/<project>/memory/<project>.md` | Agents working on that project | 150 lines |
| Activities | `activities/` and `../projects/<project>/memory/activities/` | Anyone following a link | One short note each |

The files are the source of truth and live in Git. Basic Memory indexes them so agents can
search and follow links, and Obsidian shows them as a graph. Neither replaces the files.

## Format

Each entry is one line, written as an observation that Basic Memory and Obsidian
understand:

```markdown
- [lesson] Read every file back after writing it and compare it. #delivery ([[001]], [[tasks]])
```

- **Category** in brackets: `lesson` for something learned, `fact` for how a project is,
  `pending` for known open work.
- **Tags** with `#`, without spaces: `#delivery`, `#security`.
- **Links** in brackets at the end: the activity that taught it and the repositories it
  applies to, as `[[001]]` or `[[tasks]]`. Links are what make the graph.
- A note that links to other notes as a whole lists them under `## Relations`, as
  `- part_of [[tasks-app]]`.
- Every file starts with frontmatter that has `title`, `type` and `permalink`. Without it,
  Basic Memory adds a permalink to the file the first time it indexes it.

## Writing

- Only Eva Bourgeais-Boon writes memory, after the user approves the entries. See the
  `memory-review` skill.
- Newest entries first in each section.
- A new activity that taught something gets its own note in `activities/`, so the
  entries can link to it.
- Remove an entry when it stops being true. Do not keep history here; Git keeps it.
- A lesson that must always be followed becomes a rule in `AGENTS.md`, a skill or the
  project context, and leaves memory.
- Never record secrets, passwords, tokens, personal data or values from `.env` files.
