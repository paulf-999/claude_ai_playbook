# 🤖 Agent return format

The `code_reviewer` agent must return findings in this structure — one block per finding:

```
FILE: <path>
LINE: <line number in new file>
SEVERITY: Must | Should
ISSUES:
* <issue bullet>
* <additional issue if needed>
SUGGESTED_FIX_LANG: <bash|sql|python|yaml|none>
SUGGESTED_FIX:
<runnable code, or empty>
```

## Rules

- `LINE` — line number in the new file (`side: RIGHT`)
- `SEVERITY` — `Must` is blocking; `Should` is non-blocking
- `ISSUES` — use `*` bullets
- `SUGGESTED_FIX` — omit or leave empty if no concrete code fix applies
- Every finding must anchor to a specific file — do not return general or architectural concerns without a file anchor
