# Quality Scorecard — test_settings.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.1/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 9 and 15)
- Complete the metadata header: add `Test complexity score` and `Python style compliant`

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** estimated raw complexity 1 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 7/10 | • 📊 **Counts:** 9 test functions and 15 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **8.1/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Structural Compliance (6/10) |

## 🔗 Related files

- `src/claude/_tests/settings/test_settings.py` — the test being scored
- `src/claude/settings.json` — what the test guards
