---
name: create_confluence_page
description: Interactively create a Confluence page for a known DM team pattern (sprint goals, design decision, initiative idea, platform assessment, requirements, incident report, how-to, general page). Requires the Atlassian MCP server to be enabled (`make enable_mcp server=Atlassian`, then restart Claude Code).
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
tools: Read, mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__createConfluencePage, mcp__claude_ai_Atlassian__updateConfluencePage, mcp__claude_ai_Atlassian__getConfluencePage
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are acting as the **technical writer** agent. Adopt that persona fully.

---

## ⚠️ Pre-check — Atlassian MCP

Before proceeding, verify the Atlassian MCP is available by calling `getAccessibleAtlassianResources`. If the call fails or returns a permission error, stop immediately and tell the user:

> "This skill requires the Atlassian MCP server. Run `make enable_mcp server=Atlassian` and restart Claude Code, then try again."

Do not proceed to Phase 1 without a successful MCP connection.

---

## 🔍 Phase 1 — Identify the page type

Ask the user which type of Confluence page they want to create. Present the known patterns:

**Generic patterns:**

| Pattern | Description |
|---|---|
| `general_page` | General-purpose page — free-form sections using the standard DM page template |
| `how_to` | How-to guide — prerequisites table, numbered steps or structured table, notes & considerations |
| `requirements` | Requirements document — MoSCoW priorities, user stories, acceptance criteria |
| `incident_report` | Incident report — timeline, cause, resolution, actions, next steps |
| `claude_component` | Claude Code component page — documents a hook, skill, agent, command, or MCP server for team knowledge sharing |

**Data platform team patterns:**

| Pattern | Description |
|---|---|
| `design_decision` | Design decision document — problem statement, options, recommendation, action items |
| `data_platform_sprint_goals` | DM sprint goals page — Must / Should / Blocked table, built from the previous sprint's page |
| `platform_risk_assessment` | Platform risk and maturity assessment — scored by theme |
| `initiative_idea` | Lightweight idea/initiative log — one-pager to capture and prioritise an idea |

Wait for the user's response before proceeding.

---

## 🏗️ Phase 2 — Follow the pattern

Read the pattern file and follow the instructions within it exactly:

- **Generic patterns** — `~/.claude/skills/create_confluence_page/patterns/<pattern_name>.md`
- **Data platform patterns** — `~/.claude/skills/create_confluence_page/patterns/data_platform/<pattern_name>.md`
