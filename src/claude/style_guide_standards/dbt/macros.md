# ⚙️ dbt Macros

Documents the team's custom macros, third-party packages, and the macro directory structure — so engineers know what is available before writing equivalent logic from scratch.

## 📏 Standards

- The macro file name must match the macro name exactly (e.g. `create_surrogate_key.sql` for the `create_surrogate_key` macro).
- Macros are organised into subdirectories by category under `prod_analytics/macros/`.
- All macros must be documented in a `macros.yml` file.

---

## 🛠️ Team custom macros

The following macros are defined in the project and should be used in preference to writing equivalent logic inline.

### 🔨 Data processing

| Macro | Description |
|-------|-------------|
| `create_surrogate_key(field_list)` | Generates a surrogate key from a list of fields. Wrapper around `dbt_utils.generate_surrogate_key()` — use this instead of calling dbt_utils directly. |
| `clean_and_cast_numeric(field_expr, precision, scale, default_value)` | Cleans currency strings (strips symbols, handles parentheses as negatives) and casts to the specified precision/scale. Use for any numeric field sourced from text. |
| `clean_string_for_join(field_expr)` | Normalises a string expression for safe use in join conditions (trims whitespace, uppercases). |
| `unknown_key()` | Returns the sentinel value for unknown/missing surrogate key references. Use in place of `-1` or `NULL` for foreign key defaults. |

### 🌍 Environment and control

| Macro | Description |
|-------|-------------|
| `limit_rows()` | Returns `LIMIT {{ var('limit_rows') }}` on `dev` and `cicd` targets; returns nothing in `prod`. Always append to the final SELECT and to major intermediate CTEs. |
| `dbt_last_modified_field()` | Appends the standard `DA_FILE_LAST_MODIFIED` audit timestamp column. Include in every staging model. |

<details>
<summary>Click to expand — macro usage examples</summary>

```sql
-- Surrogate key
{{ create_surrogate_key(['MERCHANT_ID', 'SOURCE_SYSTEM']) }} AS "KEY"

-- Numeric cleaning
{{ clean_and_cast_numeric('M."Gross Volume"', precision=38, scale=4, default_value=0) }} AS gross_volume

-- Row limiting (append to every major CTE and final SELECT)
SELECT *
FROM FINAL
{{ limit_rows() }}
```

</details>

---

## 📦 dbt packages

The project uses the following packages (defined in `packages.yml`):

| Package | Version | Purpose |
|---------|---------|---------|
| `dbt-labs/dbt_utils` | 1.3.3 | General utility macros (surrogate keys, date spine, etc.) |
| `dbt-labs/dbt_date` | via `godatadriven/dbt_date` 0.14.2 | Date dimension and date utility macros |
| `dbt-labs/audit_helper` | 0.12.2 | Helpers for comparing model outputs during refactoring |
| `brooklyn-data/dbt_artifacts` | 2.9.3 | Captures dbt run metadata to Snowflake for observability |
| `get-select/dbt_snowflake_monitoring` | 5.5.1 | Snowflake query cost and performance monitoring |
| `dbt-labs/dbt_external_tables` | 0.12.0 | Manages Snowflake external table definitions |
| `dbt-labs/dbt_project_evaluator` | 1.0.2 | Enforces dbt project structure best practices |

---

## 📁 Macro directory structure

Macros are organised into subdirectories under `prod_analytics/macros/`:

```
macros/
├── audit_field_macros/         # DA_* audit field generation
├── data_processing_macros/     # Numeric cleaning, surrogate key, string normalisation
├── environment_macros/         # limit_rows(), environment-conditional logic
└── helper_macros/
    ├── dbt_test_helper_macros/
    ├── jinja_function_wrapper_macros/
    └── validation_macros/
```
