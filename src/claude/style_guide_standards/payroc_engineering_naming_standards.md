# 🏷️ Payroc Engineering Naming Standards

Company-wide naming standards for all Payroc engineering resources — repositories, infrastructure objects, automation jobs, and related artefacts. Source of truth: [DM - Payroc Naming Standards (Reference)](https://payroc.atlassian.net/wiki/spaces/DA/pages/5112365057) in the TEC Confluence space.

---

## 🔤 Naming rules

- **Lowercase by default** — all segments are lowercase
- **Hyphens between segments** — e.g. `dmt-scripts-claude_ai_playbook`
- **Underscores for multi-word values within a segment** — e.g. `claude_ai_playbook` as the descriptor
- **Periods** only when hyphens and underscores are unavailable (e.g. DNS hostnames)
- **Standard segment order:** `[app]-[environment]-[site]-[resource-type]-[descriptor]`
- Optional segments are placed at the end; omit segments that do not apply

---

## 🗂️ Segment reference

### Environments

| Code | Environment |
|------|-------------|
| `dev` | Development |
| `sdx` | Sandbox |
| `stg` | Staging |
| `prf` | Performance |
| `uat` | User Acceptance Testing |
| `ent` | Enterprise |
| `crp` | Corporate |
| `prd` | Production |
| `pnr` | Partner |

> **Note:** The Terraform repo uses `prod` as its environment directory name — a pre-existing deviation from the company standard (`prd`). Do not change live Terraform directories to align with this standard without an explicit decision.

---

### Repository types

| Code | Meaning |
|------|---------|
| `app` | Application |
| `cac` | Configuration as Code |
| `config` | Configuration files |
| `etl` | ETL / data pipeline |
| `iac` | Infrastructure as Code |
| `lib` | Shared library |
| `llm` | LLM / AI tooling |
| `rpa` | Robotic Process Automation |
| `scripts` | Utility scripts |
| `sdk` | Software Development Kit |
| `specs` | Specifications |
| `test` | Test suite |
| `ui` | User Interface |

---

### Departments (DM-relevant subset)

| Code | Department |
|------|-----------|
| `dmt` | Data Management |
| `dpe` | Data Platform Engineering |
| `dan` | Data Analytics |
| `den` | Data Engineering |
| `daa` | Data Architecture & Analytics |
| `pyrc` | Payroc (cross-team / company-level) |

For the full departments list, see the [Departments page](https://payroc.atlassian.net/wiki/spaces/TEC/pages/5112299554) in the TEC Confluence space.

---

### Cloud providers

| Code | Provider |
|------|---------|
| `aws` | Amazon Web Services |
| `azu` | Microsoft Azure |
| `gcp` | Google Cloud Platform |

---

### Automation job types

| Code | Type |
|------|------|
| `ansible` | Ansible playbook / role |
| `terraform` | Terraform configuration |
| `operations` | Operational / maintenance job |

---

## 📦 Repository naming

Pattern: `[dept]-[repo-type]-[descriptor]`

- `dept` — from the Departments segment (e.g. `dmt`, `pyrc`)
- `repo-type` — from the Repository Types segment (e.g. `scripts`, `lib`, `iac`, `etl`)
- `descriptor` — snake_case for multi-word names

Examples:

| Repository | Breakdown |
|------------|-----------|
| `dmt-scripts-claude_ai_playbook` | dept=`dmt`, type=`scripts`, descriptor=`claude_ai_playbook` |
| `dmt-lib-airflow_platform` | dept=`dmt`, type=`lib`, descriptor=`airflow_platform` |
| `dmt-iac-snowflake_terraform` | dept=`dmt`, type=`iac`, descriptor=`snowflake_terraform` |
| `pyrc-iac-tf` | dept=`pyrc`, type=`iac`, descriptor=`tf` |
| `pyrc-cac-ans` | dept=`pyrc`, type=`cac`, descriptor=`ans` |

For complete reference tables (Applications, Business Units, Sites, Geographical Regions), see the [Payroc Naming Standards](https://payroc.atlassian.net/wiki/spaces/DA/pages/5112365057) in Confluence.

---

## 🖥️ Virtual machine naming

Pattern (no separators, 15-char NetBIOS limit):

```
[site][environment][pci_scope_short_code][application_owner][asset_role][sequential_index]
```

Annotated example: `elkprdcpyrcabt1`
- `elk` = site
- `prd` = environment
- `c` = PCI scope short code (`connected_to`, non-dev)
- `pyrc` = application owner (department)
- `abt` = asset role (Airbyte)
- `1` = sequential index

Source of truth: `modules/payroc/primitives/virtual_machine/main.tf` in `pyrc-iac-tf`.

---

## 🔐 PCI scope codes

Three valid scope names, corresponding to standard PCI DSS scoping categories:

| Scope | Meaning |
|---|---|
| `cardholder_data` | Systems that directly store, process, or transmit cardholder data (PANs, CVVs, expiry dates). The Cardholder Data Environment (CDE) — most sensitive tier. |
| `connected_to` | Systems connected to the CDE but not directly handling card data (e.g. auth servers, monitoring, jump hosts). In scope because a compromise here could impact the CDE. |
| `out_of_scope` | Systems with no connection to the CDE and no ability to affect its security. Fully isolated. |

Dev environments: `sdx`, `stg`, `dev`, `prf`. Non-dev: `prd`, `uat`, `crp`, `pnr`, `ent`.

Short codes appear in VM names. Long codes appear in Azure resource names.

| Scope | Short code (dev) | Short code (non-dev) | Long code (dev) | Long code (non-dev) |
|---|---|---|---|---|
| `cardholder_data` | `h` | `i` | `dcd` | `cde` |
| `connected_to` | `b` | `c` | `dct` | `ctd` |
| `out_of_scope` | `n` | `o` | `doo` | `oos` |

---

### Sites

Valid site codes (from `modules/payroc/standards/sites.tf` in `pyrc-iac-tf`):

`am1`, `am3`, `az4`, `az5`, `az6`, `elk`, `ent`, `ind`, `sbd`

---

### Asset roles (DM-relevant subset)

Three-letter codes used in VM names. Full list: [Naming - Asset Roles](https://payroc.atlassian.net/wiki/spaces/TEC/pages/1853161585) in Confluence.

| Code | Role |
|------|------|
| `abt` | Airbyte |
| `afl` | Airflow |
| `ans` | Ansible |
| `cld` | Claude |
| `dkr` | Docker |
| `etl` | ETL |
| `gar` | GitHub Actions Runner |
| `ghe` | GitHub Enterprise |
| `run` | Rundeck |
| `scr` | Scalr |
| `sno` | Snowflake |
| `vlt` | Vault |
