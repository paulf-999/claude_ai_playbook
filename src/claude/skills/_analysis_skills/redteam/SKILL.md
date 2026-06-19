---
name: redteam
description: Adversarial critique — find the weakest assumptions, most exploitable failure points, and strongest counter-arguments in any plan, design, or proposal.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
triggers:
  explicit:
    - /redteam
    - "red team this"
    - "tear this apart"
    - "find the weaknesses"
    - "steelman against this"
  contextual:
    - user wants adversarial critique before committing to an approach
not_for:
  - backward-from-failure analysis — use /premortem
  - forward-looking implementation traps — use /pitfalls
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

## 🔴 Red Team

Approach this as an adversary trying to disprove, defeat, or exploit the proposal — not as a neutral reviewer.

### Step 1 — Identify the subject
Extract the plan, design, or argument being red-teamed from context. If ambiguous, ask.

### Step 2 — Verdict
Open with a one-line verdict: **Strong**, **Shaky**, or **Broken** — and a single sentence justifying it.

### Step 3 — Attack vectors
Identify the 3–5 weakest points. For each:
- **Assumption being attacked** — what belief is this built on?
- **How to exploit it** — what specific scenario breaks it?
- **Severity** — High / Medium / Low

Order by severity descending.

### Step 4 — Strongest counter-argument
State the best single argument *against* the plan as if making the case to kill it.

### Step 5 — Suggested defences
For each High/Medium attack vector: one concrete change that closes the gap.

---

## 📋 Output format

**Verdict:** [Strong / Shaky / Broken] — [one sentence]

**Attack vectors:**
| # | Assumption | Exploit scenario | Severity |
|---|---|---|---|

**Strongest counter-argument:** [paragraph]

**Defences:**
- Attack N: [action per High/Medium vector]
