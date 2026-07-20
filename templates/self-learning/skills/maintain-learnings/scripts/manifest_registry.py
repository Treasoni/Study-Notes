#!/usr/bin/env python3
"""Discover and validate agent component manifest.yaml files.

The parser intentionally supports a small YAML subset so target projects do not
need PyYAML just to validate the platform registry contract.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SUPPORTED_API_VERSION = "agent-platform/v1alpha1"
SUPPORTED_KINDS = {"Workflow", "Skill", "Subagent", "Hook"}
DEPENDENCY_KINDS = {
    "skills": "Skill",
    "workflows": "Workflow",
    "subagents": "Subagent",
    "hooks": "Hook",
}
DEFAULT_SCANS = (".agents", ".claude", ".codex/hooks", ".claude/hooks")
KEY_VALUE_RE = re.compile(r"^([^:][^:]*):(.*)$")


@dataclass
class Finding:
    level: str
    path: str
    message: str


@dataclass
class Manifest:
    path: Path
    data: dict[str, Any]

    @property
    def kind(self) -> str:
        return str(self.data.get("kind", ""))

    @property
    def name(self) -> str:
        metadata = self.data.get("metadata")
        if isinstance(metadata, dict):
            return str(metadata.get("name", ""))
        return ""


class ManifestParseError(ValueError):
    pass


def strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if index == 0 or line[index - 1].isspace():
                return line[:index].rstrip()
    return line.rstrip()


def prepare_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ManifestParseError(f"line {number}: tabs are not allowed for indentation")
        stripped = strip_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.strip()))
    return lines


def split_inline_list(value: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    quote = ""
    escape = False
    for char in value:
        if escape:
            current.append(char)
            escape = False
            continue
        if char == "\\" and quote == '"':
            current.append(char)
            escape = True
            continue
        if char in {"'", '"'}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            current.append(char)
            continue
        if char == "," and not quote:
            items.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if quote:
        raise ManifestParseError("unterminated quote in inline list")
    tail = "".join(current).strip()
    if tail:
        items.append(tail)
    return items


def parse_scalar(value: str) -> Any:
    value = value.strip()
    lowered = value.lower()
    if value == "":
        return ""
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in split_inline_list(inner)]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        unquoted = value[1:-1]
        if value.startswith('"'):
            return bytes(unquoted, "utf-8").decode("unicode_escape")
        return unquoted.replace("''", "'")
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def split_key_value(text: str) -> tuple[str, str | None]:
    match = KEY_VALUE_RE.match(text)
    if not match:
        raise ManifestParseError(f"expected key/value pair, got: {text}")
    key = match.group(1).strip()
    value = match.group(2)
    if not key:
        raise ManifestParseError(f"empty key in: {text}")
    return key, value.strip() if value.strip() else None


def parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, text = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent != indent:
        raise ManifestParseError(f"unexpected indentation before: {text}")
    if text.startswith("- "):
        return parse_list(lines, index, indent)
    return parse_map(lines, index, indent)


def parse_map(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ManifestParseError(f"unexpected nested line: {text}")
        if text.startswith("- "):
            break
        key, value = split_key_value(text)
        index += 1
        if value is not None:
            result[key] = parse_scalar(value)
            continue
        if index < len(lines) and lines[index][0] > current_indent:
            nested, index = parse_block(lines, index, lines[index][0])
            result[key] = nested
        else:
            result[key] = None
    return result, index


def parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ManifestParseError(f"unexpected nested list line: {text}")
        if not text.startswith("- "):
            break
        item_text = text[2:].strip()
        index += 1
        if not item_text:
            if index < len(lines) and lines[index][0] > current_indent:
                item, index = parse_block(lines, index, lines[index][0])
            else:
                item = None
            result.append(item)
            continue
        if KEY_VALUE_RE.match(item_text):
            key, value = split_key_value(item_text)
            item: dict[str, Any] = {key: parse_scalar(value) if value is not None else None}
            while index < len(lines) and lines[index][0] > current_indent:
                nested, index = parse_block(lines, index, lines[index][0])
                if isinstance(nested, dict):
                    item.update(nested)
                else:
                    item.setdefault("items", nested)
            result.append(item)
        else:
            result.append(parse_scalar(item_text))
            if index < len(lines) and lines[index][0] > current_indent:
                raise ManifestParseError(f"scalar list item cannot have nested children: {item_text}")
    return result, index


def parse_yaml_subset(text: str) -> dict[str, Any]:
    lines = prepare_lines(text)
    if not lines:
        return {}
    document, index = parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise ManifestParseError(f"unparsed content near: {lines[index][1]}")
    if not isinstance(document, dict):
        raise ManifestParseError("manifest root must be a mapping")
    return document


def read_manifest(path: Path) -> Manifest:
    try:
        data = parse_yaml_subset(path.read_text(encoding="utf-8"))
    except ManifestParseError:
        raise
    except OSError as exc:
        raise ManifestParseError(str(exc)) from exc
    return Manifest(path=path, data=data)


def as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def add(findings: list[Finding], level: str, path: Path, message: str) -> None:
    findings.append(Finding(level, str(path), message))


def require_string(findings: list[Finding], manifest: Manifest, dotted: str) -> str:
    value = get_path(manifest.data, dotted)
    if isinstance(value, str) and value.strip():
        return value
    add(findings, "ERROR", manifest.path, f"missing string field: {dotted}")
    return ""


def require_list(findings: list[Finding], manifest: Manifest, dotted: str) -> list[Any]:
    value = get_path(manifest.data, dotted)
    if isinstance(value, list):
        return value
    add(findings, "ERROR", manifest.path, f"missing list field: {dotted}")
    return []


def check_entrypoint(findings: list[Finding], manifest: Manifest) -> None:
    entrypoint = get_path(manifest.data, "spec.entrypoint")
    if not isinstance(entrypoint, str) or not entrypoint:
        add(findings, "ERROR", manifest.path, "missing string field: spec.entrypoint")
        return
    target = (manifest.path.parent / entrypoint).resolve()
    if not target.exists():
        add(findings, "ERROR", manifest.path, f"entrypoint does not exist: {entrypoint}")


def validate_common(manifest: Manifest) -> list[Finding]:
    findings: list[Finding] = []
    api_version = require_string(findings, manifest, "apiVersion")
    kind = require_string(findings, manifest, "kind")
    metadata = get_path(manifest.data, "metadata")
    spec = get_path(manifest.data, "spec")
    permissions = get_path(manifest.data, "permissions")

    if api_version and api_version != SUPPORTED_API_VERSION:
        add(findings, "WARN", manifest.path, f"unsupported apiVersion: {api_version}")
    if kind and kind not in SUPPORTED_KINDS:
        add(findings, "ERROR", manifest.path, f"unsupported kind: {kind}")
    if not isinstance(metadata, dict):
        add(findings, "ERROR", manifest.path, "metadata must be a mapping")
    if not isinstance(spec, dict):
        add(findings, "ERROR", manifest.path, "spec must be a mapping")
    if not isinstance(permissions, dict):
        add(findings, "ERROR", manifest.path, "permissions must be a mapping")

    require_string(findings, manifest, "metadata.name")
    version = require_string(findings, manifest, "metadata.version")
    require_string(findings, manifest, "metadata.description")
    if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        add(findings, "WARN", manifest.path, f"metadata.version is not semver-like: {version}")

    fs = get_path(manifest.data, "permissions.filesystem")
    if not isinstance(fs, dict):
        add(findings, "ERROR", manifest.path, "permissions.filesystem must be a mapping")
    else:
        if not isinstance(fs.get("read"), list):
            add(findings, "ERROR", manifest.path, "permissions.filesystem.read must be a list")
        if not isinstance(fs.get("write"), list):
            add(findings, "ERROR", manifest.path, "permissions.filesystem.write must be a list")
    if not isinstance(get_path(manifest.data, "permissions.network"), bool):
        add(findings, "ERROR", manifest.path, "permissions.network must be true or false")
    if not isinstance(get_path(manifest.data, "permissions.tools"), list):
        add(findings, "ERROR", manifest.path, "permissions.tools must be a list")

    dependencies = get_path(manifest.data, "dependencies")
    if dependencies is not None and not isinstance(dependencies, dict):
        add(findings, "ERROR", manifest.path, "dependencies must be a mapping")
    events = get_path(manifest.data, "events.triggers")
    if events is not None and not isinstance(events, list):
        add(findings, "ERROR", manifest.path, "events.triggers must be a list")
    platforms = get_path(manifest.data, "compatibility.platforms")
    if platforms is not None and not isinstance(platforms, list):
        add(findings, "ERROR", manifest.path, "compatibility.platforms must be a list")
    return findings


def validate_kind(manifest: Manifest) -> list[Finding]:
    findings: list[Finding] = []
    kind = manifest.kind
    if kind not in SUPPORTED_KINDS:
        return findings

    if kind in {"Skill", "Subagent", "Hook"}:
        require_string(findings, manifest, "spec.runtime")
        check_entrypoint(findings, manifest)

    if kind == "Workflow":
        require_string(findings, manifest, "spec.runtime")
        steps = require_list(findings, manifest, "spec.steps")
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                add(findings, "ERROR", manifest.path, f"spec.steps[{index}] must be a mapping")
                continue
            if not isinstance(step.get("id"), str) or not step.get("id"):
                add(findings, "ERROR", manifest.path, f"spec.steps[{index}] missing id")
            if not step.get("uses") and not step.get("action"):
                add(findings, "ERROR", manifest.path, f"spec.steps[{index}] needs uses or action")
    elif kind == "Skill":
        if not isinstance(get_path(manifest.data, "spec.activation.description"), str):
            add(findings, "WARN", manifest.path, "Skill should declare spec.activation.description")
    elif kind == "Subagent":
        if not isinstance(get_path(manifest.data, "spec.model"), str):
            add(findings, "WARN", manifest.path, "Subagent should declare spec.model")
        if not isinstance(get_path(manifest.data, "spec.tools"), list):
            add(findings, "WARN", manifest.path, "Subagent should declare spec.tools")
    elif kind == "Hook":
        require_string(findings, manifest, "spec.event")
        if not isinstance(get_path(manifest.data, "spec.blocking"), bool):
            add(findings, "WARN", manifest.path, "Hook should declare spec.blocking")
        timeout = get_path(manifest.data, "spec.timeoutSeconds")
        if timeout is not None and not isinstance(timeout, int):
            add(findings, "WARN", manifest.path, "Hook spec.timeoutSeconds should be an integer")
    return findings


def dependency_name(raw: Any) -> str:
    text = str(raw)
    return text.split("@", 1)[0].strip()


def validate_dependencies(manifests: list[Manifest]) -> list[Finding]:
    findings: list[Finding] = []
    available: dict[str, set[str]] = {kind: set() for kind in SUPPORTED_KINDS}
    for manifest in manifests:
        if manifest.kind in available and manifest.name:
            available[manifest.kind].add(manifest.name)

    for manifest in manifests:
        dependencies = as_mapping(manifest.data.get("dependencies"))
        for key, kind in DEPENDENCY_KINDS.items():
            for item in as_list(dependencies.get(key)):
                name = dependency_name(item)
                if name and name not in available[kind]:
                    add(findings, "WARN", manifest.path, f"dependency not found in scan set: {key}.{name}")
    return findings


def discover(root: Path, scans: list[str]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for scan in scans:
        base = (root / scan).resolve()
        candidates: list[Path]
        if base.is_file():
            candidates = [base]
        elif base.exists():
            candidates = sorted(list(base.rglob("manifest.yaml")) + list(base.rglob("manifest.yml")))
        else:
            continue
        for path in candidates:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                paths.append(path)
    return paths


def render_markdown(manifests: list[Manifest], findings: list[Finding]) -> str:
    lines = ["# Manifest Registry Report", ""]
    if manifests:
        lines.append("## Components")
        lines.append("")
        lines.append("| Kind | Name | Version | Path |")
        lines.append("|---|---|---:|---|")
        for manifest in sorted(manifests, key=lambda item: (item.kind, item.name, str(item.path))):
            version = get_path(manifest.data, "metadata.version") or ""
            lines.append(f"| {manifest.kind} | `{manifest.name}` | {version} | `{manifest.path}` |")
        lines.append("")
    else:
        lines.extend(["No manifests found.", ""])

    lines.append("## Findings")
    lines.append("")
    if not findings:
        lines.append("- [OK] all manifests passed validation")
    else:
        for finding in findings:
            lines.append(f"- [{finding.level}] `{finding.path}` {finding.message}")
    return "\n".join(lines) + "\n"


def render_json(manifests: list[Manifest], findings: list[Finding]) -> str:
    return json.dumps(
        {
            "components": [
                {
                    "kind": manifest.kind,
                    "name": manifest.name,
                    "version": get_path(manifest.data, "metadata.version"),
                    "path": str(manifest.path),
                }
                for manifest in manifests
            ],
            "findings": [finding.__dict__ for finding in findings],
        },
        ensure_ascii=False,
        indent=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root.")
    parser.add_argument("--scan", action="append", help="Directory or manifest file to scan. Repeatable.")
    parser.add_argument("--kind", choices=sorted(SUPPORTED_KINDS), help="Only report a specific component kind.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    scan_paths = args.scan or list(DEFAULT_SCANS)
    manifests: list[Manifest] = []
    findings: list[Finding] = []
    for path in discover(root, scan_paths):
        try:
            manifest = read_manifest(path)
        except ManifestParseError as exc:
            findings.append(Finding("ERROR", str(path), f"parse failed: {exc}"))
            continue
        if args.kind and manifest.kind != args.kind:
            continue
        manifests.append(manifest)
        findings.extend(validate_common(manifest))
        findings.extend(validate_kind(manifest))

    findings.extend(validate_dependencies(manifests))
    print(render_json(manifests, findings) if args.json else render_markdown(manifests, findings))

    if any(finding.level == "ERROR" for finding in findings):
        return 1
    if args.strict and any(finding.level == "WARN" for finding in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

