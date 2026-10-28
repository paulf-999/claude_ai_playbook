# Quality Scorecard — claude_operational_efficiency.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.3/10

**Recommended improvements:**
- Make the two parallelism bullets agree: either merge "Don't parallelise for its own sake" (line 27) into "Parallel tool calls" (line 35), or say which one wins when both apply.
- Add dated evidence (an incident or usage record) for the cost-overrun risk the `miss_cost` header claims, or cite where that evidence lives.
- Rewrite the negative bullets ("Don't parallelise…", "do not re-read…", "do not summarise…") as positive actions, as `writing_style.md` asks.
- Give the H1 the file's name ("Operational Efficiency"), not "Operational Discipline".
- Record a passing run of `test_rule_cross_references.py` and `test_rules_structure.py` against this commit.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Actionable bullets:** each default behaviour (lines 35–39) is a concrete instruction.<br>• ⚠️ **Conflicting guidance:** line 27 says "Don't parallelise for its own sake", but line 35 says "execute independent operations concurrently", and nothing says which wins.<br>• ⚠️ **Vague purpose:** line 9's "preserving reasoning capability through deliberate choices" doesn't say what the reader should do. |
| **Complexity** | 6/10 | 2026-10-27 | • 🧮 **Raw complexity ~4:** three of its own concepts (token awareness, defaults, intervention mode), plus six children in one folder and one lazy-load pointer to another tree.<br>• ⚠️ **Mixed scope:** it groups unrelated children, such as TODO-logging conventions and MCP restart steps, under "efficiency". |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded incident:** the body cites no dated problem or usage record.<br>• ⚠️ **Claim only:** line 5's `miss_cost: high — uncapped automation… overrun cost` states a risk but points to no evidence. |
| **Token Cost Justification** | 8/10 | 2026-10-27 | • ✅ **Justified header:** `applies_to: *` and line 6's "tool-use and delegation choices come up in every session" fit always-on placement.<br>• ⚖️ **Lean parent:** most of the body is one-line child pointers, so its own cost is small.<br>• ⚠️ **Narrow children:** some children it names (`_mcp_server_toggling.md`, `_task_request_conventions.md`) apply to few sessions but still load every session. |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Clean shape:** 83 lines, a metadata header, a Purpose line, emoji headers, bold-keyword bullets, and a Contents list that matches its 9 headings.<br>• ⚠️ **Negative framing:** lines 27, 36 and 38 say what not to do, against `writing_style.md`'s "positive actions" rule.<br>• ⚠️ **Name mismatch:** the H1 "Claude Operational Discipline" doesn't match the filename `claude_operational_efficiency.md`. |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **All paths resolve:** all six `Loads on its own from` children and `_rules_lazy_load/claude_config/claude_cost/latency_optimisation.md` exist at commit 1705887.<br>• ✅ **Consistent prefix:** `~/.claude/` matches the other `02_claude_standards` rules in the repo. |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Targeted tests:** `test_rule_cross_references.py` checks that every child resolves inside its folder, that no child is orphaned, and that the Contents list matches the headings.<br>• ✅ **Structural test:** `test_rules_structure.py` covers it.<br>• ⚠️ **No recorded pass:** no file records these tests passing at this commit, and this review didn't run them.<br>• 🔍 **No regression test needed:** the rule documents no incident. |
| **Overall** | **7.3/10** | 2026-10-27 | • 💪 **Well-wired index:** a lean parent whose child pointers are tested and all resolve.<br>• ⚠️ **Gaps:** no recorded evidence of need, two parallelism bullets that conflict, and negative framing. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_claude_when_to_delegate.md` — Currency, Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_turn_budgets.md` — Currency, Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md` — Currency, Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_external_system_access.md` — Currency, Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_task_request_conventions.md` — Token Cost, Complexity
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_mcp_server_toggling.md` — Token Cost, Complexity
- `src/claude/rules/_rules_lazy_load/claude_config/claude_cost/latency_optimisation.md` — Currency
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance
