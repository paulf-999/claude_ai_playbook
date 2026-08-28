# 🛠️ Rule Authoring

**Purpose:** Establish a standardized process for creating rules that ensures intentionality, proper scoping, and mechanical rigor.

Create focused, well-tested rules that solve real problems. One concept per rule.

## ✅ Pre-Creation Checklist

Before writing any rule, answer these five essential questions:

1. **Mechanical enforcement or instructional?**
   - Enforcement (hook, test, pre-commit validation) → requires tests per `testing.md`
   - Instructional (Claude reads and follows) → structural tests via test_rules_structure.py

2. **Always-on or lazy-loaded?**
   - Always-on: import into CLAUDE.md (core safety rules, ~100–150 tokens/session cost)
   - Lazy-load: `04_lazy_load/` (domain-specific, load on-demand only)
   - Justify token cost if always-on

3. **Evidence of need** (not hypothetical)
   - Usage data, recurring incidents, user feedback, or prior failures
   - If speculative: defer or rephrase as question/guidance instead (per `guiding_principles.md`)

4. **Related/conflicting rules?**
   - Check **full rule list** in `~/.claude/_rules/03_claude_reference/claude_rule_system/claude_rule_loading_strategy.md`
   - Search codebase for similar guidance to prevent duplication
   - Clarify which rules this complements or overlaps with

5. **Which directory & how to name?**
   - Directory choice (per below); naming via `naming_standards.md` → children files for directory structure and naming patterns
   - `01_essentials/` — blocking/safety rules (guiding_principles, behaviour, security, testing)
   - `02_claude_standards/` — how Claude operates (efficiency, git, memory, MCP trust)
   - `04_lazy_load/` — domain-specific or discretionary (style guides, tools, automation)

## 🚀 Rule Creation (4 Steps)

1. **Answer the checklist above** — clarify scope before writing
2. **Pick a template:** Use `~/.claude/_templates/RULE.md.template`
   - Template A (single principle, ~60 lines) vs. Template B (multiple patterns, ~100 lines)
3. **Write the rule** — follow template structure, emoji headers, one sentence per bullet
4. **Write tests:** Enforcement rules require tests in `_tests/rules/`. Instructional rules use structural checks.

## 📏 Quality Gates

- **H1 emoji header** — scannability
- **Purpose statement** — one line, top of file
- **One concept per rule** — related patterns grouped, not split across files
- **~100-line limit** — split into parent + child files if needed (see writing_style.md)
- **Trailing newline** — exactly one `\n` at EOF
- **Related rules section** — links to dependencies via `@~/.claude/_rules/...` or `[[memory-slug]]`
- **Test validation** — enforcement rules pass custom tests; all rules pass test_rules_structure.py

## 📚 References & Related Rules

**Naming & placement:**
- `naming_standards.md` — self-describing, unambiguous naming principles; see children for directory structure and object patterns
- `~/.claude/_rules/03_claude_reference/claude_rule_system/claude_rule_loading_strategy.md` — full rule list; duplication detection + always-on vs. lazy-load placement

**Authoring & testing:**
- `~/.claude/_templates/RULE.md.template` — two templates (principle-based vs. constraint-based)
- `testing.md` — when tests are required; enforcement rules always need tests

**Principles & maintenance:**
- `guiding_principles.md` — intentionality principle; evidence-gathering methods; review cadence (reset every ~6 months per Boris Cherny)
- `behaviour.md` — includes decision-making as child file (_decision_making.md); when to present options vs. decide unilaterally

**Staleness & reviews:** Per `guiding_principles.md` reset cycles, audit all rules every ~6 months. Archive unused rules; update evidence for kept rules.

## 📖 Reference (Claude's design patterns)

<!-- Rule architecture: scope decisions, design patterns, and creation processes -->
@~/.claude/_reference/claude_design_patterns/rules/_adding_rules.md

---
