# Quality Scorecard — test_decision_making.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.3/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 5 and 6)
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Add a synthetic bad-input test that proves the check fails when it should
- Fix the module docstring to name `02_claude_standards/behaviour/_decision_making.md`

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 8/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message<br>• ⚠️ **Docstring:** module docstring names the retired path `_rules/01_core/behaviour/_decision_making.md` |
| **Complexity** | 9/10 | • 🧮 **Complexity:** estimated raw complexity 1 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 5/10 | • 📊 **Counts:** 5 test functions and 6 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 7/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17<br>• ⚠️ **Finding:** docstring path is stale, although the constant it tests is current |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **7.3/10** | • 💪 **Strongest:** Complexity (9/10)<br>• ⚠️ **Weakest:** Coverage (5/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_decision_making.py` — the test being scored
- `src/claude/_rules/02_claude_standards/behaviour/_decision_making.md` — what the test guards
