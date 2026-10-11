# Quality Scorecard — test_concurrent_sessions.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-11

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** Concepts 1 (reachability, Purpose line, incident record) + Scope 1 (`rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-09-30 | • 🔗 **Target:** guards a rule written after a documented incident |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 3 test functions and 4 assertions<br>• ✂️ **Trimmed:** 6 `covers_*` wording pins deleted 2026-10-11, keeping the tagged incident record |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 3.0.0 updated 2026-10-11 |
| **Regression Value** | 7/10 | 2026-10-11 | • 🛡️ **Failure cases:** fails if the rule goes unreachable or loses its incident record, but no synthetic bad case proves it |
| **Overall** | **8.9/10** | 2026-10-11 | • 💪 **Strongest:** Evidence of Need and Currency (10/10)<br>• ⚠️ **Weakest:** Regression Value (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_concurrent_sessions.py` — the test being scored
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — what the test guards
