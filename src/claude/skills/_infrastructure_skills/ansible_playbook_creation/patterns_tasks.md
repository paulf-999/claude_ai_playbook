# ✅ Patterns — Task Authoring

## ✅ changed_when / failed_when — always explicit

Every `command` or `shell` task must declare both. Never rely on defaults.

```yaml
- name: Check service status
  ansible.builtin.command: systemctl is-active myapp
  register: svc_status
  changed_when: false      # read-only probe
  failed_when: false       # caller decides what to do with rc
```

---

## 🔄 Idempotency — check before change

Use pre-checks (register + `until`/`when`) to avoid re-running work that is already done.
Gate destructive or slow operations on the pre-check result.

```yaml
- name: Check if binary is already installed
  ansible.builtin.stat:
    path: /usr/local/bin/myapp
  register: myapp_stat

- name: Install binary
  ansible.builtin.get_url:
    url: "{{ myapp_url }}"
    dest: /usr/local/bin/myapp
  when: not myapp_stat.stat.exists
```

---

## 🧱 Complex operations — block/rescue

Use `block/rescue` whenever a task sequence has a long-running or partially-applied risk.
The `rescue` block must always call `ansible.builtin.fail` with a message that includes the
hostname and a remediation command.

```yaml
- name: Install application
  block:
    - name: Step 1 ...
    - name: Step 2 ...
  rescue:
    - name: Report failure
      ansible.builtin.debug:
        msg: "Installation failed on {{ inventory_hostname }}. Run 'app uninstall' to clean up."
    - name: Fail with actionable message
      ansible.builtin.fail:
        msg: "Run 'app uninstall' on {{ inventory_hostname }} before retrying."
```

---

## 📝 defaults/main.yml — documentation and safety rules

Three rules apply to every `defaults/main.yml`:

1. **Comment every non-obvious variable** — add a `# <purpose>` inline comment. Variables whose
   name makes their purpose self-evident (e.g. `app_port`, `app_version`) may be omitted, but
   anything relating to paths, timing, flags, or external addresses must be commented.

2. **Security-sensitive booleans default to the safe value** — override to the permissive value
   in group_vars per environment. Never ship a role where `insecure_*`, `skip_tls_*`, or
   equivalent flags default to `true`.

3. **Do not duplicate variables from a dependency role** — if your role depends on
   `install_<app>`, do not redeclare `<app>_version` or `<app>_download_url` in your own
   defaults. Reference the dependency's value directly. Duplicated defaults drift independently.

---

## 🔐 Cloudsmith registry authentication

Any role that pulls Docker images must authenticate with Cloudsmith before pulling. In SDX,
Docker Hub is directly accessible so images pull without auth. In STG and PRD, internet access
is blocked and Cloudsmith auth is enforced — the login task is required.

Add to `defaults/main.yml` using the standard credential variable pattern:

```yaml
<role>_docker_repo: third-party-software
<role>_docker_user: "{{ <role>_docker_repo }}"
<role>_docker_password: "{{ cloudsmith_third_party_entitlement_token }}"
```

`cloudsmith_third_party_entitlement_token` is Vault-backed via `group_vars/all.yml` — do not
redeclare it or hardcode it in the role.

Add the login task immediately before any `docker pull` loop or `docker_compose_v2` task:

```yaml
- name: Log in to Cloudsmith Docker registry
  community.docker.docker_login:
    registry: "{{ artifacts_docker_registry }}"
    username: "{{ <role>_docker_user }}"
    password: "{{ <role>_docker_password }}"
    reauthorize: false
  become: true
  no_log: true
```

- `reauthorize: false` — idempotent; skips re-auth if already logged in
- `no_log: true` — prevents the password appearing in task output

---

## 🔔 Handlers — limitation and liveness check pairing

Handlers only fire when a task reports `changed`. On an idempotent re-run (no tasks changed),
the handler will not trigger — leaving a service potentially not listening even if the play
completes without error.

For any task that configures a service and requires it to be reachable, pair the handler with
a post-config liveness check immediately after the task that starts or enables the service:

```yaml
- name: Check <app> is listening on expected port
  ansible.builtin.wait_for:
    host: 127.0.0.1
    port: "{{ app_port }}"
    timeout: 5
    state: started
  register: port_check
  ignore_errors: true

- name: Queue restart if port not up
  ansible.builtin.debug:
    msg: "<app> not listening on {{ app_port }} — queuing restart via handler"
  changed_when: true
  notify: Restart <app>
  when: port_check is failed

- name: Flush handlers
  ansible.builtin.meta: flush_handlers

- name: Verify <app> is listening after restart
  ansible.builtin.wait_for:
    host: 127.0.0.1
    port: "{{ app_port }}"
    timeout: 30
    state: started
  when: port_check is failed
```

Use `ignore_errors: true` on the initial probe so the play continues to the recovery path
rather than failing immediately. The final `wait_for` (no `ignore_errors`) is the hard gate —
if the port is still not up after the restart, the play fails with a clear message.
