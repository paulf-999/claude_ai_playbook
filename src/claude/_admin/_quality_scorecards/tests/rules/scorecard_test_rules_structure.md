# Quality Scorecard — test_rules_structure.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.1/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (6) down to 3 or less

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 4/10 | • 🧮 **Complexity:** header complexity score 4/10 (raw complexity 6) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | • 📊 **Counts:** 14 test functions and 17 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **8.1/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Complexity (4/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rules_structure.py` — the test being scored
- `src/claude/_rules/` — what the test guards
