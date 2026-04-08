# 📸 dbt Snapshots

Covers how dbt snapshots are used to capture point-in-time history of dimension models, including naming conventions, configuration standards, best practices, and guidance on building downstream models on top of snapshots.

## 🔍 What are dbt snapshots?

Snapshots capture point-in-time history of a dimension model. When a row changes, the snapshot records the old version with a closed effective date and creates a new current version.

- Snapshot definitions live in the `snapshots/` directory.
- Snapshots are executed using the `dbt snapshot` command.

---

## 🏷️ Naming

Snapshots follow the `dim_<entity>_history.sql` naming pattern. Examples from the repo:

- `dim_merchant_history.sql`
- `dim_merchant_all_history.sql`

---

## ⚙️ Configuration

The team uses the **check strategy** — dbt compares a defined list of columns on each run and creates a new snapshot record when any of them change.

<details>
<summary>Click to expand — snapshot example</summary>

```sql
{% snapshot dim_merchant_history %}
    {{
        config(
          target_schema='WAREHOUSE',
          strategy='check',
          unique_key='KEY',
          check_cols=['SOURCE_SYSTEM_ID', 'MID', 'DBA_NAME', ...]
        )
    }}

    SELECT *
    FROM {{ ref('dim_merchant') }}
    {{ limit_rows() }}

{% endsnapshot %}
```

</details>

Key configuration points:

| Setting | Value |
|---------|-------|
| `strategy` | `check` — monitors a defined list of columns for changes |
| `unique_key` | `KEY` — the surrogate key of the source model |
| `target_schema` | `WAREHOUSE` |
| `check_cols` | Explicit list of columns to watch — do not use `'all'` in production |

---

## ✅ Best practices

| Category | Guideline |
|----------|-----------|
| **Source** | Snapshots select from `ref()` on the corresponding `dim_` warehouse model — not directly from `source()` |
| **Transformations** | Avoid transformations inside snapshots — clean data in the upstream dim model |
| **Row limiting** | Always include `{{ limit_rows() }}` to support dev/CI execution |
| **Column list** | Define `check_cols` explicitly — avoids unintended snapshot triggers from irrelevant column changes |
| **Idempotency** | Snapshots must be safe to re-run without duplicating or corrupting history |

---

## 📐 Building models on top of snapshots

When a record-per-day view is needed rather than a record-per-change, use **date spining** — join the snapshot model to a date spine based on `dbt_valid_from` and `dbt_valid_to`. The `dbt_date` package (included in the project) provides date utilities for this.

If date spining produces high row counts, materialise the downstream model as incremental so only new `snapshot_date` records are appended on each run.
