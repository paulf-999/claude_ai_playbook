# Quality Scorecard — airflow.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.7/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Excellent:** each of the 4 core principles states Why/How/Test, plus a common-mistakes table and a DAG-lifecycle diagram |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** router to 5 child pages plus 4 inline principles, a mistakes table, a lifecycle diagram, and an acceptance checklist — single file, no dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Concrete and scoped:** explicitly targets `dmt_airflow_dags/` — a real repository, not generic Airflow advice |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** Purpose + Scope statements, consistent emoji headers, 100 lines (at the tolerated limit, not over it) |
| **Currency** | 7/10 | 2026-09-28 | • 🐛 **Orphaned duplicate:** `style_guide_standards/airflow/airflow.md` is a near-identical, unreferenced copy of this file — flagged, not fixed, out of scope here<br>• ✅ **Content itself:** no stale references found in the parent's own text |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.7/10** | 2026-10-01 | • 💪 **Strength:** the clearest why/how/test structure in this survey<br>• ⚠️ **Gap:** Currency (7/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow/airflow.md` — Currency dimension (the orphaned duplicate)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/airflow/airflow.md` is a near-identical copy of this parent file, sitting inside its own children's directory under the same filename. Confirmed via repo-wide grep — nothing references it anywhere.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
