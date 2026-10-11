# Quality Scorecard — test_audit_plans.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-11 | • 🔍 **Goal:** module docstring states the ordering, archive and stale rules<br>• 💬 **Messages:** 23 of 29 assertions carry a failure message |
| **Complexity** | 7/10 | 2026-10-11 | • 🧮 **Raw complexity 3:** Concepts 2 (status reading, ordering, staleness, drafts) + Scope 1 (`scripts/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-11 | • 🔗 **Target:** `make list_plans`, which surfaces Active plans that stalled |
| **Coverage** | 10/10 | 2026-10-11 | • 📊 **Counts:** 18 test functions and 29 assertions<br>• 🧩 **Cases:** stated and inferred status, status-line dates, subfolders, the 14-day edge, ordering, drafts and a missing folder |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.0.1 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-10-11 | • 🛡️ **Edges:** the 14-day boundary and the Active-only stale rule are each pinned on made-up plans |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/scripts/test_audit_plans.py` — the test being scored
- `src/claude/scripts/_audit_scripts/audit_plans.py` — the script under test
