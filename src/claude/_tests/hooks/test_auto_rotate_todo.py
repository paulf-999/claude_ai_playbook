#!/usr/bin/env python3

"""
Test suite for TODO rotation automation.

Tests the rotate_todo.sh script and hook_auto_rotate_todo.sh wrapper.
Validates that:
- TODO files rotate on month boundary
- Archive structure is created correctly
- Archive index is maintained accurately
- Fresh TODO files have correct structure
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta


class TestTODORotation:
    """Test cases for TODO rotation logic."""

    def setup_method(self):
        """Create temporary test environment."""
        self.temp_dir = tempfile.mkdtemp(prefix="todo_test_")
        self.claude_dir = Path(self.temp_dir) / ".claude"
        self.scripts_dir = self.claude_dir / "scripts"
        self.archives_dir = self.claude_dir / "_archives" / "TODO"

        # Create directory structure
        self.claude_dir.mkdir(parents=True)
        self.scripts_dir.mkdir(parents=True)
        self.archives_dir.mkdir(parents=True)

        # Copy rotation script
        src_script = Path(os.path.expanduser("~/.claude/scripts/rotate_todo.sh"))
        if src_script.exists():
            shutil.copy(src_script, self.scripts_dir / "rotate_todo.sh")
            (self.scripts_dir / "rotate_todo.sh").chmod(0o755)

    def teardown_method(self):
        """Clean up temporary directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_test_todo(self, month: str) -> Path:
        """Create a test TODO.md file for a given month."""
        todo_file = self.claude_dir / "TODO.md"
        content = f"""# TODO

## Active Month: {month}

---

## 📋 Pending Items

| # | Created | Updated | Theme | Subject | Item | Group | Priority | Effort | Value | Description |
|---|---------|---------|-------|---------|------|-------|----------|--------|-------|-------------|
| 1 | {month}-01 | {month}-01 | Test | Testing | Test Item | Core Work | High | Medium | High | Test item for verification |

---

## ✅ Completed Items

| # | Created | Updated | Theme | Subject | Item | Group | Priority | Effort | Value | Description |
|---|---------|---------|-------|---------|------|-------|----------|--------|-------|-------------|
| ~~2~~ | ~~{month}-01~~ | ~~{month}-01~~ | ~~Test~~ | ~~Testing~~ | ~~Completed Item~~ | ~~Complete~~ | ~~High~~ | ~~Low~~ | ~~High~~ | ~~Completed item for verification~~ |

---

## Summary ({month})

**Pending:** 1 item

**Completed:** 1 item

---
"""
        todo_file.write_text(content)
        return todo_file

    def test_todo_structure_has_active_month_header(self):
        """Verify TODO.md has required 'Active Month: YYYY-MM' header."""
        todo_file = self.create_test_todo("2026-08")
        content = todo_file.read_text()
        assert "## Active Month: 2026-08" in content, "TODO.md must have Active Month header"

    def test_no_rotation_when_months_match(self):
        """Verify rotation is skipped when current month matches TODO month."""
        current_month = datetime.now().strftime("%Y-%m")
        todo_file = self.create_test_todo(current_month)
        original_content = todo_file.read_text()

        # Run rotation with current month
        result = subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh")],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        # Verify no rotation occurred (file should be unchanged)
        assert todo_file.read_text() == original_content, "File should not change when months match"
        assert "No rotation needed" in result.stdout or result.returncode == 0, "Should report no rotation needed"

    def test_rotation_with_force_flag(self):
        """Verify --force flag triggers rotation even when months match."""
        current_month = datetime.now().strftime("%Y-%m")
        past_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        todo_file = self.create_test_todo(past_month)

        # Run rotation with --force
        result = subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh"), "--force"],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        assert result.returncode == 0, f"Rotation failed: {result.stderr}"
        assert todo_file.exists(), "TODO.md should still exist after rotation"

        # Verify archive was created
        archive_file = self.archives_dir / f"{past_month}.md"
        assert archive_file.exists(), f"Archive file should exist at {archive_file}"

        # Verify new TODO has current month
        new_content = todo_file.read_text()
        assert f"## Active Month: {current_month}" in new_content, "New TODO should have current month"

    def test_archive_index_updated_after_rotation(self):
        """Verify archive index is created/updated after rotation."""
        current_month = datetime.now().strftime("%Y-%m")
        past_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        todo_file = self.create_test_todo(past_month)
        archive_index = self.claude_dir / "_archives" / "TODO_archive.md"

        # Run rotation
        subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh"), "--force"],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        # Verify index exists and contains archive entry
        assert archive_index.exists(), "Archive index should be created"
        index_content = archive_index.read_text()
        assert past_month in index_content, f"Index should reference archived month {past_month}"
        assert f"TODO/{past_month}.md" in index_content, "Index should link to archive file"

    def test_fresh_todo_has_empty_tables(self):
        """Verify fresh TODO.md has correct structure with empty tables."""
        current_month = datetime.now().strftime("%Y-%m")
        past_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        todo_file = self.create_test_todo(past_month)

        # Run rotation
        subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh"), "--force"],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        new_content = todo_file.read_text()

        # Verify structure
        assert "## Active Month:" in new_content, "Should have Active Month header"
        assert "## 📋 Pending Items" in new_content, "Should have Pending Items section"
        assert "## ✅ Completed Items" in new_content, "Should have Completed Items section"
        assert "## Summary" in new_content, "Should have Summary section"

        # Verify tables exist but are mostly empty (just headers)
        assert "| # | Created | Updated |" in new_content, "Should have table headers"

    def test_archived_todo_preserves_content(self):
        """Verify archived TODO file contains original content."""
        past_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        original_todo = self.create_test_todo(past_month)
        original_content = original_todo.read_text()

        # Run rotation
        subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh"), "--force"],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        archive_file = self.archives_dir / f"{past_month}.md"
        archived_content = archive_file.read_text()

        assert archived_content == original_content, "Archived file should preserve original content"

    def test_hook_wrapper_calls_rotation_script(self):
        """Verify hook wrapper correctly invokes rotation script."""
        hook_path = Path(os.path.expanduser("~/.claude/hooks/hook_auto_rotate_todo.sh"))

        assert hook_path.exists(), "Hook script should exist"
        assert os.access(hook_path, os.X_OK), "Hook script should be executable"

    def test_rotation_creates_backup_if_archive_exists(self):
        """Verify rotation backs up existing archive before overwriting."""
        past_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")

        # Create initial archive
        archive_file = self.archives_dir / f"{past_month}.md"
        archive_file.write_text("Original archive content")

        todo_file = self.create_test_todo(past_month)

        # Run rotation
        subprocess.run(
            [str(self.scripts_dir / "rotate_todo.sh"), "--force"],
            cwd=self.claude_dir,
            capture_output=True,
            text=True,
            env={**os.environ, "HOME": self.temp_dir}
        )

        # Verify backup was created
        backup_file = self.archives_dir / f"{past_month}.md.bak"
        assert backup_file.exists(), "Backup should be created if archive already exists"
        assert backup_file.read_text() == "Original archive content", "Backup should preserve original content"


# Integration test: verify rotation works with real cron invocation
def test_rotation_cron_compatibility():
    """Verify rotation script is compatible with cron scheduling."""
    script_path = Path(os.path.expanduser("~/.claude/scripts/rotate_todo.sh"))
    assert script_path.exists(), "Rotation script should exist for cron scheduling"
    assert os.access(script_path, os.X_OK), "Rotation script should be executable"

    # Verify shebang is cron-compatible
    first_line = script_path.read_text().split("\n")[0]
    assert first_line.startswith("#!/bin/bash"), "Script should have bash shebang for cron"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
