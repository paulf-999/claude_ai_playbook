# Quality Scorecard — test_claude_rule_loading_strategy.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-11

**Overall score:** 8.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and 100% of assertions carry a failure message |
| **Complexity** | 7/10 | 2026-09-30 | • 🧮 **Complexity:** header complexity score 7/10 (raw complexity 3) |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** guards a real, installed artefact |
| **Coverage** | 9/10 | 2026-10-11 | • 📊 **Counts:** 10 test functions and 16 assertions<br>• 🧩 **Checks:** the folder table against the disk, examples, loading claims, pointers, line limit and newline<br>• ✂️ **Trimmed:** 7 wording pins deleted 2026-10-11, and 2 structural anchors tagged `# wording-check:` |
| **Structural Compliance** | 9/10 | 2026-09-30 | • ✅ **Header:** full metadata header, marked Python style compliant |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 4.0.0 updated 2026-10-11 |
| **Regression Value** | 7/10 | 2026-09-30 | • 🛡️ **Failure cases:** checks real files, but no function proves the check fails on a bad case |
| **Overall** | **8.6/10** | 2026-10-11 | • 💪 **Strongest:** Currency (10/10)<br>• ⚠️ **Weakest:** Complexity and Regression Value (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_claude_rule_loading_strategy.py` — the test being scored
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — what the test guards
