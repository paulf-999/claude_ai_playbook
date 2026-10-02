# Quality Scorecard — hook_enforcement_markdown_location.sh

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 8.4/10

**Recommended improvements:**
- Record the hook's first real hit in `_admin/_docs/decisions/hooks.md`, or retire it if none appears within 90 days

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Header:** clearly lists the two checks and why it exits 2<br>• ✅ **Name:** says it checks where markdown files live |
| **Complexity** | 7/10 | 2026-10-02 | • 🧮 **Raw complexity 3:** root files and `_reference/` names (Concepts 1), one folder (Scope 1), `jq` (Dependencies 1) |
| **Evidence of Need** | 6/10 | 2026-10-02 | • 📘 **Rules:** enforces the root-files and `_reference/` naming rules<br>• ⚠️ **No hit yet:** it never ran before the 2026-10-01 fix in #195, so no real catch is recorded |
| **Test Coverage** | 9/10 | 2026-10-02 | • 📊 **Cases:** 14 tests and 20 assertions cover allowed root files, stray files, reference names and paths outside the config |
| **Structural Compliance** | 9/10 | 2026-10-02 | • ✅ **Basics:** metadata header, registered on `PostToolUse`, paths from the script's own location, listed in `decisions/hooks.md` |
| **Failure Safety** | 9/10 | 2026-10-02 | • 🛡️ **Fails open:** an unreadable payload gives an empty path, so it exits quietly<br>• ↩️ **After the fact:** exit 2 hands Claude the fix, since the edit has already happened |
| **Runtime Cost** | 10/10 | 2026-10-02 | • ⚡ **Speed:** plain bash, about 0.02s<br>• 🤫 **Quiet:** silent for every file it doesn't flag |
| **Overall** | **8.4/10** | 2026-10-02 | • 💪 **Strongest:** Runtime Cost (10/10)<br>• ⚠️ **Weakest:** Evidence of Need (6/10) |

## 🔗 Related files

- `src/claude/hooks/hook_enforcement_markdown_location.sh` — the hook being scored
- `src/claude/_tests/hooks/enforcement/test_enforcement_markdown_location.py` — Test Coverage dimension
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — the rule it points to
- `src/claude/_admin/_docs/decisions/hooks.md` — Evidence of Need and Structural Compliance dimensions
