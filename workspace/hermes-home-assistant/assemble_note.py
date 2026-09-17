#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P5 收尾组装：把 chapters/ 下的 10 个文件按大纲顺序拼成 output/final_note.md。

设计约束（与项目学习记录一致）：
- 只做「确定性拼接 + 标题归一 + 目录生成」，不改写正文、不动引用机制。
- 拼接前对每章尾部做幂等归一（去尾部空行与 `---` 分隔线）。
- 断言：章标题数、导航小标题出现次数 == 期望值、脚注 ID 全局唯一、fence 闭合。
"""

import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "chapters"
OUT = ROOT / "output" / "final_note.md"

TITLE = "用 Hermes Agent 控制 Home Assistant：能力地图与实现路线"

# 章节顺序（大纲已确认的顺序），同时携带章节编号归一映射
ORDER = [
    ("01-结论先行与能力地图.md", "第一章", "第 1 章"),
    ("02-三方对照轴.md", "第二章", "第 2 章"),
    ("03-路线选型.md", "第三章", "第 3 章"),
    ("04-落地-社区ha-mcp.md", None, None),
    ("05-落地-官方mcp_server.md", None, None),
    ("06-事件驱动与定时任务.md", None, None),
    ("07-安全与限界.md", None, None),
    ("08-文档与代码不一致.md", None, None),
    ("09-成本与可靠性.md", None, None),
    ("10-附录.md", None, None),
]

# 不进目录的导航性小节（按标题前缀匹配）
NAV_PREFIXES = ("本章小结", "下一章预告", "本章来源", "附录小结")

FRONTMATTER = """---
title: "{title}"
created: 2026-09-18
updated: 2026-09-18
status: draft
source_project: hermes-home-assistant
---

""".format(title=TITLE)


def load(name):
    return (SRC / name).read_text(encoding="utf-8")


def strip_tail(text):
    """幂等归一：去掉尾部空行与 `---` 分隔线，返回 (正文, 被去掉的行数)。"""
    lines = text.split("\n")
    removed = 0
    while lines:
        s = lines[-1].strip()
        if s == "" or s == "---":
            lines.pop()
            removed += 1
        else:
            break
    return "\n".join(lines), removed


def check_fences(name, text):
    n = sum(1 for l in text.split("\n") if l.lstrip().startswith("```"))
    if n % 2 != 0:
        raise SystemExit("!! {} 的代码块 fence 未闭合（{} 行）".format(name, n))


# 尾部导航的归一只做一次，且做在源文件上（见 normalize_chapters.py）。
# 这里刻意不再持有归一规则：否则「合并件被归一、发布件没被归一」，
# 同一份源文会产出两种形态。下游一律只做机械变换。
def strip_code(text):
    """剥掉 fenced 代码块与行内代码，用于脚注/ID 扫描（避免把正则字符类当脚注）。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def headings(text):
    """返回 (level, title) 列表，只取 fence 之外的标题。"""
    out = []
    infence = False
    for l in text.split("\n"):
        if l.lstrip().startswith("```"):
            infence = not infence
            continue
        if infence:
            continue
        m = re.match(r"^(#{2,6})\s+(.*)$", l)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def main():
    bodies = []
    report = []

    for name, old_word, new_word in ORDER:
        raw = load(name)
        check_fences(name, raw)
        body, removed = strip_tail(raw)

        # 章标题编号归一：只在正文首行的标题里替换
        if old_word:
            lines = body.split("\n")
            idx = next(i for i, l in enumerate(lines) if l.startswith("## "))
            if old_word not in lines[idx]:
                raise SystemExit("!! {} 首行标题里找不到 {}".format(name, old_word))
            lines[idx] = lines[idx].replace(old_word, new_word, 1)
            body = "\n".join(lines)

        bodies.append((name, body))
        report.append((name, removed, len(body.encode("utf-8"))))

    # ---- 组装目录 ----
    # 含反引号 / 竖线 / 方括号 / 井号 / 箭头的标题不能做 Obsidian 锚点：
    # 反引号会被当成行内代码、`|` 是别名分隔符、`#` 是标题分隔符，都会让链接解析失败。
    UNSAFE = ("`", "|", "[", "]", "#", "→")

    toc = ["## 目录", ""]
    toc_targets = []
    skipped = []
    for name, body in bodies:
        for level, h in headings(body):
            if level not in (2, 3):
                continue
            if h.startswith(NAV_PREFIXES):
                continue
            if any(ch in h for ch in UNSAFE):
                skipped.append((name, level, h))
                continue
            if level == 2:
                toc.append("- **[[#{}]]**".format(h))
            else:
                toc.append("  - [[#{}]]".format(h))
            toc_targets.append(h)
    toc.append("")

    # 目录锚点必须全局唯一，否则 Obsidian 会跳到第一个同名标题
    dup = [h for h in set(toc_targets) if toc_targets.count(h) > 1]
    if dup:
        raise SystemExit("!! 目录锚点重复，Obsidian 会跳错：{}".format(dup))

    # ---- 拼接 ----
    parts = [FRONTMATTER, "# {}\n\n".format(TITLE), "\n".join(toc), "\n"]
    for name, body in bodies:
        parts.append("---\n\n")
        parts.append(body.rstrip("\n") + "\n\n")

    merged = "".join(parts)

    # ---- 成品断言 ----
    problems = []

    n_ch = len(re.findall(r"^## (?:第 \d+ 章|附录)：", merged, re.M))
    if n_ch != len(ORDER):
        problems.append("章标题数 {} != {}".format(n_ch, len(ORDER)))

    for nav, expect in (("下一章预告", 9), ("本章来源", 9), ("本章小结", 7)):
        got = len(re.findall(r"^###\s+" + re.escape(nav) + r"\s*$", merged, re.M))
        if got != expect:
            problems.append("`### {}` 出现 {} 次（期望 {}）".format(nav, got, expect))

    # 脚注：定义与引用都必须全局唯一（跨章撞号会让正文跳到别人的脚注）
    scan = strip_code(merged)
    defs = re.findall(r"^\[\^([^\]]+)\]:", scan, re.M)
    refs = re.findall(r"\[\^([^\]]+)\](?!:)", scan)
    dup_defs = sorted({d for d in defs if defs.count(d) > 1})
    orphan_refs = sorted(set(refs) - set(defs))
    orphan_defs = sorted(set(defs) - set(refs))
    if dup_defs:
        problems.append("脚注定义撞号：{}".format(dup_defs))
    if orphan_refs:
        problems.append("有引用无定义：{}".format(orphan_refs))
    if orphan_defs:
        problems.append("有定义无引用：{}".format(orphan_defs))

    n_fence = sum(1 for l in merged.split("\n") if l.lstrip().startswith("```"))
    if n_fence % 2 != 0:
        problems.append("成品 fence 未闭合（{} 行）".format(n_fence))

    # 来源 ID 卫生：不得出现局部编号
    local_ids = sorted(set(re.findall(r"\b(?:H-\d\d|HA-\d\d|HAS-M\d+|HMS-M\d+|COM-M\d+)\b", scan)))
    if local_ids:
        problems.append("出现局部编号：{}".format(local_ids))

    han = len(re.findall(r"[一-鿿]", re.sub(r"```.*?```", "", merged, flags=re.S)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(merged, encoding="utf-8", newline="\n")

    print("== 各章（文件 / 归一移除行数 / 字节） ==")
    for name, removed, nb in report:
        print("  {:<34} -{:<3} {:>7} B".format(name, removed, nb))
    print()
    print("== 成品 ==")
    print("  路径        {}".format(OUT.relative_to(ROOT.parent.parent)))
    print("  字节        {}".format(len(merged.encode("utf-8"))))
    print("  正文汉字    {}".format(han))
    print("  章标题      {}".format(n_ch))
    print("  目录条目    {}（另有 {} 条因标题含反引号/竖线等被跳过，见下）".format(
        len(toc_targets), len(skipped)))
    print("  脚注        定义 {} 条 ／ 引用 {} 处".format(len(defs), len(refs)))
    if skipped:
        print()
        print("== 未进目录的标题（Obsidian 锚点不安全，正文中仍然存在） ==")
        for name, level, h in skipped:
            print("  {} h{} {}".format(name[:2], level, h))
    print()
    if problems:
        print("!! 断言未通过：")
        for p in problems:
            print("   - {}".format(p))
        raise SystemExit(1)
    print("所有断言通过。")


if __name__ == "__main__":
    main()
