---
name: eli5
description: Explain any concept simply — no jargon, plain analogies, written for someone encountering it for the first time.
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: true
triggers:
  explicit:
    - /eli5
    - "explain like i'm 5"
    - "explain this simply"
    - "how do i explain this to"
    - "in plain english"
  contextual:
    - user needs to explain a technical concept to a non-technical audience
    - user asks how to describe something to their manager or stakeholders
not_for:
  - stakeholder-ready event summaries — use /exec-summary
  - full technical documentation — out of scope for this skill
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

## 🧒 ELI5

### Step 1 — Identify the concept and audience
Extract what needs explaining from context. If the target audience is specified (e.g. "my manager", "a non-technical stakeholder"), note it — the analogy should be drawn from their world, not the technical domain.

### Step 2 — Strip the jargon
List every technical term in the explanation. Replace each with plain English or a concrete object the audience already understands. If a term is unavoidable, define it in one clause before using it.

### Step 3 — Build one anchor analogy
Choose a single everyday situation that mirrors the core mechanism. The analogy must:
- Require no domain knowledge to understand
- Capture the most important structural truth (not a surface similarity)
- Be stated before the explanation, not after

### Step 4 — State the so-what
One sentence: why does this concept matter or what does it change for the person hearing it?

### Output rules
- No bullet lists — write in plain sentences
- Maximum 150 words
- If the concept has a common misconception, name and correct it in one sentence

---

## 📋 Output format

**The short version:** [one sentence — what it is]

**Think of it like:** [anchor analogy]

**What's actually happening:** [2–4 sentences, no jargon]

**Why it matters:** [one sentence]
