#!/usr/bin/env python3
"""Obsidian Markdown structure self-check: catch "valid Markdown that renders wrong".

内容校验（`note-citation-check.py` 的 V 逐字回源 / S 引文体例 / C 多副本一致）查的是
引文与副本一致性，查不到「合法 Markdown 却渲染异常」的排版缺陷——callout 续行缺 `>`
会让表格掉出框外，而内容校验照样全绿。本脚本只查三类**已确认**的 Obsidian 渲染形态，
不做通用 Markdown lint（避免误报把门变噪音）：

  1. 表格行前缺空行               → 表格不渲染
  2. callout 内表格未用 `>` 续接   → 表格掉出 callout
  3. 缩进的表格（疑似嵌进列表项）   → Obsidian 不渲染列表内的表格

配套：`.codex/rules/obsidian/note-system.md`（格式规则）、`note-beautifier` 的 Step 4 清单。
Stdlib only.

Usage:
  python .codex/scripts/check-md-structure.py <file-or-dir> [more...]

Exit codes: 0 = clean, 1 = findings, 2 = no input path.
"""

from __future__ import annotations

import glob
import os
import sys


def _force_utf8() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def iter_markdown(paths: list[str]):
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*.md"), recursive=True)):
                yield f
        elif os.path.isfile(p):
            yield p
        else:
            print(f"[skip] 路径不存在：{p}", file=sys.stderr)


def _fence_marker(line: str):
    s = line.strip()
    if s.startswith("```"):
        return "```"
    if s.startswith("~~~"):
        return "~~~"
    return None


def check_file(path: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except (OSError, UnicodeDecodeError) as exc:  # pragma: no cover - IO guard
        print(f"[skip] 读取失败 {path}：{exc}", file=sys.stderr)
        return findings

    fence = None
    for i, line in enumerate(lines):
        marker = _fence_marker(line)
        if fence is None and marker:
            fence = marker
            continue
        if fence is not None:
            if marker == fence:
                fence = None
            continue

        prev = lines[i - 1] if i > 0 else ""

        # 类 3：缩进的表格（疑似嵌进列表项）——同一张表只报首行
        if line[:1] in (" ", "\t") and line.lstrip().startswith("|"):
            prev_is_row = prev[:1] in (" ", "\t") and prev.lstrip().startswith("|")
            if not prev_is_row:
                findings.append((i + 1, "缩进的表格（疑似嵌进列表项）：Obsidian 不渲染列表内的表格"))
            continue

        # 类 2：callout 内表格（本行以 `>` 开头，去掉 `>` 后是表格行）
        if line.startswith(">") and line[1:].lstrip().startswith("|"):
            if not prev.startswith(">"):
                findings.append((i + 1, "callout 内表格未用 `>` 续接：表格掉出 callout"))
            else:
                inner = prev[1:].lstrip()
                if inner != "" and not inner.startswith("|"):
                    findings.append(
                        (i + 1, "callout 内表格未以空 `>` 行与上文分隔：表格不渲染")
                    )
            continue

        # 类 1：顶层表格行前缺空行
        if line.startswith("|"):
            if prev.strip() and not prev.startswith("|"):
                findings.append((i + 1, "表格行前缺空行：表格不渲染"))

    return findings


def main(argv: list[str]) -> int:
    _force_utf8()
    paths = argv[1:]
    if not paths:
        print(
            "用法：python .codex/scripts/check-md-structure.py <file-or-dir> [more...]",
            file=sys.stderr,
        )
        return 2

    files = list(iter_markdown(paths))
    total = 0
    for f in files:
        for ln, msg in check_file(f):
            print(f"{f}:{ln}  {msg}")
            total += 1
    print(f"结构自检：扫描 {len(files)} 个文件，发现 {total} 处可疑")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
