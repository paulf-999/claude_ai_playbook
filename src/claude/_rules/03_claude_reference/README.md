# 03_claude_reference

**Purpose:** Technical and meta-knowledge about how Claude Code and the config system work.

**Scope:** Reference material for understanding the platform and system architecture (not for general audience). Guidance on how to implement standards; platform/system knowledge.

---

## 📋 Structure

**Top-level (reference index):**
| File | Purpose |
|---|---|
| **README.md** | This file; directory overview |

**claude_conduct/ (Operational conduct guidance):**
| File | Purpose |
|---|---|
| **external_system_access.md** | How to safely access external systems; check tool availability before claiming inaccessibility |
| **mcp_server_toggling.md** | Why Claude Code must be restarted after toggling MCP servers; recovery steps |
| **task_request_conventions.md** | Behavioral conventions for recurring user request types (task logging, hook proposals) |
| **task_request_conventions/_task_logging.md** | Task logging patterns for managing in-progress work |
| **task_request_conventions/_hooks_decision_framework.md** | Framework for proposing new hooks vs. rules |

**claude_rule_system/ (Rule loading & classification):**
| File | Purpose |
|---|---|
| **claude_rule_loading_strategy.md** | Lazy-load principle; points to authoritative sources (CLAUDE.md, filesystem) |
| **claude_rule_classification.md** | Four-tier directory structure for rules (01_essentials, 02_claude_standards, 03_claude_reference, 04_lazy_load) |

---

## 🔍 Scope: System/platform knowledge, not user conventions

These rules explain **how the Claude config system works** and guide Claude's implementation of standards.

**Examples:**
- ✅ "How to load rules (always-on vs. lazy-load)" (System knowledge)
- ✅ "How to access external systems safely" (Platform guidance)
- ✅ "Git workflow patterns for this repo" (Workflow/process)
- ❌ NOT "Use type hints in Python" (That's user-facing code standards)
- ❌ NOT "Prompt injection defence" (That's foundational safety, in 02_claude_standards)

---

## 🚀 How to use these rules

- **Understanding rule placement?** Check `claude_rule_system/claude_rule_loading_strategy.md` for the lazy-load principle, then refer to CLAUDE.md and the filesystem for actual rule locations
- **Understanding rule tier organization?** Check `claude_rule_system/claude_rule_classification.md` for the four-tier system
- **Accessing external systems?** Check `claude_conduct/external_system_access.md` before claiming inaccessibility
- **Managing MCP servers?** Check `claude_conduct/mcp_server_toggling.md` for restart requirements
- **Understanding user request patterns?** Check `claude_conduct/task_request_conventions.md` for behavioral templates

**Note:** Git workflow patterns and standards have been moved to `02_claude_standards/git.md` (they're quality/safety gates, not reference material).

---
