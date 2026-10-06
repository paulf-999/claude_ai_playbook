<!-- version: 2.0.1 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-10-06 -->
# 🚫 Rule Common Mistakes & Anti-Patterns

**Purpose:** The rule-authoring mistakes this config has actually shipped, shown as wrong/right pairs so they aren't repeated.

---

## ❌ **Child in the wrong folder for how it should load**

**Wrong:** an on-demand child sits under `rules/`, where it loads every session, or an always-on child sits in `_rules_lazy_load/`, where nothing loads it.

**Right:** an always-on child sits in `rules/<tier>/<parent>/`, named in a `**Loads on its own from:**` line; an on-demand child sits in `_rules_lazy_load/<parent>/`, named in a `**Read on demand:**` pointer.

- **Why:** Claude Code loads every `.md` under `rules/` and nothing outside it, so the folder decides what loads, silently.
- **Caught by:** `test_always_on_reachability.py` fails the build on a README, `_lazy_load/` folder or `@import` under `rules/`, or a pointer that leads nowhere.

---

## ❌ **Hardcoded path or username**

**Wrong:** `source ~/.claude/_templates/utils/shell_utils.sh` or `/home/paul/.claude/hooks/...` in a hook or test.

**Right:** resolve the config directory at runtime, using `CLAUDE_DIR` in Python or the script's own location in shell.

- **Why:** these passed on one machine and failed silently on another (see `portable_paths.md`, 2026-09-17 incidents).

---

## ❌ **Stale tier names**

**Wrong:** a rule or test refers to `02_claude_internal/`, `03_lazy_load/` or another directory name from before the tier reorganisation.

**Right:** use the current `rules/01_essentials/`–`04_path_scoped/` and `_rules_lazy_load/` names, and check the directory tree instead of copying a path from an older file.

- **Why:** PR #94 had to replace pre-reorg names across the config, because the old ones had been copied from file to file.

---

## ❌ **Too long, not split**

**Wrong:** a single rule file grows past 110 lines "because it's all one topic".

**Right:** split it into a parent index plus `_<aspect>.md` children in a `<parent>/` subdirectory, each named from the parent.

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
