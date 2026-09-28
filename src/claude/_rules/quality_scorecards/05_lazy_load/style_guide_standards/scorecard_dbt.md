# Quality Scorecard — dbt.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Reconcile the redundant `@./dbt/*.md` imports block with the "Child pages" markdown-link table above it — `05_lazy_load/` is documented as never auto-imported, so having both patterns is ambiguous about whether children load automatically.
- Delete or reconcile the orphaned duplicate `dbt/dbt.md` — an unreferenced near-copy of this file.
- Add a dedicated structural test for this file.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 10/10 | • 📋 **Excellent:** each core principle states Why/How/Test, plus a model-layer table, mistakes table, and workflow diagram |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** router to 5 children plus 4 inline principles, a layer table, a mistakes table, and a workflow diagram — single file, no external dependencies |
| **Evidence of Need** | 9/10 | • 🔗 **Concrete and scoped:** targets a real project (`da-etl-dbtanalytics`), cites the external dbt Labs style guide |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | • 🚩 **Inconsistent with siblings:** carries BOTH a "Child pages" markdown-link table AND a separate `@./dbt/*.md` imports block at the bottom — `airflow.md` and `bash.md` use only the link-table pattern<br>• ✅ **Otherwise compliant:** Purpose + Scope statements, emoji headers |
| **Currency** | 5/10 | • 🐛 **Orphaned duplicate:** `dbt/dbt.md` is a near-identical, unreferenced copy of this file — flagged, not fixed<br>• 🐛 **Ambiguous import mechanism:** the `@./` block's actual effect when this file is read on-demand (vs. imported at CLAUDE.md load time) isn't documented anywhere in this repo |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references `dbt` style guide content by name |
| **Overall** | **6.7/10** | • 💪 **Strength:** the same strong why/how/test structure as `airflow.md`<br>• ⚠️ **Gap:** a confusing dual child-loading pattern, an orphaned duplicate, and no test coverage |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/dbt.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/dbt/dbt.md` — Currency dimension (the orphaned duplicate)
- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow.md` — Structural Compliance dimension (sibling using only the link-table pattern)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/dbt/dbt.md` is a near-identical copy of this parent file, unreferenced anywhere in the repo (confirmed via grep).
- 🐛 **Dual child-loading pattern:** this file lists its 5 children in a markdown-link "Child pages" table AND separately `@./`-imports the same 5 files at the bottom — inconsistent with sibling style guides (`airflow.md`, `bash.md`), which use only the link table, and the effect of `@./` imports outside CLAUDE.md's own load chain isn't documented.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
