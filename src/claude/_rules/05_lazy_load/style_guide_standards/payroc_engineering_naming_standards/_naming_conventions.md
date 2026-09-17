# 🔤 Naming Conventions & Segments

**Purpose:** Core naming standards and segment definitions for all Payroc engineering resources.

**Scope:** Establishes the naming pattern, valid segments, and codes used across all repositories and infrastructure naming.

---

## 🔤 Core Naming Rules

All naming follows these rules:

- **Lowercase by default** — all segments are lowercase unless context requires otherwise
- **Hyphens between segments** — separates major parts (e.g., `dmt-scripts-claude_ai_playbook`)
- **Underscores for multi-word values within a segment** — allows compound names (e.g., `claude_ai_playbook`)
- **Periods only when necessary** — use when hyphens/underscores unavailable (e.g., DNS hostnames)
- **Standard segment order:** `[app]-[environment]-[site]-[resource-type]-[descriptor]`
- **Optional segments at end** — omit segments that don't apply

---

## 📋 Segment Reference

### Environments

| Code | Environment | Usage |
|------|-------------|-------|
| `dev` | Development | Local development work |
| `sdx` | Sandbox | Isolated testing environment |
| `stg` | Staging | Pre-production validation |
| `prf` | Performance | Performance testing environment |
| `uat` | User Acceptance Testing | Customer validation |
| `ent` | Enterprise | Enterprise-grade pre-prod |
| `crp` | Corporate | Corporate systems |
| `prd` | Production | Live production |
| `pnr` | Partner | Partner-facing systems |

**Note:** Terraform legacy uses `prod` not `prd`. Don't change live directories without explicit approval.

---

### Repository Types

| Code | Meaning | Usage |
|------|---------|-------|
| `app` | Application | Executable/service apps |
| `cac` | Configuration as Code | CloudFormation, Ansible |
| `config` | Configuration | Config files and settings |
| `etl` | ETL / data pipeline | Data processing pipelines |
| `iac` | Infrastructure as Code | Terraform/CloudFormation |
| `lib` | Shared library | Reusable code libraries |
| `llm` | LLM / AI tooling | Claude, OpenAI integrations |
| `rpa` | Robotic Process Automation | RPA workflows |
| `scripts` | Utility scripts | Automation and utilities |
| `sdk` | Software Development Kit | SDKs for external use |
| `specs` | Specifications | Design docs and specs |
| `test` | Test suite | Test automation |
| `ui` | User Interface | Frontend applications |

---

### Departments (DM-relevant)

| Code | Department |
|------|-----------|
| `dmt` | Data Management |
| `dpe` | Data Platform Engineering |
| `dan` | Data Analytics |
| `den` | Data Engineering |
| `daa` | Data Architecture & Analytics |
| `pyrc` | Payroc (cross-team/company) |

**Full list:** [Departments](https://payroc.atlassian.net/wiki/spaces/TEC/pages/5112299554) in Confluence

---

### Cloud Providers

| Code | Provider |
|------|----------|
| `aws` | Amazon Web Services |
| `azu` | Microsoft Azure |
| `gcp` | Google Cloud Platform |

---

### Automation Job Types

| Code | Type |
|------|------|
| `ansible` | Ansible playbook / role |
| `terraform` | Terraform configuration |
| `operations` | Operational / maintenance job |

---

## 🔗 Related Standards

- **[_naming_repositories.md](_naming_repositories.md)** — Repository naming examples
- **[_naming_infrastructure.md](_naming_infrastructure.md)** — VM and cloud resource naming

---

## ✅ Verification Checklist

When creating a named resource:

- [ ] Used correct segment codes from this reference
- [ ] Segments appear in standard order
- [ ] Lowercase and hyphen/underscore rules followed
- [ ] Multi-word values use underscores (not hyphens)
- [ ] Optional segments omitted if not applicable

---

**Source of truth:** [Payroc Naming Standards (Reference)](https://payroc.atlassian.net/wiki/spaces/DA/pages/5112365057) in Confluence
