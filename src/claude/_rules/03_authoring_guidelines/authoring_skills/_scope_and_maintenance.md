# 🚪 Scope Boundaries & Low-Maintenance Design

**Purpose:** Every skill must declare what it does NOT do, and be designed to minimize ongoing maintenance burden.

---

## 🚪 Scope Boundaries [REQUIRED]

Every skill must explicitly declare what it does AND what it does NOT do. This prevents feature creep and sets user expectations upfront.

**In `skill.contract.yaml`, use the `dispatch.not_for` field:**

```yaml
dispatch:
  not_for:
    - Edge case 1 (skill doesn't handle this)
    - Edge case 2 (skill explicitly out of scope)
    - Future enhancement (v2.0+)
```

**Example (git_create_pr):**
```yaml
not_for:
  - complex merge conflict scenarios
  - non-main branch PRs
  - release branch workflows (v2.0+)
```

**In SKILL.md's Best For line, explain why:**
- Why these boundaries? (design choice? technical limitation? future roadmap?)
- What would v2.0 add?
- What's the tradeoff? (keeps skill lean vs. limits applicability)

### Anti-Patterns: What NOT to Do

**❌ Don't try to handle everything**
- A skill that handles "all Confluence page operations" becomes bloated and unmaintainable
- Better: narrow scope (e.g., `confluence_create_page`, `confluence_update_page` as separate skills)
- Use `not_for` to document explicit boundaries

**❌ Don't use ad-hoc test_*_handler.py scripts**
- Use `evals.yaml` (THE standard for all skills)
- Ad-hoc test scripts become unmaintained and unreliable
- evals.yaml is discoverable, testable, and documented

**❌ Don't claim maturity without evidence**
- Draft: speculative, one-time use only
- Tactical: recurring problem, battle-tested, fully tested
- Strategic: core workflow, heavy use, all edge cases covered
- Justify maturity in SKILL.md's Best For line with evidence

---

## 🛠️ Low-Maintenance Design [CRITICAL]

Skills should be designed to minimize ongoing maintenance burden. This section establishes principles for creating skills that are stable, self-contained, and resist scope creep and complexity debt.

### The Maintenance Trap: What NOT to Do

**❌ Don't create skills that require constant updates:** coupling to external APIs (fragility), versioning complexity (v1.0/v1.1/v2.0 branches = debt), interdependencies (Skill A depends on Skill B = cascade failures), or broad scope ("handle all X" = endless feature requests).

**Anti-pattern consequence:** A skill that's updated 5+ times/year is a sign of poor design, not evolution. It's a maintenance liability.

### Stability-First Design Principles

**✅ Design for immutability:**
- Once v1.0 ships, assume it won't need changes
- Future enhancements = new skill with different name (e.g., `slack_send_message` v1.0 stays frozen; threading goes in `slack_send_thread` v1.0)
- Deprecate old version cleanly: announce 6-month sunset, provide migration guide

**✅ Isolate dependencies:**
- **No skill-to-skill calls** — Use MCP or CLI for inter-skill communication, not direct calls
- **No external API coupling if avoidable** — Local-only > API-dependent (fewer failure modes)
- **Battle-tested tools only** — Slack API, GitHub API = proven stable; experimental tools = avoid

**✅ Enforce tight boundaries:**
- Use `dispatch.not_for` to explicitly freeze scope (v1.0 says "no thread replies, no reactions, no editing")
- Document v2.0 roadmap separately (doesn't belong in v1.0 contract)
- Future enhancements are *new* skills, not updates to existing ones

**✅ Test for stability:** `evals.yaml` captures the contract — future maintainers run evals before any update. If evals break, you've broken the contract; don't merge.

### Maintenance Policy

**Update only for critical reasons:**
- 🔴 **Security vulnerability** — Something is actively broken/unsafe
- 🔴 **Broken external dependency** — External API changed, tool deprecated
- ❌ **Feature requests** — Create new skill instead (prevents scope creep)
- ❌ **"Improvements"** — Refactoring is scope creep in disguise (old version works fine)

**Deprecate when truly necessary:**
- Old version is superseded by better design (e.g., `slack_send_message` → `slack_send_with_threading`)
- Announce 6-month sunset date upfront (give users time to migrate)
- Provide clear migration guide (how to switch to new skill)
- Keep old skill functional for full deprecation period (no breaking changes during sunset)

### Measurement: Tracking Maintenance Burden

Track per skill: **update frequency** (target <2/year Tactical, <1/year Strategic), **reason** (only security/API-change are valid), and **contract breakage** (does the update require changing evals.yaml?).

**Red flag:** >2 updates/year means too broad or too coupled — redesign it. **Healthy:** Tactical gets 0–1/year; Strategic gets 0.

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
