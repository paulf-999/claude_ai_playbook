---
name: pitfalls
description: Forward-looking trap-spotting — surfaces implementation traps, integration risks, and hidden dependencies before work begins.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
triggers:
  explicit:
    - /pitfalls
    - "what could go wrong"
    - "surface the traps"
    - "what am I missing"
    - "flag the risks"
  contextual:
    - user is about to start implementation and wants to catch problems early
not_for:
  - backward-from-failure analysis — use /premortem
  - adversarial critique of a proposal — use /redteam
output:
  type: conversational
  confirmation_required: false
tools: []
---

## 📊 Scope gate

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## ⚠️ Pitfalls

Work forward from the current plan to identify what will bite the team during execution — not hypothetical failure modes but practical traps that are easy to miss.

### Categories to check

- **Implementation traps** — steps that look simple but have hidden complexity or ordering constraints
- **Integration risks** — external systems, APIs, or dependencies that may behave unexpectedly
- **Hidden assumptions** — things the plan implicitly relies on that haven't been validated
- **Rollback/recovery gaps** — what happens if a step partway through needs to be undone
- **Testing blind spots** — parts of the implementation that are hard to test or verify

### Output rules

- Rank by likelihood of actually being hit (high → low)
- Be specific — name the exact component, step, or dependency, not a generic warning
- Include a one-line mitigation for each pitfall

---

## 📋 Output format

**Pitfalls for:** [subject]

| # | Pitfall | Category | Likelihood | Mitigation |
|---|---|---|---|---|
