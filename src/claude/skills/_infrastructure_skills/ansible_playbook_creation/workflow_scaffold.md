# 🏗️ Workflow — Role Scaffold (Steps 1a–1c)

## 🏗️ Step 1a — Initialise role

```bash
cd ~/git_repos/infrastructure/eng/pyrc-cac-ans
ansible-galaxy role init --offline roles/<category>/<app>
```

Category conventions: `application`, `systems`, `database`, `security`, `observability`.

> 🏷️ **DM team:** roles live under `roles/application/ddp/<app>/` — `ddp` is the DM team's directory qualifier. Check `roles/application/ddp/` for an existing role before creating a new one.

---

## 📝 Step 1b — defaults/main.yml

Structure: header comment → config variables → Vault path placeholders (empty strings only).

```yaml
---
# Role: <category>/<app>
# Purpose: one-line description

# Core config
app_version: "1.2.3"
app_install_dir: /pyrc/<app>
app_port: 8080

# Download URL — default to internal mirror; see patterns_structure.md for DC3 guidance
# Public upstream: https://upstream.example.com/app-{{ app_version }}.tar.gz
app_download_url: "{{ artifacts_generic_url }}/myteam/myapp/{{ app_version }}/app-{{ app_version }}.tar.gz"

# Vault paths — intentionally empty; set in group_vars per environment.
# DM team conventions: mount = "dmt-kv-app-secrets"
#                      secret = "dmt-{{ deployment_environment }}-<service>-creds-login"
app_vault_mount: ""
app_vault_secret: ""

# Populated at runtime from Vault — do not set here.
app_admin_user: ""
app_admin_password: ""
```

---

## ✅ Step 1c — tasks/main.yml

Structure: pre-flight asserts → install/deploy → post-deploy verify.

```yaml
---
# Role tasks: <category>/<app>

- name: Assert Vault credential variables are configured
  ansible.builtin.assert:
    that:
      - app_vault_mount | length > 0
      - app_vault_secret | length > 0
    fail_msg: >
      app_vault_mount and app_vault_secret must be set in group_vars.

# ... install tasks ...

- name: Fetch credentials from Vault
  no_log: true
  ansible.builtin.set_fact:
    app_admin_password: >-
      {{ lookup('community.hashi_vault.vault_kv2_get',
         app_vault_secret,
         engine_mount_point=app_vault_mount)['secret']['password'] }}

- name: Assert credentials were fetched
  ansible.builtin.assert:
    that:
      - app_admin_password | length > 0
    fail_msg: >-
      Failed to fetch credentials from Vault:
      {{ app_vault_mount }}/{{ app_vault_secret }}
```

---

## 🔔 Step 1d — handlers/main.yml

Create `roles/<category>/<app>/handlers/main.yml`. Add handlers for any service restart or reload triggered by config changes.

```yaml
---
# Systemd variant (non-Docker roles):
- name: Restart <app>
  ansible.builtin.systemd:
    name: <app>
    state: restarted
    daemon_reload: true
  become: true

# Docker Compose variant:
- name: Restart <app> stack
  community.docker.docker_compose_v2:
    project_src: "{{ app_install_dir }}"
    state: restarted
  become: true
```

> ⚠️ **Handler limitation:** handlers only fire when a task reports `changed`. On an idempotent
> re-run (no files changed), the handler will not trigger — leaving a service potentially not
> listening even if the role completes without error. For service availability checks (ports,
> health endpoints), pair the handler with a post-config liveness check.
> See [patterns_tasks.md](patterns_tasks.md) → *Handlers — limitation and liveness check pairing*.
