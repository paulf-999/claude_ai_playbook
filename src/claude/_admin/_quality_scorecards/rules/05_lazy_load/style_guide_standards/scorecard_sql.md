# Quality Scorecard — sql.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add an emoji to the "## Imports" heading — it's the only heading in this file without one.
- Reconcile the redundant "Child pages" markdown-link table with the separate `@./sql/*.md` imports block at the bottom, same inconsistency found in `dbt.md`.
- Delete or reconcile the orphaned duplicate `sql/sql.md`.
- Add a dedicated structural test for this file.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** concrete cost guardrails (`AUTO_SUSPEND`, warehouse sizing), ❌/✅ mistake examples with recovery steps, a pre-commit checklist |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** router to 4 children plus principles, tooling, dbt-specific, cost guardrails, mistakes, and a checklist — single file, no dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Concrete and enforced:** SQLFluff is a real pre-commit gate; warehouse-cost thresholds are specific operational limits |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | 2026-09-28 | • 🚩 **Missing emoji:** "## Imports" is the only heading in the file without one<br>• 🚩 **Dual child-loading pattern:** same inconsistency as `dbt.md` — a "Child pages" table AND a separate `@./` imports block for the same 4 files |
| **Currency** | 4/10 | 2026-09-28 | • 🐛 **Orphaned duplicate:** `sql/sql.md` is a near-identical, unreferenced copy of this file (confirmed via `diff`)<br>• 🐛 **Ambiguous import mechanism:** same undocumented `@./` behavior as `dbt.md` |
| **Test Coverage** | 2/10 | 2026-09-28 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **6.3/10** | 2026-09-28 | • 💪 **Strength:** the most concrete, operationally-grounded content in this survey (real cost thresholds, real SQLFluff codes)<br>• ⚠️ **Gap:** same dual-loading and orphaned-duplicate pattern seen in `dbt.md`, plus one missing heading emoji |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/sql.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/sql/sql.md` — Currency dimension (the orphaned duplicate)
- `src/claude/_rules/05_lazy_load/style_guide_standards/dbt.md` — Structural Compliance dimension (same dual-loading-pattern issue)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/sql/sql.md` is a near-identical copy of this parent file, unreferenced anywhere in the repo (confirmed via `diff` and grep).
- 🐛 **Dual child-loading pattern:** this file lists its 4 children in a "Child pages" table AND separately `@./`-imports the same 4 files — same inconsistency as `dbt.md`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
