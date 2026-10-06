<!-- version: 2.0.0 -->
<!-- created: 2026-05-20 -->
<!-- updated: 2026-10-06 -->
# ✅ Definition of Ready

Validation checklist for Jira tickets before sprint entry. All blocking checks must pass before a ticket is moved into a sprint. Custom field IDs live in the Jira values in `~/.claude/_rules/05_lazy_load/org.md`.

## Blocking (must pass before entering a sprint)

| # | Check |
|---|---|
| 1 | Title follows naming convention (`<Area> — <action or topic>` em-dash format) |
| 2 | Description populated — not a placeholder or reminder note |
| 3 | Acceptance criteria present in description |
| 4 | Story points assigned and non-zero (Story points custom field) |
| 5 | Assignee set |
| 6 | Epic / parent linked (`parent` field) |
| 7 | At least one component assigned (`components` field) |
| 8 | Business Value Statement populated (Business value custom field) |
| 9 | Business Value ends with Impact Rating block (includes Prioritization Matrix link) |
| 10 | Status is not `Triage` |

---

## Recommended (should pass)

| # | Check |
|---|---|
| 11 | Sprint assigned (Sprint custom field) |
| 12 | Priority set |
