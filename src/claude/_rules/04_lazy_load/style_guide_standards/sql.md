# 🗄️ SQL Style Guide & Standards

**Purpose:** Define team SQL standards for consistency, readability, and cost optimization. Standards apply to all SQL written in the warehouse (dbt, Airflow, ad-hoc queries).

**Enforcement:** All SQL must pass SQLFluff validation before commit/merge. Violations surface in pre-commit checks.

## 📋 Child pages

| File | Purpose | When to load |
|------|---------|-------------|
| [`sql/formatting.md`](sql/formatting.md) | Keywords, structure, joins, aliases, indentation rules | Writing SQL queries |
| [`sql/cte_style_guide.md`](sql/cte_style_guide.md) | CTE grouping pattern (Import → Logical → Final → SELECT) | Structuring complex queries |
| [`sql/snowflake_data_type_standards.md`](sql/snowflake_data_type_standards.md) | Preferred Snowflake data types and why (cost, correctness) | Choosing data types in model definitions |
| [`sql/sqlfluff.md`](sql/sqlfluff.md) | SQLFluff dialect/templater settings, excluded rules, troubleshooting | Debugging SQLFluff violations |

---

## 🎯 Core Principles

- **Consistency:** All SQL follows the same style; code reviews focus on logic, not formatting
- **Readability:** SQL is read more than written; prioritize clarity (CTEs > subqueries; explicit aliases)
- **Cost control:** Write queries that minimize Snowflake warehouse spend (smallest warehouse sufficient, query scans optimized)
- **Correctness:** Use `ref()` and `source()` in dbt; never hardcode references (enables safe refactoring)

---

## 🛠️ Tooling

SQL style is enforced by **SQLFluff** in dialect mode `snowflake`:
- Pre-commit hook validates all `.sql` files and dbt models
- Violations block commits; fix before retry
- See [`sql/sqlfluff.md`](sql/sqlfluff.md) for dialect settings, rule exclusions, and troubleshooting

**Common violations & fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `L019: Inconsistent capitalisation` | Mixed case keywords | Use UPPERCASE for keywords |
| `L029: Ambiguous reference` | Unqualified column name | Add table alias: `table.column` |
| `L031: Avoid using reserved keywords` | Keyword used as identifier | Use backticks: `` `column` `` |

---

## 🏗️ dbt-specific

- **Use `ref()` for all model references** — never hardcode schema or table names (enables refactoring)
- **Use `source()` for raw source references** — documents data lineage and owner
- **Document all models and columns in YAML** — `description:` fields are source-of-truth for downstream teams
- **Test all source and ref relationships** — prevents silent schema changes from breaking pipelines

---

## 💰 Cost guardrails

- **`AUTO_SUSPEND = 60`:** set on all pipeline warehouses (idle warehouses are the largest spend leak)
- **Match warehouse size to query complexity:**
  - XS: Simple aggregations, tests, dbt runs in dev
  - S: Standard dbt runs in CI/prod
  - M+: Complex transformations, join-heavy queries (should be rare)
- **Validate query scans:** check query profile before merging large refactors
  - Increased scans = increased cost; flag in PR if scan count jumps >20%

---

## ⚠️ Common Mistakes & Recovery

**Hardcoding table references in dbt models**
- ❌ `FROM schema.my_table`
- ✅ `FROM {{ source('raw', 'my_table') }}`
- **Recovery:** Search and replace all hardcoded refs; document source ownership

**Over-aliasing leading to unreadable queries**
- ❌ `SELECT a.id, b.amt, c.dt FROM table_a a JOIN table_b b ON a.id = b.id ...`
- ✅ Use CTEs: `WITH customers AS (SELECT ...), orders AS (SELECT ...) SELECT customer.id, order.amount FROM customers JOIN orders ...`
- **Recovery:** Refactor into CTEs following CTE style guide

**Forgetting to document new columns**
- ❌ Adding column to model without updating YAML
- ✅ Every column has `name:` and `description:` in YAML
- **Recovery:** Add missing YAML; PR cannot merge without it

---

## 📚 Related Rules

- **style_guide_standards/dbt.md** — dbt-specific conventions (naming, macros, snapshots)
- **style_guide_standards/airflow.md** — Airflow SQL task patterns
- **testing.md** — How to test dbt models and raw sources

---

## ✅ Pre-commit Validation

Before committing SQL changes:

- [ ] SQLFluff passes (no violations)
- [ ] All hardcoded refs replaced with `ref()` or `source()`
- [ ] dbt models have `description:` fields for all columns
- [ ] Query scan cost validated if query complexity increased
- [ ] Aliases are meaningful (not single letters)

---

## Imports

@./sql/formatting.md
@./sql/cte_style_guide.md
@./sql/snowflake_data_type_standards.md
@./sql/sqlfluff.md
