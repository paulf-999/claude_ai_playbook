# 📊 Audit Scorecards

Central index for audit scorecards across Claude config, skills, rules, and other domains. Each audit uses a consistent 7-dimension scoring rubric and provides recommendations for improvement.

---

## 📋 Available Audits

| Domain | File | Last updated | Coverage | Status |
|---|---|---|---|---|
| **Reference files** | [`reference_files.md`](reference_files.md) | 2026-08-19 | 9 reference files | ✅ Complete |

---

## 🎯 Scoring Rubric

All audits use a consistent 7-dimension framework (1–10 scale per dimension):

| Dimension | What it measures | Example |
|---|---|---|
| **Complexity** | Domain count and conceptual breadth; higher = tighter scope | File covers 1 concept vs. 5 mixed concepts |
| **Clarity** | Writing quality, jargon avoidance, 60-second comprehension | Reader understands purpose in one pass |
| **Comprehensiveness** | Coverage of the topic; completeness of examples | All cases covered with concrete examples |
| **Currency** | Alignment with live practice; reference freshness; date-checked | External links work; assertions verified |
| **Structure/Organization** | Hierarchy, formatting, emoji headers, bullet style | Clear headings, tables, progressive disclosure |
| **Documentation** | Inline explanations, examples, links to related docs | Why + what + how for each concept |
| **Standards Compliance** | Adherence to style guides (line limits, naming, formatting) | <110 lines, emoji headers, proper naming |

**Overall Score:** Weighted average (Standards 20%, Clarity/Docs/Structure 15% each, Complexity/Currency 10% each)

**Tiers:**
- **8.5+:** Exemplary — maintain as reference
- **7.0–8.4:** Good — functional but may have improvement opportunities
- **<7.0:** Consider refactoring or lazy-loading

---

## 📊 Audit Methodology

### Before audit

1. **Scope definition:** Which files/features are being audited?
2. **Baseline establishment:** What are current scores? What's the trend?
3. **Scoring guide review:** Reference the scoring rubric above

### During audit

1. **Individual scoring:** Score each file on all 7 dimensions
2. **Dimension breakdown:** Summarize strengths/weaknesses across files
3. **File-by-file assessment:** Detailed feedback on each file with actions
4. **Recommendations:** Refactoring, lazy-loading, consolidation, removal

### After audit

1. **Implementation:** Execute recommended actions (refactoring, moves, deletions)
2. **Verification:** Spot-check changes; validate cross-references
3. **Documentation update:** Update affected READMEs, MEMORY, docs
4. **Schedule next audit:** Quarterly or annually depending on domain churn

---

## 🔄 When to Audit

| Trigger | Frequency | Scope |
|---|---|---|
| **Domain growth** | Ad-hoc | Audit the domain that grew (e.g., new skills, new rules) |
| **Quarterly review** | Q1, Q2, Q3, Q4 | Comprehensive audit of active domains |
| **Annual reset** | Once/year | Full audit before Boris Cherny's 6-month reset cycle |
| **Maintenance window** | As-needed | Spot-check 1–2 files if they're modified or referenced frequently |

---

## 📝 How to Create a New Audit

1. **Choose a domain** (skills, rules, hooks, agents, etc.)
2. **List files** in that domain
3. **Score each file** on all 7 dimensions (use rubric above)
4. **Summarize findings:**
   - Dimension breakdown (strengths/weaknesses)
   - File-by-file assessment
   - Refactoring/lazy-load/removal recommendations
5. **Create file** named `<domain>.md` in this directory
6. **Update this README** with a new row in the table
7. **Implement recommendations** in follow-up PRs

---

## 🔗 Related Files

- **Scoring guide (reference):** `SCORING_GUIDE.md` (in `~/.claude/_reference/`)
- **Reference files:** `~/.claude/_reference/` — the first domain audited
- **Writing style:** `~/.claude/_rules/writing_style.md` — governing all written content

---

## 📈 Audit History

| Date | Domain | Auditor | Notes |
|---|---|---|---|
| 2026-08-19 | Reference files | Claude Code | Initial comprehensive audit; 2 refactoring, 2 lazy-load candidates identified |

---

Last updated: **2026-08-19**
