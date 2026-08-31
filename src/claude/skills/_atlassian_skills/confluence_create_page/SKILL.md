---
name: confluence_create_page
description: Create a Confluence page using the general_page pattern. Requires Atlassian MCP enabled.
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
tools: Read, mcp__atlassian__createConfluencePage, mcp__atlassian__updateConfluencePage
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## 🚀 How it works

**Phase 1 — Gather page details:** Title, creator, status, purpose, sections

**Phase 2 — Local Draft Review:** Generate markdown draft, request approval, iterate

**Phase 3 — Publish to Confluence:** Create and publish after explicit approval

---

## 📚 Documentation

- **`_phases.md`** — Interactive phases and draft review process
- **`_testing.md`** — Test cases validating core skill behavior
- **`_roadmap.md`** — Phase 2+ planned enhancements (more patterns)

---

## ⏱️ Timeout Protection

This skill includes protection against Confluence API hangs. If a publish takes too long, you'll see a timeout dialog:

**Default behavior:**
- Normal publish: 30–40 seconds
- 2-minute timeout: If still publishing after 120 seconds, shows dialog
- Maximum 6-minute wait: Total elapsed time capped at 360 seconds

**When timeout occurs:**

```
⏱️  CONFLUENCE PUBLISH TIMEOUT

Your page has been publishing for 2 minutes (120 seconds).
Confluence is not responding. Choose an action:

[A]bort   — Cancel now, preserve draft in ~/.claude/_drafts/confluence/
[R]etry   — Cancel and start a fresh publish attempt
[C]ontinue — Wait 4 more minutes (max 6 minutes total)

Enter your choice (A/R/C):
```

**Customization:**
- Use `--timeout-seconds N` to set custom timeout (e.g., `--timeout-seconds 60` for 1 minute)
- Default: 120 seconds (2 minutes)

---

## ⚠️ Known gaps

- Only general_page pattern (MVP) — Additional patterns deferred to Phase 2
- Wide view toggle must be done manually in Confluence (API limitation)

---

## 📌 Prerequisites

- Atlassian MCP server enabled: `make enable_mcp server=Atlassian` + restart Claude Code
- Confluence space `DA` exists and is accessible
