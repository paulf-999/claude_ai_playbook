# ⚙️ Tasks & Operators

Standards for task design, operator selection, and DAG boilerplate within the Airflow project.

## 🧩 Task design principles

- One task must map to one logical operation — do not bundle unrelated steps into a single task.
- Tasks must be independently re-runnable without side effects from previous runs.
- Keep task functions small and single-purpose — extract complex logic into importable modules in `includes/` rather than defining business logic inline in `dag.py`.
- Task IDs must be unique within a DAG and descriptive of the action performed.

### 🏷️ Task naming

| Construct | Prefix | Example |
|-----------|--------|---------|
| Individual task | `task_` | `task_snowflake_query`, `task_hello_world` |
| TaskGroup | `tg_` | `tg_airbyte_tasks`, `tg_dbt_run_staging` |

---

## 📋 Standard dag.py boilerplate

Every `dag.py` starts with the same two lines after imports. All DAG configuration comes from `config.yaml` — nothing is hardcoded in the Python file.

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

- `default_dag_params` contains: `dag_id`, `schedule_interval`, `start_date`, `catchup`, `tags`, `description`, `doc_md`, `default_args`.
- `optional_dag_params` contains: `dag_inputs` (raw config.yaml values), `py_helpers` (from `__py_helpers.py`), and `sql_queries` (from `__sql_queries.py`).
- Always end the DAG block with a `# DAG graph` comment followed by all task dependency declarations.

---

## 🔧 Operator selection

Prefer purpose-built operators over generic ones where they exist:

| Use case | Preferred operator |
|----------|--------------------|
| Python logic | `PythonOperator` with callable from `__py_helpers.py` |
| Snowflake SQL | `SnowflakeOperator` with SQL from `__sql_queries.py` |
| dbt runs | `DockerOperator` with `common.get_common_dbt_docker_params()` |
| Airbyte sync | `common.generate_common_airbyte_tasks(data_src, airbyte_job_name)` |
| Trigger child DAG | `TriggerDagRunOperator` with `common.get_common_trigger_dagrun_params()` |
| Waiting for a condition | `Sensor` (set `mode="reschedule"` to avoid holding a worker slot) |
| Branching | `BranchPythonOperator` |

<details>
<summary>Click to expand — Snowflake template example</summary>

```python
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from dmt_airflow_dags.includes import common  # ruff: isort: skip

default_dag_params, optional_dag_params = common.get_default_dag_params(__file__)

SNOWFLAKE_CONN_ID = "snowflake_prod_key_pair_auth"
sql_queries = optional_dag_params["sql_queries"]

with DAG(**default_dag_params) as dag:
    task_run_query = SnowflakeOperator(
        task_id="snowflake_query_eg_show_dbs",
        sql=sql_queries.sql_query,
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
    )

    # DAG graph
    task_run_query
```

</details>

<details>
<summary>Click to expand — TriggerDagRunOperator example</summary>

```python
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from dmt_airflow_dags.includes import common  # ruff: isort: skip

default_dag_params, optional_dag_params = common.get_default_dag_params(__file__)
common_trigger_dagrun_params = common.get_common_trigger_dagrun_params()
data_src = optional_dag_params["dag_inputs"]["data_src"]

with DAG(**default_dag_params) as dag:
    task_trigger_child_dag = TriggerDagRunOperator(
        task_id="trigger_child_dag",
        trigger_dag_id="target_dag_name",
        **common_trigger_dagrun_params,
    )

    # DAG graph
    task_trigger_child_dag
```

</details>
