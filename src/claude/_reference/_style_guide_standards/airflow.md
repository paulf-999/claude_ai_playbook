---
paths:
  - "**/dags/**/*.py"
---
<!-- version: 1.3.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
<!-- miss_cost: medium — DAGs that fail review or misbehave on schedule -->
<!-- loading: path-scoped — only applies to Airflow DAGs, so it loads when a DAG file is open -->
# 🌬️ Airflow Style Guide & Standards

**Purpose:** Define standards for Apache Airflow DAGs and pipelines. Standards ensure reliability, debuggability, and maintainability across all workflows in the platform.

**Scope:** All DAGs in `dmt_airflow_dags/` repository. Standards apply to task definition, error handling, scheduling, and dependency management.

## 📋 Child pages

| File | Purpose | When to load |
|------|---------|-------------|
| [`airflow/_dag_design.md`](airflow/_dag_design.md) | DAG file structure, naming conventions, mandatory attributes | Creating a new DAG |
| [`airflow/_dag_configuration.md`](airflow/_dag_configuration.md) | config.yaml fields, default args, scheduling, tags, documentation | Configuring DAG behavior |
| [`airflow/_tasks_and_operators.md`](airflow/_tasks_and_operators.md) | Task design, operator selection, dependencies, TaskGroups, XComs | Writing DAG logic |
| [`airflow/_best_practices.md`](airflow/_best_practices.md) | Idempotency, catchup, retries, error handling, testing | Debugging DAG failures |

- **Read on demand:** `~/.claude/_rules_lazy_load/org.md` — before adding a connection or variable, for any organisation-specific secrets conventions.

---

## 🏗️ Core Principles

**These four principles define all DAG design decisions:**

1. **Idempotency** — Re-running the same logical date produces identical results
   - **Why:** airflow backfills and retries are common; non-idempotent DAGs accumulate corrupted data
   - **How:** dedupe inputs, upsert rather than insert, make task result independent of prior runs
   - **Test:** verify that running a DAG twice produces same data in warehouse

2. **Atomicity** — One task = one logical operation; no bundling unrelated steps
   - **Why:** failure granularity enables targeted retries without re-running successful work
   - **How:** split long pipelines into focused tasks; use TaskGroups for related work
   - **Test:** can I identify why a failed task failed without inspecting adjacent tasks?

3. **Config-driven** — Never hardcode environment-specific values; put them in each DAG's `config.yaml`
   - **Why:** the same DAG code runs in dev, CI and prod, and hardcoded values block safe transitions
   - **How:** env-specific values (warehouse size, Slack channels, S3 paths) go in `config.yaml`, read through `common.get_default_dag_params()`, and Variables are read only in `includes/` utilities
   - **Test:** can I change the environment by only modifying config, not DAG code?

4. **Fail fast** — Configure retries deliberately; surface errors immediately; don't silently swallow failures
   - **Why:** silent failures corrupt downstream data, and deliberate retries handle transient issues
   - **How:** inherit `retries` and `retry_delay` from `default_args`, never set retries to `0` in production, and use `on_failure_callback`
   - **Test:** do I know why a DAG failed within 10 seconds of checking the Airflow UI?

---

## ⚠️ Common Mistakes & Recovery

| Mistake | Impact | How to fix |
|---------|--------|-----------|
| Hardcoded warehouse size | Wrong cost/performance tradeoff | Move it to the DAG's `config.yaml` |
| No retries on flaky tasks | Overnight DAG failures block analysis | Inherit `retries=3, retry_delay=timedelta(minutes=5)` from `default_args` |
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
   └─ Pre-commit validates DAG syntax and config

5. Production backfill
   └─ Run DAG for past N days; verify results identical across runs

6. Scheduling
   └─ Unpause the DAG (its `schedule` comes from `config.yaml`); monitor first week
```

---

## ✅ DAG Acceptance Checklist

Before marking a DAG as production-ready:

- [ ] All hardcoded env values moved to `config.yaml`
- [ ] Each task is atomic (single logical operation)
- [ ] Idempotency verified (run twice, compare results)
- [ ] Retries configured based on actual failure patterns
- [ ] Error notification enabled (Slack, Teams, or email)
- [ ] SQL follows style guide (SQLFluff passes)
- [ ] Documentation updated in DAG description
