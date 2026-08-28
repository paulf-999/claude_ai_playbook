| Field | Value |
|---|---|
| **Description** | Audit your global Claude config across four core quality dimensions. Receive scorecard with A-F grade, gap analysis, and actionable recommendations. |
| **Version** | 0.1.0 |
| **Maturity** | Draft |
| **Tested** | Yes (34 tests) |

---

## 🎯 What this skill does

Audits your global Claude config across four quality dimensions: testing, security, documentation, and standards compliance. Produces a scorecard with per-dimension scores, overall grade (A-F), a MoSCoW prioritisation table of missing elements, and actionable recommendations.

---

## 📋 Can do

- Score global config (`~/.claude/`) against four distinct quality dimensions
- Produce detailed scorecard with per-dimension scores and overall grade
- Generate MoSCoW table (Must/Should items only)
- Create recommendations table with severity ratings
- Optionally apply fixes to both `~/.claude/` and playbook repo source

---

## 🚫 Can't do

- Review single rule files in isolation (read the file directly instead)
- Review playbook repo structure (use `/audit_skills` or `/audit_agents` instead)
- Enforce compliance automatically — only scores subjectively

---

## 📌 Prerequisites

- Access to `~/.claude/` config files
- Bash, Read, and Agent tools available

---

## 🔍 How it works

**Phase 1: Audit and score**
- Read key artefacts: CLAUDE.md, rules, memory index, aliases, settings
- Score each of four dimensions (1–10 scale) with reasoning
- Produce scorecard, MoSCoW table, and recommendations

**Phase 2: Offer to fix (optional)**
- Ask if you want fixes applied for Must and Should items
- Address each item with your confirmation

Detailed guidance:
- **Scoring dimensions & artefacts:** see phase1.md
- **MoSCoW definitions:** see phase2.md
- **Output format & recommendations:** see phase3.md
- **Fix workflow:** see phase4.md

---

## ❓ Known gaps

- **Subjective scoring:** Uses heuristics, not automated checks
- **Happy path only:** No error recovery for edge cases
