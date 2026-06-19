---
name: compare
description: Structured side-by-side comparison of two or more options with consistent criteria and a clear recommendation.
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
triggers:
  explicit:
    - /compare
    - "compare X vs Y"
    - "side by side"
    - "which is better"
  contextual:
    - user is choosing between two or more tools, approaches, or designs
not_for:
  - adversarial critique of a single option — use /redteam
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

## ⚖️ Compare

### Step 1 — Parse the options
Extract what is being compared. If only one option is given, ask for the alternative.

### Step 2 — Identify relevant criteria
Derive criteria from context (e.g. for a technology choice: cost, operational complexity, team familiarity, scalability, lock-in). State the criteria before populating the table so the user can adjust.

Label each criterion's weight: **Critical**, **Important**, or **Nice-to-have**.

### Step 3 — Populate the comparison table
One row per criterion. Rate each option: ✅ Strong / ⚠️ Acceptable / ❌ Weak.

### Step 4 — Recommendation
Give a direct recommendation with a 2–3 sentence rationale. State any conditions under which the other option would be the right call instead.

---

## 📋 Output format

**Comparing:** [Option A] vs [Option B]

| Criterion | Weight | [Option A] | [Option B] |
|---|---|---|---|

**Recommendation:** [Option] — [rationale]

**When to choose [the other option] instead:** [condition]
