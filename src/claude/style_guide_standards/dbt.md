# 🔵 dbt Style Guide & Standards

This guide defines standards for the `da-etl-dbtanalytics` project — covering model organisation, naming, YAML properties, snapshots, and macros — grounded in the actual repo structure and aligned with the [dbt Labs style guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md) where applicable.

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`dbt/model_organisation.md`](dbt/model_organisation.md) | Model layers, folder structure, and minimum model requirements |
| [`dbt/naming_conventions.md`](dbt/naming_conventions.md) | Naming conventions for models, keys, data types, marts, audit fields, and null handling |
| [`dbt/yaml_resource_properties.md`](dbt/yaml_resource_properties.md) | YAML naming conventions and style guide for resource properties |
| [`dbt/snapshots.md`](dbt/snapshots.md) | Snapshot background, best practices, and examples |
| [`dbt/macros.md`](dbt/macros.md) | Team custom macros, dbt packages, and macro directory structure |

For SQL formatting rules that apply within dbt models, see [`sql.md`](sql.md).

---

## 📥 Imports

@./dbt/model_organisation.md
@./dbt/naming_conventions.md
@./dbt/yaml_resource_properties.md
@./dbt/snapshots.md
@./dbt/macros.md
