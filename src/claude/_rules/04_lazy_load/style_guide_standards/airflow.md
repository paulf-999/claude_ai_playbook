# 🌬️ Airflow Style Guide & Standards

**Purpose:** Define standards for Apache Airflow DAGs and pipelines. Standards ensure reliability, debuggability, and maintainability across all workflows in the platform.

**Scope:** All DAGs in `dmt_airflow_dags/` repository. Standards apply to task definition, error handling, scheduling, and dependency management.

## 📋 Child pages

| File | Purpose | When to load |
|------|---------|-------------|
| [`airflow/dag_design.md`](airflow/dag_design.md) | DAG file structure, naming conventions, mandatory attributes | Creating a new DAG |
| [`airflow/dag_configuration.md`](airflow/dag_configuration.md) | config.yaml fields, default args, scheduling, tags, documentation | Configuring DAG behavior |
| [`airflow/tasks_and_operators.md`](airflow/tasks_and_operators.md) | Task design, operator selection, dependencies, TaskGroups, XComs | Writing DAG logic |
| [`airflow/best_practices.md`](airflow/best_practices.md) | Idempotency, catchup, retries, error handling, testing | Debugging DAG failures |
| [`airflow/connections_and_variables.md`](airflow/connections_and_variables.md) | AKV-backed connections/variables, naming, provisioning | Configuring external integrations |

---

## 🏗️ Core Principles

**These four principles define all DAG design decisions:**

1. **Idempotency** — Re-running the same logical date produces identical results
   - Why: Airflow backfills and retries are common; non-idempotent DAGs accumulate corrupted data
   - How: Dedupe inputs, upsert rather than insert, make task result independent of prior runs
   - Test: Verify that running a DAG twice produces same data in warehouse

2. **Atomicity** — One task = one logical operation; no bundling unrelated steps
   - Why: Failure granularity enables targeted retries without re-running successful work
   - How: Split long pipelines into focused tasks; use TaskGroups for related work
   - Test: Can I identify why a failed task failed without inspecting adjacent tasks?

3. **Config-driven** — Never hardcode environment-specific values; use Airflow Variables or config.yaml
   - Why: Same DAG code runs in dev/ci/prod; hardcoded values block safe transitions
   - How: All env-specific values (warehouse size, slack channels, S3 paths) → Variables
   - Test: Can I change the environment by only modifying Variables, not code?

4. **Fail fast** — Configure retries deliberately; surface errors immediately; don't silently swallow failures
   - Why: Silent failures corrupt downstream data; deliberate retries handle transient issues
   - How: Set retries based on actual SLA (3x for flaky, 0x for non-transient); use `on_failure_callback`
   - Test: Do I know why a DAG failed within 10 seconds of checking Airflow UI?

---

## ⚠️ Common Mistakes & Recovery

| Mistake | Impact | How to fix |
|---------|--------|-----------|
| Hardcoded warehouse size | Wrong cost/performance tradeoff | Move to Variables: `Variable.get("WH_SIZE")` |
| No retries on flaky tasks | Overnight DAG failures block analysis | Add `retries=3, retry_delay=timedelta(minutes=1)` |
| SQL inserted fresh without upsert logic | Duplicate rows after retries | Use `CREATE OR REPLACE TABLE` / `MERGE` instead of `INSERT` |
| Tasks bundled into single operator | Single failure blocks entire pipeline | Split into separate tasks with explicit dependencies |
| No error notification | Failures discovered hours later | Add `on_failure_callback` to notify Slack/Teams |

---

## 🎯 DAG Lifecycle

```
1. Design
   └─ Idempotent? Atomic? Config-driven? Fail-fast?

2. Development
   └─ Test locally; verify idempotency by running twice

3. Code review
   └─ Reviewer checks principles against DAG file

4. CI validation
   └─ Pre-commit validates DAG syntax, Variable references

5. Production backfill
   └─ Run DAG for past N days; verify results identical across runs

6. Scheduling
   └─ Enable schedule_interval; monitor first week
```

---

## 📚 Related Rules

- **style_guide_standards/sql.md** — SQL standards within Airflow tasks
- **style_guide_standards/utilities/makefile_style_guide.md** — DAG testing and invocation patterns
- **testing.md** — How to test Airflow DAGs locally

---

## ✅ DAG Acceptance Checklist

Before marking a DAG as production-ready:

- [ ] All hardcoded env values moved to Variables
- [ ] Each task is atomic (single logical operation)
- [ ] Idempotency verified (run twice, compare results)
- [ ] Retries configured based on actual failure patterns
- [ ] Error notification enabled (Slack, Teams, or email)
- [ ] SQL follows style guide (SQLFluff passes)
- [ ] Documentation updated in DAG description
