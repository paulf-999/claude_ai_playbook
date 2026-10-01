# Quality Scorecard — test_hook_registry_utils.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 9/10 | • 🧮 **Raw complexity 1:** Concepts 1 (registry integrity and its path parser) + Scope 0 (`settings.json`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** a stale hook reference makes Claude Code skip the hook with no error |
| **Coverage** | 9/10 | • 📊 **Counts:** 11 test functions and 15 assertions<br>• 🧩 **New:** unknown event names, hook type, location and naming, duplicates, and the path parser on synthetic settings |
| **Structural Compliance** | 10/10 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | • 🛡️ **Parser:** `~/.claude/` and `~/claude/` both resolve to the config dir, so the portable-paths fix can't regress |
| **Overall** | **9.3/10** | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** none below 9/10 |

## 🔗 Related files

- `src/claude/_tests/hooks/test_hook_registry_utils.py` — the test being scored
- `src/claude/settings.json` — what the test guards
- `src/claude/_rules/02_claude_standards/portable_paths.md` — why the parser never calls `.expanduser()`
