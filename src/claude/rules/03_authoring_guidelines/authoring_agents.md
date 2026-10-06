---
paths:
  - "**/agents/**"
---
<!-- version: 1.3.1 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-06 -->
<!-- miss_cost: low — agents drift from the house structure -->
<!-- loading: path-scoped — loads with agent files through paths:, and through a pointer in authoring_rules.md for a new agent -->
# 🛠️ Agent Authoring

**Purpose:** Establish standardized process for creating agents that ensures clarity, consistency, and intentionality. One concept per agent.

---

## 🧭 Quick Navigation

**New agent author?** Start here in order:
1. **Core Standards** — Naming pattern, structure, maturity levels, testing requirements
2. **Decision Tree** — When to create an agent vs. rule vs. skill
3. **5-Step Creation Process** — Workflow: name → contract → AGENT.md → evals → score
4. **Hard Gates Checklist** — Final validation before finalizing

**Experienced author, need to refresh?** Jump to specific child files:
- **Scope Boundaries** — Defining what your agent does NOT do (`_scope_and_maturity.md`)
- **Maturity Justification** — Choosing Draft vs. Tactical vs. Strategic (`_scope_and_maturity.md`)
- **Common Mistakes** — Catch anti-patterns (`_common_mistakes.md`)

**Reviewing someone else's agent?** Use these child files:
- **Hard Gates Checklist** (below) — Verify completeness
- **Common Mistakes** — Catch anti-patterns
- **Maturity Justification** — Verify evidence-based maturity

---

## 📚 Read on demand

Before creating or reviewing an agent, read the children below in order.

- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_agents/_core_standards.md` — Core Standards: naming pattern, structure, maturity levels and testing requirements.
- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_agents/_decision_tree_and_process.md` — Decision Tree & Creation Process: agent vs. rule vs. skill, then the 5-step workflow.
- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_agents/_scope_and_maturity.md` — Scope Boundaries & Maturity Justification: what the agent does not do, and why its maturity fits.
- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_agents/_hard_gates_checklist.md` — Hard Gates Checklist: the final validation before finishing an agent.
- **Read on demand:** `~/.claude/_rules_lazy_load/authoring_agents/_common_mistakes.md` — Common Mistakes & Anti-Patterns: what to catch when writing or reviewing.
