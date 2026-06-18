---
name: premortem
description: Failure-first analysis — assume the plan already failed and work backwards to find the specific cause chain.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
triggers:
  explicit:
    - /premortem
    - "run a premortem"
    - "assume this fails"
    - "what could kill this"
  contextual:
    - user wants to stress-test a plan before committing to it
not_for:
  - forward-looking implementation trap-spotting — use /pitfalls
  - adversarial critique of an existing artefact — use /redteam
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

## 💀 Premortem

It is now [timeframe]. The plan has already failed. Not "it might fail" — it **has** failed.

### Step 1 — Confirm subject
Identify (or ask for) the plan, design, or decision being analysed. If clear from context, proceed without asking.

### Step 2 — Set the failure frame
State the failure explicitly before analysing:
> "It is [timeframe]. [Subject] has failed. Now: why?"

Do not hedge or qualify. The failure is the starting premise.

### Step 3 — Generate 3 cause chains
Each chain is a narrative sequence of 3–5 linked events — not a generic risk, but a specific story:
> "Staging wasn't representative → load test missed a Snowflake concurrency limit → first production run hit it → pipeline SLA breached → stakeholder cancelled."

Most plausible chain first.

### Step 4 — Rank by likelihood × impact
State which chain is most likely and briefly explain why.

### Step 5 — Mitigations
For each chain: one concrete action that breaks the chain at its earliest link.

---

## 📋 Output format

**Failure assumed:** [subject] — [timeframe]

**Cause chain 1 (most likely):** [narrative sequence]
**Cause chain 2:** [narrative sequence]
**Cause chain 3:** [narrative sequence]

**Mitigations:**
- Chain 1: [break point and action]
- Chain 2: [break point and action]
- Chain 3: [break point and action]
