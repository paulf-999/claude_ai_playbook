# Bypass arguments

This skill supports simple argument bypass: provide a pattern name to skip Phase 1 (pattern selection).

## Quick examples

```
# Fully interactive (default behavior)
/confluence_create_page

# Pattern pre-selected, rest interactive
/confluence_create_page general_page
```

## Pattern argument

| Argument | Example | Purpose |
|---|---|---|
| `<pattern>` | `general_page` | Pattern name. Skips Phase 1 pattern selection. |

## ⚙️ Bypass Logic

**Pattern argument provided?** → Skip Phase 1 (pattern selection)
**Otherwise:** Run all phases interactively

## ⚠️ Critical Constraint

**Draft review is always mandatory.** Even with pattern pre-selected, the skill will:
1. Run the pattern's interactive phases
2. Generate a local draft markdown file in `~/_drafts/confluence/`
3. Ask for your approval before publishing to Confluence

This ensures no page lands in Confluence without human review.

## 🛣️ Phase 2+ Roadmap

Full metadata bypass (`--title`, `--creator`, `--status`, `--purpose`) and section pre-fill (`--sections`) are planned for Phase 2. See `_roadmap.md` for detailed specifications.
