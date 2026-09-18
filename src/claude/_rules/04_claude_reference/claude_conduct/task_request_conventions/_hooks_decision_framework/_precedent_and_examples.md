# 📅 Hooks ROI — Precedent & Examples

**Purpose:** The real incidents behind the hooks decision framework — one negative (5 low-ROI hooks removed), one positive — grounding the framework in evidence, not theory.

---

## 📅 Precedent: 2026-08-07 hook removal

**What happened:** 5 hooks were proposed without ROI evaluation:
- `enforcement_task_tracking.sh`
- `enforcement_naming_convention.sh`
- `enforcement_dir_structure.sh`
- `enforcement_subagent_reads.sh`
- `style_guide_dispatch.sh`

**Cost:** 5000+ tokens/session baseline, zero observed value.

**Outcome:** All removed; user spent time auditing and removing low-value automation.

**Lesson:** Without explicit ROI criteria, automation becomes silent debt.

---

## ✅ Success example

**enforcement_writing_style.sh** (active):
- Real problem: many sessions produce output violating writing style
- Frequency: ~40+ times/month across all sessions
- Manual alternative: user would review, ask Claude to rewrite (~15 min/violation)
- ROI: Positive; hook saves ~10 hours/month; setup cost recouped in weeks

---

## 🔗 Related

- Parent: `_hooks_decision_framework.md` — the decision framework and ROI formula this evidence supports
