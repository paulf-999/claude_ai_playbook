# Quality Scorecard — test_rule_directory_organisation.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.3/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-30 | • 🔍 **Messages:** every test function has a docstring, and every assertion says what to move or flatten |
| **Complexity** | 8/10 | 2026-10-01 | • 🧮 **Raw complexity 2:** Concepts 1 (01_essentials layout and the parent-and-children rule) + Scope 1 (`_rules/`) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 9/10 | 2026-09-30 | • 🔗 **Target:** enforces `_multifile_document_organisation.md`, which stops flat-level sprawl |
| **Coverage** | 9/10 | 2026-10-01 | • 📊 **Counts:** 11 test functions and 16 assertions<br>• 🧩 **Wider:** the parent-and-children checks now cover tiers 01–04, not just 01 |
| **Structural Compliance** | 10/10 | 2026-10-01 | • ✅ **Header:** full metadata header, marked Python style compliant and checked with `ruff` |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **References:** passes against the current config, header last updated 2026-10-01 |
| **Regression Value** | 10/10 | 2026-10-01 | • 🐛 **Found and fixed:** `writing_style/` held one child, breaking the 2+ rule the old test skipped, so it was flattened<br>• 🛡️ **Stale guard:** fails if a grouping exemption's folder disappears |
| **Overall** | **9.3/10** | 2026-10-01 | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (8/10) |

## 🔗 Related files

- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — the test being scored
- `src/claude/_rules/01_essentials/claude_usage_standards/multifile_document_organisation.md` — the layout rule it enforces
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — now covers the CLAUDE.md import checks this test dropped
