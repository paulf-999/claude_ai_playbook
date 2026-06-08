# Pattern: batch_create_from_template

Create multiple Jira tickets from a defined internal template, with per-ticket field overrides applied at creation time.

---

## 🔍 Phase 1 — Select a template

Ask the user which template to use:

| Template | Description |
|---|---|
| `planning_prep` | Sprint planning prep ticket — standard DM planning prep shape with description, ACs, business value, and quarter-aware component/epic mapping |
| `vm_ansible_deployment` | 5-story VM deployment set — scoping, VM provisioning, Ansible configuration, deployment, and validation. Variable inputs: service name, target environment, sprint, and parent epic |

Read the template file before proceeding:

`~/.claude/skills/_atlassian_skills/jira_create/templates/data_platform/<template_name>.md`

Wait for the user's response before proceeding.

---

## 📋 Phase 2 — Gather per-ticket data

Based on the template's variable fields, ask the user to provide the per-ticket data. Present the required fields clearly — a table is the preferred format for multi-ticket input.

For `planning_prep`, the variable fields per ticket are:
- Sprint number (N) — the sprint being prepped for
- Title — ask the user for their team/area prefix (e.g. `Data Platform`, `Data Analytics`), then construct as `<Area> — Sprint N planning prep`. Do not default to `Data Platform`. Store the area prefix and use it consistently for all ticket titles in this batch.

For `vm_ansible_deployment`, the variable fields are:
- Service name — the service being deployed (e.g. `Airbyte`)
- Target environment — the destination environment or data centre (e.g. `DC3`)
- Sprint ID — plain integer sprint ID to assign all 5 tickets to (components and parent epic are derived from sprint via the quarter mapping)

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
