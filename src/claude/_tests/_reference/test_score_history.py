# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates ``score_history.csv``, the append-only record of every scorecard run.

Issue #381 found that no scorecard recorded who scored it, with which model, or how many
attempts it took. Each row records one run, so re-runs show up as attempts 2, 3 and so on,
and the latest row for an artefact must match the Overall score its scorecard shows.
"""

import csv
import io
import re
from datetime import date

from _shared_paths import CLAUDE_DIR

CARDS = CLAUDE_DIR / "_reference" / "_quality_scorecards"
HISTORY = CARDS / "score_history.csv"
HEADER = ["run_date", "artefact", "type", "attempt", "reviewer", "model", "overall", "commit"]
TYPES = {"skill": "skills", "rule": "rules", "agent": "agents"}
SCORE = re.compile(r"^(10\.0|[1-9]\.\d)$")
COMMIT = re.compile(r"^([0-9a-f]{7,40}|uncommitted)$")
OVERALL = re.compile(r"^\*\*Overall score:\*\* ([\d.]+)/10\b", re.M)

VALID = """run_date,artefact,type,attempt,reviewer,model,overall,commit
2026-10-01,git,rule,1,author,unrecorded,8.7,33e91f0
2026-10-22,git,rule,2,quality_scorecard_reviewer,claude-opus-5-5,8.2,uncommitted
2026-10-05,code_reviewer,agent,1,author,unrecorded,8.9,b7e49c7
"""


def read_rows(text: str) -> tuple[list[str], list[dict]]:
    """Parse CSV text into its header and rows.

    :param text: Full CSV content.
    :return: The header fields and one dict per row.
    """
    reader = csv.DictReader(io.StringIO(text))
    return list(reader.fieldnames or []), list(reader)


def is_iso_date(value: str) -> bool:
    """Tell whether a value is a real ``YYYY-MM-DD`` date."""
    try:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)) and bool(date.fromisoformat(value))
    except ValueError:
        return False


def row_errors(row: dict) -> list[str]:
    """Return every field problem in one row.

    :param row: One parsed CSV row.
    :return: One message per problem; empty when the row is valid.
    """
    errors = []
    if not is_iso_date(row["run_date"] or ""):
        errors.append(f"run_date '{row['run_date']}' is not a YYYY-MM-DD date")
    if row["type"] not in TYPES:
        errors.append(f"type '{row['type']}' is not one of {sorted(TYPES)}")
    if not (row["attempt"] or "").isdigit() or int(row["attempt"]) < 1:
        errors.append(f"attempt '{row['attempt']}' is not a whole number from 1")
    if not SCORE.match(row["overall"] or ""):
        errors.append(f"overall '{row['overall']}' is not a score from 1.0 to 10.0")
    if not COMMIT.match(row["commit"] or ""):
        errors.append(f"commit '{row['commit']}' is not a short hash or 'uncommitted'")
    errors += [f"{field} is empty" for field in ("artefact", "reviewer", "model") if not row[field]]
    return errors


def history_errors(text: str) -> list[str]:
    """Return every problem in a history file: header, fields, and attempt order per artefact.

    :param text: Full CSV content.
    :return: One message per problem; empty when the file is valid.
    """
    header, rows = read_rows(text)
    if header != HEADER:
        return [f"header is {header}, expected {HEADER}"]
    errors, seen = [], {}
    for number, row in enumerate(rows, start=2):
        problems = row_errors(row)
        errors += [f"line {number}: {p}" for p in problems]
        if problems:
            continue
        key = (row["type"], row["artefact"])
        attempt, last_date = seen.get(key, (0, ""))
        if int(row["attempt"]) != attempt + 1:
            errors.append(f"line {number}: {key[1]} attempt {row['attempt']}, expected {attempt + 1}")
        if row["run_date"] < last_date:
            errors.append(f"line {number}: {key[1]} run_date {row['run_date']} is before attempt {attempt}")
        seen[key] = (int(row["attempt"]), row["run_date"])
    return errors


def scorecards(type_name: str) -> dict:
    """Map each scorecard of a type to its Overall score.

    :param type_name: ``skill``, ``rule`` or ``agent``.
    :return: Artefact name to header Overall score, as text.
    """
    found = {}
    for path in (CARDS / TYPES[type_name]).rglob("scorecard_*.md"):
        match = OVERALL.search(path.read_text())
        found[path.stem.removeprefix("scorecard_")] = match.group(1) if match else None
    return found


def latest_rows() -> dict:
    """Map each (type, artefact) in the real history to its last row."""
    return {(row["type"], row["artefact"]): row for row in read_rows(HISTORY.read_text())[1]}


# --- Accepted ---


def test_valid_history_accepted():
    """Rows with good fields and attempts numbered 1, 2 per artefact pass."""
    assert history_errors(VALID) == [], history_errors(VALID)


# --- Rejected ---


def test_wrong_header_rejected():
    """A missing or reordered column is caught before any row is read."""
    errors = history_errors(VALID.replace("attempt,reviewer", "reviewer,attempt"))
    assert errors and "header" in errors[0], errors


def test_score_out_of_range_rejected():
    """A score above 10, below 1, or without one decimal place is rejected."""
    for bad in ("10.5", "0.9", "8"):
        assert history_errors(VALID.replace(",8.9,", f",{bad},")), f"overall {bad} was accepted"


def test_skipped_attempt_rejected():
    """Attempts must count up by one, so a skipped re-run can't hide."""
    errors = history_errors(VALID.replace(",rule,2,", ",rule,3,"))
    assert errors and "expected 2" in errors[0], errors


def test_first_attempt_must_be_one():
    """An artefact's first row is attempt 1."""
    errors = history_errors(VALID.replace(",agent,1,", ",agent,2,"))
    assert errors and "expected 1" in errors[0], errors


def test_attempt_dated_before_previous_rejected():
    """A re-run can't be dated before the attempt it follows."""
    errors = history_errors(VALID.replace("2026-10-22,git", "2026-09-01,git"))
    assert errors and "before attempt 1" in errors[0], errors


def test_bad_fields_rejected():
    """A bad date, unknown type, bad commit and empty reviewer are each caught."""
    for old, new in (("2026-10-05", "05/10/2026"), (",agent,", ",hook,"), ("b7e49c7", "HEAD"), (",author,", ",,")):
        assert history_errors(VALID.replace(old, new)), f"{new!r} was accepted"


# --- Real history ---


def test_real_history_is_valid():
    """The committed history has the right header, valid fields and attempt order."""
    assert HISTORY.is_file(), f"{HISTORY} is missing"
    errors = history_errors(HISTORY.read_text())
    assert not errors, errors


def test_every_row_has_a_scorecard():
    """Each artefact in the history has a scorecard in its type's folder."""
    for type_name, artefact in latest_rows():
        assert artefact in scorecards(type_name), f"{artefact} ({type_name}) has no scorecard"


def test_every_scorecard_has_a_row():
    """Each skill, rule and agent scorecard has at least one history row."""
    rows = latest_rows()
    for type_name in TYPES:
        cards = scorecards(type_name)
        assert cards, f"no {type_name} scorecards found, so this check proves nothing"
        missing = sorted(name for name in cards if (type_name, name) not in rows)
        assert not missing, f"{type_name} scorecards with no history row: {missing}"


def test_latest_row_matches_scorecard():
    """An artefact's latest run is the score its scorecard shows."""
    for (type_name, artefact), row in latest_rows().items():
        shown = scorecards(type_name).get(artefact)
        assert row["overall"] == shown, f"{artefact}: history says {row['overall']}, scorecard says {shown}"
