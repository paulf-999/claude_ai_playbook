# Quality Scorecard — terraform.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Split `terraform/structure.md` (145 lines) and `terraform/conventions.md` (142 lines) to fit the 110-line limit
- Resolve `conventions.md` line 82's "declare all three" against line 88's optional `default`
- Give the children `_` prefixes and Purpose lines, and record evidence of need

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear parent:** `infra/terraform.md` lines 12–29 make the purpose, child map and five principles easy to follow.<br>• ⚠️ **Self-contradiction:** `terraform/conventions.md` line 82 says "Every variable must declare all three", but line 88 says to leave `default` out unless a safe default exists.<br>• ⚠️ **Mixed signal:** `terraform/ci_and_tooling.md` line 49 draws the PR stages as a sequence (`DEV → UAT → …`) but labels them "all in parallel on PR". |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 + Scope 1 + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Many concepts:** the 4 children cover layout, naming, validation, modules, lifecycle, pre-commit and two pipelines, which is 6+ concepts across `infra/terraform/`. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded need:** no incident, PR or usage record appears in the parent or any child.<br>• ⚠️ **Hypothetical miss cost:** `infra/terraform.md` line 8 (`miss_cost: medium — modules that fail review or plan checks`) describes a possible failure, not one that happened.<br>• 💡 **Note:** the concrete repo layout in `terraform/structure.md` lines 10–30 suggests a real codebase, but no file records any use. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 5/10 | 2026-10-25 | • ✅ **Parent clean:** `infra/terraform.md` has the `paths:` frontmatter, a metadata header (lines 5–7), an emoji H1, a Purpose line and 30 lines.<br>• ⚠️ **Over length:** `terraform/structure.md` (145 lines) and `terraform/conventions.md` (142 lines) are both past the 110-line limit and not split.<br>• ⚠️ **No Purpose lines:** each child opens with a plain sentence instead (`terraform/structure.md` line 6, `conventions.md` line 6, `modules.md` line 6, `ci_and_tooling.md` line 6).<br>• ⚠️ **Child naming:** the children have no `_` prefix (`terraform/structure.md`, not `_structure.md`), against the child-file rule in `_hard_gates_checklist.md` line 16.<br>• ⚠️ **Bullet style:** `infra/terraform.md` lines 25–29 use a bold keyword with an em dash instead of a colon.<br>• ⚠️ **No bold keywords:** `terraform/structure.md` lines 81–84 open with no bold keyword at all.<br>• ⚠️ **Contents placement:** each child puts its Contents after the first section, and the Contents leaves that section out (`structure.md` line 32, `conventions.md` line 30, `modules.md` line 25, `ci_and_tooling.md` line 25). |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Links resolve:** all 4 child links in `infra/terraform.md` lines 18–21 point to files that exist.<br>• 🔍 **Unverifiable paths:** `terraform/ci_and_tooling.md` lines 52 and 68 name pipeline templates under `src/cicd/pipelines/`, which live in another repo and can't be checked from here.<br>• 🔍 **Unverifiable version:** `terraform/structure.md` line 99 pins Snowflake provider `2.5.0`, and nothing records when that was last checked.<br>• ⚠️ **Header lag:** the children's headers were last updated 2026-09-17, while the parent was updated 2026-10-10. |
| **Test Coverage** | 7/10 | 2026-10-25 | • ✅ **Parent guarded:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 49 tracks the parent's header, Purpose line, child links, link resolution and its two H2 headings.<br>• ⚠️ **Children unchecked:** no test checks the children's headers, Purpose lines or line counts, so the over-length files and missing Purpose lines in `terraform/*.md` get through.<br>• 💡 **Note:** no incident is recorded, so no content-regression test is needed. |
| **Overall** | **6.2/10** | 2026-10-25 | • 💪 **Strength:** a short, well-loaded parent with a clear child map and a structural test that checks it.<br>• ⚠️ **Gap:** the children are over length, have no Purpose lines, break the `_` naming rule and contradict themselves once.<br>• ⚠️ **Gap:** nothing records evidence of need. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/terraform.md` — the rule being scored
