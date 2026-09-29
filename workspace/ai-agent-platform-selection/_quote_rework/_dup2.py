# -*- coding: utf-8 -*-
"""补充诊断：_lcs.py 只覆盖「中译汉字 >= 5」的长引文。

短引文（中译只有 1-4 个汉字，如 `约 1,300 token`）不在覆盖范围内，会漏掉
「合计约 `约 1,300 token`」这种**边界处叠字**。这里换一个窄判据：

  引文译文里**第一个汉字** == 引文之前**最后一个汉字**（跳过标点/空白）
  → 一个词被写了两遍

窄判据误报少（不会把「的」这种高频字算进来，因为要求它紧贴 span 边界、
且是译文的首字）。输出到 _dup2.txt。
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as C  # noqa: E402

trans = C.load_trans()
# 原文件里 span 是英文（键），落盘后 span 是中文（值）。两态都要能跑，
# 所以建一张「值 -> 键」反查表。
REV = {v: k for k, v in trans.TRANS.items()}
CJK = re.compile(r"[一-鿿]")
PUNCT = "，。：；、 「」（）、——…！？,.:;()\"'"


def cjk_only(s):
    return "".join(CJK.findall(s))


def last_cjk_before(line, pos):
    for i in range(pos - 1, -1, -1):
        ch = line[i]
        if CJK.match(ch):
            return ch, i
        if ch not in PUNCT and not ch.isspace():
            return None, -1      # 中间夹了英文/反引号/数字，不是紧邻
    return None, -1


hits = []
for path, _kind in C.TARGETS:
    lines, _eol = C.read(path)
    for n, line in enumerate(lines, 1):
        if "`" not in line:
            continue
        for a, b, s, _k in C.spans(line):
            if s in trans.TRANS:
                zh = cjk_only(trans.TRANS[s])
            elif s in REV:
                zh = cjk_only(s)          # 已落盘：span 本身就是中译
            else:
                continue
            if not zh:
                continue
            prev, pi = last_cjk_before(line, a)
            if prev and prev == zh[0]:
                hits.append((path.name, n, prev, line[max(0, a - 40):b + 10]))

out = ["# 边界叠字候选（译文首字 == 紧邻其前的末字）", ""]
for tag, n, ch, ctx in hits:
    out.append("- [%s:%d] 叠字「%s」  %s" % (tag, n, ch, ctx.strip()))
out.append("")
out.append("合计 %d 处" % len(hits))
(HERE / "_dup2.txt").write_bytes("\n".join(out).encode("utf-8"))
print("候选 %d 处 -> _dup2.txt" % len(hits))
