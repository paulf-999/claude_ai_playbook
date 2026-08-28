# 📛 Naming

**Purpose:** Establish self-describing, unambiguous naming conventions that enable readers to understand files and identifiers without additional context.

Applies to all files, directories, and identifiers Claude creates or proposes.

## 🎯 Overview

All naming conventions follow four foundational principles:
1. **Self-describing** — names must be unambiguous without context
2. **Offer options** — propose candidates before deciding (never unilateral)
3. **snake_case** — lowercase, words separated by underscores
4. **Name for scale** — fit the likely higher grouping, not just today's problem

These principles apply across all artefacts: files, directories, hooks, skills, rules, and identifiers.

## 📋 Contents

- [Overview](#-overview)
- [Load details on-demand](#-load-details-on-demand)
- [Related rules](#-related-rules)

---

## 📚 Load details on-demand

This file provides the overview and entry point for naming conventions across all Claude config artefacts. Detailed guidance is organized into child files by topic:

- **🎯 Foundational Principles** — Self-describing, offer options, snake_case, name for scale
  - `_naming_principles.md` — Core concepts that apply to all naming
- **🏷️ Naming Patterns** — Detailed patterns for specific artefact types (hooks, skills, rules)
  - `_claude_naming_patterns.md` — Detailed patterns for hooks, skills, and rules
- **🗂️ Directory Structure & Naming** — Directory organization, user-created vs. auto-generated, directory naming
  - `~/.claude/_rules/01_essentials/conventions/claude_directory_structure.md` — Full directory structure and naming conventions for directories

---

## 🔗 Related rules

- `claude_directory_structure.md` — Directory organization and naming conventions for `~/.claude/`
- `authoring_rules.md` — Rule naming standards and directory placement (01_essentials, 02_claude_standards, 04_lazy_load)
- `writing_style.md` → `_multifile_document_organization.md` — File organization conventions; when to split into parent + child files
