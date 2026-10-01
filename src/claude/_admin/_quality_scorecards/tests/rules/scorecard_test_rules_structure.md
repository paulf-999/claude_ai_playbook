# Quality Scorecard — test_rules_structure.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.3/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (6) down to 3 or less

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 4/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 4/10 (raw complexity 6) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 16 test functions and 19 assertions |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Failure cases:** 2 test functions prove a detector fails on a bad case, including the new H2 emoji check |
| **Overall** | **8.3/10** | 2026-10-01 | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Complexity (4/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rules_structure.py` — the test being scored
- `src/claude/_rules/` — what the test guards
