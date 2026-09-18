# ✅ Skill Hard Gates Checklist

**Purpose:** Final validation checklist before submitting a new skill — verify completeness and compliance across every required artifact.

---

## Before Submitting

- [ ] **Contract complete BEFORE SKILL.md** — never write SKILL.md without contract finalization
  - [ ] name, version, summary, maturity all defined
  - [ ] dispatch.triggers documented (when is skill invoked?)
  - [ ] dispatch.not_for documented (scope boundaries; MOST IMPORTANT)
  - [ ] output (type, confirmation_required, reversible, returns) declared
  - [ ] requires [IF APPLICABLE] — tools, resources, permissions
  - [ ] dependencies [IF APPLICABLE] — external APIs or systems
- [ ] **SKILL.md structure [REQUIRED]:** 5 sections only, ~60 lines max
  - [ ] Frontmatter: name, description, version, maturity, tags
  - [ ] Purpose: 1 sentence value prop + 3–4 bullets
  - [ ] Example Usage: realistic scenario showing complete journey
  - [ ] Best For: use cases + explicit caveats (when NOT to use)
  - [ ] References: links to reference/ files (no inline detail)
  - [ ] Total length: ≤60 lines (if longer, detail belongs in reference/)
- [ ] **Complexity score [REQUIRED]:** 0–10 rating
  - [ ] Score ≤ maturity limit (Draft ≤4, Tactical ≤6, Strategic ≤8)
  - [ ] If over limit: reduce scope or split into multiple skills
- [ ] **evals.yaml [REQUIRED]:** 10–15 scenarios organized by phase
  - [ ] Each eval: name, description, input, setup, expected_output
  - [ ] Coverage: happy paths, error cases, edge cases, user interactions
  - [ ] Count matches maturity (Draft 5–8, Tactical 8–12, Strategic 12+)
  - [ ] evals.yaml is THE testing vehicle (not ad-hoc test_*_handler.py)
- [ ] **Quality scorecard [REQUIRED]:** reference/_quality_scorecard.md
  - [ ] 7 dimensions scored (Design, Complexity, Test Coverage, Code Quality, Security, Documentation, Standards)
  - [ ] Dimensions scored *against evals.yaml*, not independently
  - [ ] Maturity level justified with evidence
  - [ ] Design rationale explained
- [ ] **Reference files [REQUIRED]:**
  - [ ] reference/_quality_scorecard.md exists with all 7 dimensions
  - [ ] reference/_implementation.md exists (phases, logic, error handling)
  - [ ] reference/_formats.md [IF APPLICABLE] (standards, validation, examples)
- [ ] **Scope boundaries enforced:**
  - [ ] dispatch.not_for defined and specific (not empty)
  - [ ] Rationale documented in quality scorecard
  - [ ] Skill has clear, narrow focus (not "everything related to X")
- [ ] **Naming:** `<domain>_<action>` format, valid domain ID, directory matches

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and core standards
