# 🌬️ Airflow Style Guide & Standards

Defines the team's standards for writing and structuring Apache Airflow DAGs and pipelines.

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`dag_design.md`](dag_design.md) | DAG file structure, naming conventions, and mandatory attributes |
| [`dag_configuration.md`](dag_configuration.md) | config.yaml fields, default args, scheduling, tags, and DAG documentation |
| [`tasks_and_operators.md`](tasks_and_operators.md) | Boilerplate, task design, operator selection, helpers, dependencies, TaskGroups, and XComs |
| [`best_practices.md`](best_practices.md) | Idempotency, catchup, retries, error handling, testing, and Variables |
| [`connections_and_variables.md`](connections_and_variables.md) | AKV-backed connections and variables — naming conventions, derivation rules, and provisioning |

## 📋 Contents

- [🏗️ Core principles](#-core-principles)

---

## 🏗️ Core principles

- **Idempotency** — every DAG and task must be safe to re-run; the same execution for the same logical date must produce the same result.
- **Atomicity** — one task, one logical operation; do not bundle unrelated steps into a single task.
- **Config-driven** — never hardcode environment-specific values inside a DAG; use Airflow Variables and Connections, or `config.yaml`-sourced values.
- **Fail fast** — configure retries deliberately; do not silently swallow failures; use `on_failure_callback` to surface errors.
