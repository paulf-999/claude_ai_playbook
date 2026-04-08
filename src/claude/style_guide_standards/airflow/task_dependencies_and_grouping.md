# 🔗 Task Dependencies & Grouping

Standards for DAG-specific helper files, task dependency declarations, TaskGroup usage, and XCom conventions.

## 📂 DAG-specific helpers

When a DAG requires Python callables or SQL queries, store them in dedicated files within the DAG folder rather than inline in `dag.py`:

| File | Purpose | Accessed via |
|------|---------|--------------|
| `__py_helpers.py` | DAG-specific Python functions | `optional_dag_params["py_helpers"].<function_name>` |
| `__sql_queries.py` | DAG-specific SQL queries as string variables | `optional_dag_params["sql_queries"].<variable_name>` |

Both files are auto-imported by `common.get_default_dag_params()` if they exist in the DAG folder.

---

## 🔗 Task dependencies

- Use the `>>` operator to define dependencies — do not use `set_upstream` or `set_downstream`.
- Define all dependencies at the bottom of the DAG block under a `# DAG graph` comment, kept separate from task definitions.

<details>
<summary>Click to expand — dependency definition example</summary>

```python
    # DAG graph
    tg_airbyte_tasks >> tg_dbt_run_staging_base_tasks
```

</details>

---

## 📦 TaskGroups

Use `TaskGroup` to visually group related tasks in the Airflow UI. Common task generation patterns (Airbyte, dbt) are wrapped in reusable TaskGroup generators in `includes/airflow_tasks/`.

<details>
<summary>Click to expand — parent DAG TaskGroup example</summary>

```python
from airflow.utils.task_group import TaskGroup
from dmt_airflow_dags.includes import common  # ruff: isort: skip

default_dag_params, optional_dag_params = common.get_default_dag_params(__file__)
data_src = optional_dag_params["dag_inputs"]["data_src"]
airbyte_conn_name_list = optional_dag_params["dag_inputs"]["airbyte_conn_name"]

with DAG(**default_dag_params) as dag:
    with TaskGroup(f"airbyte_tasks_{data_src}") as tg_airbyte_tasks:
        for data_src, airbyte_job_name in airbyte_conn_name_list:
            tg_airbyte_tasks_per_job = common.generate_common_airbyte_tasks(data_src, airbyte_job_name)

    tg_dbt_run_staging_base_tasks = common.generate_common_dbt_run_staging_base_tasks(data_src)

    # DAG graph
    tg_airbyte_tasks >> tg_dbt_run_staging_base_tasks
```

</details>

---

## 📤 XComs

- Use XComs sparingly — they are not designed for large data transfers, so pass only small values such as IDs, counts, or status flags.
- Do not use XComs to pass DataFrames or large result sets between tasks; instead, write intermediate data to storage (S3, Snowflake stage) and pass only the reference.
