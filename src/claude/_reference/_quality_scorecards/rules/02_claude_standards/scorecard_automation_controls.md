# Quality Scorecard — _automation_controls.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 6.4/10

**Recommended improvements:**
- Move the rule out of the always-on tier into `_rules_lazy_load/claude_config/`, and keep the `aliases.md` pointer as the way in.
- Make the `/loop` "confirm the task is complete before stopping" note match the kill-switch "Stop immediately" step, or state which one wins.
- Remove the `/loop` and `/goal` overlap: "Keep running tests until they pass" (loop) and "Run tests until all pass" (goal) currently sit under both.
- Explain what "10 turns per iteration" means for `/loop`, or replace it with one total cap.
- Add a source for each numeric limit (5 min, 2 h, 20 turns, 3 iterations, 30 min, 12 items), such as a dated incident or a usage record, or label them as starting values.
- Split the two-sentence kill-switch bullet (line 85) and change "judgment" to "judgement" (lines 37 and 75).
- Add a small test that checks the limits in this rule match those in `automation_troubleshooting.md` and `_turn_budgets.md`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • ⚠️ **Conflicting stop guidance:** line 32 says "always confirm the task is actually complete before stopping; don't interrupt mid-work", but kill-switch step 1 (line 83) says "Stop immediately"<br>• ⚠️ **Overlapping use cases:** `/loop` "Monitoring: Keep running tests until they pass" (line 37) duplicates `/goal` "Run tests until all pass" (line 57), so two readers could pick different commands<br>• ⚠️ **Unclear unit:** "stop after 10 turns per iteration" (line 29) gives no total cap for a loop, alongside a separate 2-hour runtime limit<br>• ⚠️ **Inconsistent example:** `/goal` says not to use it for "External dependencies" (line 57), yet its own example is "Implement feature until QA sign-off" (line 55)<br>• 🔍 **Clear structure:** each command has its limits plus a Use for / Don't use for table |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** Concepts 3 (three commands, kill-switch, permission gates, troubleshooting pointer) + Scope 0 (single file) + Dependencies 0 + Prerequisites 0<br>• 🔍 **One job:** guardrails for experimental automation, with troubleshooting already moved to a lazy child |
| **Evidence of Need** | 5/10 | 2026-10-27 | • ❓ **No incident recorded:** the rule cites no dated incident, issue or usage record, unlike `portable_paths.md`<br>• ⚠️ **Unsourced limits:** the 5 min, 10 min, 2 h, 20 turns, 3 iterations, 30 min and 12 items limits have no stated origin<br>• 🔍 **Experimental status:** `aliases.md` marks `/batch`, `/goal` and `/loop` as Testing, so there's no recorded repeat use |
| **Token Cost Justification** | 4/10 | 2026-10-27 | • 💸 **Narrow but always-on:** the file sits in `rules/02_claude_standards/` with no `paths:` frontmatter, so it loads every session, yet only sessions that explicitly invoke three experimental commands need it<br>• ⚠️ **Existing pointer:** `aliases.md` already points to this file for all three commands, so a read-on-demand pointer would serve<br>• 🔍 **Partial mitigation:** troubleshooting detail is already lazy-loaded (line 101) |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Within limits:** 102 lines, metadata header on lines 1–3, emoji H1 and H2s, Purpose line, Contents earned by 6 headings<br>• ⚠️ **Multi-sentence bullet:** line 85 "Check the transcript: what was the agent doing? Where did it diverge?"<br>• ⚠️ **American spelling:** "judgment" on lines 37 and 75<br>• ⚠️ **Negation framing:** "nothing shorter allowed", "no auto-triggering", "no multi-PR agents", where `writing_style.md` prefers positive actions |
| **Currency** | 8/10 | 2026-10-27 | • ✅ **Paths exist:** `_turn_budgets.md` (sibling) and `rules/_rules_lazy_load/claude_config/automation_troubleshooting.md` both exist at commit 1705887<br>• ✅ **Prefix convention:** `~/.claude/` on line 101 matches the repo's other read-on-demand pointers<br>• 🔍 **Unverified external claims:** the behaviour of `TaskStop`, `/loop`, `/goal`, `/batch` and auto mode can't be checked from repo files, so it isn't confirmed current |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural coverage:** `test_rules_structure.py` scans every native rule file (line 116)<br>• 🧪 **Reference guarded:** `test_aliases.py` requires each Testing automation alias to name this file's path, and `test_always_on_reachability.py` counts it<br>• 🔍 **No incident, so no regression test needed:** the rubric doesn't call for one<br>• ⚠️ **No consistency check:** nothing checks the numeric limits against `automation_troubleshooting.md` or `_turn_budgets.md`, and no recorded run in the files shows the tests passing |
| **Overall** | **6.4/10** | 2026-10-27 | • 💪 **Concrete guardrails:** every command has measurable caps, a kill-switch and an approval gate<br>• ⚠️ **Wrong tier:** narrow, experimental content is always-on<br>• ⚠️ **Unsourced limits:** no evidence behind the numbers, and the stop guidance and loop/goal examples contradict each other |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_turn_budgets.md` — Currency and Test Coverage
- `src/claude/rules/_rules_lazy_load/claude_config/automation_troubleshooting.md` — Currency, Token Cost and Test Coverage
- `src/claude/aliases.md` — Evidence of Need and Token Cost
- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — Evidence of Need (comparison)
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/_tests/_root_files/test_aliases.py` — Test Coverage
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
