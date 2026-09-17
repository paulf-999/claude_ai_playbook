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
