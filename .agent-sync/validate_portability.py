#!/usr/bin/env python3
"""Reject platform-bound shared agent assets before synchronization."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


AGENT_DIRECTORIES = (".agents", ".codex", ".claude", ".codebuddy", ".agent-sync")
# Generated from portable templates by .agent-sync/bootstrap.py, but committed to
# the repository -- so they get inspected like any other shared asset. They were
# previously skipped outright, which is exactly how a host-absolute interpreter
# path reached a Windows checkout unnoticed.
GENERATED_HOOK_CONFIGS = {
    Path(".codex/hooks.json"),
    Path(".claude/settings.json"),
    Path(".codebuddy/settings.json"),
}
LOCAL_ONLY_FILES = {
    Path(".claude/settings.local.json"),
}
SCANNER_IMPLEMENTATIONS = {
    Path(directory_name) / "skills/multi-agent-sync/scripts/validate_portability.py"
    for directory_name in AGENT_DIRECTORIES
}
SCANNER_IMPLEMENTATIONS.add(Path(".agent-sync/validate_portability.py"))
PLATFORMS = ("windows", "macos", "linux")
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".sh", ".txt"}
ABSOLUTE_PATH = re.compile(r"/Users/|/home/|(?<![A-Za-z0-9_])[A-Za-z]:[\\/]")
SHELL_SHEBANG = re.compile(r"^#!.*\b(?:zsh|bash|sh|cmd(?:\.exe)?|powershell(?:\.exe)?|pwsh(?:\.exe)?)(?:\s|$)", re.IGNORECASE)
SHELL_COMMAND = re.compile(r"(?<![A-Za-z0-9_.-])(?:zsh|bash|cmd\.exe|powershell(?:\.exe)?|pwsh(?:\.exe)?)(?![A-Za-z0-9_.-])", re.IGNORECASE)
ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
INDEX_EOL = re.compile(r"\bi/(lf|crlf|mixed|none)\b")


def candidate_files(root: Path) -> Iterable[tuple[Path, Path]]:
    """Yield shared-source files in a stable, repository-relative order."""
    files: list[tuple[Path, Path]] = []
    for directory_name in AGENT_DIRECTORIES:
        directory = root / directory_name
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            relative_path = path.relative_to(root)
            if relative_path in LOCAL_ONLY_FILES:
                continue
            # Packaged copies contain the detector's own regex literals.
            if relative_path in SCANNER_IMPLEMENTATIONS:
                continue
            # Machine identity, deliberately not shared and not committed.
            if relative_path.parts[:2] == (".agent-sync", "local"):
                continue
            files.append((relative_path, path))
    yield from sorted(files, key=lambda item: item[0].as_posix())


def is_hook(relative_path: Path) -> bool:
    return "hooks" in relative_path.parts


def index_line_endings(root: Path) -> dict[str, str] | None:
    """Map repository-relative paths to their index line ending, if git can tell us.

    Working-tree CRLF is not a portability defect when the repository normalizes
    line endings (core.autocrlf, .gitattributes): the index holds LF, and the index
    is what gets committed. Judging raw working-tree bytes therefore painted every
    file in this repository red -- 567 findings, all of them noise -- and the gate
    was ignored. Return None when git is unavailable so callers can fall back.
    """

    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--eol"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    endings: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        fields, separator, path = line.partition("\t")
        if not separator:
            continue
        match = INDEX_EOL.search(fields)
        if match:
            endings[path] = match.group(1)
    return endings


def is_host_absolute(command: str) -> bool:
    """True for POSIX, drive-letter, or UNC host-absolute paths."""

    return (
        command.startswith("/")
        or command.startswith("\\\\")
        or bool(re.match(r"^[A-Za-z]:[\\/]", command))
    )


def iter_hook_commands(node: Any) -> Iterable[str]:
    """Yield every hook `command` string in a parsed settings document."""

    if isinstance(node, dict):
        for key, value in node.items():
            if key == "command" and isinstance(value, str):
                yield value
            else:
                yield from iter_hook_commands(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_hook_commands(item)


def command_executable(command: str) -> str | None:
    """Return a hook command's executable, ignoring leading env assignments.

    A bare absolute path elsewhere in a shared asset is not automatically a defect:
    a probe list of candidate interpreter locations (e.g. the conda search list in
    the research-collector scripts) is portable code. An absolute *executable in a
    hook command* is not -- it pins the hook to the machine that generated it.
    """

    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return None
    for token in tokens:
        if ENV_ASSIGNMENT.match(token):
            continue
        return token
    return None


def hook_command_findings(display_path: str, text: str) -> list[str]:
    findings: list[str] = []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return [f"{display_path}: invalid-json"]
    for command in iter_hook_commands(payload):
        executable = command_executable(command)
        if executable is not None and is_host_absolute(executable):
            findings.append(
                f"{display_path}: absolute-path: hook command runs {executable}"
            )
    return findings


def validate_tree(root: Path, platform_name: str) -> list[str]:
    """Return deterministic portability findings for shared agent sources."""
    if platform_name not in PLATFORMS:
        raise ValueError(f"unsupported platform: {platform_name}")

    index_eol = index_line_endings(root)
    findings: list[str] = []
    for relative_path, path in candidate_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = path.read_bytes()
        display_path = relative_path.as_posix()

        if index_eol is None:
            if b"\r\n" in content:
                findings.append(f"{display_path}: crlf")
        elif index_eol.get(display_path) in ("crlf", "mixed"):
            findings.append(f"{display_path}: crlf")

        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"{display_path}: invalid-utf8")
            continue
        if ABSOLUTE_PATH.search(text):
            findings.append(f"{display_path}: absolute-path")
        if relative_path in GENERATED_HOOK_CONFIGS:
            findings.extend(hook_command_findings(display_path, text))
        elif is_hook(relative_path) and (SHELL_SHEBANG.search(text) or SHELL_COMMAND.search(text)):
            findings.append(f"{display_path}: shell-hook")
    return findings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root")
    parser.add_argument("--platform", choices=PLATFORMS, default="windows", help="target platform")
    args = parser.parse_args(argv)

    try:
        findings = validate_tree(Path(args.root).resolve(), args.platform)
    except OSError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2
    if not findings:
        print("[OK] shared agent sources are portable")
        return 0
    for finding in findings:
        print(f"[ERROR] {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
