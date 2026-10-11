# Quality Scorecard — test_guiding_principles.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-11

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 9/10 | 2026-10-01 | • 🧮 **Raw complexity 1:** Concepts 1 (CLAUDE.md import discipline and its parser) + Scope 0 (`CLAUDE.md`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** every import costs tokens in every session, so the import list needs guarding |
| **Coverage** | 8/10 | 2026-10-11 | • 📊 **Counts:** 8 test functions and 10 assertions<br>• 🧩 **Checks:** purpose comments, duplicates, one config dir, only memory and aliases imported, the Imports heading and the parser<br>• ✂️ **Trimmed:** emoji pins and 4 import checks that the memory-and-aliases test already covers |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Bug fixed:** the old lazy-load check looked for `_rules/lazy_load/`, a path that doesn't exist, so it could never fail |
| **Overall** | **9.3/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity, Complexity, Evidence of Need and Coverage (9/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — the test being scored
- `src/claude/rules/01_essentials/guiding_principles.md` — what the test guards
- `src/claude/CLAUDE.md` — what the test guards
