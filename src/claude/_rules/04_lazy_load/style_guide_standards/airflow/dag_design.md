# 🗂️ DAG Design

**Purpose:** Establish folder structure, naming conventions, and mandatory attributes for Airflow DAG files and configuration.

## 📁 File structure

Each DAG is a **folder**, not a single file. Every DAG folder must contain:

- **`dag.py`:** thin orchestration file — DAG definition and task wiring only
- **`config.yaml`:** all DAG configuration (schedule, start date, tags, description, data source)
- **`README.md`:** DAG documentation, auto-rendered as `doc_md` in the Airflow UI
- **`__py_helpers.py`:** (optional) DAG-specific Python helper functions
- **`__sql_queries.py`:** (optional) DAG-specific SQL queries

DAGs are organized under `dags/topics/<topic>/` subdirectories, not placed directly in `dags/`. Shared utilities and reusable task generators live in `includes/` — not `plugins/`.

```
dags/
  topics/
    parent_dags/
      parent_dag_salesforce_hourly/
        dag.py
        config.yaml
        README.md
    dbt_dags/
      _02_schedule_based_dags/
        dbt_tasks_morning_refresh_daily/
          dag.py
          config.yaml
          README.md
includes/
  common.py
  scripts/
  airflow_tasks/
  classes/
```

- **Shared files:** files in `includes/` are shared across all DAGs — do not modify without team review
- **DAG-specific logic:** belongs in `__py_helpers.py` or `__sql_queries.py` in the DAG folder

## 📋 Contents

- [🏷️ Naming conventions](#-naming-conventions)
- [✅ Mandatory DAG attributes](#-mandatory-dag-attributes)

---

## 🏷️ Naming conventions

DAG ID is derived automatically from the folder name by `common.get_default_dag_params(__file__)` — never set `dag_id` explicitly in `dag.py`.

| Construct | Convention | Example |
|-----------|------------|---------|
| DAG folder / ID | `snake_case`, descriptive of the pipeline | `parent_dag_salesforce_hourly` |
| Task ID | `snake_case`, verb-first or noun-first | `task_dbt_debug`, `tg_airbyte_tasks` |
| DAG file | Always `dag.py` within the DAG folder | `dag.py` |
| Config file | Always `config.yaml` within the DAG folder | `config.yaml` |
| Python variables | `snake_case` | `data_src`, `airbyte_job_name` |

- **Clarity over brevity:** avoid abbreviations
- **Avoid acronyms:** only use business acronyms that are meaningful to all readers

### Folder naming patterns

| Pattern | Use for | Example |
|---------|---------|---------|
| `parent_dag_<data_src>_<frequency>` | Parent DAG orchestrating Airbyte + dbt | `parent_dag_salesforce_hourly` |
| `dbt_tasks_<description>_<frequency>` | Schedule-based dbt DAG | `dbt_tasks_morning_refresh_daily` |
| `template_dag_<technology>` | Reusable DAG template | `template_dag_airbyte`, `template_dag_dbt` |

- **Include frequency:** frequency (e.g., `_daily`, `_hourly`) distinguishes DAGs that differ only by schedule
- **Note:** this overrides older Confluence guidance that omitted frequency from DAG names

---

## ✅ Mandatory DAG attributes

The following must be present in every `config.yaml` (CI checks enforce this):

| Attribute | Reason |
|-----------|--------|
| `description` | Surfaces in the Airflow UI and is used to generate `doc_md` |
| `schedule` | Required for scheduling; must be an explicit cron expression |
| `start_date` | Required for scheduling; must be a fixed historical ISO date |
| `tags` | Required for discoverability and filtering in the Airflow UI |
| `data_src` | Required for task generation via `common` helpers |
