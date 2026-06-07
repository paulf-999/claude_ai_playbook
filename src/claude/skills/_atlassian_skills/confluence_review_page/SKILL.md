---
name: confluence_review_page
description: Generate and post a structured Claude review comment on a Confluence page — scored across structure, completeness, clarity, consistency, and links & references.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools: Agent, mcp__claude_ai_Atlassian__getAccessibleAtlassianResources, mcp__claude_ai_Atlassian__getConfluencePage, mcp__claude_ai_Atlassian__getConfluencePageFooterComments, mcp__claude_ai_Atlassian__createConfluenceFooterComment
schema: skill_schema.yaml
---

## Scope gate

This skill is at **draft** maturity — happy path only.

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## ⚠️ Pre-check — Atlassian MCP

Before proceeding, call `getAccessibleAtlassianResources`. If it fails, stop:

> "This skill requires the Atlassian MCP server. Run `make enable_mcp server=Atlassian` and restart Claude Code, then try again."

---

## 🔍 Phase 1 — Identify the page

See [phase1.md](phase1.md) — identifies the page from a passed argument or prompts the user.

---

## 📥 Phase 2 — Fetch page data

See [phase2.md](phase2.md) — fetches page content, space, author, version, and existing comments in parallel.

---

## 🤖 Phase 3 — Analyse

Use the Agent tool with `subagent_type: technical_writer`. Pass:
- Page title, space key, author, last modified date
- Page body content (truncate to 3000 words if longer; note truncation in the review)
- The output format and scoring guidance from [comment_format.md](comment_format.md)

Instruct the agent to produce **only** the structured output defined in `comment_format.md` — no preamble, no trailing commentary.

---

## ✅ Phase 4 — Format and confirm

Show the full review comment to the user and ask:

> "Post this as a footer comment on \"<page_title>\"? (y/n)"

If the user says no, stop.

---

## 💬 Phase 5 — Post the comment

Write the comment body to `/tmp/review_confluence_<page_id>.md`, then post via `createConfluenceFooterComment`.

Return the Confluence page URL.

---

> TODO (tactical): detect page pattern from title/content and pass to reviewer for pattern-specific completeness scoring
> TODO (tactical): guard against posting a duplicate review if one already exists from a prior run
> TODO (tactical): handle ADF body formats that produce very long plain-text extractions
