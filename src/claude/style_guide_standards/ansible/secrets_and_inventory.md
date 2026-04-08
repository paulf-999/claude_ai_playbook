# 🔒 Secrets, Inventory & Config Inputs

## 🔑 Secrets management

- Never commit secrets or credentials. Use a `.env` file (git-ignored) populated from `.env_template`.
- Load secrets into Ansible facts via a dedicated `secrets_env` role using the `ansible.builtin.env` lookup.
- Always set `no_log: true` on tasks that read or set secret values.
- Always assert that required secrets are present and non-empty immediately after loading — fail with a descriptive message if missing.
- Provide a `.env_template` in the repo root documenting all required environment variables without values.

<details>
<summary>Click to expand — example <code>secrets_env</code> role tasks</summary>

```yaml
---
- name: Load required secrets from environment
  no_log: true
  ansible.builtin.set_fact:
    GIT_PAT_TOKEN: "{{ lookup('ansible.builtin.env', 'GIT_PAT_TOKEN') | default('', true) }}"

- name: Fail if required secrets are missing
  ansible.builtin.assert:
    that:
      - GIT_PAT_TOKEN | length > 0
    fail_msg: >
      Missing required env vars. Ensure .env exists (copied from .env_template) and is populated.
```

</details>

<details>
<summary>Click to expand — example <code>.env_template</code></summary>

```bash
# Copy this file to .env and populate with real values.
# Never commit .env.
GIT_PAT_TOKEN=
```

</details>

---

## 📦 Inventory

- One inventory directory per environment under `inventories/`.
- Use `.ini` format for inventory files. Include inline comments to explain host connection settings.
- Define `ansible_connection`, `ansible_python_interpreter`, and other connection parameters explicitly.
- Place group-level variables in `inventories/<env>/group_vars/` — do not embed them in the inventory file.

<details>
<summary>Click to expand — example <code>inventories/sandbox/inventory.ini</code></summary>

```ini
[sandbox]  # Docker-based sandbox host
sandbox_webserver ansible_connection=docker ansible_python_interpreter=/usr/bin/python3
```

</details>

---

## 🎛️ Config-driven inputs

- Externalise all run-time configuration into YAML files under `inputs/`.
- Playbooks and roles read from these files rather than accepting ad-hoc `--extra-vars`.

<details>
<summary>Click to expand — example <code>inputs/docker_config.yml</code></summary>

```yaml
docker:
  container_name: sandbox_webserver
  image: ubuntu:22.04
```

</details>
