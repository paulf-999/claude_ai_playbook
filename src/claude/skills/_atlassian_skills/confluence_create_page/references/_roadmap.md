# Phase 2 Roadmap

- Command-line metadata arguments (`--title`, `--creator`, `--status`, `--purpose`, `--space`, `--sections`)
- Additional patterns (sprint goals, incident report, design decision)
- Config file support (`--config <path>`)

See Linear or GitHub issues for detailed planning.
5. **Determine skip logic** — if all metadata fields provided, skip pattern phases 1-2; if sections provided, skip phase 3
6. **Mandatory draft review** — always run, even with full bypass

## Test plan

See `_testing.md` for Phase 1 tests. Phase 2 tests to add:

- **Test 4:** Pattern + metadata, sections interactive
- **Test 5:** Full bypass path (all args provided) — verify draft review still executes
- **Test 6:** Malformed JSON sections — verify error handling
- **Test 7:** Config file bypass — verify merge logic

## Success criteria

✅ Pattern argument correctly skips Phase 1
✅ Metadata args correctly skip pattern phases
✅ Sections arg correctly skips section gathering
✅ Config file parsing works with valid JSON
✅ Invalid status/malformed JSON produce clear errors
✅ Draft review always executes (cannot be bypassed)
✅ All tests pass without breaking backward compatibility

---

## Phase 3+ — Pattern expansion & strategic maturity

### Multi-pattern support

Implement and test: how_to, requirements, incident_report, design_decision, and data platform patterns (sprint_goals, platform_assessment, etc.).

### Strategic maturity

- Full coverage of edge cases (orphaned sections, nested pages, page parent resolution)
- Comprehensive error handling (permission denied, space not found, quota exceeded)
- Complete test suite with integration tests against a Confluence sandbox
- Documentation and best-practices guide for pattern authors

---

## Deferred decisions

**Wide view toggle:** Cannot be set via API. Document that users should toggle **Page width → Wide** in the Confluence editor after publishing.

**Named individuals:** Constraint remains: pages must use role descriptors, not individual names.

---
