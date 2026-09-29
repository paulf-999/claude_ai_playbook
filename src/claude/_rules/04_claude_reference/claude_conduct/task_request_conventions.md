<!-- version: 1.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-29 -->
# 🎯 Task Request Conventions

**Purpose:** Establish durable, version-controlled conventions for how Claude responds to specific, recurring user request types — patterns that are behavioral, not mechanical, and codified as guidance rules.

> **Scope:** Behavioral conventions for user request patterns (e.g., "add to TODOs", "propose a hook"). Not mechanical enforcement (hooks, tests) — those are governed by `testing.md` and individual enforcement rules.

---

## 🎯 Overview

When a user makes a specific request type, Claude should follow the documented convention. This parent file groups repeatable behavioral patterns — not foundational principles, but rather patterns for handling common, recurring requests. The structure allows grouping related conventions and scales to future patterns (e.g., "when user asks for a plan", "when user says verify").

**Benefits:**
- Conventions are versioned and tracked (not lost in resets)
- Discoverable in one parent file
- Can be applied consistently across sessions
- Easily extended with new convention child files

---

## 📚 Child files (load on-demand)

Each child file documents a specific user request pattern and the expected Claude behavior.

### Task Logging Convention
@~/.claude/_rules/04_claude_reference/claude_conduct/task_request_conventions/_task_logging.md

Convention for "add to TODOs" requests. When a user says "add to TODOs" or "add a TODO", Claude should edit `~/.claude/TODO.md` with a new entry in the Items table.

### Hooks Decision Framework
**Read on demand:** `~/.claude/_rules/05_lazy_load/hooks_decision_framework.md` — before proposing any hook or automation.

ROI criteria and guardrails before proposing automation. When considering hook proposals, evaluate using the framework to prevent low-ROI automation.
