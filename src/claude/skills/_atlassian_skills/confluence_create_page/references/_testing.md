# Testing & validation

The following test cases validate core skill behavior:

## Test 1: Full interactive (backward compatibility)

```
/confluence_create_page
→ Phase 1: Ask which pattern? (user: general_page)
→ general_page pattern phases: Ask 5 questions (title, creator, status, purpose, sections)
→ Local Draft Review: Write draft, ask for approval
→ Publishing: Create page in Confluence
```

**Expected:** Fully interactive; all current workflows unaffected.

---

## Test 2: Pattern provided (simple bypass)

```
/confluence_create_page general_page
→ Phase 1: SKIP (pattern provided)
→ general_page pattern phases: Ask 5 questions (title, creator, status, purpose, sections)
→ Local Draft Review: Write draft, ask for approval
→ Publishing: Create page in Confluence
```

**Expected:** One fewer prompt. Phase 1 skipped cleanly.

---

## Test 3: Invalid pattern error

```
/confluence_create_page invalid_pattern
→ Error: "Pattern 'invalid_pattern' not found."
→ Available patterns: general_page
→ Proceed with full interactive mode (Phase 1: Ask which pattern?)
```

**Expected:** Clear error; user offered full interactive mode or can retry with valid pattern.

---

## Phase 2 testing

Full metadata bypass (`--title`, `--creator`, `--status`, `--purpose`, `--sections`) and config file support are deferred to Phase 2. See `_roadmap.md` for test specifications.
