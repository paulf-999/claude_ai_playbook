# Quality Scorecard — test_rules_structure_layout.py

**Date Created:** 2026-10-01
**Date Updated:** 2026-10-11

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-01 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message |
| **Complexity** | 7/10 | 2026-10-01 | • 🧮 **Raw complexity 3:** Concepts 1 (folder layout and the import graph) + Scope 2 (`CLAUDE.md`, `aliases.md` and `_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-01 | • 🔗 **Target:** guards the tier layout and keeps `_reference/` out of every session |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 7 test functions and 7 assertions<br>• 🧩 **Checks:** root files, `aliases.md` placement, imports resolving, tier order, `_reference/` reachability and the parser<br>• ✂️ **Trimmed:** the dissolved-path migration checks, 2026-10-11 |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header version 5.0.0 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-10-01 | • 🛡️ **Tier order:** a reversed 02-before-01 sample proves the order check fails when it should |
| **Overall** | **9.0/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/test_rules_structure_layout.py` — the test being scored
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — the tier layout it guards
- `src/claude/_tests/rules/test_rules_structure.py` — the per-file format half of the old test
