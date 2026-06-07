# ✅ Workflow — README, Playbook, group_vars & Validate (Steps 1d–4)

## 📄 Step 1e — README.md

Required sections in order:

```markdown
# Role: <category>/<app>
<one-line description>

## Requirements
- <pre-requisite role> must run first

## Security note          ← include only if credentials are handled
<describe how credentials are passed and any residual risk>

## Required variables (no defaults — must be set in group_vars)
| Variable | Description |
|---|---|
| `app_vault_mount` | Vault KV2 mount point |
| `app_vault_secret` | Vault secret name |

## Key optional variables
| Variable | Default | Description |
|---|---|---|
| `app_port` | `8080` | Port the service listens on |

## DC3 override example
```yaml
# group_vars/l4_<env>_<org>_<qualifier>.yml
app_download_url: "{{ artifacts_generic_url }}/..."
```

## Usage
```yaml
roles:
  - role: systems/docker
  - role: <category>/<app>
```
```

---

## 📦 Step 2 — Playbook

Create `playbooks/<team>/<app>_setup.yml` — no vars block, no header comments.
Apply base playbook import first. List roles in dependency order, each with a tag.

---

## 🔍 Step 2b — Confirm inventory group exists

Before creating `group_vars`, verify the target group is present in the inventory.

```bash
cd ~/git_repos/infrastructure/eng/pyrc-cac-ans
ansible-inventory -i inventory/<scope>/ --graph 2>/dev/null | grep -q "<target_group>" \
  && echo "Group confirmed" \
  || echo "WARNING: <target_group> not found in inventory/<scope>/ — verify before proceeding"
```

If the group is not found: do not create `group_vars`. Surface the finding and ask the user
to confirm or correct the group name and inventory scope before continuing.

---

## 🗂️ Step 3 — group_vars

Create `group_vars/l4_<env>_<org>_<qualifier>.yml` for each target environment.

Always include:
- `prtg_lnx_proc_list` if the role installs a daemon
- `app_vault_mount` and `app_vault_secret`
- CloudSmith URL overrides for DC3

Use a comment with the PLATOPS ticket reference for any CloudSmith URLs pending provisioning:
```yaml
# CloudSmith mirrors — https://payroc.atlassian.net/servicedesk/customer/portal/99/PLATOPS-XXXX
```

---

## ✅ Step 4 — Validate

Run in order. Fix all issues before proceeding to PR.

```bash
# 1. Ansible lint (uses repo profile — excludes pipelines/)
ansible-lint roles/<category>/<app>/

# 2. YAML lint
yamllint --strict roles/<category>/<app>/defaults/main.yml
yamllint --strict roles/<category>/<app>/tasks/main.yml
yamllint --strict playbooks/<team>/<app>_setup.yml
yamllint --strict group_vars/l4_*.yml

# 3. Dry-run check (optional but recommended)
ansible-playbook playbooks/<team>/<app>_setup.yml --check --diff -i inventory/<env>/
```

Then invoke `/create_pr`.

---

## 🔎 Common lint failures and fixes

| Failure | Fix |
|---|---|
| `yaml[line-length]` | Wrap long strings with `>` or `>-` YAML block scalars |
| `fqcn[action]` | Add `ansible.builtin.` prefix to bare module names |
| `no-changed-when` | Add `changed_when: false` (or `true`) to command/shell tasks |
| `var-naming[no-role-prefix]` | Skip — this check is disabled in the repo ansible-lint config |
| `role-name[path]` | Skip — this check is disabled in the repo ansible-lint config |
