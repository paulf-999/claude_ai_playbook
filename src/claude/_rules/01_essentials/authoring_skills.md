# 🛠️ Skill Authoring

**Purpose:** Create focused, well-documented, properly tested skills. One concept per skill.

---

## 🚀 Create a Skill (7 Steps)

1. **Run `/skill_creator`** → answers questions → generates directory with template
2. **Name it:** `<domain>_<action>` format (e.g., `confluence_create_page`, `jira_create`)
   - **Valid domains:** See `skill_domains.yaml`
   - **Hard rule:** Directory prefix must match domain ID (e.g., `confluence_create_page` → `_confluence_skills/`)
3. **Fill `skill.contract.yaml`** with name, version, summary, maturity, when, requires
4. **Write `SKILL.md`** using `~/.claude/_templates/skills/SKILL.md.template` as starting point (see `_skill_structure_contract.md` for structure details)
5. **Score complexity** (0–10): Concepts (0–3) + Scope (0–3) + Dependencies (0–2) + Prerequisites (0–2)
   - **Maturity gates:** Draft ≤4, Tactical ≤6, Strategic ≤8, 9+ = must split
6. **Write tests:** Draft 1–2, Tactical 5–8, Strategic 15+
7. **Submit:** Pre-commit validates structure + naming + complexity; human review validates design

---

## 📐 SKILL.md Structure & Contract

@~/.claude/_rules/01_essentials/skill_authoring/_skill_structure_contract.md

## ✅ Quality & Review Checklists

@~/.claude/_rules/01_essentials/skill_authoring/_skill_quality_checklist.md

## 🔎 Review Framework

@~/.claude/_rules/01_essentials/skill_authoring/_skill_review_framework.md

---

## 📁 Child File Organization

Most skills only need `SKILL.md` + `skill.contract.yaml`. For skills with multiple supporting documents:

**Supportive documentation files** (reference material):
- Use leading underscore: `_<topic>.md` (e.g., `_arguments.md`, `_phases.md`, `_roadmap.md`)
- Readers find via references in `SKILL.md`

**Pattern/template files** (reusable templates):
- Place in `templates/` subdirectory: `templates/<pattern_name>.md` (e.g., `templates/general_page.md`)
- Kept separate from skill configuration

**Main entry point:**
- `SKILL.md` — the only required file

---

## ⚡ Quick Reference

**Naming pattern:** `<domain>_<action>` (domains defined in `skill_domains.yaml` + `skill_domains_future.yaml`)
**Line goal for SKILL.md:** ~100 lines (8 sections, one concept per section)
**Maturity:** draft (0.x) → tactical (1.x) → strategic (2.x+)
**Tool:** `review_skill <path>` for Claude auto-review
**Validation:** Pre-commit checks domain prefix against YAML config

For detailed checklists, review process, and complexity scoring → see child files: `_skill_structure_contract.md`, `_skill_quality_checklist.md`, `_skill_review_framework.md`.

---

## 🔗 Related Rules

- **naming_standards.md** — Foundational naming principles; child file `_claude_naming_patterns.md` contains skill naming patterns and domain reference
- **testing.md** — Skill testing requirements by maturity level
- **authoring_rules.md** — General rule authoring process (complementary to skill authoring)
