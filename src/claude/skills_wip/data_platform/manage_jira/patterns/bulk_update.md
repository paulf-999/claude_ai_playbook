# Pattern: bulk_update

Update one or more fields across multiple Jira tickets matched by a JQL filter.

---

## 📋 Phase 1 — Gather inputs

Ask the user in a single message:

1. **JQL filter** — the query that selects the tickets to update (e.g. `project = DM AND sprint = "DM Sprint 63" AND priority = Lowest`)
2. **Field(s) to update** — field name and new value for each (e.g. `priority → Medium`, `labels → add dm-claude-created`)
3. **Mode** — report only (show what would change without applying) or apply changes

Wait for the user's response before proceeding.

---

## 🔎 Phase 2 — Fetch and confirm scope

Run `searchJiraIssuesUsingJql` with the provided JQL. Request only the fields being updated plus `summary` and `key`.

Present a summary:
- Total tickets matched
- Current values of the field(s) being updated (sample or full list depending on count)
- Proposed new value(s)
- Estimated duration and credit cost

> "This will update N tickets across N API calls — approximately $X in credits. Confirming before I apply."

If mode is **report only**, output the matched tickets and proposed changes, then stop. Do not apply.

Wait for explicit confirmation before applying changes.

---

## ⚙️ Phase 3 — Apply updates

Update tickets in **parallel batches** where safe (field updates with no dependencies). After each batch, output a progress line:

> "Updated 4 of 12 (33%)"

Use `editJiraIssue` for field updates. For status changes, use `transitionJiraIssue`.

---

## ✅ Phase 4 — Report

Output a summary of applied changes. Flag any failures with the ticket key and error message.
