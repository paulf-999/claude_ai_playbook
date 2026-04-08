# 🗂️ dbt Model Organisation

Defines the four-layer model architecture, folder structure, and the minimum requirements that every dbt model in the project must satisfy.

## 🏛️ Model layers

The project uses a four-layer architecture. Each layer has a distinct responsibility and source of truth:

| Layer | Purpose | Selects from | Materialisation |
|-------|---------|-------------|-----------------|
| **Staging** | Cleans and standardises raw source data. One model per source entity. Light transformations only — rename, recast, deduplicate. | `source()` | Incremental |
| **Base** | Thin interface layer between staging and marts. Applies final column selection and aliasing before business logic. | `ref(staging_*)` | View or table |
| **Mart** | Business logic and transformation. Domain-organised. Combines base models into business-facing datasets. | `ref(base_*)` or `ref(mart_*)` | Table |
| **Publication** | Exposed layer for downstream consumers and reporting. Minimal transformation — selects from mart. | `ref(mart_*)` | Table or view |

Additional directories exist for specific purposes:

| Directory | Purpose |
|-----------|---------|
| `warehouse/` | Dimensional and fact table models (e.g. `dim_merchant`) |
| `intermediate/` | Intermediate transformation models where needed between layers |
| `operations/` | Operational and admin models |
| `dq_framework/` | Data quality framework models |

---

## 📁 Folder structure

```
prod_analytics/
└── models/
    ├── staging/
    │   └── <source_system>/
    │       ├── _staging_src.yml         # source definitions
    │       └── staging_<source>_<entity>.sql
    ├── base/
    │   └── <source_system>/
    │       ├── _src_base.yml
    │       └── <source>_<entity>.sql
    ├── mart/
    │   └── <domain>/
    │       └── mart_<domain>_<entity>.sql
    ├── publication/
    │   └── <domain>/
    │       └── pub_<domain>_<entity>.sql
    ├── warehouse/
    ├── intermediate/
    ├── operations/
    └── dq_framework/
```

Source systems each have a corresponding folder under both `staging/` and `base/`. Marts and publications are organised by **business domain**, not by source system.

---

## ✅ Minimum requirements for dbt models

| Requirement | Detail |
|-------------|--------|
| **Surrogate key** | Every model must have a surrogate key named `KEY`, generated using `{{ create_surrogate_key(['field1', 'field2']) }}`. |
| **dbt tests** | At minimum, apply `unique` and `not_null` tests to `KEY` on every model. |
| **Source selection** | Only `staging` models select from `source()`. All downstream models use `ref()`. |
| **CTEs over subqueries** | Use CTEs — never subqueries. See [`../sql/cte_style_guide.md`](../sql/cte_style_guide.md). |
| **Row limiting** | Always append `{{ limit_rows() }}` to the final SELECT and to major intermediate CTEs. This is a no-op in production and limits rows in dev/CI targets. |
| **Audit fields** | Staging models must include audit fields via `{{ dbt_last_modified_field() }}` or the relevant audit macro. |
