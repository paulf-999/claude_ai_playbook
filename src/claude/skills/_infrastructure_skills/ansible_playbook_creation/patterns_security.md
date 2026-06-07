# 🔐 Patterns — Security & Module Naming

## 🔤 Module naming — FQCN always

Use fully-qualified collection names on every task. No shorthand.

```yaml
# Correct
ansible.builtin.command: docker ps
community.hashi_vault.vault_kv2_get: ...

# Wrong
command: docker ps
```

---

## 🔐 Secrets — Vault only, never CLI args

All credentials come from Vault at runtime via `community.hashi_vault.vault_kv2_get`. Never
hardcode, never pass on the command line, never store in group_vars or defaults.

```yaml
- name: Fetch credentials from Vault
  no_log: true
  ansible.builtin.set_fact:
    app_password: >-
      {{ lookup('community.hashi_vault.vault_kv2_get',
         vault_secret,
         engine_mount_point=vault_mount)['secret']['password'] }}
```

When a CLI tool does not support stdin/file input for credentials, use `environment:` to pass
them as env vars. This avoids process-list exposure. Document the residual `/proc/<pid>/environ`
risk in both an inline comment and the role README.

```yaml
- name: Set credentials via CLI
  ansible.builtin.shell: app-cli --password "${APP_PASSWORD}"
  args:
    executable: /bin/bash
  environment:
    APP_PASSWORD: "{{ app_password }}"
  register: set_creds_result
  no_log: true
  changed_when: true
  failed_when: set_creds_result.rc != 0
```

If this task is inside a `block/rescue`, the rescue block handles failures — `failed_when` may be
omitted or set to `false` with a comment explaining that the rescue will surface the error.
