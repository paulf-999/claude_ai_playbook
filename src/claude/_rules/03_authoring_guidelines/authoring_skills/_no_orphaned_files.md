# 🧹 No Orphaned Files

**Purpose:** Every file in a skill directory must earn its place — referenced from `SKILL.md`, another reference doc, the handler, or evals. Files that aren't are dead weight nobody will notice until someone goes looking.

---

## 🎯 Core principle

**If nothing else in the skill mentions a file by name, it isn't part of the skill.** A `patterns/` or `templates/` directory that grew alongside a feature that was later descoped, a draft contract left behind after a rename, a reference doc nobody linked — these accumulate silently because nothing breaks when they're unused, so nothing prompts their removal.

**Why this matters:** found via a real audit (2026-09-19) — `confluence_create_page` had 16 unreachable files (an entire duplicate `templates/` directory, four patterns never wired into `VALID_PATTERNS`, a stale draft `skill.contract.yaml`), `jira_create` had 6 more of the same, and `git_create_pr`'s `SKILL.md` linked to three `reference/` files that had never existed while its one real reference file sat unlinked.

---

## ✅ How to apply

**Before adding a file to a skill directory:**
- Make sure something else in the skill will reference it — a `SKILL.md` link, a mention in another reference doc, or a literal string the handler reads (e.g. a pattern name in `VALID_PATTERNS`).
- If it's speculative ("might need this pattern later"), it doesn't belong yet — per `guiding_principles.md`, add it when the need is real, not before.

**Before removing a file you think is orphaned:**
- Confirm it's not read via a runtime-constructed path (e.g. `f"patterns/{pattern}.md"`) — the pattern *name* itself should still appear somewhere (in a validation list, evals, or `SKILL.md`) if it's genuinely reachable.
- Check `evals.yaml`/`evals.json` — a scenario testing a specific file's behavior counts as a reference.

**Mechanically enforced by `test_no_orphaned_skill_files.py`** — scans every skill under `src/claude/skills/` for files whose name never appears in any of that skill's other content, and separately verifies every `reference/` path a `SKILL.md` names actually exists on disk. Both checks are generic: they run against all current and future skills, not any one skill by name.

**Exempt by design:** `SKILL.md`, `skill.contract.yaml`, `README.md`, `__init__.py`, `conftest.py`, `evals.yaml`, `test_*.py`, and auto-generated artifacts (`__pycache__`, `.coverage`) — these don't need to be "referenced by name" to be legitimate.

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
- `guiding_principles.md` — "Reversible by design" and "no speculative work" — the same reasoning this rule mechanizes for skill files specifically
