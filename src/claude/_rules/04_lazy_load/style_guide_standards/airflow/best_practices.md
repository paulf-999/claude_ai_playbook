# ✅ Best Practices

**Purpose:** Establish practices for idempotency, retries, error handling, testing, and configuration to ensure reliable and maintainable Airflow pipelines.

## 🔄 Idempotency

Every DAG run for a given `execution_date` must produce the same result regardless of re-runs. Design tasks to be safe to retry:

- **SQL writes:** use `INSERT OVERWRITE` or `MERGE` rather than bare `INSERT`
- **Data replacement:** delete and recreate target data for the execution window before writing — never append blindly
- **State assumptions:** do not assume previous run state exists or is accurate

## 📋 Contents

- [📅 Catchup and backfilling](#-catchup-and-backfilling)
- [🔁 Retries and backoff](#-retries-and-backoff)
- [🚨 Error handling](#-error-handling)
- [🧪 Testing](#-testing)
- [🔐 Variables and Connections](#-variables-and-connections)
- [📖 Astronomer anti-patterns](#-astronomer-anti-patterns)

---

## 📅 Catchup and backfilling

- **Central control:** `catchup=False` is enforced in `common.get_default_dag_params()` — do not set in individual DAG files
- **Intentional backfill:** use the Airflow CLI command: `airflow dags backfill -s <start> -e <end> <dag_id>`

---

## 🔁 Retries and backoff

- **Set in defaults:** configure `retries` and `retry_delay` in `default_args` so all tasks inherit consistent behaviour
- **Assume failures:** do not set retries to `0` for production DAGs — network timeouts and API rate limits are common
- **Exponential backoff:** use for tasks that call external APIs:

```python
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

- **Use callbacks:** use `on_failure_callback` to notify on task failure — do not rely solely on email alerts
- **Share callbacks:** keep callback functions in a shared module (`plugins/callbacks.py`) rather than inlining in DAG files

```python
def notify_on_failure(context: dict) -> None:
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["execution_date"]
    # send alert (Slack, PagerDuty, etc.)

default_args = {
    "on_failure_callback": notify_on_failure,
}
```

---

## 🧪 Testing

- **Load test:** `python dags/my_dag.py` must exit cleanly
- **Unit tests:** use `pytest` with Airflow test utilities for task callables
- **Integrity validation:** both `airflow dags list` and `airflow dags test <dag_id> <execution_date>` must pass in CI
- **Avoid `depends_on_past=True`:** without explicit justification — it makes testing and backfilling significantly harder

---

## 🔐 Variables and Connections

- **Never hardcode:** environment-specific values (URLs, credentials, schema names) must not be in DAG files
- **Use `config.yaml`:** DAG inputs (data source, Airbyte connection names, schedule) are passed via `config.yaml` and accessed through `common.get_default_dag_params()`
- **Don't read Variables in dag.py:** do not directly access Airflow Variables in `dag.py`
- **Connections:** use Airflow Connections for external system credentials (databases, APIs, cloud); reference IDs in utility functions in `includes/`, not hardcoded
- **Variables:** use for runtime configuration values not DAG-specific (e.g., `AIRFLOW_ENVIRONMENT_LEVEL`); access via `Variable.get("my_var")` in `includes/` utilities only
- **Secrets backend:** store sensitive values in the configured secrets backend, not plaintext in Airflow metadata

---

## 📖 Astronomer anti-patterns

Additional parse-time and runtime pitfalls to avoid (from [Astronomer best practices](https://docs.astronomer.io/learn/dag-best-practices)):

- **Heavy parse-time computation:** keep DAG files as configuration only — do not perform computation at import time
- **Top-level DB/API calls:** avoid them in DAG files — they run on every scheduler heartbeat
- **Metadata DB overload:** use connection and variable caching to reduce load on the metadata database
