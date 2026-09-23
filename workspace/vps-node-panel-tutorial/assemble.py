#!/usr/bin/env python3
"""P5 组装：chapters/*.md -> output/final_note.md（确定性拼接，不派推理代理）。

归一规则：
- 章标题统一为 `## 第 N 章 ...`（原文有 `第1章` / `第 N 章` 两种写法）。
- 既有笔记双链统一为短式 `[[自建代理节点搭建实战]]`（与 vault 内 MOC / 既有笔记一致）。
- 章间用 `---` 分隔；文首生成 H1 + 目录。

幂等：每次先清空重建，重跑两遍输出逐字节相同；末尾打印改动计数。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CH_DIR = os.path.join(ROOT, "chapters")
OUT = os.path.join(ROOT, "output", "final_note.md")

TITLE = "VPS 自建节点零基础全流程（面板流）"
INTRO = (
    "> 本文以一条 YouTube 教程的章节顺序为骨架，事实性内容全部取自官方文档与一手研究，"
    "每条论断行内标注来源 ID。视频本身无字幕轨，其口播内容未被引用。"
)

LINK_CANON = "[[自建代理节点搭建实战]]"
LINK_VARIANTS = [
    "[[自建代理节点/自建代理节点搭建实战.md]]",
    "[[自建代理节点/自建代理节点搭建实战]]",
    "[[自建代理节点搭建实战.md]]",
]


def fail(msg):
    print(f"ASSEMBLE-FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def normalize(text):
    """返回 (归一后文本, 改动说明列表)。"""
    changes = []
    before = text

    # 1) 章标题统一 `## 第 N 章`
    def fix_h2(m):
        return f"## 第 {m.group(1)} 章"

    text, n = re.subn(r"^## 第\s*(\d+)\s*章", fix_h2, text, flags=re.M)
    if n:
        changes.append(f"章标题归一 {n} 处")

    # 2) 双链写法统一
    for v in LINK_VARIANTS:
        if v in text:
            c = text.count(v)
            text = text.replace(v, LINK_CANON)
            changes.append(f"双链 {v} -> {LINK_CANON} {c} 处")

    if text != before:
        changes.append("(内容已变更)")
    return text, changes


def main():
    files = sorted(f for f in os.listdir(CH_DIR) if f.endswith(".md"))
    if len(files) != 11:
        fail(f"期望 11 个章节文件，实际 {len(files)}: {files}")

    parts, headings, all_changes = [], [], []
    for fn in files:
        raw = io.open(os.path.join(CH_DIR, fn), encoding="utf-8").read()
        if raw.startswith("# "):
            fail(f"{fn} 含 H1 标题，应由组装层生成")
        body, ch = normalize(raw)
        if ch:
            all_changes.append(f"{fn}: " + "；".join(ch))
        body = body.strip("\n")
        parts.append(body)
        headings += [l for l in body.splitlines() if l.startswith("## ")]

    if len(headings) != 12:
        fail(f"期望 12 个 H2（10 章 + 2 附录），实际 {len(headings)}")
    dupes = {h for h in headings if headings.count(h) > 1}
    if dupes:
        fail(f"H2 标题重复: {dupes}")

    toc = "\n".join(f"- [[#{h[3:].strip()}]]" for h in headings)
    doc = (
        f"# {TITLE}\n\n{INTRO}\n\n## 目录\n\n{toc}\n\n"
        + "\n\n---\n\n".join(parts)
        + "\n"
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(doc)

    han = len(re.findall(r"[一-鿿]", doc))
    print(f"写出 {os.path.relpath(OUT, ROOT)}  {os.path.getsize(OUT)} B  中文 {han}")
    print(f"章节 {len(parts)}   H2 {len(headings)}   目录项 {len(headings)}")
    print("归一改动：" if all_changes else "归一改动：无")
    for c in all_changes:
        print("  -", c)


if __name__ == "__main__":
    main()
