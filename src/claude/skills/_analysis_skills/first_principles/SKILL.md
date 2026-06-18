---
name: first_principles
description: Strip all assumptions, identify atomic truths, and rebuild a solution from scratch — useful when questioning inherited designs.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
triggers:
  explicit:
    - /first-principles
    - "first principles"
    - "strip the assumptions"
    - "start from scratch"
    - "what do we actually know"
  contextual:
    - user is questioning an inherited design or approach
    - user wants to rebuild reasoning without inherited constraints
not_for:
  - forward-looking trap-spotting — use /pitfalls
  - adversarial critique — use /redteam
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

## 🧱 First Principles

Strip inherited conventions, received wisdom, and untested assumptions. Identify only what is demonstrably true, then rebuild from there.

### Step 1 — Identify the subject
Name the design, decision, or approach being decomposed. If not clear from context, ask.

### Step 2 — Surface the assumptions
List every assumption baked into the current approach — explicit and implicit. Mark each:
- **Inherited** — came with the design, never questioned
- **Untested** — believed to be true but not verified
- **Validated** — tested and confirmed

### Step 3 — Atomic truths
What do we actually know to be true, independent of the inherited design? List only facts that can be verified — constraints, data, requirements, measured behaviour.

### Step 4 — Rebuild
Construct an approach using only the atomic truths from Step 3. Do not reintroduce inherited assumptions — if one needs to come back, name it explicitly and justify it.

### Step 5 — Delta
Compare the rebuilt approach to the original. Note:
- What changed and why
- Which inherited assumptions were valid (can be re-added)
- Which were not (should be dropped)

---

## 📋 Output format

**Subject:** [design or decision being decomposed]

**Assumptions stripped:**
| Assumption | Type | Verdict |
|---|---|---|

**Atomic truths:**
- [fact 1]
- [fact 2]

**Rebuilt approach:** [description]

**Delta from original:** [what changed; which assumptions were valid vs invalid]
