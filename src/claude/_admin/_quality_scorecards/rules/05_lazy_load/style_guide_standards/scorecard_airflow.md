# Quality Scorecard — airflow.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** each of the 4 core principles states Why/How/Test, plus a common-mistakes table and a DAG-lifecycle diagram |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** router to 5 child pages plus 4 inline principles, a mistakes table, a lifecycle diagram, and an acceptance checklist — single file, no dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Concrete and scoped:** explicitly targets `dmt_airflow_dags/` — a real repository, not generic Airflow advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** Purpose + Scope statements, consistent emoji headers, 100 lines (at the tolerated limit, not over it) |
| **Currency** | 9/10 | 2026-10-01 | • ✅ **Resolved:** the orphaned duplicate `airflow/airflow.md` was deleted in #90 (confirmed 2026-10-01)<br>• ✅ **Content itself:** no stale references found |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strength:** the clearest why/how/test structure in this survey<br>• ⚠️ **Gap:** Complexity (8/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/05_path_scoped/style_guide_standards/airflow.md` — the rule being scored

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/airflow/airflow.md` was deleted in #90, confirmed absent on 2026-10-01.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
