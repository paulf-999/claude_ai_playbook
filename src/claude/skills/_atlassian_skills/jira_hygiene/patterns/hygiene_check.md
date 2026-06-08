# Pattern: hygiene_check

Scan Jira tickets for missing or incorrect fields against the DM minimum hygiene criteria. Surface a report and optionally auto-fix issues.

---

## 📋 Phase 1 — Gather inputs

Ask the user in a single message:

1. **JQL filter** — the query that selects the tickets to check (e.g. `project = DM AND sprint = "DM Sprint 63"`)
2. **Mode** — report only, or report and auto-fix where possible

Wait for the user's response before proceeding.

---

## 🔎 Phase 2 — Fetch tickets

Run `searchJiraIssuesUsingJql` with the provided JQL. Fetch the following fields for each ticket:

`summary, priority, assignee, status, story_points (customfield_10028), description, customfield_10020 (sprint), labels`

---

## 🧪 Phase 3 — Run hygiene checks

For each ticket, check against the following minimum criteria:

| Check | Pass condition |
|---|---|
| Priority | Not `Lowest` and not unset |
| Story points | `customfield_10028` is set and > 0 |
| Assignee | Set |
| Description | Not empty |
| Sprint | `customfield_10020` is set |
| Status | Not `Triage` — tickets should be in `Backlog` or beyond |
| Claude label | If ticket was created by Claude (`dm-claude-created` label expected), verify it is present |

---

## 📊 Phase 4 — Report findings

Present a results table grouped by check:

| Ticket | Summary | Failed checks |
|---|---|---|

Include a summary line: `N tickets checked — M passed, K have issues`.

If mode is **report only**, stop here.

---

## 🔧 Phase 5 — Auto-fix (optional)

For issues that can be fixed without user input, offer to apply fixes:

| Issue | Auto-fixable | Fix applied |
|---|---|---|
| Priority is Lowest | Yes | Set to Medium |
| Status is Triage | Yes | Transition to Backlog (transition ID `11`) |
| Missing `dm-claude-created` label | Yes | Add label |
| Missing story points | No — requires user input | Flag only |
| Missing assignee | No — requires user input | Flag only |
| Missing description | No — requires user input | Flag only |
| Missing sprint | No — requires user input | Flag only |

Confirm the list of auto-fixes with the user before applying. Report any failures after applying.
