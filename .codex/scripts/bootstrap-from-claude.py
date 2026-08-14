#!/usr/bin/env python3
"""Seed the canonical Codex configuration from an existing Claude mirror.

This is a one-time migration helper.  It copies only the directories managed by
``sync-codex-to-claude.py`` and rewrites runtime-specific references in text
files.  It refuses to overwrite an existing destination unless ``--force`` is
given, and never mutates the source Claude configuration.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


MANAGED_DIRECTORIES = ("skills", "agents", "rules", "scripts", "platform", "workflows", "hooks")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".json"}
IGNORED_NAMES = {".DS_Store"}


def transform_text(path: Path) -> None:
    if path.suffix not in TEXT_SUFFIXES:
        return
    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    target = source.replace(".claude", ".codex").replace("Claude Code", "Codex")
    if target != source:
        path.write_text(target, encoding="utf-8")


def assert_safe_tree(root: Path, shared_skills_root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_symlink():
            continue
        resolved = path.resolve(strict=True)
        if path.parent == root / "skills" and resolved.is_relative_to(shared_skills_root):
            continue
        raise ValueError(f"refusing symlinked migration input: {path}")


def copy_tree(source: Path, destination: Path, force: bool) -> list[Path]:
    copied: list[Path] = []
    if not source.is_dir():
        return copied
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part in IGNORED_NAMES for part in relative.parts):
            continue
        if path.is_symlink():
            continue
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists() and not force:
            raise FileExistsError(f"destination already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        transform_text(target)
        copied.append(target)
    return copied


def copy_linked_shared_skills(source_root: Path, destination_root: Path, shared_skills_root: Path, force: bool) -> list[Path]:
    copied: list[Path] = []
    skills = source_root / "skills"
    if not skills.is_dir():
        return copied
    for link in sorted(skills.iterdir()):
        if not link.is_symlink():
            continue
        resolved = link.resolve(strict=True)
        if not resolved.is_dir() or not resolved.is_relative_to(shared_skills_root):
            raise ValueError(f"refusing non-shared skill link: {link}")
        copied.extend(copy_tree(resolved, destination_root / "skills" / link.name, force))
    return copied


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--check", action="store_true", help="report planned copies without writing")
    parser.add_argument("--force", action="store_true", help="replace existing Codex mirror files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    source_root = root / ".claude"
    destination_root = root / ".codex"
    shared_skills_root = root / ".agents" / "skills"
    if not source_root.is_dir():
        print(f"bootstrap-from-claude: missing source directory: {source_root}", file=sys.stderr)
        return 2
    try:
        assert_safe_tree(source_root, shared_skills_root)
    except ValueError as error:
        print(f"bootstrap-from-claude: {error}", file=sys.stderr)
        return 2

    planned = [source_root / directory for directory in MANAGED_DIRECTORIES if (source_root / directory).is_dir()]
    if args.check:
        print("Would seed .codex from:")
        for directory in planned:
            print(f"  - {directory.relative_to(root)}")
        return 0

    try:
        copied: list[Path] = []
        for directory in MANAGED_DIRECTORIES:
            copied.extend(copy_tree(source_root / directory, destination_root / directory, args.force))
        copied.extend(copy_linked_shared_skills(source_root, destination_root, shared_skills_root, args.force))
    except (FileExistsError, OSError) as error:
        print(f"bootstrap-from-claude: {error}", file=sys.stderr)
        return 2
    print(f"Seeded {len(copied)} files into {destination_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
