# -*- coding: utf-8 -*-
"""给 .learnings/RULES.md 的 Do 区补一条「引文语言」偏好。

行尾照原样保留（read_bytes/write_bytes）。插入点取 `## Don't` 之前 ——
Do 区的最后一条，紧跟语义相邻的「官方引文摆放」那条。
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = pathlib.Path("D:/Study-Notes/.learnings/RULES.md")
raw = P.read_bytes()
crlf = b"\r\n" in raw
t = raw.decode("utf-8")
t = t.replace("\r\n", "\n") if crlf else t
print("行尾:", "CRLF" if crlf else "LF", "| 字节:", len(raw))

ANCHOR = "\n## Don't"
assert t.count(ANCHOR) == 1, "锚点命中 %d 次" % t.count(ANCHOR)

RULE = (
    "- **引文语言**：笔记正文里的**成句英文引文**给中译，"
    "**代码 / 命令 / 配置键 / 路径 / 文件名 / 产品名 / 单个技术术语**保留原文"
    "（用户明确要求：「那个英文我不是很想看，我更想直接看中文」）。"
    "只换不留档不行：逐字原文要另存到章末「引文对照（原文 / 中译 / 出处）」表，"
    "否则引用链断掉、读者无法回源核对。译完必须复查两件事——原文是英文时都看不出来："
    "① 引导语 / 括注与中译**撞车**（变成了同一句话。判据：两者最长公共汉字子串 ≥ 5；"
    "改法：引导语缩成话题标签，或把括注里那截中译删掉只留出处）"
    "② 「出处」列有没有把正文列举的**产品文件名**（`SOUL.md`、`MEMORY.md`）当来源——"
    "**错的出处比空着更糟**，查不到就写 `—` 并在表格引导句里说明 `—` 的含义"
)

t = t.replace(ANCHOR, "\n" + RULE + ANCHOR, 1)
out = t.encode("utf-8") if not crlf else t.replace("\n", "\r\n").encode("utf-8")
P.write_bytes(out)
print("写入:", len(out), "字节 | 行尾:", "CRLF" if b"\r\n" in out else "LF")
