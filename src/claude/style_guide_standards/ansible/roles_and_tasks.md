# 🔧 Ansible Roles & Tasks

## 🗂️ Role layout

Roles live under `roles/[technical_capability]/[role_name]/`. The capability directory is a functional grouping — choose the closest fit:

| Capability | Covers |
|------------|--------|
| `application` | Application-specific installation and configuration |
| `backups` | Backup agents and configuration |
| `database` | Database engines and clients |
| `networks` | Networking, load balancers, firewall rules |
| `observability` | Monitoring agents, logging, alerting |
| `provisioning` | VM bootstrapping and base configuration |
| `security` | Hardening, certificates, secret agents |
| `systems` | OS-level configuration, system utilities, CI/CD agents |
| `www` | Web servers and reverse proxies |

Each role must follow the standard subdirectory structure — `tasks/` and `defaults/` are the minimum required:

```
roles/
  <capability>/
    <role_name>/
      defaults/
        main.yml    # default variable values (all variables the role accepts)
      tasks/
        main.yml    # task entry point
      handlers/     # (if needed)
      templates/    # Jinja2 templates (if needed)
      files/        # static files (if needed)
      meta/         # role metadata and dependencies
```

Create new roles with:

```bash
ansible-galaxy role init --offline <role_name>
```

---

## 📌 Role versioning

- `main` is the current stable version of every role.
- When a breaking change is introduced that requires callers to update, create a short-lived branch with a `_BREAKINGCHANGE` suffix (e.g. `feature/my_role_BREAKINGCHANGE`) to stage the transition.
- Callers must migrate before the branch is merged. Do not leave `_BREAKINGCHANGE` branches open indefinitely.

---

## 🔤 Variable naming

- Within a role: prefix every variable with the role name — `[role_name]_[variable]` (e.g. `webserver_port`, `nginx_ssl_cert_path`).
- `defaults/main.yml` must define and comment every variable the role accepts. No undocumented variables.

---

## ✅ Task standards

- Every task must have a `name` in sentence case describing what it does.
- Use FQCN for all modules (`ansible.builtin.*`, `community.*`, etc.).
- Assert required variables are defined and non-empty at the start of a role — fail fast with a clear message.
- Use `no_log: true` on any task that handles secrets or sensitive values.
- Roles must be self-contained and reusable — no hardcoded environment-specific values inside a role.

<details>
<summary>Click to expand — example <code>tasks/main.yml</code></summary>

```yaml
---
- name: Assert required vars are provided
  ansible.builtin.assert:
    that:
      - webserver_port is defined
      - webserver_port | int > 0
    fail_msg: "webserver_port must be defined and non-zero."

- name: Install nginx package
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy nginx configuration
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: "0644"
  notify: Restart nginx
```

</details>
