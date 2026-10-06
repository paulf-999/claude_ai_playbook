# Quality Scorecard — test_lazy_load_triggers.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Goal:** module docstring names the three triggers and why a README mention doesn't count<br>• 💬 **Messages:** the real-config failure lists each orphan and the three ways to fix it |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (triggers, loaded files, symlinks) + Scope 2 (`_rules/`, `rules/`, `skills/`, `hooks/`, `CLAUDE.md`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 10/10 | 2026-10-01 | • 📊 **Measured:** `python.md`, `bash.md` and `testing_guidance.md` missed 91–100% of the sessions they applied to<br>• 🔴 **Red first:** failed on `main` with 13 untriggered lazy rules |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 12 test functions and 15 assertions, one inside a 4-rule loop<br>• 🧩 **Cases:** each trigger type, orphans, bare names, body-text `paths:`, nested imports, skill READMEs, symlinks and the 2026-10-01 fixes |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against all 22 lazy entry points |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Pinned:** `python.md` and `bash.md` must keep `paths:`, and `jira.md` and `latency_optimisation.md` must keep their pointers |
| **Overall** | **9.1/10** | 2026-10-01 | • 💪 **Strongest:** Evidence of Need, Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10), from reading five parts of the config |

## 🔗 Related files

- `src/claude/_tests/rules/05_lazy_load/test_lazy_load_triggers.py` — the test being scored
- `src/claude/rules/05_path_scoped/claude_rule_loading_strategy.md` — "Pointers aren't triggers" and the placement table
- `src/claude/_tests/rules/05_lazy_load/test_path_scoped_rules.py` — the companion checks on `rules/` symlinks and imports
