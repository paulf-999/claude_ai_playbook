# Quality Scorecard — test_aliases_behavior.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.1/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 5 and 7)
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** header complexity score 9/10 (raw complexity 1) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 5/10 | • 📊 **Counts:** 5 test functions and 7 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.1/10** | • 💪 **Strongest:** Clarity, Complexity, Evidence of Need, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage (5/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_aliases_behavior.py` — the test being scored
- `src/claude/aliases.md` — what the test guards
