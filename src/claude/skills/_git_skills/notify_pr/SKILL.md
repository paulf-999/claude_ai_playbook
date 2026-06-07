---
name: notify_pr
description: Post a Teams channel notification after raising a PR. Repo-agnostic — reviewer pools and layer mappings are defined per-repo in teams_config.json. Resolves reviewers from a local cache (GitHub → Teams mapping), falling back to the Microsoft 365 MCP for unknown users.
version: 1.1.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
tools: Bash, Read, Write
triggers:
  explicit:
    - /notify_pr
    - /notify_pr <number>
  contextual:
    - auto-triggered at end of /create_pr when user opts in
not_for:
  - creating a PR — use /create_pr instead
  - posting a GitHub review comment — use /git_review_pr instead
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

## Output style

- **Phase 1** — silent. No output.
- **Phase 2** — print a concise PR summary so the context is clear:
  ```
  PR #N — <title>
  Files: <path> → <layer>, <path> → <layer>
  Change Type: <type>
  ```
- **Phase 3** — print the reviewer confirmation prompt only (already defined in Phase 3a). No other output.
- **Phase 4** — print a confirmation prompt showing the proposed title and resolved reviewer list. Wait for approval before posting. Then print the post result.

---

## Overview

Posts a formatted Teams notification for a GitHub PR. See [phase4.md](phase4.md) for the full message format and payload examples.

---

## Setup

See [setup/overview.md](setup/overview.md) — teams_config.json schema, webhook setup steps, and reviewer cache format.

---

## Phase 1 — Config check

1. Run `pwd` to get the current working directory.

2. Derive the project memory directory: take the CWD, prefix with `~/.claude/projects/`, and replace every `/` with `-`. Use `ls ~/.claude/projects/` and match the closest directory if the derived path doesn't exist exactly.

3. Check for `teams_config.json` in that directory.
   - **Not found** — stop and tell the user:
     > "No Teams config found for this repo. Create `<memory_dir>/teams_config.json` with the required structure (see skill README). Set up the incoming webhook in Teams: channel → Manage channel → Connectors → Incoming Webhook."
   - **Found** — read and extract:
     - `webhook_url`
     - `go_to_reviewers` — object with `uk_ireland` and `north_america` keys, each containing `window.start`, `window.end`, and `handles` array
     - `layers` — array of `{prefix, label}` objects (may be empty)

4. Check for `github_teams_mapping.json` in the same directory.
   - **Not found** — create it as `{}` using the Write tool.
   - **Found** — read and parse it as the reviewer cache.

---

## Phase 2 — Get PR metadata

See [phase2.md](phase2.md) — PR number, title, author, reviewer handles, change type, and DWH layer detection.

---

## Phase 3 — Resolve reviewers

See [phase3.md](phase3.md) — reviewer handle lookup, window-based selection, and Teams AAD ID resolution.

---

## Phase 4 — Build message and post

See [phase4.md](phase4.md) — message assembly, Adaptive Card / MessageCard format, and Teams webhook POST.
