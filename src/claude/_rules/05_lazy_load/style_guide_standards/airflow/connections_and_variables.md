# 🔐 Connections & Variables

**Purpose:** Establish naming and provisioning standards for Airflow connections and variables backed by Azure Key Vault.

Airflow is configured to use Azure Key Vault as its secrets backend (`airflow.cfg`). Secrets with the prefix `AF-CONNS-` are picked up as **connections**; secrets with prefix `AF-VARS-` are picked up as **variables**.

## 🔑 How it works

To use a connection or variable in code, strip the prefix, lowercase, and replace hyphens with underscores:

| AKV secret name | Used in code as |
|---|---|
| `AF-CONNS-DOCKER-DEFAULT` | `connection_id="docker_default"` |
| `AF-CONNS-DOCKER-CLOUDSMITH-DEFAULT` | `connection_id="docker_cloudsmith_default"` |
| `AF-VARS-SNOWFLAKE-ACCOUNT` | `Variable.get("snowflake_account")` |

## 📋 Contents

- [🔌 Connections](#-connections)
- [📦 Variables](#-variables)
- [🏗️ Provisioning](#-provisioning)
- [Related](#-related)

---

## 🔌 Connections

Secret naming pattern: `AF-CONNS-<TYPE>-<NAME>`

Common type prefixes:

| Type prefix | Used for |
|---|---|
| `AF-CONNS-DOCKER-<REGISTRY>` | Docker registry connections |
| `AF-CONNS-AIRBYTE-<NAME>` | Airbyte connections |
| `AF-CONNS-SNOWFLAKE-<ENV>-<AUTH>` | Snowflake connections (e.g., `KEY-PAIR-AUTH`) |

- **Reference location:** connection IDs are referenced in `includes/` utility functions — never hardcoded in `dag.py`

---

## 📦 Variables

Secret naming pattern: `AF-VARS-<NAME>`

- **Access pattern:** use `Variable.get("variable_name")` in `includes/` utilities only
- **Never in dag.py:** do not access variables directly in `dag.py`

---

## 🏗️ Provisioning

| Environment | Key Vault | Provisioning |
|---|---|---|
| DTE | `dmt-dte-uscn-dmt-kv` | Self-service — add directly |
| PROD | `dmt-prd-uscn-dmt-kv` | Raise a PlatOps ticket |
| UAT | `dmt-uat-uscn-oos-kv` | Raise a PlatOps ticket |

- **Note:** KV names above are infrastructure identifiers, not secrets — included here for provisioning reference only

## Related

- [Airflow Connections](https://payroc.atlassian.net/wiki/spaces/DA/pages/3038347265)
- [Airflow Variables](https://payroc.atlassian.net/wiki/spaces/DA/pages/3421929479)
- [AKV Naming Standard](https://payroc.atlassian.net/wiki/spaces/DA/pages/3556671573)
- [Secrets Backend](https://payroc.atlassian.net/wiki/spaces/DA/pages/3036774402)
