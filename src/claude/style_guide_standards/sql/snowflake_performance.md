# ❄️ Snowflake Performance

## Clustering keys

Clustering keys control the physical order of micro-partitions in a table, enabling Snowflake to skip partitions that do not match a query's filter. Without clustering, every query scans all micro-partitions.

**When to define a clustering key:**
- The table is large (> ~50M rows)
- Queries consistently filter on the same column(s)
- The dominant query pattern filters by date range, merchant ID, or entity ID

**Column selection:**
- Prefer low-to-medium cardinality expressions: `DATE_TRUNC('day', created_at)`, `merchant_id`, `entity_type`
- Use `DATE_TRUNC` rather than raw timestamps — timestamp clustering creates too many distinct values to cluster effectively
- Composite keys (up to 3–4 columns) are valid; order matters — put the most selective filter column first

**Defining in SQL:**
```sql
ALTER TABLE my_schema.my_table
  CLUSTER BY (DATE_TRUNC('day', created_at), merchant_id);
```

**Reviewing clustering health:**
```sql
SELECT SYSTEM$CLUSTERING_INFORMATION('my_schema.my_table', '(DATE_TRUNC(''day'', created_at))');
```

A `average_overlaps` value above ~5 indicates significant clustering degradation — consider re-clustering or reviewing the key choice.

---

## Query Profile

Snowflake's Query Profile identifies where time and credit are spent in a query. Use it when a query is slower or more expensive than expected.

Key nodes to inspect:
- **TableScan**: high `Partitions scanned` relative to `Partitions total` means the clustering key is not aligned with the query filter
- **Sort**: large sort operations often indicate a missing or misaligned clustering key
- **Spillage to disk**: the warehouse is undersized for this workload; consider scaling up or optimising the query

Access via: Snowflake UI → Query History → select query → Query Profile tab.

---

## Warehouse sizing and auto-suspend

- Use the smallest warehouse that meets the SLA — start at XS or S and scale up only if pipeline runtime exceeds the SLA budget
- Configure `AUTO_SUSPEND = 60` on all pipeline warehouses; idle warehouses are the most common source of unexpected Snowflake spend
- Separate pipeline warehouses from interactive/BI query warehouses — shared warehouses create contention and make cost attribution impossible

```sql
ALTER WAREHOUSE my_pipeline_wh SET
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;
```

- Review warehouse utilisation monthly via the `WAREHOUSE_METERING_HISTORY` view in `SNOWFLAKE.ACCOUNT_USAGE` — identify warehouses with high idle credit consumption
