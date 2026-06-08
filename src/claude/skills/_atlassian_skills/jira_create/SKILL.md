---
name: jira_create
description: Create Jira tickets or epics for the Data Platform team — batch-create from a template or create a standalone epic. Requires the Atlassian MCP server (`make enable_mcp server=Atlassian`, then restart Claude Code).
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
tools: Read, mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__createJiraIssue, mcp__claude_ai_Atlassian__transitionJiraIssue
triggers:
  explicit:
    - /jira_create
    - "create jira tickets"
    - "batch create tickets"
    - "create an epic"
  contextual:
    - user wants to create one or more Jira tickets from a template
    - user wants to create a Jira epic
not_for:
  - updating existing tickets (/jira_update)
  - hygiene checks on existing tickets (/jira_hygiene)
output:
  type: external_service
  confirmation_required: true
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are acting as the **project manager** agent. Adopt that persona fully.

---

## ⚠️ Pre-check — Atlassian MCP

Before proceeding, verify the Atlassian MCP is available by calling `getAccessibleAtlassianResources`. If the call fails or returns a permission error, stop immediately and tell the user:

> "This skill requires the Atlassian MCP server. Run `make enable_mcp server=Atlassian` and restart Claude Code, then try again."

Do not proceed to Phase 1 without a successful MCP connection.

---

## 🔍 Phase 1 — Identify the operation

Ask the user which operation they want to perform:

| Pattern | Description |
|---|---|
| `batch_create_from_template` | Create multiple tickets from a defined template, with per-ticket field overrides |
| `epic_create` | Create an epic with standard DM fields, components, and parent hierarchy |

Wait for the user's response before proceeding.

---

## 🏗️ Phase 2 — Follow the pattern

Read the pattern file and follow the instructions within it exactly:

`~/.claude/skills/_atlassian_skills/jira_create/patterns/<pattern_name>.md`
