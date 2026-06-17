---
name: audit_skills
description: Audit all installed skills in ~/.claude/skills/ and produce a prioritised gap report covering frontmatter, file length, scope gate, and standards compliance.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools: Agent, Read, Glob
triggers:
  explicit:
    - /audit_skills
    - "audit my skills"
    - "check skill quality"
    - "run the skill auditor"
    - "skill health check"
  contextual:
    - user wants to surface quality issues or missing guidance across the Claude skill library
not_for:
  - reviewing a single skill (read the file directly instead)
  - making skill fixes without first seeing the gap report
output:
  type: conversational
  confirmation_required: false
---

## 🚧 Scope gate

This skill is at **draft** maturity — happy path only.

---

## 🗂️ Playbook repo path

Installed skills at `~/.claude/skills/` are copies managed by the playbook repo. Source of truth:

```
~/git_repos/core/dmt-scripts-claude_ai_playbook/src/claude/skills/
```

Skills are organised into category subdirectories in the repo but installed flat at `~/.claude/skills/`.

### Path mapping

| Installed path | Repo source path |
|---|---|
| `~/.claude/skills/<name>/SKILL.md` | `src/claude/skills/_<category>_skills/<name>/SKILL.md` |

If the category for an installed skill is uncertain, search `src/claude/skills/` by name. If no repo source exists, flag this to the user — fixes should still be applied to the installed copy.

Any fix applied only to `~/.claude/skills/` will be **overwritten** the next time `make install` runs. All fixes must be applied to both paths.

---

## 🔍 Phase 1 — Run the audit

Dispatch the `skill_auditor` agent via the Agent tool:

> "Audit all skill files in ~/.claude/skills/. Follow all skill_auditor instructions. Read every SKILL.md in full before reporting. Produce the full structured gap report."

---

## 📋 Phase 2 — Present findings

Print the report to the user in full.

Then summarise in one sentence: total skills audited, total findings, and the single highest-priority fix.

---

## 🔧 Phase 3 — Offer to fix

Ask the user:

> "Would you like me to work through the High and Medium findings and apply fixes? I'll tackle them one at a time and confirm each change with you before applying. Each fix will be applied to both the installed skill and the playbook repo source file."

- If **no**: stop. The report is available above for manual action.
- If **yes**: work through findings in priority order — High first, then Medium. For each: state the finding, propose the fix, wait for confirmation, apply to both paths, then move to the next.
