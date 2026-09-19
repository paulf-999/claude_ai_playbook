---
name: jira_create
description: Create individual Jira tickets with full field configuration. Requires Atlassian MCP enabled.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
tools: Read, mcp__atlassian__createJiraIssue
---

## 🎯 Purpose

Create individual Jira tickets with the fields your team actually needs:
- **Gather details** — ticket type, title, description, assignee, story points
- **Validate before creating** — story points must be ≥0.5
- **Report the result** — displays the new issue's ID and link

## 💡 Example Usage

```
$ /jira_create create a ticket for the login bug, 2 story points
[Phase 1] Gathering details: type=Task, title, description, assignee, story points
[Phase 2] Validating: story points 2 ≥ 0.5 ✓
          Creating ticket in Jira...
[Phase 3] Ticket created: PROJ-1234

PROJ-1234 created: https://yourteam.atlassian.net/browse/PROJ-1234
```

**Best for:** One ticket at a time, with basic fields. Currently at the **draft** development stage — happy path only, gaps logged as TODOs rather than solved. Can't update existing tickets, batch-create from templates, create epics, manage sprints/components, assign labels, or create issue links between tickets yet.

---

**For detailed specifications, see:**
- `reference/error_handling.md` — Atlassian connection errors and recovery steps
- `reference/field_constraints.md` — story point rules and other field validation
- `_quality_scorecard.md` — 7-dimension quality assessment

## 📌 Prerequisites

- **Atlassian MCP enabled:** `make enable_mcp server=Atlassian` and Claude Code restarted
- **Jira project access:** Write permission to target project
