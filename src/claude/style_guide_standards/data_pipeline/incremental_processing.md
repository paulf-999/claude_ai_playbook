# ⚡ Incremental Processing

## When to use incremental vs full refresh

Choose based on table size and load frequency:

| Condition | Pattern |
|---|---|
| Table grows continuously (events, transactions, logs) | Incremental |
| Load runs multiple times per day | Incremental |
| Table is small and rarely changes | Full refresh acceptable |
| Source data is mutable (updates or deletes are common) | Incremental with `merge` or `delete+insert` |
| Table must be fully auditable from scratch | Full refresh or snapshot |

A full refresh that is acceptable at 10M rows becomes a cost and SLA problem at 1B rows. Default to incremental for any table expected to grow beyond ~50M rows.

---

## Watermark patterns

A watermark is a high-water mark stored externally (a variable, metadata table, or DAG parameter) that records the last successfully processed offset — typically a timestamp or sequence ID.

Standard approach:
1. Read the current watermark at the start of each run
2. Process records where `event_time > watermark`
3. Write the new high-water mark only after the run succeeds

Never update the watermark before the run completes — a partial write followed by a watermark advance will silently skip records on retry.

---

## Late-arriving data

Data does not always arrive in event-time order. Define and document a **lookback window** — the period beyond the watermark within which late records are expected:

- Typical range: 1–7 days depending on source SLA
- The lookback window must be documented in the pipeline config or model comment
- Incremental models must re-process the lookback window on every run, not just records newer than the watermark

Do not assume strict ordering. A pipeline that processes only `event_time > last_run` will silently drop late-arriving records.

---

## Bounded execution windows

Parameterise pipeline runs on a logical execution date rather than wall-clock time. This enables:
- Reproducible backfills (re-run any past window and get the same result)
- Idempotent retries (re-running the same window is safe)
- Clear SLA attribution (latency is measured against the execution date, not system time)

Airflow: use `{{ ds }}` / `{{ data_interval_start }}` to derive the processing window — never `datetime.now()`.
dbt: pass `execution_date` via `vars` in production runs; use the same var in `where` filters.
