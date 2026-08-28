# 📋 Decisions — CLAUDE.md

## 🔗 Composition file pattern

- **Why:** Rules evolve independently — separate imported files mean changes can be
  tracked and committed to git without touching CLAUDE.md itself.
- **Note:** CLAUDE.md is a thin orchestration file only. All content belongs in
  imported files; nothing goes inline.

## 📁 `_rules/` directory

- **Why:** Files in `_rules/` are Claude-facing behavioral instructions, categorically
  different from `_docs/` which is human-facing documentation.
  - Separation keeps the distinction clear and makes git tracking cleaner.
- **Note:** Underscore prefix marks it as user-created per the `~/.claude/` naming
  convention.

## 📄 `writing_style.md` in `_rules/` not `_docs/`

- **Why:** Writing style is a behavioral rule — Claude writes files and must
  follow it. It belongs in `_rules/` alongside other behavioral instructions.

## 🧠 `memory/MEMORY.md` imported first

- **Why:** Personal context loads before behavioral rules, so memories and corrections
  are available as the most immediate framing when rules are applied.
