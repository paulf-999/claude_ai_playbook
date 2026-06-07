# Large diff fixture — eval 4 (diff truncation path)

## Test setup

This eval exercises the diff-truncation behaviour. To run it, the active PR or the PR
passed as context must have a diff exceeding 500 lines (e.g. a PR with many file changes
or a large single-file addition).

The truncation is applied by the skill itself when `gh pr diff` returns >500 lines —
no manual intervention is needed beyond choosing an appropriately large PR.

## Expected behaviour

1. Claude fetches the diff via `gh pr diff <number>`.
2. Seeing the diff exceeds 500 lines, Claude truncates to the first 500 lines.
3. The review comment includes the note:
   > "Note: diff truncated to 500 lines — review covers visible changes only."
4. The full scorecard and verdict are still generated and posted.
