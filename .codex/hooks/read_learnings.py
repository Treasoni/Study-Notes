#!/usr/bin/env python3
"""Print .learnings context for agent session-start hooks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def default_project_root() -> Path:
    # Expected install shape: <project>/<agent-dir>/hooks/read_learnings.py
    return Path(__file__).resolve().parents[2]


def force_utf8_streams() -> None:
    """Emit .learnings text as UTF-8 regardless of the inherited console code page.

    The host reads hook output as UTF-8, but on Windows sys.stdout defaults to the
    ANSI code page (e.g. GBK) while the learnings files are Chinese: printing them
    raises UnicodeEncodeError, the hook exits non-zero, and the reminder silently
    never reaches the agent. errors="replace" keeps a reminder hook from ever
    failing the session over one unencodable character.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def tail_lines(text: str, count: int) -> str:
    lines = text.splitlines()
    return "\n".join(lines[-count:])


def tail_entries(text: str, count: int) -> str:
    """Return the last `count` complete `## [ID] ...` entries from a learnings file."""
    if count <= 0:
        return ""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("## [")]
    if not starts:
        return ""
    body = lines[starts[-count]:]
    while body and body[-1].strip() in ("", "---"):
        body.pop()
    return "\n".join(body)


def print_section(title: str, body: str) -> None:
    if not body:
        return
    print(f"## {title}")
    print("")
    print(body.rstrip())
    print("")
    print("---")
    print("")


def main() -> int:
    force_utf8_streams()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=None, help="Project root. Defaults to two directories above this hook.")
    parser.add_argument("--tail-lines", type=int, default=30, help="Number of recent LEARNINGS.md lines to include.")
    parser.add_argument("--error-entries", type=int, default=2, help="Number of recent ERRORS.md entries to include.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve() if args.project_root else default_project_root()
    learnings_dir = project_root / ".learnings"

    print("<system-reminder>")
    print("# Learnings Reminder")
    print("")

    print_section("Rules (highest priority)", read_text(learnings_dir / "RULES.md"))

    errors = read_text(learnings_dir / "ERRORS.md")
    if errors:
        error_entries = tail_entries(errors, args.error_entries)
        if not error_entries:
            error_entries = tail_lines(errors, 12)
        print_section("Error Log (avoid repeating)", error_entries)
        if len([l for l in errors.splitlines() if l.startswith("## [")]) > args.error_entries:
            print("> 更早的错误记录见 `.learnings/ERRORS.md`（按需读取，避免重复预载）。")
            print("")
        print("---")
        print("")

    learnings = read_text(learnings_dir / "LEARNINGS.md")
    if learnings:
        print("## Recent Learnings")
        print("")
        print(tail_lines(learnings, args.tail_lines).rstrip())
        print("")

    print("")
    print("Before doing task work, apply the rules and avoid repeating recorded errors.")
    print("</system-reminder>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
