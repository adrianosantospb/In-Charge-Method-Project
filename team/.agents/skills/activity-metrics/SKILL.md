---
name: activity-metrics
description: Record where the errors of a finished activity were caught and what the activity cost, and rebuild the team metrics dashboard. Use at the end of every activity, after the memory review.
---

# Activity metrics

Only `docs_maintainer` runs this skill, and it writes the row only after the user
approves it. The metrics belong to the team: they live in `metrics/<project>.csv` in the
team repository, one file per project, and the team repository itself counts as a
project. Start a new file with `bin/metrics --new <project>`.

## Count

Read the activity's reports and its feature file, and count:

| Column | What to count |
|---|---|
| `review_high`, `review_medium`, `review_low` | Findings of every independent review in the activity, by severity. Leave out notes of information only. Count a finding once, even if a second review mentions it again. |
| `readback_failures` | Files that did not match what was written when they were read back. |
| `manual_findings` | Problems the user found in manual tests that the agents had not found. |
| `questions` | Questions the team asked the user before development started. |
| `plan_changes` | Of those questions, how many answers changed the plan. |
| `production_errors` | Errors from this activity found in production so far. Update the row when one appears later. |
| `duration_hours` | Hours from the plan's approval to the delivery report. |
| `tokens`, `cost_usd` | Tokens and cost of the activity, from `bin/metrics --budget` (below). |

Count only what the reports show. If a number is unknown, ask the user. The budget
columns may stay empty when the number is unknown; never estimate them.

## Budget

Take the times of the plan's approval and of the delivery report from the activity's
feature file or ask the user, then run:

```bash
bin/metrics --budget --since <approval time> --until <delivery time> --cwd <team repo> --cwd <project repo>
```

Write the times with their zone (`Z` or `-03:00`); without one the machine's zone is
assumed. Use one `--cwd` for each repository the activity touched. Show the user the list of
sessions it found, so they can spot work from another activity in the same interval.
Copy `duration_hours,tokens,cost_usd` from the last line. If it names models without a
price, leave `cost_usd` empty and tell the user which prices are missing in
`metrics/prices.json`. When there is a cost, add "cost at API prices" to the row's note.

## Propose and write

1. Show the user the new row of `metrics/<project>.csv`, with a one-line note on where the
   numbers came from.
2. After the user approves it, add the row, with the activity number, the date in
   `YYYY-MM-DD` and the activity name.
3. Run `bin/metrics --check`, then `bin/metrics`, and read `metrics/dashboard.html` back.
4. Report the row and the totals of the project.
