---
name: jira_create
description: Create individual Jira tickets with full field configuration. Requires Atlassian MCP enabled.
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools: Read, mcp__atlassian__createJiraIssue
---
<!-- version: 0.2.0 -->
<!-- created: 2026-04-11 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** call `getAccessibleAtlassianResources` to confirm Atlassian access and get the cloud ID.
  - **On failure:** stop and tell the user to run `make enable_mcp server=Atlassian` and restart Claude Code.
- **Read first:** read `reference/_field_constraints.md` before drafting, and `reference/_error_handling.md` if a call fails.
- **Always:** show the full ticket (project, type, title, description, assignee, story points) and wait for a yes before creating it.
- **Never:** infer the Jira project, so confirm it with the user.
- **Never:** create a ticket with story points below 0.5.

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

## ✨ Best For

One ticket at a time, with basic fields. Currently at the **draft** development stage — happy path only, gaps logged as TODOs rather than solved. Can't update existing tickets, batch-create from templates, create epics, manage sprints/components, assign labels, or create issue links between tickets yet.

## 📚 References

- `reference/_error_handling.md` — Atlassian connection errors and recovery steps
- `reference/_field_constraints.md` — story point rules and other field validation
- `~/.claude/_rules/05_lazy_load/style_guide_standards/jira.md` — team ticket conventions, read before drafting the ticket
- `_admin/_quality_scorecards/skills/scorecard_jira_create.md` — 7-dimension quality assessment
