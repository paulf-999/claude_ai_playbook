# Quality Scorecard — test_aliases.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.0/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 7 and 10)
- Move the test next to `rules/test_aliases_behavior.py`, or merge the two
- Fix the style gaps and set `Python style compliant: Yes`

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 9/10 | • 🧮 **Complexity:** header complexity score 9/10 (raw complexity 1) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 6/10 | • 📊 **Counts:** 7 test functions and 10 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header says `Python style compliant: No`<br>• 📁 **Location:** guards `aliases.md` but sits in `_tests/settings/`, apart from `rules/test_aliases_behavior.py` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-17 |
| **Regression Value** | 8/10 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **8.0/10** | • 💪 **Strongest:** Clarity, Complexity, Evidence of Need and Currency (9/10)<br>• ⚠️ **Weakest:** Coverage and Structural Compliance (6/10) |

## 🔗 Related files

- `src/claude/_tests/settings/test_aliases.py` — the test being scored
- `src/claude/aliases.md` — what the test guards
