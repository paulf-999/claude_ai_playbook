# Quality Scorecard — test_path_scoped_rules.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-11 | • 🔍 **Goal:** module docstring explains the PR #184 regression it stops<br>• ⚠️ **Messages:** only 4 of 14 assertions carry a failure message |
| **Complexity** | 8/10 | 2026-10-11 | • 🧮 **Raw complexity 2:** Concepts 1 (`paths:` frontmatter and `@` imports) + Scope 1 (`rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-10-11 | • 🔗 **Incident:** sql.md's `@` children loaded every session and broke the 150k-char limit (PR #184) |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 13 test functions and 14 assertions<br>• 🧩 **Checks:** real files not links, only scoped rules in the folder, no imports, and the frontmatter and import parsers |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 2.3.2 updated 2026-10-11 |
| **Regression Value** | 10/10 | 2026-10-11 | • 🛡️ **Original case:** the sql.md regression is rebuilt in `tmp_path` and flagged, while on-demand pointers pass |
| **Overall** | **9.0/10** | 2026-10-11 | • 💪 **Strongest:** Evidence of Need, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Clarity (6/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules.py` — the test being scored
- `src/claude/rules/02_claude_standards/path_scoped_rules/` — the path-scoped rules it guards
