# 🗄️ SQL Style Guide & Standards

Defines the team's SQL coding standards, formatting conventions, and SQLFluff configuration.

## Child pages

| File | Purpose |
|------|---------|
| [`sql/formatting.md`](formatting.md) | Keywords, structure, joins, aliases, and indentation rules |
| [`sql/cte_style_guide.md`](cte_style_guide.md) | CTE grouping pattern (Import → Logical → Final → SELECT) |
| [`sql/snowflake_data_type_standards.md`](snowflake_data_type_standards.md) | Preferred Snowflake data types and rationale |
| [`sql/sqlfluff.md`](sqlfluff.md) | SQLFluff dialect/templater settings and excluded rules |

## 📋 Contents

- [Tooling](#-tooling)
- [dbt-specific](#-dbt-specific)
- [Cost guardrails](#-cost-guardrails)
- [Imports](#-imports)

---

## Tooling

SQL style is enforced by SQLFluff — see [`sql/sqlfluff.md`](sqlfluff.md) for the full config reference. All SQLFluff violations must be resolved before committing.

---

## dbt-specific

- Use `ref()` for all model references — never hardcode schema or table names.
- Use `source()` for raw source references.
- Document all models and columns in `.yml` files.

---

## Cost guardrails

- **`AUTO_SUSPEND = 60`:** set on all pipeline warehouses — idle warehouses are the most common source of unexpected Snowflake spend.

---

## Imports

@./formatting.md
@./cte_style_guide.md
@./snowflake_data_type_standards.md
@./sqlfluff.md
