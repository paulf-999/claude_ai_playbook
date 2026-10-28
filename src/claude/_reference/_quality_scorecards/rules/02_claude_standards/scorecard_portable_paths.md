# Quality Scorecard — portable_paths.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 8.0/10

**Recommended improvements:**
- Say how code under `scripts/` reaches `CLAUDE_DIR`, since `_shared_paths.py` lives in `_tests/_helpers/`.
- Add the `CLAUDE_HOOKS_DIR` → `CLAUDE_ROOT_DIR` form as an accepted shell pattern, because 3 of the 4 hooks use it.
- Mark the deleted files named in the incidents as historical, so a reader doesn't go looking for them.
- Point the `test_rules_structure.py` incident at the file that now holds the import check (`test_rules_structure_layout.py`).
- Make the closing `**Both:**` paragraph a bullet, and split the run-on hook-scripts incident bullet into child bullets.
- Load the rule only when a file matching `applies_to` is open, or record in a file how often a hook or test gets written before such a file is open.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Concrete:** gives a Python and a shell form for each case, with a wrong example and a right example<br>• ⚠️ **Scripts gap:** line 36 covers "Python (tests, scripts)", but line 37's `from _shared_paths import CLAUDE_DIR` only resolves from `_tests/_helpers/`, so it's unclear what a script should import<br>• ⚠️ **Two names:** line 16 says resolve "from `CLAUDE_CONFIG_DIR`" and line 37 says use `CLAUDE_DIR`, without saying one is built from the other |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** one concept (don't hardcode the config dir), applied across three folders (`hooks/`, `_tests/`, `scripts/`), with one dependency (`_shared_paths.py`)<br>• 📐 **Anchor:** matches the ~7 row, "one job that reads across several folders" |
| **Evidence of Need** | 9/10 | 2026-10-25 | • 📈 **Recurring:** four dated incidents across 2026-09-17 and 2026-09-18 (lines 25–30)<br>• 🔁 **Repeat:** the fourth incident came back minutes after the rule was written, which shows the mistake keeps happening |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • ⚖️ **Arguable:** `applies_to` is set (line 4) to hook, test and script files, but the rule still loads every session (line 6)<br>• ✅ **Reason given:** line 6 argues a new hook or test can start before a matching file is open, and line 5 records the miss cost as high<br>• ⚠️ **No usage record:** no file shows how often that early-start case happens, so the always-on cost rests on the argument alone |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Clean basics:** 48 lines, metadata header, emoji headers, a Purpose line and bold-keyword bullets<br>• ⚠️ **Run-on bullet:** line 29 packs the hook name, the failing command, the directory explanation and the result into one bullet<br>• ⚠️ **Prose block:** line 47 `**Both:**` is a stand-alone paragraph, not a bullet |
| **Currency** | 8/10 | 2026-10-27 | • ✅ **How-to paths exist:** `_tests/_helpers/_shared_paths.py`, `_templates/utils/shell_utils.sh` and `hooks/hook_enforcement_naming_convention.sh` are all there today<br>• ⚠️ **Gone files:** `test_response_standards_hook.py`, `_inject.py` and `hook_enforcement_dir_structure.sh` (lines 27, 29) no longer exist, which is acceptable as incident evidence but isn't marked as history<br>• ⚠️ **Moved check:** the import-reachability logic cited on line 28 now seems to live in `test_rules_structure_layout.py` (its line 36 cites this rule)<br>• 🔍 **Idiom drift:** only `hook_style_guide_response_standards_reminder.sh` uses line 44's exact one-liner, while the other three hooks reach the same result through `CLAUDE_HOOKS_DIR` |
| **Test Coverage** | 9/10 | 2026-10-27 | • ✅ **Content regression:** `test_portable_paths_python.py` covers the `.expanduser()`, home-constant and single-prefix incidents, with boundary cases that fail if a regex is loosened<br>• ✅ **Hook side:** `test_portable_paths_hooks.py` covers hardcoded file operations and the guard-substring anti-pattern<br>• ⚠️ **Narrow match:** `HARDCODED_HOME_CONSTANT` only catches uppercase module-level assignments, so a hardcoded home path inside a function goes unflagged<br>• 🔍 **Not run here:** these tests weren't run in this review, so this score assumes they pass |
| **Overall** | **8.0/10** | 2026-10-27 | • 💪 **Strength:** dated, recurring incidents plus two tests that enforce the rule<br>• ⚠️ **Gap:** always-on cost argued but not measured, small currency drift in the incident and shell sections, and unclear guidance for `scripts/` |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_python.py` — Test Coverage
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_hooks.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance, Currency
- `src/claude/_tests/rules/test_rules_structure_layout.py` — Currency
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Evidence of Need
- `src/claude/_tests/_helpers/_shared_paths.py` — Clarity, Currency
- `src/claude/_templates/utils/shell_utils.sh` — Currency
- `src/claude/hooks/hook_enforcement_naming_convention.sh` — Currency
- `src/claude/hooks/hook_style_guide_response_standards_reminder.sh` — Currency
- `src/claude/hooks/hook_enforcement_mcp_stale_settings.sh` — Currency
- `src/claude/hooks/hook_enforcement_markdown_location.sh` — Currency
