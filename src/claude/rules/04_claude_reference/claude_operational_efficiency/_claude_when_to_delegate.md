<!-- version: 2.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-06 -->
# 🤝 Claude When to Delegate

**Purpose:** Decide whether to run a command yourself, hand it to the user, or spawn a sub-agent — saving turns and context.

---

## 👤 Delegating to the user

| Situation | Action |
|---|---|
| Output gates the next step (test failures, git state, file content, env vars) | Run it in Claude |
| Copy-paste safe, self-contained and safe to retry (install, build, test, format, cleanup) | Offer the user the command |

- **Offer format:** show the command in a code block, say what it does in one sentence, and add "Or I can run it and continue."
- **Wait:** get an explicit yes or no, and don't run verification until the user reports back.
- **On error:** ask for the output, diagnose it, then offer a fix or run the corrected command.

## 🤖 Delegating to a sub-agent

- **Read on demand:** `~/.claude/_rules_lazy_load/delegating_to_subagent.md` — before spawning a sub-agent, for the decision table, constraints and token-cost breakeven.
