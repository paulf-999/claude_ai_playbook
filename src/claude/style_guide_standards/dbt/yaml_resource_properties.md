# 📄 YAML Resource Properties

Standards for declaring dbt resource properties in YAML — covering file naming, formatting style, source definitions, tests, and sensitive data tagging.

## 🔍 What are dbt resource properties?

Resources in a dbt project (models, snapshots, seeds, sources) can have declared **properties** — descriptions, tests, and source definitions. Properties are declared in `.yml` files co-located with the resources they describe.

---

## 🏷️ YAML file naming

- YAML files must be prefixed with an underscore (`_`) so that they sort to the top of the directory listing.
- Each layer uses a consistent file name pattern:

| Layer | File name convention | Example |
|-------|---------------------|---------|
| Staging — source definitions | `_staging_src.yml` | `staging/<source>/_staging_src.yml` |
| Base — source definitions | `_src_base.yml` | `base/<source>/_src_base.yml` |

---

## 🎨 YAML style guide

- Indent with **2 spaces**.
- Keep lines to a maximum of **120 characters** (matches the project SQLFluff config).
- List items must be indented relative to their parent key.
- Use a blank line to separate list items that are dictionaries.

---

## 🗃️ Source definitions

Source YAML files use **Jinja templating** to select the correct database per environment, and **YAML anchors** to avoid repeating the database name across tables in the same source.

<details>
<summary>Click to expand — source YAML example</summary>

```yaml
sources:
  - name: ACCESS_ONE_SOURCE
    database: &db_name |
        {%- if 'dev' in target.name -%} src_dev
        {%- elif 'uat' in target.name -%} src_uat
        {%- elif 'prod' in target.name -%} src_prd
        {%- endif -%}
    schema: ACCESS_ONE_SOURCE
    tables:
        - name: MERCHANT_LIST
        - name: MERCHANT_PROFILE_OMAHA
        - name: MERCHANT_PROFILE_NORTH
```

</details>

- The `database` field uses a YAML anchor (`&db_name`) so that it can be referenced by other entries in the same file.
- The Jinja block selects the environment-appropriate database based on `target.name`.
- Source names and table names must be `UPPER_CASE`, matching Snowflake object names.

---

## 🧪 Tests

Apply at minimum `unique` and `not_null` tests to the surrogate key (`KEY`) of every model. Declare tests in the resource property YAML co-located with the model.

```yaml
models:
  - name: staging_access_one_merchant_list
    columns:
      - name: KEY
        tests:
          - unique
          - not_null
```

---

## 🔒 Sensitive data

Columns containing PII or data that should not be exposed must be flagged in the YAML using the `meta` key:

```yaml
columns:
  - name: contact_email
    meta:
      sensitive: true
  - name: contact_name
    meta:
      sensitive: true
```
