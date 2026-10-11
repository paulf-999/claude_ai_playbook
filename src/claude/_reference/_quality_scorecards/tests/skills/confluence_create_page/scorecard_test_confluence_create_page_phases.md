# Quality Scorecard — test_confluence_create_page_phases.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 8.4/10

**Recommended improvements:**
- Add failure messages that say how to fix each assertion (0% have one today)
- Confirm the handler still mirrors what SKILL.md tells Claude to do, or move the handler into the skill so the test covers real behaviour

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 5/10 | 2000-01-01 | • 🔍 **Messages:** every test function has a docstring, but none of the assertions carry a failure message |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (publish phases, failure modes and the end-to-end flow) + Scope 0 + Dependencies 0 + Prerequisites 1 (`MagicMock` for the Confluence call) |
| **Evidence of Need** | 7/10 | 2000-01-01 | • 🔗 **Target:** the confluence_create_page handler<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md |
| **Coverage** | 10/10 | 2000-01-01 | • 📊 **Counts:** 15 test functions and 31 assertions<br>• 🧩 **Failure modes:** timeout, permission, bad space, network and unexpected errors |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current handler, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Errors:** each failure mode is checked for the error type it returns |
| **Overall** | **8.4/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Clarity (5/10) |

## 🔗 Related files

- `src/claude/_tests/skills/confluence_create_page/test_confluence_create_page_phases.py` — the test being scored
- `src/claude/_tests/skills/confluence_create_page/confluence_create_page_handler.py` — the handler under test
