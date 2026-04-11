# Pattern: batch_create_from_template

Create multiple Jira tickets from a defined internal template, with per-ticket field overrides applied at creation time.

---

## 🔍 Phase 1 — Select a template

Ask the user which template to use:

| Template | Description |
|---|---|
| `planning_prep` | Sprint planning prep ticket — standard DM planning prep shape with description, ACs, business value, and quarter-aware component/epic mapping |

Read the template file before proceeding:

`~/.claude/skills_wip/data_platform/manage_jira/templates/data_platform/<template_name>.md`

Wait for the user's response before proceeding.

---

## 📋 Phase 2 — Gather per-ticket data

Based on the template's variable fields, ask the user to provide the per-ticket data. Present the required fields clearly — a table is the preferred format for multi-ticket input.

For `planning_prep`, the variable fields per ticket are:
- Sprint number (N) — the sprint being prepped for
- Title — defaults to `Data Platform — Sprint N planning prep`

All other fields (assignee, story points, priority, label, description structure, business value shape) are fixed by the template.

Wait for the user's response before proceeding.

---

## 🔎 Phase 3 — Confirm scope

Present a summary of what will be created:
- Number of tickets
- Template being used
- Fixed fields applied to all tickets
- Per-ticket variable fields (title, sprint assignment)
- Estimated duration and credit cost

State scope before proceeding:

> "This will create N tickets across ~N+1 API calls (creation + Backlog transition per ticket) — approximately $X in credits. Proceeding now."

Wait for explicit confirmation before proceeding.

---

## ⚙️ Phase 4 — Create tickets

Create tickets **sequentially** (not in parallel) to make progress easy to follow and errors easy to isolate. After each ticket, output a brief status line:

> "Created 1 of N — DM-XXXXX"

For each ticket, apply in a single `createJiraIssue` call:
- All fixed fields from the template
- Per-ticket overrides (title, sprint number substituted into description and title)
- `labels: ["dm-claude-created"]`
- `priority: {"name": "Medium"}`
- Sprint assignment via `customfield_10020` as a **plain integer** (not an object)

After creation, transition each ticket to **Backlog** using `transitionJiraIssue` with transition ID `11`.

---

## ✅ Phase 5 — Report

Output a summary table of all created tickets:

| Ticket | Title | Sprint assigned | Status |
|---|---|---|---|

Flag any failures (sprint not found, transition failed) with the ticket key and error. Do not silently skip failures.
