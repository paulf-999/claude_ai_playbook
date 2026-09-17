# 📄 YAML Resource Properties

Standards for declaring dbt resource properties in YAML — covering file naming, formatting style, source definitions, tests, and sensitive data tagging.

## 🏷️ YAML file naming

- YAML files must be prefixed with an underscore (`_`) so that they sort to the top of the directory listing.
- Each layer uses a consistent file name pattern:

| Layer | File name convention | Example |
|-------|---------------------|---------|
| Staging — source definitions | `_staging_src.yml` | `staging/<source>/_staging_src.yml` |
| Base — source definitions | `_src_base.yml` | `base/<source>/_src_base.yml` |

## 📋 Contents

- [🎨 YAML style guide](#-yaml-style-guide)
- [🧪 Tests](#-tests)
- [🗃️ Source definitions](#-source-definitions)
- [🔒 Sensitive data](#-sensitive-data)

---

## 🎨 YAML style guide

- Indent with **2 spaces**.
- Keep lines to a maximum of **120 characters** (matches the project SQLFluff config).
- List items must be indented relative to their parent key.
- Use a blank line to separate list items that are dictionaries.

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

## 🗃️ Source definitions

Source YAML files use Jinja templating to select the correct database per environment, and YAML anchors to avoid repeating the database name across tables in the same source. See the working example:
`~/.claude/_rules/lazy_load/style_guide_standards/dbt/templates/template_source.yml`

- The `database` field uses a YAML anchor (`&db_name`) so that it can be referenced by other entries in the same file.
- The Jinja block selects the environment-appropriate database based on `target.name`.
- Source names and table names must be `UPPER_CASE`, matching Snowflake object names.

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
