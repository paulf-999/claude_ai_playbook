# 🔄 Turn Budgets

**Purpose:** Establish constraints on turns for non-interactive automation to prevent runaway sessions and cost overrun.

---

## 🎯 Core principle

Unbounded turns are a known source of significant cost overrun. Always cap turns when invoking Claude Code non-interactively (skills, automation, CI/CD).

---

## 📋 Turn budget discipline

**Use `--max-turns N` on every non-interactive invocation**

- **Default:** 20 turns is reasonable for most tasks
- **Higher cap:** If a task genuinely needs more turns, set it deliberately — don't remove the limit hoping it will be fine
- **Scope before invoking:** Plan the critical path before launching so it completes within the turn budget

---

## 📊 Turn budget examples

| Scenario | Recommended Cap | Rationale |
|----------|-----------------|-----------|
| Simple automation (linting, formatting) | 5–10 | Single, well-scoped operation |
| Code generation or refactoring | 15–20 | May need iteration or verification |
| Multi-step workflows (build + test + deploy) | 20–30 | Several sequential steps |
| Open-ended research or exploration | 25–50 | Unpredictable scope; higher cap needed |
| CI/CD pipelines (strict requirements) | 10–15 | Must be predictable and fast |

---

## 🚫 Red flags (adjust cap or reconsider automation)

- **Task hitting turn limit repeatedly** — scope is bigger than estimated; increase cap or decompose task
- **Unclear success criteria** — automation needs clear exit condition; clarify before running
- **Manual spot-checks needed** — if human judgment required mid-run, automation may not be appropriate

---

## 🔗 Related

- `context_management.md` — automation and delegation context
- `behaviour/_session_conduct.md` — how Claude conducts itself in sessions
