---
name: grill_me
description: Stress-test a plan or design by interviewing the user relentlessly — resolves each branch of the decision tree one question at a time. Use before starting non-trivial work.
version: 0.1.0
maturity: draft
tags:
  criticality: low
  status: active
  tested: true
tools: []
triggers:
  explicit:
    - /grill_me
    - "grill me"
  contextual:
    - user wants to stress-test a plan before implementation
    - user is uncertain about a design decision
not_for:
  - simple or low-risk tasks that don't warrant stress-testing
  - after implementation has already started
output:
  type: conversational
  confirmation_required: false
---

## 🔒 Scope gate

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

## 🔥 Phase 1 — Interview

Interview the user relentlessly about every aspect of the plan until reaching shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one at a time.

Rules:
- Ask **one question at a time** — never batch questions
- For each question, provide your recommended answer before asking the user to respond
- If a question can be answered by exploring the codebase, do so instead of asking
- Stop when the user has confirmed each decision — do not re-litigate settled questions
