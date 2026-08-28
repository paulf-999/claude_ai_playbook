# 🧠 Context window management — options reference

> **Why this matters:** Claude Code shows an "X% until auto-compact" indicator. When the window fills, Claude auto-compacts (summarising history), which can lose detail. The options below keep you well below that threshold through configuration and architecture — not manual intervention.

---

## ⚡ Ranked options

| # | Option | Impact | In use? |
|---|---|---|---|
| 1 | Sub-agents | Highest | ✅ Yes — nudged by hook |
| 2 | Lean CLAUDE.md + `lazy_load/` rules | High | ✅ Yes |
| 3 | Offload to persistent files | Medium-high | ✅ Yes — enforced by rule |
| 4 | One task per session | Medium-high | ✅ Yes — enforced by rule |
| 5 | Auto memory | Medium | ✅ Yes |
| 6 | MCP tool schema deferral | Medium | ✅ Yes |
| 7 | Scope reads | Low-medium | ✅ Yes — nudged by hook |
| 8 | Task tracking over in-context checklists | Low-medium | ✅ Yes — nudged by hook |
| 9 | Skill visibility | Low-medium | ❌ No — skills not installed |
| 10 | `showClearContextOnPlanAccept` | Low | ✅ Yes |

---

## 1. Sub-agents — Highest impact

- **What:** sub-agent reads stay out of the main window; only the summary (~500 tokens) returns, not the raw reads (10K+).
- **How to enable:** use Agent/Explore/Plan tools for research; define custom agents in `.claude/agents/` with `allowedTools` restrictions.
- **Constraining levers** (see also `_rules/context_management.md`):
  - Tight prompt scoping — narrow the task so the agent reads only what's needed.
  - `Explore` sub-agent type — read-only, bounded exploration.
  - Tool restrictions in agent definitions — omit write/bash tools for read-only agents.

## 2. Lean CLAUDE.md + `lazy_load/` rules — High impact

- **What:** each removed import saves its full file size every session.
- **How to enable:** move domain-specific rules to `_rules/lazy_load/`; only import rules needed every session.
- **Status:** ✅ established in v2 reset — `_rules/lazy_load/` structure is in place.

## 3. Offload to persistent files — Medium-high impact

- **What:** decisions, file paths, and build commands written to a project file (`CLAUDE.md`, `TODO.md`) don't need to repeat in conversation; Claude reads the file on demand.
- **How to enable:** establish a convention of writing active decisions to a project-root file rather than restating them in chat.
- **Status:** ✅ enforced by rule in `_rules/context_management.md`.

## 4. One task per session — Medium-high impact

- **What:** limiting each thread to a single discrete task (40–50 messages) prevents design, coding, and debugging context from accumulating in the same window.
- **How to enable:** start a new Claude window between unrelated tasks.
- **Status:** ✅ enforced by rule in `_rules/context_management.md`.

## 5. Auto memory — Medium impact

- **What:** learnings persist across sessions without growing conversation history; only the 200-line index loads at startup.
- **How to enable:** already active (`autoMemoryEnabled: true` in settings).
- **Note:** keep `MEMORY.md` index under 200 lines — lines beyond that are truncated.

## 6. MCP tool schema deferral — Medium impact

- **What:** saves 2,500+ tokens at startup when many MCP tools are registered; schemas load on first use via `ToolSearch`.
- **How to enable:** already the default behaviour — no config needed.

## 7. Scope reads — Low-medium impact

- **What:** every tool result lands in context — reading only relevant lines avoids loading entire large files.
- **How to enable:** use `Read` with `offset`/`limit` to target specific line ranges; use `grep` to locate symbols rather than reading whole modules.
- **Note:** particularly valuable in large repos where a single full file read can consume thousands of tokens.

## 8. Task tracking over in-context checklists — Low-medium impact

- **What:** a running checklist kept in conversation grows the context window with every update; `TaskCreate`/`TaskUpdate` persist outside the context window entirely.
- **How to enable:** use `TaskCreate` at the start of multi-step work; mark each step complete with `TaskUpdate` as you go.
- **Note:** tasks survive `/compact` and `/clear` — in-conversation checklists do not.

## 9. Skill visibility — Low-medium impact

- **What:** ~150–300 tokens saved per hidden skill.
- **How to enable:**
  - Add `disable-model-invocation: true` to skill frontmatter, **or**
  - Set `"visibility": "hidden"` in `settings.json` under `skillOverrides`.
- **Status:** ❌ not applied — skills are visible by default.

## 10. `showClearContextOnPlanAccept` — Low impact

- **What:** prompts to clear context when accepting a plan so implementation starts with a fresh window.
- **How to enable:** already enabled in `settings.json`.

---

## 🖐️ Manual options

> Noted for completeness — not a primary strategy.

- **`/compact [focus on X]`** — summarises history between major tasks; optionally scoped to a focus area.
- **`/clear`** — full reset when switching to an unrelated task.
