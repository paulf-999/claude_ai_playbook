# Quality Scorecard — test_clean_plans.py

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Goal:** module docstring says why live plans must never be archived<br>• 💬 **Messages:** every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-02 | • 🧮 **Raw complexity 2:** Concepts 1 (which plans are archived) + Scope 0 (one script) + Dependencies 0 + Prerequisites 1 (small `tmp_path` plan folders) |
| **Evidence of Need** | 9/10 | 2026-10-02 | • 🔗 **Target:** the script was rewritten on 2026-10-02 after its old PLANS.md design matched no real plans folder |
| **Coverage** | 10/10 | 2026-10-02 | • 📊 **Counts:** 13 test functions and 19 assert statements, from status parsing through the full y/N run |
| **Structural Compliance** | 10/10 | 2026-10-02 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-02 | • 🔍 **References:** passes against the current config |
| **Regression Value** | 9/10 | 2026-10-02 | • 🛡️ **Guard:** fails if a Pending, undated, recent or already-archived plan would be moved |
| **Overall** | **9.3/10** | 2026-10-02 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** none below 8/10 |

## 🔗 Related files

- `src/claude/_tests/scripts/test_clean_plans.py` — the test being scored
- `src/claude/_scripts/_clean_scripts/clean_plans.py` — what the test guards
