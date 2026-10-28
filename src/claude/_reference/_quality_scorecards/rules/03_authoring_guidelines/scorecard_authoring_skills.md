# Quality Scorecard — authoring_skills.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.6/10

**Recommended improvements:**
- Record each time a skill shipped without a contract or evals, so the parent's `miss_cost` claim has dated evidence behind it.
- Add `applies_to: *`, or move the rule into `path_scoped_rules/` with a skill-authoring trigger, so where it loads matches what `applies_to` says.
- Add a test that checks a skill's folder against the File Organisation section, so a missing `tests/README.md`, a root-level `evals.yaml` or an extra subfolder fails the build.
- Mark in the tree whether `reference/_implementation.md` is required or optional, as `_formats.md` already is.
- Join the two "Exception" bullets to the list above them, and reword "Nothing else: add no…" as a positive instruction.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear pointers:** each of the five "Read on demand" lines says what that child covers.<br>• 🔍 **Clear layout:** the tree plus five bullets say exactly what a skill folder may hold.<br>• ⚠️ **Optional or required:** line 35 marks `_formats.md` "(if applicable)", but line 34's `_implementation.md` says neither. |
| **Complexity** | 7/10 | 2026-10-27 | • 🧮 **Raw complexity 3:** one concept (how a skill folder is laid out), but its scope covers `skills/`, `_reference/_quality_scorecards/skills/` and `_tests/skills/`, and it depends on five lazy children. |
| **Evidence of Need** | 7/10 | 2026-10-27 | • 🔗 **Children's incidents:** `_core_standards.md` line 37 records an incident on 2026-10-01, and `_no_orphaned_files.md` line 14 records a 2026-09-19 audit across three skills.<br>• ⚠️ **Parent unbacked:** the parent's own `miss_cost` ("skills ship without contracts or evals") has no dated incident or usage record.<br>• ⚠️ **Reasoning only:** the `tests/` folder rule is argued from readability (line 43), not from an observed problem. |
| **Token Cost Justification** | 6/10 | 2026-10-27 | • 🎯 **Lean:** 50 lines, and the long content sits in lazy children.<br>• ⚠️ **Mismatch:** it loads in every session, but line 4 says `applies_to: **/skills/**`, so most of the sessions it loads in don't need it.<br>• 💡 **Reason given:** line 6 explains that a new skill can start before any `skills/` file is open, which softens the mismatch without fixing it. |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Header and length:** a full metadata header (version, dates, applies_to, miss_cost, loading), an emoji H1, a Purpose line and 50 lines.<br>• ⚠️ **List gaps:** blank lines at 46 and 48 split the two "Exception" bullets off from the list above.<br>• ⚠️ **Negative wording:** line 45's "add no `templates/`…" is phrased as a ban, which `writing_style.md` asks to avoid.<br>• ⚠️ **Not run:** the reviewer read but did not run `test_rules_structure.py` or the header tests. |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **Paths exist:** all five children, `_reference/_quality_scorecards/skills/`, `capture_session_prompts.py` and `_tests/skills/claude_capture_session_prompts/` exist.<br>• ✅ **Matches practice:** all 8 skills keep `evals.yaml` in `tests/` with a `README.md` beside it.<br>• 🔍 **Pointer prefix:** the pointers use `~/.claude/`, as the sibling rules in this tier do, and the repo alone can't show whether the install rewrites it to `~/claude/`. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Content tests:** `test_authoring_skills.py` checks that the children resolve, the six SKILL.md sections (the 2026-10-01 incident), the contract fields, eval counts and complexity caps.<br>• ⚠️ **Layout untested:** no test covers the parent's File Organisation section, meaning the mandatory `tests/README.md`, the ban on `evals.yaml` at skill root and the "nothing else" rule.<br>• 🔍 **Checked:** `test_skill_structure_compliance.py` only writes `tests/evals.yaml` into a test fixture. |
| **Overall** | **7.6/10** | 2026-10-27 | • 💪 **Thin parent:** a short, current parent that sends the detail to tested lazy children.<br>• ⚠️ **Gaps:** loads in every session against a narrow `applies_to`, the File Organisation section has no test, and the parent has no evidence of its own. |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_skills.md` — the rule being scored
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/_core_standards.md` — Evidence of Need (2026-10-01 incident)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/_no_orphaned_files.md` — Evidence of Need (2026-09-19 audit)
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/_trigger_design.md` — Currency
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/_scope_and_maintenance.md` — Currency
- `src/claude/rules/_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/_hard_gates_checklist.md` — Currency, Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — Token Cost Justification (applies_to and loading fields)
- `src/claude/skills/_claude_skills/claude_capture_session_prompts/capture_session_prompts.py` — Currency
- `src/claude/_tests/skills/claude_capture_session_prompts/test_capture_session_prompts.py` — Currency
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_skills.py` — Test Coverage
- `src/claude/_tests/skills/_all_skills/test_skill_structure_compliance.py` — Test Coverage
