# Quality Scorecard — airflow.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 5.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the parent and `airflow/best_practices.md` agree on Variables vs `config.yaml`, retries and retry delay
- Move callbacks to `includes/` or change `dag_design.md` line 18, so the two agree
- Replace the deprecated `schedule_interval` and `execution_date` with `schedule` and `logical_date`
- Replace the literal `~/.claude/` paths, and give the bullets bold keywords

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 5/10 | 2026-10-25 | • ⚠️ **Variables contradiction:** `airflow.md` lines 43–45 and 59 send env values to Airflow Variables (`Variable.get("WH_SIZE")`), but `airflow/best_practices.md` lines 84–87 say to use `config.yaml` and never read Variables in `dag.py`<br>• ⚠️ **Retries contradiction:** `airflow.md` line 50 allows "0x for non-transient", but `airflow/best_practices.md` line 37 says never set retries to `0` in production<br>• ⚠️ **Retry delay drift:** `airflow.md` line 60 uses `retry_delay=timedelta(minutes=1)`, but `airflow/best_practices.md` line 45 uses 5 minutes<br>• ⚠️ **Callback location:** `airflow/best_practices.md` line 56 puts callbacks in `plugins/callbacks.py`, but `airflow/dag_design.md` line 18 says shared code goes in `includes/`, "not `plugins/`" |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3 (6+ topics: idempotency, naming, config, operators, retries, testing and more) + Scope 1 (one parent plus the `airflow/` folder) + Dependencies 2 (Airflow, Snowflake, dbt and Airbyte) + Prerequisites 0 — see `_complexity_scoring.md`<br>• ⚠️ **Wide reach:** `airflow.md` lines 18–23 fan out to 4 children plus a `templates/` folder |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ✅ **Drawn from real practice:** `airflow/dag_design.md` line 75 overrides "older Confluence guidance", and the `common.get_default_dag_params` helpers point to a real team repo<br>• ⚠️ **No recorded need:** no dated incident, PR or usage record anywhere in `airflow.md` (lines 1–102) or its children, so it sits below the "one real use" anchor |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and length:** `paths:` frontmatter, metadata header (lines 5–9), emoji H1 and 102 lines, all within the limit<br>• ⚠️ **Hardcoded paths:** `airflow.md` line 25 and `airflow/dag_configuration.md` lines 22 and 61 use a literal `~/.claude/` (as do `airflow/tasks_and_operators.md` lines 67 and 101), which breaks the hard gate's `portable_paths.md` check<br>• ⚠️ **Bullet style:** `airflow.md` lines 34–51 open bullets with plain `Why:`/`How:`/`Test:` instead of bold keywords<br>• ⚠️ **Purpose length:** `airflow.md` line 12 is two sentences, not one line<br>• ⚠️ **Contents placement:** `airflow/dag_design.md` line 44 (and the same pattern in the other children) puts Contents after the first section, not at the top |
| **Currency** | 5/10 | 2026-10-25 | • 🍂 **Deprecated parameter:** `airflow.md` line 86 says "Enable schedule_interval", but `airflow/dag_configuration.md` line 36 calls it deprecated, and `airflow/tasks_and_operators.md` line 27 still lists it<br>• 🍂 **Deprecated context key:** `airflow/best_practices.md` lines 10 and 62 use `execution_date`, which Airflow 2.2+ replaced with `logical_date`<br>• ⚠️ **Stale module path:** `airflow/best_practices.md` line 56 names `plugins/callbacks.py`, while `airflow/dag_configuration.md` line 77 shows the team's real callbacks in `email_notifications` |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Runs:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 46 checks the header, Purpose line, required H2s, child links and link resolution, and `test_lazy_load_coverage.py` catches orphaned children<br>• ⚠️ **Children only checked through links:** the 4 child pages aren't in that test's `RULES` (lines 44–59), so their headers and Purpose lines are never tested<br>• ⚠️ **No consistency check:** no test catches the parent and children contradicting each other (see Clarity) |
| **Overall** | **5.7/10** | 2026-10-25 | • 💪 **Well split:** a short parent with path-scoped loading, four focused children and a tested structure<br>• ⚠️ **Contradictions and stale API names:** the parent and children disagree on Variables, retries, callbacks and `schedule_interval` |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/airflow.md` — the rule being scored

---

## 🚩 Pre-existing issues — since resolved

- ✅ **Resolved:** the orphaned duplicate `style_guide_standards/airflow/airflow.md` was deleted in #90, confirmed absent on 2026-10-01.
- 📋 **Disposition:** resolved by later PRs and kept here as a record.
