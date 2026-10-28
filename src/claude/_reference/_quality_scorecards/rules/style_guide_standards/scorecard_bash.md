# Quality Scorecard — bash.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Replace the relative `source src/sh/shell_utils.sh` (lines 47 and 50) with a source line that works from any folder, such as one that finds the path from the script's own location, matching the guide's own "Absolute paths" bullet on line 87.
- Decide whether `set -e` is enough as the required minimum, and if it isn't, require `set -euo pipefail`, which the newer hooks already use, and update `template_bash_script.sh` to match.
- Say whether function `local` variables also follow `UPPER_SNAKE_CASE`, or give them their own case.
- Rewrite the bullet on line 82 in `**Keyword:** text` form, and turn the intro sentence on line 28 into a bullet.
- Add evidence of need: a dated incident, a review finding or a usage record, since the `miss_cost` comment is currently the only justification.
- Add a test that checks the five functions and six log-level constants named on lines 51–58 still exist in `shell_utils.sh`, and that the template path on line 30 still exists.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear body:** each section is short and gives a direct instruction<br>• ⚠️ **Self-conflict:** line 47 requires a relative `source src/sh/shell_utils.sh`, but line 87 says to use absolute paths where the working directory may vary<br>• ⚠️ **Case ambiguity:** line 72 says variables are `UPPER_SNAKE_CASE`, and line 78 requires `local`, but nothing says what case locals use |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3 (8 sections: structure, flags, utilities and log levels, tooling, naming, variables, conditionals, general) + Scope 1 (points into `_templates/utils/`) + Dependencies 1 (`shellcheck`) + Prerequisites 1 (copy `shell_utils.sh` into each project's `src/sh/`) |
| **Evidence of Need** | 5/10 | 2026-10-28 | • ⚠️ **Undated:** the only justification is line 8's `miss_cost: medium — scripts without strict mode that fail review`<br>• ⚠️ **No record:** no dated incident, issue or usage row is cited |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/*.sh"` loads it only when a shell script is open, so the rubric leaves this out of the average |
| **Structural Compliance** | 8/10 | 2026-10-28 | • ✅ **Within limits:** 90 lines, metadata header straight after the frontmatter, Purpose line, emoji H2s, and a Contents list earned by 8 headings<br>• ⚠️ **Style slips:** line 82 `**Prefer `[[ ]]`** over `[ ]`` isn't in keyword-colon form, and line 28 is a prose lead-in rather than a bullet |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths exist:** `template_bash_script.sh` and `shell_utils.sh` exist, and all 5 functions and 6 constants on lines 51–58 are defined there<br>• ✅ **Install rewrite:** the `~/.claude/` paths are pointed at the real config folder at install time by `claude_file_utils.sh`<br>• ⚠️ **Practice drift:** `hook_style_guide_response_standards_reminder.sh` and `_checker.sh` use `set -euo pipefail`, and `hook_enforcement_mcp_stale_settings.sh` uses `set -eu`<br>• ⚠️ **Not followed:** none of the hooks source `src/sh/shell_utils.sh`, although line 44 says "All scripts must" |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural:** `test_lazy_load_rule_structure.py` pins only 2 of the 8 H2s (`Safety flags`, `Naming conventions`) and the metadata header<br>• 🧪 **Trigger:** `test_lazy_load_triggers.py` checks that the installed file loads through `paths`<br>• ⚠️ **Unchecked references:** no test confirms the functions, constants and template path the guide names still exist<br>• ⚠️ **Not run:** this review didn't run the tests (read-only), so passing is inferred, not seen |
| **Overall** | **6.7/10** | 2026-10-28 | • 💪 **Lean and scoped:** short, path-scoped, and every file it names exists<br>• ⚠️ **Gaps:** the relative `source` line contradicts its own advice, the required flags are weaker than the repo's newer hooks, and there is no evidence of need |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/bash.md` — the rule being scored
- `src/claude/_templates/utils/template_bash_script.sh` — Currency, Clarity (it mirrors the `set -e` and relative `source` lines)
- `src/claude/_templates/utils/shell_utils.sh` — Currency (functions and log-level constants)
- `src/claude/_install/helpers/claude_file_utils.sh` — Currency (install-time `~/.claude/` path rewrite)
- `src/claude/hooks/hook_style_guide_response_standards_reminder.sh` — Currency (`set -euo pipefail`)
- `src/claude/hooks/hook_style_guide_response_standards_checker.sh` — Currency (`set -euo pipefail`)
- `src/claude/hooks/hook_enforcement_mcp_stale_settings.sh` — Currency (`set -eu`)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_triggers.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
