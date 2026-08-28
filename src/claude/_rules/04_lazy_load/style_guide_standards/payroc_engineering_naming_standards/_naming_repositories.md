# 🏗️ Repository Naming

**Purpose:** Standards for naming repositories within Payroc engineering.

**Scope:** All Git repositories created under `~/git_repos/`. Follows the segment codes defined in `_naming_conventions.md`.

---

## Pattern

```
[department]-[type]-[descriptor]
```

| Part | Meaning | Example |
|------|---------|---------|
| **department** | Team/org owning the repo | `dmt`, `dpe`, `pyrc` |
| **type** | Repo type code | `scripts`, `lib`, `iac`, `app` |
| **descriptor** | What it does (multi-word: use underscore) | `claude_ai_playbook`, `airflow_platform` |

---

## Examples

### Data Management (dmt) repos

| Repo | Pattern | Purpose |
|------|---------|---------|
| `dmt-scripts-claude_ai_playbook` | dmt-scripts-[name] | Claude playbook and rules |
| `dmt-lib-airflow_platform` | dmt-lib-[name] | Shared Airflow platform code |
| `dmt-iac-aws` | dmt-iac-[name] | AWS infrastructure (CloudFormation) |
| `dmt-scripts-airbyte` | dmt-scripts-[name] | Airbyte configuration and transforms |
| `da-etl-dbtanalytics` | [legacy] | dbt analytics project (legacy naming) |

### Engineering (pyrc) repos

| Repo | Pattern | Purpose |
|------|---------|---------|
| `pyrc-iac-tf` | pyrc-iac-[name] | Company-wide Terraform |
| `pyrc-cac-ans` | pyrc-cac-[name] | Company-wide Ansible (CaC) |

---

## ✅ Validation Checklist

When creating a new repo:

- [ ] Department code matches owning team
- [ ] Type code is one of: `app`, `cac`, `config`, `etl`, `iac`, `lib`, `llm`, `rpa`, `scripts`, `sdk`, `specs`, `test`, `ui`
- [ ] Descriptor uses underscores for multi-word values (not hyphens)
- [ ] Lowercase throughout
- [ ] Fewer than 60 characters total

---

## 🔗 Related Standards

- **[_naming_conventions.md](_naming_conventions.md)** — Full segment reference
- **[_naming_infrastructure.md](_naming_infrastructure.md)** — VM and resource naming
