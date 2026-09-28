<!-- version: 2.0.0 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-09-28 -->
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
| **Rule** (`_rules/**/*.md`) | Lines 1–3, above the H1 | `<!-- version: 1.0.0 -->` |
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

## 🔗 Related

- `authoring_rules.md` — imports this file; rule template at `~/.claude/_templates/RULE.md.template`
- `authoring_skills.md`, `authoring_agents.md` — apply the placement above
- `_complexity_scoring.md` — sibling shared standard, same "define once" pattern
