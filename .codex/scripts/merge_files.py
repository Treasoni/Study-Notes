#!/usr/bin/env python3
"""Merge many Markdown files into one, separated by HTML comments.

Replaces N sequential Reads with a single Read: see `.codex/rules/common/context-discipline.md`.
Stdlib only; deterministic (files sorted by name).

Usage:
  python .codex/scripts/merge_files.py --input-dir workspace/<topic>/chapters
  python .codex/scripts/merge_files.py --input-dir <dir> --output -     # print to stdout

Behavior:
  - Input files: <input-dir>/<pattern> (default *.md), sorted by name.
  - Skips: the output file itself, empty files, and files whose YAML frontmatter
    contains `status: failed` (unless --keep-failed).
  - Output: <input-dir>/_merged.md (or --output PATH / '-' for stdout), UTF-8, LF.

Exit codes: 0 = merged at least one file, 1 = nothing merged, 2 = usage or IO error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FAILED_RE = re.compile(r'^\s*status:\s*["\']?failed["\']?\s*$', re.IGNORECASE | re.MULTILINE)


def frontmatter(text: str) -> str:
    """Return the YAML frontmatter block (without the --- fences), or ''."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[:end] if end != -1 else ""


def is_failed(text: str) -> bool:
    fm = frontmatter(text)
    return bool(fm) and bool(FAILED_RE.search(fm))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, help="Directory holding the files to merge.")
    parser.add_argument("--pattern", default="*.md", help="Glob pattern inside --input-dir (default: *.md).")
    parser.add_argument("--output", default=None, help="Output path; '-' prints to stdout (default: <input-dir>/_merged.md).")
    parser.add_argument("--sep", choices=["html-comment", "none"], default="html-comment", help="Separator style (default: html-comment).")
    parser.add_argument("--keep-failed", action="store_true", help="Do not skip files whose frontmatter has status: failed.")
    args = parser.parse_args()

    in_dir = Path(args.input_dir).expanduser()
    if not in_dir.is_dir():
        print(f"error: not a directory: {in_dir}", file=sys.stderr)
        return 2

    if args.output == "-":
        out_path = None
    elif args.output:
        out_path = Path(args.output).expanduser()
    else:
        out_path = in_dir / "_merged.md"

    files = sorted(p for p in in_dir.glob(args.pattern) if p.is_file())
    parts: list[str] = []
    included: list[str] = []
    skipped = {"empty": 0, "failed": 0}
    for path in files:
        if out_path is not None and path.resolve() == out_path.resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            skipped["empty"] += 1
            continue
        if not args.keep_failed and is_failed(text):
            skipped["failed"] += 1
            continue
        body = text.rstrip("\n") + "\n"
        if args.sep == "html-comment":
            size = len(text.encode("utf-8"))
            parts.append(f"<!-- SOURCE: {path.name} | {size} bytes -->\n{body}<!-- END: {path.name} -->\n")
        else:
            parts.append(body)
        included.append(path.name)

    if not parts:
        print(
            f"error: nothing to merge in {in_dir} (pattern={args.pattern}, "
            f"skipped empty={skipped['empty']}, failed={skipped['failed']})",
            file=sys.stderr,
        )
        return 1

    merged = "\n".join(parts)
    size = len(merged.encode("utf-8"))
    shown = ", ".join(included[:12]) + (f" (+{len(included) - 12} more)" if len(included) > 12 else "")
    if out_path is None:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.write(merged)
        print(
            f"merged {len(parts)} file(s) to stdout ({size} bytes); skipped empty={skipped['empty']}, failed={skipped['failed']}; {shown}",
            file=sys.stderr,
        )
    else:
        out_path.write_text(merged, encoding="utf-8", newline="")
        print(
            f"merged {len(parts)} file(s) -> {out_path} ({size} bytes); "
            f"skipped empty={skipped['empty']}, failed={skipped['failed']}"
        )
        print(f"included: {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
