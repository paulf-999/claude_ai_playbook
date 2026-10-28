# Quality Scorecard — airflow.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Choose one place for retries, either the central `common.get_dag_default_args()` or each DAG's `default_args`, and make the parent, `_best_practices.md` and `_dag_configuration.md` all say the same thing
- Add `retries` and `retry_delay` to the team-standard `default_args` block in `_dag_configuration.md`, or stop the parent telling readers to inherit `retries=3` from it
- Make the parent's idempotent-write fix match `_best_practices.md`, which uses `INSERT OVERWRITE` / `MERGE`, and drop `CREATE OR REPLACE TABLE`, which throws away history on incremental loads
- Make the acceptance checklist agree with the mistakes table on retries ("based on actual failure patterns" vs "inherit `retries=3`")
- Record a dated incident or usage evidence (for example a DAG review that missed one of these principles) next to the `miss_cost` comment
- Say whether CI, pre-commit or both validate DAGs, and name the hook or command, so the parent's lifecycle step 4 agrees with `_best_practices.md`'s Testing section
- Fix the style slips: "behavior" → "behaviour", one sentence on the Scope line, and bold-keyword-colon openers on the principle and checklist items
- Add a content check that the parent and child pages give the same retry and write-pattern values

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-28 | • 💪 **Actionable principles:** each of the four principles has a Why, a How and a self-check Test (lines 33–51)<br>• ⚠️ **Retry source conflict:** line 50 and line 60 say to inherit `retries=3, retry_delay=5min` from `default_args`, but `_dag_configuration.md` line 67 sets default args centrally in `common.get_dag_default_args()` with no retries in its team-standard block<br>• ⚠️ **Child contradicts sibling:** `_best_practices.md` line 36 says to configure retries in `default_args`, while `_dag_configuration.md` line 67 says not to redefine default args in DAG files<br>• ⚠️ **Write-pattern mismatch:** line 61 recommends `CREATE OR REPLACE TABLE` / `MERGE`, while `_best_practices.md` line 12 says `INSERT OVERWRITE` / `MERGE`<br>• ⚠️ **Checklist vs table:** line 98 says "Retries configured based on actual failure patterns", which pulls against the fixed `retries=3` on line 60 |
| **Complexity** | 5/10 | 2026-10-28 | • 🧮 **Raw complexity 5:** Concepts 2 (four principles, mistakes table, lifecycle, checklist) + Scope 1 (parent plus the `airflow/` child folder) + Dependencies 2 (Airflow's `common` helpers, SQLFluff and the SQL style guide) + Prerequisites 0 |
| **Evidence of Need** | 5/10 | 2026-10-28 | • ⚠️ **No recorded incident:** the only signal is `<!-- miss_cost: medium — DAGs that fail review or misbehave on schedule -->` (line 8), with no dated failure, review finding or usage record<br>• 🔗 **Plausible need:** the mistakes table (lines 57–63) lists realistic failure modes, but nothing shows they have actually happened |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/dags/**/*.py"` (lines 1–4) loads it only when a DAG file is open, so it is left out of the average |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Within limits:** 102 lines, metadata header after the frontmatter, Purpose line, emoji H2s, and children in `airflow/_*.md` linked from a table<br>• ⚠️ **Spelling:** "Configuring DAG behavior" (line 21) uses American spelling<br>• ⚠️ **Multi-sentence lines:** the Scope line (line 14) runs two sentences<br>• ⚠️ **Bullet openers:** principles use `**Idempotency** — ` (lines 33–48) and the checklist items (lines 95–101) have no bold keyword, which breaks the bold-keyword-colon convention<br>• ⚠️ **Fence rendering:** the lifecycle block (lines 69–87) puts inline backticks inside a plain code fence, so they show up as literal characters |
| **Currency** | 7/10 | 2026-10-28 | • ✅ **Links resolve:** all four child pages and `org.md` exist, and the `~/.claude/` pointer form matches sibling guides such as `ansible.md` and `naming_standards.md`<br>• ⚠️ **Unbacked claim:** lifecycle step 4 "Pre-commit validates DAG syntax and config" (line 80) names no hook, and `_best_practices.md` line 76 puts that validation in CI instead<br>• 🔍 **Unverifiable externals:** `dmt_airflow_dags/` (line 14) and `common.get_default_dag_params()` (line 45) live outside this repo, so nothing here confirms they are current |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Dedicated structural test:** `test_lazy_load_rule_structure.py` tracks `airflow.md` (line 47), checking its required H2s, metadata header, Purpose line, child links, relative links, and the `_` prefix and Purpose line on each child<br>• ⚠️ **No consistency check:** nothing tests that the parent and children agree, which is exactly where the Clarity gaps above sit<br>• 🔍 **No incident test owed:** the rule documents no real incident, so the rubric does not require a content-regression test |
| **Overall** | **6.3/10** | 2026-10-28 | • 💪 **Strong spine:** clear principles with self-checks, path-scoped loading and a dedicated structural test<br>• ⚠️ **Parent–child drift:** retry source and idempotent-write guidance disagree across the parent, `_best_practices.md` and `_dag_configuration.md`<br>• ⚠️ **Thin evidence:** no dated incident or usage record |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/airflow.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/airflow/_best_practices.md` — Clarity (retries, write pattern) and Currency (CI validation)
- `src/claude/_reference/_style_guide_standards/airflow/_dag_configuration.md` — Clarity (central default args with no retries)
- `src/claude/_reference/_style_guide_standards/airflow/_dag_design.md` — Structural Compliance (linked child page)
- `src/claude/_reference/_style_guide_standards/airflow/_tasks_and_operators.md` — Structural Compliance (linked child page)
- `src/claude/rules/_rules_lazy_load/org.md` — Currency (read-on-demand pointer target)
- `src/claude/_reference/_style_guide_standards/infra/ansible.md` — Currency (same `~/.claude/` pointer form)
- `src/claude/rules/01_essentials/claude_usage_standards/naming_standards.md` — Currency (same `~/.claude/` pointer form)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity formula
