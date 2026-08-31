---
name: jira_create
description: Create Jira tickets and epics with full field configuration. Requires Atlassian MCP enabled.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
tools: Read, mcp__atlassian__createJiraIssue
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## 📋 What This Skill Can Do

✅ **Create individual Jira tickets:** Title, description, assignee, story points
✅ **Create Jira epics:** Name, description, assignee
✅ **Validate constraints:** Story points ≥0.5

---

## 🚫 What This Skill Can't Do

❌ **Update existing tickets** — Only creates new ones
❌ **Batch-create from templates** — One ticket at a time
❌ **Manage sprints or components** — Not supported yet
❌ **Create issue links** — Child issues not supported

---

## 📌 Prerequisites

- **Atlassian MCP enabled:** `make enable_mcp server=Atlassian` and Claude Code restarted
- **Jira project access:** Write permission to target project

---

## 🔧 How it works

**Phase 1: Gather details** → Ask for ticket type, title, description, assignee, story points

**Phase 2: Validate & create** → Validate story points ≥0.5, call `createJiraIssue` MCP method

**Phase 3: Report result** → Display issue ID and link

---

## 🧠 Known Gaps

- **No template system:** Must provide details for each ticket individually.
- **No sprint/component caching:** Recent selections not remembered.
- **No labels/components:** Cannot assign labels or components yet.

---
