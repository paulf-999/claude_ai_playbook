# Quality Scorecard — test_enforcement_mcp_stale_settings.py

**Date Created:** 2026-09-30
**Date Updated:** 2026-10-01

**Overall score:** 9.1/10

**Recommended improvements:**
- None blocking — add an enable-direction live check if a restart hang is ever reproduced

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 🔍 **Messages:** every test function has a docstring, and every assertion carries a failure message<br>• 🧩 **Helpers:** `HookSandbox`, `assert_silent` and `warning_text` keep each test to a few lines |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** three behaviours (snapshot, warn once on change, fail open), one hook, `jq`, a simple `tmp_path` sandbox |
| **Evidence of Need** | 9/10 | • 🔗 **Target:** guards a registered `UserPromptSubmit` hook that runs on every prompt<br>• 🧪 **Premise checked:** on 2026-10-01 a server disabled mid-session kept working until restart, so a stale session is real |
| **Coverage** | 9/10 | • 📊 **Counts:** 13 test functions and 23 assertions<br>• ✅ **Cases:** first prompt, no change, reorder, unrelated setting, disable, enable, warn once, second change, revert, separate sessions, bad input |
| **Structural Compliance** | 10/10 | • ✅ **Header:** full metadata header including complexity score and Python style compliance |
| **Currency** | 10/10 | • 🔍 **References:** matches the renamed hook and its `deniedMcpServers` comparison |
| **Regression Value** | 10/10 | • 🛡️ **Guard:** `test_warns_once_per_change` and `test_state_stays_out_of_config_dir` catch the old version's two bugs (wrong timing, a flag file that never reset) |
| **Overall** | **9.1/10** | • 💪 **Strongest:** Structural Compliance, Currency and Regression Value (10/10)<br>• ⚠️ **Weakest:** Complexity (7/10) |

## 🔗 Related files

- `src/claude/_tests/hooks/enforcement/test_enforcement_mcp_stale_settings.py` — the test being scored
- `src/claude/hooks/hook_enforcement_mcp_stale_settings.sh` — what the test guards
