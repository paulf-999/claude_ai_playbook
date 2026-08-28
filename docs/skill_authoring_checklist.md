# Skill Authoring Checklist

## Overview

Skills follow a **three-level gate** as they mature from draft to production-ready.

| Level | Name | Criteria | Enforcement | Author Action |
|-------|------|----------|-------------|---|
| 🏗️ | **Crawl** (C0–C7) | Foundation: structure, contract, no coupling | Auto-gate (pre-commit hook) | ✅ Must pass before commit |
| 🚶 | **Walk** (W1–W6) | Quality: clarity, style, testing, documentation | Manual review + local tests | ⚠️ Test locally; reviewers spot-check |
| 🏃 | **Run** (R1–R5) | Comprehensive: versioning, gap documentation, maturity progression | Manual review | ⚠️ Required for strategic skills only |

---

## 🏗️ Crawl Level: Foundation (C0–C7)

These criteria ensure every skill has the basic structure to be safe to use. **The linter validates C0–C7 automatically via pre-commit hook — these must pass before you can commit.**

### C0: Created via skill-creator (mandatory gate)
- ✅ Use `/skill_creator` command (not manual directory creation)
- ✅ Skill stamped with contract template automatically

### C1: skill.contract.yaml exists and complete
- ✅ File exists at `<skill>/skill.contract.yaml`
- ✅ All required fields present:
  - `name`, `version`, `summary`
  - `maturity`, `test_coverage_level`
  - `when`, `dont_use_for`
  - `requires` (tools, mcp_servers, external)
  - `output`, `reversible`

### C2: No hard coupling to other skills
- ❌ Don't assume other skills exist
- ✅ Only invoke optional skills via Agent with fallback
- ❌ Avoid phrases like "execute skill_name" or "requires skill_name"

### C3: Semantic versioning aligned with maturity
- ✅ Version format: `X.Y.Z` (e.g., `0.1.0`)
- ✅ Major version matches maturity:
  - Draft: `0.x.x`
  - Tactical: `1.x.x`
  - Strategic: `2+.x.x`

### C4: SKILL.md has required structure
- ✅ Sections present (in order):
  1. Metadata table (Description, Version, Tested)
  2. "What this skill can/can't do" section
  3. Prerequisites section
  4. "How it works" or phases section
  5. "Known gaps" section

### C5: SKILL.md is end-user-first
- ✅ Opens with metadata table, not YAML frontmatter
- ✅ Supports quick skimming (<60 seconds to understand purpose)
- ✅ No jargon in opening sections without explanation

### C6: No hardcoded paths or personal references
- ❌ No `/home/`, `/Users/`, absolute paths
- ❌ No personal names or usernames
- ✅ Use relative paths, environment variables, or parameterized paths

### C7: External dependencies declared
- ✅ All tools listed in `requires.tools` (Bash, Read, Agent, etc.)
- ✅ All MCP servers in `requires.mcp_servers` (GitHub, Atlassian, etc.)
- ✅ All external access in `requires.external` (GitHub repo access, API keys, etc.)

---

## 🚶 Walk Level: Quality (W1–W6)

These criteria ensure the skill is clear, well-tested, and follows style standards. **Reviewers spot-check these; use local tests to validate before submitting.**

### W1: SKILL.md is readable at a glance
- ✅ Opening is clear without jargon (~100 lines max for opening section)
- ✅ Non-technical user can understand purpose in <60 seconds
- **How to test locally:** Read your SKILL.md opening paragraph aloud — does it make sense?

### W2: Follows writing_style.md conventions
- ✅ All `##` headers have emojis
- ✅ Bullets use bold keywords: `**Why:**`, `**Note:**`, `**Example:**`
- ✅ One sentence per bullet (use child bullets for multi-sentence ideas)
- ✅ Line count: file <150 lines (split if longer)
- **How to test:** `grep "^## " SKILL.md | grep -v "[^[:ascii:]]*"` (look for emojis)

### W3: Test coverage matches maturity
- Draft: 1–2 tests (happy path)
- Tactical: 5–8 tests (main path + error cases)
- Strategic: 15+ tests (main path, errors, edge cases)
- **How to test locally:** `pytest tests/skills/test_<skill_name>*.py -v`

### W4: No unexplained Claude jargon
- ❌ Don't use jargon without explanation:
  - maturity, scope gate, crawl/walk/run
  - triggers, MCP, skill contract
  - tools, reversible, output types
- ✅ Either explain inline or use plain language
- **How to check:** Search SKILL.md for jargon terms; if found, explain or remove

### W5: No TODO/FIXME in tactical+ skills
- ✅ Draft skills: TODOs allowed (mark incomplete work)
- ❌ Tactical+ skills: no unresolved TODOs/FIXMEs
- **How to check:** `grep -i "TODO\|FIXME" SKILL.md` should return nothing

### W6: Phase files focused and complete (if multi-phase)
- ✅ Each phase is 100+ lines (meaningful content)
- ✅ Named in order: `phase1.md`, `phase2.md`, etc.
- ✅ Each phase is self-contained
- **How to check:** `wc -l phase*.md` — each should be >100 lines

---

## 🏃 Run Level: Comprehensive (R1–R5)

These criteria apply to **strategic skills only** — production-ready skills expected to be stable and complete.

### R1: Semantic versioning aligns with maturity
- ✅ Major version matches maturity (verified in C3, but worth double-checking)
- ✅ Version history in git shows progression: `0.x` → `1.x` → `2.x`

### R2: Test coverage is thorough
- ✅ Tests cover main path, error cases, edge cases
- ✅ Test file >100 lines (substantive coverage)
- ✅ Parametrized tests for multiple scenarios

### R3: Maturity progression documented
- ✅ SKILL.md has "Version History" or "Changelog" section
- ✅ Each major version bump is explained
- ✅ Rationale for promotion to next tier documented

### R4: No unresolved gaps in strategic skills
- ❌ No TODO/FIXME (should have been resolved in tactical)
- ✅ "Known gaps" section explicitly lists limitations
- ✅ Gaps have documented workarounds

### R5: Complex skills have optional skill_schema.yaml
- If `output: external_service` (e.g., Jira, GitHub API calls):
  - 💡 Optional: Create `skill_schema.yaml` documenting inputs/outputs
  - This helps future maintainers understand the skill's surface area

---

## 🚀 Quick Start: 10 Steps to Publish

1. **Create:** Run `/skill_creator` (generates directory + contract template)
2. **Contract:** Fill in `skill.contract.yaml` with metadata
3. **Write:** Create `SKILL.md` with required sections
4. **Test:** Add test file with cases matching maturity
5. **Local check:** Run `make lint_skills` (linter validates C0–C7)
6. **Local test:** Run `pytest tests/skills/test_<skill>.py -v` (validate W1–W6)
7. **Style:** Verify emojis, formatting, line length
8. **Jargon:** Search for unexplained Claude terms; explain or remove
9. **Commit:** Make a pull request with your skill
10. **Review:** Respond to reviewer feedback on walk/run criteria

---

## ⚠️ Common Mistakes

### Crawl level (will block commit)

**C1 mistake:** Missing required field in contract
- ❌ `requires:` empty or missing
- ✅ List all tools, MCP servers, external access needed

**C3 mistake:** Version doesn't match maturity
- ❌ Draft skill with version `1.0.0`
- ✅ Draft = `0.x.x`, Tactical = `1.x.x`, Strategic = `2+.x.x`

**C4 mistake:** Missing SKILL.md sections
- ❌ Skipped "Known gaps" section
- ✅ Include all 5 sections (metadata, can/can't, prerequisites, how it works, gaps)

**C6 mistake:** Hardcoded paths
- ❌ `requires.external: [/home/paul/config.yaml]`
- ✅ Use parameterized paths or env vars

### Walk level (will be flagged in review)

**W1 mistake:** Opening is too jargon-heavy
- ❌ "This tactical skill uses scope gates and crawl-level validation..."
- ✅ "Create a Confluence page from a template"

**W2 mistake:** Missing emojis on headers
- ❌ `## How it works`
- ✅ `## 📋 How it works`

**W3 mistake:** Test file too small
- ❌ Tactical skill with 2 tests
- ✅ Tactical skill with 5–8 tests

**W4 mistake:** Using jargon without explanation
- ❌ "This skill uses the maturity framework..."
- ✅ "This skill is in draft stage (early exploration) — expect breaking changes"

### Run level (strategic skills only)

**R4 mistake:** Strategic skill with TODOs
- ❌ "TODO: add error handling for timeout"
- ✅ Resolve all TODOs or move to "Known gaps" with workaround

---

## 📋 Enforcement Summary

| Level | How it's enforced | What happens if you fail? |
|-------|------------------|---|
| **Crawl (C0–C7)** | Pre-commit hook (`skill_authoring_gate_lint.py`) | ❌ Commit blocked; fix and retry |
| **Walk (W1–W6)** | Local tests + manual review | ⚠️ Reviewer requests changes in PR |
| **Run (R1–R5)** | Manual review (strategic skills) | ⚠️ Reviewer requests changes in PR |

---

## 🔍 How to Run Tests Locally

**Before committing:**

```bash
# Validate crawl criteria (C0–C7)
make lint_skills

# Validate walk/run criteria (W1–R5)
pytest tests/test_skill_authoring_gate.py -v

# Or test your specific skill
pytest tests/test_skill_authoring_gate.py -k "your_skill_name" -v
```

If linter fails, fix the issues and retry. If tests skip/warn, review the feedback and address in your PR.

---

## 📚 Related Documentation

- `skill.contract.yaml.template` — Contract field definitions
- `writing_style.md` — Style guide (emojis, formatting, brevity)
- `prerequisites_checklist.md` — Enforcement mechanisms (internal reference)
- CONTRIBUTING.md — Governance and maturity workflow

---

## Questions?

Refer to the quick start section or ask during code review. Reviewers are here to help clarify what "good" looks like for your skill.
