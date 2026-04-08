# ✅ Best Practices

Guidance on idempotency, catchup, retries, error handling, Variables, Connections, and testing to ensure reliable and maintainable Airflow pipelines.

## 🔄 Idempotency

Every DAG run for a given `execution_date` must produce the same result regardless of how many times it is re-run. Design tasks to be safe to retry:

- Use `INSERT OVERWRITE` or `MERGE` rather than a bare `INSERT` in SQL tasks.
- Delete and recreate target data for the execution window before writing — never append blindly.
- Do not assume that state from a previous run exists or is accurate.

---

## 📅 Catchup and backfilling

- `catchup=False` is enforced centrally in `common.get_default_dag_params()` — do not set it in individual DAG files.
- To backfill intentionally, use the Airflow CLI command: `airflow dags backfill -s <start> -e <end> <dag_id>`.

---

## 🔁 Retries and retry delay

- Set `retries` and `retry_delay` in `default_args` so that all tasks inherit consistent retry behaviour.
- Do not set retries to `0` for production DAGs — transient failures such as network timeouts and API rate limits are common.
- Use exponential backoff for tasks that call external APIs:

```python
from airflow.models import DAG
from datetime import timedelta

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=60),
}
```

---

## 🚨 Error handling

- Use `on_failure_callback` to notify on task failure — do not rely solely on email alerts.
- Keep callback functions in a shared module (`plugins/callbacks.py`) rather than inlining them in a DAG file.

<details>
<summary>Click to expand — on_failure_callback example</summary>

```python
def notify_on_failure(context: dict) -> None:
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["execution_date"]
    # send alert (Slack, PagerDuty, etc.)

default_args = {
    "on_failure_callback": notify_on_failure,
    ...
}
```

</details>

---

## 🔐 Variables and Connections

- Never hardcode environment-specific values (URLs, credentials, schema names) inside a DAG file.
- DAG-level inputs (data source name, Airbyte connection names, schedule) are passed via `config.yaml` and accessed through `common.get_default_dag_params()` — do not read them directly from Airflow Variables in `dag.py`.
- Use **Airflow Connections** for external system credentials (databases, APIs, cloud services); connection IDs are referenced in utility functions in `includes/`, not hardcoded in DAG files.
- Use **Airflow Variables** for runtime configuration values that are not DAG-specific (e.g. `AIRFLOW_ENVIRONMENT_LEVEL`); access them via `Variable.get("my_var")` in `includes/` utilities only.
- Store sensitive variable values as secrets — use the configured secrets backend rather than storing them as plaintext in the Airflow metadata database.

---

## 🧪 Testing

- Test that DAG files load without errors: `python dags/my_dag.py` must exit cleanly.
- Use `pytest` with the Airflow test utilities to unit test task callables.
- Validate DAG integrity in CI — both `airflow dags list` and `airflow dags test <dag_id> <execution_date>` must pass.
- Do not use `depends_on_past=True` without a clear, documented reason — it makes testing and backfilling significantly harder.

---

## 📖 Astronomer best practices

Follow the [Astronomer DAG best practices guide](https://docs.astronomer.io/learn/dag-best-practices) as the baseline reference. Key points it covers that complement this guide:

- Keep DAG files as configuration only — do not perform heavy computation at parse time.
- Avoid top-level database or API calls in DAG files, as they run on every scheduler heartbeat.
- Use connection and variable caching to reduce load on the metadata database.
