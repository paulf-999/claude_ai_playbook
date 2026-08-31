# 🗂️ SQL Formatting Standards

**Purpose:** Establish formatting and style conventions for SQL queries and dbt models to ensure readability, consistency, and maintainability.


## 📋 Contents

- [🔠 Keywords and capitalisation](#-keywords-and-capitalisation)
- [🏷️ Naming conventions](#-naming-conventions)
- [🗂️ Structure](#-structure)
- [🔗 Joins](#-joins)
- [🔤 Aliases](#-aliases)
- [↔️ Indentation](#-indentation)
- [📊 Ordering and aggregation](#-ordering-and-aggregation)
- [💬 Commenting](#-commenting)

---
## 🔠 Keywords and capitalisation

- **Keywords:** UPPERCASE for `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, etc.
- **Functions:** UPPERCASE for `COALESCE`, `SUM`, `DATE_TRUNC`, etc.
- **Literals:** UPPERCASE for `TRUE`, `FALSE`, `NULL`
- **Consistency:** identifier capitalisation (column names, table names) must be consistent within a statement

## 🏷️ Naming conventions

- **Format:** `snake_case` only — letters, numbers, underscores; begin with letter; don't end with underscore
- **Case:** never `CamelCase` — harder to scan
- **Singularity:** use singular names, not plural (e.g., `staff` over `employees`)
- **No abbreviations:** only universally understood abbreviations allowed
- **No prefixes:** do not prefix table names with `tbl_` or other descriptors
- **Descriptive IDs:** avoid plain `id` as sole primary key — use `order_id`, `customer_id`, etc.

## 🗂️ Structure

- **Use CTEs over subqueries:** one CTE per logical step, named descriptively
- **Follow grouping pattern:** Import → Logical → Final → SELECT (see [`cte_style_guide.md`](cte_style_guide.md))
- **DRY code:** consolidate repeated logic using CTEs and Jinja
- **No wildcards:** use explicit column lists — never `SELECT *` in production
- **One column per line:** in `SELECT` statements
- **Leading commas:** commas start the line, not end the previous line:

```sql
SELECT
    order_id
    , customer_id
    , order_date
FROM orders
```

## 🔗 Joins

- **Explicit type:** always specify `INNER JOIN`, `LEFT JOIN` — never bare `JOIN`
- **ON placement:** place join conditions on a new indented line
- **Always alias:** meaningful aliases, never single letters
- **Prefix columns:** in joins with multiple tables, always prefix column names with table alias
- **Prefer LEFT:** use `LEFT JOIN` over `RIGHT JOIN` — swap `FROM` and `JOIN` tables if needed
- **Use UNION ALL:** prefer `UNION ALL` over `UNION` unless duplicate elimination is required

## 🔤 Aliases

- **Use AS:** explicitly when aliasing columns or tables
- **Meaningful names:** aliases should describe what the column or table represents

## ↔️ Indentation

- **Spacing:** 4 spaces per indent level
- **Joins:** indented relative to `FROM` clause
- **ON conditions:** indented relative to their `JOIN` statement

## 📊 Ordering and aggregation

- **Select order:** list plain fields before aggregates and window functions
- **Early aggregation:** aggregate before joining to another table where feasible
- **Positional references:** use `GROUP BY 1, 2` instead of repeating column names
- **Limit columns:** avoid grouping by many columns — if needed, reconsider model design

## 💬 Commenting

- **When:** include comments where logic is non-obvious
- **Block comments:** use `/* ... */` for multi-line or statement-level comments
- **Inline comments:** use `--` for brief explanations

```sql
SELECT file_hash  -- inline comment here
FROM file_system
WHERE file_name = '.abc';
```

```sql
/* Updating the file record after writing to the file */
UPDATE file_system
SET file_modified_date = '1980-02-22 13:19:01.00000',
    file_size = 209732
WHERE file_name = '.abc';
```
