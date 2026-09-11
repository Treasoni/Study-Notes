#!/usr/bin/env python3
"""Retired: the legacy `.codex/skills` migration is complete.

`.agents/skills` is the canonical skill root (see `.codex/platform/registry.yaml`,
`discovery.Skill`).  The `.codex/skills` tree this script used to migrate has been
removed, so there is nothing left to migrate and the old copy-into-canonical
behaviour can no longer run.

The entry point is kept as a tombstone rather than deleted, because a retired
script that silently does nothing is worse than one that explains itself.  It now
doubles as a guard: if `.codex/skills` ever reappears, it fails loudly, because a
second skill tree at that path is drift, not a migration.

Known way it can reappear: the Claudian Obsidian plugin's "Add Codex Skill" modal
defaults its Directory field to `.codex/skills` (`main.js`: `targetRootId =
input.rootId ?? "vault-codex"`) and never creates the folder itself.  Adding a
skill through that UI without switching Directory to `.agents/skills` recreates
the retired tree.
"""

from __future__ import annotations

import argparse
from pathlib import Path

CANONICAL_ROOT = ".agents/skills"
RETIRED_ROOT = ".codex/skills"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not (root / CANONICAL_ROOT).is_dir():
        raise SystemExit(f"migrate-legacy-skills: canonical skill root is missing: {CANONICAL_ROOT}")

    if (root / RETIRED_ROOT).is_dir():
        raise SystemExit(
            "migrate-legacy-skills: the retired root reappeared: "
            + RETIRED_ROOT
            + "\n"
            "The migration is already complete and that path is not canonical; a second skill\n"
            "tree there is drift. Move its contents into "
            + CANONICAL_ROOT
            + " and remove the directory.\n"
            "If the Claudian plugin created it, re-add the skill with the modal's Directory\n"
            "field set to " + CANONICAL_ROOT + " instead."
        )

    print(
        "migrate-legacy-skills: nothing to do; migration complete, canonical root is "
        + CANONICAL_ROOT
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
