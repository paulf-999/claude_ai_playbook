---
name: ooda
description: Structured decision loop for ambiguous or fast-moving problems — Observe, Orient, Decide, Act.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
triggers:
  explicit:
    - /ooda
    - "ooda loop"
    - "walk me through this decision"
    - "help me think through this"
  contextual:
    - user is facing a complex or ambiguous problem with no obvious path forward
    - user needs a structured framework to move from information to action
not_for:
  - backward-from-failure analysis — use /premortem
  - choosing between predefined options — use /compare
  - adversarial stress-testing — use /redteam
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

## 🔄 OODA Loop

Work through the four phases in order. Do not skip or merge phases — each one changes the frame for the next.

### Observe — what do we actually know?
Separate facts from assumptions. List only what can be verified:
- Data points, measurements, events that have occurred
- Constraints that are fixed (deadlines, budget, team capacity)
- Mark anything unverified as **assumed, not confirmed**

### Orient — what does this mean?
Interpret the observations through relevant context:
- What mental models or past patterns apply here?
- What is the threat or opportunity this situation presents?
- What biases or blind spots might be distorting the picture?

### Decide — what are we going to do?
Generate 2–3 options, then commit to one:
- State each option in one sentence
- Name the key trade-off for each
- Give a direct recommendation and the reason

### Act — what happens next?
Make the decision concrete and testable:
- The first specific action, owner, and timeline
- The signal that confirms the decision was right
- The tripwire that would trigger a reassessment

---

## 📋 Output format

**Observe:** [verified facts and constraints — flag assumptions explicitly]

**Orient:** [interpretation — patterns, threats/opportunities, blind spots]

**Decide:**
| Option | Trade-off |
|---|---|
| [A] | [trade-off] |
| [B] | [trade-off] |

**Recommendation:** [option] — [reason]

**Act:** [first action] · Owner: [who] · By: [when] · Signal: [how we know it worked] · Tripwire: [what would change the call]
