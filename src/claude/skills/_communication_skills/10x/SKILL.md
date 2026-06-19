---
name: 10x
description: Rewrite any text sharper and tighter — cut filler, kill hedging, make every sentence earn its place.
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: active
  tested: false
triggers:
  explicit:
    - /10x
    - "10x this"
    - "make this sharper"
    - "tighten this up"
    - "rewrite this"
  contextual: []
not_for:
  - generating new content from scratch — this skill rewrites existing text only
  - stakeholder summaries — use /exec_summary
  - making text sound human — use /ghost (if installed)
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

## ✍️ 10x Rewrite

### What to cut — non-negotiable
- **Filler openers:** "As you know", "It is worth noting", "In order to", "I wanted to"
- **Hedge clusters:** "sort of", "kind of", "perhaps", "it might be the case that"
- **Passive constructions:** rewrite as active where the actor is known
- **Redundant pairs:** "each and every", "first and foremost", "full and complete"
- **Meta-commentary:** sentences that describe what the next sentence will say

### What to preserve
- The author's core argument — do not change the substance
- Technical terms that are precise and necessary
- Intentional emphasis (e.g. deliberate repetition for rhetorical effect)
- The original voice where it is strong

### Output rules
- Rewritten text first, no preamble
- Follow with a one-line note: word count reduction and the single biggest change made
- If the original is already tight (under 20% reducible), say so and return it unchanged

---

## 📋 Output format

[rewritten text]

---
**Cut:** [original word count] → [new word count] · [single biggest change]
