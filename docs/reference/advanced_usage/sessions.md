# 🔄 Session Management

Resume interrupted sessions, pick up from a PR, or fork a session to explore an alternative approach — all without losing context.

---

## Resume the most recent session

```bash
claude --continue
```

Resumes the last session in the current directory. Use this when you close a terminal mid-task and want to pick up exactly where you left off.

---

## Pick from recent sessions

```bash
claude --resume
```

Opens an interactive list of recent sessions so you can select one to resume. Useful when you have multiple in-flight tasks and want to switch between them.

---

## Resume from a pull request

```bash
claude --from-pr 123
```

Resumes the session that was active when PR #123 was created. Useful for revisiting the context behind a PR — for example, when addressing review feedback or investigating a regression.

Sessions are linked to PRs automatically when created via `gh pr create`.

---

## Fork a session

```bash
claude --resume --fork-session
```

Creates a new independent session with the same conversation history up to that point. Use this when you want to explore an alternative approach without affecting the original session.

> **Note:** Forked and resumed sessions do not inherit session-scoped permissions — these will need to be re-approved.

---

## Avoid parallel resume conflicts

Resuming the same session in two terminals simultaneously causes interleaved messages and a jumbled history. If you need to work from a common starting point in parallel, use `--fork-session` so each terminal has its own distinct session.

---

## Related

- [Parallel sessions with worktrees](worktrees.md) — run independent Claude sessions on separate branches simultaneously
