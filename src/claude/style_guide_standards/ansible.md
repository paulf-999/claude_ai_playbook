# 📦 Ansible Style Guide & Standards

Defines the team's standards for writing and structuring Ansible projects. Informed by [payroc/dmt-cac-ansible_sandbox](https://github.com/payroc/dmt-cac-ansible_sandbox).

---

## 📋 Child pages

| File | Purpose |
|------|---------|
| [`ansible/playbooks.md`](ansible/playbooks.md) | Playbook structure, role references, tags, and examples |
| [`ansible/roles_and_tasks.md`](ansible/roles_and_tasks.md) | Role structure, defaults, task conventions, and examples |
| [`ansible/secrets_and_inventory.md`](ansible/secrets_and_inventory.md) | Secrets management, inventory layout, and config-driven inputs |

---

## 🗂️ Repo structure

```
ansible.cfg                     # project-level Ansible configuration
inputs/                         # config-driven input files (YAML)
inventories/
  <environment>/                # one subdirectory per environment (sandbox, dev, uat, prod)
    inventory.ini               # host definitions
    group_vars/                 # group-level variable files
playbooks/
  site.yml                      # top-level playbook
roles/
  <role_name>/
    defaults/
      main.yml                  # default variable values
    tasks/
      main.yml                  # task entry point
    handlers/                   # (if needed)
    templates/                  # Jinja2 templates (if needed)
    files/                      # static files (if needed)
src/                            # supporting scripts and utilities
docs/                           # project documentation
```

- One inventory directory per environment — never share inventory files across environments.
- All configurable inputs live in `inputs/` as YAML files, keeping playbooks free of hardcoded values.

---

## ⚙️ ansible.cfg

Every project must have an `ansible.cfg` at the repo root. At minimum, define:

```ini
[defaults]
inventory  = inventories/<default_env>/inventory.ini
roles_path = ./roles
```

Explicitly setting `roles_path` ensures roles are resolved from the project root regardless of where Ansible is invoked.

---

## 🏷️ Naming conventions

| Construct | Convention |
|-----------|------------|
| Roles | `snake_case` |
| Variables | `snake_case` |
| Playbook files | `snake_case.yml` |
| Inventory files | `inventory.ini` |
| Task names | Sentence case, descriptive — every task must have a `name` |
| Tags | `snake_case` or `kebab-case`, consistent within a project |

Use fully qualified collection names (FQCN) for all modules: `ansible.builtin.apt`, not `apt`. This avoids ambiguity as collections grow.

---

## 🔩 Linting

- All YAML files must pass `yamllint` before committing. The canonical config is `.yamllint` at the repo root.
- All playbooks and roles must pass `ansible-lint` before committing.
- Both are enforced via pre-commit hooks — fix the underlying issue rather than suppressing warnings.

---

## 📥 Imports

@./ansible/playbooks.md
@./ansible/roles_and_tasks.md
@./ansible/secrets_and_inventory.md
