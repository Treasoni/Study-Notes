#!/usr/bin/env python3
"""章节源文件的发布前归一：① 中文直引号 -> 「」；② 反引号包住的 wikilink 脱壳。

① 只动正文：围栏代码块与行内代码里的引号一律跳过（JSON 字段名靠它们保护）。
   规则是确定性的：按出现顺序交替开合。逐行断言引号数成对，不成立即失败退出。
② 反引号包住的 [[目标]] 在 Obsidian 里渲染成字面量而不是链接，必须脱掉反引号，
   否则链接校验会通过、读者点不动（校验绿灯 != 产物正确）。
"""

from __future__ import annotations

import pathlib
import re
import sys

NL = chr(10)
SRC_DIR = pathlib.Path(__file__).parent / "chapters"
FILES = ["00_导读.md", "01_CDN是什么.md", "02_为什么能救被墙.md",
         "03_接入Cloudflare.md", "04_套上CDN.md",
         "05_被墙判定与加速取舍.md", "06_排错速查.md"]

OPEN, CLOSE = "「", "」"
OPEN2, CLOSE2 = "『", "』"
FENCE = "```"
TICKLINK = re.compile(r"`\[\[([^\]]+)\]\]`")


def unwrap_ticklinks(line: str) -> tuple[str, int]:
    """把 `[[目标]]` 脱壳成 [[目标]]（反引号里的 wikilink 渲染不出链接）。"""
    return TICKLINK.subn(lambda m: f"[[{m.group(1)}]]", line)


def convert_line(line: str) -> tuple[str, int, int]:
    """返回 (新行, 本行替换数, 本行引号数)。"""
    if line.count('"') % 2:
        raise ValueError(f"引号不成对：{line}")
    total = line.count('"')
    if total == 0:
        return line, 0, 0
    out = []
    i = 0
    hits = 0
    # 行内代码段位置
    code_spans = [(m.start(), m.end()) for m in re.finditer(r"`[^`]*`", line)]
    depth = 0  # >0 表示处在中文引号内
    while i < len(line):
        ch = line[i]
        if ch == "`":
            covered = next((s for s in code_spans if s[0] == i), None)
            if covered:
                out.append(line[covered[0]:covered[1]])
                i = covered[1]
                continue
        if ch == '"':
            if depth == 0:
                out.append(OPEN)
                depth = 1
            else:
                out.append(CLOSE)
                depth = 0
            hits += 1
        else:
            out.append(ch)
        i += 1
    # 只报真实替换数：行内代码里的引号虽被数进 total，但并未改动
    return "".join(out), hits, total


def main() -> int:
    changed_total = 0
    for name in FILES:
        p = SRC_DIR / name
        text = p.read_text(encoding="utf-8")
        lines = text.split(NL)
        in_fence = False
        new_lines = []
        n_here = 0
        for ln, line in enumerate(lines, 1):
            if line.lstrip().startswith(FENCE):
                in_fence = not in_fence
                new_lines.append(line)
                continue
            if in_fence:
                new_lines.append(line)
                continue
            line, n_tick = unwrap_ticklinks(line)
            try:
                new, cnt, _ = convert_line(line)
            except ValueError as e:
                print(f"FAIL {name}:{ln} {e}", file=sys.stderr)
                return 1
            n_here += cnt + n_tick
            new_lines.append(new)
        if n_here:
            p.write_text(NL.join(new_lines), encoding="utf-8", newline=NL)
        changed_total += n_here
        print(f"  {name}: 替换 {n_here} 处")
    print(f"本次改动 {changed_total} 处")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
