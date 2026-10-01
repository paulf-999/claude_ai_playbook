# Quality Scorecard — test_rule_directory_organisation.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 8.0/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (4) down to 3 or less
- Add test functions and assertions toward 10+ and 15+ (now 11 and 13)
- Add a synthetic bad-input test that proves the check fails when it should

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 6/10 | • 🧮 **Complexity:** header complexity score 6/10 (raw complexity 4) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 7/10 | • 📊 **Counts:** 11 test functions and 13 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-29 |
| **Regression Value** | 7/10 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.0/10** | • 💪 **Strongest:** Clarity, Evidence of Need, Structural Compliance and Currency (9/10)<br>• ⚠️ **Weakest:** Complexity (6/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards.md` — what the test guards
