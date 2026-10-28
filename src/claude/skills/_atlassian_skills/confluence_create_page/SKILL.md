---
name: confluence_create_page
description: Create, add, write or publish a Confluence page (or publish a local draft to Confluence) from the general_page or platform_risk_assessment template, with a local draft you approve first. Requires the Atlassian MCP server.
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
  date_created: "2026-06-07"
  date_updated: "2026-10-28"
tools: Read, Write, mcp__atlassian__getAccessibleAtlassianResources, mcp__atlassian__createConfluencePage, mcp__atlassian__updateConfluencePage
---
<!-- version: 1.5.0 -->
<!-- created: 2026-04-08 -->
<!-- updated: 2026-10-28 -->

## 🤖 Instructions for Claude

- **Read first:** read `reference/_implementation.md` before acting, and follow its phases in order.
- **Pre-check:** call `getAccessibleAtlassianResources` to confirm Atlassian access works and to get the cloud ID.
  - **On failure:** stop and tell the user to run `make enable_mcp server=Atlassian` and restart Claude Code.
- **Never:** call `createConfluencePage` or `updateConfluencePage` until the user has approved the local draft — even when asked to "just publish".
- **Never:** infer the target space or parent page — confirm both with the user, and never publish at the space root.
- **Always:** write the draft to `~/_drafts/confluence/YYYY_MM_DD_<topic>.md`, expanding `~` to the user's absolute home path before calling Write.
  - **Never:** write drafts inside the Claude config folder.
- **Always:** create the page with `status: draft`, so nothing goes live without the user publishing it in Confluence.

## 🎯 Purpose

Create a Confluence page from a team-approved template, with a local draft you review and approve before anything is published:
- **Gather details** — title, creator, status, purpose, and sections
- **Local draft review** — generates a markdown draft, asks for approval, and iterates on your feedback before publishing
- **Explicit publish** — only writes to Confluence after you approve the draft

## 💡 Example Usage

```
$ /confluence_create_page create a page about the Q3 roadmap
[Phase 1] Gathering details: title, creator, status, purpose, sections
[Phase 2] Local draft ready — review at ~/_drafts/confluence/2026_09_30_q3_roadmap.md
          Approve, request changes, or cancel? (y/e/n): y
[Phase 3] Publishing to Confluence...
          ✓ Page created

Page created: https://yourteam.atlassian.net/wiki/spaces/<SPACE_KEY>/pages/12345
```

## ✨ Best For

One-off pages using the general_page pattern, or a Platform Risk & Maturity Assessment using the platform_risk_assessment pattern, in the space you confirm (`<SPACE_KEY>`). Currently at the **tactical** development stage — main path plus light error handling, not full edge-case coverage. Only these two patterns are supported; the wide-view toggle still has to be set manually in Confluence.

## 📚 References

- `reference/_implementation.md` — the interactive phases and the mandatory local draft review, in full
- `reference/patterns/_general_page.md` — the general_page pattern, followed in Phase 2
- `reference/patterns/_platform_risk_assessment.md` — the platform_risk_assessment pattern, followed in Phase 2
- `reference/_error_recovery.md` — what to do when Confluence access, drafts, or publishing fail
- `reference/_troubleshooting.md` — symptoms, causes and fixes, including a stray draft folder and a publish that fails part-way
- `reference/_confluence_page_formatting.md` — page header structure and formatting rules
- `_reference/_quality_scorecards/skills/scorecard_confluence_create_page.md` — 7-dimension quality assessment

## 📌 Prerequisites

- Atlassian MCP server enabled: `make enable_mcp server=Atlassian` + restart Claude Code
- The target Confluence space (`<SPACE_KEY>`) exists and you can write to it
