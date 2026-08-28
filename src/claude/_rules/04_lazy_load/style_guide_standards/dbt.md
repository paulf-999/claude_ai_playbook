# 🔵 dbt Style Guide & Standards

**Purpose:** Define standards for `da-etl-dbtanalytics` — covering model organization, naming, YAML properties, testing, snapshots, and macros. Standards ensure consistency, maintainability, and correctness across the dbt project.

**Scope:** All models, macros, and YAML in `da-etl-dbtanalytics/`. Standards are checked in CI and enforce best practices from [dbt Labs style guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md).

## 📋 Child pages

| File | Purpose | When to load |
|------|---------|-------------|
| [`dbt/model_organisation.md`](dbt/model_organisation.md) | Model layers (staging → base → intermediate → mart), folder structure, minimum requirements | Creating a new model or directory |
| [`dbt/naming_conventions.md`](dbt/naming_conventions.md) | Naming for models (prefixes), keys, marts, audit fields, null handling | Choosing names for models/columns |
| [`dbt/yaml_resource_properties.md`](dbt/yaml_resource_properties.md) | YAML structure, property names, style conventions | Writing `.yml` files |
| [`dbt/snapshots.md`](dbt/snapshots.md) | Snapshot use cases, configuration, best practices, examples | Working with slowly-changing dimensions |
| [`dbt/macros.md`](dbt/macros.md) | Custom macros directory, dbt packages, conventions | Building shared/reusable logic |

For SQL formatting rules within dbt models, see [`sql.md`](sql.md).

---

## 🎯 Core Principles

**dbt excellence rests on these four pillars:**

1. **Lineage clarity** — use `ref()` and `source()` everywhere; never hardcoded table references
   - Why: Enables `dbt lineage` visualization, allows safe refactoring
   - How: Every table reference is `{{ ref('model') }}` or `{{ source('raw', 'table') }}`
   - Test: Does `dbt lineage` show the correct upstream and downstream dependencies?

2. **Documentation completeness** — every model and column has a description
   - Why: Undocumented models create confusion; descriptions are the source-of-truth for downstream teams
   - How: Add `description:` field for every model and column in YAML
   - Test: Does `dbt docs` clearly explain what each model/column contains and who owns it?

3. **Testing discipline** — all sources and logical joins have tests
   - Why: Broken lineage silently corrupts downstream data; tests catch schema changes immediately
   - How: Add `dbt_expectations` tests for source freshness, referential integrity, uniqueness
   - Test: Do CI checks block PRs with missing tests?

4. **Selective materialization** — choose materialization strategically, not by default
   - Why: Wrong materialization wastes Snowflake compute or creates stale data
   - How: view (frequent changes), table (stable marts), incremental (large volumes)
   - Test: Is each materialization choice justified by query frequency and data volume?

---

## 📂 Model Layers (Architecture)

Models are organized by **semantic maturity** — each layer serves a specific purpose:

| Layer | Purpose | SLA | Examples |
|-------|---------|-----|----------|
| **Staging** | 1:1 with sources; minimal transformation | Daily | `stg_orders`, `stg_customers` |
| **Base** | Logical entities; foundational business logic | Daily | `base_transactions`, `base_customer_lifetime` |
| **Intermediate** | Pre-mart joins; complex transformations | Daily | `int_customer_payments`, `int_order_timeline` |
| **Mart** | Denormalized fact/dimension tables; BI-ready | Daily+ | `fct_orders`, `dim_customer` |
| **Operations** | Alerts, audits, metadata | Per-run | `audit_column_changes`, `alert_failed_dbt_tests` |

---

## ⚠️ Common Mistakes & Recovery

| Mistake | Impact | How to fix |
|---------|--------|-----------|
| Missing `ref()` relationships | Lineage broken; schema changes undetected | Replace `schema.table` with `{{ ref('model_name') }}` |
| No documentation on new columns | BI users confused about column meaning | Add `description:` for every column in YAML |
| Materialized as table when should be view | Stale data served to BI | Change `materialized: view` and re-run dbt |
| Missing uniqueness test on key | Duplicate fact rows silently accumulated | Add `dbt_expectations.expect_table_columns_to_match_ordered_list` test |
| No incremental logic in large models | Full model rebuilds waste Snowflake compute | Use `is_incremental()` block with `unique_key` |

---

## 🎯 Development Workflow

```
1. Create model
   └─ Choose layer (staging/base/intermediate/mart)
   └─ Write SQL following SQL style guide
   └─ Declare `ref()` and `source()` dependencies

2. Document
   └─ Add model description in YAML
   └─ Add descriptions for all columns

3. Test
   └─ Add tests for sources (freshness, completeness)
   └─ Add tests for keys (uniqueness, referential integrity)

4. Code review
   └─ Reviewer checks layer, naming, lineage, tests

5. CI validation
   └─ dbt parse (syntax check)
   └─ dbt test (all tests pass)
   └─ dbt docs (documentation present)

6. Production deploy
   └─ dbt run (build models)
   └─ dbt test (final verification)
   └─ Monitor freshness in BI layer
```

---

## 📚 Related Rules

- **style_guide_standards/sql.md** — SQL formatting and standards
- **style_guide_standards/airflow.md** — Airflow orchestration of dbt runs
- **testing.md** — dbt test strategy and best practices

---

## ✅ Model Acceptance Checklist

Before marking a model PR as ready:

- [ ] All tables referenced via `{{ ref() }}` or `{{ source() }}`
- [ ] Model and all columns have descriptions in YAML
- [ ] Tests defined for sources (freshness, completeness)
- [ ] Tests defined for keys (uniqueness, foreign key)
- [ ] SQL passes SQLFluff validation
- [ ] dbt lineage shows correct upstream/downstream
- [ ] Materialization choice justified (view/table/incremental)
- [ ] Documentation generated and reviewed (`dbt docs`)

---

## 📥 Imports

@./dbt/model_organisation.md
@./dbt/naming_conventions.md
@./dbt/yaml_resource_properties.md
@./dbt/snapshots.md
@./dbt/macros.md
