#!/usr/bin/env python3
"""Measure how often each rule applies to a session, and how often it was loaded.

Reads Claude Code session transcripts and the rule folders (``rules/`` and the
``_rules_lazy_load/`` beside it), then writes a markdown
report and appends one row per rule to a CSV history, so dates survive after old
transcripts are deleted.

- **Applied:** the session touched a file matching the rule's globs (``*`` = every session).
- **Loaded:** the rule reached Claude's context — a ``rules/`` file loaded natively,
  a ``paths:`` rule loaded with a matching file, or a ``Read`` of the rule file.
- **Miss:** the rule applied but was never loaded.

Standard library only, no LLM calls. Every location is a required argument, because the
script is installed into the live config too and must never guess the repo.

Usage:
    python3 src/claude/_scripts/_audit_scripts/audit_rule_usage.py \\
        --rules src/claude/rules --transcripts ~/.claude/projects --out src/claude/_admin/_audits
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
from typing import Any

# ── first-guess cut-offs — review after 3 reports ─────────────────────────────

# First guess: fewer applied sessions than this shows "not enough data"
MIN_SAMPLE_SESSIONS = 10
# First guess: an always-on rule applying in fewer sessions may be lazy
DEMOTE_APPLIED_BELOW = 0.5
# First guess: no use for this long marks a rule stale
STALE_AFTER_DAYS = 90

# ── constants ─────────────────────────────────────────────────────────────────

EVERY_SESSION = "*"
LAZY_FOLDER = "_rules_lazy_load"
PATH_SCOPED_TIER = "05_path_scoped"
REPORT_NAME = "audit_rule_usage.md"
HISTORY_NAME = "rule_usage_history.csv"
LEDGER_NAME = "rule_usage_sessions.csv"
SUMMARY_NAME = "rule_usage_history.md"
LEDGER_FIELDS = ["session", "date", "rule", "applied", "loaded"]
TOP_INSIGHTS = 5
TIER_TITLES = {
    "01_essentials": "🧭 01 Essentials",
    "02_claude_standards": "🛡️ 02 Claude standards",
    "03_authoring_guidelines": "🛠️ 03 Authoring guidelines",
    "04_claude_reference": "📚 04 Claude reference",
    "05_path_scoped": "🪶 05 Path-scoped",
    LAZY_FOLDER: "💤 Lazy load",
}
HISTORY_FIELDS = [
    "run_date", "rule", "tier", "tokens", "sessions", "applied", "loaded", "misses", "last_applied", "last_loaded",
]
TOP_SECTIONS = 15
CHARS_PER_TOKEN = 4
TIER_DIR = re.compile(r"^\d\d_")
# A rule path in a transcript: the new folders, or the old _rules/ layout older sessions used
RULE_PATH = re.compile(r"(?:^|/)(rules|_rules_lazy_load|_rules)/(\S+\.md)$")
# A parent's pointer to a child that loads on its own from rules/
NATIVE_POINTER = re.compile(r"^- \*\*Loads on its own from:\*\* `(rules/\S+\.md)`", re.M)
MISS_COST = re.compile(r"<!--\s*miss_cost:\s*(high|medium|low)\b", re.I)
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}

APPLIES_TO = re.compile(r"^<!--\s*applies_to:\s*(.+?)\s*-->$")
# paths: frontmatter (up to 4) + version, created, updated, applies_to, miss_cost
HEADER_LINES = 10

# First-guess globs for lazy rules with no ``applies_to`` header and no ``paths:`` frontmatter,
# keyed by path under 05_path_scoped/ or _rules_lazy_load/.
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
    path_scoped: bool = False

    @property
    def always_on(self) -> bool:
        """Whether the rule loads every session.

        :return: True for rules/ files without ``paths:`` (tiers 01–04).
        :rtype: bool
        """
        return not self.path_scoped and self.tier not in (PATH_SCOPED_TIER, LAZY_FOLDER)


@dataclass
class Session:
    """What one session touched and which rules reached its context."""

    project: str
    last_date: date | None = None
    touched: set[str] = field(default_factory=set)
    loaded: set[str] = field(default_factory=set)
    sid: str = ""


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


def is_child(path: Path, tier_dir: Path, roots: tuple[Path, ...] = ()) -> bool:
    """Tell whether a rule file belongs to a parent topic rather than standing alone.

    :param path: Rule file path.
    :type path: Path
    :param tier_dir: The tier folder the file sits in.
    :type tier_dir: Path
    :param roots: Other folders a parent may sit in, since a lazy child's parent can live under rules/.
    :type roots: tuple[Path, ...]
    :return: True when the name starts with ``_`` or a folder above it has a parent ``.md`` in any root.
    :rtype: bool
    """
    if path.name.startswith("_"):
        return True
    for folder in path.parents:
        if folder == tier_dir:
            return False
        rel = folder.relative_to(tier_dir).with_suffix(".md")
        if folder.with_suffix(".md").is_file() or any((root / rel).is_file() for root in roots):
            return True
    return False


def native_files(path: Path, rules_dir: Path) -> list[Path]:
    """Return a rules/ entry point and the children that load beside it, i.e. those without ``paths:``.

    :param path: An entry-point rule under rules/.
    :type path: Path
    :param rules_dir: The ``rules`` folder its pointers are relative to.
    :type rules_dir: Path
    :return: The rule first, then each child in its ``<topic>/`` folder or named in a ``Loads on its own from`` line.
    :rtype: list[Path]
    """
    folder = path.with_suffix("")
    children = sorted(folder.rglob("*.md")) if folder.is_dir() else []
    # Shared children, e.g. shared_standards/_complexity_scoring.md, sit outside the topic folder
    children += [rules_dir.parent / rel for rel in NATIVE_POINTER.findall(path.read_text(encoding="utf-8"))]
    found = [path]
    for child in children:
        if child.is_file() and child not in found and not frontmatter_paths(child.read_text(encoding="utf-8")):
            found.append(child)
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


def header_globs(text: str) -> list[str]:
    """Read the globs from a rule's ``<!-- applies_to: … -->`` header line.

    :param text: Rule file content.
    :type text: str
    :return: The globs, or an empty list when the rule has no header.
    :rtype: list[str]
    """
    for line in text.splitlines()[:HEADER_LINES]:
        match = APPLIES_TO.match(line)
        if match:
            return [glob.strip() for glob in match.group(1).split(",") if glob.strip()]
    return []


def token_count(config_dir: Path, rels: list[str]) -> int:
    """Estimate tokens as characters divided by four.

    :param config_dir: The config folder the paths are relative to.
    :type config_dir: Path
    :param rels: Rule files to count.
    :type rels: list[str]
    :return: Estimated tokens.
    :rtype: int
    """
    return sum(len((config_dir / rel).read_text(encoding="utf-8")) for rel in rels) // CHARS_PER_TOKEN


def discover_rules(rules_dir: Path) -> list[Rule]:
    """Find every entry-point rule in the rules/ tiers and in _rules_lazy_load/ beside it.

    :param rules_dir: The ``rules`` folder.
    :type rules_dir: Path
    :return: Rules sorted by tier then path, each keyed by its path from the config folder.
    :rtype: list[Rule]
    """
    config_dir, lazy_dir = rules_dir.parent, rules_dir.parent / LAZY_FOLDER
    tier_dirs = sorted(d for d in rules_dir.iterdir() if d.is_dir() and TIER_DIR.match(d.name))
    roots = tuple(tier_dirs) + ((lazy_dir,) if lazy_dir.is_dir() else ())
    rules = []
    for tier_dir in roots:
        for path in sorted(tier_dir.rglob("*.md")):
            in_tier = path.relative_to(tier_dir)
            if path.name == "README.md" or in_tier.parts[0] in ("_tier_readmes", "learned"):
                continue
            if is_child(path, tier_dir, tuple(r for r in roots if r != tier_dir)):
                continue
            rel = path.relative_to(config_dir).as_posix()
            text = path.read_text(encoding="utf-8")
            scoped = bool(frontmatter_paths(text))
            if scoped or tier_dir == lazy_dir:
                files = [rel]
                fallback = frontmatter_paths(text) or DEFAULT_APPLIES_TO.get(in_tier.as_posix(), [])
            else:
                files = [f.relative_to(config_dir).as_posix() for f in native_files(path, rules_dir)]
                fallback = [EVERY_SESSION]
            globs = header_globs(text) or fallback
            cost = MISS_COST.search(text)
            rules.append(Rule(
                rel=rel,
                tier=tier_dir.name,
                tokens=token_count(config_dir, files),
                globs=globs,
                miss_cost=cost.group(1).lower() if cost else "—",
                files=files,
                path_scoped=scoped,
            ))
    return rules


def section_sizes(rules_dir: Path, rules: list[Rule]) -> list[tuple[str, str, int]]:
    """Size every ``##`` section in the always-on files, largest first.

    :param rules_dir: The ``rules`` folder.
    :type rules_dir: Path
    :param rules: Discovered rules.
    :type rules: list[Rule]
    :return: ``(file, heading, tokens)`` tuples.
    :rtype: list[tuple[str, str, int]]
    """
    sizes = []
    files = {rel for rule in rules if rule.always_on for rel in rule.files}
    for rel in sorted(files):
        for chunk in re.split(r"^(?=## )", (rules_dir.parent / rel).read_text(encoding="utf-8"), flags=re.M)[1:]:
            sizes.append((rel, chunk.splitlines()[0][3:].strip(), len(chunk) // CHARS_PER_TOKEN))
    return sorted(sizes, key=lambda s: -s[2])


# ── transcripts ───────────────────────────────────────────────────────────────


def rule_rel(raw: str, rules_dir: Path) -> str | None:
    """Map a path seen in a transcript to a rule path relative to the config folder.

    Handles the repo copy, the live copy, and the layout older sessions used before 2026-10-06:
    ``_rules/0X_tier/...``, ``_rules/05_lazy_load/...`` and the flat ``rules/<name>.md`` links.

    :param raw: A file path from the transcript.
    :type raw: str
    :param rules_dir: The ``rules`` folder.
    :type rules_dir: Path
    :return: The rule path, e.g. ``rules/01_essentials/x.md``, or None when it isn't a rule.
    :rtype: str | None
    """
    match = RULE_PATH.search(raw)
    if not match:
        return None
    folder, rest = match.groups()
    if folder == LAZY_FOLDER:
        return f"{LAZY_FOLDER}/{rest}"
    if folder == "_rules":
        if not rest.startswith("05_lazy_load/"):
            return f"rules/{rest}"
        rest = rest.removeprefix("05_lazy_load/")
        scoped = (rules_dir / PATH_SCOPED_TIER / rest).is_file()
        return f"rules/{PATH_SCOPED_TIER}/{rest}" if scoped else f"{LAZY_FOLDER}/{rest}"
    if "/" in rest:
        return f"rules/{rest}"
    # A flat rules/<name>.md was an old install link to a path-scoped rule
    found = sorted(rules_dir.rglob(rest))
    return f"rules/{found[0].relative_to(rules_dir).as_posix()}" if len(found) == 1 else None


def record_date(record: dict[str, Any]) -> date | None:
    """Read the day from a record's ISO timestamp.

    :param record: One transcript record.
    :type record: dict[str, Any]
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


def tool_calls(record: dict[str, Any]) -> list[tuple[str, str]]:
    """List the file tools an assistant record calls.

    :param record: One transcript record.
    :type record: dict[str, Any]
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


def attachment_paths(attachment: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Split an attachment into files it loaded into context and files it says were edited.

    :param attachment: The record's ``attachment`` object.
    :type attachment: dict[str, Any]
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
    :param rules_dir: The ``rules`` folder.
    :type rules_dir: Path
    :return: The session's touched files, loaded rules and last date.
    :rtype: Session
    """
    session = Session(project=path.parent.name, sid=path.stem)
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
    :param rules_dir: The ``rules`` folder.
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


def append_history(path: Path, usages: list[Usage], today: date):
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
        "- **Applied:** sessions that touched a file matching the rule's `applies_to` globs (or its `paths:` "
        "or a built-in default for lazy rules); `*` means every session.",
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
            f"| `{u.rule.rel}` | {tier_code(u.rule.tier)} | {u.rule.tokens:,} | {percent(u.applied, u.sessions)} | "
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


# ── all-time session ledger ───────────────────────────────────────────────────


def session_rows(rules: list[Rule], sessions: list[Session]) -> list[dict[str, str]]:
    """Build one ledger row per session and rule where the rule applied or loaded.

    :param rules: Discovered rules.
    :type rules: list[Rule]
    :param sessions: Parsed sessions.
    :type sessions: list[Session]
    :return: Rows keyed by ``LEDGER_FIELDS``.
    :rtype: list[dict[str, str]]
    """
    rows = []
    for session in sessions:
        for rule in rules:
            applied = bool(rule.globs) and applies(rule, session)
            loaded = rule.rel in session.loaded
            if applied or loaded:
                rows.append({
                    "session": session.sid,
                    "date": session.last_date.isoformat() if session.last_date else "",
                    "rule": rule.rel,
                    "applied": str(int(applied)),
                    "loaded": str(int(loaded)),
                })
    return rows


def update_ledger(path: Path, rules: list[Rule], sessions: list[Session]) -> list[dict[str, str]]:
    """Record each session once per rule, replacing rows for sessions seen again.

    Sessions whose logs are gone keep their old rows, so the totals survive log deletion.

    :param path: The ledger CSV.
    :type path: Path
    :param rules: Discovered rules.
    :type rules: list[Rule]
    :param sessions: Parsed sessions.
    :type sessions: list[Session]
    :return: Every ledger row after the update.
    :rtype: list[dict[str, str]]
    """
    existing = []
    if path.is_file():
        with path.open(newline="", encoding="utf-8") as handle:
            existing = list(csv.DictReader(handle))
    measured = {s.sid for s in sessions}
    rows = [r for r in existing if r["session"] not in measured] + session_rows(rules, sessions)
    rows.sort(key=lambda r: (r["date"], r["session"], r["rule"]))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def run_dates(path: Path) -> dict[str, set[str]]:
    """Read the distinct run dates per rule from the history CSV.

    :param path: The history file.
    :type path: Path
    :return: Run dates keyed by rule.
    :rtype: dict[str, set[str]]
    """
    dates: dict[str, set[str]] = {}
    if path.is_file():
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                dates.setdefault(row["rule"], set()).add(row["run_date"])
    return dates


def rule_totals(rows: list[dict[str, str]]) -> dict[str, Any]:
    """Total one rule's ledger rows.

    :param rows: The rule's ledger rows.
    :type rows: list[dict[str, str]]
    :return: ``applied``, ``loaded``, ``misses``, ``rate`` (a fraction, or None) and ``first``/``last`` dates.
    :rtype: dict[str, Any]
    """
    applied = sum(r["applied"] == "1" for r in rows)
    misses = sum(r["applied"] == "1" and r["loaded"] == "0" for r in rows)
    seen = sorted(r["date"] for r in rows if r["date"])
    return {
        "applied": applied,
        "loaded": sum(r["loaded"] == "1" for r in rows),
        "misses": misses,
        "rate": misses / applied if applied else None,
        "first": seen[0] if seen else "—",
        "last": seen[-1] if seen else "—",
    }


def insight_lines(totals: dict[str, dict], every_session: set[str]) -> list[str]:
    """Summarise the worst miss rates and the most used rules, above the tables.

    :param totals: ``rule_totals`` keyed by rule.
    :type totals: dict[str, dict]
    :param every_session: Rules whose globs are ``*``, which apply to every session by definition.
    :type every_session: set[str]
    :return: Markdown lines.
    :rtype: list[str]
    """
    heading = f"### 🔥 Highest miss rates (at least {MIN_SAMPLE_SESSIONS} applied sessions)"
    lines = ["## 🔎 Key insights", "", heading, ""]
    measurable = [(rel, t) for rel, t in totals.items() if t["applied"] >= MIN_SAMPLE_SESSIONS and t["misses"]]
    worst = sorted(measurable, key=lambda item: (-item[1]["rate"], -item[1]["misses"], item[0]))[:TOP_INSIGHTS]
    lines += [
        f"{i}. `{rel}` — missed {t['misses']} of {t['applied']} sessions ({round(100 * t['rate'])}%)"
        for i, (rel, t) in enumerate(worst, start=1)
    ] or [f"No rule has missed loads across {MIN_SAMPLE_SESSIONS} or more applied sessions yet."]
    small = sum(1 for t in totals.values() if 0 < t["applied"] < MIN_SAMPLE_SESSIONS and t["misses"])
    if small:
        lines += [
            "",
            f"- **Too few sessions to rank:** {small} more rules have misses "
            f"but under {MIN_SAMPLE_SESSIONS} applied sessions.",
        ]
    lines += ["", "### ⭐ Most used", ""]
    always = [totals[rel] for rel in every_session if rel in totals]
    if always:
        loads = sorted(t["loaded"] for t in always)
        lines += [
            f"- **Every-session rules:** {len(always)} rules apply to every session (`applies_to: *`), "
            f"loaded in {loads[0]}–{loads[-1]} sessions each.",
        ]
    rest = sorted(
        ((rel, t) for rel, t in totals.items() if rel not in every_session and t["applied"]),
        key=lambda item: (-item[1]["applied"], item[0]),
    )[:TOP_INSIGHTS]
    if rest:
        lines += ["- **Most needed of the rest, by sessions applied:**", ""]
        lines += [
            f"{i}. `{rel}` — applied in {t['applied']} sessions, loaded in {t['loaded']}"
            for i, (rel, t) in enumerate(rest, start=1)
        ]
    return lines + [""]


def tier_code(tier: str) -> str:
    """Return a tier's short label for report tables: its number, or ``lazy`` for the lazy folder.

    :param tier: e.g. ``01_essentials`` or ``_rules_lazy_load``.
    :type tier: str
    :return: e.g. ``01`` or ``lazy``.
    :rtype: str
    """
    return tier[:2] if tier[0].isdigit() else "lazy"


def tier_of(rel: str) -> str:
    """Return the tier a rule path belongs to: its rules/ tier folder, or the lazy folder.

    :param rel: Rule path from the config folder, e.g. ``rules/01_essentials/x.md``.
    :type rel: str
    :return: e.g. ``01_essentials`` or ``_rules_lazy_load``.
    :rtype: str
    """
    parts = rel.split("/")
    return parts[1] if parts[0] == "rules" and len(parts) > 2 else parts[0]


def tier_tables(totals: dict[str, dict], runs: dict[str, set[str]], current: set[str]) -> list[str]:
    """Build one table per tier.

    :param totals: ``rule_totals`` keyed by rule.
    :type totals: dict[str, dict]
    :param runs: Distinct run dates per rule.
    :type runs: dict[str, set[str]]
    :param current: Rules that still exist.
    :type current: set[str]
    :return: Markdown lines.
    :rtype: list[str]
    """
    lines = ["## 📋 Rules by tier", ""]
    for tier in sorted({tier_of(rel) for rel in totals}):
        lines += [
            f"### {TIER_TITLES.get(tier, f'📁 {tier}')}",
            "",
            "| Rule | Applied | Loaded | Misses | Miss rate | Runs | First seen | Last used |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for rel in sorted(r for r in totals if tier_of(r) == tier):
            t = totals[rel]
            rate = f"{round(100 * t['rate'])}%" if t["rate"] is not None else "—"
            name = f"`{rel}`" if rel in current else f"`{rel}` (removed)"
            lines.append(
                f"| {name} | {t['applied']} | {t['loaded']} | {t['misses']} | {rate} | "
                f"{len(runs.get(rel, ()))} | {t['first']} | {t['last']} |"
            )
        lines.append("")
    return lines


def render_history(
    ledger: list[dict[str, str]], rules: list[Rule], runs: dict[str, set[str]], today: date
) -> str:
    """Build the all-time summary, counting each session once per rule.

    :param ledger: Every ledger row.
    :type ledger: list[dict[str, str]]
    :param rules: Discovered rules, so rules with no rows still get a line.
    :type rules: list[Rule]
    :param runs: Distinct run dates per rule.
    :type runs: dict[str, set[str]]
    :param today: The run date.
    :type today: date
    :return: Summary markdown.
    :rtype: str
    """
    current = {rule.rel for rule in rules}
    by_rule: dict[str, list[dict[str, str]]] = {rel: [] for rel in current}
    for row in ledger:
        by_rule.setdefault(row["rule"], []).append(row)
    totals = {rel: rule_totals(rows) for rel, rows in by_rule.items()}
    every_session = {rule.rel for rule in rules if EVERY_SESSION in rule.globs}
    dates = sorted(r["date"] for r in ledger if r["date"])
    all_runs = set().union(*runs.values()) if runs else set()
    lines = [
        "# 📈 Rule usage history",
        "",
        f"**Generated:** {today} by `make audit_rule_usage` · **Sessions recorded:** "
        f"{len({r['session'] for r in ledger})}"
        + (f" ({dates[0]} to {dates[-1]})" if dates else "")
        + f" · **Runs:** {len(all_runs)}",
        "",
        "Each session counts once per rule, however many runs saw it. Sessions stay in the record "
        "after Claude Code deletes their logs, so these totals keep growing past the 90-day log limit.",
        "",
        "## 📖 How to read this",
        "",
        "- **Applied / Loaded / Misses:** sessions, all time — the same meaning as in `audit_rule_usage.md`.",
        "- **Miss rate:** misses as a share of applied sessions.",
        "- **Runs:** distinct days `make audit_rule_usage` measured the rule.",
        "- **First seen / Last used:** the earliest and latest session where the rule applied or loaded.",
        "- **Removed:** a rule in the record that no longer exists, usually after a rename.",
        "",
    ]
    lines += insight_lines(totals, every_session)
    lines += tier_tables(totals, runs, current)
    lines += [
        "## ⚠️ Limits",
        "",
        "- **Always-on misses:** usually sessions that ran before the file was added or renamed, "
        "not times Claude skipped it.",
        "- **Globs at measure time:** a session's applied value uses the rule's globs from the last run "
        "that still had its log, so changing a rule's `applies_to` doesn't rewrite older sessions.",
        f"- **Starts at the first run:** sessions deleted before {min(all_runs) if all_runs else 'the first run'} "
        "were never recorded.",
        "",
    ]
    return "\n".join(lines)


# ── entry point ───────────────────────────────────────────────────────────────


def run(rules_dir: Path, transcripts_dir: Path, out_dir: Path, today: date) -> list[Usage]:
    """Measure usage, flag it, append history, update the session ledger and write both reports.

    :param rules_dir: The ``rules`` folder.
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
    ledger = update_ledger(out_dir / LEDGER_NAME, rules, sessions)
    summary = render_history(ledger, rules, run_dates(history_path), today)
    (out_dir / SUMMARY_NAME).write_text(summary, encoding="utf-8")
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
    parser.add_argument("--rules", required=True, type=Path, help="the rules folder, e.g. src/claude/rules")
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
