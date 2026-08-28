# 🏗️ Directory Organization — `~/.claude/`

**Purpose:** Define what directories exist in the Claude config, their purpose, and the distinction between user-created and auto-generated directories.

---

## 📁 Directory types

- **User-created dirs:** underscore prefix — e.g. `_docs/`, `_rules/`, `_templates/`, `_reference/`, `_tests/`
  - **Pattern:** `_<name>/` — user explicitly creates these to organize content
  - **Note:** These directories are tracked in version control and intentionally maintained
- **Claude Code auto-generated dirs:** no prefix — e.g. `backups/`, `memory/`, `sessions/`, `projects/`
  - **Pattern:** `<name>/` — Claude Code creates these automatically; you should not manually create them
  - **Note:** These are excluded from version control (`.gitignore`)

---

## 📂 The Full Tree

```
~/.claude/
├── CLAUDE.md                    # Entry point: config imports and comments
├── aliases.md                   # Quick reference for shortcuts
├── settings.json                # Claude Code settings (permissions, hooks, etc.)
├── keybindings.json             # Keyboard binding customization
│
├── _rules/                      # Core rules (always-on or lazy-load)
│   ├── 01_essentials/                 # Blocking/safety rules (always-on imports)
│   │   ├── behaviour.md
│   │   ├── guiding_principles.md
│   │   ├── naming_standards.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   ├── writing_style.md
│   │   ├── authoring_skills.md
│   │   ├── authoring_rules.md
│   │   ├── claude_directory_structure.md
│   │   ├── claude_directory_structure/
│   │   │   ├── _claude_directory_organization.md
│   │   │   └── _claude_directory_naming.md
│   │   ├── naming_standards/
│   │   │   ├── _naming_principles.md
│   │   │   └── _claude_naming_patterns.md
│   │   ├── behaviour/
│   │   │   └── _decision_making.md
│   │   ├── skill_authoring/
│   │   │   ├── _skill_structure_contract.md
│   │   │   ├── _skill_quality_checklist.md
│   │   │   └── _skill_review_framework.md
│   │   ├── testing/
│   │   │   ├── _testing_design_pattern.md
│   │   │   ├── _testing_anti_patterns.md
│   │   │   ├── _testing_file_organization.md
│   │   │   └── _testing_maintenance.md
│   │   └── writing_style/
│   │       └── _multifile_document_organization.md
│   │
│   ├── 02_claude_standards/      # How Claude operates (always-on imports)
│   │   ├── claude_efficiency.md
│   │   ├── external_system_access.md
│   │   ├── git.md
│   │   ├── loading_strategy_rules.md
│   │   ├── memory.md
│   │   ├── security_guardrails.md
│   │   └── mcp_trust_model.md
│   │
│   └── 04_lazy_load/            # Domain-specific rules (loaded on-demand)
│       ├── style_guide_standards/
│       │   ├── sql.md
│       │   ├── airflow.md
│       │   ├── dbt.md
│       │   └── [other domain style guides]
│       ├── automation_controls.md
│       ├── [other domain-specific rules]
│
├── _tests/                      # Test files for validation
│   ├── rules/                   # Tests for rule enforcement
│   ├── hooks/                   # Tests for hook behavior
│   ├── skills/                  # Tests for skill functionality
│   └── test_file_structure_compliance.py
│
├── _templates/                  # Templates for creating new artefacts
│   ├── skills/
│   │   ├── SKILL.md.template
│   │   └── skill.contract.yaml.template
│   └── RULE.md.template
│
├── _reference/                  # Reference documentation (evergreen, no date prefix)
│   ├── claude_config_architecture.md
│   ├── claude_config_architecture/
│   │   ├── _security.md
│   │   ├── _testing.md
│   │   ├── _adding_rules.md
│   │   └── [other deep-dive docs]
│   └── [other reference docs]
│
├── _docs/                       # Additional documentation
├── agents/                      # Custom sub-agents for specific tasks
├── hooks/                       # Enforcement and style-guide hooks
├── skills/                      # Reusable skills (slash commands)
├── wip/                         # Work-in-progress features
│
├── backups/                     # 🔧 Auto-generated: backup files
├── memory/                      # 🔧 Auto-generated: persistent memory/knowledge graph
├── projects/                    # 🔧 Auto-generated: per-project context
└── sessions/                    # 🔧 Auto-generated: session transcripts
```

---

## 🔀 When to create a subdirectory

Create a subdirectory when **two or more related files** share the same theme and benefit from grouping:

- ✅ Create when: `naming_standards/` contains `_naming_principles.md` + `_claude_naming_patterns.md` (related, reusable grouping)
- ✅ Create when: `claude_directory_structure/` contains `_claude_directory_organization.md` + `_claude_directory_naming.md` (organization + naming are paired concerns)
- ❌ Avoid when: one file stands alone (e.g. a single style guide doesn't need a folder)

**Note:** Prefer flat `_rules/*.md` for standalone rules; introduce a subdir only when the grouping is clear and reusable.

---

## ✅ Rules

- **User-created directories always have underscore prefix** — `_rules/`, `_tests/`, `_templates/`, `_reference/`, `_docs/`
- **Auto-generated directories have no prefix** — `backups/`, `memory/`, `sessions/`, `projects/`
- **When unsure if a directory is auto-generated:** Check `~/.claude/.gitignore` — auto-generated dirs are typically excluded
- **Never create files directly in `~/.claude/` root** — they belong in `_docs/`, `_reference/`, or a domain-specific subdirectory

---

## 🔗 Related rules

- **Parent:** `claude_directory_structure.md` — entry point; organization and naming overview
- **Sibling:** `_claude_directory_naming.md` — naming patterns for files and directories
- **Related:** `writing_style.md` → `_multifile_document_organization.md` — when to split documents into parent + child files
- **Related:** `authoring_rules.md` — directory placement for new rules (01_essentials, 02_claude_standards, 04_lazy_load)
