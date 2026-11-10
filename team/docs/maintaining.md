# Maintaining this repository

This repository holds the team and the context of the projects it works on. It holds no
product code.

## Rules

- Keep the agents, the team rules and the team skills free of any one project. Project
  details belong in `projects/<project>/`.
- Name models only in the places listed under "Models" in `AGENTS.md`.
- Never add `sandbox_mode` to an agent file. Codex ignores it there.
- Keep `README.md`, `AGENTS.md` and `docs/` consistent when the team
  changes.
- Record each change to the team as an activity: a feature file in `docs/features/`, and
  a decision record in `docs/adr/` when a decision changes.

## Who works here

| Agent | Folders | Read first |
|---|---|---|
| `platform_engineer` | `bin/`, `.basic-memory/.bmignore`, `.obsidian/`, `.codex/config.toml` | This file |
| `docs_maintainer` | `README.md`, `AGENTS.md`, `.agents/skills/`, `memory/`, `projects/`, `templates/`, `docs/` | `documentation-check`, `memory-review`, `activity-metrics` |
| `security_reviewer` | Whole repository | `security-baseline` |
| `fixer`, `code_mapper` | Files named in the task / whole repository | This file |

## Checks

```bash
bash -n bin/work
python3 -c "import tomllib, glob; [tomllib.load(open(f, 'rb')) for f in glob.glob('.codex/**/*.toml', recursive=True) + glob.glob('projects/*/repos.toml')]"
bin/work --list
bin/work tasks-app --folders
bash -n bin/memory
bin/memory index
bin/memory status
git status --short   # indexing must not change any file
```

`bin/memory search "<question>" --path memory/team` searches as the agents do.
