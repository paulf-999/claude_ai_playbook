# Quality Scorecard — test_session_start_mcp_stale_settings.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 7.9/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (14% have one today)
- Split the test by concept to bring raw complexity (7) down to 3 or less

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 6/10 | • 🔍 **Messages:** every test function has a docstring, and 14% of assertions carry a failure message |
| **Complexity** | 3/10 | • 🧮 **Complexity:** header complexity score 3/10 (raw complexity 7) |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | • 📊 **Counts:** 10 test functions and 28 assertions |
| **Structural Compliance** | 9/10 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | • 🔍 **References:** passes against the current config, header last updated 2026-09-29 |
| **Regression Value** | 9/10 | • 🛡️ **Failure cases:** 4 test functions named for a failure case |
| **Overall** | **7.9/10** | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (3/10) |

## 🔗 Related files

- `src/claude/_tests/hooks/session_start/test_session_start_mcp_stale_settings.py` — the test being scored
- `src/claude/hooks/hook_session_start_mcp_stale_settings.sh` — what the test guards
