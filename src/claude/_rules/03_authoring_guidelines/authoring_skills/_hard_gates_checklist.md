<!-- version: 2.1.0 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-09-29 -->
# ✅ Skill Hard Gates Checklist

**Purpose:** The single checklist for creating and reviewing a skill — work through it in order, and every box must be ticked before submitting.

---

## Before Submitting

- [ ] **1. Naming:** `<domain>_<action>` format, valid domain ID, directory matches (see `_core_standards.md`)
- [ ] **2. Contract complete BEFORE SKILL.md** — never write SKILL.md without contract finalization
  - [ ] name, version, summary, maturity all defined
  - [ ] dispatch.triggers documented (when is skill invoked?)
  - [ ] dispatch.not_for documented, specific and not empty (scope boundaries; MOST IMPORTANT)
  - [ ] output (type, confirmation_required, reversible, returns) declared
  - [ ] Destructive operations set `confirmation_required: true`
  - [ ] requires [IF APPLICABLE] — tools, resources, permissions
  - [ ] dependencies [IF APPLICABLE] — external APIs or systems
  - [ ] Secrets come from environment variables only, each listed in `requires.resources`
  - [ ] Each permission is listed in `dependencies.permissions`, with no more than the skill needs
- [ ] **3. SKILL.md structure [REQUIRED]:** start from `~/.claude/_templates/skills/SKILL.md.template`
  - [ ] Frontmatter: name, description, maturity, tags
  - [ ] Metadata header straight after the frontmatter: version (matching the contract), created, updated
  - [ ] Purpose: 1 sentence value prop + 3–4 bullets
  - [ ] Example Usage: realistic scenario showing complete journey
  - [ ] Best For: use cases, explicit caveats, and a one-sentence maturity justification
  - [ ] References: links to reference/ files (no inline detail)
  - [ ] Every `##` heading has an emoji
  - [ ] Total length: ≤60 lines (if longer, detail belongs in reference/)
- [ ] **4. tests/evals.yaml [REQUIRED]:** written before any handler code, organized by phase
  - [ ] Lives at `tests/evals.yaml`, not skill root
  - [ ] Each eval: name, description, input, setup, expected_output
  - [ ] Count and coverage match maturity (Draft 5–8 evals, Tactical 8–12 evals, Strategic 12+ evals)
  - [ ] evals.yaml is THE testing vehicle (not ad-hoc test_*_handler.py)
- [ ] **5. tests/README.md [REQUIRED]:** plain-language explanation of what evals.yaml is
- [ ] **6. Reference files [REQUIRED]:**
  - [ ] reference/_implementation.md exists (phases, logic, error handling)
  - [ ] reference/_formats.md [IF APPLICABLE] (standards, validation, examples)
- [ ] **7. Quality scorecard [REQUIRED]:** `scorecard_<skill_name>.md` at skill root, table-only
  - [ ] Follows `~/.claude/_templates/skills/_quality_scorecard_template.md`, including Date Created and Date Updated
  - [ ] 7 dimensions scored *against evals.yaml*, not independently
- [ ] **8. Complexity score [REQUIRED]:** raw sum per `_complexity_scoring.md`
  - [ ] Score ≤ maturity limit (Draft ≤4, Tactical ≤6, Strategic ≤8)
  - [ ] If over limit: reduce scope or split into multiple skills
- [ ] **9. Clean-up:**
  - [ ] No hardcoded paths or usernames (see `portable_paths.md`)
  - [ ] User input is validated before it reaches an API or shell command (see `security.md`)
  - [ ] No TODO/FIXME left in a tactical or strategic skill
  - [ ] Skill has clear, narrow focus (not "everything related to X")
  - [ ] Doesn't duplicate or conflict with an existing skill

---

## 🔗 Related

- Parent: `authoring_skills.md` — child index and file organisation
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields, maturity levels
