# 🔐 Ansible Secrets & Inventory

## 🔑 Secrets — HashiCorp Vault

No secrets are stored in this repo. All credentials are retrieved at runtime from HashiCorp Vault using the `community.hashi_vault.vault_kv2_get` lookup plugin.

Vault lookups are declared in `group_vars/all.yml` so they are available to all playbooks:

```yaml
# group_vars/all.yml
my_service_password: >-
  {{ lookup('community.hashi_vault.vault_kv2_get',
     'secret/my_service',
     token=vault_token)['data']['password'] }}
```

- Never hardcode credentials, tokens, or passwords anywhere in the repo.
- Never log secret values — use `no_log: true` on tasks that consume them.
- If a credential must be passed as a variable, ensure it originates from a Vault lookup, not a defaults file or plain vars file.

---

## 🔒 Secrets passed to external tools

When a secret or sensitive value must be passed to an external CLI tool (`kubectl apply`, `helm upgrade --values`, etc.), pipe it via `stdin` rather than writing it to a file on the target host. Writing credentials to disk — even to a temp file — risks leaving them behind if the task fails mid-execution.

```yaml
- name: Apply credentials secret
  ansible.builtin.shell: |    # shell required — heredoc (<<EOF) is a shell feature
    kubectl apply -f - <<EOF
    apiVersion: v1
    kind: Secret
    ...
    EOF
  no_log: true
  register: result
  changed_when: "'configured' in result.stdout or 'created' in result.stdout"
```

For `helm upgrade --values`, pass values inline using `--set` flags or pipe a rendered template via `--values -` (stdin). Never write a values file containing secrets to the target host filesystem.

---

## 🗃️ Inventory layout

Inventories are organised under `inventory/` with one subdirectory per scope:

```
inventory/
  <org>-<env>-<qualifier>/        # e.g. pyrc-prd-cde, pyrc-stg-dct, tech_ops-crp
    ansible.cfg                   # scope-specific Ansible configuration
    vars.yaml                     # scope metadata and variables
    <provider>_<account>_<plugin>.yml  # dynamic inventory plugin config
```

Each scope directory is self-contained — its `ansible.cfg` sets the inventory path, roles path, and filter_plugins path for that scope.

---

## ⚙️ ansible.cfg per scope

Each `inventory/<scope>/ansible.cfg` must contain three sections. Use an existing scope as a reference template — do not build one from scratch.

```ini
[defaults]
host_key_checking = False
inventory      = <absolute_path_to_this_scope_dir>
roles_path     = <absolute_path_to_repo_root>/roles
filter_plugins = <absolute_path_to_repo_root>/filter_plugins

[hashi_vault_collection]
auth_method  = token
namespace    = admin/<scope>-ns-secretstore
mount_point  = pyrc-kv-ansible
url          = https://<vault_cluster_url>:8200
token_file   = vault-token-via-agent
token_path   = /opt/hcp/token

[inventory]
cache            = True
cache_plugin     = jsonfile
cache_timeout    = 300
cache_connection = <cache_dir>
```

There is no root-level `ansible.cfg`. All configuration is scope-scoped.

---

## 🔌 Dynamic inventory plugins

All inventory uses dynamic plugins — no static `.ini` files. Plugin config files are named:

```
[provider]_[account/site]_[plugin].yml
```

| Provider prefix | Plugin type | Example filename |
|-----------------|-------------|-----------------|
| `aws` | AWS EC2 | `aws_28122221233-aws_ec2.yml` |
| `azu` | Azure RM | `azu_3aa06344-c271-4c9a-9cfd-e29dd9e99fe6-azure_rm.yml` |
| `vca` | VMware vCenter | `vca_lon_prd_vdc_vmware.yml` |

Each plugin YAML file contains only the configuration for that cloud provider and account — no host lists, no credentials.
