---
name: togaf_prep
description: Active recall drill for TOGAF Level 1 cert prep — reads local study notes, prioritises weak themes, and drills one exam question at a time.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
triggers:
  explicit:
    - /togaf_prep
  contextual:
    - user wants to practice TOGAF exam questions
    - user asks to drill TOGAF concepts
not_for:
  - reading or editing the notes files themselves
  - answering general TOGAF questions outside a drill session
output:
  type: conversational
  confirmation_required: false
---

## Scope gate

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

# 🎓 TOGAF Cert Prep — Active Recall Drill

Notes path: `~/_drafts/togaf/`

---

## 📂 Phase 1 — Load & confirm focus

1. Read `readiness.md` — extract all theme scores
2. Read all 8 topic files: `adm.md`, `architecture_domains.md`, `architecture_repository.md`, `building_blocks.md`, `enterprise_continuum.md`, `governance.md`, `principles.md`, `stakeholders_views.md`
   - **Do NOT read `revision_list.md`** — it contains answers and would bias the drill
3. Identify the 3 weakest themes (lowest % in the readiness tracker)
4. Present a summary:
   - Overall readiness score
   - Full theme score table with 🔴/🟡/🟢 indicators
   - Proposed drill order (weakest first)
5. Ask: "Drill weakest themes first, or focus on a specific theme?" — wait for reply before starting

---

## 🔁 Phase 2 — Drill loop

Ask **one question at a time**. Draw questions from the `🎯 Exam trigger` callouts in the notes. Drill 🔴 themes before 🟡 themes.

**Question format:**
> **Q[N] — [Theme name]:** [exam trigger question]

Wait for the user's answer. Then reveal the correct answer and ask them to self-score:
- ✅ Got it
- ⚠️ Partial / needed a prompt
- ❌ Missed it

Track scores per theme internally. After every 10 questions, output a mini-summary:

> **After Q10:** Key Concepts ✅✅⚠️ | Principles ✅❌⚠️ | Governance ⚠️✅✅

Continue until the user types `done`, `stop`, or `summary`.

---

## 📊 Phase 3 — Session summary

Output a score table:

| Theme | Qs | ✅ | ⚠️ | ❌ | % |
|---|---|---|---|---|---|
| [theme name] | N | N | N | N | N% |

Then list all ❌ items for revision:

> **Add to revision list:**
> - [question] → [correct answer]

The user updates `~/_drafts/togaf/revision_list.md` manually — this skill does not write files.
