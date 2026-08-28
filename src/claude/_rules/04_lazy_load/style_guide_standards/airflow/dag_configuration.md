# ⚙️ DAG Configuration

**Purpose:** Establish standards for configuring DAGs via `config.yaml`, defining schedules, tagging, and writing DAG documentation.

## ⚙️ config.yaml parameters

All DAG parameters are read from `config.yaml` by `common.get_default_dag_params(__file__)`. Do not hardcode schedule, tags, or description in `dag.py`.

| Field | Required | Purpose |
|-------|----------|---------|
| `description` | Yes | Short description of what the DAG does |
| `schedule` | Yes | Cron expression for the DAG schedule |
| `schedule_comment` | Yes | Human-readable explanation of the cron expression |
| `start_date` | Yes | ISO date string, e.g., `'2025-04-09'` |
| `tags` | Yes | List of tags for discoverability |
| `data_src` | Yes | Data source name |
| `airbyte_conn_name` | Conditional | Airbyte connection name(s); required for Airbyte DAGs |

- **Template:** see `~/.claude/_rules/04_lazy_load/style_guide_standards/airflow/templates/template_config.yaml` for working example

## 📋 Contents

- [📅 Scheduling](#-scheduling)
- [🔖 Tags](#-tags)
- [📝 DAG documentation](#-dag-documentation)
- [🔧 Default args](#-default-args)

---

## 📅 Scheduling

- **Use `schedule` field:** set in `config.yaml`, never rely on the Airflow default
- **Never use `schedule_interval`:** it is deprecated
- **Add `schedule_comment`:** always include a human-readable explanation of the cron expression
- **Central `catchup` control:** `catchup=False` is enforced by `common.get_default_dag_params()` — do not override on individual DAGs

---

## 🔖 Tags

Tags are defined in `config.yaml` as a list. Tag by source system, load type, technology, frequency, and DAG type for Airflow UI filterability:

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

- **Template:** see `~/.claude/_rules/04_lazy_load/style_guide_standards/airflow/templates/template_dag_readme.md`

---

## 🔧 Default args

Default args are set centrally in `common.get_dag_default_args()`. Do not redefine them in individual DAG files.

The team standard `default_args`:

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
