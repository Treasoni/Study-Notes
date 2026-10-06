#!/usr/bin/env python3
"""Bounded digest of a Markdown note: size, frontmatter, heading tree, per-section excerpts.

Read this instead of whole-file Reads of large notes (> ~15 KB); then target-read only the
sections you need (Read offset/limit, or Grep for anchors).
See `.codex/rules/common/context-discipline.md`. Stdlib only.

Usage:
  python .codex/scripts/note-digest.py <file.md> [--max-chars 400] [--max-sections 60] [--headings-only]

Exit codes: 0 = ok, 1 = file not found, 2 = error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def split_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    """Return (frontmatter lines, body start index)."""
    if not lines or lines[0].strip() != "---":
        return [], 0
    index = 1
    fm: list[str] = []
    while index < len(lines) and lines[index].strip() != "---":
        fm.append(lines[index])
        index += 1
    return fm, min(index + 1, len(lines))


def excerpt(text: str, max_chars: int) -> str:
    for para in re.split(r"\n\s*\n", text):
        cleaned = " ".join(line.strip() for line in para.splitlines() if line.strip())
        if cleaned:
            return cleaned[:max_chars] + ("…" if len(cleaned) > max_chars else "")
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--max-chars", type=int, default=400, help="Excerpt length per section (default 400).")
    parser.add_argument("--max-sections", type=int, default=60, help="Max sections listed (default 60).")
    parser.add_argument("--headings-only", action="store_true", help="Skip excerpts.")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    lines = text.splitlines()
    fm, body_start = split_frontmatter(lines)
    headings = []
    for idx in range(body_start, len(lines)):
        match = HEADING_RE.match(lines[idx])
        if match:
            headings.append((len(match.group(1)), match.group(2), idx))

    size = len(text.encode("utf-8"))
    print(f"note: {path.name}")
    print(f"size: {size} bytes, {len(lines)} lines, {len(headings)} sections")
    if fm:
        items = [line.strip() for line in fm if line.strip()]
        joined = "; ".join(items)
        print(f"frontmatter: {joined[:500]}{'…' if len(joined) > 500 else ''}")
    print("---")

    shown = headings[: args.max_sections]
    for level, title, idx in shown:
        start = idx + 1
        end = len(lines)
        for next_level, _t, next_idx in headings:
            if next_idx > idx and next_level <= level:
                end = next_idx
                break
        section = "\n".join(lines[start:end]).strip()
        sec_size = len(section.encode("utf-8"))
        indent = "  " * (level - 1)
        print(f"{indent}[H{level}] {title} ({sec_size} bytes)")
        if not args.headings_only:
            text_excerpt = excerpt(section, args.max_chars)
            if text_excerpt:
                print(f"{indent}  {text_excerpt}")

    if len(headings) > len(shown):
        print(f"... {len(headings) - len(shown)} more sections omitted (use --max-sections)")
    print(f"hint: read only what you need — Read with offset/limit, or Grep for anchors; total size above tells you if a full read is worth it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
