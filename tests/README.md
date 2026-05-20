# 🧪 Tests

Automated tests for the Claude AI playbook. Run with `make test`.

---

## 🏗️ Structural tests

- **Context:** Claude's behaviour is configured through a collection of markdown files — skills, agents, rules, commands, process files, and style guides.
- **Purpose:** Catch broken or missing config files before changes are merged — these tests do not cover logic or behaviour.

| File | What it checks |
|---|---|
| `test_skills_structural.py` | Each skill definition file exists and is correctly named and formatted |
| `test_agents.py` | Each agent definition file exists and contains the required sections |
| `test_commands.py` | Each command file exists and all links within the command index resolve |
| `test_process.py` | Required session and settings files exist and are correctly formatted |
| `test_rules.py` | Each rules file exists and all links within the rules index resolve |
| `test_style_guide_standards.py` | All file references within style guide files resolve to files that exist on disk |

---

## 🎯 Claude skill tests — behavioural (`skills/`)

- Validate the *rules* embedded in skill prose
- Covers the deterministic logic a skill instructs Claude to follow
- See [`skills/README.md`](skills/README.md) for details.

---

## 🪝 Claude hook tests (`hooks/`)

- Unit tests for Claude hook scripts in `src/claude/hooks/`
- See [`hooks/README.md`](hooks/README.md) for details.

---

## 🛠️ Maintenance script tests (`tooling/`)

- Unit tests for standalone Python scripts in `src/sh/claude/`
- Invoked via `make lint_tags` and `make audit_components`
- Not Claude components — repo maintenance tools
- See [`tooling/README.md`](tooling/README.md) for details.
