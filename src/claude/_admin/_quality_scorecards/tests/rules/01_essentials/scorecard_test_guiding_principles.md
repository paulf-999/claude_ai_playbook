# Quality Scorecard — test_guiding_principles.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 7.6/10

**Recommended improvements:**
- Add test functions and assertions toward 10+ and 15+ (now 3 and 3)
- Replace the `< 20 imports` limit with a check tied to a documented budget

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 10/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 10/10 (raw complexity 0) |
| **Evidence of Need** | 7/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact<br>• ⚠️ **Finding:** the `< 20 imports` limit is an arbitrary stand-in for 'no speculative imports' |
| **Coverage** | 3/10 | 2026-09-30 | • 📊 **Counts:** 3 test functions and 3 assertions |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 9/10 | 2026-09-30 | • 🔍 **References:** passes against the current config, header last updated 2026-09-21 |
| **Regression Value** | 6/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case<br>• ⚠️ **Finding:** the import-count check would pass a speculative import as long as the total stays under 20 |
| **Overall** | **7.6/10** | 2026-10-01 | • 💪 **Strongest:** Complexity (10/10)<br>• ⚠️ **Weakest:** Coverage (3/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — the test being scored
- `src/claude/_rules/01_essentials/guiding_principles.md` — what the test guards
- `src/claude/CLAUDE.md` — what the test guards
