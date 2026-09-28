<!-- version: 1.0.0 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-09-28 -->
# 🚫 Rule Common Mistakes & Anti-Patterns

**Purpose:** The rule-authoring mistakes this config has actually shipped, shown as wrong/right pairs so they aren't repeated.

---

## ❌ **Unwired child file**

**Wrong:** the parent names a child in prose ("see `_decision_making.md` for details") but has no `@import` line for it.

**Right:** every child the parent describes gets a real `@~/.claude/_rules/<tier>/<parent>/_<child>.md` line.

- **Why:** a child that is only named in prose is never loaded, and nothing warns you.
- **Caught by:** `test_always_on_reachability.py` fails the build for any unreachable file under `01_essentials/`–`04_claude_reference/`.

---

## ❌ **Hardcoded path or username**

**Wrong:** `source ~/.claude/_templates/utils/shell_utils.sh` or `/home/paul/.claude/hooks/...` in a hook or test.

**Right:** resolve the config directory at runtime, using `CLAUDE_DIR` in Python or the script's own location in shell.

- **Why:** these passed on one machine and failed silently on another (see `portable_paths.md`, 2026-09-17 incidents).

---

## ❌ **Stale tier names**

**Wrong:** a rule or test refers to `02_claude_internal/`, `03_lazy_load/` or another directory name from before the tier reorganisation.

**Right:** use the current `01_essentials/`–`05_lazy_load/` names, and check the directory tree instead of copying a path from an older file.

- **Why:** PR #94 had to replace pre-reorg names across the config, because the old ones had been copied from file to file.

---

## ❌ **Too long, not split**

**Wrong:** a single rule file grows past 110 lines "because it's all one topic".

**Right:** split it into a parent index plus `_<aspect>.md` children in a `<parent>/` subdirectory, each imported from the parent.

- **Why:** `test_rules_structure.py` enforces the 110-line limit, and long files bury the part the reader needs.

---

## ❌ **Missing or unbumped metadata header**

**Wrong:** a new rule with no header, or an edited rule that still shows its old `updated` date and `version`.

**Right:** lines 1–3 carry `version`, `created` and `updated`, and every edit bumps `updated` and `version` (see `_claude_config_metadata.md`).

- **Why:** the header is the staleness signal for audits, and PR #97 had to add it to every rule after the fact.

---

## ❌ **Rule without evidence**

**Wrong:** "Add a rule so Claude always does X, in case it ever comes up."

**Right:** name the incident, PR or repeated failure that prompted the rule, and record it in the rule itself when it's worth keeping.

- **Why:** speculative rules cost tokens every session without preventing anything (see `guiding_principles.md`, "Intentionality gates everything").

---

## 🔗 Related

- Parent: `authoring_rules.md` — pre-creation checklist, creation steps and quality gates
- Sibling: `_hard_gates_checklist.md` — the tick-box check to run before finishing a rule
