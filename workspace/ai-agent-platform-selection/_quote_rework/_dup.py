# -*- coding: utf-8 -*-
"""诊断（非校验）：找「引导语已经把紧随引文的意思说了一遍」的重复。

判据：一行的某个反引号 span，其**中译**与 span 前 40 字以内的引导语尾部的
2-gram 重叠 >= 6，即认为引导语在复述引文。跳过附录区（附录本身就要对照）。
只报告，不判定失败——有的重复是有意的强调。
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

import re

CJK = re.compile(r"[一-鿿]")
NOTE = core.VAULT_NOTE
lines = NOTE.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")

out = []
inap = False
hits = 0
for n, l in enumerate(lines, 1):
    if core.APPENDIX_TITLE in l:
        inap = True
    if inap:
        if l.startswith("## ") and core.APPENDIX_TITLE not in l:
            inap = False
        else:
            continue
    t = l
    for a, b, _s, _k in reversed(core.spans(l)):
        quote = t[a + 1:b - 1] if len(t) > b else ""
        if not CJK.search(quote) or len(CJK.findall(quote)) < 8:
            continue                       # 出处路径之类的 span，不算引文
        lead = t[max(0, a - 60):a]
        lead = lead.split("`")[-1]         # 砍掉前面几条出处，只看本条引导语
        qs = "".join(CJK.findall(quote))
        ls = "".join(CJK.findall(lead))
        if len(ls) < 8:
            continue
        g = {qs[i:i + 2] for i in range(len(qs) - 1)}
        h = {ls[i:i + 2] for i in range(len(ls) - 1)}
        ov = len(g & h)
        ratio = ov / max(1, min(len(g), len(h)))
        if ov >= 5 and ratio >= 0.5:
            hits += 1
            out.append("重叠 %d（占比 %.2f）  行 %d" % (ov, ratio, n))
            out.append("   引导语尾: …%s" % ls[-40:])
            out.append("   引文    : %s" % qs[:80])
            out.append("")

(HERE / "_dup.txt").write_bytes(("# 引导语 vs 紧随引文重复（只比汉字 2-gram，跳过附录区）\n共 %d 条\n\n\n%s"
                                % (hits, "\n".join(out))).encode("utf-8"))
print("_dup.txt ->", hits)
