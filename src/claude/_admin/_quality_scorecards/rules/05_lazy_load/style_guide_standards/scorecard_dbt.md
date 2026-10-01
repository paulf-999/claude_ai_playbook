# Quality Scorecard — dbt.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Reconcile the redundant `@./dbt/*.md` imports block with the "Child pages" markdown-link table above it — `05_lazy_load/` is documented as never auto-imported, so having both patterns is ambiguous about whether children load automatically.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** each core principle states Why/How/Test, plus a model-layer table, mistakes table, and workflow diagram |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** router to 5 children plus 4 inline principles, a layer table, a mistakes table, and a workflow diagram — single file, no external dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Concrete and scoped:** targets a real project (`da-etl-dbtanalytics`), cites the external dbt Labs style guide |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | 2026-09-28 | • 🚩 **Inconsistent with siblings:** carries BOTH a "Child pages" markdown-link table AND a separate `@./dbt/*.md` imports block at the bottom — `airflow.md` and `bash.md` use only the link-table pattern<br>• ✅ **Otherwise compliant:** Purpose + Scope statements, emoji headers |
| **Currency** | 7/10 | 2026-10-01 | • ✅ **Resolved:** the orphaned duplicate `dbt/dbt.md` was deleted in #90 (confirmed 2026-10-01)<br>• 🐛 **Ambiguous import mechanism:** the `@./` block's effect when this file is read on demand still isn't documented |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.2/10** | 2026-10-01 | • 💪 **Strength:** the same strong why/how/test structure as `airflow.md`<br>• ⚠️ **Gap:** Structural Compliance (6/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/dbt.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow.md` — Structural Compliance dimension (sibling using only the link-table pattern)

---

## 🚩 Pre-existing issue disclosed, not fixed

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/dbt/dbt.md` was deleted in #90, confirmed absent on 2026-10-01.
- 🐛 **Dual child-loading pattern:** this file lists its 5 children in a markdown-link "Child pages" table AND separately `@./`-imports the same 5 files at the bottom — inconsistent with sibling style guides (`airflow.md`, `bash.md`), which use only the link table, and the effect of `@./` imports outside CLAUDE.md's own load chain isn't documented.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
