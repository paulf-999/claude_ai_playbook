# 🖥️ Infrastructure & Resource Naming

**Purpose:** Standards for naming virtual machines, cloud resources, and infrastructure assets.

**Scope:** VM hostnames, cloud storage, databases, and other infrastructure managed by Payroc.

---

## Virtual Machine Naming

VM hostnames follow this pattern:

```
[environment]-[site]-[asset-role]-[instance-number].[domain]
```

| Component | Values | Example |
|-----------|--------|---------|
| **environment** | `dev`, `stg`, `prf`, `uat`, `prd` | prd |
| **site** | 2-letter AWS region code (see Sites table) | us |
| **asset-role** | VM type/purpose (see Asset Roles table) | app, db, web |
| **instance-number** | Numeric ID if multiple of same type | 01 |
| **domain** | Always `.payroc.io` | |

### Example VMs

| VM | Breakdown | Purpose |
|----|-----------|---------|
| `prd-us-app-01.payroc.io` | prod + US + application server + #1 | Production app server |
| `stg-eu-db-01.payroc.io` | staging + EU + database + #1 | Staging database |
| `dev-us-web-01.payroc.io` | dev + US + web server + #1 | Development web tier |

---

## Cloud Resources (AWS/Azure/GCP)

Use repository naming convention extended to resources:

```
[department]-[environment]-[site]-[resource-type]-[descriptor]
```

**Examples:**

- S3 bucket: `dmt-prd-us-s3-dbt-models`
- RDS instance: `dmt-prd-snowflake-replica`
- Azure storage: `dmt-prd-datalake-raw`

---

## PCI Scope Codes

Used to classify infrastructure subject to PCI DSS compliance:

| Code | Scope | Definition |
|------|-------|-----------|
| `0` | No PCI | Not in PCI scope; no cardholder data |
| `1` | Restricted | May contain CHD; requires access controls |
| `2` | Internal only | Internal systems; segmented from public network |
| `3` | Monitored | Systems under continuous audit and monitoring |

**PCI marking:** Include PCI scope in VM naming if applicable:

- Non-PCI: No annotation needed
- PCI Scope 1-3: Tag in comments or monitoring system

---

## Sites (AWS Regions)

| Code | Region | Availability |
|------|--------|--------------|
| `us` | US East (N. Virginia) | Primary production |
| `eu` | EU (Ireland) | European compliance |
| `sg` | Singapore | APAC |
| `ca` | Canada (Central) | Data residency |

---

## Asset Roles (VM Purpose)

| Code | Role | Purpose | PCI Scope |
|------|------|---------|-----------|
| `app` | Application Server | Business logic, services | 0-1 |
| `api` | API Gateway | Request routing | 1 |
| `web` | Web Server | Public-facing frontend | 0-1 |
| `db` | Database | Persistent storage | 1-3 |
| `cache` | Cache Server | Redis, Memcached | 0 |
| `queue` | Message Queue | SQS, RabbitMQ | 0 |
| `mon` | Monitoring | Prometheus, Datadog | 0-2 |
| `sec` | Security/Bastion | SSH jumphost, WAF | 2-3 |
| `orch` | Orchestration | Airflow, Kubernetes | 0-1 |
| `etl` | ETL Server | Talend, Informatica | 1 |

---

## ✅ Validation Checklist

When naming infrastructure:

- [ ] VM hostname uses `[env]-[site]-[role]-[#]` pattern
- [ ] Domain suffix is `.payroc.io` (not `.internal`, `.local`)
- [ ] PCI scope documented if applicable
- [ ] Asset role matches actual purpose
- [ ] Instance number used if multiple of same role in environment

---

## 🔗 Related Standards

- **[_naming_conventions.md](_naming_conventions.md)** — Core segment definitions
- **[_naming_repositories.md](_naming_repositories.md)** — Repository naming standards
