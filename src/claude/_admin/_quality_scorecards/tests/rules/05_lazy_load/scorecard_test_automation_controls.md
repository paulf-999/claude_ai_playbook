# Quality Scorecard — test_automation_controls.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.1/10

**Recommended improvements:**
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | • 🧮 **Complexity:** estimated raw complexity 2 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | • 📊 **Counts:** 10 test functions and 20 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.1/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Structural Compliance (6/10) |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_automation_controls.py` — the test being scored
- `src/claude/_rules/05_lazy_load/automation_controls.md` — what the test guards
