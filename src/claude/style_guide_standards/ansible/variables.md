# 📊 Ansible Variables

## 🗂️ group_vars hierarchy

Variables are organised into a 6-level hierarchy under `group_vars/` at the repo root. More specific levels override less specific ones (Ansible precedence applies).

| Level | File pattern | Scope |
|-------|-------------|-------|
| Global | `all.yml` | All hosts, all environments |
| L1 | `l1_<env>.yml` | Environment-wide (e.g. `l1_prd.yml`, `l1_stg.yml`) |
| L2 | `l2_<env>_<site>.yml` | Site within an environment (e.g. `l2_crp_ind.yml`) |
| L3 | `l3_<env>_<app>.yml` | Application within an environment (e.g. `l3_prd_pps.yml`) |
| L4 | `l4_<env>_<app>_<role>.yml` | Role within app/env (e.g. `l4_prd_pyrc_ilb.yml`) |
| L5 | `l5_<env>_<app>_<role>_<site>.yml` | Role at a specific site (e.g. `l5_prd_pyrc_ilb_ind.yml`) |
| L6 | `l6_<env>_<app>_<role>_<site>_<scope>.yml` | Most specific — scope within a site (e.g. `l6_prd_pyrc_ftp_ind_cde.yml`) |

Use the lowest level that satisfies the requirement — do not define variables at L4 if L1 is sufficient.

---

## 🔗 Symlinks in playbook directories

Each playbook directory symlinks to the root `group_vars/` so Ansible resolves the hierarchy correctly:

```bash
# Run once when creating a new playbook directory
# Adjust the relative path to match actual directory depth:
#   playbooks/<dept>/         → ../group_vars
#   playbooks/<dept>/<team>/  → ../../group_vars
ln -s <relative_path>/group_vars group_vars
ln -s <relative_path>/roles roles
```

Without these symlinks, group_vars and roles will not be resolved when the playbook is invoked from its own directory.

---

## 📝 Variable naming

### In role defaults (`roles/<cap>/<role>/defaults/main.yml`)

Prefix every variable with the role name:

```
[role_name]_[variable]
```

Examples: `nginx_port`, `nginx_ssl_cert_path`, `mysql_root_password`

### In group_vars files

Use the double-underscore pattern to namespace by application and role:

```
[app/dept]__[role]_[variable_name]_[descriptor]
```

Examples: `pyrc__nginx_port_http`, `dmt__mysql_backup_retention_days`

The double underscore (`__`) separates the application/department namespace from the role-level variable name. This avoids collisions across applications sharing the same role.

---

## 🖥️ host_vars

Host-specific variables go in `host_vars/<inventory_hostname>.yml`. The filename must exactly match the hostname as it appears in the dynamic inventory output.

Use `host_vars` only when a value genuinely differs per host and cannot be expressed at a group level. Prefer group_vars for consistency.

---

## 📌 Precedence reminder

When the same variable is defined at multiple levels, the most specific level wins. L6 > L5 > L4 > L3 > L2 > L1 > `all.yml`. `host_vars` always overrides `group_vars` at any level.
