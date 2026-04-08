# 🗂️ DAG Design

Standards for structuring DAG files, naming conventions, and mandatory attributes within the Airflow project.

## 📁 File structure

Each DAG is a **folder**, not a single file. Every DAG folder contains:

| File | Purpose |
|------|---------|
| `dag.py` | Thin orchestration file — DAG definition and task wiring only |
| `config.yaml` | All DAG configuration: schedule, start date, tags, description, data source |
| `README.md` | DAG documentation, auto-rendered as `doc_md` in the Airflow UI |
| `__py_helpers.py` | (Optional) DAG-specific Python helper functions |
| `__sql_queries.py` | (Optional) DAG-specific SQL queries |

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

---

## 🏷️ Naming conventions

The DAG ID is derived automatically from the folder name by `common.get_default_dag_params(__file__)` — there is no `dag_id` string set explicitly in `dag.py`.

| Construct | Convention | Example |
|-----------|------------|---------|
| DAG folder / DAG ID | `snake_case`, descriptive of the pipeline | `parent_dag_salesforce_hourly` |
| Task ID | `snake_case`, verb-first or noun-first describing the action | `task_dbt_debug`, `tg_airbyte_tasks` |
| DAG file | Always `dag.py` within the DAG folder | `dag.py` |
| Config file | Always `config.yaml` within the DAG folder | `config.yaml` |
| Python variables | `snake_case` | `data_src`, `airbyte_job_name` |

- Avoid abbreviations — prefer clarity over brevity.
- Avoid business-specific acronyms that are not meaningful to all readers of the codebase.

### 🔖 DAG folder naming patterns

| Pattern | Use case | Example |
|---------|----------|---------|
| `parent_dag_<data_src>_<frequency>` | Parent DAG orchestrating Airbyte + dbt for a source | `parent_dag_salesforce_hourly` |
| `dbt_tasks_<description>_<frequency>` | Schedule-based dbt DAG | `dbt_tasks_morning_refresh_daily` |
| `template_dag_<technology>` | Reusable DAG template | `template_dag_airbyte`, `template_dag_dbt` |

> **Note:** Frequency (e.g. `_daily`, `_hourly`) is included in the folder name for parent DAGs and schedule-based dbt DAGs in practice, as it distinguishes DAGs that differ only by their schedule. This overrides the older Confluence guidance to omit frequency from DAG names.

---

## ✅ Mandatory DAG attributes

The following must be present in every `config.yaml` — CI checks enforce this:

| Attribute | Reason |
|-----------|--------|
| `description` | Surfaces in the Airflow UI and is used to generate `doc_md` |
| `schedule` | Required for scheduling; must be an explicit cron expression |
| `start_date` | Required for scheduling; must be a fixed historical ISO date |
| `tags` | Required for discoverability and filtering in the Airflow UI |
| `data_src` | Required for task generation via `common` helpers |
