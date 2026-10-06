# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           1.3.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that every lazy rule has something that makes Claude load it.

A lazy rule loads only through a trigger: ``paths:`` frontmatter (it then lives under
``rules/``), a hook that names it, or a pointer in a file Claude already has — an always-on
rule under ``rules/``, a file ``CLAUDE.md`` imports, or a skill's own files. A mention in a
README doesn't count, because no README is ever loaded.
"""
import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, CLAUDE_MD, HOOKS_DIR, LAZY_RULES_DIR, RULES_DIR, SKILLS_DIR

LAZY_DIR = LAZY_RULES_DIR
PATH_SCOPED_DIR = RULES_DIR / "04_path_scoped"
ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines")
# Folders under _rules_lazy_load/ that hold indexes or ledgers rather than rules
NON_RULE_FOLDERS = {"_tier_readmes", "_learned"}
IMPORT = re.compile(r"^@~/[^/\s]+/(\S+\.md)\s*$", re.M)


def imported_texts(root: Path, claude_md: Path) -> dict[str, str]:
    """Follow ``@`` imports from CLAUDE.md, returning every file loaded at startup.

    :param root: The config directory imports resolve against.
    :type root: Path
    :param claude_md: The CLAUDE.md to start from.
    :type claude_md: Path
    :return: File text keyed by path relative to ``root``.
    :rtype: dict[str, str]
    """
    texts = {"CLAUDE.md": claude_md.read_text()}
    pending = IMPORT.findall(texts["CLAUDE.md"])
    while pending:
        rel = pending.pop()
        path = root / rel
        if rel in texts or not path.is_file():
            continue
        texts[rel] = path.read_text()
        pending += IMPORT.findall(texts[rel])
    return texts


def skill_texts(skills_dir: Path) -> dict[str, str]:
    """Return the text of every skill file Claude reads when the skill runs, skipping READMEs.

    :param skills_dir: The ``skills`` folder.
    :type skills_dir: Path
    :return: File text keyed by path.
    :rtype: dict[str, str]
    """
    return {str(p): p.read_text() for p in skills_dir.rglob("*.md") if p.name != "README.md"}


def native_texts(rules_dir: Path) -> dict[str, str]:
    """Return every rules/ file Claude Code loads at session start, i.e. those without paths:.

    :param rules_dir: The ``rules/`` folder.
    :type rules_dir: Path
    :return: File text keyed by path relative to the config directory.
    :rtype: dict[str, str]
    """
    return {
        p.relative_to(rules_dir.parent).as_posix(): p.read_text()
        for p in sorted(rules_dir.rglob("*.md")) if not has_paths(p.read_text())
    }


def loaded_texts() -> dict[str, str]:
    """Return everything Claude already has in a session: imports, native rules and skill files."""
    return {**imported_texts(CLAUDE_DIR, CLAUDE_MD), **native_texts(RULES_DIR), **skill_texts(SKILLS_DIR)}


def has_paths(text: str) -> bool:
    """Tell whether a rule opens with ``paths:`` frontmatter.

    :param text: Rule file text.
    :type text: str
    :return: True when the frontmatter declares ``paths:``.
    :rtype: bool
    """
    return text.startswith("---\n") and "\npaths:" in text.split("\n---", 1)[0]


def trigger_for(inner: str, text: str, loaded: dict[str, str], hooks: list[str]) -> str:
    """Name the trigger that loads a lazy rule, or return an empty string.

    :param inner: Rule path relative to ``_rules_lazy_load``, e.g. ``style_guide_standards/jira.md``.
    :type inner: str
    :param text: Rule file text.
    :type text: str
    :param loaded: Texts Claude already has, from startup imports and skills.
    :type loaded: dict[str, str]
    :param hooks: Text of every hook script.
    :type hooks: list[str]
    :return: ``paths``, ``hook``, ``pointer`` or ``""``.
    :rtype: str
    """
    if has_paths(text):
        return "paths"
    if any(f"_rules_lazy_load/{inner}" in hook for hook in hooks):
        return "hook"
    if any(f"_rules_lazy_load/{inner}" in body for body in loaded.values()):
        return "pointer"
    return ""


def entry_points(lazy_dir: Path) -> list[Path]:
    """List lazy rules that stand alone rather than belonging to a parent topic.

    :param lazy_dir: The ``_rules_lazy_load`` folder.
    :type lazy_dir: Path
    :return: Entry-point rule paths.
    :rtype: list[Path]
    """
    # A child's parent may sit under rules/, e.g. sql/formatting.md belongs to rules/04_path_scoped/.../sql.md
    roots = [lazy_dir, PATH_SCOPED_DIR] + [RULES_DIR / tier for tier in ALWAYS_ON_TIERS]
    found = []
    for path in sorted(lazy_dir.rglob("*.md")):
        rel = path.relative_to(lazy_dir)
        if path.name == "README.md" or path.name.startswith("_") or rel.parts[0] in NON_RULE_FOLDERS:
            continue
        folders = [rel.parents[i] for i in range(len(rel.parts) - 1)]
        if not any((root / f).with_suffix(".md").is_file() for f in folders for root in roots):
            found.append(path)
    return found


# --- Trigger detection ---

def test_paths_frontmatter_is_a_trigger():
    """A rule with paths: frontmatter loads when Claude reads a matching file."""
    assert trigger_for("x.md", '---\npaths:\n  - "**/*.py"\n---\n# X\n', {}, []) == "paths"


def test_hook_naming_the_rule_is_a_trigger():
    """A hook that names the rule's path loads it mechanically."""
    assert trigger_for("x.md", "# X\n", {}, ['cat "$ROOT/_rules_lazy_load/x.md"']) == "hook"


def test_pointer_in_a_loaded_file_is_a_trigger():
    """A pointer in a file Claude already has counts, whatever the config-dir prefix."""
    loaded = {"rules/a.md": "- **Read on demand:** `~/.claude/_rules_lazy_load/style_guide_standards/x.md`"}
    assert trigger_for("style_guide_standards/x.md", "# X\n", loaded, []) == "pointer"


def test_nothing_loads_an_orphan():
    """With no paths:, hook or pointer, there is no trigger."""
    assert trigger_for("x.md", "# X\n", {"rules/a.md": "unrelated"}, ["echo hi"]) == ""


def test_bare_file_name_is_not_a_pointer():
    """Naming only the file, without its _rules_lazy_load path, is too vague to follow."""
    assert trigger_for("style_guide_standards/x.md", "# X\n", {"a.md": "see x.md"}, []) == ""


def test_paths_must_be_frontmatter():
    """A paths: line in the body is text, not a trigger."""
    assert not has_paths("# X\n\npaths:\n  - '**/*.py'\n"), "body text was read as frontmatter"
    assert has_paths('---\npaths:\n  - "**/*.sql"\n---\n'), "real frontmatter was missed"


# --- Loaded files ---

def test_imports_are_followed_through_every_level(tmp_path):
    """Startup texts include files imported by imported files, but not unimported ones."""
    (tmp_path / "_rules").mkdir()
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/a.md\n")
    (tmp_path / "_rules" / "a.md").write_text("@~/.claude/_rules/b.md\n")
    (tmp_path / "_rules" / "b.md").write_text("leaf\n")
    (tmp_path / "_rules" / "c.md").write_text("never imported\n")
    texts = imported_texts(tmp_path, tmp_path / "CLAUDE.md")
    assert set(texts) == {"CLAUDE.md", "_rules/a.md", "_rules/b.md"}, sorted(texts)


def test_native_rules_without_paths_are_loaded(tmp_path):
    """Files under rules/ count as loaded at startup, except those with paths: frontmatter."""
    (tmp_path / "rules" / "04_path_scoped").mkdir(parents=True)
    (tmp_path / "rules" / "a.md").write_text("always\n")
    (tmp_path / "rules" / "04_path_scoped" / "b.md").write_text('---\npaths:\n  - "**/*.sql"\n---\n# B\n')
    assert set(native_texts(tmp_path / "rules")) == {"rules/a.md"}, sorted(native_texts(tmp_path / "rules"))


def test_skill_readmes_are_not_loaded(tmp_path):
    """Skill files count as loaded, but a README inside a skill doesn't."""
    skill = tmp_path / "group" / "demo"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("pointer\n")
    (skill / "README.md").write_text("pointer\n")
    names = [Path(p).name for p in skill_texts(tmp_path)]
    assert names == ["SKILL.md"], names


# --- Real config ---

def test_lazy_tier_has_entry_points():
    """The scan finds lazy rules and skips children of a parent topic."""
    names = [p.name for p in entry_points(LAZY_DIR)]
    assert len(names) >= 8, f"expected at least 8 lazy entry points, found {len(names)}"
    assert "formatting.md" not in names, "sql/formatting.md is a child of sql.md, not an entry point"


def test_every_lazy_rule_has_a_trigger():
    """Each lazy entry point loads through paths:, a hook or a pointer in a loaded file."""
    loaded = loaded_texts()
    hooks = [h.read_text() for h in HOOKS_DIR.glob("*.sh")]
    orphans = [
        p.relative_to(LAZY_DIR).as_posix() for p in entry_points(LAZY_DIR)
        if not trigger_for(p.relative_to(LAZY_DIR).as_posix(), p.read_text(), loaded, hooks)
    ]
    assert not orphans, (
        f"lazy rules nothing loads: {orphans} — add paths: frontmatter and move it to rules/04_path_scoped/, "
        "a 'Read on demand' pointer with the full _rules_lazy_load path in an always-on rule or skill, "
        "or move the file to _archive/"
    )


def test_triggers_added_on_2026_10_01_stay():
    """The rules that missed most often keep the trigger that fixed them."""
    loaded = loaded_texts()
    hooks = [h.read_text() for h in HOOKS_DIR.glob("*.sh")]
    expected = {
        "style_guide_standards/python.md": "paths",
        "style_guide_standards/bash.md": "paths",
        "style_guide_standards/jira.md": "pointer",
        "latency_optimisation.md": "pointer",
    }
    for inner, kind in expected.items():
        path = PATH_SCOPED_DIR / inner if (PATH_SCOPED_DIR / inner).is_file() else LAZY_DIR / inner
        found = trigger_for(inner, path.read_text(), loaded, hooks)
        assert found == kind, f"{inner} should load through {kind}, found {found or 'nothing'}"
    assert not (LAZY_DIR / "environment_setup").exists(), "ohmyzsh_setup.md was archived to _archive/ — keep it out"
