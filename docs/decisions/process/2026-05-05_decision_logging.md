# Introduce proactive decision logging to the memory system
**Date:** 2026-05-05
**Status:** active

Session wrap-up captured decisions in `context.md`, but they were overwritten each session — no persistent log, no searchable history. A new `decision` memory type was introduced, with Claude logging non-obvious choices proactively using a two-part grain test.

**Rationale:** The existing memory types (user, feedback, project, reference) had no home for architectural or convention decisions. File-based memory was chosen over MCP memory server to keep decision records consistent with the existing memory system and human-readable in the repo. The grain test (non-obvious + persistent value) was designed to suppress noise from routine choices while capturing the calls that would be hard to reconstruct from code or commit history alone.
