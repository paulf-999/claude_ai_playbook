#!/usr/bin/env python3
"""Measure how often each rule applies to a session, and how often it was loaded.

Reads Claude Code session transcripts and the rules folder, then writes a markdown
report and appends one row per rule to a CSV history, so dates survive after old
transcripts are deleted.

- **Applied:** the session touched a file matching the rule's globs (``*`` = every session).
- **Loaded:** the rule reached Claude's context — an always-on import, a ``paths:``
  rule loaded automatically, or a ``Read`` of the rule file.
- **Miss:** the rule applied but was never loaded.

Standard library only, no LLM calls. Every location is a required argument, because the
script is installed into the live config too and must never guess the repo.

Usage:
    python3 src/claude/_scripts/audit_rule_usage.py \\
        --rules src/claude/_rules --transcripts ~/.claude/projects --out src/claude/_admin/_audits
    make audit_rule_usage
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from fnmatch import fnmatch
from pathlib import Path

# ── first-guess cut-offs — review after 3 reports ─────────────────────────────

MIN_SAMPLE_SESSIONS = 10  # first guess: fewer applied sessions than this shows "not enough data"
DEMOTE_APPLIED_BELOW = 0.5  # first guess: an always-on rule applying in fewer sessions may be lazy
STALE_AFTER_DAYS = 90  # first guess: no use for this long marks a rule stale

# ── constants ─────────────────────────────────────────────────────────────────

EVERY_SESSION = "*"
LAZY_TIER = "05_lazy_load"
REPORT_NAME = "audit_rule_usage.md"
HISTORY_NAME = "rule_usage_history.csv"
HISTORY_FIELDS = [
    "run_date", "rule", "tier", "tokens", "sessions", "applied", "loaded", "misses", "last_applied", "last_loaded",
]
TOP_SECTIONS = 15
CHARS_PER_TOKEN = 4
TIER_DIR = re.compile(r"^\d\d_")
IMPORT_LINE = re.compile(r"^@~/[^/]+/_rules/(\S+\.md)\s*$", re.M)
MISS_COST = re.compile(r"<!--\s*miss_cost:\s*(high|medium|low)\b", re.I)
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}

# First-guess globs for lazy rules without ``paths:`` frontmatter, keyed by path under 05_lazy_load/.
# Phase 4 replaces these with an ``applies_to`` header in each rule.
DEFAULT_APPLIES_TO = {
    "style_guide_standards/python.md": ["**/*.py"],
    "style_guide_standards/bash.md": ["**/*.sh"],
    "style_guide_standards/dbt.md": ["**/models/**/*.sql", "**/dbt_project.yml"],
    "style_guide_standards/airflow.md": ["**/dags/**/*.py"],
    "style_guide_standards/infra/terraform.md": ["**/*.tf"],
    "style_guide_standards/infra/ansible.md": ["**/playbooks/**/*.yml", "**/roles/**/*.yml"],
    "style_guide_standards/infra/docker.md": ["**/Dockerfile*", "**/docker-compose*.yml"],
    "style_guide_standards/utilities/makefile.md": ["**/Makefile", "**/*.mk"],
    "style_guide_standards/utilities/mermaid.md": ["**/*.mmd"],
    "testing_guidance.md": ["**/test_*.py"],
    "response_standards_enforcement.md": ["**/hook_style_guide_response_standards*.sh"],
    "hooks_decision_framework.md": ["**/hooks/hook_*.sh"],
}


# ── data ──────────────────────────────────────────────────────────────────────


@dataclass
class Rule:
    """One entry-point rule and what counts as it applying."""

    rel: str
    tier: str
    tokens: int
    globs: list[str]
    miss_cost: str = "—"
    files: list[str] = field(default_factory=list)

    @property
    def always_on(self) -> bool:
        """Whether the rule loads every session.

        :return: True for tiers 01–04.
        :rtype: bool
        """
        return self.tier != LAZY_TIER


@dataclass
class Session:
    """What one session touched and which rules reached its context."""

    project: str
    last_date: date | None = None
    touched: set[str] = field(default_factory=set)
    loaded: set[str] = field(default_factory=set)


@dataclass
class Usage:
    """Measured usage of one rule across all sessions."""

    rule: Rule
    sessions: int
    applied: int | None
    loaded: int
    misses: int | None
    last_applied: date | None
    last_loaded: date | None
    flag: str = ""


# ── rules ─────────────────────────────────────────────────────────────────────


def is_child(path: Path, tier_dir: Path) -> bool:
    """Tell whether a rule file belongs to a parent topic rather than standing alone.

    :param path: Rule file path.
    :type path: Path
    :param tier_dir: The tier folder the file sits in.
    :type tier_dir: Path
    :return: True when the name starts with ``_`` or a folder above it has a sibling parent ``.md``.
    :rtype: bool
    """
    if path.name.startswith("_"):
        return True
    for folder in path.parents:
        if folder == tier_dir:
            return False
        if folder.with_suffix(".md").is_file():
            return True
    return False


def imported_files(rules_dir: Path, rel: str, seen: set[str] | None = None) -> list[str]:
    """Follow ``@`` imports from a rule, returning it and every file it pulls in.

    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :param rel: Rule path relative to ``rules_dir``.
    :type rel: str
    :param seen: Files already visited, to stop import cycles.
    :type seen: set[str] | None
    :return: Relative paths, the rule first.
    :rtype: list[str]
    """
    seen = set() if seen is None else seen
    path = rules_dir / rel
    if rel in seen or not path.is_file():
        return []
    seen.add(rel)
    found = [rel]
    for child in IMPORT_LINE.findall(path.read_text(encoding="utf-8")):
        found += imported_files(rules_dir, child, seen)
    return found


def frontmatter_paths(text: str) -> list[str]:
    """Read the ``paths:`` globs from a rule's YAML frontmatter, without a YAML library.

    :param text: Rule file content.
    :type text: str
    :return: The globs, or an empty list.
    :rtype: list[str]
    """
    if not text.startswith("---\n"):
        return []
    block = text.split("\n---", 1)[0]
    if "paths:" not in block:
        return []
    return re.findall(r"^\s*-\s*[\"']?([^\"'\n]+?)[\"']?\s*$", block.split("paths:", 1)[1], re.M)


def token_count(rules_dir: Path, rels: list[str]) -> int:
    """Estimate tokens as characters divided by four.

    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :param rels: Rule files to count.
    :type rels: list[str]
    :return: Estimated tokens.
    :rtype: int
    """
    return sum(len((rules_dir / rel).read_text(encoding="utf-8")) for rel in rels) // CHARS_PER_TOKEN


def discover_rules(rules_dir: Path) -> list[Rule]:
    """Find every entry-point rule in the numbered tiers.

    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :return: Rules sorted by tier then path.
    :rtype: list[Rule]
    """
    rules = []
    for tier_dir in sorted(d for d in rules_dir.iterdir() if d.is_dir() and TIER_DIR.match(d.name)):
        for path in sorted(tier_dir.rglob("*.md")):
            if path.name == "README.md" or "_lazy_load" in path.parts or is_child(path, tier_dir):
                continue
            rel = path.relative_to(rules_dir).as_posix()
            text = path.read_text(encoding="utf-8")
            if tier_dir.name == LAZY_TIER:
                files = [rel]
                in_tier = path.relative_to(tier_dir).as_posix()
                globs = frontmatter_paths(text) or DEFAULT_APPLIES_TO.get(in_tier, [])
            else:
                files = imported_files(rules_dir, rel)
                globs = [EVERY_SESSION]
            cost = MISS_COST.search(text)
            rules.append(Rule(
                rel=rel,
                tier=tier_dir.name,
                tokens=token_count(rules_dir, files),
                globs=globs,
                miss_cost=cost.group(1).lower() if cost else "—",
                files=files,
            ))
    return rules


def section_sizes(rules_dir: Path, rules: list[Rule]) -> list[tuple[str, str, int]]:
    """Size every ``##`` section in the always-on files, largest first.

    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :param rules: Discovered rules.
    :type rules: list[Rule]
    :return: ``(file, heading, tokens)`` tuples.
    :rtype: list[tuple[str, str, int]]
    """
    sizes = []
    files = {rel for rule in rules if rule.always_on for rel in rule.files}
    for rel in sorted(files):
        for chunk in re.split(r"^(?=## )", (rules_dir / rel).read_text(encoding="utf-8"), flags=re.M)[1:]:
            sizes.append((rel, chunk.splitlines()[0][3:].strip(), len(chunk) // CHARS_PER_TOKEN))
    return sorted(sizes, key=lambda s: -s[2])


# ── transcripts ───────────────────────────────────────────────────────────────


def rule_rel(raw: str, rules_dir: Path) -> str | None:
    """Map a path seen in a transcript to a rule path relative to ``rules_dir``.

    Handles the repo copy, the live copy, and the ``rules/`` symlinks Claude Code reads.

    :param raw: A file path from the transcript.
    :type raw: str
    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :return: The relative rule path, or None when it isn't a rule.
    :rtype: str | None
    """
    if "_rules/" in raw:
        return raw.rsplit("_rules/", 1)[1]
    match = re.search(r"(?:^|/)rules/([^/]+\.md)$", raw)
    if match:
        link = rules_dir.parent / "rules" / match.group(1)
        if link.is_symlink():
            try:
                return link.resolve().relative_to(rules_dir.resolve()).as_posix()
            except ValueError:
                return None
    return None


def record_date(record: dict) -> date | None:
    """Read the day from a record's ISO timestamp.

    :param record: One transcript record.
    :type record: dict
    :return: The day, or None when the record has no valid timestamp.
    :rtype: date | None
    """
    stamp = record.get("timestamp")
    if not isinstance(stamp, str):
        return None
    try:
        return date.fromisoformat(stamp[:10])
    except ValueError:
        return None


def tool_calls(record: dict) -> list[tuple[str, str]]:
    """List the file tools an assistant record calls.

    :param record: One transcript record.
    :type record: dict
    :return: ``(tool name, file path)`` pairs.
    :rtype: list[tuple[str, str]]
    """
    content = (record.get("message") or {}).get("content")
    calls = []
    for item in content if isinstance(content, list) else []:
        if not isinstance(item, dict) or item.get("type") != "tool_use" or item.get("name") not in FILE_TOOLS:
            continue
        tool_input = item.get("input") or {}
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if isinstance(target, str):
            calls.append((item["name"], target))
    return calls


def attachment_paths(attachment: dict) -> tuple[list[str], list[str]]:
    """Split an attachment into files it loaded into context and files it says were edited.

    :param attachment: The record's ``attachment`` object.
    :type attachment: dict
    :return: ``(loaded paths, touched paths)``.
    :rtype: tuple[list[str], list[str]]
    """
    kind = attachment.get("type")
    if kind == "instructions":
        return [f.get("path", "") for f in attachment.get("files", []) if isinstance(f, dict)], []
    if kind == "nested_memory":
        return [attachment.get("path", "")], []
    if kind == "edited_text_file" and isinstance(attachment.get("filename"), str):
        return [], [attachment["filename"]]
    return [], []


def parse_session(path: Path, rules_dir: Path) -> Session:
    """Read one transcript into a Session.

    :param path: A ``.jsonl`` transcript.
    :type path: Path
    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :return: The session's touched files, loaded rules and last date.
    :rtype: Session
    """
    session = Session(project=path.parent.name)
    loaded_paths = []
    days = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        days.append(record_date(record))
        if record.get("type") == "assistant":
            for name, target in tool_calls(record):
                session.touched.add(target)
                if name == "Read":
                    loaded_paths.append(target)
        elif record.get("type") == "attachment":
            loaded, touched = attachment_paths(record.get("attachment") or {})
            loaded_paths += loaded
            session.touched.update(touched)
    session.last_date = max((d for d in days if d), default=None)
    session.loaded = {rel for raw in loaded_paths if raw and (rel := rule_rel(raw, rules_dir))}
    return session


def discover_sessions(transcripts_dir: Path, rules_dir: Path) -> list[Session]:
    """Read every main-session transcript, skipping sub-agent logs.

    :param transcripts_dir: Claude Code's ``projects`` folder.
    :type transcripts_dir: Path
    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :return: Parsed sessions.
    :rtype: list[Session]
    """
    paths = sorted(p for p in transcripts_dir.rglob("*.jsonl") if "subagents" not in p.parts)
    return [parse_session(p, rules_dir) for p in paths]


# ── measuring ─────────────────────────────────────────────────────────────────


def applies(rule: Rule, session: Session) -> bool:
    """Tell whether a rule applied to a session.

    :param rule: The rule.
    :type rule: Rule
    :param session: The session.
    :type session: Session
    :return: True when the rule covers every session or a touched file matches a glob.
    :rtype: bool
    """
    if EVERY_SESSION in rule.globs:
        return True
    touched = [t if t.startswith("/") else f"/{t}" for t in session.touched]
    return any(fnmatch(t, glob) for t in touched for glob in rule.globs)


def latest(sessions: list[Session]) -> date | None:
    """Return the latest session date, if any.

    :param sessions: Sessions to check.
    :type sessions: list[Session]
    :return: The latest date, or None.
    :rtype: date | None
    """
    dates = [s.last_date for s in sessions if s.last_date]
    return max(dates) if dates else None


def measure(rules: list[Rule], sessions: list[Session]) -> list[Usage]:
    """Count applied, loaded and missed sessions for every rule.

    :param rules: Discovered rules.
    :type rules: list[Rule]
    :param sessions: Parsed sessions.
    :type sessions: list[Session]
    :return: One Usage per rule, flags still empty.
    :rtype: list[Usage]
    """
    usages = []
    for rule in rules:
        loaded = [s for s in sessions if rule.rel in s.loaded]
        applied = [s for s in sessions if applies(rule, s)] if rule.globs else None
        misses = None if applied is None else sum(1 for s in applied if rule.rel not in s.loaded)
        usages.append(Usage(
            rule=rule,
            sessions=len(sessions),
            applied=None if applied is None else len(applied),
            loaded=len(loaded),
            misses=misses,
            last_applied=latest(applied or []),
            last_loaded=latest(loaded),
        ))
    return usages


def flag_for(usage: Usage, last_used: date | None, data_start: date | None, today: date) -> str:
    """Choose the flag for one rule.

    :param usage: The rule's measured usage.
    :type usage: Usage
    :param last_used: Latest use across this run and the history.
    :type last_used: date | None
    :param data_start: Earliest date covered by transcripts or history.
    :type data_start: date | None
    :param today: The run date.
    :type today: date
    :return: Flags joined by ``, ``, or an empty string.
    :rtype: str
    """
    if usage.applied is None:
        return "no trigger"
    if usage.applied < MIN_SAMPLE_SESSIONS:
        return "not enough data"
    flags = []
    rule = usage.rule
    if not rule.always_on and rule.miss_cost == "high" and usage.misses:
        flags.append("promote")
    applied_share = usage.applied / usage.sessions if usage.sessions else 0
    if rule.always_on and rule.miss_cost == "low" and applied_share < DEMOTE_APPLIED_BELOW:
        flags.append("demote")
    cutoff = today - timedelta(days=STALE_AFTER_DAYS)
    if (last_used and last_used < cutoff) or (last_used is None and data_start and data_start <= cutoff):
        flags.append("stale")
    return ", ".join(flags)


# ── history ───────────────────────────────────────────────────────────────────


def read_history(path: Path) -> tuple[dict[str, date], date | None]:
    """Read the latest use per rule, and the earliest run date, from the history CSV.

    :param path: The history file.
    :type path: Path
    :return: ``(last use by rule, first run date)``.
    :rtype: tuple[dict[str, date], date | None]
    """
    last_used: dict[str, date] = {}
    first_run = None
    if not path.is_file():
        return last_used, first_run
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            run = date.fromisoformat(row["run_date"])
            first_run = min(run, first_run) if first_run else run
            for key in ("last_applied", "last_loaded"):
                if row.get(key):
                    day = date.fromisoformat(row[key])
                    last_used[row["rule"]] = max(day, last_used.get(row["rule"], day))
    return last_used, first_run


def append_history(path: Path, usages: list[Usage], today: date) -> None:
    """Append one row per rule to the history CSV, writing the header on first use.

    :param path: The history file.
    :type path: Path
    :param usages: Measured usage.
    :type usages: list[Usage]
    :param today: The run date.
    :type today: date
    """
    new_file = not path.is_file()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HISTORY_FIELDS)
        if new_file:
            writer.writeheader()
        for u in usages:
            writer.writerow({
                "run_date": today.isoformat(), "rule": u.rule.rel, "tier": u.rule.tier, "tokens": u.rule.tokens,
                "sessions": u.sessions, "applied": "" if u.applied is None else u.applied, "loaded": u.loaded,
                "misses": "" if u.misses is None else u.misses,
                "last_applied": u.last_applied.isoformat() if u.last_applied else "",
                "last_loaded": u.last_loaded.isoformat() if u.last_loaded else "",
            })


# ── report ────────────────────────────────────────────────────────────────────


def percent(count: int | None, total: int) -> str:
    """Format a count as ``NN% (n)``.

    :param count: Sessions counted, or None when unmeasurable.
    :type count: int | None
    :param total: All sessions.
    :type total: int
    :return: The formatted cell.
    :rtype: str
    """
    if count is None:
        return "—"
    return f"{round(100 * count / total) if total else 0}% ({count})"


def render_report(
    usages: list[Usage], sections: list[tuple[str, str, int]], sessions: list[Session], today: date
) -> str:
    """Build the markdown report.

    :param usages: Measured and flagged usage.
    :type usages: list[Usage]
    :param sections: Always-on section sizes, largest first.
    :type sections: list[tuple[str, str, int]]
    :param sessions: Parsed sessions.
    :type sessions: list[Session]
    :param today: The run date.
    :type today: date
    :return: Report markdown.
    :rtype: str
    """
    dates = sorted(s.last_date for s in sessions if s.last_date)
    window = f"{dates[0]} to {dates[-1]}" if dates else "no dated sessions"
    projects = Counter(s.project for s in sessions)
    always_on_tokens = sum(u.rule.tokens for u in usages if u.rule.always_on)
    lines = [
        "# 📊 Rule usage audit",
        "",
        f"**Generated:** {today} by `make audit_rule_usage` · **Sessions:** {len(sessions)} across "
        f"{len(projects)} projects · **Window:** {window}",
        "",
        f"**Always-on load:** ≈{always_on_tokens:,} tokens per session (characters ÷ 4).",
        "",
        "## 📖 How to read this",
        "",
        "- **Applied:** sessions that touched a file matching the rule's globs; `*` means every session.",
        "- **Loaded:** sessions where the rule reached Claude's context — imported, auto-loaded by `paths:`, or read.",
        "- **Misses:** sessions where the rule applied but was never loaded.",
        "- **Miss cost:** read from a `<!-- miss_cost: … -->` header; `—` until Phase 5 adds them.",
        f"- **Not enough data:** fewer than {MIN_SAMPLE_SESSIONS} applied sessions, so no other flag is set.",
        "- **No trigger:** a lazy rule with no `paths:` or default glob, so nothing can measure when it applies.",
        f"- **Cut-offs:** {MIN_SAMPLE_SESSIONS} sessions, {round(DEMOTE_APPLIED_BELOW * 100)}% and "
        f"{STALE_AFTER_DAYS} days are first guesses, to review after 3 reports.",
        "",
        "## 📋 Rules",
        "",
        "| Rule | Tier | Tokens | Applied | Loaded | Misses | Miss cost | Last applied | Last loaded | Flag |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for u in usages:
        lines.append(
            f"| `{u.rule.rel}` | {u.rule.tier[:2]} | {u.rule.tokens:,} | {percent(u.applied, u.sessions)} | "
            f"{percent(u.loaded, u.sessions)} | {'—' if u.misses is None else u.misses} | {u.rule.miss_cost} | "
            f"{u.last_applied or '—'} | {u.last_loaded or '—'} | {u.flag or '—'} |"
        )
    lines += [
        "",
        f"## 📐 Largest always-on sections (top {TOP_SECTIONS})",
        "",
        "| File | Section | Tokens |",
        "|---|---|---|",
    ]
    lines += [f"| `{rel}` | {heading} | {tokens:,} |" for rel, heading, tokens in sections[:TOP_SECTIONS]]
    lines += [
        "",
        "## 🗺️ Session spread",
        "",
        "Project names are hidden, since this report is committed to a public repo.",
        "",
        "| Project | Sessions |",
        "|---|---|",
    ]
    lines += [f"| project {i} | {n} |" for i, (_, n) in enumerate(projects.most_common(), start=1)]
    lines += [
        "",
        "## ⚠️ Limits",
        "",
        "- **Always-on misses:** a session misses an always-on rule when its startup file list doesn't name it — "
        "usually because the file was added or renamed after that session ran.",
        "- **Edits count as loads:** reading a rule file to edit it counts as loading it.",
        "- **Sub-agents skipped:** only main-session transcripts are read.",
        "- **Followed is not measured:** loaded means the rule was in context, not that Claude acted on it.",
        "",
    ]
    return "\n".join(lines)


# ── entry point ───────────────────────────────────────────────────────────────


def run(rules_dir: Path, transcripts_dir: Path, out_dir: Path, today: date) -> list[Usage]:
    """Measure usage, flag it, append history and write the report.

    :param rules_dir: The ``_rules`` folder.
    :type rules_dir: Path
    :param transcripts_dir: Claude Code's ``projects`` folder.
    :type transcripts_dir: Path
    :param out_dir: Where the report and history go.
    :type out_dir: Path
    :param today: The run date.
    :type today: date
    :return: The flagged usage rows.
    :rtype: list[Usage]
    """
    rules = discover_rules(rules_dir)
    sessions = discover_sessions(transcripts_dir, rules_dir)
    usages = measure(rules, sessions)
    history_path = out_dir / HISTORY_NAME
    history_last_used, first_run = read_history(history_path)
    starts = [d for d in [earliest(sessions), first_run] if d]
    data_start = min(starts) if starts else None
    for u in usages:
        candidates = [d for d in [u.last_applied, u.last_loaded, history_last_used.get(u.rule.rel)] if d]
        u.flag = flag_for(u, max(candidates) if candidates else None, data_start, today)
    out_dir.mkdir(parents=True, exist_ok=True)
    append_history(history_path, usages, today)
    report = render_report(usages, section_sizes(rules_dir, rules), sessions, today)
    (out_dir / REPORT_NAME).write_text(report, encoding="utf-8")
    return usages


def earliest(sessions: list[Session]) -> date | None:
    """Return the earliest session date, if any.

    :param sessions: Sessions to check.
    :type sessions: list[Session]
    :return: The earliest date, or None.
    :rtype: date | None
    """
    dates = [s.last_date for s in sessions if s.last_date]
    return min(dates) if dates else None


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run the audit.

    :param argv: Arguments after the script name; defaults to ``sys.argv[1:]``.
    :type argv: list[str] | None
    :return: 0 on success, 1 when a folder is missing.
    :rtype: int
    """
    parser = argparse.ArgumentParser(description="Measure how often each rule applies and loads.")
    parser.add_argument("--rules", required=True, type=Path, help="the _rules folder, e.g. src/claude/_rules")
    parser.add_argument("--transcripts", required=True, type=Path, help="session logs, e.g. ~/.claude/projects")
    parser.add_argument("--out", required=True, type=Path, help="output folder, e.g. src/claude/_admin/_audits")
    args = parser.parse_args(argv)
    for name in ("rules", "transcripts"):
        if not getattr(args, name).is_dir():
            print(f"error: --{name} folder not found: {getattr(args, name)}", file=sys.stderr)
            return 1
    usages = run(args.rules, args.transcripts, args.out, date.today())
    print(f"Wrote {args.out / REPORT_NAME} ({len(usages)} rules) and appended to {args.out / HISTORY_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
