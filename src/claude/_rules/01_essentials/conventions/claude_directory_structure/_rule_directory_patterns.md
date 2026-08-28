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
_rules/01_essentials/
├── behaviour.md                                ← parent: foundational behavior guidelines
├── behaviour/
│   ├── _artefact_proposal_gates.md            ← child: artifact proposal validation
│   └── _decision_making.md                    ← child: decision-making patterns
│
├── authoring_skills.md                         ← parent: skill creation framework
├── skill_authoring/
│   ├── _skill_structure_contract.md           ← child: structure and contract fields
│   ├── _skill_quality_checklist.md            ← child: quality gates
│   └── _skill_review_framework.md             ← child: review process
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

## ✅ Examples

### ✅ Correct: Multi-concept structure (Behaviour)

```
behaviour.md                            ← parent: safe conduct guidelines
behaviour/
├── _artefact_proposal_gates.md         ← child: validating proposals
└── _decision_making.md                 ← child: when to present options
```

**Why:** Two distinct concepts (safe conduct, decision-making) grouped under behaviour. Parent is entry point; children are reference material.

### ✅ Correct: Single-concept rule (Security)

```
security.md                             ← complete, self-contained rule
```

**Why:** One concept (secure coding practices), no child rules, <110 lines, discoverable at top level.

### ❌ Wrong: Orphaned child at flat level (Anti-pattern)

```
_rules/01_essentials/
├── _decision_making.md                 ← ❌ orphaned child at flat level
└── behaviour.md                        ← ❌ parent created after sprawl
```

**Why:** Child file at flat level creates clutter and confusion. No clear grouping; difficult to navigate and maintain.

---

## 🚫 The "2+ Rule"

Do not create a subdirectory for a single child file.

- ❌ `behaviour/` with only `_decision_making.md` → Flatten to top-level, name `decision_making.md`
- ✅ `behaviour/` with `_artefact_proposal_gates.md` + `_decision_making.md` → Justified; two related children

**Why:** Single-child subdirectories create unnecessary navigation overhead. Threshold is 2+.

---

## ✅ Verification Checklist

Before organizing a rule into parent+child structure:

- [ ] **Is this a single-concept rule?** → Keep flat at top level
- [ ] **Is this multi-concept (2+ related rules)?** → Create parent + subdirectory
  - [ ] Parent rule at: `_rules/<tier>/<concept>.md`
  - [ ] Child rules at: `_rules/<tier>/<concept>/_<aspect>.md`
  - [ ] Child files use underscore prefix `_<aspect>.md`
  - [ ] Parent rule has contents section with links to `<concept>/_<aspect>.md`
  - [ ] Sibling links within subdirectory use relative paths: `[_file.md](_file.md)`
- [ ] **Is the parent rule >110 lines?** → Consider if splitting is justified
- [ ] **Do you have only 1 child rule?** → Violates 2+ rule; flatten to top level instead
- [ ] **Are all children directly related to parent concept?** → Avoid mixing unrelated rules in one subdirectory

---

## 📝 Documentation Requirements

When creating a multi-concept rule structure:

1. **Parent rule:** Explain purpose, link to all children, guide reader to start with parent
2. **Child rules:** Reference parent and siblings clearly; use relative links
3. **README:** Update `_rules/<tier>/README.md` to show new parent+child structure
4. **CLAUDE.md:** If rule is top-level import, update path from `@~/.claude/_rules/<tier>/<concept>.md` to match parent location

---

## 🔗 Related rules

- **Parent:** `claude_directory_structure.md` — directory organization overview
- **Sibling:** `_claude_directory_naming.md` — naming patterns for files and directories
- **Related:** `writing_style.md` → `_multifile_document_organization.md` — when to split documents into parent + child files (general principle, applies to rules too)
