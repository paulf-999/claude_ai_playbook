# 🏷️ dbt Naming Conventions

Naming standards for models, files, keys, data types, audit fields, CTEs, and null handling across all layers of the dbt project.

## 🔠 General conventions

- Use `snake_case` for file names and Python/Jinja identifiers.
- Source column references must use the original casing from the source system (often quoted upper-case, e.g. `"MerchantNumber"`).
- Transformed and derived columns use `lowercase_snake_case`.
- Use names based on business terminology, not source system terminology.
- Avoid reserved words as column names.
- Be consistent — use the same field names across models wherever possible.

---

## 📂 Model layer naming

| Layer | File naming convention | Example |
|-------|------------------------|---------|
| Staging | `staging_<source>_<entity>.sql` | `staging_access_one_merchant_list.sql` |
| Base | `<source>_<entity>.sql` | `access_one_merchant_list.sql` |
| Mart | `mart_<domain>_<entity>.sql` | `mart_payroc_commerce_payouts.sql` |
| Publication | `pub_<domain>_<entity>.sql` | `pub_payroc_commerce_payouts.sql` |
| Snapshots | `dim_<entity>_history.sql` | `dim_merchant_history.sql` |
| Macros | File name must match the macro name | `create_surrogate_key.sql` |

---

## 🔑 Surrogate keys

Every model must have a surrogate key named `KEY`, generated using the `create_surrogate_key` macro (a wrapper around `dbt_utils.generate_surrogate_key`):

```sql
{{ create_surrogate_key(['FIELD1', 'FIELD2']) }} AS "KEY"
```

- `KEY` must always be the first column in the SELECT list.
- The input fields must uniquely identify the row.
- Use `unknown_key()` to return a sentinel value for unknown or missing key references.

---

## 📅 Data type naming

| Type | Convention | Example |
|------|------------|---------|
| **Timestamps** | `<event>_at`, stored in UTC | `created_at` |
| **Dates** | `<event>_date` or `<event>_KEY` for date dimension joins | `snapshot_date`, `SNAPSHOT_DATE_KEY` |
| **Booleans** | Prefixed with `is_` or `has_` | `is_active`, `has_admin_access` |
| **Amounts** | Decimal — use `clean_and_cast_numeric()` macro for cleaning currency values from source | `gross_volume` |

---

## 🔍 Audit (DA_*) fields

Staging models must include the following audit fields. These are added via the `dbt_last_modified_field()` macro and related audit macros.

| Field | Description |
|-------|-------------|
| `DA_FILE_YEARMONTH` | Year-month of the source file |
| `DA_PROCESS_ID` | ID of the process that loaded the record |
| `DA_FILE_NAME` | Name of the source file |
| `DA_FILE_ROW_NUMBER` | Row number within the source file |
| `DA_UNIQUE_KEY` | Unique key from the source system |
| `DA_FILE_LAST_MODIFIED` | Last modified timestamp of the source file |
| `DA_START_SCAN_TIME` | Timestamp when the scan/load started |

---

## 🏷️ CTE naming

CTEs within models should be named descriptively in `UPPER_SNAKE_CASE` to reflect their purpose:

| CTE name | Use |
|----------|-----|
| `REMOVE_DUPLICATES` | Deduplication step |
| `GET_MAX` | Retrieving the latest record per key |
| `FINAL` | The last CTE before the final SELECT — always named `FINAL` |

The final SELECT always reads from `FINAL`:

```sql
SELECT *
FROM FINAL
{{ limit_rows() }}
```

---

## 🚫 Null handling

| Column type | NULL / NOT NULL |
|-------------|-----------------|
| Surrogate key (`KEY`) | `NOT NULL` |
| Foreign keys | `NOT NULL` — use `unknown_key()` sentinel for unknown references |
| Audit / DA_* fields | `NOT NULL` |
| Measures | Nullable where source data may be absent |
| All other fields | As applicable |
