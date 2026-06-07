# 📋 provision_vm — Parameters

Full parameter reference for the VM provisioning skill. Present this table to the user with
pre-filled suggestions derived from their VM description. Wait for confirmation on every field.

---

## 📥 Parameters

| Parameter | Description | Default / suggestion |
|---|---|---|
| `REPO_PATH` | Local path to `pyrc-iac-tf` clone | `~/git_repos/infrastructure/eng/pyrc-iac-tf` |
| `ENV` | Target environment directory under `envs/`. **Discovered at runtime** — run `ls <REPO_PATH>/envs/` and present the list to the user. | (discovered) |
| `TIER` | Subdirectory under `apps/` for the chosen env. **Discovered at runtime** — run `ls <REPO_PATH>/envs/<ENV>/apps/` and present the list to the user. | (discovered) |
| `WORKLOAD_DIR` | Directory name under `apps/<TIER>/` — also used in the workspace entry (e.g. `dmt`). Check whether it already exists to determine Scenario A vs B. | (suggest from VM description) |
| `APPLICATION_OWNER` | Short ownership code for the team/system (e.g. `dmws`). Used in `application_owner` field and module name. | (suggest from VM description) |
| `ASSET_ROLE` | Describes what workload this VM runs (e.g. `dbt`, `abt`, `webserver`). Used in `asset_role` field and in the module block name (`module "instance_<APPLICATION_OWNER>_<ASSET_ROLE>"`). **Must be unique per instance file** in the target directory — always surface existing module names before asking the user to confirm this value. | (suggest from VM description) |
| `INSTANCE_SUFFIX` | Suffix for `instance_<suffix>.tf`. Follow the abbreviation convention used by sibling files (e.g. if sibling files use `dbt`, `abt`, use the same 3-letter style — not `instance_airbyte.tf` but `instance_abt.tf`). | (suggest from existing filenames) |
| `OS_TYPE` | Operating system: `ubuntu` or `windows` | `ubuntu` |
| `SEQUENTIAL_INDEX` | VM index number for naming (e.g. `"1"`) — quoted string | `"1"` |
| `COMPUTE_RESOURCES` | Compute size — see table below | (ask user to select) |
| `DISKS` | Disk configuration as HCL list (e.g. `[{ size = 40 }, { size = 50 }]`) | (suggest from similar VMs) |
| `PCI_SCOPE` | PCI scope: `out_of_scope`, `cardholder_data`, or `connected_to` | `out_of_scope` |
| `PATCH_GROUP` | Patch group: `a`, `b`, or `c` | `a` |

⚠️ **Branch naming constraint:** `WORKLOAD_DIR` must contain only lowercase letters, numbers, and
underscores (`[a-z0-9_]`) to comply with the branch naming convention. Flag and correct if not.

---

## ⚡ Compute sizes

Present this table when asking for `COMPUTE_RESOURCES`. Reference: `modules/payroc/compute/compute_resources.tf`

| Option | CPUs | Memory | Notes |
|---|---|---|---|
| `c_small` | 1 | 2 GB | Balanced |
| `m_small` | 1 | 4 GB | Memory optimised |
| `c_medium` | 2 | 4 GB | Balanced — typical Ubuntu default |
| `m_medium` | 2 | 8 GB | Memory optimised — typical Windows default |
| `c_large` | 4 | 8 GB | Balanced |
| `m_large` | 4 | 16 GB | Memory optimised |
| `c_xlarge` | 8 | 16 GB | Balanced |
| `m_xlarge` | 8 | 32 GB | Memory optimised |
| `c_xxlarge` | 16 | 32 GB | Balanced |
| `m_xxlarge` | 16 | 64 GB | Memory optimised |

---

## 🖥️ OS details

Set automatically based on `OS_TYPE`, but show to the user for confirmation:

| OS_TYPE | `os` | `os_edition` | `os_version` |
|---|---|---|---|
| `ubuntu` | `ubuntu` | `server` | `22.04` |
| `windows` | `windows` | `servercore` | `2022` |

---

## 🔍 golden_image_version detection

Do **not** ask the user for this value. Detect it automatically:

1. If Scenario A (new dir): list `<REPO_PATH>/envs/<ENV>/apps/<TIER>/` and pick the
   alphabetically first sibling directory; read the instance `.tf` file in that directory.
2. If Scenario B (existing dir): read an existing `instance_*.tf` in `<WORKLOAD_DIR>/`.
3. Extract the `golden_image_version` value and use it in the generated instance file.
