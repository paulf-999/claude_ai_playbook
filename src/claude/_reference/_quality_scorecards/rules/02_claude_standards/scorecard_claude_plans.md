# Quality Scorecard — claude_plans.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.1/10

**Recommended improvements:**
- Reconcile the gate exceptions in `claude_plans.md` line 31 with `_plan_mode_phase_gates.md` line 6
- Say which phase threshold wins, 3+ phases or every plan-mode phase
- Replace the literal `~/.claude/` prefix in `_plan_mode_phase_gates.md` lines 22, 27 and 35
- Give bullets bold keywords and use British spelling ("deprioritise", "summarise")

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Conflicting scope:** `claude_plans.md` line 31 waives gates for tightly coupled phases, but `claude_plans/_plan_mode_phase_gates.md` line 6 says plan-mode gates apply "without exception".<br>• 🔍 **Threshold drift:** the parent gates only 3+ phase work (line 15), but the child's line 8 gates every plan-mode phase, and neither says which rule wins.<br>• ⚠️ **Self-contradiction:** `_plan_mode_phase_gates.md` line 22 calls `TODO.md` "Read-only content" while allowing edits to it. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (phase gates, plan-mode approval, plan persistence, plan file format, plan status) + Scope 1 (parent plus 2 children in one folder) + Dependencies 1 (`make list_plans`/`clean_plans` and the `ExitPlanMode` harness) + Prerequisites 0.<br>• ⚠️ **Bundled concepts:** `_plan_file_format.md` lines 31–50 add a five-state status lifecycle on top of the table format. |
| **Evidence of Need** | 7/10 | 2026-10-25 | • ✅ **One real incident:** `_plan_mode_phase_gates.md` line 34 records the 2026-09-19 literal-`~` incident.<br>• ⚠️ **Parent unevidenced:** the core gate rule's only example (`claude_plans.md` line 80) is hypothetical, with no dated incident or usage record. |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • ⚖️ **Arguable:** `applies_to: *` (line 4) is fair for the gate principle, since any task can become multi-phase.<br>• ⚠️ **Narrow child always-on:** `_plan_file_format.md` (53 lines) matters only when writing a plan file in `_plans/`, yet it loads every session. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Basics met:** metadata header, emoji H1, Purpose line, 81 lines, and 2 children in `claude_plans/` named in `Loads on its own from:` lines.<br>• ⚠️ **No bold keywords:** `claude_plans.md` lines 24–27, 30–32 and 68–72 are bullets that don't open with a bold keyword.<br>• ⚠️ **Multi-sentence bullet:** `_plan_mode_phase_gates.md` line 22, and `_plan_file_format.md` lines 12 and 18 are multi-sentence paragraphs.<br>• ⚠️ **American spelling:** `claude_plans.md` uses "deprioritize" (line 17) and "Summarize" (lines 40 and 70), and `_plan_mode_phase_gates.md` line 22 uses "pre-authorized".<br>• ⚠️ **Negative framing:** `claude_plans.md` line 29 heading reads "Do NOT apply gates when". |
| **Currency** | 8/10 | 2026-10-25 | • 🔍 **Mostly current:** `test_clean_plans.py` and `test_audit_plans.py` exist, which supports the `make clean_plans`/`list_plans` behaviour in `_plan_file_format.md` lines 47–48.<br>• ⚠️ **Unverified targets:** I could not confirm that the `make list_plans` and `make install` targets (`_plan_file_format.md` lines 47–48) exist using only the allowed inputs.<br>• ⚠️ **Hardcoded prefix:** `_plan_mode_phase_gates.md` lines 22, 27 and 35 use a literal `~/.claude/`, which `portable_paths.md` warns breaks on non-default installs. |
| **Test Coverage** | 9/10 | 2026-10-25 | • 🧪 **Incident pinned:** `_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` asserts that the persistence section and the 2026-09-19 incident survive, and its asserts are tagged `wording-check`.<br>• ✅ **Status behaviour runs:** `_tests/scripts/test_clean_plans.py` tests the Plan status line parsing and folder filing.<br>• 🔍 **Structural assumed:** I didn't open `test_rules_structure.py` to confirm it covers these files. I assumed coverage because it scans every rule. |
| **Overall** | **7.1/10** | 2026-10-25 | • 💪 **Strength:** a real incident is recorded and pinned by a test, and the plan-status lifecycle is backed by script tests.<br>• ⚠️ **Gap:** the parent and child disagree on exceptions and the phase threshold, and several style slips remain (unbolded bullets, American spelling, multi-sentence bullets). |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` — Test Coverage dimension
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans/_plan_file_format.md` — Test Coverage dimension (untested child)
