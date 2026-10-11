# Quality Scorecard — test_git.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion names the clause that broke |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (git.md clauses and its branch pattern) + Scope 1 (`02_claude_standards/` and `git/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** git safety rules, including protected main and the under-20-file PR limit |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 15 assertions<br>• 🧩 **Checks:** child imports, main protection, branch names, PR template, size, titles, gh CLI and stash care |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Executable:** runs the documented branch regex against its own examples and four bad names |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_git.py` — the test being scored
- `src/claude/rules/02_claude_standards/git.md` — what the test guards
