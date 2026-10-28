# Quality Scorecard — dbt.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the source-test requirement say the same thing in every section, and define "completeness" or drop it (lines 47, 89, 114).
- Swap the `dbt-labs/corp` link for the current dbt Labs best-practices page, and back up "checked in CI" with a named job or remove the claim (line 15).
- Add a dated incident or record of use showing models that broke naming or layering.
- Bring the file to 110 lines or fewer by merging the Development Workflow block into the Acceptance Checklist, which repeats it.
- Use British spellings ("organisation", "materialisation") throughout, and cut the Purpose and Scope lines to one sentence each.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-28 | • 🔍 **Clear core:** the `ref()`/`source()` and description rules say exactly what to do and how to check it (lines 35–43)<br>• ⚠️ **Source tests conflict:** line 47 asks for freshness "where they fit", but lines 89 and 114 make "freshness, completeness" source tests a must<br>• ⚠️ **Undefined term:** "completeness" (lines 89, 114) isn't a dbt test, and nothing in the file defines it<br>• ⚠️ **Principle wider than its How:** line 45 says "all sources and logical joins have tests", but line 47 only asks for `KEY` tests |
| **Complexity** | 4/10 | 2026-10-28 | • 🧮 **Raw complexity 6:** Concepts 3 (lineage, docs, tests, materialisation, layers, naming, workflow, checklist) + Scope 1 (one parent plus `dbt/` with five children) + Dependencies 2 (dbt plus Snowflake and SQLFluff) + Prerequisites 0 — see `_complexity_scoring.md` |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded incident:** the only sign of need is the `miss_cost: medium` comment (line 9), with no dated failure, issue or usage record in any file |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths:` limits loading to `**/models/**/*.sql` and `**/dbt_project.yml` (lines 2–4), so it isn't always-on |
| **Structural Compliance** | 6/10 | 2026-10-28 | • ✅ **Header and split:** has the metadata header, Purpose line, emoji H2s, and five linked `_`-prefixed children<br>• ⚠️ **Over length:** 120 lines, past the 110 tolerated, even with children already split out<br>• ⚠️ **Spelling mix:** "organization" (line 13) and "materialization" (lines 50, 118) next to "materialisation" (lines 51–53)<br>• ⚠️ **Multi-sentence lines:** Purpose (line 13) and Scope (line 15) are two sentences each<br>• ⚠️ **Repetition:** the Development Workflow (lines 78–104) and Acceptance Checklist (lines 112–119) repeat the Core Principles |
| **Currency** | 7/10 | 2026-10-28 | • ✅ **Local links resolve:** all five `dbt/_*.md` children and `sql.md` exist<br>• ⚠️ **External link likely stale:** `github.com/dbt-labs/corp/.../dbt_style_guide.md` (line 15) points at a guide dbt Labs has since moved to its docs site, and the reviewer couldn't check it<br>• ⚠️ **Unbacked claim:** "Standards are checked in CI" (line 15) names no CI job, and no file shows one |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `test_lazy_load_rule_structure.py` lists `dbt.md` (line 53) and checks its header, Purpose, child links, relative links and required H2s<br>• 🧪 **Frontmatter guard:** `test_path_scoped_rules.py` scans the style-guide folder (line 124)<br>• ⚠️ **Not run in this review:** the reviewer had no shell, so the pass is inferred from the test file, and nothing tests that the guidance stays consistent with itself, such as the line 47 vs 114 conflict |
| **Overall** | **6.2/10** | 2026-10-28 | • 💪 **Well-scoped:** path-scoped loading, linked children and a dedicated structural test<br>• ⚠️ **Thin evidence and drift:** no recorded need, a source-test rule that disagrees with itself, and an external link that's likely stale |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/dbt.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/dbt/_model_organisation.md` — child linked from line 21 (Currency)
- `src/claude/_reference/_style_guide_standards/dbt/_naming_conventions.md` — child linked from line 22 (Currency)
- `src/claude/_reference/_style_guide_standards/dbt/_yaml_resource_properties.md` — child linked from line 23 (Currency)
- `src/claude/_reference/_style_guide_standards/dbt/_snapshots.md` — child linked from line 24 (Currency)
- `src/claude/_reference/_style_guide_standards/dbt/_macros.md` — child linked from line 25 (Currency)
- `src/claude/_reference/_style_guide_standards/sql.md` — sibling linked from line 27 (Currency)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — structural test (Test Coverage)
- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules.py` — frontmatter test (Test Coverage)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — complexity formula (Complexity)
