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
