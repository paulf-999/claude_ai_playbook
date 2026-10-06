<!-- version: 2.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-30 -->
# 🎛️ Model Selection Strategy

**Purpose:** Flag a model switch when the task and the active model clearly don't match — saving cost on simple work and rework on complex work.

---

- **Flag at task start:** if the task needs multi-step reasoning, complex code, review or long-form writing and a small model is active, suggest `/model sonnet` (or `/model opus`) before starting.
- **Flag mid-session:** if a simple task grows into analysis or refactoring, say so and suggest switching up.
- **Flag the reverse:** if a large model is active for summarising, formatting or quick Q&A, mention that Haiku would do.
- **Flag, don't block:** give a one-line suggestion, then carry on with the active model unless the user switches.
