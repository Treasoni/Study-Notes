# -*- coding: utf-8 -*-
"""诊断：附录「出处」里那些**没有斜杠也没有行号**的裸文件名，都是什么。

背景：`cite_kind` 把任何 `X.md` 形态的反引号 span 都当出处，于是正文里
「要迁移的产品文件」也被当成了来源——第 6 章「迁移内容清单（README）：
`SOUL.md` / `记忆`（MEMORY.md + USER.md）/ …」这一行，`SOUL.md` 后面的
8 条引文全都把出处标成了 `SOUL.md`。这是**错**的出处，比空着更糟。

本脚本只列不判：把所有裸文件名出处按出现次数排出来，看全库有多少、
哪些是真的来源件（`02_deep_research.md` 这种），哪些是产品文件名。
"""
import pathlib
import re
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

# 直接扫 pristine 正文 + 现成的成品附录，两处都看
NAME_ONLY = re.compile(r"^[A-Za-z0-9_\-]+\.md$")

src_ctr = Counter()
span_ctr = Counter()
span_where = {}
for path, _k in core.TARGETS:
    lines, _eol = core.read(path)
    inap = False
    for n, l in enumerate(lines, 1):
        if core.APPENDIX_TITLE in l:
            inap = True
        if inap:
            if l.startswith("## ") and core.APPENDIX_TITLE not in l:
                inap = False
            else:
                cells = [c.strip() for c in l.split("|")]
                if len(cells) == 6:      # | N | 原文 | 中译 | 出处 |
                    src_ctr[cells[4].strip("`")] += 1
                continue
        for a, b, s, _k in core.spans(l):
            if NAME_ONLY.match(s):
                span_ctr[s] += 1
                span_where.setdefault(s, []).append("%s:%d" % (path.name, n))

out = ["# 附录「出处」列的全部取值（去重、按次数）", ""]
for t, c in src_ctr.most_common():
    out.append("%-64s %3d 次" % (t, c))
out += ["", "合计 %d 种、%d 次" % (len(src_ctr), sum(src_ctr.values())), "",
        "# 正文里所有裸文件名 span（判断哪些是来源件、哪些是产品文件名）", ""]
for t, c in span_ctr.most_common():
    out.append("%-28s %3d 次   例：%s" % (t, c, span_where[t][0]))
out.append("")
out.append("# 上表里**全小写**的（本项目来源件命名习惯）")
for t, c in span_ctr.most_common():
    if t == t.lower():
        out.append("    小写  %-24s %d 次" % (t, c))
out.append("")
out.append("# 上表里**含大写**的（产品/内容文件名，不该当出处）")
for t, c in span_ctr.most_common():
    if t != t.lower():
        out.append("    含大写 %-23s %d 次" % (t, c))

(HERE / "_bare.txt").write_bytes(("\n".join(out) + "\n").encode("utf-8"))
print("_bare.txt ok")
