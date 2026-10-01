# Quality Scorecard — test_portable_paths.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.7/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (7) down to 3 or less
- Update the header quality score from 9/10 to reflect the current counts
- Add test functions and assertions toward 10+ and 15+ (now 9 and 13)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 77% of assertions carry a failure message |
| **Complexity** | 3/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 3/10 (raw complexity 7) |
| **Evidence of Need** | 10/10 | 2026-09-30 | • 🔗 **Target:** guards a rule written after a documented incident |
| **Coverage** | 7/10 | 2026-09-30 | • 📊 **Counts:** 9 test functions and 13 assertions<br>• ⚠️ **Header drift:** header quality score is 9/10, but the counts support 7/10 |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-18 |
| **Regression Value** | 8/10 | 2026-09-30 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **7.7/10** | 2026-09-30 | • 💪 **Strongest:** Evidence of Need (10/10)<br>• ⚠️ **Weakest:** Complexity (3/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_portable_paths.py` — the test being scored
- `src/claude/_rules/02_claude_standards/portable_paths.md` — what the test guards
