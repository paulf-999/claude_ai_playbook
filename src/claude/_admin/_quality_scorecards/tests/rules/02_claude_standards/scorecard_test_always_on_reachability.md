# Quality Scorecard — test_always_on_reachability.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 8.3/10

**Recommended improvements:**
- Split the test by concept to bring raw complexity (7) down to 3 or less

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 70% of assertions carry a failure message |
| **Complexity** | 3/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 3/10 (raw complexity 7) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | 2026-09-30 | • 📊 **Counts:** 15 test functions and 23 assertions |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 10/10 | 2026-09-30 | • 🛡️ **Failure cases:** 7 test functions named for a failure case |
| **Overall** | **8.3/10** | 2026-09-30 | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (3/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — the test being scored
- `src/claude/CLAUDE.md` — what the test guards
- `src/claude/_rules/04_claude_reference/claude_rule_loading_strategy.md` — what the test guards
