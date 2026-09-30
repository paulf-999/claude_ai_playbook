# Error Recovery

| Scenario | Root Cause | Solution |
|---|---|---|
| **No history entries found** | history.jsonl empty or date outside recorded range | Verify date is in YYYY-MM-DD format. Check session activity on target date. Inspect history.jsonl: `tail "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/history.jsonl"`. |
| **Malformed JSON in history.jsonl** | Corrupted history entries | Script skips invalid lines (non-blocking). Check for truncated entries at end of file. |
| **Date parsing error** | Invalid date format or non-existent date (e.g., Feb 30) | Use YYYY-MM-DD format (e.g., 2026-08-20). Verify date is valid calendar date. |
| **File write permission denied** | ~/_sessions/ not writable | Check directory permissions: `ls -ld ~/_sessions/`. Or pass `--output-dir <dir>` to write elsewhere. |
| **Categorization inaccurate** | Heuristics miss edge cases or context | Manual refinement in markdown post-generation. Update heuristics in script if pattern repeats. |
| **Script not found** | Skill folder missing its script | Verify `capture_session_prompts.py` sits next to this skill's `SKILL.md`. Reinstall the skill if not. |
| **Python version too old** | Python <3.9 | Verify Python version: `python3 --version`. Install Python 3.9+. |
| **Timestamp offset incorrect** | Machine time zone differs from the one wanted | Script uses local time. Override it per run: `TZ=Europe/Dublin python3 ...`. |
