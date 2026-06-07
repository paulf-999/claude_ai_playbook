# 🏗️ Patterns — File and Repo Structure

## 📦 DC3 artefact URLs — CloudSmith mirror

DC3 VMs cannot reach the internet. All download URLs must use the internal CloudSmith mirror by
default. Set `app_download_url` in `defaults/main.yml` to the `artifacts_generic_url` path; add
the public upstream URL as a commented fallback for reference only.

```yaml
# defaults/main.yml — default to internal mirror; public URL is a reference only
app_version: "1.2.3"
# Public upstream: https://upstream.example.com/app-{{ app_version }}.tar.gz
app_download_url: "{{ artifacts_generic_url }}/myteam/myapp/{{ app_version }}/app-{{ app_version }}.tar.gz"
```

If the CloudSmith mirror is not yet provisioned, set the public URL as a temporary default and
add a comment referencing the PLATOPS ticket:

```yaml
# TODO: switch to CloudSmith mirror once provisioned — PLATOPS-XXXX
app_download_url: "https://upstream.example.com/app-{{ app_version }}.tar.gz"
```

---

## 📊 PRTG monitoring hook

For any role that installs a long-running process, add a `prtg_lnx_proc_list` entry to the
environment group_vars so PRTG can monitor the process automatically.

```yaml
# group_vars/l4_<env>_<team>_<qualifier>.yml
prtg_lnx_proc_list:
  - name: myprocessd
```

---

## 🗂️ group_vars naming

Use the `l4_<env>_<team>_<qualifier>.yml` pattern for application-specific overrides.

| Segment | Meaning | Example |
|---|---|---|
| `l4` | fourth variable precedence tier | `l4` |
| `<env>` | environment code | `prd`, `sdx`, `stg` |
| `<team>` | playbook team namespace — matches `playbooks/<team>/` | `ddp`, `dmt`, `pyrc` |
| `<qualifier>` | 2-3 letter application code | `abt` (Airbyte), `afl` (Airflow) |

Example: `l4_prd_ddp_abt.yml` — production DDP Airbyte vars (playbook at `playbooks/ddp/`).

The `<team>` segment aligns with the playbook directory, not the broader Payroc org code — use
`ddp` for DDP playbooks, `dmt` for Data Management playbooks, `pyrc` only for cross-team
playbooks living directly under `playbooks/pyrc/`.

---

## 🗒️ Playbook structure

```yaml
---
- name: Include base playbook
  ansible.builtin.import_playbook: ../pyrc/base.yml

- name: <App> Deployment
  hosts: all
  gather_facts: true
  become: true

  roles:
    - role: systems/docker          # dependencies first
      tags: [docker]
    - role: application/<cat>/<app>
      tags: [<app>]
```

No `vars:` block in the playbook — all variables belong in `defaults/main.yml` or `group_vars/`.

**Tag naming:** use the role's short application name in lowercase (e.g. `airbyte`, `abctl`,
`docker`). Tags must be documented in the playbook README or inline comment — do not introduce
undocumented tags. Where an existing tag from the repo's tag vocabulary applies (e.g. `docker`,
`install`), prefer it over a new one.
