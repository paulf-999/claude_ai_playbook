# Quality Scorecard — test_concurrent_sessions.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.7/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 7/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) |
| **Evidence of Need** | 10/10 | 2026-09-30 | • 🔗 **Target:** guards a rule written after a documented incident |
| **Coverage** | 9/10 | 2026-09-30 | • 📊 **Counts:** 13 test functions and 22 assertions |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-29 |
| **Regression Value** | 8/10 | 2026-09-30 | • 🛡️ **Failure cases:** 1 test function named for a failure case |
| **Overall** | **8.7/10** | 2026-09-30 | • 💪 **Strongest:** Evidence of Need (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_concurrent_sessions.py` — the test being scored
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — what the test guards
