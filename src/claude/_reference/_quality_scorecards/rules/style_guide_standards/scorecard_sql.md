# Quality Scorecard — sql.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the Child pages table and the line 41 link resolve after install, or delete the table and keep only the absolute `Read on demand` pointers.
- Change "optimization" (line 12) and "prioritize" (line 30) to British spelling, and give the Tooling and dbt-specific bullets a bold keyword and colon.
- Say exactly what "scan count jumps >20%" measures (bytes or partitions scanned) and where to read it.
- Say which repo's pre-commit runs SQLFluff, and how ad-hoc queries are checked when no hook covers them.
- Fix `sql/_formatting.md`'s `UPDATE` example so it uses leading commas, matching its own leading-comma rule.
- Add a test that every child link in an installed path-scoped style guide resolves.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-28 | • 🔍 **Clear core:** principles, the dbt `ref()`/`source()` rules and the pre-commit checklist can be acted on as written<br>• ⚠️ **Vague metric:** "flag in PR if scan count jumps >20%" (line 69) doesn't say whether it means bytes or partitions scanned, or where to read it<br>• ⚠️ **Enforcement scope:** line 12 covers "ad-hoc queries", but line 14 says all SQL "must pass SQLFluff validation before commit", and ad-hoc queries aren't committed<br>• ⚠️ **Child contradiction:** `sql/_formatting.md` asks for leading commas, but its own `UPDATE` example uses trailing commas |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 2 (tooling, dbt, cost, mistakes, checklist) + Scope 1 (parent plus the `sql/` folder) + Dependencies 2 (SQLFluff, dbt, Snowflake) + Prerequisites 1 (the dbt repo's `.sqlfluff`)<br>• ⚠️ **Mixed concern:** `AUTO_SUSPEND = 60` and warehouse sizing (lines 63–67) are warehouse settings, not SQL style |
| **Evidence of Need** | 8/10 | 2026-10-28 | • 📈 **Recorded use:** `docs/audits/rule_usage_sessions.csv` shows it loading in 5 sessions between 2026-09-09 and 2026-10-01<br>• 🔗 **Loading incident:** `test_path_scoped_rules.py` records the PR #184 incident, where its `@` imports loaded every session<br>• ⚠️ **Unbacked thresholds:** no file records where the 20% scan threshold or "PR cannot merge without it" (line 88) came from |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/*.sql"` means it loads only when a `.sql` file is read, and `test_path_scoped_rules_live.py` proves it stays out of a `.txt`-only session |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and Purpose:** has the metadata header, emoji headings and Purpose line<br>• ⚠️ **At the limit:** 110 lines, the top of the tolerated range<br>• ⚠️ **American spelling:** "optimization" (line 12) and "prioritize" (line 30)<br>• ⚠️ **Bullet format:** Tooling (lines 39–41) has no bold keywords, and dbt-specific (lines 54–57) uses "**…** —" instead of keyword + colon<br>• ⚠️ **Listed twice:** the four children appear in both the Child pages table and the Read on demand section |
| **Currency** | 7/10 | 2026-10-28 | • 🔍 **Children exist:** all four `sql/_*.md` files named exist, and the SQLFluff dialect matches `sql/_sqlfluff.md`<br>• ✅ **Quoting fixed:** line 48 now quotes Snowflake identifiers with double quotes<br>• ⚠️ **Links break once installed:** `split_style_guides` moves `sql.md` to `rules/02_claude_standards/path_scoped_rules/style_guide_standards/` and leaves `sql/` in `_reference/`, so the relative links on lines 20–23 and 41 don't resolve |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structure:** `test_lazy_load_rule_structure.py` requires its four key headings<br>• 🧪 **Regression:** `test_path_scoped_rules.py` fails if it brings back the pre-#184 `@` imports<br>• 🧪 **Live load:** `test_path_scoped_rules_live.py` checks its `paths:` trigger and both its load and no-load cases<br>• ⚠️ **No link check:** no test confirms the child links resolve in the installed layout |
| **Overall** | **6.7/10** | 2026-10-28 | • 💪 **Well tested loading:** path-scoped, with live and regression tests and recorded usage<br>• ⚠️ **Gaps:** child links break after install, plus style slips and two vague enforcement claims |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/sql.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/sql/_formatting.md` — Clarity (comma contradiction), Currency
- `src/claude/_reference/_style_guide_standards/sql/_sqlfluff.md` — Currency (dialect check)
- `src/claude/_reference/_style_guide_standards/sql/_cte_style_guide.md` — Currency (child exists)
- `src/claude/_reference/_style_guide_standards/sql/_snowflake_data_type_standards.md` — Currency (child exists)
- `src/claude/_install/helpers/claude_file_utils.sh` — Currency (`split_style_guides` install layout)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `docs/audits/rule_usage_sessions.csv` — Evidence of Need
- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules.py` — Evidence of Need, Test Coverage
- `src/claude/_tests/rules/02_claude_standards/test_path_scoped_rules_live.py` — Token Cost, Test Coverage
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
