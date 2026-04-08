# 🗂️ SQL Formatting Standards

## 🔠 Keywords and capitalisation

- Keywords in UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, etc.
- Function names in UPPERCASE: `COALESCE`, `SUM`, `DATE_TRUNC`, etc.
- Boolean and null literals in UPPERCASE: `TRUE`, `FALSE`, `NULL`
- Identifier capitalisation (column names, table names) must be consistent within a statement.

---

## 🏷️ Naming conventions

- Use `snake_case` for all identifiers: only letters, numbers, and underscores. Names must begin with a letter and must not end with an underscore.
- Do not use `CamelCase` — it is harder to scan quickly.
- Use singular names, not plural. Where a collective term exists, prefer it (e.g., `staff` over `employees`).
- Do not use abbreviations unless they are universally understood.
- Do not prefix table names with `tbl` or any other descriptive prefix.
- Avoid using plain `id` as the sole primary key column name — use a descriptive identifier (e.g., `order_id`, `customer_id`).

---

## 🗂️ Structure

- Use CTEs (`WITH`) over subqueries. One CTE per logical step, named descriptively. Follow the four-grouping pattern (Import → Logical → Final → SELECT) — see [`cte_style_guide.md`](cte_style_guide.md).
- Make code DRY using CTEs and Jinja — if the same logic appears twice, it must be consolidated.
- Always use explicit column lists — no `SELECT *` in production models or queries.
- One column per line in `SELECT` statements.
- Commas are **leading** (start of line), not trailing:

```sql
SELECT
    order_id
    , customer_id
    , order_date
FROM orders
```

- No trailing comma on the final column in a `SELECT` clause.

---

## 🔗 Joins

- Always specify the join type explicitly: `INNER JOIN`, `LEFT JOIN` — never bare `JOIN`.
- Place join conditions on a new indented line using `ON`.
- Always alias joined tables; aliases should be meaningful, not single letters.
- When joining two or more tables, always prefix column names with the table alias. Prefixes are not required when selecting from a single table.
- Prefer `LEFT JOIN` over `RIGHT JOIN` — a `RIGHT JOIN` usually indicates the `FROM` and `JOIN` tables should be swapped.
- Prefer `UNION ALL` over `UNION` unless duplicate elimination is explicitly required.

---

## 🔤 Aliases

- Use `AS` explicitly when aliasing columns or tables.
- Aliases should describe what the column or table represents.

---

## ↔️ Indentation

- Indent with 4 spaces.
- Joins are indented relative to the `FROM` clause.
- `ON` conditions are indented relative to their `JOIN`.

---

## 📊 Ordering and aggregation

- In `SELECT` statements, list plain fields before aggregates and window functions.
- Perform aggregations as early as possible — aggregate before joining to another table where feasible.
- Use positional references in `GROUP BY` and `ORDER BY` (e.g., `GROUP BY 1, 2`) rather than repeating column names. Avoid grouping by more than a few columns — if you are, reconsider the model design.

---

## 💬 Commenting

- Include comments where the logic is non-obvious.
- Use C-style block comments (`/* ... */`) for multi-line or statement-level comments.
- Use `--` for inline comments.

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
