# -*- coding: utf-8 -*-
"""诊断：`02_deep_research.md` 里那 8 处 weak 命中，是**中间件引错**还是**校验器误报**？

对每条 weak 引文，在语料里找「归一化后 LCS 最长」的文件，打印：
  · 覆盖率 = LCS / 引文长度 —— 接近 1 说明只是标记差异（误报）；明显 < 1 说明中间件改过字
  · 该文件里最接近的那一段——人工一眼可判
"""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path("D:/Study-Notes/.codex/scripts")))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "cc", "D:/Study-Notes/.codex/scripts/note-citation-check.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

PROJ = pathlib.Path("D:/Study-Notes/workspace/ai-agent-platform-selection")
out = []
primary, derived = cc.collect_corpus(PROJ, [])
pn = [(n, cc.corpus_norm(t)) for n, t in primary]
probe = PROJ / "02_deep_research.md"
for i, line in enumerate(cc.read_text(probe).splitlines(), 1):
    for q, kind in cc.quotes_in_line(line):
        qs = q.strip()
        if cc.CITE_PATH.match(qs) or cc.CITE_NUM_ARTIFACT.match(qs) or cc.CITE_FULL.match(qs):
            continue
        for seg in cc.verbatim_segments(q):
            nq = cc.norm(seg)
            if nq in cc.corpus_norm("\n".join(t for _n, t in primary)):
                continue
            best = (0, "", "")
            for n, t in pn:
                m = cc.lcs(nq, t)
                if m[0] > best[0]:
                    j = t.find(m[1])
                    best = (m[0], n, t[max(0, j - 60):j + len(m[1]) + 60])
            cov = best[0] / max(1, len(nq))
            out.append("L%-4d 长度=%-4d 覆盖率=%.2f  %s\n     引文: %s\n     语料: %s   [%s]"
                       % (i, len(nq), cov, "", seg[:160], best[2][:200], best[1]))

pathlib.Path("D:/Study-Notes/workspace/_weak_diag.txt").write_bytes(
    ("\n\n".join(out) + "\n").encode("utf-8"))
print("wrote %d entries" % len(out))
