# Quality Scorecard — test_no_orphaned_skill_files.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.3/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (16% have one today)
- Split the test by concept to bring raw complexity (5) down to 3 or less

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 6/10 | • 🔍 **Messages:** every test function has a docstring, and 16% of assertions carry a failure message |
| **Complexity** | 5/10 | • 🧮 **Complexity:** header complexity score 5/10 (raw complexity 5) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | • 📊 **Counts:** 16 test functions and 19 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 10/10 | • 🛡️ **Failure cases:** 13 test functions named for a failure case |
| **Overall** | **8.3/10** | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (5/10) |

## 🔗 Related files

- `src/claude/_tests/skills/test_no_orphaned_skill_files.py` — the test being scored
- `src/claude/skills/` — what the test guards
