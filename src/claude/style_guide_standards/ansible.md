# 📦 Ansible Style Guide & Standards

Defines the team's standards for writing and structuring Ansible projects. Sourced from `pyrc-cac-ans`, the Payroc Engineering Ansible monorepo.

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`ansible/playbooks.md`](ansible/playbooks.md) | Playbook naming, folder structure, symlinks, CODEOWNERS, and tags |
| [`ansible/roles_and_tasks.md`](ansible/roles_and_tasks.md) | Role layout, capability categories, task conventions, and versioning |
| [`ansible/secrets_and_inventory.md`](ansible/secrets_and_inventory.md) | Vault secrets, dynamic inventory plugins, and scope layout |
| [`ansible/variables.md`](ansible/variables.md) | `l1`–`l6` group_vars hierarchy, precedence, and variable naming |

---

## 🗂️ Repo structure

```
group_vars/                         # variable files shared across all playbooks
  all.yml                           # global defaults and Vault lookups
  l1_<env>.yml                      # environment-wide variables
  l2_<env>_<site>.yml               # site-level within an environment
  ...                               # l3–l6 files as needed (see variables.md)
host_vars/                          # host-specific variable files
  <inventory_hostname>.yml
inventory/
  <scope>/                          # one subdirectory per inventory scope
    ansible.cfg                     # scope-specific configuration
    vars.yaml                       # scope metadata/variables
    <provider>_<account>_<plugin>.yml  # dynamic inventory plugin config
playbooks/
  <dept_or_app>/                    # one subdirectory per owner or application
    [<team>/]                       # optional team-level nesting
      <app>_<asset_role>_<descriptor>.yml
      group_vars -> ../../group_vars  # symlink
      roles -> ../../roles            # symlink
roles/
  <technical_capability>/           # functional grouping (e.g. application, systems)
    <role_name>/
      defaults/
        main.yml
      tasks/
        main.yml
      handlers/
      templates/
      files/
      meta/
filter_plugins/                     # custom Jinja2 filters
pipelines/                          # CI/CD pipeline definitions
```

- No `inputs/` directory — this repo does not use a config-driven YAML inputs pattern.
- No single root-level `ansible.cfg` — each inventory scope has its own (see `secrets_and_inventory.md`).
- No static `.ini` inventory files — all inventories use dynamic plugins.

---

## 🏷️ Naming conventions

| Construct | Convention | Example |
|-----------|------------|---------|
| Playbook files | `[app]_[asset_role]_[descriptor].yml` | `pyrc_ilb_setup.yml` |
| Role directories | `roles/[capability]/[role_name]` | `roles/systems/azure_devops_agent` |
| Inventory scope dirs | `[org]-[env]-[qualifier]` | `pyrc-prd-cde`, `pyrc-stg-dct` |
| Dynamic plugin files | `[provider]_[account/site]_[plugin].yml` | `aws_28122221233-aws_ec2.yml` |
| Variables in roles | `[role]_[variable_name]` | `webserver_port` |
| Variables in vars files | `[app/dept]__[role]_[variable_name]_[descriptor]` | `pyrc__nginx_port_http` |
| Task names | Sentence case, descriptive | `Install nginx package` |
| Tags | `snake_case` | `install`, `configure`, `restart` |

Use FQCN for all modules: `ansible.builtin.apt`, not `apt`.

---

## 🔩 Linting

- All YAML files must pass `yamllint --strict` before committing.
- All playbooks and roles must pass `ansible-lint` (production profile) before committing.
- Both are enforced via pre-commit hooks — fix the underlying issue rather than suppressing warnings.
- Ansible-lint skips: `role-name[path]`, `var-naming[no-role-prefix]`.

---

## 📥 Imports

@./ansible/playbooks.md
@./ansible/roles_and_tasks.md
@./ansible/secrets_and_inventory.md
@./ansible/variables.md
