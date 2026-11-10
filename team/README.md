# Example team repository

A complete team of Codex agents, ready to copy into its own Git repository. It commands
the work on the example project in `../tasks-app`, which holds no information about AI
agents.

The display names are the author's own team. Rename them to yours.

## Before the first session

1. Copy this folder to its own repository, for example `~/work/my-team`.
2. Replace `<strong-model>` in `.codex/agents/orchestrator.toml`,
   `security_reviewer.toml` and `database_reviewer.toml`, and `<fast-model>` in
   `.codex/config.toml`, with models your Codex plan offers.
3. Set the path of the product repository in `projects/tasks-app/repos.toml`.
4. Install [uv](https://docs.astral.sh/uv/) for the memory search, then run
   `bin/memory index`.
5. Start a session with `bin/work tasks-app` and trust the folder when Codex asks.

## Layout

```text
.
├── AGENTS.md                  # Team rules, loaded in every session opened here
├── .codex/
│   ├── config.toml            # Fast model, subagent limits, memory server
│   └── agents/                # One file per agent
├── .agents/skills/            # Team skills, used in every project
├── memory/
│   ├── README.md              # Memory format and limits
│   ├── team/                  # What the whole team learned
│   └── agents/                # What each agent learned
├── projects/
│   └── tasks-app/
│       ├── AGENTS.md          # System context
│       ├── repos.toml         # Repositories and their paths
│       ├── repos/             # Who works where in each repository
│       ├── .agents/skills/    # Project skills
│       └── memory/            # What the team learned about the project
├── templates/project/         # Start a new project folder
├── bin/work                   # Open a session for a project
├── bin/memory                 # Index and search the memory
├── bin/metrics                # Build the dashboard; --budget reads Codex sessions
├── metrics/                   # One CSV per project, dashboard.html, prices.json
├── .basic-memory/.bmignore    # What Basic Memory indexes
├── .obsidian/                 # Graph filter and colours for Obsidian
└── docs/                      # How to maintain this repository, and templates
```

The book *In Charge* explains every file, in Part II.
