#!/usr/bin/env python3
"""Capture one day's prompts from Claude Code's history.jsonl into a markdown table.

Reads ``history.jsonl`` from the Claude config directory (``CLAUDE_CONFIG_DIR``,
falling back to ``~/.claude``), keeps the entries for one local-time date, and
writes ``~/_sessions/YYYY_MM_DD_claude_prompts.md``.

Usage::

    python3 capture_session_prompts.py [--date YYYY-MM-DD] [--output-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

# Credential formats masked before any prompt text reaches the report
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36}"),
    re.compile(r"xox[abprs]-[A-Za-z0-9-]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]
# Keeps the key name so the reader still sees what was there, masking only the value
KEY_VALUE_SECRET = re.compile(r"(?i)\b(password|secret|token|api[_-]?key)(\s*[:=]\s*)\S{8,}")
REDACTED = "[REDACTED]"

STATUSES = [
    "✅ Done",
    "⏳ Pending",
    "❓ Question",
    "✔️ Clarifying Question",
    "↩️ Response",
    "📋 Note",
]


def config_dir() -> Path:
    """Return the Claude config directory.

    :return: ``CLAUDE_CONFIG_DIR`` if set, otherwise ``~/.claude`` (Claude Code's default).
    """
    configured = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(configured) if configured else Path.home() / ".claude"


def default_output_dir() -> Path:
    """Return the session-checkpoint directory the output is written to.

    :return: ``~/_sessions``.
    """
    return Path.home() / "_sessions"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    :param argv: Arguments to parse; ``None`` reads ``sys.argv``.
    :return: Parsed arguments with ``date`` and ``output_dir``.
    """
    parser = argparse.ArgumentParser(description="Capture session prompts from history")
    parser.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today, local time)")
    parser.add_argument("--output-dir", default=None, help="Directory to write to (default: ~/_sessions)")
    return parser.parse_args(argv)


def get_target_date(date_str: str | None = None) -> date:
    """Parse the date argument, defaulting to today in local time.

    :param date_str: Date in ``YYYY-MM-DD`` format, or ``None`` for today.
    :return: The target date.
    """
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return date.today()


def read_history(history_file: Path) -> list[dict]:
    """Read every valid JSON line from a history file, skipping malformed ones.

    :param history_file: Path to ``history.jsonl``.
    :return: Parsed entries; empty if the file doesn't exist.
    """
    if not history_file.exists():
        return []
    entries = []
    for line in history_file.read_text(encoding="utf-8").splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def filter_by_date(entries: list[dict], target_date: date) -> list[dict]:
    """Keep entries whose millisecond timestamp falls on the target local date.

    :param entries: History entries.
    :param target_date: Date to keep.
    :return: Matching entries, in original order.
    """
    return [
        entry for entry in entries
        if "timestamp" in entry and datetime.fromtimestamp(entry["timestamp"] / 1000).date() == target_date
    ]


def extract_time(timestamp_ms: int) -> tuple[int, int]:
    """Return the local hour and minute of a millisecond timestamp.

    :param timestamp_ms: Unix timestamp in milliseconds.
    :return: ``(hour, minute)``.
    """
    moment = datetime.fromtimestamp(timestamp_ms / 1000)
    return moment.hour, moment.minute


def categorize_theme(prompt: str) -> str:
    """Classify a prompt into a theme by keyword.

    :param prompt: Prompt text.
    :return: Theme name.
    """
    prompt_lower = prompt.lower()
    if len(prompt.split()) <= 2 and prompt.strip() in ["yes", "no", "1", "y", "n"]:
        return "Unclassified (-)"
    rule_keywords = ["rule", "hooks", "naming", "multifile", "style guide", "framework", "claude_config"]
    if any(kw in prompt_lower for kw in rule_keywords):
        return "Rules"
    if any(kw in prompt_lower for kw in ["skill", "domain", "skill.md"]):
        return "Skills"
    if any(kw in prompt_lower for kw in ["refactor", "trimming", "file", "structure", "child page"]):
        return "Process"
    if "todo" in prompt_lower:
        return "TODOs"
    planning_keywords = ["prompt", "audit", "capture", "session", "table", "theme", "status"]
    if sum(1 for kw in planning_keywords if kw in prompt_lower) >= 2:
        return "Planning"
    return "Other"


def determine_status(prompt: str) -> str:
    """Infer a prompt's status from its wording.

    :param prompt: Prompt text.
    :return: Status label.
    """
    prompt_lower = prompt.lower()
    if prompt.rstrip().endswith("?") and not prompt.startswith('"'):
        return "✔️ Clarifying Question"
    response_starters = [
        "but", "however", "no.", "yes,", "i never said", "re:", "go to plan", "go to planning", "entries containing",
    ]
    if any(starter in prompt_lower for starter in response_starters):
        return "↩️ Response"
    if prompt.strip() in ["yes", "y", "1"]:
        return "↩️ Response"
    directive_verbs = ["create", "add", "update", "review", "audit", "ensure"]
    if prompt.startswith(("this ", "the ", "it ")) and not any(verb in prompt_lower for verb in directive_verbs):
        return "📋 Note"
    if any(word in prompt_lower for word in ["create a dir", "go to plan", "go to planning", "create artifact"]):
        return "✅ Done"
    pending_markers = ["so i don't like", "you've jumped", "i want", "i told you", "you should", "before continuing"]
    if any(marker in prompt_lower for marker in pending_markers):
        return "⏳ Pending"
    if any(action in prompt_lower for action in [*directive_verbs, "document"]):
        return "✅ Done"
    return "↩️ Response"


def extract_subject(prompt: str) -> str:
    """Pick a subject label from keywords in the prompt.

    :param prompt: Prompt text.
    :return: Subject, or an empty string when nothing matches.
    """
    prompt_lower = prompt.lower()
    subjects = {
        "Style guides": ["style guide", "naming_standards"],
        "Hooks": ["hooks", "hook"],
        "Child pages": ["child page", "multifile"],
        "Naming": ["naming", "name"],
        "Skill domains": ["domain", "skill domain"],
        "Rules": ["rule"],
        "Prompt audit": ["prompt", "audit", "capture"],
        "TODOs": ["todo"],
    }
    for subject, keywords in subjects.items():
        if any(kw in prompt_lower for kw in keywords):
            return subject
    return ""


def extract_proposed_action(prompt: str) -> str:
    """Return a proposed action named in the prompt, if any.

    :param prompt: Prompt text.
    :return: Title-cased action, or an empty string.
    """
    for marker in ["create artifact", "go to plan mode"]:
        if marker in prompt.lower():
            return marker.title()
    return ""


def extract_closure(prompt: str) -> str:
    """Return a file-change phrase from the prompt, if any.

    :param prompt: Prompt text.
    :return: Matched phrase, or an empty string.
    """
    patterns = [
        r"created? [\w/_.-]+\.md",
        r"created? [\w/_.-]+\.yaml",
        r"[\w/_.-]+\.md created",
        r"[\w/_.-]+ updated",
        r"renamed? [\w_]+ → [\w_]+",
        r"removed? [\w_]+ from",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return ""


def extract_moscow(status: str, prompt: str) -> str:
    """Return a MoSCoW priority for pending prompts.

    :param status: The prompt's status.
    :param prompt: Prompt text.
    :return: ``Must``, ``Should``, ``Could`` or an empty string.
    """
    if status != "⏳ Pending":
        return ""
    prompt_lower = prompt.lower()
    for label, words in [("Must", ["must", "critical", "urgent", "blocker"]),
                         ("Should", ["should", "important", "priority"]),
                         ("Could", ["could", "nice", "defer"])]:
        if any(word in prompt_lower for word in words):
            return label
    return ""


def mask_secrets(text: str) -> str:
    """Replace known credential formats, and the values of password/secret/token/api_key pairs, with a marker."""
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(REDACTED, text)
    return KEY_VALUE_SECRET.sub(rf"\1\2{REDACTED}", text)


def build_row(entry_num: int, timestamp_ms: int, prompt: str) -> dict:
    """Build one table row from a history entry, masking secrets before any field is derived.

    :param entry_num: 1-based row number.
    :param timestamp_ms: Entry timestamp in milliseconds.
    :param prompt: Prompt text.
    :return: Row fields keyed by column.
    """
    prompt = mask_secrets(prompt)
    hour, minute = extract_time(timestamp_ms)
    status = determine_status(prompt)
    return {
        "num": entry_num,
        "hour": f"{hour:02d}",
        "min": f"{minute:02d}",
        "theme": categorize_theme(prompt),
        "subject": extract_subject(prompt),
        "status": status,
        "proposed_action": extract_proposed_action(prompt),
        "closure": extract_closure(prompt),
        "moscow": extract_moscow(status, prompt),
        "prompt": prompt,
    }


def escape_markdown_cell(text: str) -> str:
    """Make text safe for a single markdown table cell.

    :param text: Raw cell text.
    :return: Text with pipes escaped and whitespace collapsed to single spaces.
    """
    if not text:
        return ""
    return " ".join(text.replace("|", "\\|").split())


def generate_markdown_table(rows: list[dict]) -> str:
    """Render rows as a markdown table.

    :param rows: Rows from :func:`build_row`.
    :return: Markdown table text.
    """
    columns = ["num", "hour", "min", "theme", "subject", "status", "proposed_action", "closure", "moscow", "prompt"]
    lines = [
        "| # | Hour | Min | Theme | Subject | Status | Proposed Action | Closure | MoSCoW | Prompt |",
        "|---|------|-----|-------|---------|--------|-----------------|---------|--------|--------|",
    ]
    for row in rows:
        cells = " | ".join(escape_markdown_cell(str(row[col])) for col in columns)
        lines.append(f"| {cells} |")
    return "\n".join(lines)


def generate_summary(rows: list[dict], target_date: date) -> str:
    """Render totals by status, by theme, and by theme and status.

    :param rows: Rows from :func:`build_row`.
    :param target_date: The captured date.
    :return: Markdown summary text.
    """
    status_counts: dict[str, int] = defaultdict(int)
    theme_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        status_counts[row["status"]] += 1
        theme_counts[row["theme"]] += 1

    lines = [
        "---\n",
        "## Summary\n",
        f"- **Total prompts:** {len(rows)}",
        f"- **Date:** {target_date} (local time)\n",
        "**By status:**\n",
    ]
    lines += [f"- **{status}:** {status_counts[status]}" for status in sorted(status_counts)]
    lines.append("\n**By theme:**\n")
    lines += [f"- **{theme}:** {theme_counts[theme]}" for theme in sorted(theme_counts)]
    lines.append("\n**By theme & status:**\n")
    lines.append(f"| Theme | {' | '.join(STATUSES)} | Total |")
    lines.append("|-------|" + "---|" * len(STATUSES) + "-------|")
    for theme in sorted(theme_counts):
        theme_rows = [r for r in rows if r["theme"] == theme]
        counts = " | ".join(str(sum(1 for r in theme_rows if r["status"] == s)) for s in STATUSES)
        lines.append(f"| {theme} | {counts} | {len(theme_rows)} |")
    return "\n".join(lines)


def output_path_for(target_date: date, output_dir: Path) -> Path:
    """Return the output file path for a date.

    :param target_date: The captured date.
    :param output_dir: Directory to write into.
    :return: ``<output_dir>/YYYY_MM_DD_claude_prompts.md``.
    """
    return output_dir / f"{target_date:%Y_%m_%d}_claude_prompts.md"


def write_report(rows: list[dict], target_date: date, output_path: Path) -> None:
    """Write the table and summary to a markdown file, creating its directory.

    :param rows: Rows from :func:`build_row`.
    :param target_date: The captured date.
    :param output_path: File to write.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"# 📊 Prompts — {target_date}\n\n"
        f"**Purpose:** Structured view of all prompts for {target_date}, with time, theme, subject, "
        f"status, proposed action, closure, MoSCoW, and full prompt text.\n\n"
        f"{generate_markdown_table(rows)}\n\n{generate_summary(rows, target_date)}\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Capture one day's prompts and write the report.

    :param argv: Arguments to parse; ``None`` reads ``sys.argv``.
    :return: Exit code (always 0; an empty day is reported, not an error).
    """
    args = parse_args(argv)
    target_date = get_target_date(args.date)
    entries = filter_by_date(read_history(config_dir() / "history.jsonl"), target_date)
    if not entries:
        print(f"No history entries found for {target_date}")
        return 0

    rows = [build_row(idx, entry["timestamp"], entry.get("display", "")) for idx, entry in enumerate(entries, 1)]
    output_dir = Path(args.output_dir) if args.output_dir else default_output_dir()
    output_path = output_path_for(target_date, output_dir)
    write_report(rows, target_date, output_path)
    print(f"✅ Generated {output_path}")
    print(f"   {len(rows)} prompts captured")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
