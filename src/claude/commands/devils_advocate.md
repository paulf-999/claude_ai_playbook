---
description: Devil's advocate code review of current branch diff against main
argument-hint: [max-rounds (default 5)]
---

# Devil's Advocate Code Review

Simulate a code review conversation between two engineers:

- **Author**: The engineer who wrote the code. Defends decisions, explains
  tradeoffs, and proposes concrete fixes when conceding a point.
- **Reviewer**: A senior engineer doing a thorough review. Raises real,
  substantive concerns and provides specific code suggestions when pointing
  out problems.

## Scope

Review ONLY the diff between the current branch and `main`:

```
!`git diff main...HEAD`
```

If the diff is empty, say so and stop.

## Topic priority

Work through concerns in this order. Spend as many rounds as needed on each
topic before moving to the next. Skip topics where there's nothing to say.

1. Correctness - bugs, logic errors, unhandled edge cases, race conditions
2. Error handling - missing error paths, swallowed exceptions, unclear failure modes
3. Performance - N+1 queries, unnecessary allocations, algorithmic issues
4. Security - injection risks, auth gaps, data exposure
5. Maintainability - unclear abstractions, coupling, naming, readability
6. Testing gaps - missing test cases, untested branches, brittle assertions

## Rules

- Run up to $ARGUMENTS rounds (default 5).
- Label each round: "### Round N — [Topic]"
- Reviewer MUST raise a substantive concern per round.
- Author MUST push back before conceding.
- Both parties must include code snippets/diffs when suggesting changes.
- Early termination if all topics resolved before N rounds.

## Summary

After all rounds, print:
- Round breakdown table (topic, rounds, action items)
- Agreed changes (with code snippets)
- Open disagreements
- Action items (priority-ranked, total count)
- Deferred concerns
- Re-run recommendation
