# 🔁 CTE Style Guide

**Purpose:** Establish CTE patterns and grouping conventions for dbt models and SQL queries to improve readability and maintainability.

## 🚫 Use CTEs rather than subqueries

- **Preferred:** CTE statements (Common Table Expressions)
- **Avoid:** subqueries in SELECT or FROM clauses
- **Why:** CTEs are more readable and maintainable — see [dbt docs: CTE vs Subquery](https://docs.getdbt.com/terms/cte#cte-vs-subquery) for details

## 🗂️ CTE grouping structure

Use four logical grouping layers for all CTEs:

1. **Import CTEs:** base queries referencing source tables
2. **Logical CTEs:** preparation and transforms on base tables
3. **Final CTE:** join together all logical CTEs
4. **Simple SELECT:** final SELECT statement from the final CTE

See working example: `~/.claude/_rules/03_lazy_load/style_guide_standards/sql/templates/template_cte.sql`

## 📋 Contents

- [📥 Import CTEs](#-import-ctes)
- [⚙️ Logical CTEs](#-logical-ctes)
- [🏁 Final CTE](#-final-cte)
- [🔍 Final SELECT](#-final-select)

---

## 📥 Import CTEs

Base queries that reference source tables:

```sql
base_orders as (
    SELECT *
    FROM {{ source('jaffle_shop', 'orders') }}
),

base_customers as (
    SELECT *
    FROM {{ source('jaffle_shop', 'customers') }}
),
```

---

## ⚙️ Logical CTEs

Perform preparation and transforms on base tables:

```sql
customers as (
    SELECT
        first_name || ' ' || last_name AS name,
        *
    FROM base_customers
),

orders as (
    -- perform transforms on base_orders
    SELECT *
    FROM base_orders
),
```

---

## 🏁 Final CTE

Join together all logical CTEs into a single result set:

```sql
final_cte as (
    SELECT
        c.name,
        o.order_id,
        o.total
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
)
```

---

## 🔍 Final SELECT

Simple SELECT from the final CTE:

```sql
SELECT *
FROM final_cte
```
