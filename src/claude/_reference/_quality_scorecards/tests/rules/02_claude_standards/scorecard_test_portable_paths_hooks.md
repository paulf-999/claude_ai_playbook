# Quality Scorecard — test_portable_paths_hooks.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (hardcoded paths in hooks) + Scope 1 (`hooks/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-09-30 | • 🔗 **Incident:** hooks hardcoded `~/.claude/` and failed on a `~/claude` config (2026-09-17) |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 15 assertions<br>• 🧩 **Checks:** source/cat/file tests, guard substrings, and roots resolved from the hook's own location |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Bug fixed:** the old pattern's `\b` could never match before `[[`, so file tests like `[[ -f ~/.claude/x ]]` were never caught |
| **Overall** | **9.4/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_hooks.py` — the test being scored
- `src/claude/rules/02_claude_standards/portable_paths.md` — what the test guards
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_python.py` — the Python half of the old `test_portable_paths.py`
