#!/usr/bin/env python3
"""Apply team-specific patches to the skill-creator plugin after installation.

Patches applied:
  1. Adds maturity tier question (question 5) to the Capture Intent phase.
  2. Updates Skill Writing Guide to generate skill.contract.yaml (contract-first design).
  3. Updates SKILL.md template to use new structure: metadata table → can/can't do → prerequisites → phases.
  4. Copies claude-tag-schema.md and prereqs_checklist.md into plugin's references/.

Idempotent: safe to re-run. Uses an HTML comment marker to detect whether
the patch has already been applied.

Must be run from the repo root after `make install_plugins`.
"""

import shutil
import sys
from pathlib import Path


PATCH_MARKER = "<!-- [TEAM-PATCH:skill-contract-first-design] -->"
PLUGIN_CACHE_ROOT = Path.home() / ".claude" / "plugins" / "cache" / "claude-plugins-official" / "skill-creator"
SCHEMA_SRC = Path(__file__).parent / "claude-tag-schema.md"
CHECKLIST_SRC = Path.home() / ".claude" / "skills" / "prereqs_checklist.md"
TEMPLATE_SRC = Path.home() / ".claude" / "_templates" / "skills" / "skill.contract.yaml.template"

# Inserted before "### Interview and Research"
MATURITY_QUESTION = """\
5. What maturity tier is this skill targeting?
   - **draft** — exploring the problem space; happy path only, no error handling, breaking changes expected
   - **tactical** — stable and dependable; main path + light error handling, no gold-plating
   - **strategic** — production-ready, generalised; full coverage, edge cases, docs, evals expected

   See `references/claude-tag-schema.md` for the full scope gate behaviour per tier.

"""

# Inserted before "### Skill Writing Guide"
SKILL_CONTRACT_INSTRUCTION = """\
### Contract-first skill design

<!-- [TEAM-PATCH:skill-contract-first-design] -->

Before writing SKILL.md, generate skill.contract.yaml — the formal contract for the skill.

**Create skill.contract.yaml** in the skill directory with this structure:

    name: <skill-identifier>
    version: 0.1.0
    summary: <one-line description of what the skill does>

    maturity: <draft|tactical|strategic>  # from your Capture Intent answer
    test_coverage_level: none

    when:
      - /<skill-name>
      - "phrase that triggers this skill"

    dont_use_for:
      - "anti-pattern 1"
      - "anti-pattern 2"

    requires:
      tools: [Bash, Read, Agent, ...]  # tools this skill uses
      mcp_servers: []                   # MCP servers (GitHub, Atlassian, etc.)
      external: []                      # external system access needed

    output: conversational              # or: file, external_service, mixed
    reversible: true                    # false if actions are permanent

See `references/prereqs_checklist.md` for field definitions and examples.

**Update SKILL.md** with the contract-first structure:

    # Skill: `<skill-name>`

    | | |
    |---|---|
    | **Description** | <one-line summary from contract> |
    | **Version** | 0.1.0 |
    | **Tested** | No |

    ## 🎯 What this skill can and can't do

    **This skill does:**
    - <capability 1>
    - <capability 2>

    **This skill doesn't do:**
    - <limitation 1>
    - <limitation 2>

    ## ✅ Prerequisites

    [List what's needed before using: tools, auth, permissions, etc.]

    ## 📋 How it works

    [Brief overview of phases; reference phase1.md, phase2.md, etc. for detail]

    ## ⚠️ Known gaps

    [List limitations and workarounds]

The SKILL.md is for end users; the contract declares what the skill needs and does.
See `references/prereqs_checklist.md` for the author checklist.

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
    content = content.replace(writing_guide_anchor, SKILL_CONTRACT_INSTRUCTION + writing_guide_anchor, 1)

    skill_md.write_text(content, encoding="utf-8")
    return True


def copy_reference_files(skill_md: Path) -> None:
    """Copy reference files into the plugin's references/ directory.

    Copies:
      - claude-tag-schema.md (tag definitions)
      - prereqs_checklist.md (skill authoring checklist)

    :param skill_md: Path to the SKILL.md (used to resolve references/).
    :type skill_md: Path
    """
    references_dir = skill_md.parent / "references"
    references_dir.mkdir(exist_ok=True)

    if SCHEMA_SRC.exists():
        shutil.copy2(SCHEMA_SRC, references_dir / "claude-tag-schema.md")
        print(f"  Copied claude-tag-schema.md → {references_dir}/")
    else:
        print(f"  WARNING: Tag schema not found at {SCHEMA_SRC}")

    if CHECKLIST_SRC.exists():
        shutil.copy2(CHECKLIST_SRC, references_dir / "prereqs_checklist.md")
        print(f"  Copied prereqs_checklist.md → {references_dir}/")
    else:
        print(f"  WARNING: Skill prerequisites checklist not found at {CHECKLIST_SRC}")
        print(f"           Ensure {CHECKLIST_SRC} exists in global config")


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

    copy_reference_files(skill_md)

    print("skill-creator-patch: done.")


if __name__ == "__main__":
    main()
