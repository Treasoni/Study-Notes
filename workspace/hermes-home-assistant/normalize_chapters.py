#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 chapters/ 各章的尾部导航收敛成统一的 `###` 小标题。

为什么在源文件上做，而不是在某个下游产物上做：
各章是四批并行写出来的，尾部导航长出了三种写法（粗体引导词 / 裸段落 / `###` 标题）。
原先只在 assemble_note.py 里归一，结果是「合并件是齐的、发布件是花的」——
发布器直接从 chapters/ 取源文，把没归一的原文发了出去。归一只做一次，做在源上，
下游（assemble_note.py / publish_volume.py）只做机械变换，不再各自持有一套规则。

本脚本只改「小节标题的写法」，不改任何句子。防篡改断言见 verify()。
"""

import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(__file__).resolve().parent / "chapters"

# 第 4、5 章的来源是脚注体，补一个小节标题 + 一行体例说明，与其余各章对齐。
SRC_SIGNPOST = (
    "### 本章来源\n\n"
    "本章采用**脚注体**引用：正文里的上标与该章的脚注定义一一对应，"
    "下附脚注定义块即本章来源清单，每条开头标注 canonical ID（`HAS-*` / `HMS-*` / `SRC-*` / `COM-*`）。"
    "其余各章为来源表体，两处内容等价。"
)
SIGNPOST_CHAPTERS = {"04-落地-社区ha-mcp.md", "05-落地-官方mcp_server.md"}

# (正则, 替换) —— 逐行应用；只允许命中这些形态
RULES = [
    (re.compile(r"^\*\*本章小结\*\*\s*$"), "### 本章小结"),
    (re.compile(r"^\*\*下一章预告\*\*[：:]\s*(?=\S)"), "### 下一章预告\n\n"),
    (re.compile(r"^\*\*本章引用来源\*\*（按 canonical ID）[：:]\s*(?=\S)"), "### 本章来源\n\n"),
    (re.compile(r"^### 本章来源与回源核对\s*$"), "### 本章来源"),
    (re.compile(r"^(?=下一章换)"), "### 下一章预告\n\n"),
]

# 被整行替换掉的旧形态（用于反向断言）
OLD_NAV = re.compile(
    r"^\*\*本章小结\*\*\s*$"
    r"|^\*\*下一章预告\*\*[：:]"
    r"|^\*\*本章引用来源\*\*（按 canonical ID）[：:]"
    r"|^### 本章来源与回源核对\s*$"
    r"|^下一章换"
)

FIXED_NEW = {"### 本章小结", "### 下一章预告", "### 本章来源", ""}
FIXED_NEW |= set(SRC_SIGNPOST.split("\n"))

# `^(?=下一章换)` 是零宽前瞻：它不消耗「下一章换…」那一段，所以第二次运行时
# 上一轮刚插进去的 `### 下一章预告` 还在，会再插一个。折叠「中间只有空行」的重复标题。
DUP_NAV = re.compile(r"(### 下一章预告[ \t]*\n(?:[ \t]*\n)+)### 下一章预告[ \t]*\n")


def normalize(text):
    out = []          # 物理行（不是逻辑行），这样才能看上一非空行
    for line in text.split("\n"):
        for pat, repl in RULES:
            m = pat.match(line)
            if m:
                line = repl + line[m.end():]
                break
        # 零宽前瞻那条规则：上一非空行已经是 `### 下一章预告` 时只保留段落，
        # 否则每跑一遍都会再插一个标题（并多留一个空行）。
        if line.startswith("### 下一章预告"):
            j = len(out) - 1
            while j >= 0 and out[j].strip() == "":
                j -= 1
            if j >= 0 and out[j].strip() == "### 下一章预告":
                rest = line[len("### 下一章预告"):].lstrip("\n")
                if rest:
                    out.append(rest)
                continue
        out.extend(line.split("\n"))
    text = "\n".join(out)
    # 兜底：中间只有空行的重复标题一并折叠
    while True:
        folded = DUP_NAV.sub(r"\1", text)
        if folded == text:
            return text
        text = folded


def trailing_def_start(lines):
    """返回「尾部连续脚注定义块」的起始行号。

    第 4、5 章的脚注定义是分散写的：正文中段散着几条（跟在被引段落后面），
    文末另有一个密集块。体例说明必须插在**文末那个块**之前——
    插在「第一个定义」之前会落进正文中段。
    """
    i = len(lines) - 1
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    if i < 0 or not re.match(r"^\[\^[^\]]+\]:", lines[i]):
        return None
    start = i
    while start - 1 >= 0:
        prev = lines[start - 1]
        if re.match(r"^\[\^[^\]]+\]:", prev) or prev.strip() == "":
            start -= 1
        else:
            break
    return start


def strip_signpost(text):
    """幂等：先移除既有的体例说明块（含两种历史位置），再重新插入正确位置。"""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if (lines[i].strip() == "### 本章来源"
                and i + 2 < len(lines)
                and lines[i + 1].strip() == ""
                and lines[i + 2].startswith("本章采用**脚注体**引用")):
            i += 3
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            # 去掉被移除块留下的多余空行
            while out and out[-1].strip() == "":
                out.pop()
            out.append("")
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def verify(before, after, name, problems):
    """正向：新行必须逐字来自原文，或是原文某行剥掉前缀后的后缀。
    反向：消失的行必须全部命中已知的旧导航形态。"""
    old = before.split("\n")
    new = after.split("\n")
    old_set, new_set = set(old), set(new)
    for l in new:
        if l in old_set or l in FIXED_NEW:
            continue
        if l and any(o.endswith(l) and o != l for o in old):
            continue
        problems.append("{} 出现了无法追溯的新行：{!r}".format(name, l[:70]))
    for l in old:
        if l in new_set or OLD_NAV.match(l) or l in FIXED_NEW:
            continue
        problems.append("{} 有正文行消失：{!r}".format(name, l[:70]))


def main():
    problems = []
    pending = []

    # 第一遍：只计算并校验，不落盘——任何一处断言失败就整体不写
    for p in sorted(SRC.glob("*.md")):
        before = p.read_text(encoding="utf-8").rstrip("\n")
        text = normalize(before)

        if p.name in SIGNPOST_CHAPTERS:
            # 幂等：先撤掉任何既有说明块（含此前插错位置的那份），再重插
            text = strip_signpost(text)
            lines = text.split("\n")
            start = trailing_def_start(lines)
            if start is None:
                problems.append("{} 找不到尾部脚注定义块".format(p.name))
                continue
            lines.insert(start, SRC_SIGNPOST + "\n")
            text = "\n".join(lines)

        verify(before, text, p.name, problems)
        pending.append((p, before, text))

    if problems:
        print("!! 断言未通过，未写盘（文件保持原样）：")
        for x in problems:
            print("   - {}".format(x))
        raise SystemExit(1)

    # 第二遍：全部校验通过后才落盘
    print("== 归一结果 ==")
    for p, before, text in pending:
        if text != before:
            p.write_text(text + "\n", encoding="utf-8", newline="\n")
            print("  {:<34} 已归一".format(p.name))
        else:
            print("  {:<34} 无变化".format(p.name))
    print()
    print("所有断言通过：改动仅限小节标题写法，正文未变。")


if __name__ == "__main__":
    main()
