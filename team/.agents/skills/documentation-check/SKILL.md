---
name: documentation-check
description: Check and fix the documentation at the end of an activity, so that READMEs, development guides, contracts, decision records, feature files, architecture models and the team's project context match what was delivered, and review the team's model settings. Use before reporting any activity as done, in any project.
---

# Documentation check

Run this at the end of every activity, in every repository it touched and in the team
repository. Write in each repository's documentation language. Change documents only,
never product code.

## Checklist

- [ ] The feature file of the activity has the right status, plan steps and open items.
- [ ] Earlier feature files that this activity completes are updated.
- [ ] `README.md` describes the current behavior, setup and commands.
- [ ] The repository's development guide lists new and removed files, rules and commands.
- [ ] Target repositories have no `AGENTS.md`, `.agents/` or `.codex/`, and no agent names.
      Their documents describe work by role.
- [ ] In the team repository, `projects/<project>/AGENTS.md`, its `repos/` files and its
      skills match the code, the folders and the commands.
- [ ] A changed decision has a new decision record, and the old one is marked as
      superseded, if the project keeps decision records.
- [ ] Documentation indexes list new decision records and feature files.
- [ ] The architecture model, if the project has one, matches the containers and flows.
- [ ] Other repositories affected by the activity have consistent documentation.
- [ ] No statement is left over from before the change.

## Check the models

When the activity touched the team repository, or when the user asks, read
`default_subagent_model` in the team's `.codex/config.toml` and every `model` value in
`.codex/agents/*.toml`. Check that:

- model names appear only in the places listed under "Models" in the team's `AGENTS.md`;
- each agent's `model_reasoning_effort` matches that table;
- the current Codex documentation still lists each model and still recommends it for
  that kind of work.

Do not change a model or an effort yourself. When a change is worth making, send the
user a proposal with:

- the current and the suggested model or effort, for each agent affected;
- the main benefits, such as cost, speed or quality;
- the reasons, such as a retired model, a new recommendation or repeated mistakes;
- what you could not verify, such as whether the model is available in the user's plan.

Apply the change only after the user approves it, and record it in the activity report.

## Find leftovers

Search for wording that the activity made false, such as:

```bash
grep -rnI -iE "not .* yet|in progress|not started|ready for review" \
  --include=*.md --include=*.toml --include=*.dsl .
```

Review each hit. Keep a superseded decision record as it is, apart from its status.

## Rules

- Do not edit generated files, such as `CHANGELOG.md`, unless the project says to.
- Do not record secrets, passwords, tokens or values from `.env` files.
- Report anything you could not verify.
