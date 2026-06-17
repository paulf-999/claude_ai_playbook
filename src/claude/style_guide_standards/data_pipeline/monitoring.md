# 📊 Pipeline Monitoring

## The two failure modes

Pipelines fail in two ways — noisy failures (exceptions, job crashes) and silent failures (a job succeeds but produces wrong or stale data). Logging and error handling address the first. Threshold-based monitoring addresses the second.

A table that stopped loading three days ago is a failure even if no exception was raised. Design monitoring to catch both.

---

## Freshness SLAs

Every dataset that feeds a downstream consumer should have a defined freshness SLA — the maximum acceptable age of the data before it is considered stale.

For each dataset, document:
- **Expected load frequency** (e.g. daily at 06:00 UTC)
- **Freshness threshold** (e.g. alert if data is older than 25 hours)
- **Downstream impact** (which dashboards or processes depend on it)

dbt: use `freshness` blocks in `sources.yml` to define and automatically check source freshness. Set `warn_after` and `error_after` thresholds that match the dataset's SLA.

Airflow: use SLA misses (`sla` parameter on tasks/DAGs) or a dedicated freshness-check task at the end of each pipeline run.

---

## Row-count monitoring

Unexpected row count changes are an early signal of upstream problems — truncated extracts, schema changes, or silent data quality failures.

At each stage of a pipeline, log and compare:
- **Absolute count**: how many records were processed
- **Delta from previous run**: flag drops > X% or spikes > Y% as warnings
- **Zero-record runs**: a pipeline that processed zero records when it normally processes thousands should alert, not succeed silently

Define what "normal" looks like per dataset and codify it — do not rely on manual inspection to catch anomalies.

---

## What to alert on vs log

Not everything worth logging is worth alerting on. Reserve alerts for conditions that require human action:

| Alert | Log only |
|---|---|
| Freshness threshold breached | Row counts within normal range |
| Row count drops > 20% from baseline | Warning-level anomalies under investigation |
| Pipeline failure after all retries | Retry attempts (transient failures) |
| Schema change detected at source | New column detected (if non-breaking) |
| Zero records processed | Processing time within normal range |

Avoid alert fatigue — over-alerting trains teams to ignore notifications. Every alert should have a clear owner and a defined response action.
