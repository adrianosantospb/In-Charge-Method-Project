---
name: orchestrate-work
description: Plan and coordinate work that spans more than one agent role, such as a feature touching the backend, frontend, tests, database or documentation. Use for any multi-area task, in any project.
---

# Orchestrate work

Handle a small change in one role directly with the matching agent. Use this playbook
when a task crosses roles or repositories.

## Plan

1. Read the request, `projects/<project>/AGENTS.md` and the `repos/` files of the
   repositories involved.
2. Ask `code_mapper` where the affected code lives when that is not already clear.
3. List the affected roles and repositories, and what each agent must produce.
4. Consult `database_reviewer` when the plan changes a schema, a migration or heavy
   queries, and `security_reviewer` when it changes access rules.
5. Stop and ask the user about undecided business rules.
6. For changes that cross an API boundary, define the contract first, in the place the
   project context names.
7. Propose a name for the activity with every plan: short, in English and in kebab-case,
   so it can name the branch and the feature file.
8. For a new activity, follow "Starting new work" in the team's `AGENTS.md`: the user confirms
   the plan, gives the number and creates the branches before any feature file or code.

## Delegate

Give each agent the goal, its folders, the contract and how to verify the result.

| Order | Agent | Delivers |
|---|---|---|
| 1 | `backend_engineer` | Domain rules, routes, migrations and tests |
| 2 | `frontend_engineer` | Screens in every supported language, and tests |
| 3 | `platform_engineer` | Runtime changes, if the task needs any |
| 4 | `qa_engineer` | Independent tests for rules and denied cases |
| 5 | `security_reviewer` | Review of any sensitive change |
| 5 | `database_reviewer` | Review of any database change |
| 6 | `docs_maintainer` | Documentation check in every repository touched |

Two helpers support this order:

- `code_mapper` finds where code lives before work is planned or delegated. It is
  read-only.
- `fixer` applies small fixes from failures or findings that were already reviewed, in the
  files named in the task. Send design decisions and contract changes to the owning
  agent instead.

Run agents in parallel only when their files do not overlap and the contract is settled.
Do not let two agents edit the same file at once.

## Integrate

1. Send each failure or finding back to the agent that owns the code, or to `fixer`
   when the fix is small and limited to named files.
2. Have the reviewers review again after fixes to code they reviewed.
3. Have `docs_maintainer` run the `documentation-check` and `memory-review` skills.
4. Run all the project's checks on the combined result.

## Report

State what changed, what passed, and anything not verified. List every file or directory
that should be deleted, with its reason, and ask the user before anything is removed. A specialist saying a task is
done does not count as evidence. Commit only when the user asks. Never create branches,
pull or push; those belong to the user.
