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
