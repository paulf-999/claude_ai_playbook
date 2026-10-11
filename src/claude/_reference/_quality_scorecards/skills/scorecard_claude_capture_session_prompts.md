# Quality Scorecard — claude_capture_session_prompts

**Date Created:** 2026-09-07
**Date Updated:** 2026-10-06

**Overall score:** 9.0/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Design** | 9/10 | 2026-10-06 | • ✅ **Workflow:** capture, review and plan, with a sensible default of today's date |
| **Complexity** | 8/10 | 2026-10-06 | • 🧮 **Raw complexity 2:** capture and categorise (Concepts 1), one history file in and one table out (Scope 1), no external services |
| **Test Coverage** | 9/10 | 2026-10-06 | • 📊 **Count:** 6 evals plus 18 pytest functions that actually run against the script, including secret masking |
| **Code Quality** | 9/10 | 2026-10-06 | • ✅ **Errors:** catches malformed JSON lines specifically, and the 374-line script passes ruff |
| **Security** | 9/10 | 2026-10-06 | • ✅ **Local only:** reads `history.jsonl` and makes no network calls<br>• ✅ **Masking:** known key and token formats are replaced with `[REDACTED]` before any column is built, with 4 pytest checks<br>• ⚠️ **Pattern-based:** a secret in an unknown format can still get through |
| **Documentation** | 9/10 | 2026-10-06 | • ✅ **Reference:** implementation, examples and error recovery, with masking and its limits described in SKILL.md |
| **Standards Compliance** | 10/10 | 2026-10-06 | • ✅ **Hard gates:** Instructions for Claude before Purpose, off the baseline, 60 lines, and the maturity justification in Best For<br>• ✅ **Tested:** pytest runs against the script, so `tested` is true |
| **Overall** | **9.0/10** | 2026-10-06 | A simple, well-tested local script that masks secrets and meets the full SKILL.md standard. |

## 🔗 Related files

- `src/claude/skills/_claude_skills/claude_capture_session_prompts/SKILL.md` — the skill being scored
- `src/claude/skills/_claude_skills/claude_capture_session_prompts/tests/evals.yaml` — Test Coverage dimension
