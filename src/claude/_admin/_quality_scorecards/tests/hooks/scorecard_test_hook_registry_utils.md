# Quality Scorecard — test_hook_registry_utils.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (registry integrity, its path parser and reserved hooks) + Scope 2 (`settings.json`, `hooks/` and `_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** a stale hook reference makes Claude Code skip the hook with no error |
| **Coverage** | 10/10 | 2026-10-01 | • 📊 **Counts:** 16 test functions and 23 assertions<br>• 🧩 **Run-time config dir:** every hook command must read `CLAUDE_CONFIG_DIR`<br>• 🧩 **Reserved hooks:** every hook file must be registered or listed in `RESERVED_HOOKS` with the rule that explains why |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🛡️ **Parser:** `~/.claude/`, `~/claude/` and `${CLAUDE_CONFIG_DIR:-…}/` all resolve to the config dir, so the portable-paths fix can't regress<br>• 🛡️ **Mutation check:** deleting the reserved hook fails two tests |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Coverage, Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), from reading three folders |

## 🔗 Related files

- `src/claude/_tests/hooks/test_hook_registry_utils.py` — the test being scored
- `src/claude/settings.json` — what the test guards
- `src/claude/rules/02_claude_standards/portable_paths.md` — why the parser never calls `.expanduser()`
- `src/claude/rules/_rules_lazy_load/response_standards_enforcement.md` — why `hook_style_guide_response_standards.sh` is reserved
