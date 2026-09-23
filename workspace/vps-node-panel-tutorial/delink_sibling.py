#!/usr/bin/env python3
"""按用户决策 [2] 处理：既有笔记《自建代理节点搭建实战》已被用户有意删除。

- 把本篇中指向它的 7 处双链改为纯文本提及（不再产生死链）；
- 附录 B 由「与既有笔记的分工与互链」改写为「本篇的内容边界」。

每处替换都断言命中次数，末尾打印「本次改动 N 处」。
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LINK_A = "[[自建代理节点搭建实战]]"
LINK_B = "[[自建代理节点/自建代理节点搭建实战.md]]"

EDITS = [
    ("chapters/01-what-is-vps.md", [
        ("### 与既有笔记的分工", "### 本篇的内容边界"),
        (
            '传输分层模型、REALITY 原理、手写 Xray JSON、nftables / suricata 深度加固这些内容，'
            f'已经在 {LINK_A} 里写过，本篇只做指引与双链，不重复展开。',
            '传输分层模型、REALITY 原理、手写 Xray JSON、nftables / suricata 深度加固这些内容'
            '属于「内核直配」范畴，超出本篇范围，本篇只做指引、不展开。',
        ),
    ]),
    ("chapters/05-install-panel.md", [
        (
            f'想在面板之外理解内核层原理（手写 Xray JSON、REALITY 等），可对照 {LINK_B}。',
            '内核层原理（手写 Xray JSON、REALITY 等）属于内核直配范畴，超出本篇范围，不展开。',
        ),
    ]),
    ("chapters/07-domain-cloudflare.md", [
        (
            f'若后续需要内核级配置（手写 Xray JSON、REALITY 原理），本篇只做指引，见 {LINK_B}。',
            '若后续需要内核级配置（手写 Xray JSON、REALITY 原理），那属于内核直配范畴，超出本篇范围。',
        ),
    ]),
    ("chapters/10-security.md", [
        (
            f'**超出本篇范围的深度加固**：`nftables` / `suricata` 级别的防火墙与入侵检测、内核直配、'
            f'传输层前沿方案的原理，请在既有笔记中展开，本篇只做指引与双链：{LINK_A}。',
            '**超出本篇范围的深度加固**：`nftables` / `suricata` 级别的防火墙与入侵检测、内核直配、'
            '传输层前沿方案的原理，超出本篇范围，本篇只做指引、不展开。',
        ),
    ]),
]

APPENDIX_OLD_HEAD = "## 附录 B：与《自建代理节点搭建实战》的分工与互链"
APPENDIX_NEW = """## 附录 B：本篇的内容边界

本篇（面板流）只覆盖一条主线：**买回来 → 点选跑通**，把变量压到最少，让零基础读者一次成功。
以下三类内容属于「内核直配」范畴，超出本篇范围，本篇只做指引、不展开：

| 内容 | 范畴 | 本篇的处置 |
|---|---|---|
| 手写 Xray JSON 配置 | 内核直配 | 不展开 |
| REALITY 原理 | 传输层原理 | 不展开 |
| `nftables` / `suricata` 深度加固 | 系统级加固 | 不展开 |

需要这些内容时，按上表关键词检索对应官方文档（Xray-core 官方文档、`nftables` 与 `suricata` 官方手册）。

索引层：本篇收录在 [[自建代理节点 MOC]] 的「节点搭建」分组下。"""


def fail(msg):
    print(f"DELINK-FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    total = 0
    for rel, pairs in EDITS:
        p = os.path.join(ROOT, rel)
        t = io.open(p, encoding="utf-8").read()
        n = 0
        for old, new in pairs:
            c = t.count(old)
            if c != 1:
                fail(f"{rel}: 期望命中 1 次，实际 {c} 次 -> {old[:60]!r}")
            t = t.replace(old, new)
            n += 1
        io.open(p, "w", encoding="utf-8", newline="").write(t)
        print(f"{rel}: 改动 {n} 处")
        total += n

    # 附录 B 整块替换
    p = os.path.join(ROOT, "chapters/11-appendix.md")
    t = io.open(p, encoding="utf-8").read()
    i = t.find(APPENDIX_OLD_HEAD)
    if i < 0:
        fail("附录 B 原标题未找到")
    if t.count(APPENDIX_OLD_HEAD) != 1:
        fail("附录 B 原标题出现多次")
    new_t = t[:i] + APPENDIX_NEW + "\n"
    io.open(p, "w", encoding="utf-8", newline="").write(new_t)
    print("chapters/11-appendix.md: 附录 B 整块改写 1 处")
    total += 1

    # 残留检查
    for rel, _, _ in [(r, 0, 0) for r, _ in EDITS] + [("chapters/11-appendix.md", 0, 0)]:
        body = io.open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for lk in (LINK_A, LINK_B):
            if lk in body:
                fail(f"{rel} 仍残留 {lk}")

    print(f"\n本次改动 {total} 处")


if __name__ == "__main__":
    main()
