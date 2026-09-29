# -*- coding: utf-8 -*-
"""定位单条 weak 引文在语料里的**断点**（只查一个已知文件，秒级）。"""
import importlib.util
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
spec = importlib.util.spec_from_file_location(
    "cc", "D:/Study-Notes/.codex/scripts/note-citation-check.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

PROJ = pathlib.Path("D:/Study-Notes/workspace/ai-agent-platform-selection")
QUOTE = ("orchestrates the observe-reason-act-feedback cycle, including step scheduling, "
         "stopping criteria, retries, reflection, delegation, handoffs, and multi-agent "
         "coordination. In multi-model settings, ℒ additionally implements model routing "
         "and role assignment.")
corpus = cc.corpus_norm(cc.read_text(PROJ / "research/framework/13_arxiv_2606.20683v1_fulltext.md"))
nq = cc.norm(QUOTE)
print("笔记侧长度 %d" % len(nq))
print(nq)
print()
# 逐字符找最长可匹配前缀
lo, hi = 0, len(nq)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if nq[:mid] in corpus:
        lo = mid
    else:
        hi = mid - 1
print("最长可匹配前缀 = %d 字符" % lo)
print("断点处：笔记侧 ...%r || %r..." % (nq[max(0, lo - 40):lo], nq[lo:lo + 40]))
j = corpus.find(nq[max(0, lo - 40):lo])
print("语料侧对应：        ...%r" % corpus[j:j + 90])
