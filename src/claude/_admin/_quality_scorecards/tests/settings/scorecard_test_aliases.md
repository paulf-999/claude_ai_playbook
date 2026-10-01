# Quality Scorecard — test_aliases.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 9/10 | 2026-09-30 | • 🧮 **Raw complexity 1:** Concepts 1 (the alias table and its parser) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards `aliases.md`, which is imported into every session |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 13 test functions and 15 assertions<br>• 🧩 **New:** rule-path links, the controls note matching the table, and parser failure cases |
| **Structural Compliance** | 8/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff`<br>• 📁 **Location:** guards `aliases.md` but sits in `_tests/settings/`, apart from `rules/test_aliases_behavior.py` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Failure cases:** a missing table, a wrong header and a short row each fail<br>• 🐛 **Fix:** a broken row used to vanish silently, but now it fails |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Structural Compliance (8/10), for the location |

## 🔗 Related files

- `src/claude/_tests/settings/test_aliases.py` — the test being scored
- `src/claude/aliases.md` — what the test guards
- `src/claude/_tests/rules/test_aliases_behavior.py` — the sibling test that checks alias behaviour
