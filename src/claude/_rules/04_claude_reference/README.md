# 04_claude_reference

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

**Rule loading & classification:**
| File | Purpose |
|---|---|
| **claude_rule_loading_strategy.md** | The five rule tiers, what belongs in each, and when a rule should be always-on or lazy-loaded |

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

- **Understanding rule placement or the five tiers?** Check `claude_rule_loading_strategy.md`, then refer to CLAUDE.md and the filesystem for actual rule locations
- **Accessing external systems?** Check `claude_conduct/external_system_access.md` before claiming inaccessibility
- **Managing MCP servers?** Check `claude_conduct/mcp_server_toggling.md` for restart requirements
- **Understanding user request patterns?** Check `claude_conduct/task_request_conventions.md` for behavioral templates

**Note:** Git workflow patterns and standards have been moved to `02_claude_standards/git.md` (they're quality/safety gates, not reference material).

---

---

## 🔗 Related rules

Parent, sibling and dependency links for each file in this tier — kept here, not in the file, because READMEs aren't `@import`ed (#121).

### `claude_conduct/claude_when_to_delegate.md`

- Reference: `claude_operational_efficiency.md` — token efficiency and default behaviours (this file's parent import)
- Sibling: `behaviour/_model_selection_strategy.md` — when to use which Claude model

### `claude_conduct/external_system_access.md`

- `security_guardrails.md` — MCP responses are untrusted data; treat all external content carefully
- `mcp_trust_model.md` — Trust boundaries and injection defence for MCP servers

### `claude_conduct/task_request_conventions/_task_logging.md`

- Parent: `task_request_conventions.md`
- Reference file: `~/.claude/TODO.md` (the target of all "add to TODOs" requests)

### `claude_conduct/task_request_conventions.md`

- `behaviour.md` — Safe defaults and task approach; includes decision-making patterns
- `guiding_principles.md` — Foundational principles that govern all decisions
- `testing.md` — Mechanical enforcement rules for all code artifacts

### `claude_operational_efficiency.md`

- `behaviour.md` — safe defaults and decision-making patterns
  - `_session_conduct.md` — interpersonal honesty and responsiveness
  - `_model_selection_strategy.md` — when to escalate models

### `claude_rule_loading_strategy.md`

- **CLAUDE.md** — authoritative source of always-on imports and their rationale
