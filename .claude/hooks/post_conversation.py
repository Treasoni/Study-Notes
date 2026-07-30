#!/usr/bin/env python3
"""Report project changes after a Codex conversation and optionally commit them."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = Path(gettempdir()) / "study-system-post-conversation.log"
SECRET_AUDIT = PROJECT_ROOT / ".claude/skills/security-secret-audit/scripts/audit-secrets.sh"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def log(message: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(line)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        pass


def audit(*args: str) -> bool:
    result = run(str(SECRET_AUDIT), *args)
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    return result.returncode == 0


def main() -> int:
    if run("git", "rev-parse", "--is-inside-work-tree").returncode != 0:
        return 0

    changed = run("git", "status", "--short")
    changed_files = changed.stdout.rstrip()
    if not changed_files:
        log("Study System: no project changes.")
        return 0

    log("Study System: project changes detected:")
    print(changed_files)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(changed_files + "\n")
    except OSError:
        pass

    if os.environ.get("CODEX_AUTO_GIT") != "1":
        log("Auto commit disabled because CODEX_AUTO_GIT is not 1.")
        return 0

    if not audit():
        log("Automatic commit blocked by working-tree secret audit.")
        return 1

    log("Running git add -A.")
    if run("git", "add", "-A").returncode != 0:
        log("Automatic commit blocked because git add failed.")
        return 1

    if run("git", "diff", "--cached", "--quiet").returncode == 0:
        log("No staged changes after git add.")
        return 0

    if not audit("--staged"):
        log("Automatic commit blocked by staged secret audit.")
        return 1

    log("Creating automatic commit.")
    commit = run("git", "commit", "-m", "chore: automated project change")
    if commit.returncode != 0:
        if commit.stdout:
            print(commit.stdout, file=sys.stderr, end="" if commit.stdout.endswith("\n") else "\n")
        log("Automatic commit failed.")
        return 1
    log("Automatic commit complete. Push manually after review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
