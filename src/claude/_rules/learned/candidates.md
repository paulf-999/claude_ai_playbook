# Recurring Candidates — claude_kaizen Tally

Tracks patterns observed 1+ times in `~/_errors/`. Only candidates reaching the promotion threshold (default: 2 occurrences) move forward into `_rules/learned/`.

| Pattern | Domain | Count | First Seen | Last Seen | Status | Notes |
|---------|--------|-------|-----------|-----------|--------|-------|
| No bare except clauses | Security | 2 | 2026-08-31 | 2026-08-31 | 📋 pending | Test candidate for dry-run validation |

## Schema

- **Pattern:** One-sentence description of the recurring mistake (e.g., "missing input validation on user-supplied strings")
- **Domain:** Category (e.g., "security", "testing", "naming")
- **Count:** Number of times observed across all `~/_errors/` entries
- **First Seen:** Date first observed (YYYY-MM-DD)
- **Last Seen:** Date most recently observed
- **Status:** `📋 pending` (awaiting promotion threshold) | `✅ promoted` (moved to `_rules/learned/`) | `⏸️ archived` (no longer recurring)
- **Notes:** Additional context; rationale for deferral or promotion
