---
name: memory-review
description: Consolidate what the team learned in an activity into the individual, team and project memories, after the user approves the entries. Use at the end of every activity, after the documentation check.
---

# Memory review

Only `docs_maintainer` runs this skill, and it writes memory files only after the user
approves the entries. Read `memory/README.md` first for the format and the limits.

## Collect

1. Read the reports of the activity and list every memory entry the agents proposed.
2. Add lessons the reports show but nobody proposed, such as a check that failed for a
   reason worth remembering, or a correction the user made.
3. Read the current memory files that each candidate would change.

## Sort

Put each candidate in one place only:

| Candidate | Memory |
|---|---|
| Helps one role in any project | `memory/agents/<agent>.md` |
| Helps every role in any project | `memory/team/lessons.md` |
| True only in one project | `projects/<project>/memory/` |
| A rule that must always be followed | Not memory: propose a change to `AGENTS.md`, a skill or the project context |
| A decision | Not memory: propose a decision record |

Drop candidates that repeat an existing entry, a rule or a document.

## Propose

Send the user one list, grouped by file:

- entries to add, each with its text and source activity;
- entries to change or remove because they are no longer true;
- files that would pass their size limit, and what you would cut.

If there is nothing to add, change or remove, say so in the report, so the user knows the
review ran.

## Write

After the user approves, apply exactly the approved entries. Keep each file within its
limit, newest entries first within each section. Never record secrets, passwords, tokens,
personal data or values from `.env` files.

Write each entry in the format of `memory/README.md`: one observation per line, with
links to the activity and the repositories. When the activity has no note yet, create it
in `memory/activities/` or `projects/<project>/memory/activities/`. Every new file needs
`title`, `type` and `permalink` frontmatter, and its title must match its file name when
other notes link to it.

Basic Memory picks up the changes by itself. Run `bin/memory index` and `git status` to
confirm the files were indexed and not changed. Report the files you changed.
