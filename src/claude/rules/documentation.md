# 📝 Rules — Documentation updates

Applies when updating any document: style guides, CLAUDE.md files, rules, CODEOWNERS,
Confluence pages, PR descriptions, READMEs, and any other human-facing file.

---

## Before making changes

- State what you will change and why, before touching the file.
- If a request implies related changes that weren't explicitly asked for, confirm scope first.
- If unsure whether something is in scope: ask, do not include.

---

## Minimal diff

- Change only what was explicitly requested.
- Do not tidy adjacent content, correct unrelated issues, or add sections not asked for.
- Do not add entries, examples, or headings beyond the scope of the request.
- One request = one diff. Do not batch opportunistic improvements into the same change.

---

## Self-validation checklist

Before presenting output, verify each item. If any check fails, fix or flag it:

| # | Check |
|---|---|
| 1 | Every change made was explicitly requested |
| 2 | Nothing was added that wasn't asked for |
| 3 | No instance-specific details (names, regions, environments) appear in a general-purpose document |
| 4 | Output is consistent with the relevant style guide |
| 5 | If the total diff is 1–3 lines: flag that a direct commit may be more appropriate than a PR |

---

## Presentation format

- Show a diff (before/after for each changed section), not just the final result.
- For each change, one sentence explaining why it was made.
- Do not narrate or summarise beyond the diff — the diff speaks for itself.

---

## General-purpose documents

Documents that encode shared principles — style guides, rules, CLAUDE.md, CODEOWNERS,
READMEs, skill files:

- Must not contain instance-specific examples: names of individuals, team members, specific
  environment values, or region codes.
- Personal context belongs in memory files or comments, not in shared documents.
- CODEOWNERS: do not add entries for `archive/`, `docs/`, or paths that do not need explicit
  ownership enforcement.
