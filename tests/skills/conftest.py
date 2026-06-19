"""Shared fixtures for skill behavioural tests."""
from pathlib import Path

import pytest

_SKILLS_ROOT = Path(__file__).parent.parent.parent / "src" / "claude" / "skills"
_SKILL_MD_PATHS = sorted(_SKILLS_ROOT.rglob("SKILL.md"))


@pytest.fixture(
    params=_SKILL_MD_PATHS,
    ids=[f"{p.parent.parent.name}/{p.parent.name}" for p in _SKILL_MD_PATHS],
)
def skill_md_path(request: pytest.FixtureRequest) -> Path:
    """Parametrised fixture providing each SKILL.md path for frontmatter validation."""
    return request.param  # type: ignore[no-any-return]
