# Quality Scorecard — test_hook_metadata_header.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-09-30

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 8/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 8/10 (raw complexity 2) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 10/10 | 2026-09-30 | • 📊 **Counts:** 11 test functions and 15 assertions |
| **Structural Compliance** | 8/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant<br>• 📁 **Location:** sits at the `_tests/` root instead of `_tests/hooks/` |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-30 |
| **Regression Value** | 10/10 | 2026-09-30 | • 🛡️ **Failure cases:** 6 test functions named for a failure case |
| **Overall** | **9.0/10** | 2026-09-30 | • 💪 **Strongest:** Coverage (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/test_hook_metadata_header.py` — the test being scored
- `src/claude/hooks/` — what the test guards
- `src/claude/_rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — what the test guards
