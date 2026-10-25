# Quality Scorecard — sql.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 5.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix `sql.md` line 49's advice to quote Snowflake identifiers with backticks, since Snowflake uses double quotes
- Update the SQLFluff codes on lines 47–49 and in `sql/sqlfluff.md` to current, correctly described rules
- Bring the `sql/cte_style_guide.md` examples in line with `sql/formatting.md` (no `SELECT *`, trailing commas or bare `JOIN`)
- Remove the duplicate child index, and give the children Purpose lines

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • 🔍 **Clear parent:** `sql.md` lines 27-32 and 93-101 give short principles and a checklist you can act on.<br>• ⚠️ **Children contradict each other:** `sql/cte_style_guide.md` lines 39-46 and 80-84 use `SELECT *`, trailing commas, single-letter aliases `o`/`c` and a bare `JOIN`, but `sql/formatting.md` lines 41, 43, 55 and 57 forbid all four.<br>• ⚠️ **L029 means two things:** `sql.md` line 48 says L029 is "Ambiguous reference", while `sql/sqlfluff.md` line 26 says L029 is "Keywords permitted as column names" and excluded, so a reader can't tell whether it's a violation to fix. |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3 (formatting, CTEs, data types, SQLFluff, dbt and cost guardrails) + Scope 1 (`_style_guide_standards/sql/`) + Dependencies 2 (SQLFluff, Snowflake, dbt) + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Breadth:** `sql.md` lines 53-70 mix dbt practice and warehouse sizing into the SQL style guide. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded need:** `sql.md` lines 12-14 state the purpose but cite no incident, PR or repeated failure.<br>• 🔗 **Partial:** the `miss_cost: medium` header on `sql.md` line 8 gives a reason but no usage record, and the pre-#184 regression in `_tests/rules/02_claude_standards/test_path_scoped_rules.py` lines 15 and 172-177 is a loading incident, not evidence the content is needed. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent mostly clean:** `sql.md` has `paths:`, a metadata header, an emoji H1 and a Purpose line, and is 102 counted lines once the frontmatter and comment lines are excluded.<br>• ⚠️ **Bullets without a bold keyword:** `sql.md` lines 39-41 and 66-70, plus `sql/sqlfluff.md` lines 13-15.<br>• ⚠️ **Children without a Purpose line:** `sql/sqlfluff.md` lines 4-9 have no `**Purpose:**`, and `sql/snowflake_data_type_standards.md` lines 6-8 use a numbered `## 1. Purpose` heading instead.<br>• ⚠️ **Contents out of place:** `sql/cte_style_guide.md` line 25 puts Contents after two sections and lists only 4 of its 6 headings.<br>• ⚠️ **Duplicate index:** the child list appears twice, in `sql.md` lines 18-23 and again in lines 105-110. |
| **Currency** | 5/10 | 2026-10-25 | • 🍂 **Old SQLFluff codes:** `sql.md` lines 47-49 use pre-2.0 codes L019, L029 and L031, and `sql/sqlfluff.md` lines 25-32 mix those with new-style LT15 and ST09.<br>• 🍂 **Wrong descriptions:** in current SQLFluff, L029 is keywords used as identifiers and L031 is table aliases, not what `sql.md` lines 48-49 say.<br>• ❌ **Wrong fix for Snowflake:** `sql.md` line 49 says to quote identifiers with backticks, but Snowflake uses double quotes.<br>• ⚠️ **Vague config pointer:** `sql/sqlfluff.md` lines 6-7 point at "the dbt project's `.sqlfluff`" with no repo or path.<br>• ⚠️ **Literal home paths:** `sql.md` lines 107-110 and `sql/cte_style_guide.md` line 23 hardcode `~/.claude/`. |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Structural guard:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 56 pins `sql.md`'s required headings, and the file also checks its header, Purpose line, child links and Contents.<br>• ✅ **Loading proven in a live session:** `_tests/rules/02_claude_standards/test_path_scoped_rules_live.py` lines 197-223 show `sql.md` loads when a `.sql` file is read and stays out when only a `.txt` file is.<br>• ⚠️ **Children not checked:** nothing caught the missing Purpose lines in `sql/sqlfluff.md` and `sql/snowflake_data_type_standards.md`, or the contradictions between `sql/cte_style_guide.md` and `sql/formatting.md`. |
| **Overall** | **5.7/10** | 2026-10-25 | • 💪 **Loading well tested:** the `paths:` trigger is proven in a live session, with a negative control.<br>• ⚠️ **Accuracy:** the child examples contradict the formatting rules, the SQLFluff codes are old and inconsistent, and the Snowflake quoting advice is wrong. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/sql.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/dbt.md` — Structural Compliance dimension (same dual-loading-pattern issue)

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/sql/sql.md` was deleted in #90, confirmed absent on 2026-10-01.
- ✅ **Resolved:** the dual child-loading pattern went when #184 replaced the `@./` imports with a Read on demand section.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
