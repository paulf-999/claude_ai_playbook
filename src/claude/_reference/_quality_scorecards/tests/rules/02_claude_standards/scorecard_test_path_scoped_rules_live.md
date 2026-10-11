# Quality Scorecard — test_path_scoped_rules_live.py

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-11

**Overall score:** 8.7/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-11 | • 🔍 **Goal:** module docstring explains the opt-in, cost and how to run it<br>• 💬 **Messages:** 9 of 13 assertions carry a failure message |
| **Complexity** | 7/10 | 2026-10-11 | • 🧮 **Raw complexity 3:** Concepts 1 (transcript parsing and live loading) + Scope 1 (`rules/` and the session transcripts) + Dependencies 1 (the `claude` CLI) + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-10-11 | • 🔗 **Target:** the only proof that `paths:` rules really load mid-session, which the placement rule relies on |
| **Coverage** | 8/10 | 2026-10-11 | • 📊 **Counts:** 10 test functions and 13 assertions<br>• ⚠️ **Opt-in:** the two live checks skip unless `CLAUDE_LIVE_CANARY=1`, so a normal run proves only the parsers |
| **Structural Compliance** | 10/10 | 2026-10-11 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-11 | • 🔍 **References:** passes against the current config, header version 1.2.3 updated 2026-10-11 |
| **Regression Value** | 9/10 | 2026-10-11 | • 🛡️ **Both ways:** a `.sql` read must load the rule and a `.txt` read must not<br>• 🧹 **Cleanup:** proves it deletes only the transcripts it created |
| **Overall** | **8.7/10** | 2026-10-11 | • 💪 **Strongest:** Structural Compliance and Currency (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules_live.py` — the test being scored
- `src/claude/rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md` — names this test as the evidence for `paths:`
