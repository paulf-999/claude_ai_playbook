---
name: release
description: Create a GitHub Release for a completed phase. Checks all phase issues are closed, generates a changelog from merged PRs, and cuts a release via gh CLI. Invoke as /release <phase> (e.g. /release 1).
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

# 🚀 Release

Create a GitHub Release after a phase is complete. Checks issue state, generates a changelog from merged PRs, and publishes the release via `gh release create`.

**Invocation:** `/release <phase>` — e.g. `/release 1` for phase 1.

## 🏷️ Versioning

| Phase | Release tag |
|---|---|
| 1 | `v1.0.0` |
| 2 | `v2.0.0` |
| N | `vN.0.0` |

Patch and minor increments within a phase follow standard semver (e.g. `v1.1.0`, `v1.0.1`). The skill detects the latest existing tag and proposes the next version — the user can override before the release is created.

---

## ⚠️ Pre-check — verify tools

Before doing anything else:

1. Run `git status` to confirm Bash is available and we are inside a git repo. If not, stop.
2. Run `gh auth status`. If not authenticated, stop and tell the user:
   > "This skill requires `gh` CLI authenticated to GitHub. Run `gh auth login` and try again."

---

## 🔍 Phase 1 — Check issue state

Extract the phase number from `$ARGUMENTS` (the text after `/release`). If no phase number is provided, ask the user: "Which phase are you releasing? (e.g. 1, 2)"

Run:

```bash
gh issue list --label "phase-<N>" --state open --json number,title
```

If any open issues are returned, list them and stop:

```
X issue(s) are still open for phase N:

  #42 — Add weekly manager updates skill
  #38 — MCP installation approach revision

Resolve or close these before releasing phase N.
```

If the command returns no issues (all closed), proceed to Phase 2.

---

## 🏷️ Phase 2 — Determine release version

Get the latest existing tag:

```bash
git describe --tags --abbrev=0 2>/dev/null || echo ""
```

If no tags exist, the latest tag is considered empty (first release).

Propose the release tag:
- If releasing phase N and no prior `vN.x.x` tag exists: propose `vN.0.0`
- If a `vN.x.x` tag already exists: propose incrementing the minor version (e.g. `v1.0.0` → `v1.1.0`)

Show the proposal and wait for confirmation or override:

```
Proposed release tag: v1.0.0
Latest existing tag:  (none)

Accept, or enter a different tag:
```

---

## 📝 Phase 3 — Generate changelog

Get merged PRs since the last release tag. If no prior tag exists, get all merged PRs:

```bash
# With a prior tag — get PRs merged after the tag date
LAST_TAG_DATE=$(git log -1 --format=%aI <last_tag> 2>/dev/null)
gh pr list --state merged --limit 100 \
  --json number,title,labels,mergedAt \
  | jq --arg since "$LAST_TAG_DATE" \
    '[.[] | select(.mergedAt > $since)] | sort_by(.mergedAt)'

# Without a prior tag — get all merged PRs
gh pr list --state merged --limit 100 \
  --json number,title,labels,mergedAt \
  | jq 'sort_by(.mergedAt)'
```

Group PRs by their Conventional Commits type prefix in the title (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`). PRs without a recognisable prefix go under **Other**.

Format the changelog:

```markdown
## <tag> — <YYYY-MM-DD>

### Features
- <PR title> (#N)

### Fixes
- <PR title> (#N)

### Chores
- <PR title> (#N)
```

Display the full changelog and ask the user to confirm or edit before proceeding.

---

## 🚀 Phase 4 — Create release

Write the changelog to a temp file and create the release:

```bash
cat > /tmp/release_notes.md << 'NOTES'
<changelog>
NOTES

gh release create <tag> \
  --title "<tag>" \
  --notes-file /tmp/release_notes.md
```

On success, report the release URL returned by `gh release create`.

> TODO (tactical): group changelog by theme tag (from doc4 PR auto-tagging convention) rather than commit type prefix.
> TODO (tactical): auto-trigger after PR merge via a hook — check if all phase issues closed and prompt for release without manual invocation.
> TODO (tactical): support pre-release tags (e.g. `v1.0.0-rc.1`).
> TODO (tactical): handle the case where `gh pr list` pagination cuts off older PRs.
