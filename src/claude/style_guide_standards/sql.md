# 🗄️ SQL Style Guide & Standards

Defines the team's SQL coding standards, formatting conventions, and SQLFluff configuration.

## Child pages

| File | Purpose |
|------|---------|
| [`sql/formatting.md`](sql/formatting.md) | Keywords, structure, joins, aliases, and indentation rules |
| [`sql/cte_style_guide.md`](sql/cte_style_guide.md) | CTE grouping pattern (Import → Logical → Final → SELECT) |
| [`sql/snowflake_data_type_standards.md`](sql/snowflake_data_type_standards.md) | Preferred Snowflake data types and rationale |
| [`sql/sqlfluff.md`](sql/sqlfluff.md) | SQLFluff dialect/templater settings and excluded rules |

---

## Tooling

SQL style is enforced by SQLFluff — see [`sql/sqlfluff.md`](sql/sqlfluff.md) for the full config reference. All SQLFluff violations must be resolved before committing.

---

## dbt-specific

- Use `ref()` for all model references — never hardcode schema or table names.
- Use `source()` for raw source references.
- Document all models and columns in `.yml` files.

---

## Imports

@./sql/formatting.md
@./sql/cte_style_guide.md
@./sql/snowflake_data_type_standards.md
@./sql/sqlfluff.md
