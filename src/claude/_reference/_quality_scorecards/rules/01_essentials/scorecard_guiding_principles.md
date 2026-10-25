# Quality Scorecard — guiding_principles.md

**Date Created:** 2026-09-21
**Date Updated:** 2026-10-25

**Overall score:** 6.9/10

**Recommended improvements:**
- Align line 17's 200-line target with the 110-line rule limit, or say which files each applies to
- Record evidence of need, meeting the bar the rule sets on line 19
- Give the child `usage_evidence.md` emoji headings and bold-keyword bullets
- Spell out the ROI example on line 22 and what counts as "directly referenced" on line 15

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Actionable table:** each principle has Description, Rationale and How to apply columns, so a reader can apply it straight away.<br>• ⚠️ **Contradiction:** `rules/01_essentials/guiding_principles.md` line 17 says "keep each CLAUDE.md, rule and imported file under 200 lines". The rule limit in `_hard_gates_checklist.md` line 24 is 110 lines, which breaks the rule's own "remove conflicts" advice on line 25.<br>• ⚠️ **Vague bullets:** line 15 "Imports: only when directly referenced" doesn't say what counts as a reference.<br>• ⚠️ **Unclear example:** line 22 "manual 10 min < Claude 2 min + $5" uses a bare inequality that has to be decoded before it means anything. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (11 principles, lines 15–25), Scope 2 (covers settings, hooks, imports, rules and skills across several folders), Dependencies 0, Prerequisites 0.<br>• ⚠️ **Many concepts:** 11 separate principles sit in one always-on file, which matches the ~5 anchor ("several jobs, several folders"). |
| **Evidence of Need** | 6/10 | 2026-10-25 | • 🔗 **Cited sources:** lines 17–18 link the Claude Code memory docs for the size and enforcement claims.<br>• 🔗 **Reused:** `_reference/_quality_scorecards/rules/README.md` lines 75 and 87 build two scoring dimensions on this rule.<br>• ⚠️ **No dated incident:** neither `guiding_principles.md` nor `usage_evidence.md` records an incident, PR or usage count, so the rule doesn't meet the bar it sets itself on line 19 ("Require evidence"). |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • 🎯 **Headers set:** `applies_to`, `miss_cost` and `loading` are on lines 4–6, and the bulky evidence guidance is moved out to a lazy child (line 19).<br>• ⚠️ **Loads beyond its scope:** line 4 limits it to `**/claude/**, **/.claude/**`, but the file loads in every session, including non-config work. Line 6 only argues that path-scoping saves nothing *inside* the config.<br>• ⚠️ **Dense rows:** 11 long table rows (lines 15–25) for a medium miss cost (line 5). |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Parent clean:** the metadata header (lines 1–3), emoji H1 (line 7), Purpose (line 9), 26 lines and bold-keyword cell bullets all pass. There is no Contents section, which is correct with no `##` headings.<br>• ⚠️ **Child style slips:** `rules/_rules_lazy_load/claude_config/usage_evidence.md` `##` headings on lines 14, 24, 32 and 45 have no emoji. Its bullets on lines 26–30 and 47–49 don't open with a bold keyword followed by a colon (they use ❌ markers or bold without the colon).<br>• ⚠️ **Redundant line:** line 11 repeats the Purpose on line 9. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Pointer resolves:** the line 19 child `rules/_rules_lazy_load/claude_config/usage_evidence.md` exists.<br>• ⚠️ **Drifted limit:** line 17's 200-line target doesn't match the 110-line limit the authoring gates now use (`_hard_gates_checklist.md` line 24).<br>• ⚠️ **Unconfirmed commands:** no allowed input confirms `/doctor prompt-audit` (line 17) or `/faster-mode` (`usage_evidence.md` line 18). |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Dedicated test:** `_tests/rules/01_essentials/test_guiding_principles.py` checks the CLAUDE.md import discipline against three principles (docstring lines 13–15). `_tests/_shared_checks/test_resolved_rule.py` line 22 also uses this rule.<br>• 🧪 **No incident, no regression test needed:** the rule records no incident, so a content-regression test isn't required.<br>• ⚠️ **No recorded run:** no allowed input shows these tests or `test_rules_structure.py` passing. |
| **Overall** | **6.9/10** | 2026-10-25 | • 💪 **Foundational and lean:** 26 lines, a clean header, and the evidence detail moved out to a lazy child.<br>• ⚠️ **Gaps:** the 200-vs-110 line contradiction, 11 concepts in one always-on file, no recorded evidence of need, and style slips in the child. |

## 🔗 Related files

- `src/claude/rules/01_essentials/guiding_principles.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_guiding_principles.py` — Test Coverage dimension
- `src/claude/rules/03_authoring_guidelines/authoring_rules.md` — Evidence of Need dimension
- `src/claude/rules/02_claude_standards/git/_concurrent_sessions.md` — Evidence of Need dimension
- `src/claude/rules/_rules_lazy_load/claude_config/hooks_decision_framework.md` — Evidence of Need dimension
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance dimension
- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — Test Coverage dimension (the disclosed violation)

---

## 🚩 Pre-existing issue — found here, fixed separately

- 🐛 **Violation found:** `test_guiding_principles.py` (lines 32, 81) hardcoded `@~/.claude/` when parsing `@import` lines.
- 🚫 **Rule broken:** `portable_paths.md` forbids this — "never hardcode the `@~/.claude/` or `@~/claude/` import-prefix string when parsing `@import` lines."
- ✅ **Resolved:** fixed in PR #88, on its own hotfix branch rather than bundled into this scorecard PR.
- 📋 **Disposition:** per this config's pre-existing-issue disclosure rule — flagged here, fixed separately, not silently absorbed into scope.
