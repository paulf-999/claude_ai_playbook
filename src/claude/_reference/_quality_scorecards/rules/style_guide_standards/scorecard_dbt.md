# Quality Scorecard — dbt.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 5.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the parent's model layers and name prefixes match `dbt/model_organisation.md` and `dbt/naming_conventions.md`
- Replace the non-existent `dbt lineage` (lines 38 and 124) and complete `dbt docs generate` (lines 105 and 126)
- Fix line 78's uniqueness advice, which names a column-order test
- Split the parent to fit 110 lines, remove the duplicate child index and the literal `~/.claude/` paths

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 5/10 | 2026-10-25 | • ⚠️ **Parent contradicts child on layers:** `dbt.md` lines 21 and 61–67 list Staging/Base/Intermediate/Mart/Operations with `stg_orders`, `fct_orders` and `dim_customer`, but `dbt/model_organisation.md` lines 10–17 define four layers (Staging/Base/Mart/Publication), and `dbt/naming_conventions.md` lines 44–49 require `staging_`, `mart_` and `pub_` prefixes.<br>• ⚠️ **Wrong fix advice:** `dbt.md` line 78 tells you to fix a missing uniqueness test with `expect_table_columns_to_match_ordered_list`, which checks column order, not uniqueness.<br>• ⚠️ **Testing advice conflicts:** line 47 says to add `dbt_expectations` tests, while `dbt/model_organisation.md` line 33 and `dbt/yaml_resource_properties.md` line 38 say `unique` and `not_null` on `KEY`.<br>• ⚠️ **Materialisation conflicts:** line 52 says view for models that change often, but `dbt/model_organisation.md` line 14 says staging is always incremental. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (layers, naming, YAML, testing, materialisation, snapshots, macros) + Scope 1 (`dbt.md` plus the `dbt/` child folder and templates) + Dependencies 1 (dbt and its packages, `dbt/macros.md` lines 47–55) + Prerequisites 0.<br>• ⚠️ **Several jobs in one guide:** this matches the "~5 Raw 5" anchor. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded incident or use:** no file records a review failure, PR or usage count.<br>• ⚠️ **Unbacked claim:** `dbt.md` line 15 says "Standards are checked in CI", but nothing in the files shows that.<br>• 🔍 **Some sign of a real project:** `dbt/snapshots.md` line 10 says "Examples from the repo", but nothing dated or repeated. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 5/10 | 2026-10-25 | • 📏 **Over length:** `dbt.md` has 126 counted lines (136 minus frontmatter and metadata), past the 110 limit, even though it is already a parent with children.<br>• ⚠️ **Duplicate child index:** the Child pages table (lines 19–25) and the "Read on demand" section (lines 130–136) list the same five children twice.<br>• ⚠️ **Hardcoded paths:** lines 132–136 use a literal `~/.claude/`, which fails the "No hardcoded paths" hard gate (`_hard_gates_checklist.md` line 27).<br>• ⚠️ **Child naming:** `dbt/model_organisation.md` and its siblings have no `_` prefix (`_hard_gates_checklist.md` line 16).<br>• ⚠️ **Children have no Purpose line:** e.g. `dbt/model_organisation.md` line 6.<br>• ⚠️ **Bullet style:** the Core Principles sub-bullets (lines 36–53) use a plain `Why:`/`How:`/`Test:` with no bold keyword. |
| **Currency** | 5/10 | 2026-10-25 | • 🍂 **Command that doesn't exist:** `dbt.md` lines 38 and 124 rely on "`dbt lineage`", which is not a dbt CLI command.<br>• 🍂 **Incomplete command:** lines 105 and 126 give `dbt docs` without the `generate` subcommand.<br>• ⚠️ **Package entry is muddled:** `dbt/macros.md` line 50 names `dbt-labs/dbt_date` "via `godatadriven/dbt_date`".<br>• ✅ **Local links resolve:** `sql.md`, `../sql/cte_style_guide.md` and the three `dbt/templates/` files exist. |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Structural test runs:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 52 tracks `dbt.md` (its header, Purpose line, required H2s, child links, whether links resolve, and Contents entries).<br>• ✅ **Also checked by:** `_tests/rules/rules_lazy_load/test_lazy_load_coverage.py`.<br>• ⚠️ **Gaps the test can't see:** no check of the children's own Purpose lines, and no check that parent and children agree, which is the cause of the Clarity gaps. |
| **Overall** | **5.5/10** | 2026-10-25 | • 💪 **Strength:** correctly path-scoped, and the structural test runs.<br>• ⚠️ **Gap:** the parent's layers, naming, test advice and dbt commands contradict its own children or are wrong, and it runs past the line limit. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/dbt.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/airflow.md` — Structural Compliance dimension (sibling using only the link-table pattern)

---

## 🚩 Pre-existing issue disclosed, not fixed

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/dbt/dbt.md` was deleted in #90, confirmed absent on 2026-10-01.
- 🐛 **Dual child-loading pattern:** this file lists its 5 children in a markdown-link "Child pages" table AND separately `@./`-imports the same 5 files at the bottom — inconsistent with sibling style guides (`airflow.md`, `bash.md`), which use only the link table, and the effect of `@./` imports outside CLAUDE.md's own load chain isn't documented.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
