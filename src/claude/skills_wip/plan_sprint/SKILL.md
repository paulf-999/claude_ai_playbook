---
name: plan_sprint
description: Plan a DM sprint — review Jira capacity, identify committed and missing tickets, confirm scope, and optionally update or create the sprint goals Confluence page. Requires the Atlassian MCP server to be enabled (`make enable_mcp server=Atlassian`, then restart Claude Code).
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: wip
  tested: false
tools: mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__createJiraIssue, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Atlassian__updateConfluencePage
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

Plan a Data Management sprint. Work through the steps below in order, waiting for user input at each phase before proceeding.

## ⚠️ Pre-check — Atlassian MCP

Before proceeding, verify the Atlassian MCP is available by calling `getAccessibleAtlassianResources`. If the call fails or returns a permission error, stop immediately and tell the user:

> "This skill requires the Atlassian MCP server. Run `make enable_mcp server=Atlassian` and restart Claude Code, then try again."

Do not proceed to Step 1 without a successful MCP connection.

---

## Step 1 — Gather sprint details

Ask the user in a single message:

1. Sprint number
2. Team capacity — story points per person (1 SP = 1 person-day). Ask for each team member separately.
3. Is there an existing sprint goals Confluence page? If yes, ask for the page URL or ID.

---

## Step 2 — Query Jira

Use `searchJiraIssuesUsingJql` with the following JQL to retrieve all issues assigned in the sprint:

```
project = DM AND sprint = "DM Sprint <number>" ORDER BY assignee ASC
```

For each issue, capture: key, summary, status, story points (if set), assignee.

If no sprint name is known, try `sprint in openSprints() AND project = DM`.

---

## Step 3 — Capacity review

Present a summary table grouped by assignee:

| Person | Capacity (SP) | Committed (SP) | Delta |
|---|---|---|---|

Flag:
- Anyone over capacity
- Anyone with significant slack (>1 SP unused)
- Issues with no story points set
- Issues with no assignee

---

## Step 4 — Review Confluence page (if provided)

If the user provided an existing sprint goals page, read it using `getConfluencePage` (markdown format is sufficient here).

Cross-reference the Confluence Must/Should items against the Jira issues:
- Items on the Confluence page with no linked Jira ticket — flag these
- Jira issues not reflected on the Confluence page — flag these

Present the gaps to the user and ask:
1. Should any missing Jira tickets be created?
2. Should the Confluence page be updated to reflect the confirmed sprint scope?

---

## Step 5 — Create missing Jira tickets (optional)

If the user wants to create tickets for untracked items:

For each item, collect:
- Summary (title)
- Description (key tasks)
- Story points
- Assignee

Create each issue using `createJiraIssue` in project `DM` with type `Story`. Confirm each ticket key back to the user.

---

## Step 6 — Update Confluence page (optional)

If the user wants to update the existing sprint goals page:

Read the current page in ADF format. Add or update rows in the Must/Should/Blocked tables to reflect the confirmed sprint scope. Use `updateConfluencePage` with `contentFormat: adf`.

If no page exists yet, offer to create one using the `data_platform_sprint_goals` pattern from `/create_confluence_page`.
