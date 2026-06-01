"""Tests for merge_sources.py"""

import os
import tempfile
import shutil

import pytest

from merge_sources import read_frontmatter, merge_files


@pytest.fixture
def tmp_dir():
    """Create a temporary directory for test files."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def _write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def test_read_frontmatter_basic():
    content = """---
source_url: https://example.com
status: success
---

Body content here."""
    fm = read_frontmatter(content)
    assert fm["source_url"] == "https://example.com"
    assert fm["status"] == "success"


def test_read_frontmatter_missing():
    fm = read_frontmatter("No frontmatter here.")
    assert fm == {}


def test_read_frontmatter_partial():
    content = """---
source_url: https://example.com
---

Body."""
    fm = read_frontmatter(content)
    assert fm["source_url"] == "https://example.com"
    assert "status" not in fm


def test_merge_multiple_files(tmp_dir):
    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nsource_url: https://a.com\nstatus: success\n---\n\n# Page 1\n\nContent 1",
    )
    _write_file(
        os.path.join(tmp_dir, "doc-02.md"),
        "---\nsource_url: https://b.com\nstatus: success\n---\n\n# Page 2\n\nContent 2",
    )

    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")

    assert stats["total_files"] == 2
    assert stats["merged"] == 2
    assert stats["skipped_empty"] == 0
    assert stats["skipped_failed"] == 0
    assert os.path.exists(output_file)

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "<!-- SOURCE: doc-01.md | url: https://a.com -->" in content
    assert "<!-- END: doc-01.md -->" in content
    assert "<!-- SOURCE: doc-02.md | url: https://b.com -->" in content
    assert "<!-- END: doc-02.md -->" in content
    assert "# Page 1" in content
    assert "# Page 2" in content


def test_skip_empty_files(tmp_dir):
    _write_file(os.path.join(tmp_dir, "doc-01.md"), "")
    _write_file(
        os.path.join(tmp_dir, "doc-02.md"),
        "---\nsource_url: https://b.com\nstatus: success\n---\n\nContent",
    )

    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")

    assert stats["total_files"] == 2
    assert stats["merged"] == 1
    assert stats["skipped_empty"] == 1

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "doc-02.md" in content
    assert "doc-01.md" not in content


def test_skip_failed_files(tmp_dir):
    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nsource_url: https://a.com\nstatus: failed\n---\n\nError content",
    )
    _write_file(
        os.path.join(tmp_dir, "doc-02.md"),
        "---\nsource_url: https://b.com\nstatus: success\n---\n\nContent",
    )

    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")

    assert stats["merged"] == 1
    assert stats["skipped_failed"] == 1

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "doc-02.md" in content
    assert "doc-01.md" not in content


def test_nonexistent_directory():
    stats = merge_files("/nonexistent/path", "output.md", "html-comment")
    assert stats["total_files"] == 0
    assert stats["merged"] == 0


def test_empty_directory(tmp_dir):
    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")
    assert stats["merged"] == 0


def test_only_whitespace_files_skipped(tmp_dir):
    _write_file(os.path.join(tmp_dir, "doc-01.md"), "   \n\n  \n  ")
    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")
    assert stats["merged"] == 0
    assert stats["skipped_empty"] == 1


def test_frontmatter_preserved_in_output(tmp_dir):
    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nsource_url: https://example.com\nstatus: success\ntitle: Test\n---\n\nBody.",
    )
    output_file = os.path.join(tmp_dir, "merged.md")
    merge_files(tmp_dir, output_file, "html-comment")

    with open(output_file, encoding="utf-8") as f:
        content = f.read()

    assert "source_url: https://example.com" in content
    assert "title: Test" in content


def test_output_file_created(tmp_dir):
    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nstatus: success\n---\n\nContent.",
    )
    output_file = os.path.join(tmp_dir, "out.md")
    merge_files(tmp_dir, output_file, "html-comment")
    assert os.path.exists(output_file)


def test_non_md_files_ignored(tmp_dir):
    _write_file(os.path.join(tmp_dir, "notes.txt"), "some text")
    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nstatus: success\n---\n\nContent.",
    )
    output_file = os.path.join(tmp_dir, "merged.md")
    stats = merge_files(tmp_dir, output_file, "html-comment")
    assert stats["merged"] == 1


def test_exit_code_success(tmp_dir):
    """Integration test: calling main() via subprocess for exit code check."""
    import subprocess
    import sys

    _write_file(
        os.path.join(tmp_dir, "doc-01.md"),
        "---\nsource_url: https://a.com\nstatus: success\n---\n\nContent",
    )
    output_file = os.path.join(tmp_dir, "merged.md")
    result = subprocess.run(
        [sys.executable, "merge_sources.py", "--input-dir", tmp_dir, "--output", output_file],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )
    assert result.returncode == 0


def test_exit_code_no_valid_files(tmp_dir):
    """Integration test: exit code 1 when no valid files."""
    import subprocess
    import sys

    output_file = os.path.join(tmp_dir, "merged.md")
    result = subprocess.run(
        [sys.executable, "merge_sources.py", "--input-dir", tmp_dir, "--output", output_file],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )
    assert result.returncode == 1


def test_exit_code_nonexistent_dir():
    """Integration test: exit code 1 for nonexistent dir."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "merge_sources.py", "--input-dir", "/nonexistent", "--output", "out.md"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )
    assert result.returncode == 1
