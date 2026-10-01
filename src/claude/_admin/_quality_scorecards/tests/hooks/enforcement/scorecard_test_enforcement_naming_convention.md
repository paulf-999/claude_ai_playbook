# Quality Scorecard — test_enforcement_naming_convention.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

**Recommended improvements:**
- None blocking — revisit if the compliance checks gain directory-name rules, since the hook would then need folder-name cases too

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message<br>• 🧩 **Helpers:** `deny_reason` and `assert_allowed` keep each test to one or two lines |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** three behaviours (deny, allow, skip), one hook, `jq` and `python3` via the hook, no fixtures |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a registered `PreToolUse` hook that can deny every Write under the config dir<br>• 🐛 **History:** the previous version denied every new file, including auto memory and plans |
| **Coverage** | 9/10 | • 📊 **Counts:** 13 test functions and 24 assertions<br>• ✅ **Cases:** bad names, good names, exact-name files, auto-generated and hidden folders, existing files, other tools, malformed input |
| **Structural Compliance** | 10/10 | • ✅ **Header:** full metadata header including complexity score and Python style compliance |
| **Currency** | 10/10 | • 🔍 **References:** fixture paths use current tier names, and the hook reuses the live compliance checks |
| **Regression Value** | 10/10 | • 🛡️ **Guard:** `test_auto_generated_folders_skipped` and `test_snake_case_rule_allowed` would catch a return to blocking every new file |
| **Overall** | **9.1/10** | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/hooks/enforcement/test_enforcement_naming_convention.py` — the test being scored
- `src/claude/hooks/hook_enforcement_naming_convention.sh` — what the test guards
- `src/claude/_tests/_file_structure_validator.py` — the checks the hook calls
