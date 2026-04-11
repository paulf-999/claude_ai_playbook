#!/usr/bin/env python3
"""Stop hook — session cost summary.

Prints a one-line cost summary to the terminal after each Claude turn.

Input:  JSON on stdin — {"session_id": "...", "transcript_path": "...", "stop_hook_active": bool}
Output: None (prints to stdout for terminal display; exits 0 always)

Pricing (as of 2026):
  claude-sonnet-4-6:       input $3.00/MTok   output $15.00/MTok  cache write $3.75/MTok  cache read $0.30/MTok
  claude-opus-4-6:         input $15.00/MTok  output $75.00/MTok  cache write $18.75/MTok cache read $1.50/MTok
  claude-haiku-4-5-20251001: input $0.80/MTok  output $4.00/MTok   cache write $1.00/MTok  cache read $0.08/MTok

Remaining credit balance is not fetched automatically — run `/cost` in Claude Code to see it.
"""

import json
import sys

# ---------------------------------------------------------------------------
# Pricing table — USD per token (not per million)
# ---------------------------------------------------------------------------

_PRICING: dict[str, dict[str, float]] = {
    "claude-sonnet-4-6": {
        "input": 3.00 / 1_000_000,
        "output": 15.00 / 1_000_000,
        "cache_write": 3.75 / 1_000_000,
        "cache_read": 0.30 / 1_000_000,
    },
    "claude-opus-4-6": {
        "input": 15.00 / 1_000_000,
        "output": 75.00 / 1_000_000,
        "cache_write": 18.75 / 1_000_000,
        "cache_read": 1.50 / 1_000_000,
    },
    "claude-haiku-4-5-20251001": {
        "input": 0.80 / 1_000_000,
        "output": 4.00 / 1_000_000,
        "cache_write": 1.00 / 1_000_000,
        "cache_read": 0.08 / 1_000_000,
    },
}
_DEFAULT_RATES = _PRICING["claude-sonnet-4-6"]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _read_hook_input() -> dict:
    """Parse JSON from stdin.

    :return: Parsed hook input dict, or empty dict on failure.
    :rtype: dict
    """
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return {}


def _sum_usage(transcript_path: str) -> tuple[dict[str, int], str]:
    """Sum token usage across all unique assistant messages in the transcript.

    Each Anthropic API message appears twice in the JSONL (once as a streaming
    entry, once as the final entry). Deduplicate by message.id to avoid
    double-counting.

    :param transcript_path: Absolute path to the session JSONL file.
    :type transcript_path: str
    :return: Tuple of (usage totals dict, last model name seen).
    :rtype: tuple[dict[str, int], str]
    """
    seen: set[str] = set()
    totals: dict[str, int] = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}
    last_model = "claude-sonnet-4-6"

    try:
        with open(transcript_path) as fh:
            for raw_line in fh:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    entry = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                if entry.get("type") != "assistant":
                    continue

                msg = entry.get("message", {})
                msg_id: str = msg.get("id", "")

                if msg_id:
                    if msg_id in seen:
                        continue
                    seen.add(msg_id)

                usage = msg.get("usage", {})
                totals["input"] += usage.get("input_tokens", 0)
                totals["output"] += usage.get("output_tokens", 0)
                totals["cache_write"] += usage.get("cache_creation_input_tokens", 0)
                totals["cache_read"] += usage.get("cache_read_input_tokens", 0)

                model: str = msg.get("model", "")
                if model:
                    last_model = model

    except OSError:
        pass

    return totals, last_model


# ---------------------------------------------------------------------------
# Cost calculation
# ---------------------------------------------------------------------------

def _calculate_cost(totals: dict[str, int], model: str) -> float:
    """Calculate total session cost in USD.

    :param totals: Token counts for input/output/cache_write/cache_read.
    :type totals: dict[str, int]
    :param model: Model name string used to look up pricing.
    :type model: str
    :return: Total cost in USD.
    :rtype: float
    """
    rates = _PRICING.get(model, _DEFAULT_RATES)
    return (
        totals["input"] * rates["input"]
        + totals["output"] * rates["output"]
        + totals["cache_write"] * rates["cache_write"]
        + totals["cache_read"] * rates["cache_read"]
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Read session transcript, calculate cost, and print a one-line summary."""
    hook_data = _read_hook_input()

    # Avoid running inside a hook loop
    if hook_data.get("stop_hook_active"):
        sys.exit(0)

    transcript_path: str = hook_data.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    totals, model = _sum_usage(transcript_path)

    total_tokens = sum(totals.values())
    if total_tokens == 0:
        sys.exit(0)

    cost = _calculate_cost(totals, model)

    print(
        f"💰 session: ${cost:.4f}"
        f"  |  in {totals['input']:,}"
        f"  out {totals['output']:,}"
        f"  cache-r {totals['cache_read']:,}"
        f"  cache-w {totals['cache_write']:,}"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
