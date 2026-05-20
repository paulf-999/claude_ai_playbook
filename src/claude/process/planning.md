# 🗺️ Planning

## ✅ Before trivial work

For simple, low-risk tasks, plan mode is still the minimum requirement — state what you are about to do and wait for confirmation before proceeding.

---

## ⚠️ Before non-trivial work

For any non-trivial task, plan mode is the minimum requirement — do not make changes until the plan has been reviewed and confirmed.

- Use plan mode to outline your approach before touching any file or running any command.
- Outline your approach in plain English.
- List assumptions you are making.
- Flag risks, tech debt, or security concerns.
- For complex or uncertain designs, run `/grill_me` to stress-test the plan — walks down the decision tree one question at a time before any code is written.
- Wait for my go-ahead before proceeding.

---

## 🔄 Design principles

Every design must be **idempotent** and **DRY** before being considered acceptable. Flag any violation explicitly when outlining your approach. See `rules/development.md` for definitions and technology-specific guidance.

---

## 🗂️ Plan catalogue

Plan files are auto-named with random strings by Claude Code. Maintain `~/.claude/plans/PLANS.md` as a structured index so plans are navigable.

**On plan creation:**
After writing a plan file, add a row to `~/.claude/plans/PLANS.md`:

| Column | Value |
|--------|-------|
| File | Markdown link to the plan file |
| Project | Working directory basename (e.g. `playbook`, `airflow`) |
| Task | One-line description of what the plan covers |
| Date | Today's date in `YYYY-MM-DD` format |
| Status | `pending` |

Create the file if it does not exist.

**On plan approval — rename the file (first step of implementation):**
Claude Code assigns a random filename (e.g. `glistening-munching-kahn.md`). Immediately after the plan is approved and before doing any other implementation work, rename it to a descriptive name:

```
mv ~/.claude/plans/<random-name>.md ~/.claude/plans/YYYY-MM-DD_<keyword>.md
```

- **Date:** today's date in `YYYY-MM-DD` format (e.g. `2026-04-23`)
- **Keyword:** 1–3 lowercase words from the plan title joined by underscores (e.g. `plans_catalogue`, `catchup_prep`, `codeowners_review`)

Examples: `2026-04-23_plans_catalogue.md`, `2026-04-23_catchup_prep.md`

Update the PLANS.md row to use the new filename.

**On plan execution** (plan approved and implemented):
Update the plan's row in `PLANS.md` — change `pending` to `executed`. Do not delete or archive the file — that is the user's call via `make clean_plans`.

**On plan supersession** (replaced by a revised plan mid-session):
Update status to `superseded`. File is retained.

Run `make clean_plans` in the playbook repo to archive executed/superseded plans to `~/.claude/plans/archive/` when ready to tidy up.
