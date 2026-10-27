---
paths:
  - "**/models/**/*.sql"
  - "**/dbt_project.yml"
---
<!-- version: 1.2.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-27 -->
<!-- miss_cost: medium — models that break naming or layering and fail review -->
<!-- loading: path-scoped — only applies to dbt models, so it loads when a model or dbt_project.yml is open -->
# 🔵 dbt Style Guide & Standards

**Purpose:** Define standards for the dbt project — covering model organization, naming, YAML properties, testing, snapshots, and macros. Standards ensure consistency, maintainability, and correctness across the dbt project.

**Scope:** All models, macros, and YAML in the dbt project. Standards are checked in CI and enforce best practices from [dbt Labs style guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md).

## 📋 Child pages

| File | Purpose | When to load |
|------|---------|-------------|
| [`dbt/model_organisation.md`](dbt/model_organisation.md) | Model layers (staging → base → mart → publication), folder structure, minimum requirements | Creating a new model or directory |
| [`dbt/naming_conventions.md`](dbt/naming_conventions.md) | Naming for models (prefixes), keys, marts, audit fields, null handling | Choosing names for models/columns |
| [`dbt/yaml_resource_properties.md`](dbt/yaml_resource_properties.md) | YAML structure, property names, style conventions | Writing `.yml` files |
| [`dbt/snapshots.md`](dbt/snapshots.md) | Snapshot use cases, configuration, best practices, examples | Working with slowly-changing dimensions |
| [`dbt/macros.md`](dbt/macros.md) | Custom macros directory, dbt packages, conventions | Building shared/reusable logic |

For SQL formatting rules within dbt models, see [`sql.md`](sql.md).

---

## 🎯 Core Principles

**dbt excellence rests on these four pillars:**

1. **Lineage clarity** — use `ref()` and `source()` everywhere; never hardcoded table references
   - **Why:** builds the lineage graph that `dbt docs generate` renders, and allows safe refactoring
   - **How:** every table reference is `{{ ref('model') }}` or `{{ source('raw', 'table') }}`
   - **Test:** does the lineage graph in the generated docs show the correct upstream and downstream models?

2. **Documentation completeness** — every model and column has a description
   - **Why:** undocumented models create confusion, and descriptions are the source of truth for downstream teams
   - **How:** add a `description:` field for every model and column in YAML
   - **Test:** do the docs from `dbt docs generate` explain what each model and column contains and who owns it?

3. **Testing discipline** — all sources and logical joins have tests
   - **Why:** broken lineage silently corrupts downstream data, and tests catch schema changes immediately
   - **How:** apply `unique` and `not_null` to every model's `KEY`, plus source freshness and `relationships` tests where they fit
   - **Test:** do CI checks block PRs with missing tests?

4. **Selective materialization** — choose materialization strategically, not by default
   - **Why:** the wrong materialisation wastes Snowflake compute or creates stale data
   - **How:** start from each layer's default in `model_organisation.md`, and justify any change
   - **Test:** is each materialisation choice justified by query frequency and data volume?

---

## 📂 Model Layers (Architecture)

- **Four layers:** Staging → Base → Mart → Publication, defined with their materialisations in [`dbt/model_organisation.md`](dbt/model_organisation.md).
- **Prefixes:** `staging_`, `mart_` and `pub_`, with no prefix for base models, per [`dbt/naming_conventions.md`](dbt/naming_conventions.md).

---

## ⚠️ Common Mistakes & Recovery

| Mistake | Impact | How to fix |
|---------|--------|-----------|
| Missing `ref()` relationships | Lineage broken; schema changes undetected | Replace `schema.table` with `{{ ref('model_name') }}` |
| No documentation on new columns | BI users confused about column meaning | Add `description:` for every column in YAML |
| Materialized as table when should be view | Stale data served to BI | Change `materialized: view` and re-run dbt |
| Missing uniqueness test on key | Duplicate fact rows silently accumulated | Add `unique` and `not_null` tests on `KEY` in the model's YAML |
| No incremental logic in large models | Full model rebuilds waste Snowflake compute | Use `is_incremental()` block with `unique_key` |

---

## 🎯 Development Workflow

```
1. Create model
   └─ Choose layer (staging/base/mart/publication)
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
   └─ dbt docs generate (documentation present)

6. Production deploy
   └─ dbt run (build models)
   └─ dbt test (final verification)
   └─ Monitor freshness in BI layer
```

---

## ✅ Model Acceptance Checklist

Before marking a model PR as ready:

- [ ] All tables referenced via `{{ ref() }}` or `{{ source() }}`
- [ ] Model and all columns have descriptions in YAML
- [ ] Tests defined for sources (freshness, completeness)
- [ ] Tests defined for keys (uniqueness, foreign key)
- [ ] SQL passes SQLFluff validation
- [ ] Lineage graph in the generated docs shows correct upstream/downstream
- [ ] Materialization choice justified (view/table/incremental)
- [ ] Documentation generated and reviewed (`dbt docs generate`)
