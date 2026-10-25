# Quality Scorecard — authoring_skills.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.3/10

**Recommended improvements:**
- Resolve line 45's `patterns/` ban against line 47's `reference/patterns/` exception
- Update line 31's "~60 lines" to match `_core_standards.md` line 20's instructions exemption
- Make the drafts-path guidance agree between `_core_standards.md` line 34 and the hard gates
- Add a content-regression test for the 2026-10-01 incident in `_core_standards.md` line 37

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear opening:** line 11 tells the reader to go through the five children in order and finish with the checklist.<br>• ⚠️ **Contradicting exception:** `authoring_skills.md` line 45 bans `patterns/` subdirectories, then line 47 allows `reference/patterns/`.<br>• ⚠️ **Line budget differs:** line 31 says SKILL.md is "~60 lines", but `_core_standards.md` line 20 says "~60 lines plus the instructions section". |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (naming, structure, instructions, contract, maturity, triggers, scope, orphans, file layout) + Scope 2 (`skills/`, `_reference/_quality_scorecards/skills/`, `_tests/skills/`) + Dependencies 0 + Prerequisites 0, matching the ~5 anchor.<br>• ⚠️ **Wide spread:** about a dozen concepts across a parent and five children (`_core_standards.md` alone covers naming, structure, description, contract and maturity). |
| **Evidence of Need** | 8/10 | 2026-10-25 | • 🔗 **Dated incidents:** `_core_standards.md` line 37 (instructions pushed into `reference/` and skipped, 2026-10-01).<br>• 🔗 **Audit evidence:** `_no_orphaned_files.md` line 14 (2026-09-19 audit: 16, 6 and 3 unreachable or missing files across three skills).<br>• ⚠️ **No repeat-use record:** no usage CSV or session count shows how often the rule is applied, so it falls short of the ~9 anchor. |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • 🎯 **Justified header:** `applies_to: **/skills/**` and a `loading:` reason (new-skill gap) are set on lines 4 and 6.<br>• 💪 **Lean parent:** the bulky detail is in five on-demand children, and the parent is 50 lines.<br>• ⚠️ **Loads everywhere:** the always-on "File Organization" block (lines 25–49) loads in sessions that never touch `skills/`. It is more than the pointer the new-file gap needs. |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Header and shape:** metadata header on lines 1–3, emoji H1, Purpose line, 50 lines, no Related section, children wired with `**Read on demand:**`.<br>• ⚠️ **Multi-sentence paragraphs:** `authoring_skills.md` lines 41, 43 and 45 are bold-led paragraphs with two or three sentences each.<br>• ⚠️ **Missing bold keywords:** `_core_standards.md` lines 12–16, `_trigger_design.md` lines 17–21 and `_scope_and_maintenance.md` lines 29–37 have bullets without a bold keyword.<br>• ⚠️ **Spelling:** American "Organization" in the heading on line 25 (house style is British). |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths exist:** every path checked exists (`_templates/skills/SKILL.md.template`, `_quality_scorecard_template.md`, `skill_domains.yaml`, `test_no_orphaned_skill_files.py`, `capture_session_prompts.py`, `git_create_pr/skill.contract.yaml`).<br>• ⚠️ **Path guidance differs:** `_core_standards.md` line 34 says use `~/claude/_drafts/<domain>/`, but `_hard_gates_checklist.md` line 27 says `$HOME`-based paths.<br>• ⚠️ **Stale line limit:** parent line 31 ("~60 lines") predates the instructions-section exemption. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Content tests:** `_tests/rules/03_authoring_guidelines/test_authoring_skills.py` checks that the children resolve, the six sections stay in order, the frontmatter example is valid and the contract fields match. It also checks that the maturity eval counts and complexity caps match the checklist and `_complexity_scoring.md`.<br>• 🧪 **Mechanical backstop:** `_tests/skills/_all_skills/test_no_orphaned_skill_files.py` enforces `_no_orphaned_files.md`.<br>• ⚠️ **Incident record not tested:** no `# wording-check: incident record` assert protects the 2026-10-01 record in `_core_standards.md` line 37. |
| **Overall** | **7.3/10** | 2026-10-25 | • 💪 **Strengths:** a slim always-on parent, lazy children backed by dated incidents, and a solid test that checks the parts agree.<br>• ⚠️ **Gaps:** wide concept spread, style slips in the children, wording that differs between files on paths and line budget, and no test for the incident record. |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/authoring_skills.md` — the rule being scored
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_skills.py` — Test Coverage dimension
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_test_metadata.md` — Test Coverage dimension (metadata-header format the test's own header is missing fields from)
