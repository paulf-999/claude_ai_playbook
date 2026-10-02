# Quality Scorecard — hook_enforcement_naming_convention.sh

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 8.4/10

**Recommended improvements:**
- Add a test that runs the validator's `--check` mode directly, so a change in `_tests/` can't silently switch the hook off

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Header:** says it checks new config file names, denies only on errors and why it ignores advisory notes |
| **Complexity** | 6/10 | 2026-10-02 | • 🧮 **Raw complexity 4:** one concern (Concepts 0), hooks plus the validator in `_tests/` (Scope 2), `jq` and `python3` (Dependencies 2) |
| **Evidence of Need** | 8/10 | 2026-10-02 | • 🔗 **Recurring miss:** badly named config files kept appearing, and a name can't be fixed after creation without a rename |
| **Test Coverage** | 9/10 | 2026-10-02 | • 📊 **Cases:** 13 tests cover good names, bad names, existing files, other tools, paths outside the config and a missing checker |
| **Structural Compliance** | 9/10 | 2026-10-02 | • ✅ **Basics:** correct name, metadata header, registered on `PreToolUse` for Write, listed in `decisions/hooks.md` |
| **Failure Safety** | 10/10 | 2026-10-02 | • 🛡️ **Fails open:** a missing checker, missing `python3` or checker error never blocks a write<br>• 🎯 **Narrow block:** denies only names with an error, never advisory notes |
| **Runtime Cost** | 8/10 | 2026-10-02 | • ⚡ **Speed:** exits in about 0.02s for anything but a new config file<br>• 🐍 **Python start:** pays a `python3` launch only when it checks a new config file |
| **Overall** | **8.4/10** | 2026-10-02 | • 💪 **Strongest:** Failure Safety (10/10)<br>• ⚠️ **Weakest:** Complexity (6/10), because it depends on a validator in another folder |

## 🔗 Related files

- `src/claude/hooks/hook_enforcement_naming_convention.sh` — the hook being scored
- `src/claude/_tests/_file_structure_validator.py` — Complexity and Failure Safety dimensions
- `src/claude/_tests/hooks/enforcement/test_enforcement_naming_convention.py` — Test Coverage dimension
- `src/claude/_admin/_docs/decisions/hooks.md` — Evidence of Need dimension
