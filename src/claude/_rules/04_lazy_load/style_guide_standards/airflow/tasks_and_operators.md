# ⚙️ Tasks, Operators & Dependencies

**Purpose:** Establish standards for DAG boilerplate, task design, operator selection, helper files, and task dependencies to ensure consistent and maintainable DAG structure.

## 📋 Standard dag.py boilerplate

Every `dag.py` starts the same way. All DAG configuration comes from `config.yaml` — nothing is hardcoded:

```python
from airflow import DAG
from dmt_airflow_dags.includes import common  # ruff: isort: skip

# Retrieve default & optional DAG parameters
default_dag_params, optional_dag_params = common.get_default_dag_params(__file__)

# Create the Airflow DAG
with DAG(**default_dag_params) as dag:
    # task definitions here

    # DAG graph
    task_a >> task_b
```

- **`default_dag_params`:** contains `dag_id`, `schedule_interval`, `start_date`, `catchup`, `tags`, `description`, `doc_md`, `default_args`
- **`optional_dag_params`:** contains `dag_inputs` (raw config.yaml), `py_helpers` (from `__py_helpers.py`), and `sql_queries` (from `__sql_queries.py`)
- **DAG graph:** always end the DAG block with a `# DAG graph` comment followed by all task dependency declarations

## 📋 Contents

- [🧩 Task design principles](#-task-design-principles)
- [🔧 Operator selection](#-operator-selection)
- [📂 DAG-specific helpers](#-dag-specific-helpers)
- [🔗 Task dependencies](#-task-dependencies)
- [📦 TaskGroups](#-taskgroups)
- [📤 XComs](#-xcoms)

---

## 🧩 Task design principles

- **One operation per task:** do not bundle unrelated steps into a single task
- **Independently re-runnable:** tasks must be safe to rerun without side effects from previous runs
- **Simplicity:** keep task functions small and single-purpose — extract complex logic into importable modules in `includes/`
- **Descriptive IDs:** task IDs must be unique and describe the action performed
  - **Individual tasks:** prefix with `task_` (e.g., `task_snowflake_query`)
  - **TaskGroups:** prefix with `tg_` (e.g., `tg_airbyte_tasks`)

---

## 🔧 Operator selection

Prefer purpose-built operators over generic ones. Common patterns:

| Use case | Preferred operator | Example |
|----------|-------------------|---------|
| Python logic | `PythonOperator` with callable from `__py_helpers.py` | `task_transform()` |
| Snowflake SQL | `SnowflakeOperator` with SQL from `__sql_queries.py` | `task_load()` |
| dbt runs | `DockerOperator` with `common.get_common_dbt_docker_params()` | `task_dbt_run()` |
| Airbyte sync | `common.generate_common_airbyte_tasks()` | `task_sync_source()` |
| Trigger child DAG | `TriggerDagRunOperator` with `common.get_common_trigger_dagrun_params()` | `task_trigger_child()` |
| Wait for condition | `Sensor` with `mode="reschedule"` | avoid holding worker slots |
| Branching | `BranchPythonOperator` | conditional task routing |

- **Templates:** see `~/.claude/_rules/04_lazy_load/style_guide_standards/airflow/templates/` for Snowflake and TriggerDagRun examples

---

## 📂 DAG-specific helpers

Store Python callables and SQL queries in dedicated files within the DAG folder, not inline in `dag.py`:

| File | Purpose | Access pattern |
|------|---------|-----------------|
| `__py_helpers.py` | DAG-specific Python functions | `optional_dag_params["py_helpers"].<function_name>` |
| `__sql_queries.py` | DAG-specific SQL queries as strings | `optional_dag_params["sql_queries"].<variable_name>` |

Both files are auto-imported by `common.get_default_dag_params()` if they exist in the DAG folder.

---

## 🔗 Task dependencies

- **Use `>>`:** always use the `>>` operator to define dependencies
- **Never use:** `set_upstream()` or `set_downstream()`
- **Group at bottom:** define all dependencies at the bottom of the DAG block under a `# DAG graph` comment, kept separate from task definitions

```python
    # DAG graph
    tg_airbyte_tasks >> tg_dbt_run_staging_base_tasks
```

---

## 📦 TaskGroups

Use `TaskGroup` to visually group related tasks in the Airflow UI. Common patterns (Airbyte, dbt) are wrapped in reusable TaskGroup generators in `includes/airflow_tasks/`.

- **Template:** see `~/.claude/_rules/04_lazy_load/style_guide_standards/airflow/templates/template_dag_parent.py`

---

## 📤 XComs

- **Use sparingly:** XComs are not designed for large data transfers — pass only small values (IDs, counts, status flags)
- **Avoid large data:** do not pass DataFrames or large result sets between tasks
- **Use storage:** write intermediate data to storage (S3, Snowflake stage) and pass only the reference
