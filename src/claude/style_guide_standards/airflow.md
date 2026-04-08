# 🌬️ Airflow Style Guide & Standards

Defines the team's standards for writing and structuring Apache Airflow DAGs and pipelines.

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`airflow/dag_design.md`](airflow/dag_design.md) | DAG file structure, naming conventions, and mandatory attributes |
| [`airflow/dag_configuration.md`](airflow/dag_configuration.md) | config.yaml fields, default args, scheduling, tags, and DAG documentation |
| [`airflow/tasks_and_operators.md`](airflow/tasks_and_operators.md) | Task design, operator selection, and DAG boilerplate |
| [`airflow/task_dependencies_and_grouping.md`](airflow/task_dependencies_and_grouping.md) | Helper files, task dependencies, TaskGroups, and XComs |
| [`airflow/best_practices.md`](airflow/best_practices.md) | Idempotency, catchup, retries, error handling, Variables, and testing |

---

## 🏗️ Core principles

- **Idempotency** — every DAG and task must be safe to re-run. The same execution for the same logical date must produce the same result. See also `rules/development.md`.
- **Atomicity** — one task, one logical operation. Do not bundle unrelated steps into a single task.
- **Config-driven** — never hardcode environment-specific values inside a DAG. Use Airflow Variables and Connections, or `.env`-sourced environment variables.
- **Fail fast** — configure retries deliberately; do not silently swallow failures. Use `on_failure_callback` to surface errors.

---

## 📥 Imports

@./airflow/dag_design.md
@./airflow/dag_configuration.md
@./airflow/tasks_and_operators.md
@./airflow/task_dependencies_and_grouping.md
@./airflow/best_practices.md
