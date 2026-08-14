#!/usr/bin/env python3
"""Promote retained legacy Study System skills into the canonical Codex root.

The Agent Template Kits profile treats `.agents/skills` as the canonical skill
directory.  This migration preserves project-specific skills that predate that
layout and restores manifests for shared skills without replacing a newer
template-kit implementation.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


LEGACY_PROJECT_SKILLS = (
    "batch-note-updater",
    "legacy-note-importer",
    "moc-organizer",
    "note-beautifier",
    "note-starter",
    "note-updater",
    "research-planner",
    "security-secret-audit",
    "skill-creator",
    "tool-discovery",
    "workflow-orchestrator",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--apply", action="store_true", help="copy planned files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    legacy_root = root / ".codex" / "skills"
    canonical_root = root / ".agents" / "skills"
    if not legacy_root.is_dir() or not canonical_root.is_dir():
        raise SystemExit("migrate-legacy-skills: expected both .codex/skills and .agents/skills")

    plans: list[tuple[str, Path, Path]] = []
    for name in LEGACY_PROJECT_SKILLS:
        source, target = legacy_root / name, canonical_root / name
        if source.is_dir() and not target.exists():
            plans.append(("skill", source, target))

    for target in sorted(canonical_root.iterdir()):
        if not target.is_dir() or (target / "manifest.yaml").exists():
            continue
        source_manifest = legacy_root / target.name / "manifest.yaml"
        if source_manifest.is_file():
            plans.append(("manifest", source_manifest, target / "manifest.yaml"))

    for kind, source, target in plans:
        print(f"[PLAN] {kind}: {source.relative_to(root)} -> {target.relative_to(root)}")
    if not args.apply:
        print(f"[DRY RUN] {len(plans)} migration action(s); add --apply to write.")
        return 0

    for kind, source, target in plans:
        if kind == "skill":
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    print(f"[OK] applied {len(plans)} migration action(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
