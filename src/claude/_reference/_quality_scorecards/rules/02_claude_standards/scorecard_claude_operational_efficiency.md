# Quality Scorecard — claude_operational_efficiency.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 5.9/10

**Recommended improvements:**
- Add the `make disable_mcp` target, or stop naming it in `_mcp_server_toggling.md` line 8
- Move TODO logging and MCP restarts out from under "operational efficiency"
- Record evidence of need, including a source for `_turn_budgets.md` line 12
- Path-scope or lazy-load the narrow children that load every session

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear parent:** the parent's bullets (lines 27–39, 63–65) are short and actionable.<br>• ⚠️ **Contradiction:** `_automation_controls.md` line 27 sets a "5-minute interval floor" and then bans only "sub-minute intervals", so it gives two different limits.<br>• ⚠️ **Overlapping caps:** `_turn_budgets.md` lines 32–33 give 20–30 and 25–50 turns for neighbouring scenarios, so two readers could pick different caps.<br>• ⚠️ **Redundant wording:** `_automation_controls.md` line 48 says "capped at 20 turns by default, or stop after 20 turns", the same limit twice. |
| **Complexity** | 3/10 | 2026-10-25 | • 🧮 **Raw complexity 7:** Concepts 3 (6+ topics: token awareness, defaults, delegation, turn caps, automation, intervention, external access, TODO logging, MCP restarts) + Scope 2 (the rule's own folder plus `_rules_lazy_load/claude_config/claude_cost/`) + Dependencies 2 (ToolSearch/MCP, make targets, hooks) + Prerequisites 0 — see `_complexity_scoring.md`.<br>• ⚠️ **Bundled concepts:** `_task_request_conventions.md` lines 24–65 (TODO logging) and `_mcp_server_toggling.md` (restart after a toggle) are not operational efficiency, but sit under its parent. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ⚠️ **No dated incident:** no file in the bundle records an incident, PR or usage row.<br>• ⚠️ **Unbacked claim:** `_turn_budgets.md` line 12 says "Unbounded turns are a known source of significant cost overrun" but cites no source.<br>• 🔗 **Observed symptom:** `_mcp_server_toggling.md` lines 12–14 describe 2–6 minute hangs, which suggests a real problem, but gives no date or record. |
| **Token Cost Justification** | 6/10 | 2026-10-25 | • 🎯 **Header consistent:** parent lines 4–6 set `applies_to: *`, `miss_cost: high` and `loading: always-on`, which fit tool-use and delegation guidance.<br>• ⚠️ **Narrow children always-on:** `_mcp_server_toggling.md` (only after `make enable_mcp`), `_task_request_conventions.md` (only on "add to TODOs") and `_automation_controls.md` (102 lines, only when `/loop`, `/goal` or `/batch` is used) load every session and inherit the parent's `*` scope. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent clean:** 84 lines, metadata header on lines 1–6, emoji H1, Purpose, Contents with 3+ headings, `Loads on its own from:` wiring, no Related section.<br>• ⚠️ **Bullet style slips:** bullets without a bold keyword and colon at `_turn_budgets.md` lines 40–42, `_external_system_access.md` lines 21–24, `_mcp_server_toggling.md` lines 13–14 and `_task_request_conventions.md` lines 17–20.<br>• ⚠️ **Prose instead of bullets:** `_task_request_conventions.md` line 14 is a multi-sentence paragraph, and `_turn_budgets.md` line 18 is a bold sentence standing alone.<br>• ⚠️ **One concept per file:** hard gate (`_hard_gates_checklist.md` line 22) is strained by the bundled TODO and MCP-restart children. |
| **Currency** | 6/10 | 2026-10-25 | • ⚠️ **Missing target:** `_mcp_server_toggling.md` line 8 names `make disable_mcp server=<name>`, but `src/make/mcp.mk` defines only `enable_mcp` (lines 38–42), and its `.PHONY` list has no `disable_mcp`.<br>• ⚠️ **Unverified command:** `_automation_controls.md` line 31 names `/stop_loop`, and no other file in `src/claude/` defines it.<br>• ✅ **Paths exist:** `latency_optimisation.md`, `delegating_to_subagent.md`, `automation_troubleshooting.md`, `hooks_decision_framework.md`, `hook_enforcement_mcp_stale_settings.sh`, `_install/helpers/mcp_toggle.py` and `TODO.md` all exist. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Wiring tested:** `_tests/rules/test_rule_cross_references.py` lines 224–247 check that every child resolves, that the folder has no orphans, and that Contents entries match the headings.<br>• 🧪 **Pointers tested:** `_tests/_root_files/test_aliases.py` line 29 pins the `_automation_controls.md` path, and `test_lazy_load_triggers.py` line 260 and `test_lazy_load_coverage.py` line 147 cover the latency pointer.<br>• ⚠️ **Commands untested:** no test checks that the make targets or commands named in the children exist, which is why the missing `disable_mcp` target went unnoticed.<br>• ⚠️ **Not run:** this review did not run the suite, so the pass status is not confirmed. |
| **Overall** | **5.9/10** | 2026-10-25 | • 💪 **Strength:** a lean, well-wired parent with structural tests for its children.<br>• ⚠️ **Gap:** the bundle mixes unrelated concepts, records no evidence, and names one or two commands that don't exist. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_claude_when_to_delegate.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_turn_budgets.md` — Test Coverage dimension (untested child)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_task_request_conventions.md` — Test Coverage dimension (untested child)
- `src/claude/_tests/hooks/enforcement/test_enforcement_mcp_stale_settings.py` — Test Coverage dimension (adjacent, not direct)
