#!/usr/bin/env python3
"""Apply team-specific patches to the skill-creator plugin after installation.

Patches applied:
  1. Adds maturity tier question (question 5) to the Capture Intent phase.
  2. Adds Tier 1 tag stamping and scope gate injection instructions before
     the Skill Writing Guide section.
  3. Copies claude-tag-schema.md into the plugin's references/ directory.

Idempotent: safe to re-run. Uses an HTML comment marker to detect whether
the patch has already been applied.

Must be run from the repo root after `make install_plugins`.
"""

import shutil
import sys
from pathlib import Path


PATCH_MARKER = "<!-- [TEAM-PATCH:maturity-tags-scope-gate] -->"
PLUGIN_CACHE_ROOT = Path.home() / ".claude" / "plugins" / "cache" / "claude-plugins-official" / "skill-creator"
SCHEMA_SRC = Path(__file__).parent / "claude-tag-schema.md"

# Inserted before "### Interview and Research"
MATURITY_QUESTION = """\
5. What maturity tier is this skill targeting?
   - **draft** — exploring the problem space; happy path only, no error handling, breaking changes expected
   - **tactical** — stable and dependable; main path + light error handling, no gold-plating
   - **strategic** — production-ready, generalised; full coverage, edge cases, docs, evals expected

   See `references/claude-tag-schema.md` for the full scope gate behaviour per tier.

"""

# Inserted before "### Skill Writing Guide"
TIER1_TAGS_INSTRUCTION = """\
### Tier 1 tags and scope gate

<!-- [TEAM-PATCH:maturity-tags-scope-gate] -->

Every generated SKILL.md must include the following additions based on what you collected
in Capture Intent (question 5).

**Frontmatter** — after `name`, `description`, and `version`, stamp these Tier 1 tags:

    maturity: <draft|tactical|strategic>   # from question 5
    tags:
      criticality: <must|should|could|want>
      status: wip
      tested: false

**Skill body** — add a `## Scope gate` section immediately after the YAML frontmatter,
before the first heading in the skill content:

    ## Scope gate

    This skill is at **<maturity>** maturity. Claude behaviour is constrained accordingly:

    | Maturity | Allowed |
    |---|---|
    | draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
    | tactical | Main path + light error handling. No gold-plating. |
    | strategic | Full coverage, edge cases, documentation, evals expected. |

Full tag schema: `references/claude-tag-schema.md`

"""


def find_skill_md() -> Path:
    """Locate the skill-creator SKILL.md in the plugin cache.

    :raises FileNotFoundError: If the plugin has not been installed or the
        path structure has changed.
    :return: Path to the SKILL.md file.
    :rtype: Path
    """
    if not PLUGIN_CACHE_ROOT.exists():
        raise FileNotFoundError(
            f"skill-creator plugin not found at {PLUGIN_CACHE_ROOT}. "
            "Run `make install_plugins` before `make patch_plugins`."
        )

    matches = list(PLUGIN_CACHE_ROOT.glob("*/skills/skill-creator/SKILL.md"))
    if not matches:
        raise FileNotFoundError(
            f"No SKILL.md found under {PLUGIN_CACHE_ROOT}. "
            "The plugin structure may have changed — update this script."
        )

    # If multiple versions exist, take the most recently modified.
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0]


def patch_skill_md(skill_md: Path) -> bool:
    """Apply text insertions to SKILL.md if not already patched.

    :param skill_md: Path to the SKILL.md to patch.
    :type skill_md: Path
    :return: True if patches were applied; False if already patched.
    :rtype: bool
    """
    content = skill_md.read_text(encoding="utf-8")

    if PATCH_MARKER in content:
        print("  SKILL.md already patched — skipping.")
        return False

    interview_anchor = "### Interview and Research"
    writing_guide_anchor = "### Skill Writing Guide"

    for anchor in (interview_anchor, writing_guide_anchor):
        if anchor not in content:
            raise RuntimeError(
                f"Expected anchor not found in SKILL.md: '{anchor}'. "
                "The plugin may have been updated — review and update this script."
            )

    content = content.replace(interview_anchor, MATURITY_QUESTION + interview_anchor, 1)
    content = content.replace(writing_guide_anchor, TIER1_TAGS_INSTRUCTION + writing_guide_anchor, 1)

    skill_md.write_text(content, encoding="utf-8")
    return True


def copy_tag_schema(skill_md: Path) -> None:
    """Copy claude-tag-schema.md into the plugin's references/ directory.

    :param skill_md: Path to the SKILL.md (used to resolve references/).
    :type skill_md: Path
    """
    if not SCHEMA_SRC.exists():
        raise FileNotFoundError(
            f"Tag schema source not found: {SCHEMA_SRC}. "
            "Ensure the repo is up to date and `make install` has been run."
        )
    references_dir = skill_md.parent / "references"
    references_dir.mkdir(exist_ok=True)
    shutil.copy2(SCHEMA_SRC, references_dir / "claude-tag-schema.md")
    print(f"  Copied claude-tag-schema.md → {references_dir}/")


def main() -> None:
    """Entry point."""
    print("skill-creator-patch: applying team patches...")

    try:
        skill_md = find_skill_md()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"  Found SKILL.md: {skill_md}")

    try:
        applied = patch_skill_md(skill_md)
        if applied:
            print("  SKILL.md patched.")
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        copy_tag_schema(skill_md)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print("skill-creator-patch: done.")


if __name__ == "__main__":
    main()
