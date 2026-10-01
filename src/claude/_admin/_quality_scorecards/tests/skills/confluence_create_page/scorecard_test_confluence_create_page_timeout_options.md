# Quality Scorecard — test_confluence_create_page_timeout_options.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 9/10 | 2026-10-01 | • 🧮 **Raw complexity 1:** Concepts 1 (argument parsing, dialog wording, answer handling) + Scope 0 + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 7/10 | 2000-01-01 | • 🔗 **Target:** the confluence_create_page handler<br>• ⚠️ **Finding:** tests a Python handler kept beside the test, while the skill itself runs from its SKILL.md |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 13 test functions and 17 assertions<br>• 🧩 **Edge cases:** bad and missing values, singular minute, the 6-minute cap and unknown answers |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current handler, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **No waiting:** every answer is proven without threads, so these cases run in milliseconds |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Evidence of Need (7/10) |

## 🔗 Related files

- `src/claude/_tests/skills/confluence_create_page/test_confluence_create_page_timeout_options.py` — the test being scored
- `src/claude/_tests/skills/confluence_create_page/confluence_create_page_handler.py` — the handler under test
