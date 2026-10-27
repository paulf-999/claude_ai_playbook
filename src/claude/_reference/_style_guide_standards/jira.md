<!-- version: 2.0.2 -->
<!-- created: 2026-05-20 -->
<!-- updated: 2026-10-27 -->
<!-- miss_cost: low — tickets in the wrong format -->
<!-- loading: lazy — only applies when writing Jira tickets, which have no local file to trigger on -->
# 🎫 Jira Style Guide & Standards

**Purpose:** Define standards for a team's Jira project — field requirements, ticket structure, component and sprint assignment, and hygiene expectations.

- **Read on demand:** the Jira values in `~/.claude/_rules_lazy_load/org.md` — your organisation's project key, board, field IDs, components, label and scoring weights.

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`jira/_ticket_conventions.md`](jira/_ticket_conventions.md) | Summary naming, description structure, acceptance criteria, and issue type usage |
| [`jira/_field_standards.md`](jira/_field_standards.md) | Required fields, default values, custom fields, components, and label conventions |
| [`jira/_definition_of_ready.md`](jira/_definition_of_ready.md) | Definition of Ready checklist — blocking and recommended checks before sprint entry |
| [`jira/_sprint_planning.md`](jira/_sprint_planning.md) | Sprint IDs, quarter components, parent epics, and capacity conventions |
| [`jira/_business_value.md`](jira/_business_value.md) | Business Value tab format, audience guidance, scoring frameworks, and worked example |

## 🏗️ Core principles

- **Completeness** — all required fields set before a ticket enters the sprint: priority, story points, assignee, sprint, description
- **Scannability** — bullet points throughout; no prose walls in description or acceptance criteria
- **Consistency** — standard components, labels, and description structure on every ticket
- **Traceability** — a Claude-created label on every Claude-authored ticket, named in `org.md`; enables hygiene checks and filtering
