# 🔧 Claude Operational Discipline

**Purpose:** Establish principles and decision frameworks for how Claude operates intentionally — preserving reasoning capability through deliberate choices about tool usage, automation, and monitoring for inefficiency.

## 📋 Contents

- [Token awareness](#-token-awareness)
- [Default behaviours](#-default-behaviours)
- [When to delegate](#-when-to-delegate) — `claude_when_to_delegate.md`
- [Turn budgets](#-turn-budgets) — automation turn constraints; `turn_budgets.md`
- [Intervention mode](#-intervention-mode)
- [External system access](#-external-system-access)
- [Task request conventions](#-task-request-conventions)

---

## ⚖️ Token awareness

- **Don't parallelise for its own sake:** prefer targeted, scoped operations over broad sweeps where the output would be equivalent.
  - **Note:** parallelise only where it reduces real wait time or produces meaningfully better results.

---

## ⚡ Default behaviours

- **Parallel tool calls:** execute independent operations concurrently — serialise only where there is a genuine dependency.
- **No redundant reads:** do not re-read files or re-fetch data already in the current session's context.
- **Reuse before creating:** check for existing hooks, utilities, and patterns before proposing new ones.
- **No context restating:** do not summarise content already visible in the conversation window.
- **Sub-agent justification:** the primary justification for spawning a sub-agent is context isolation — protecting the main window from large or irrelevant content; parallelism alone is not sufficient.

---

## 🤝 When to delegate

@~/.claude/_rules/03_claude_reference/claude_conduct/claude_when_to_delegate.md

---

## 🔄 Turn budgets

@~/.claude/_rules/03_claude_reference/claude_conduct/turn_budgets.md

---

## 🚩 Intervention mode

- **Flag, don't block:** when inefficiency is detected, flag it but do not block execution.
  - **Example:** "Flagging: this read duplicates one already in context — skipping."
  - **Note:** intervene only where the waste is clear and material — re-reading a file just read, spawning a sub-agent for a single tool call, re-summarising context already in the window.

---

## 🔐 External system access

@~/.claude/_rules/03_claude_reference/claude_conduct/external_system_access.md

---

## 📋 Task request conventions

@~/.claude/_rules/03_claude_reference/claude_conduct/task_request_conventions.md

---

## 🔗 Related rules

- `behaviour.md` — safe defaults and decision-making patterns
  - `_session_conduct.md` — interpersonal honesty and responsiveness
  - `_model_selection_strategy.md` — when to escalate models
