# Quality Scorecard — test_latency_optimisation.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.7/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 4 and 6)
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** estimated raw complexity 1 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 5/10 | • 📊 **Counts:** 4 test functions and 6 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-28 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **7.7/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Coverage (5/10) |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_latency_optimisation.py` — the test being scored
- `src/claude/_rules/05_lazy_load/latency_optimisation.md` — what the test guards
