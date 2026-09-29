<!-- version: 1.0.2 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-29 -->
# 📐 Rule Directory Organization Patterns

**Purpose:** Define when and how to organize related rules into parent+child directory structures, preventing flat-level sprawl while keeping rule discovery clear.

---

## 🎯 The Pattern

Rules follow a **relationship-based organization principle**:

### Single-concept rules (stay flat)
**Condition:** One rule file covering a complete concept, self-contained, no dependent child rules.

```
_rules/01_essentials/
├── security.md                    ← single concept, flat level
├── guiding_principles.md          ← single concept, flat level
└── authoring_rules.md             ← single concept, flat level
```

**Decision rule:**
- Concept is self-contained with no related child documents
- No index/parent file required
- Place directly at top level

### Multi-concept rules (get subdirectories)
**Condition:** One parent rule + 2+ child files, each covering a related aspect of the parent concept.

```
_rules/02_claude_standards/
├── behaviour.md                                ← parent: foundational behavior guidelines
└── behaviour/
    ├── _artefact_proposal_gates.md            ← child: artifact proposal validation
    └── _decision_making.md                    ← child: decision-making patterns

_rules/03_authoring_guidelines/
├── authoring_skills.md                         ← parent: skill creation framework
└── authoring_skills/
    ├── _core_standards.md                     ← child: naming, structure, contract, maturity
    ├── _hard_gates_checklist.md               ← child: the single creation checklist
    └── _scope_and_maintenance.md              ← child: scope boundaries and stability
```

**Decision rule:**
- Parent rule file at top level (entry point, discoverable)
- Related child rules in dedicated subdirectory named `<concept>/`
- Each child file uses underscore prefix: `_<aspect>.md` (distinguishes from top-level rules)
- Parent rule lists all children with links to `<concept>/_<file>.md`
- Child files reference siblings using relative paths: `[_file.md](_file.md)`

---

## 🎯 When to Apply

**Trigger:** Rule growing to 2+ related child concepts, or when parent file exceeds ~110 lines.

**Questions to ask:**

1. Is this rule a parent index for 2+ related child rules?
   - **YES** → Create parent + subdirectory structure
   - **NO** → Keep as single file at top level

2. Does the rule exceed ~110 lines?
   - **YES** → Consider splitting into parent + child files
   - **NO** → Assess if topic complexity warrants splitting anyway

3. Are child rules distinct concepts grouped under one parent?
   - **YES** → Create subdirectory for the group
   - **NO** → Each should be a standalone top-level rule

---

## ✅ Examples & Checklist

@~/.claude/_rules/01_essentials/claude_usage_standards/claude_directory_structure/_rule_directory_patterns/_examples_and_checklist.md

---

## 🔗 Related rules

- **Parent:** `claude_directory_structure.md` — directory organization overview
- **Sibling:** `_claude_directory_naming.md` — naming patterns for files and directories
- **Related:** `writing_style.md` → `_multifile_document_organization.md` — when to split documents into parent + child files (general principle, applies to rules too)
