# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates the root ``Makefile``: its install targets, and that its usage list matches its targets.

``make`` with no target prints the usage block, so a target missing from it is invisible and a
listed one that doesn't exist fails when someone types it. The install checks were split from
``test_install_claude_files.py`` on 2026-10-02.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from _install_sandbox import REPO_ROOT, make_sandbox, nothing_changed

MAKEFILE = REPO_ROOT / "Makefile"
TEXT = MAKEFILE.read_text()
TARGETS = set(re.findall(r"^([a-z_]+):", TEXT, re.M))
PHONY = set(next(line for line in TEXT.splitlines() if line.startswith(".PHONY:")).split()[1:])
USAGE = dict(re.findall(r"^# make ([a-z_]+)\s+# (.*)$", TEXT, re.M))


def recipe(target: str) -> str:
    """Return a target's recipe lines, the tab-indented lines under its name.

    :param target: Target name.
    :return: The recipe text, or an empty string if the target has none.
    """
    match = re.search(rf"^{target}:.*\n((?:\t.*\n)*)", TEXT, re.M)
    return match.group(1) if match else ""


def test_install_target_is_live():
    """``install`` is a real target, not commented out."""
    assert "install" in TARGETS, "Makefile has no live install target"


def test_install_is_phony():
    """``install`` is in ``.PHONY``, so a file called install can't block it."""
    assert "install" in PHONY, "install is not in .PHONY"


def test_install_usage_is_not_disabled():
    """The usage list no longer marks ``make install`` as disabled."""
    assert "[DISABLED]" not in USAGE["install"], "Usage line still marks make install as disabled"


def test_install_runs_the_install_script():
    """``make install`` runs ``install_claude_files.sh``, which holds the typed-confirmation gate."""
    assert "bash src/sh/claude/install_claude_files.sh" in recipe("install"), "install must run the gated script"


def test_install_windows_runs_its_script():
    """``make install_windows`` runs the Windows sync script."""
    assert "bash src/sh/claude/install_claude_files_windows.sh" in recipe("install_windows")


def test_update_windows_is_an_alias():
    """``update_windows`` just depends on ``install_windows``, as its usage line says."""
    assert re.search(r"^update_windows: install_windows$", TEXT, re.M), "update_windows should alias install_windows"


def test_every_phony_name_is_a_target():
    """Every name in ``.PHONY`` is defined, so the list can't name a target that was removed."""
    assert not PHONY - TARGETS, f".PHONY names undefined targets: {sorted(PHONY - TARGETS)}"


def test_every_usage_entry_exists_or_is_disabled():
    """Each ``# make X`` line is a real target, unless it's marked ``[DISABLED]``."""
    missing = [name for name, text in USAGE.items() if name not in TARGETS and "[DISABLED]" not in text]
    assert not missing, f"Usage lists targets that don't exist: {missing}"


def test_disabled_entries_are_not_live():
    """A target marked ``[DISABLED]`` in the usage list really is switched off."""
    live = [name for name, text in USAGE.items() if "[DISABLED]" in text and name in TARGETS]
    assert not live, f"Usage says these are disabled, but they're live targets: {live}"


def test_every_target_is_in_the_usage_list():
    """Every Makefile target appears in the usage block that ``make`` prints."""
    undocumented = sorted(TARGETS - set(USAGE))
    assert not undocumented, f"Targets missing from the usage list: {undocumented}"


def test_all_prints_the_usage_block():
    """``make all`` prints the ``# make`` lines, so the usage list is what users actually see."""
    assert "grep -E '^# make ' Makefile" in recipe("all"), "make all should print the usage block"


def test_test_target_runs_pytest():
    """``make test`` runs pytest, which reads its test folders from pytest.ini."""
    assert "@pytest" in recipe("test"), "make test should run pytest"


def test_make_install_refuses_without_tty(tmp_path: Path):
    """``make install`` from a non-terminal passes on the script's refusal and changes nothing."""
    box = make_sandbox(tmp_path)
    result = subprocess.run(
        ["make", "install"], cwd=REPO_ROOT, env=box["env"],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, timeout=30,
    )
    assert result.returncode != 0, "make install must fail without a terminal"
    assert "run from your own terminal" in result.stdout, "make install must pass through the refusal message"
    assert nothing_changed(box) == [], f"make install ran past the gate: {nothing_changed(box)}"
