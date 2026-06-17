---
name: jira_subtask
description: Create one or more Jira sub-tasks under a parent ticket for the Data Platform team. Encodes correct field names and exclusions to avoid API trial-and-error. Requires the Atlassian MCP server.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools: mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__createJiraIssue
triggers:
  explicit:
    - /jira_subtask
    - "create sub-tasks"
    - "create jira sub-tasks"
    - "add sub-tasks to"
  contextual:
    - user wants to create sub-tasks under an existing Jira ticket
not_for:
  - creating stories or epics (/jira_create)
  - updating existing tickets (/jira_update)
output:
  type: external_service
  confirmation_required: true
---

## Scope gate

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |

---

## ⚠️ Pre-check — Atlassian MCP

Call `getAccessibleAtlassianResources` before proceeding. If it fails, stop and tell the user:

> "This skill requires the Atlassian MCP server. Run `make enable_mcp server=Atlassian` and restart Claude Code, then try again."

---

## Phase 1 — Gather inputs

Ask the user for only:

1. **Parent ticket key** — e.g. `DM-12345`
2. **Sub-task list** — titles (and optionally descriptions) for each sub-task

Do not ask for assignee or priority — these are resolved from the parent in Phase 2 and defaulted silently. Only prompt for them if the user volunteers overrides. Do not ask for or set story points — sub-tasks never carry story points.

---

## Phase 2 — Validate parent and set defaults

Call `getJiraIssue` on the parent key. Confirm it exists and extract:

| Field | Used for |
|---|---|
| `project.key` | Required for sub-task creation |
| `components` | Copied to all sub-tasks |
| `assignee.accountId` | Default assignee |
| `priority.name` | Default priority (fallback: `Medium`) |

If the parent does not exist, stop and tell the user. Assignee handling is covered in [phase3.md](phase3.md).

Confirm with the user before proceeding:

> "Ready to create N sub-tasks under [parent key] — proceed?"

Wait for confirmation before continuing to Phase 3.

---

## Phase 3 — Create sub-tasks

See [phase3.md](phase3.md) for critical field rules, request structure, and creation instructions.

---

## Phase 4 — Confirm

Output a table of all sub-tasks attempted:

| # | Summary | Key | URL | Status |
|---|---|---|---|---|
| 1 | ... | DM-XXXXX | https://payroc.atlassian.net/browse/DM-XXXXX | Created |
| 2 | ... | — | — | Failed: `<error message>` |

If any failed, tell the user what went wrong and whether a retry is safe (i.e. the sub-task was not partially created).
