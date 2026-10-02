<!-- version: 2.3.0 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-10-02 -->
# 🗂️ Claude Config Metadata

**Purpose:** One shared per-file metadata standard (version, created, updated) for every authored artefact type in this config — rules, skills, agents, and hooks — defined once here so each domain references it instead of redefining it.

---

## 📐 The three fields

| Field | Format | Why it exists |
|---|---|---|
| **version** | Semver `X.Y.Z` | Shows how much the artefact has changed over its life |
| **created** | `YYYY-MM-DD` | Shows its age — git history doesn't travel with the live `~/.claude/` copy |
| **updated** | `YYYY-MM-DD` | Flags staleness — the main signal in audits and 6-month resets |

- **New artefact:** `version: 1.0.0`, with `created` and `updated` both set to today.
- **Every edit:** set `updated` to today and bump `version` — never change `created`.
- **MAJOR:** guidance or behaviour reversed or removed.
- **MINOR:** guidance or behaviour added.
- **PATCH:** wording or typo fix only.
- **Limit:** these fields show when a file *changed*, not whether it gets *used* — usage needs transcript analysis.

---

## 📍 One format, three lines, every artefact

Each field sits on its own line, in the order version → created → updated, wrapped in the file type's comment syntax:

| Artefact | Where | Comment syntax |
|---|---|---|
| **Rule** (`_rules/**/*.md`) | Lines 1–3, above the H1, or straight after `paths:` frontmatter for a path-scoped rule | `<!-- version: 1.0.0 -->` |
| **Skill** (`SKILL.md`) | The 3 lines straight after the frontmatter's closing `---` | `<!-- version: 1.0.0 -->` |
| **Agent** (`AGENT.md`) | The 3 lines straight after the frontmatter's closing `---` | `<!-- version: 1.0.0 -->` |
| **Hook** (`hooks/*.sh`) | Lines 2–4, after the shebang | `# version: 1.0.0` |

```markdown
<!-- version: 1.0.0 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-09-28 -->
```

- **Why HTML comments in markdown:** a `#` line would render as an H1 heading.
- **Why after the frontmatter:** YAML frontmatter must start on line 1 to be parsed, so skills and agents place the header just below it.
- **Single source of version:** skills and agents drop `version:` from frontmatter; a skill's `skill.contract.yaml` version must match its header.
- **Line limit:** the 3 header lines don't count toward the 110-line rule limit.
- **Token cost — zero:** Claude Code strips HTML comments from `@`-imported files too, verified 2026-09-28 (300 header lines imported → no change in input tokens, and a hidden marker was invisible to the model).
- **Tests:** tests keep their own header — see `testing/_test_metadata.md`.

---

## 🎯 Rule-only usage fields

Entry-point rules add up to three more lines straight after `updated`:

```markdown
<!-- applies_to: **/*.py, **/*.pyi -->
<!-- miss_cost: high — commits secrets if missed -->
<!-- loading: always-on — secrets can turn up in any session -->
```

- **applies_to:** comma-separated globs for the files whose sessions need the rule, or `*` alone for every session.
  - **Required:** on every always-on entry point (tiers 01–04).
  - **Lazy rules:** optional, since `paths:` frontmatter or the audit's built-in defaults apply otherwise.
- **miss_cost:** `high` (safety, security, data loss or a silent wrong result), `medium` (rework the user would catch) or `low` (style drift), then ` — ` and a reason.
- **loading:** `always-on` (tiers 01–04), `path-scoped` (lazy with `paths:` frontmatter) or `lazy` (any other lazy rule), then ` — ` and a one-line reason it loads that way.
  - **Matches the folder:** `test_rule_headers.py` fails when the value disagrees with where the rule lives, so it can't drift.
  - **Required:** on every always-on entry point.
- **Read by:** `make audit_rule_usage` reads `applies_to` and `miss_cost`, while `loading` is for people reading the rule.
- **Entry points only:** a child file inherits its parent's fields.
- **No dates:** last-used dates live in the audit's history CSV, so running an audit never edits a rule.
