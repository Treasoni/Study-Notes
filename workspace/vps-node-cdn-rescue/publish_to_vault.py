#!/usr/bin/env python3
"""把 vps-node-cdn-rescue 的分章文件发布到 Obsidian vault。

设计要点（对应 note-beautifier 的分册发布校验清单）：
- 命名只有一个真源：PUB[n]。生成侧与校验侧共用，禁止一处带 .md 一处不带。
- 发布是 (源文件, 重写表) 的纯函数；除显式登记的重写外不做任何内容改动。
- 写完做往返校验：把成品里的"发布性改动"逆向撤掉后必须与源逐字一致。
- 链接逐条断言目标存在；目标目录含外来文件则失败退出，不做 rm -rf。
"""

from __future__ import annotations

import pathlib
import re
import sys

SRC_DIR = pathlib.Path(__file__).parent / "chapters"
DEST = pathlib.Path(r"D:\Study-Notes\自建代理节点\CDN 拯救被墙节点")
VAULT = pathlib.Path(r"D:\Study-Notes")
SERIES = "CDN 拯救被墙节点"
TODAY = "2026-09-24"
NL = chr(10)

# 章号 -> 发布文件名（不含 .md）。唯一真源。
PUB: dict[int, str] = {
    0: "00 CDN 拯救被墙节点",
    1: "01 CDN 是什么",
    2: "02 为什么 CDN 能救被墙节点",
    3: "03 接入 Cloudflare 与域名解析",
    4: "04 把节点套上 CDN",
    5: "05 被墙判定与加速取舍",
    6: "06 排错速查",
}

SRC: dict[int, str] = {
    0: "00_导读.md",
    1: "01_CDN是什么.md",
    2: "02_为什么能救被墙.md",
    3: "03_接入Cloudflare.md",
    4: "04_套上CDN.md",
    5: "05_被墙判定与加速取舍.md",
    6: "06_排错速查.md",
}

H1: dict[int, str] = {
    0: "CDN 拯救被墙节点",
    1: "第 1 章 CDN 是什么",
    2: "第 2 章 为什么 CDN 能救被墙节点（原理与边界）",
    3: "第 3 章 接入 Cloudflare 与域名解析",
    4: "第 4 章 把节点套上 CDN（TLS / 端口 / WS）",
    5: "第 5 章 被墙判定与加速取舍",
    6: "第 6 章 排错速查",
}

TAGS = ["自建节点", "代理", "VPS", "CDN", "Cloudflare", "网络", "学习"]

# 跨文件指代改写成双链（正文级最小改动；同文件内的「见 4.4」保留为文字）
REWRITES: dict[int, list[tuple[str, str]]] = {
    0: [
        ("（见第二章 2.5）", "（见 [[02 为什么 CDN 能救被墙节点]] 2.5 节）"),
        ("靠第六章报错码速查", "靠 [[06 排错速查]]"),
    ],
    2: [
        ("退路是面板流第 9 章的分层排除与换 IP",
         "退路是 [[09 节点被墙的判定与换 IP（分厂商分操作）]] 的分层排除与换 IP"),
    ],
    3: [
        ("改 NS / 加记录属面板流第 7 章",
         "改 NS / 加记录属 [[07 搭建节点（带域名与 Cloudflare）]]"),
        ("正是第四章要接的那一半", "正是 [[04 把节点套上 CDN]] 要接的那一半"),
        ("与第二章的 domain fronting 无关",
         "与 [[02 为什么 CDN 能救被墙节点]] 的 domain fronting 无关"),
        ("第二章讲的 **domain fronting** 是另一种手法",
         "[[02 为什么 CDN 能救被墙节点]] 讲的 **domain fronting** 是另一种手法"),
    ],
    6: [
        ("回查第四章 4.1", "回查 [[04 把节点套上 CDN]] 4.1"),
        ("回到第五章做**分类排除**", "回到 [[05 被墙判定与加速取舍]] 做**分类排除**"),
    ],
}

INDEX_TOC = (
    "## 目录" + NL + NL
    + "- [[01 CDN 是什么]] — 缓存网络还是反向代理，一次请求怎么走到就近节点" + NL
    + "- [[02 为什么 CDN 能救被墙节点]] — 三层原理与边界：CDN 救不了什么" + NL
    + "- [[03 接入 Cloudflare 与域名解析]] — 免费版只有 NS 一条路，接入期风险与生效验证" + NL
    + "- [[04 把节点套上 CDN]] — 端口清单、TLS 五模式、WebSocket 与 443 复用" + NL
    + "- [[05 被墙判定与加速取舍]] — 分类依据与 false positive，套 CDN 是快是慢" + NL
    + "- [[06 排错速查]] — 525 / 526 / 413 / 524 / WS 断连的并列成因与排查次序" + NL + NL
)

INDEX_RELATED = (
    "## 相关" + NL + NL
    + "- [[自建代理节点 MOC]] — 本目录的分类索引" + NL
    + "- [[00 VPS 自建节点零基础全流程]] — 同系列前置：零基础面板流全流程" + NL
)

NEXT_HINT_HEAD = "### 下一章预告"
NEXT_HINT_BODY = "在讲怎么救之前，先把 CDN 到底是什么讲清楚——否则「套 CDN」会变成一个凭感觉动手的操作。"

FM_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def body_of(text: str) -> str:
    """取 frontmatter 之后的正文（不含其后的空行），供往返校验逐字比对。"""
    m = FM_RE.match(text)
    return text[m.end():].lstrip(NL) if m else text


def strip_old_footer(body: str) -> tuple[str, int]:
    """去掉源章末的旧页脚导航（含其上的 --- 分隔线）。"""
    lines = body.rstrip(NL).split(NL)
    removed = 0
    if lines and lines[-1].startswith("> 上一篇："):
        lines.pop()
        removed += 1
    while lines and lines[-1].strip() == "":
        lines.pop()
    if lines and lines[-1].strip() == "---":
        lines.pop()
        removed += 1
    while lines and lines[-1].strip() == "":
        lines.pop()
    return NL.join(lines) + NL, removed


def new_footer(n: int) -> str:
    prev = "—" if n == 1 else f"[[{PUB[n - 1]}]]"
    nxt = "—" if n == 6 else f"[[{PUB[n + 1]}]]"
    return NL + "---" + NL + NL + f"> 上一篇：{prev} ｜ 返回索引：[[{PUB[0]}]] ｜ 下一篇：{nxt}" + NL


def frontmatter(n: int) -> str:
    title = H1[n] if n else SERIES
    out = ["---", f'title: "{title}"', "tags:"]
    out += [f"  - {t}" for t in TAGS]
    out += [f"created: {TODAY}", f"updated: {TODAY}", "status: 完成",
            "source_project: vps-node-cdn-rescue"]
    if n:
        out.append(f"chapter: {n}")
    out += ["---", ""]
    return NL.join(out) + NL


def main() -> int:
    if DEST.exists():
        foreign = [p.name for p in DEST.iterdir() if p.stem not in PUB.values()]
        if foreign:
            print(f"FAIL 目标目录含非本脚本产物，拒绝写入：{foreign}", file=sys.stderr)
            return 1
    else:
        DEST.mkdir(parents=True)

    plan: dict[int, dict] = {}
    for n in sorted(PUB):
        src_body = body_of((SRC_DIR / SRC[n]).read_text(encoding="utf-8"))
        body, removed = strip_old_footer(src_body)

        nrew = 0
        for old, new in REWRITES.get(n, []):
            c = body.count(old)
            if c != 1:
                print(f"FAIL 章 {n}: 重写串命中 {c} 次（期望 1）：{old[:40]}", file=sys.stderr)
                return 1
            body = body.replace(old, new)
            nrew += c

        # 往返校验的基准 = 所有"发布性改动"之前的正文（重写已生效，页脚/索引尚未加）
        base = body

        # 索引文件：记录被替换掉的"下一章预告"块原样文本，供往返校验还原
        removed_hint = ""
        if n == 0:
            anchor = "## 0.1 "
            if body.count(anchor) != 1:
                print("FAIL 索引：找不到 0.1 锚点", file=sys.stderr)
                return 1
            body = body.replace(anchor, INDEX_TOC + anchor, 1)

            hint_block = NEXT_HINT_HEAD + NL + NL + NEXT_HINT_BODY + NL
            if body.count(hint_block) != 1:
                print(f"FAIL 索引：下一章预告块命中 {body.count(hint_block)} 次", file=sys.stderr)
                return 1
            body = body.replace(hint_block, INDEX_RELATED, 1)
            removed_hint = hint_block

            if body.count("### 本章小结") != 1:
                print("FAIL 索引：本章小结命中数不为 1", file=sys.stderr)
                return 1
            body = body.replace("### 本章小结", "### 导读小结", 1)
            body = body.rstrip(NL) + NL
        else:
            body = body.rstrip(NL) + NL + new_footer(n)

        plan[n] = {"text": frontmatter(n) + body, "src_x": base,
                   "removed": removed, "rewrites": nrew, "hint": removed_hint}

    for n, item in plan.items():
        (DEST / f"{PUB[n]}.md").write_text(item["text"], encoding="utf-8", newline=NL)

    # 往返校验：撤销发布性改动后必须与源逐字一致
    ok = True
    for n, item in plan.items():
        full = (DEST / f"{PUB[n]}.md").read_text(encoding="utf-8")
        b = body_of(full)
        if n == 0:
            if INDEX_TOC not in b or INDEX_RELATED not in b:
                print(f"FAIL 章 {n} 索引附加块缺失")
                ok = False
            b = b.replace(INDEX_TOC, "", 1)
            b = b.replace(INDEX_RELATED.rstrip(NL), item["hint"].rstrip(NL), 1)
            b = b.replace("### 导读小结", "### 本章小结", 1)
        else:
            b = b.replace(new_footer(n), "", 1)
        if b.rstrip(NL) != item["src_x"].rstrip(NL):
            print(f"FAIL 章 {n} 往返不一致：撤销发布性改动后与源不符")
            ok = False
        if re.search(r"\[\[0[0-9]_", full):
            print(f"FAIL 章 {n} 残留旧式链接")
            ok = False
        if "`[[" in full:
            # 反引号里的 wikilink 在 Obsidian 中渲染成字面量，链接校验抓不到
            print(f"FAIL 章 {n} 存在反引号包住的 wikilink（渲染不出链接）")
            ok = False

    # 链接校验：文件链接目标必须存在；带锚点的标题必须存在于目标文件
    files = {p.stem for p in DEST.glob("*.md")}
    for n in plan:
        txt = (DEST / f"{PUB[n]}.md").read_text(encoding="utf-8")
        for m in re.finditer(r"\[\[([^\]]+)\]\]", txt):
            tgt = m.group(1)
            if tgt.startswith("#"):
                continue
            note, _, head = tgt.partition("#")
            note = note.split("|")[0].strip()
            if note in files:
                if head:
                    t = (DEST / f"{note}.md").read_text(encoding="utf-8")
                    heads = {re.sub(r"^#+\s*", "", l).strip()
                             for l in t.split(NL) if l.startswith("#")}
                    if head not in heads:
                        print(f"FAIL 章 {n} 锚点不存在：[[{tgt}]]")
                        ok = False
                continue
            if not list(VAULT.rglob(f"{note}.md")):
                print(f"FAIL 章 {n} 链接目标不存在：[[{tgt}]]")
                ok = False

    print(f"发布到：{DEST}")
    for n in sorted(plan):
        b = body_of(plan[n]["text"])
        cn = len(re.findall(r"[\u4e00-\u9fff]", b))
        print(f"  {PUB[n]}.md  {cn} 汉字  去旧页脚 {plan[n]['removed']} 行  重写 {plan[n]['rewrites']} 处")
    print("ASSERT_OK" if ok else "ASSERT_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
