---
name: manage_jira
description: Manage Jira tickets and epics for the Data Platform team — batch-create from template, bulk-update fields, run a hygiene check, or create an epic. Requires the Atlassian MCP server to be enabled (`make enable_mcp server=Atlassian`, then restart Claude Code).
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: wip
  tested: false
tools: Read, mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__createJiraIssue, mcp__claude_ai_Atlassian__editJiraIssue, mcp__claude_ai_Atlassian__transitionJiraIssue
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

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

## 🔍 Phase 1 — Identify the pattern

Ask the user which operation they want to perform:

| Pattern | Description |
|---|---|
| `batch_create_from_template` | Create multiple tickets from a defined template, with per-ticket field overrides |
| `bulk_update` | Update one or more fields across multiple tickets matched by a JQL filter |
| `hygiene_check` | Scan tickets for missing or incorrect fields and surface a report — optionally auto-fix |
| `epic_create` | Create an epic with standard DM fields, components, and parent hierarchy |

Wait for the user's response before proceeding.

---

## 🏗️ Phase 2 — Follow the pattern

Read the pattern file and follow the instructions within it exactly:

`~/.claude/skills_wip/data_platform/manage_jira/patterns/<pattern_name>.md`
