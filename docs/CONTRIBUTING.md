# Contributing Skills

This guide explains how to develop, test, and contribute new skills to the Claude playbook.

## Skill Development Workflow

Skills progress through three maturity tiers:

```
draft (0.x) → tactical (1.x) → strategic (2+.x)
   ↓              ↓                    ↓
happy path    stable & tested    production-ready
```

Each tier has different quality expectations, validated via the **skill authoring gate**.

---

## The Skill Authoring Gate

All skills are validated against a **three-level gate** before merging:

### 🏗️ Crawl (Foundation): C0–C7

**What:** Basic structure and safety checks — every skill must have.

**Enforcement:** Automatic via pre-commit hook + linter
- Runs when you commit skill files
- **Blocks** commit if violations found
- **You can't merge without passing crawl level**

**Examples of crawl criteria:**
- C1: `skill.contract.yaml` exists with all required fields
- C3: Version matches maturity (draft=0.x, tactical=1.x, strategic=2+.x)
- C6: No hardcoded paths or personal names
- C7: External dependencies declared in contract

**How to pass:** Follow the [Skill Authoring Checklist](skill_authoring_checklist.md) — crawl section.

### 🚶 Walk (Quality): W1–W6

**What:** Readability, style compliance, test coverage, clarity.

**Enforcement:** Manual code review + local testing
- You run tests locally before submitting PR: `pytest tests/test_skill_authoring_gate.py`
- Reviewers spot-check during code review
- **Doesn't block merge** (advisory feedback)

**Examples of walk criteria:**
- W1: SKILL.md readable in <60 seconds
- W2: Follows writing_style.md (emojis, formatting, line length)
- W3: Test coverage matches maturity
- W4: No unexplained Claude jargon

**How to pass:** Test locally, respond to reviewer feedback.

### 🏃 Run (Comprehensive): R1–R5

**What:** Full quality, maturity progression, gap documentation.

**Enforcement:** Manual review by maintainers (strategic skills only)
- Only applies to **strategic skills** (version 2+.x)
- Reviewers verify during code review
- **Doesn't block merge** (guidance for completeness)

**Examples of run criteria:**
- R1: Semantic versioning progression documented
- R3: Version history explains each tier bump
- R4: Known gaps explicitly documented with workarounds
- R5: Complex skills (external APIs) have optional schema

**How to pass:** Comprehensive test suite, clear documentation.

---

## Before You Start: Checklist

- [ ] Understand the three-level gate (above)
- [ ] Read [skill_authoring_checklist.md](skill_authoring_checklist.md)
- [ ] Have a clear definition of what your skill does (not what it might do someday)

---

## Development Process

### 1. Create your skill

Use the skill-creator plugin:

```bash
/skill_creator
```

Follow the prompts:
- **Intent:** What problem does this solve?
- **Maturity:** draft, tactical, or strategic?
- **Tier 1 tags:** criticality (must/should/could/want), status, etc.

Skill-creator will:
- Generate a skill directory
- Stamp `skill.contract.yaml` template
- Create a `SKILL.md` template

### 2. Fill in the contract

Edit `skill.contract.yaml`:

```yaml
name: skill_identifier         # kebab-case, matches directory
version: 0.1.0                 # 0.x for draft, 1.x for tactical, 2+.x for strategic
summary: One-line description

maturity: draft                # or: tactical, strategic
test_coverage_level: none      # or: basic, comprehensive

when:
  - /skill_name
  - "phrase that triggers"

dont_use_for:
  - "don't use for bulk operations"

requires:
  tools: [Bash, Read, Agent]   # tools this skill uses
  mcp_servers: [GitHub]        # MCP servers (if any)
  external: []                 # external system access (if any)

output: conversational         # or: file, external_service, mixed
reversible: true               # false if actions are permanent
```

### 3. Write SKILL.md

Use this structure (end-user-first):

```markdown
# Skill: `skill_name`

| | |
|---|---|
| **Description** | One-line summary |
| **Version** | 0.1.0 |
| **Tested** | No |

## 🎯 What this skill can and can't do

**This skill does:**
- Task 1
- Task 2

**This skill doesn't do:**
- Anti-pattern 1
- Anti-pattern 2

## ✅ Prerequisites

[What's needed: tools, auth, permissions, etc.]

## 📋 How it works

[Brief overview; reference phase1.md, phase2.md for detail]

## ⚠️ Known gaps

[Limitations and workarounds]
```

**Style rules:**
- All `##` headers must have emojis
- Bullets use bold keywords: `**Why:**`, `**Note:**`, `**Example:**`
- One sentence per bullet (use child bullets for multi-sentence ideas)
- Keep file <150 lines (split into phases if longer)

### 4. Write tests

Create a test file: `tests/skills/test_skill_name.py`

**Test count by maturity:**
- Draft: 1–2 tests (happy path only)
- Tactical: 5–8 tests (main path + error handling)
- Strategic: 15+ tests (complete coverage)

**Example test:**

```python
import pytest
from pathlib import Path

def test_skill_name_creates_output():
    """Verify skill produces expected output."""
    result = run_skill()
    assert result is not None
    assert "expected" in result
```

### 5. Validate locally

Before committing, run:

```bash
# Check crawl criteria (C0–C7)
make lint_skills

# Check walk/run criteria (W1–R5)
pytest tests/test_skill_authoring_gate.py -v

# Optional: just test your skill
pytest tests/test_skill_authoring_gate.py -k skill_name -v
```

Fix any failures. Tests that skip are advisory (reviewer will spot-check).

### 6. Commit and open a PR

```bash
git add src/claude/skills/skill_name/
git commit -m "feat(skills): add skill_name

Brief description of what the skill does.
"
git push origin feature/add_skill_name
```

Then open a PR with your branch.

### 7. Address feedback

Reviewers will check:
- **Crawl:** Should already pass (linter validated before commit)
- **Walk:** Spot-check clarity (W1), style (W2), test coverage (W3)
- **Run:** For strategic skills only (R1–R5)

Respond to feedback and update your PR. Once approved, merge!

---

## Maturity Progression

Skills can progress from draft → tactical → strategic. Here's how:

### Draft → Tactical

**When:** Skill is stable and well-tested

**Process:**
1. Ensure all TODOs are resolved or moved to "Known gaps"
2. Test coverage: 5–8 test cases (main path + errors)
3. Update version: `0.x.x` → `1.x.x`
4. Update maturity in contract: `draft` → `tactical`
5. Add version history to SKILL.md explaining the bump
6. Submit PR for review

**Reviewer checks:** C0–C7 (crawl), W1–W6 (walk)

### Tactical → Strategic

**When:** Skill is production-ready and handles all edge cases

**Process:**
1. Ensure complete test coverage (15+ test cases)
2. Document all known gaps with workarounds
3. Update version: `1.x.x` → `2.x.x`
4. Update maturity in contract: `tactical` → `strategic`
5. Add version history documenting the journey
6. Optional: Create `skill_schema.yaml` for complex skills
7. Submit PR for review

**Reviewer checks:** All C/W/R criteria

---

## Enforcement Summary

| Stage | What's enforced | Who enforces | What happens if you fail |
|-------|---|---|---|
| **Commit** | Crawl (C0–C7) | Pre-commit hook | ❌ Commit blocked |
| **Code review** | Walk (W1–W6) | Manual review | ⚠️ Requested changes |
| **Strategic review** | Run (R1–R5) | Manual review | ⚠️ Requested changes |

---

## When You're Stuck

- **Contract questions:** See `skill.contract.yaml.template`
- **Style questions:** See `writing_style.md`
- **Checklist questions:** See `skill_authoring_checklist.md`
- **Test help:** Ask in code review; reviewers are happy to help

---

## Questions?

Ask in your PR. Reviewers are here to help you succeed!
