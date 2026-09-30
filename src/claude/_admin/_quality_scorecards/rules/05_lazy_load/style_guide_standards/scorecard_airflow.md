# Quality Scorecard — airflow.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a dedicated structural test for this file, matching the pattern used for tier-based parent rules.
- Delete or reconcile the orphaned duplicate `airflow/airflow.md` — an unreferenced near-copy of this file.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 10/10 | • 📋 **Excellent:** each of the 4 core principles states Why/How/Test, plus a common-mistakes table and a DAG-lifecycle diagram |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** router to 5 child pages plus 4 inline principles, a mistakes table, a lifecycle diagram, and an acceptance checklist — single file, no dependencies |
| **Evidence of Need** | 9/10 | • 🔗 **Concrete and scoped:** explicitly targets `dmt_airflow_dags/` — a real repository, not generic Airflow advice |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** Purpose + Scope statements, consistent emoji headers, 100 lines (at the tolerated limit, not over it) |
| **Currency** | 7/10 | • 🐛 **Orphaned duplicate:** `style_guide_standards/airflow/airflow.md` is a near-identical, unreferenced copy of this file — flagged, not fixed, out of scope here<br>• ✅ **Content itself:** no stale references found in the parent's own text |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references `airflow` by name (only unrelated hook-injection tests exist under that keyword) |
| **Overall** | **7.5/10** | • 💪 **Strength:** the clearest why/how/test structure in this survey<br>• ⚠️ **Gap:** zero test coverage and an unreferenced duplicate file sitting alongside its real children |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/airflow/airflow.md` — Currency dimension (the orphaned duplicate)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Orphaned duplicate:** `style_guide_standards/airflow/airflow.md` is a near-identical copy of this parent file, sitting inside its own children's directory under the same filename. Confirmed via repo-wide grep — nothing references it anywhere.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
