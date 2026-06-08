# Pattern: epic_create

Create a Jira epic with standard DM fields, components, and parent hierarchy.

---

## 📋 Phase 1 — Gather inputs

Ask the user in a single message:

1. **Epic name** — the title (e.g. `Data Platform H2 2026`)
2. **Description** — brief summary of the epic's purpose
3. **Half / quarter** — used to derive the correct component and parent epic (see mapping below)
4. **Parent epic** — Jira issue key of the parent epic, if applicable (e.g. a yearly roadmap epic)
5. **Assignee** — defaults to the session user if not specified

Wait for the user's response before proceeding.

---

## 🔧 Phase 2 — Derive fields

Use the half/quarter provided to look up the correct component IDs:

| Period | Component IDs | Notes |
|---|---|---|
| H1 | `13377`, `13444` | Update these IDs if components change |
| H2 Q3 | `13377`, `13445` | Update these IDs if components change |
| H2 Q4 | `13377`, `13446` | Update these IDs if components change |

> ⚠️ Component IDs are year-specific. Verify they are current before creating. If unsure, ask the user to confirm.

Apply fixed fields:
- Project: `DM`
- Issue type: `Epic`
- Priority: `Medium`
- Labels: `["dm-claude-created"]`

---

## 🔎 Phase 3 — Confirm

Present a summary of the epic fields before creating. Wait for explicit confirmation.

---

## ⚙️ Phase 4 — Create

Create the epic using `createJiraIssue`. Return the created issue key and URL.
