# 🔧 Claude Operational Discipline

**Purpose:** Establish principles and decision frameworks for how Claude operates intentionally — preserving reasoning capability through deliberate choices about tool usage, automation, and monitoring for inefficiency.

## 📋 Contents

- [Default behaviours](#-default-behaviours)
- [Intervention mode](#-intervention-mode)
- [When to delegate](#-when-to-delegate) — `_claude_when_to_delegate.md`
- [Token awareness](#-token-awareness)

---

## ⚡ Default behaviours

- **Parallel tool calls:** execute independent operations concurrently — serialise only where there is a genuine dependency.
- **No redundant reads:** do not re-read files or re-fetch data already in the current session's context.
- **Reuse before creating:** check for existing hooks, utilities, and patterns before proposing new ones.
- **No context restating:** do not summarise content already visible in the conversation window.
- **Sub-agent justification:** the primary justification for spawning a sub-agent is context isolation — protecting the main window from large or irrelevant content; parallelism alone is not sufficient.

## 🚩 Intervention mode

- **Flag, don't block:** when inefficiency is detected, flag it but do not block execution.
  - **Example:** "Flagging: this read duplicates one already in context — skipping."
  - **Note:** intervene only where the waste is clear and material — re-reading a file just read, spawning a sub-agent for a single tool call, re-summarising context already in the window.

## 🤝 When to delegate

@~/.claude/_rules/03_claude_reference/claude_conduct/_claude_when_to_delegate.md

## ⚖️ Token awareness

- **Don't parallelise for its own sake:** prefer targeted, scoped operations over broad sweeps where the output would be equivalent.
  - **Note:** parallelise only where it reduces real wait time or produces meaningfully better results.

---

## 🔗 Related rules

- `behaviour.md` — safe defaults and decision-making patterns
  - `_session_conduct.md` — interpersonal honesty and responsiveness
  - `_model_selection_strategy.md` — when to escalate models
- `claude_conduct/` — operational conduct and decision-making
  - `_when_to_delegate.md` — when to delegate vs. handle directly
  - `_turn_budgets.md` — automation turn constraints
