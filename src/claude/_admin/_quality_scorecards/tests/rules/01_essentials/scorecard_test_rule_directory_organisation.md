# Quality Scorecard — test_rule_directory_organisation.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.6/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (4) down to 3 or less
- Add test functions and assertions toward 10+ and 15+ (now 11 and 13)
- Complete the metadata header: add `Test complexity score` and `Python style compliant`
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 6/10 | • 🧮 **Complexity:** estimated raw complexity 4 — the header has no complexity score |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 7/10 | • 📊 **Counts:** 11 test functions and 13 assertions |
| **Structural Compliance** | 6/10 | • ✅ **Header:** header is missing `Test complexity score` and `Python style compliant` |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-29 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **7.6/10** | • 💪 **Strongest:** Clarity (9/10)<br>• ⚠️ **Weakest:** Complexity (6/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards.md` — what the test guards
