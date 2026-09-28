<!-- version: 1.0.0 | created: 2026-09-28 | updated: 2026-09-28 -->
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

## 📍 Placement per artefact type

| Artefact | Where | Format |
|---|---|---|
| **Rule** (`_rules/**/*.md`) | Line 1, above the H1 | `<!-- version: 1.0.0 \| created: YYYY-MM-DD \| updated: YYYY-MM-DD -->` |
| **Skill** (`SKILL.md`) | Existing YAML frontmatter | Add `created:` and `updated:` beside the existing `version:` |
| **Agent** (`AGENT.md`) | Existing YAML frontmatter | Add `created:` and `updated:` beside the existing `version:` |
| **Hook** (`hooks/*.sh`) | Line 2, after the shebang | `# version: 1.0.0 \| created: YYYY-MM-DD \| updated: YYYY-MM-DD` |

- **Why native placement:** skills and agents already carry `version` in frontmatter, so a separate comment line would duplicate it.
- **Why a one-line comment for rules:** it keeps rules near the 110-line cap within limit, and the H1 check already allows a line above it.
- **Token cost:** Claude Code strips HTML comments from `CLAUDE.md`, but the docs don't say whether this applies to `@`-imported files — assume ~20 tokens per imported rule.
- **Frontmatter safety:** Claude Code silently ignores unrecognised frontmatter keys in skills and agents, so `created`/`updated` are safe to add.
- **Tests:** tests keep their own header — see `testing/_test_metadata.md`.

---

## 🔗 Related

- `authoring_rules.md` — imports this file; rule template at `~/.claude/_templates/RULE.md.template`
- `authoring_skills.md`, `authoring_agents.md` — apply the frontmatter placement above
- `_complexity_scoring.md` — sibling shared standard, same "define once" pattern
