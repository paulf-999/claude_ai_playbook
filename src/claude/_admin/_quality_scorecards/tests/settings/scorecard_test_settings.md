# Quality Scorecard — test_settings.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.6/10

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** header complexity score 9/10 (raw complexity 1) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 7/10 | • 📊 **Counts:** 9 test functions and 15 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **8.6/10** | • 💪 **Strongest:** Clarity, Complexity, Evidence of Need, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage (7/10) |

## 🔗 Related files

- `src/claude/_tests/settings/test_settings.py` — the test being scored
- `src/claude/settings.json` — what the test guards
