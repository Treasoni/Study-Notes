# -*- coding: utf-8 -*-
"""临时预览器：把内存里改好的成品落到 _preview/ 下供人眼逐段读，并列出
「出处没解析出来」的那些行。不碰任何笔记。用完可删。"""
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

trans = core.load_trans()
stats, results = core.run(trans, write_files=False)

OUT = HERE / "_preview"
OUT.mkdir(exist_ok=True)

for path, _kind in core.TARGETS:
    lines, _eol = results[str(path)]
    (OUT / path.name.replace("/", "_")).write_bytes(("\n".join(lines)).encode("utf-8"))

# 出处缺失的引文
miss = []
for path, kind in core.TARGETS:
    lines, _eol = core.read(path)
    lp = core.last_path_by_line(lines)
    for chap, start, stop in core.split_sections(lines, kind):
        for i in range(start, stop):
            prior = lp[i - 1] if i else None
            for a, b, s, _k in core.spans(lines[i]):
                if s in trans.TRANS and not core.cite_for(lines[i], a, b, prior):
                    miss.append("%s :%d ch%d  %s" % (path.name, i + 1, chap, s[:80]))
rows = ["# 出处未解析的引文（%d 条，含 4 份副本的重复）" % len(miss), ""] + \
       sorted(set(miss))
(OUT / "_no_src.txt").write_bytes(("\n".join(rows) + "\n").encode("utf-8"))
print("preview ->", OUT, "| no_src:", len(miss))
