---
name: ansible_playbook_creation
description: Guide the end-to-end development workflow for Ansible roles and playbooks in pyrc-cac-ans — design, implement, validate, and raise a PR.
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
tools: Bash, Read, Edit, Write, Glob, Grep
schema: skill_schema.yaml
---

## 🚦 Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| 📝 draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| 🔧 tactical | Main path + light error handling. No gold-plating. |
| 🚀 strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are guiding Ansible development in `pyrc-cac-ans`. Work through the phases below in order.
**Propose changes and wait for confirmation before writing any file.**

**Repo path:** `~/git_repos/infrastructure/eng/pyrc-cac-ans`

Apply all coding standards throughout — reference these pattern guides as needed:

- [patterns_security.md](patterns_security.md) — FQCN module naming · Vault-only secrets · env var credential passing
- [patterns_tasks.md](patterns_tasks.md) — `changed_when`/`failed_when` · idempotency · `block/rescue` · `defaults/main.yml` rules
- [patterns_structure.md](patterns_structure.md) — DC3 CloudSmith URLs · PRTG hook · `group_vars` naming · playbook structure

---

## 🔍 Pre-check — understand the work

Before designing anything, establish:

1. **Scope** — New role from scratch, or extending/modifying an existing one?
2. **Target** — Which inventory group and hosts? Which environment(s) (prd, sdx, stg)?
3. **Application** — What is being deployed or configured? What does "done" look like?
4. **Dependencies** — Which existing roles are required first (e.g. `systems/docker`)?
5. **Secrets** — Are credentials needed? If so, which Vault mount and secret path?
6. **DC3** — Are the target hosts in DC3? (determines whether CloudSmith URL overrides are required)
7. **Disk capacity** — Does the target host need root partition expansion before the role runs? (VMs provisioned at 50GB default to ~20GB usable — add `provisioning/disk_operations` as a pre-step if Docker or large application stacks will consume disk)
8. **Image pull cost** — Will the role pull large or multiple Docker images from CloudSmith?
9. **Image tag mutability** — Are image tags immutable (pinned version or digest) or mutable (floating tags such as `latest`)? Determines the safe pull strategy for compose up tasks.
10. **Registry auth** — Does the role pull images from Cloudsmith? In SDX, Docker Hub is directly accessible and no auth is needed. In STG and PRD, internet access is blocked and Cloudsmith auth is enforced — add a `community.docker.docker_login` task before any `docker pull` or `docker_compose_v2` task.

Do not proceed until all ten points are established.

---

## 🏛️ Phase 1 — Design

Outline the approach before writing any code. Cover:

- **Role structure**: which files are needed (`defaults`, `tasks`, `handlers`, `templates`?)
- **Variable split**: what belongs in `defaults/main.yml` vs `group_vars/`?
- **Idempotency**: how is each task safe to re-run? (stat checks, `when:` guards, `block/rescue`)
- **Async steps**: does any task need `async`/`poll` + `async_status`?
- **Image pull strategy**: if the role pulls large or multiple Docker images from CloudSmith, include a `pre_tasks` pre-pull phase with `docker image inspect` cache checks to avoid repeat pulls.
- **Compose up resilience**: add `retries: 3` / `delay: 5` to `docker_compose_v2` tasks to guard against transient registry failures; use `pull: missing` rather than `pull: always` only when image tags are immutable and a pre-pull phase manages freshness — avoids re-pulling images already cached. Use `pull: always` if tags are mutable.
- **Partial install recovery**: are there intermediate states to detect before deciding to skip or re-run? (e.g. a process running but a dependent component missing — check the component, not just the parent process)
- **Retry strategy**: if the install fails, what is the automated recovery path? (uninstall → wait for pod/process termination → retry install; or halt and require manual intervention?) Prefer automatic recovery where the tool is idempotent.
- **Rescue block content**: surface logs inline (not just a file path); include in-cluster diagnostics (port bindings, relevant pod logs, events); do **not** auto-uninstall in rescue — preserve state for investigation; use `failed_when: false` on all diagnostic tasks so a missing resource does not mask the real error.

Present the design and wait for confirmation before implementing.

---

## 🏗️ Phase 2 — Implement

Follow these guides in order:

- [workflow_scaffold.md](workflow_scaffold.md) — role init, `defaults/main.yml`, `tasks/main.yml`, `handlers/main.yml`
- [workflow_completion.md](workflow_completion.md) — README, playbook, `group_vars`, validate + lint fixes

---

## ✅ Phase 3 — Validate

```bash
cd ~/git_repos/infrastructure/eng/pyrc-cac-ans
ansible-lint roles/<category>/<app>/
yamllint --strict playbooks/<team>/<name>_setup.yml
yamllint --strict group_vars/l4_*.yml
```

Fix all issues, then invoke `/git_create_pr`.

---
