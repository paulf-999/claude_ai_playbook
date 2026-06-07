---
name: provision_vm
description: >
  Provision a new VM in pyrc-iac-tf via the two-PR Scalr workflow — workspace
  entry PR first, VM Terraform config PR second. Also supports adding a second
  VM instance file to an existing workload directory. Supports Ubuntu and Windows.
  Invoke as /provision_vm to start from scratch, or /provision_vm phase2 to skip
  directly to the VM config PR after the workspace PR has been merged.
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
tools: Bash, Read, Edit, Glob, Write
---

## 🚦 Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| 📝 draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| 🔧 tactical | Main path + light error handling. No gold-plating. |
| 🚀 strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are executing a VM provisioning workflow in `pyrc-iac-tf` via Scalr. Work through the phases
below in order. Show proposed file changes and wait for explicit confirmation before writing
anything or raising any PR.

**🏗️ Background:** Scalr is Payroc's Terraform automation platform. It monitors directories in
`pyrc-iac-tf` and runs `plan`/`apply` automatically when changes are merged. Before a VM directory
can be deployed, a workspace must exist that maps to it — hence the two-PR sequence.

**📂 Two supported scenarios:**
- **New VM, new workload directory** — full two-PR flow: workspace entry PR (Phase 1) then VM config PR (Phase 2, Scenario A)
- **Second VM in an existing workload directory** — VM config PR only (Phase 2, Scenario B); workspace already registered

---

## ⚠️ Pre-check — gather parameters and verify environment

### 🙋 Step 1 — Ask what the VM is for

Ask the user one open question first:

> "What is this VM for? (e.g. 'a dbt docs web server for the DM team', 'an Airbyte sandbox VM')"

### 📋 Step 2 — Collect and confirm parameters

Use the answer to derive suggested values. See [parameters.md](parameters.md) for the full
parameter table, compute sizes, and OS defaults — present these to the user with pre-filled
suggestions and wait for confirmation. Do not proceed until all parameters are confirmed.

### 🔍 Step 3 — Verify environment

Run the following checks. Stop and report if any fail:

1. `git -C <REPO_PATH> status` — verify the repo exists and the working tree is clean.
2. Discover available environments: `ls <REPO_PATH>/envs/` — present the list to the user
   to confirm `ENV`. Do not accept a hardcoded value without showing the actual directories.
3. Once `ENV` is confirmed, discover available tiers: `ls <REPO_PATH>/envs/<ENV>/apps/` —
   present the list to the user to confirm `TIER`.
4. Confirm `<REPO_PATH>/envs/<ENV>/apps/workspaces.tfvars` exists.
5. `gh auth status` — verify GitHub CLI is authenticated.

If invoked as `/provision_vm phase2`, skip Phase 1 and go directly to Phase 2 once parameters
are confirmed. Still work through Steps 1–3 first; the skill has no memory of prior invocations.

---

## 🏗️ Phase 1 — Workspace PR

Add an entry to `workspaces.tfvars` to register the new VM directory as a Scalr workspace, then
raise a PR for DevOps review.

See [phase1.md](phase1.md) for the full step sequence — diff preview, branch creation, commit,
push, and PR body.

---

## 🖥️ Phase 2 — VM Config PR

Create the Terraform configuration for the new VM under `envs/<ENV>/apps/<TIER>/<WORKLOAD_DIR>/`.
Phase 2 handles two scenarios automatically:

- **Scenario A** — WORKLOAD_DIR does not exist: create directory, copy boilerplate, generate instance file
- **Scenario B** — WORKLOAD_DIR already exists: generate instance file only, detect and omit duplicate `module "compute"` blocks, surface existing module names to prevent naming clashes

See [phase2.md](phase2.md) for the full step sequence.

---

## 🚨 Error handling

| Situation | Action |
|---|---|
| 🔴 Any `git` command fails | Stop immediately. Report the full error. Do not attempt recovery. |
| 🔴 `gh pr create` fails with 422 | Report the existing PR URL and stop. |
| 🟡 File already exists at the target path (Scenario A) | Stop and ask the user whether to overwrite. Do not overwrite silently. |
| 🟡 `workspaces.tfvars` already has entry for `<TIER>/<WORKLOAD_DIR>` | Report it and ask whether to proceed. |

---

> 🔵 TODO (tactical): validate `WORKLOAD_DIR` does not already exist as a directory in the target tier before starting Phase 1 (workspace PR).
> 🔵 TODO (tactical): add `--label` to PRs once the correct label set for pyrc-iac-tf is confirmed.
> 🔵 TODO (strategic): extend Windows support fully once the provisioning guide is documented.
