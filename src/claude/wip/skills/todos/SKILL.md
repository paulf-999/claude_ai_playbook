---
name: todos
description: Lightweight todo tracker for Claude work items. Add, list, and close todos backed by the MCP memory server. Use when the user says "add a todo", "what's on my list", or "mark done". Invoked as /todos, /todos list, or /todos done <title>.
version: 0.1.1
maturity: draft
tags:
  criticality: should
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

# ✅ Todo Tracker

Add, list, and close actionable work items using the MCP memory server as persistent storage. Todos survive across sessions and are accessible from any project.

## 🗄️ Storage model

Each todo is stored as a memory entity:

| Field | Value |
|---|---|
| Entity name | `todo: <title>` |
| Entity type | `todo` |
| Observations | `description`, `priority`, `status`, `captured`, `source` |

## 🔀 Modes

| Invocation | Behaviour |
|---|---|
| `/todos` or `/todos add` | Prompt for title, then add immediately |
| `/todos add <title>` | Add a todo with the given title immediately — no prompting |
| `/todos list` | Show open and in-progress todos |
| `/todos done <title>` | Mark a todo as done |

---

## ⚠️ Pre-check — verify memory server

Before doing anything else, call `mcp__memory__read_graph`. If it fails, stop and tell the user:

> "This skill requires the MCP memory server. Ensure it is installed and active (`make install_core_mcp_servers`), then try again."

Do not proceed without a successful response.

---

## ➕ Mode: add

Todos are captured immediately with no prompting. The goal is speed — the user is capturing an idea before it is lost.

**If a title is provided in the args** (e.g. `/todos add <title>`), use it directly and add without any interaction.

**If no title is provided** (bare `/todos` or `/todos add`), prompt for the title only, then add immediately.

Never prompt for description, priority, or source. Apply these defaults silently:

| Field | Default |
|---|---|
| `description` | Same as title |
| `priority` | `should` |
| `source` | `manual` |

Call `mcp__memory__create_entities`:

```json
[{
  "name": "todo: <title>",
  "entityType": "todo",
  "observations": [
    "description: <title>",
    "priority: should",
    "status: open",
    "captured: <YYYY-MM-DD>",
    "source: manual"
  ]
}]
```

Confirm: `"Added: todo: <title>"`

---

## 📋 Mode: list

Call `mcp__memory__search_nodes` with query `"todo"`.

Filter results to entities where:
- `entityType` is `todo`
- observations do not contain `status: done`

Display sorted by priority (must → should → could → want):

```
[must]   todo: <title> · open
         <description>

[should] todo: <title> · in-progress
         <description>
```

Report total: `"X open todo(s)"`

If no open todos exist, report: `"No open todos."`

---

## ✅ Mode: done

Extract the title from the invocation — everything after `/todos done ` is the title.

Call `mcp__memory__search_nodes` with query `"todo: <title>"` to confirm the entity exists.

If not found, report: `"No todo found matching '<title>'. Use /todos list to see current todos."`

If found, call `mcp__memory__add_observations`:

```json
{
  "entityName": "todo: <title>",
  "observations": [
    "status: done",
    "completed: <YYYY-MM-DD>"
  ]
}
```

Confirm: `"Done: todo: <title>"`

> TODO (tactical): add `/todos in-progress <title>` to mark status as in-progress.
> TODO (tactical): add filtering in list mode by priority or source.
> TODO (tactical): handle partial title matching — current implementation requires exact title.
