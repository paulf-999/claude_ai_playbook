# Quality Scorecard — automation_controls.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.1/10

**Recommended improvements:**
- State the interval floor once on line 27, without the conflicting sub-minute clause
- State the 20-turn cap on line 48 once
- Confirm or remove `/stop_loop` on line 31
- Record the basis for the 5-minute, 2-hour, 30-minute and 12-item thresholds
- Consider path-scoping or lazy-loading it, since the commands never auto-trigger

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • ⚠️ **Contradictory floor:** `_automation_controls.md` line 27 sets a "5-minute interval floor" and then says "sub-minute intervals are not allowed", so a 2-minute interval is both allowed and forbidden.<br>• ⚠️ **Redundant cap:** line 48 says "capped at 20 turns by default, or stop after 20 turns if the condition isn't met", which states one cap twice as if it were two.<br>• ⚠️ **Stop conflict:** line 32 says "don't interrupt mid-work", but kill-switch line 83 says "Stop immediately".<br>• ⚠️ **Batch threshold drift:** child `automation_troubleshooting.md` line 55 says use `/batch` for "10+ times", while parent line 73 rules it out only below 5 items. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (three commands plus kill-switch and permission gates), Scope 1 (parent plus a lazy child in another folder), Dependencies 1 (Claude Code `/loop`, `/goal`, `/batch` and `TaskStop`), Prerequisites 0.<br>• ⚠️ **Several jobs in one file:** lines 23–95 cover three separate features, each with its own caps and table. |
| **Evidence of Need** | 4/10 | 2026-10-25 | • ❓ **No incident:** line 8 offers only "powerful but risky", with no dated incident, PR or usage record in the rule or its child.<br>• ❓ **Unsourced thresholds:** the 5-minute floor (line 27), 2-hour runtime (line 30), 30-minute timeout (line 51) and 12-item limit (line 65) have no recorded basis. |
| **Token Cost Justification** | 5/10 | 2026-10-25 | • 💸 **Narrow use, always-on:** the caps matter only in sessions that explicitly invoke `/loop`, `/goal` or `/batch` (line 93 says none of them auto-trigger), yet about 100 lines load every session.<br>• ⚖️ **Rationale lives elsewhere:** the only justification is a comment in `_tests/rules/02_claude_standards/test_always_on_reachability.py` lines 83–84 ("a high miss cost can't rest on a pointer").<br>• ⚠️ **Not in the rule:** no `miss_cost`, `applies_to` or `loading` header appears in lines 1–3 (it may inherit them as a child, but that isn't stated). |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Within limits:** 102 lines, with the metadata header, emoji H1, Purpose line and a Contents section earned by 6 headings.<br>• ⚠️ **Style slips:** line 84 "**Don't restart** without investigating" has no bold-keyword colon.<br>• ⚠️ **Overloaded bullets:** lines 27 and 48 pack several clauses and a parenthetical into one bullet.<br>• ⚠️ **Loose prose:** line 8 sits as free prose outside the Purpose line. |
| **Currency** | 7/10 | 2026-10-25 | • 🔍 **Unverified command:** line 31 names `/stop_loop`, and nothing in the allowed inputs shows that it exists.<br>• ✅ **Paths resolve:** the `_turn_budgets.md` link (line 10) and the `automation_troubleshooting.md` pointer (line 101) both name files that exist. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Path pinned:** `_tests/_root_files/test_aliases.py` lines 28–30 and 119–124 check that the Testing automation aliases name this file.<br>• 🧪 **Reachability:** `test_always_on_reachability.py` line 83 counts it in the startup budget.<br>• ✅ **None owed:** the rule records no incident, so no content-regression test is required.<br>• ⚠️ **Unchecked consistency:** no test catches the parent/child threshold drift (line 73 vs child line 55), and no file records a structural-test pass. |
| **Overall** | **6.1/10** | 2026-10-25 | • 💪 **Concrete caps:** every command has explicit numbers, a kill-switch and use/don't-use tables.<br>• ⚠️ **Weak basis:** no evidence of need for any threshold, an always-on cost for commands that only run when invoked, and internal contradictions on lines 27, 32 and 48. |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency.md` — Currency dimension (the real file the stale reference should point to)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale reference:** the "Related Rules" section cites `claude_efficiency.md`, a filename that doesn't exist anywhere in this repo — the actual file is `claude_operational_efficiency.md`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
