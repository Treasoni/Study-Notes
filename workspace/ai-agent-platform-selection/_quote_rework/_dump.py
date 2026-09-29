# -*- coding: utf-8 -*-
"""一次性诊断：把「替换后」的落地文本里带这几个词的整行 repr 打出来。
用来订正 FIXES 里那两条没命中的旧串（它们是在 FIXES 前序条目改过之后才存在的形态）。"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

trans = core.load_trans()
_stats, results = core.run(trans, write_files=False)

NEEDLES = ["因为一个实例要同时扛", "复用同一个", "首次安装向导"]
out = []
for name in ("05_Octop回答的是不是另一个问题.md", "06_谁把谁当参照.md"):
    path = str(core.CH_DIR / name) if (core.CH_DIR / name).exists() else None
    for k, (lines, _eol) in results.items():
        if pathlib.Path(k).name != name:
            continue
        out.append("=== %s（替换后）" % name)
        for n, l in enumerate(lines, 1):
            if any(x in l for x in NEEDLES):
                out.append("  %d| %r" % (n, l))
        out.append("")

(HERE / "_dump.txt").write_bytes(("\n".join(out) + "\n").encode("utf-8"))
print("_dump.txt written")
