# Versioning Standards (Semver)

Applies to all Claude components — skills, process docs, rules, and CLAUDE.md files.

---

## Skill-level versioning

Map the semver major version to the component's maturity tier:

| Version range | Maturity | Meaning |
|---|---|---|
| `0.x.x` | draft | Exploring the problem space. Breaking changes expected. Not yet depended on. |
| `1.x.x` | tactical | Stable enough to depend on. Solves the known use case reliably. |
| `2+.x.x` | strategic | Production-ready, generalised, fully maintained. |

Version increment rules:

- Patch (`x.x.N`) — bug fixes and minor corrections within a maturity tier
- Minor (`x.N.0`) — new capabilities added without changing the maturity tier
- Major (`N.0.0`) — promotion to the next maturity tier

---

## Repo-level release versioning

GitHub Releases align to phase completions:

| Release | Trigger |
|---|---|
| `v1.0.0` | Phase 1 complete |
| `v2.0.0` | Phase 2 complete |
| `v1.1.0` etc. | Patch or minor work within a phase |

Use semver tags on GitHub Releases. Changelog is generated from merged PR descriptions using the release skill.
