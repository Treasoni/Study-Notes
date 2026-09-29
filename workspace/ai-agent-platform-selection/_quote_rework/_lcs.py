# -*- coding: utf-8 -*-
"""诊断（非校验）：找「引导语被紧随的引文原样复述」的重复。

上一版的判据是 2-gram 重叠占比，长引文会把占比稀释掉——`密钥默认不迁：`
后面跟着一条长引文，重复明明在，占比却算不到阈值。改成看**最长公共子串**：
引导语尾部（去掉前面几条出处后）与引文的中译之间，连续相同的汉字 >= 5 个
就是可疑。判据只负责把候选挑出来给人看，好不好由人判断（标签式引导语
「目前分级管的是什么：」+ 长引文是本文有意的写法，不算缺陷）。
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

CJK = re.compile(r"[一-鿿]")
NOTE = core.VAULT_NOTE
lines = NOTE.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")


def lcs(a, b):
    """最长公共子串长度。a、b 都只有汉字。"""
    if not a or not b:
        return 0, ""
    prev = [0] * (len(b) + 1)
    best = (0, 0, 0)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best[0]:
                    best = (cur[j], i - cur[j], i)
        prev = cur
    n, s, e = best
    return n, a[s:e]


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
    for a, b, _s, _k in reversed(core.spans(l)):
        quote = "".join(CJK.findall(l[a + 1:b - 1]))
        if len(quote) < 5:
            continue
        lead = "".join(CJK.findall(l[max(0, a - 60):a].split("`")[-1]))
        if len(lead) < 5:
            continue
        k, sub = lcs(lead, quote)
        if k >= 4:
            hits += 1
            out.append("%4d  公共子串 %d「%s」" % (n, k, sub))
            out.append("        引导语: %s" % lead[-30:])
            out.append("        引文  : %s" % quote[:60])
            out.append("")

(HERE / "_lcs.txt").write_bytes(
    ("# 引导语被引文原样复述（最长公共汉字子串 >= 5）\n共 %d 条\n\n\n%s"
     % (hits, "\n".join(out))).encode("utf-8"))
print("_lcs.txt ->", hits)
