# Quality Scorecard — hook_enforcement_writing_style.sh

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 7.7/10

**Recommended improvements:**
- Rename the hook to say what it checks, such as `hook_enforcement_markdown_location.sh`
- Record the incident that justified it in `_admin/_docs/decisions/hooks.md`

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-02 | • 🔍 **Header:** clearly lists the two checks and why it exits 2<br>• ⚠️ **Name:** "writing style" doesn't say it checks where markdown files live |
| **Complexity** | 7/10 | 2026-10-02 | • 🧮 **Raw complexity 3:** root files and `_reference/` names (Concepts 1), one folder (Scope 1), `jq` (Dependencies 1) |
| **Evidence of Need** | 6/10 | 2026-10-02 | • ⚠️ **No record:** neither the header nor `decisions/hooks.md` names the stray files that prompted it |
| **Test Coverage** | 9/10 | 2026-10-02 | • 📊 **Cases:** 14 tests and 20 assertions cover allowed root files, stray files, reference names and paths outside the config |
| **Structural Compliance** | 7/10 | 2026-10-02 | • ✅ **Basics:** metadata header, registered on `PostToolUse`, paths from the script's own location<br>• ⚠️ **Name:** the domain part of the name doesn't match the check |
| **Failure Safety** | 9/10 | 2026-10-02 | • 🛡️ **Fails open:** an unreadable payload gives an empty path, so it exits quietly<br>• ↩️ **After the fact:** exit 2 hands Claude the fix, since the edit has already happened |
| **Runtime Cost** | 10/10 | 2026-10-02 | • ⚡ **Speed:** plain bash, about 0.02s<br>• 🤫 **Quiet:** silent for every file it doesn't flag |
| **Overall** | **7.7/10** | 2026-10-02 | • 💪 **Strongest:** Runtime Cost (10/10)<br>• ⚠️ **Weakest:** Clarity and Evidence of Need (6/10) |

## 🔗 Related files

- `src/claude/hooks/hook_enforcement_writing_style.sh` — the hook being scored
- `src/claude/_tests/hooks/enforcement/test_enforcement_writing_style.py` — Test Coverage dimension
- `src/claude/_rules/01_essentials/claude_usage_standards/writing_style.md` — the rule it points to
- `src/claude/_admin/_docs/decisions/hooks.md` — Evidence of Need dimension
