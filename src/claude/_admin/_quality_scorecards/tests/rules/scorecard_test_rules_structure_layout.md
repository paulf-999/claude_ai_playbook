# Quality Scorecard — test_rules_structure_layout.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-01

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2000-01-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (folder layout and the import graph) + Scope 2 (`CLAUDE.md`, `aliases.md` and `_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2000-01-01 | • 🔗 **Target:** guards the tier layout and keeps `_reference/` out of every session |
| **Coverage** | 9/10 | 2000-01-01 | • 📊 **Counts:** 11 test functions and 15 assertions<br>• 🧩 **Checks:** root files, dissolved paths, imports resolving, tier order, `_reference/` reachability and the parser |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 9/10 | 2000-01-01 | • 🛡️ **Tier order:** a reversed 02-before-01 sample proves the order check fails when it should |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rules_structure_layout.py` — the test being scored
- `src/claude/_rules/04_claude_reference/claude_rule_loading_strategy.md` — the tier layout it guards
- `src/claude/_tests/rules/test_rules_structure.py` — the per-file format half of the old test
