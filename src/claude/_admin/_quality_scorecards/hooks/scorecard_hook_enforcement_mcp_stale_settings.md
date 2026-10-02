# Quality Scorecard — hook_enforcement_mcp_stale_settings.sh

**Date Created:** 2026-10-02
**Date Updated:** 2026-10-02

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-10-02 | • 🔍 **Header:** names the event, the problem and a three-step "How it works" |
| **Complexity** | 7/10 | 2026-10-02 | • 🧮 **Raw complexity 3:** snapshot, compare and warn once (Concepts 1), settings plus a temp state folder (Scope 1), `jq` (Dependencies 1) |
| **Evidence of Need** | 9/10 | 2026-10-02 | • 🔗 **Incident:** on 2026-10-01 a server disabled mid-session kept working until restart, as `_mcp_server_toggling.md` describes |
| **Test Coverage** | 9/10 | 2026-10-02 | • 📊 **Cases:** 13 tests cover first prompt, change, revert, warn once, separate sessions and bad input |
| **Structural Compliance** | 10/10 | 2026-10-02 | • ✅ **Basics:** correct name, metadata header, registered on `UserPromptSubmit`, paths from the script's own location<br>• ✅ **Documented:** listed in the lifecycle table in `_admin/_docs/decisions/hooks.md` |
| **Failure Safety** | 10/10 | 2026-10-02 | • 🛡️ **Fails open:** exits quietly without a session id, settings file or valid `jq` output<br>• 🔒 **Input check:** rejects session ids that aren't plain names, so state can't be written outside its folder |
| **Runtime Cost** | 9/10 | 2026-10-02 | • ⚡ **Speed:** about 0.03s per prompt<br>• 🤫 **Quiet:** adds text only in the turn after the server list changes |
| **Overall** | **9.0/10** | 2026-10-02 | • 💪 **Strongest:** Structural Compliance and Failure Safety (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/hooks/hook_enforcement_mcp_stale_settings.sh` — the hook being scored
- `src/claude/_tests/hooks/enforcement/test_enforcement_mcp_stale_settings.py` — Test Coverage dimension
- `src/claude/_rules/04_claude_reference/claude_operational_efficiency/_mcp_server_toggling.md` — Evidence of Need dimension
- `src/claude/_admin/_docs/decisions/hooks.md` — Structural Compliance dimension
