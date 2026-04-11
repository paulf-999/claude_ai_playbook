#!/usr/bin/env python3
"""UserPromptSubmit hook — prompt quality reviewer.

Checks each user prompt against Claude Code best practices and either injects
a tip into Claude's context (low severity) or blocks the prompt entirely
(high severity).

Input:  JSON on stdin — {"prompt": "...", "session_id": "...", ...}
Output: JSON on stdout — {"additionalContext": "..."} or {"decision": "block", "reason": "..."}
"""

import json
import re
import sys
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Verbs that suggest the prompt is asking for a code/config change.
_IMPLEMENTATION_VERBS: frozenset[str] = frozenset({
    "add", "implement", "create", "write", "build", "fix", "update",
    "refactor", "modify", "change", "make", "develop", "generate",
    "convert", "migrate", "move", "rename", "edit", "configure", "set up",
    "install", "integrate",
})

# Keywords indicating the user has already included verification criteria.
_VERIFICATION_KEYWORDS: frozenset[str] = frozenset({
    "test", "tests", "verify", "run", "check", "confirm", "validate",
    "assert", "ensure", "pytest", "make test", "pass",
})

# Regex patterns that suggest the prompt references a specific file or path.
_FILE_PATTERNS: list[str] = [
    r"@\S+",
    r"\b\w+\.(py|sql|ts|js|sh|bash|yaml|yml|md|tf|json|toml|cfg|ini)\b",
    r"\bsrc/|tests/|docs/",
    r"[a-z_][a-z0-9_]*/[a-z_][a-z0-9_/]*\.[a-z]+",  # path/to/file.ext
]

# Risky action patterns and their human-readable labels.
_RISKY_PATTERNS: list[tuple[str, str]] = [
    (r"\bdrop\s+table\b", "DROP TABLE"),
    (r"\bdrop\s+(the\s+)?(database|schema)\b", "DROP DATABASE / SCHEMA"),
    (r"\btruncate\s+(table\s+)?\w+", "TRUNCATE"),
    (r"\brm\s+-rf?\s", "rm -rf"),
    (r"\bgit\b.*\s--force\b|push\s+.*--force\b", "git --force"),
    (r"\bgit\b.*\s--no-verify\b", "git --no-verify"),
    (
        r"\bdelete\s+(all|every|the\s+(entire|whole|all))\b"
        r"|\bdelete\s+all\s+(the\s+)?(records|rows|data|entries|tables)\b",
        "bulk delete",
    ),
]

# Minimum word count before context/verification checks apply.
# Very short prompts (questions, confirmations) are excluded.
_MIN_WORDS_FOR_CHECKS: int = 8


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    """Result of a single quality check."""

    severity: str   # "low" | "high"
    check: str      # check identifier
    tip: str        # human-readable issue description
    matched: str = ""  # for risky-action checks: the label that matched


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

def read_prompt() -> str:
    """Parse stdin JSON and return the user's prompt string.

    :return: The prompt text, or an empty string if parsing fails.
    :rtype: str
    """
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        return data.get("prompt", "")
    except (json.JSONDecodeError, AttributeError):
        return ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_implementation_prompt(prompt: str) -> bool:
    """Return True if the prompt appears to request a code or config change.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: True if implementation intent is detected.
    :rtype: bool
    """
    words = set(prompt.lower().split())
    return bool(words & _IMPLEMENTATION_VERBS)


def _has_file_reference(prompt: str) -> bool:
    """Return True if the prompt references a specific file or path.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: True if a file or path reference is found.
    :rtype: bool
    """
    return any(re.search(p, prompt, re.IGNORECASE) for p in _FILE_PATTERNS)


def _has_verification_criteria(prompt: str) -> bool:
    """Return True if the prompt includes instructions on how to verify the result.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: True if verification keywords are present.
    :rtype: bool
    """
    lower = prompt.lower()
    return any(kw in lower for kw in _VERIFICATION_KEYWORDS)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_specific_context(prompt: str) -> CheckResult | None:
    """LOW: implementation prompt with no file or scope references.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: A CheckResult if the check fails, otherwise None.
    :rtype: CheckResult | None
    """
    if len(prompt.split()) < _MIN_WORDS_FOR_CHECKS:
        return None
    if not _is_implementation_prompt(prompt):
        return None
    if _has_file_reference(prompt):
        return None
    return CheckResult(
        severity="low",
        check="specific_context",
        tip="No specific file or scope reference detected.",
    )


def check_verification(prompt: str) -> CheckResult | None:
    """LOW: implementation prompt with no verification criteria.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: A CheckResult if the check fails, otherwise None.
    :rtype: CheckResult | None
    """
    if len(prompt.split()) < _MIN_WORDS_FOR_CHECKS:
        return None
    if not _is_implementation_prompt(prompt):
        return None
    if _has_verification_criteria(prompt):
        return None
    return CheckResult(
        severity="low",
        check="verification",
        tip="No verification criteria detected.",
    )


def check_risky_actions(prompt: str) -> CheckResult | None:
    """HIGH: destructive or bypass patterns detected.

    :param prompt: The user's prompt text.
    :type prompt: str
    :return: A CheckResult if a risky pattern is matched, otherwise None.
    :rtype: CheckResult | None
    """
    for pattern, label in _RISKY_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return CheckResult(
                severity="high",
                check="risky_action",
                tip=f"Risky action detected: {label}.",
                matched=label,
            )
    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _build_suggested_prompt(original: str, results: list[CheckResult]) -> str:
    """Build a candidate improved prompt from the original and failed checks.

    :param original: The user's original prompt text.
    :type original: str
    :param results: Low-severity check results that failed.
    :type results: list[CheckResult]
    :return: A suggested improved prompt string.
    :rtype: str
    """
    checks = {r.check for r in results}
    base = original.rstrip(". ")

    if "specific_context" in checks:
        base = f"In [specify file, e.g. src/module/file.py], {base[0].lower()}{base[1:]}"

    if "verification" in checks:
        base = f"{base}. After implementing, run `make test` to verify."
    else:
        base = f"{base}."

    return base


def _build_tip_text(original: str, results: list[CheckResult]) -> str:
    """Assemble the full tip message including issues and suggested prompt.

    :param original: The user's original prompt text.
    :type original: str
    :param results: Low-severity check results that failed.
    :type results: list[CheckResult]
    :return: Formatted tip string for injection as additional context.
    :rtype: str
    """
    issues = " | ".join(r.tip for r in results)
    suggested = _build_suggested_prompt(original, results)

    lines = [
        "--- Prompt Quality Tip ---",
        f"Issue(s): {issues}",
        "",
        "Claude performs better with specific file references and clear success criteria.",
        "See: https://code.claude.com/docs/en/best-practices",
        "",
        "Suggested prompt:",
        f'  "{suggested}"',
        "--------------------------",
    ]
    return "\n".join(lines)


def emit_output(prompt: str, results: list[CheckResult]) -> None:
    """Write JSON output to stdout and exit.

    Low severity: inject tip as additionalContext (non-blocking).
    High severity: block the prompt with a reason.

    :param prompt: The user's original prompt text.
    :type prompt: str
    :param results: All check results from this prompt.
    :type results: list[CheckResult]
    """
    if not results:
        sys.exit(0)

    high = next((r for r in results if r.severity == "high"), None)

    if high:
        output = {
            "decision": "block",
            "reason": (
                f"Prompt blocked: {high.matched} detected.\n\n"
                "Please revise your prompt to specify:\n"
                "  - Which objects are affected\n"
                "  - Whether a backup or rollback plan exists\n"
                "  - The expected outcome"
            ),
        }
    else:
        low_results = [r for r in results if r.severity == "low"]
        tip = _build_tip_text(prompt, low_results)
        output = {"additionalContext": tip}

    print(json.dumps(output))
    sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Read the prompt from stdin, run all checks, and emit output."""
    prompt = read_prompt()

    if not prompt:
        sys.exit(0)

    results: list[CheckResult] = []

    # High-severity check runs first; if it fires, skip low-severity checks.
    risky = check_risky_actions(prompt)
    if risky:
        results.append(risky)
    else:
        for check_fn in (check_specific_context, check_verification):
            result = check_fn(prompt)
            if result:
                results.append(result)

    emit_output(prompt, results)


if __name__ == "__main__":
    main()
