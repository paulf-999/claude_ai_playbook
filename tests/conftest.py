"""pytest configuration: custom human-readable summary for Claude config validation."""

from collections import defaultdict
from typing import Any

import pytest

# Accumulate results during the session: category -> [(status, file_ref, message)]
_results: dict[str, list[tuple[str, str, str]]] = defaultdict(list)


def _category(nodeid: str) -> str:
    """Derive a human-readable category name from a test node ID.

    :param nodeid: pytest node ID, e.g. 'tests/test_agents.py::test_agent_has_valid_frontmatter[foo.md]'
    :type nodeid: str
    :return: Category name, e.g. 'agents'
    :rtype: str
    """
    filename = nodeid.split("::")[0].split("/")[-1]  # 'test_agents.py'
    return filename.removeprefix("test_").removesuffix(".py")  # 'agents'


def _file_ref(nodeid: str) -> str:
    """Extract the parametrised file reference from a test node ID.

    :param nodeid: pytest node ID.
    :type nodeid: str
    :return: File reference (e.g. 'example_broken_agent.md'), or '' if not parametrised.
    :rtype: str
    """
    if "[" in nodeid and nodeid.endswith("]"):
        return nodeid[nodeid.index("[") + 1:-1]
    return ""


def _error_message(report: Any) -> str:
    """Extract the human-readable assertion message from a failed test report.

    :param report: pytest test report object.
    :type report: Any
    :return: The assertion message string.
    :rtype: str
    """
    try:
        msg = report.longrepr.reprcrash.message
        if msg.startswith("AssertionError: "):
            msg = msg[len("AssertionError: "):]
        # reprcrash.message may include pytest's assert-rewriting detail on subsequent lines
        return msg.splitlines()[0].strip()
    except (AttributeError, IndexError):
        pass
    text = str(report.longrepr)
    for line in text.splitlines():
        if "AssertionError:" in line:
            return line.split("AssertionError:", 1)[1].strip()
    return "test failed"


@pytest.hookimpl()
def pytest_runtest_logreport(report: Any) -> None:
    """Collect each test result for the custom summary.

    :param report: pytest test report for a single test phase.
    :type report: Any
    """
    if report.when != "call":  # each test runs in setup/call/teardown phases; only record the body result
        return
    cat = _category(report.nodeid)
    ref = _file_ref(report.nodeid)
    if report.failed:
        _results[cat].append(("FAILED", ref, _error_message(report)))
    elif report.passed:
        _results[cat].append(("PASSED", ref, ""))


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter: Any, exitstatus: int, config: Any) -> None:
    """Print a grouped, human-readable validation summary.

    :param terminalreporter: pytest terminal reporter plugin.
    :type terminalreporter: Any
    :param exitstatus: Overall exit status code.
    :type exitstatus: int
    :param config: pytest config object.
    :type config: Any
    """
    if not _results:
        return

    terminalreporter.write_sep("=", "Claude config validation")
    terminalreporter.write_line("")

    failures_by_file: dict[str, list[str]] = defaultdict(list)

    for cat in sorted(_results):
        entries = _results[cat]
        total = len(entries)
        n_failed = sum(1 for s, _, __ in entries if s == "FAILED")

        if n_failed == 0:
            status = "PASSED"
            detail = f"{total} checks"
        else:
            status = "FAILED"
            detail = f"{n_failed} of {total} checks failed"

        terminalreporter.write_line(f"  {status:<8}  {cat:<30} {detail}")

        for s, ref, msg in entries:
            if s == "FAILED":
                key = f"{cat}/{ref}" if ref else cat
                failures_by_file[key].append(msg)

    if failures_by_file:
        terminalreporter.write_line("")
        terminalreporter.write_line("  What needs fixing:")
        for file_key in sorted(failures_by_file):
            terminalreporter.write_line(f"    {file_key}")
            for msg in failures_by_file[file_key]:
                terminalreporter.write_line(f"      x  {msg}")

    terminalreporter.write_line("")
