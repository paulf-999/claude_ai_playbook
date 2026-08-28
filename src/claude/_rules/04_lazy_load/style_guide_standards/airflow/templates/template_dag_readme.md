# parent_dag_salesforce_hourly

## 📋 Contents

- [Overview](#-overview)
- [Schedule](#-schedule)
- [Dependencies](#-dependencies)
- [Notes](#-notes)

---
## Overview

Orchestrates the hourly execution of Airbyte ingestion from Salesforce, followed by dbt staging and base model runs.

## Schedule

Runs hourly at minute 40 from 7 AM to 11:59 PM UTC (`40 7-23 * * *`).

## Dependencies

- Airbyte connection: `salesforce`
- dbt models: `models/staging/salesforce/`, `models/base/salesforce/`

## Notes

- Airbyte step is currently skipped — Airbyte AWS server not yet reachable from Airflow PROD.
