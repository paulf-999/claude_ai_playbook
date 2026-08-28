# 🪝 Hook naming conventions — decisions

## 📁 Prefix over subdirectory grouping

- **Why:** Claude Code hooks cannot be nested into subdirectories — all hooks live
  flat under `~/.claude/hooks/`. Prefixes are the only available grouping mechanism.
- **How to apply:** group hooks by purpose using a standard prefix; see
  `_rules/naming_conventions.md` for the prefix table.

## 🏷️ `enforcement_` as the prefix for rule-enforcing hooks

- **Why:** hooks that block violations or inject compliance reminders share a single
  concern — enforcing a rule. Grouping them under `enforcement_` makes that intent
  unambiguous at a glance.
- **Note:** this prefix covers both PreToolUse (hard block) and PostToolUse
  (reminder injection) hooks — the enforcement intent is the same regardless of
  lifecycle event.
- **How to apply:** name any hook that enforces a `_rules/` file as
  `enforcement_<rule_name>.sh`.

## ⚠️ Origin: badly named file incident

- **Why this matters:** a hook named `principle_guard.py` was proposed without
  consulting `naming_conventions.md` first — too vague, not self-describing.
- **Fix:** `enforcement_naming_convention.sh` now blocks new `~/.claude/` file
  creation and injects `naming_conventions.md` for review before proceeding.
