# 📋 Ansible Playbooks

## 🏷️ Naming convention

Playbook files follow the pattern: `[app]_[asset_role]_[descriptor].yml`

| Segment | Meaning | Example values |
|---------|---------|----------------|
| `app` | Application or department code | `pyrc`, `dmt`, `mobileaxept` |
| `asset_role` | Functional role of the target asset | `ilb`, `web`, `db`, `agent` |
| `descriptor` | Short description of what the playbook does | `setup`, `configure`, `upgrade` |

Examples: `pyrc_ilb_setup.yml`, `pyrc_web_configure.yml`

---

## 🗂️ Folder structure

Playbooks live under `playbooks/` organised by owner or application, with optional team nesting:

```
playbooks/
  <dept_or_app>/            # e.g. pyrc/, dev_ops/, obs/
    [<team>/]               # optional — e.g. dpe/, dba/
      <playbook>.yml
      group_vars -> ../../group_vars   # symlink — required
      roles -> ../../roles             # symlink — required
```

Each playbook directory must contain symlinks to the root `group_vars/` and `roles/` directories so Ansible resolves variables and roles correctly regardless of where the playbook is invoked. Adjust the relative path to match the actual directory depth — see [variables.md](variables.md) for the full symlink guidance.

---

## 🔖 CODEOWNERS

When adding a new playbook directory, update `.github/CODEOWNERS` with the appropriate owner. Ownership follows the directory structure — the team or individual responsible for that application or domain owns the subdirectory.

---

## 🏷️ Tags

Apply tags at the task, block, or play level to allow selective execution. Standard operational tags:

| Tag | When to use |
|-----|-------------|
| `install` | Package or software installation |
| `configure` | Configuration file management |
| `restart` | Service restarts |
| `uninstall` | Package or software removal |
| `upgrade` | Version upgrades |

Tags are `snake_case`. Apply them consistently within a playbook — tasks of the same type should share the same tag.

```bash
# Run only configuration tasks
ansible-playbook playbooks/pyrc/pyrc_ilb_setup.yml --tags configure

# Skip installation tasks
ansible-playbook playbooks/pyrc/pyrc_ilb_setup.yml --skip-tags install
```

---

## ⚙️ Play standards

- Set `gather_facts` and `become` explicitly on every play — do not rely on defaults.
- Reference roles by their full path: `role: systems/azure_devops_agent`, not `role: azure_devops_agent`.
- Comment each role reference briefly where its purpose is not obvious from the name.
