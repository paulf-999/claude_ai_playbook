<!-- version: 1.4.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-11 -->
<!-- applies_to: * -->
<!-- miss_cost: high — uncapped automation or non-interactive runs overrun cost before anyone notices -->
<!-- loading: always-on — tool-use and delegation choices come up in every session -->
# 🔧 Claude Operational Discipline

**Purpose:** Establish principles and decision frameworks for how Claude operates intentionally — preserving reasoning capability through deliberate choices about tool usage, automation, and monitoring for inefficiency.

## 📋 Contents

- [Token awareness](#-token-awareness)
- [Default behaviours](#-default-behaviours)
- [When to delegate](#-when-to-delegate) — `_claude_when_to_delegate.md`
- [Turn budgets](#-turn-budgets) — `--max-turns` caps for non-interactive runs; `_turn_budgets.md`
- [Automation controls](#-automation-controls) — caps and kill-switch for `/loop`, `/goal`, `/batch`; `_automation_controls.md`
- [Intervention mode](#-intervention-mode)
- [External system access](#-external-system-access)
- [Task request conventions](#-task-request-conventions)
- [MCP server toggling](#-mcp-server-toggling) — restart requirements after enabling/disabling servers; `_mcp_server_toggling.md`

---

## ⚖️ Token awareness

- **Don't parallelise for its own sake:** prefer targeted, scoped operations over broad sweeps where the output would be equivalent.
  - **Note:** parallelise only where it reduces real wait time or produces meaningfully better results.
- **Read on demand:** `~/.claude/_rules_lazy_load/claude_config/claude_cost/latency_optimisation.md` — when slow or costly API calls are blocking the task.

---

## ⚡ Default behaviours

- **Parallel tool calls:** execute independent operations concurrently — serialise only where there is a genuine dependency.
- **No redundant reads:** do not re-read files or re-fetch data already in the current session's context.
- **Reuse before creating:** check for existing hooks, utilities, and patterns before proposing new ones.
- **No context restating:** do not summarise content already visible in the conversation window.
- **Sub-agent justification:** the primary justification for spawning a sub-agent is context isolation — protecting the main window from large or irrelevant content; parallelism alone is not sufficient.

---

## 🤝 When to delegate

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_claude_when_to_delegate.md`

---

## 🔄 Turn budgets

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_turn_budgets.md`

---

## ⚙️ Automation controls

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md`

---

## 🚩 Intervention mode

- **Flag, don't block:** when inefficiency is detected, flag it but do not block execution.
  - **Example:** "Flagging: this read duplicates one already in context — skipping."
  - **Note:** intervene only where the waste is clear and material — re-reading a file just read, spawning a sub-agent for a single tool call, re-summarising context already in the window.

---

## 🔐 External system access

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_external_system_access.md`

---

## 📋 Task request conventions

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_task_request_conventions.md`

---

## 🔌 MCP server toggling

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_mcp_server_toggling.md`
