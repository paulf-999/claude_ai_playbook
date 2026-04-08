# ⚙️ DAG Configuration

Standards for configuring DAGs via `config.yaml`, setting default args, defining schedules, tagging, and writing DAG documentation.

## ⚙️ DAG parameters via config.yaml

All DAG parameters are read from `config.yaml` by `common.get_default_dag_params(__file__)`. Do not hardcode schedule, tags, or description in `dag.py`.

The standard `config.yaml` fields are:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Short description of what the DAG does |
| `schedule` | Yes | Cron expression for the DAG schedule |
| `schedule_comment` | Yes | Human-readable explanation of the schedule |
| `start_date` | Yes | ISO date string, e.g. `'2025-04-09'` |
| `tags` | Yes | List of tags for discoverability |
| `data_src` | Yes | Data source name |
| `airbyte_conn_name` | Conditional | Airbyte connection name(s); required for Airbyte DAGs |

<details>
<summary>Click to expand — example <code>config.yaml</code></summary>

```yaml
---
description: |
  Orchestrates the execution of HOURLY dbt staging & base models for Salesforce.
schedule: 40 7-23 * * *
schedule_comment: Runs hourly at minute 40 from 7 AM to 11:59 PM UTC.
start_date: '2025-04-09'
tags:
  - airbyte
  - dbt
  - hourly
  - parent_dag
  - salesforce
data_src: salesforce
airbyte_conn_name: [salesforce, salesforce_airbyte_job]
```

</details>

---

## 🔧 Default args

Default args are set centrally in `common.get_dag_default_args()` — do not redefine them in individual DAG files.

The team standard `default_args` are:

```python
{
    "owner": "data_management",
    "depends_on_past": False,
    "email_on_failure": False,   # custom callback handles alerts
    "email_on_retry": False,
    "on_failure_callback": email_notifications.email_on_airflow_task_failure,
    "on_success_callback": email_notifications.email_on_airflow_task_success,
}
```

---

## 📅 Scheduling

- Set `schedule` (not `schedule_interval`) in `config.yaml` — never rely on the Airflow default.
- Always add `schedule_comment` with a human-readable description of the cron expression.
- `catchup=False` is enforced centrally by `common.get_default_dag_params()` — do not set it on individual DAGs.

---

## 🔖 Tags

Tags are defined in `config.yaml` as a list. Tag by source system, load type, technology, frequency, and DAG type so that DAGs are filterable in the Airflow UI:

```yaml
tags:
  - airbyte
  - dbt
  - hourly
  - parent_dag
  - salesforce
```

---

## 📝 DAG documentation

Each DAG folder contains a `README.md` which is automatically read and rendered as `doc_md` in the Airflow UI by `common.get_default_dag_params()`. Do not write `doc_md` as a Python string in `dag.py`.

<details>
<summary>Click to expand — README.md template</summary>

```markdown
# parent_dag_salesforce_hourly

## Overview

Orchestrates the hourly execution of Airbyte ingestion from Salesforce, followed by dbt staging and base model runs.

## Schedule

Runs hourly at minute 40 from 7 AM to 11:59 PM UTC (`40 7-23 * * *`).

## Dependencies

- Airbyte connection: `salesforce`
- dbt models: `models/staging/salesforce/`, `models/base/salesforce/`

## Notes

- Airbyte step is currently skipped — Airbyte AWS server not yet reachable from Airflow PROD.
```

</details>
