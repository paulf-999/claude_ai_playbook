# 🏷️ Claude Component Tag Schema

Version: 0.1.0
Status: draft
Last reviewed: 2026-04-10

This document defines the YAML frontmatter tag schema for all Claude components —
skills, process docs, rules files, and CLAUDE.md files. Tags power three things:
the lint-style merge check, the component audit, and the quality report.

---

## 📋 Full example

```yaml
---
name: vm-provisioning
description: Automates internet engineering VM provisioning process. Use when...
version: 0.1.0
maturity: draft
tags:
  criticality: should
  domain: infra
  status: active
  tested: false
  owner: internet-engineering
  depends-on:
    - auth-helper
    - network-validator
  last-reviewed: 2026-04-10
---
```

---

## ✅ Tier 1 — Mandatory tags

These must be present on every Claude component. The merge lint check fails if
any are missing or contain invalid values.

### 🎯 `maturity`

Scope intent for the current iteration. Controls what Claude is allowed to do
when working on this component.

| Value | Meaning | Claude behaviour |
|---|---|---|
| `draft` | Exploring the problem space | Happy path only. Log gaps as TODOs, don't solve them. No refactoring. |
| `tactical` | Solves the known use case reliably | Main path + light error handling. No gold-plating. |
| `strategic` | Production-ready, generalised | Full coverage, edge cases, documentation, evals expected. |

Version alignment: `0.x.x` = draft, `1.x.x` = tactical, `2+.x.x` = strategic.

---

### ⚡ `criticality`

How important is this component to the Claude setup? Uses MoSCoW.

| Value | Meaning |
|---|---|
| `must` | Core to the Claude setup functioning. Absence causes real problems. |
| `should` | Important and expected, but a workaround exists. |
| `could` | Adds value but genuinely optional. |
| `want` | Nice to have. Low priority. |

Used by: audit report (surfaces must/should components that are dormant or untested).

---

### 🔄 `status`

Current operational state of the component.

| Value | Meaning |
|---|---|
| `active` | In use and maintained. |
| `dormant` | Exists but not being used. May be intentional (future use) or accidental. |
| `deprecated` | Superseded. Should be removed or archived. |
| `wip` | Actively being built. Not yet usable. |

The audit report flags components where `status: dormant` but `criticality: must` or `should` —
this is the primary signal for "intended but not used" components.

---

### 🧪 `tested`

Whether the component has any test coverage (eval cases, test prompts, or automated checks).

| Value | Meaning |
|---|---|
| `true` | At least one test case exists and has been run. |
| `false` | No test coverage. |

The quality report penalises `tested: false` on components with `criticality: must` or `should`.

---

## 💡 Tier 2 — Optional tags

These enrich the audit and quality reports but are not lint-checked on merge.
Strongly recommended for any component with `criticality: must` or `should`.

### 🗂️ `domain`

Functional area the component belongs to. Used for grouping in reports.

Suggested values (extend as needed):
- `infra` — provisioning, environments, CI
- `security` — auth, secrets, access control
- `dx` — developer experience, tooling
- `reporting` — audits, dashboards, quality
- `process` — workflows, runbooks
- `comms` — internal communications, templates

---

### 👤 `owner`

Team or individual responsible for maintaining this component.

```yaml
owner: internet-engineering
# or
owner: platform-team
# or
owner: jane.doe
```

---

### 🔗 `depends-on`

List of other Claude component names this component calls or relies on.
Used by the audit to surface broken dependency chains —
e.g. an `active` component depending on a `dormant` one.

```yaml
depends-on:
  - auth-helper
  - network-validator
```

Values should match the `name` field in the dependency's frontmatter exactly.

---

### 📅 `last-reviewed`

ISO 8601 date of the last deliberate human review of this component.
Distinct from the last git commit date — this is a conscious "yes, this is
still correct and relevant" sign-off.

```yaml
last-reviewed: 2026-04-10
```

The audit report flags components not reviewed in the last 90 days (configurable).

---

## 🔩 Applying tags to non-skill components

Not every Claude component is a SKILL.md. Apply the same frontmatter convention to:

| Component type | File | Notes |
|---|---|---|
| Skills | `SKILL.md` | Natural fit — frontmatter already used for `name` and `description`. |
| Process docs | `process-name.md` | Add frontmatter block at top. |
| Rules files | `RULES.md` or `.claud/rules/*.md` | Add frontmatter block at top. |
| CLAUDE.md files | `CLAUDE.md` | Treat as a component in its own right. |
| Best practices pages | `best-practices/*.md` | Tag each page individually. |

---

## 🔍 Tag validation rules (for lint check)

The merge lint check enforces the following:

```
FAIL  if maturity is missing or not in [draft, tactical, strategic]
FAIL  if criticality is missing or not in [must, should, could, want]
FAIL  if status is missing or not in [active, dormant, deprecated, wip]
FAIL  if tested is missing or not in [true, false]
WARN  if criticality is must/should and tested is false
WARN  if depends-on references a component name that does not exist
WARN  if last-reviewed is absent and criticality is must/should
WARN  if last-reviewed is older than 90 days
```

`FAIL` blocks merge. `WARN` appears in the CI summary but does not block.

---

## 🌱 Tag rot prevention

Tags are only useful if they stay accurate. A few practices help:

1. **The lint check ensures presence, not accuracy.** Accuracy is the owner's responsibility.
2. **Update `last-reviewed` deliberately** — not automatically on commit. It should mean "a human looked at this and confirmed it's still right."
3. **The weekly audit surfaces drift** — components where `status: active` but no recent usage signals, or `tested: true` but no test files found.
4. **Deprecate don't delete** — when retiring a component, set `status: deprecated` and leave it for one audit cycle before removal. This gives the dependency chain time to surface anything relying on it.

---

## 📅 Version history

| Version | Date | Notes |
|---|---|---|
| 0.1.0 | 2026-04-10 | Initial draft. Tier 1 + Tier 2 tags defined. |
