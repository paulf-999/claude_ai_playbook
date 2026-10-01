# Quality Scorecard — test_confluence_create_page_timeout.py

**Date Created:** keep
**Date Updated:** 2026-10-01

**Overall score:** 8.9/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (the timed wrapper's outcomes) + Scope 0 + Dependencies 0 + Prerequisites 2 (real threads, patched `input`, clock and home) |
| **Evidence of Need** | 7/10 | 2026-09-30 | • 🔗 **Target:** the confluence_create_page handler<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 10 test functions and 15 assertions<br>• 🧩 **New:** a failing call, an empty result and closed input at the dialog |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current handler, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Tightened:** the trigger test accepted a 'timeout' status the code never returns, and the custom-timeout test repeated it with the same timeout |
| **Overall** | **8.9/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity and Evidence of Need (7/10) |

## 🔗 Related files

- `src/claude/_tests/skills/confluence_create_page/test_confluence_create_page_timeout.py` — the test being scored
- `src/claude/_tests/skills/confluence_create_page/confluence_create_page_handler.py` — the handler under test
