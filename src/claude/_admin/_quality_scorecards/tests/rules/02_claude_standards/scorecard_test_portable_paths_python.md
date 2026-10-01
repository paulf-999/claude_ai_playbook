# Quality Scorecard — test_portable_paths_python.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (machine-specific paths in Python) + Scope 1 (`_tests/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2000-01-01 | • 🔗 **Incident:** tests hardcoded `/home/paul/...` and a parser matched only `@~/.claude/` (2026-09-17/18) |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 15 assertions<br>• 🧩 **Checks:** `.expanduser()`, home constants, import prefixes, `_shared_paths.py` and stale exemptions |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Boundaries:** each pattern is proven on real violations and on harmless lookalikes |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_python.py` — the test being scored
- `src/claude/_rules/02_claude_standards/portable_paths.md` — what the test guards
- `src/claude/_tests/_shared_paths.py` — the one file allowed to resolve the config dir from the home directory
