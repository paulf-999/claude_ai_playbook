---
name: ideas
description: Capture and browse Claude-related ideas before they are lost mid-conversation. Stores ideas in the MCP memory server with category, priority, and status metadata. Use when the user says "log an idea", "capture this", or invokes /ideas.
version: 0.1.0
maturity: draft
tags:
  criticality: must
  status: active
  tested: false
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

# 💡 Ideas Logger

Capture and browse ideas using the MCP memory server as persistent storage. Ideas survive across sessions and are accessible from any project.

## 🗄️ Storage model

Each idea is stored as a memory entity:

| Field | Value |
|---|---|
| Entity name | `idea: <title>` |
| Entity type | `idea` |
| Observations | `description`, `category`, `priority`, `status`, `captured` |

---

## ⚠️ Pre-check — verify memory server

Before doing anything else, call `mcp__memory__read_graph`. If it fails or returns an error, stop immediately and tell the user:

> "This skill requires the MCP memory server. Ensure it is installed and active (`make install_core_mcp_servers`), then try again."

Do not proceed without a successful response.

---

## 📋 Phase 1 — Browse existing ideas (optional)

Call `mcp__memory__search_nodes` with query `"idea"`. If any entities of type `idea` are returned, tell the user how many ideas exist and ask:

> "You have N idea(s) logged. View them before capturing a new one? (yes / no)"

If yes, display each idea as:

```
[priority] idea: <title>
  category: <category> · status: <status> · captured: <date>
  <description>
```

Sort by priority order: must → should → could → want.

If no ideas exist, or the user says no, proceed directly to Phase 2.

---

## ✏️ Phase 2 — Capture

Prompt for each field in order. Wait for a response before asking the next.

1. **Title** — one line, descriptive. This becomes the entity name (`idea: <title>`).

2. **Description** — free-form. Can be multi-sentence. Press Enter twice or type "done" to finish.

3. **Category** — one of:
   - `claude` — Claude AI tooling, skills, rules, agents
   - `dx` — developer experience
   - `process` — team workflows and processes
   - `tooling` — general engineering tooling
   - `data-platform` — data stack specific
   - `other`

4. **Priority** — one of: `must` / `should` / `could` / `want`

Once all fields are collected, show a preview:

```
About to log:

  idea: <title>
  description: <description>
  category: <category>
  priority: <priority>
  status: new
  captured: <today's date YYYY-MM-DD>

Confirm? (yes / edit / cancel)
```

If the user says edit, re-prompt the field they want to change. If cancel, stop.

---

## 💾 Phase 3 — Store

Call `mcp__memory__create_entities` with:

```json
[{
  "name": "idea: <title>",
  "entityType": "idea",
  "observations": [
    "description: <description>",
    "category: <category>",
    "priority: <priority>",
    "status: new",
    "captured: <YYYY-MM-DD>"
  ]
}]
```

On success, confirm to the user:

> "Logged: idea: <title>"

> TODO (tactical): handle duplicate entity names — check if an idea with the same title already exists before creating.
> TODO (tactical): add `/ideas list` mode to browse and filter by category or priority without capturing a new idea.
> TODO (tactical): add status update — mark an idea as `done` via `mcp__memory__add_observations`.
