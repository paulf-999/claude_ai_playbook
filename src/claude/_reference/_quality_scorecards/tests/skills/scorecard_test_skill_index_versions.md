# Quality Scorecard — test_skill_index_versions.py

**Date Created:** 2026-10-05
**Date Updated:** 2026-10-05

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-05 | • 🔍 **Messages:** every test function has a docstring, and every assertion says what to fix |
| **Complexity** | 8/10 | 2026-10-05 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-10-05 | • 🔗 **Incident:** four skill indexes showed stale versions on 2026-10-05 |
| **Coverage** | 10/10 | 2026-10-05 | • 📊 **Counts:** 11 test functions and 15 assertions |
| **Structural Compliance** | 9/10 | 2026-10-05 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-10-05 | • 🔍 **References:** passes against the current config, header last updated 2026-10-05 |
| **Regression Value** | 10/10 | 2026-10-05 | • 🛡️ **Failure cases:** 4 test functions named for a failure case, and injecting a stale version fails the real check |
| **Overall** | **9.1/10** | 2026-10-05 | • 💪 **Strongest:** Coverage and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/skills/test_skill_index_versions.py` — the test being scored
- `src/claude/skills/` — what the test guards
