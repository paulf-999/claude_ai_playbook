# 🚀 Skill Creation Process

**Purpose:** The proven baseline pattern for a new skill, and the 7-step workflow to create one.

---

## 🏆 Baseline Skill Pattern

All new skills should follow this proven pattern:

- **Ultra-lean SKILL.md** (~60 lines) — all detail externalized to reference/
- **Contract-first** — skill.contract.yaml defines scope *before* SKILL.md is written
- **Evals-driven** — test scenarios organized by phase; quality scorecard scored *against* evals, not independently
- **Explicit boundaries** — dispatch.not_for is authoritative; v2.0 enhancements documented separately
- **Confirmation gates** — destructive operations include explicit user confirmation
- **Maturity justified** — scorecard explains why skill is Draft/Tactical/Strategic with evidence

This pattern balances scannability (SKILL.md readable in <2 min) with comprehensive detail (reference/ files for implementation, formats, rationale).

## 🚀 Create a Skill (8 Steps)

1. **Run `/skill_creator`** → answers questions → generates directory with template
2. **Name it:** `<domain>_<action>` format (see `_core_standards.md` for naming rules and examples)
3. **Populate `skill.contract.yaml` FIRST** [REQUIRED] — defines scope before SKILL.md
   - Define what the skill does: `dispatch.triggers`
   - Define what it does NOT do: `dispatch.not_for` (prevents scope creep; MOST IMPORTANT FIELD)
   - List required tools, resources, dependencies
   - Declare output type and confirmation requirements
   - Reference: See `_core_standards.md`
4. **Write `SKILL.md` using 5-section structure** [REQUIRED]
   - Use the 5-section canonical structure (see `_core_standards.md`)
   - Reference: `~/.claude/_templates/skills/SKILL.md.template`
   - Keep to ~60 lines; externalize detail to `reference/` files
   - If SKILL.md exceeds 60 lines, detail belongs in reference/
5. **Create `quality_scorecard.md`** [REQUIRED] — at skill root, not in `reference/`
   - 7-dimension table only; maturity justification goes in SKILL.md's Best For line
6. **Create `reference/` files** [REQUIRED]
   - `_implementation.md` — phases, logic, error handling
   - `_formats.md` (if applicable) — standards, validation, examples
7. **Write `tests/evals.yaml`** [REQUIRED] — THE standard testing approach
   - Lives in `tests/`, never at skill root — "evals" is jargon to a non-technical reader
   - 10–15 scenarios organized by phase/feature
   - Each eval: name, description, input, setup, expected_output
   - Coverage: happy paths, error cases, edge cases
   - Count matches maturity level (Draft 5–8, Tactical 8–12, Strategic 12+)
   - Evals are THE source of truth; quality scorecard is scored *against* evals
   - Also write `tests/README.md` — plain language: what the file is, how many scenarios, why
8. **Score complexity & submit**
   - Complexity (0–10): Concepts (0–3) + Scope (0–3) + Dependencies (0–2) + Prerequisites (0–2)
   - Maturity gates: Draft ≤4, Tactical ≤6, Strategic ≤8, 9+ = must split
   - Pre-commit validates structure + naming + complexity
   - Human review validates design clarity and scope focus

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- Sibling: `_core_standards.md` — naming, SKILL.md structure, contract fields
