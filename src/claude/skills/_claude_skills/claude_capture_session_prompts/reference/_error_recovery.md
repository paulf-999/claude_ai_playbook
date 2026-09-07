# Error Recovery

| Scenario | Root Cause | Solution |
|---|---|---|
| **No history entries found** | history.jsonl empty or date outside recorded range | Verify date is in YYYY-MM-DD format. Check session activity on target date. Inspect history.jsonl: `tail ~/.claude/history.jsonl`. |
| **Malformed JSON in history.jsonl** | Corrupted history entries | Script skips invalid lines (non-blocking). Check for truncated entries at end of file. |
| **Date parsing error** | Invalid date format or non-existent date (e.g., Feb 30) | Use YYYY-MM-DD format (e.g., 2026-08-20). Verify date is valid calendar date. |
| **File write permission denied** | ~/.claude/sessions/ not writable | Check directory permissions: `ls -ld ~/.claude/sessions/`. Ensure user can write to ~/.claude/. |
| **Categorization inaccurate** | Heuristics miss edge cases or context | Manual refinement in markdown post-generation. Update heuristics in script if pattern repeats. |
| **Script not found** | ~/.claude/scripts/ directory missing or script moved | Verify script exists: `ls ~/.claude/scripts/capture_session_prompts.py`. Reinstall or update path. |
| **Python version too old** | Python <3.6 | Verify Python version: `python3 --version`. Install Python 3.6+. |
| **Timestamp offset incorrect** | Dublin timezone (UTC+1) not applied | Script uses Dublin time by default. Adjust TZ env var if needed: `TZ=Europe/Dublin python3 ...`. |
