# -*- coding: utf-8 -*-
"""落盘后的独立校验：不依赖 04/05 的中间结论，直接读成品文件。

校验项见 06_verify.py 的 CHECKS 说明；结果写 verify_report.md。
基线提交 6520105c 是 vault 自动备份在我落盘前的最后一次快照，
用它来证明 pristine/ 确实是「改动前」而不是「改动后又被拷了一次」。
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

BASE = "6520105c"
pr = core.PRISTINE
CH = [p for p, k in core.TARGETS if k == "chapter"]
MULTI = [p for p, k in core.TARGETS if k in ("merged", "assembled")]
ALL = [p for p, _k in core.TARGETS] + core.TITLE_ONLY
out, fails = [], []


def bad(msg):
    fails.append(msg)
    out.append("  ❌ " + msg)


def read_now(p):
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")


out.append("# 落盘校验报告")
out.append("")
out.append("基线提交：`%s`（vault 自动备份在我落盘前的最后一次快照）" % BASE)
out.append("")

# —— A. 回滚点是「改动前」 ——
out.append("## A. 回滚点是否等于改动前状态")
for p in ALL:
    base = subprocess.run(["git", "show", "%s:%s" % (BASE, p.relative_to(core.ROOT)
                                                     .as_posix())],
                          cwd=str(core.ROOT), capture_output=True).stdout
    base = base.decode("utf-8").replace("\r\n", "\n")
    bak = (pr / p.name).read_bytes().decode("utf-8").replace("\r\n", "\n")
    if base != bak:
        bad("%s 的 pristine 与基线提交不一致" % p.name)
out.append("  %s 11 个文件的 pristine 均等于基线提交（逐字符，行尾归一后）"
           % ("✅" if not [f for f in fails] else "见上"))

# —— B. 行尾保留 ——
out.append("")
out.append("## B. 行尾保留")
for p in ALL:
    e1 = "CRLF" if b"\r\n" in (pr / p.name).read_bytes() else "LF"
    e2 = "CRLF" if b"\r\n" in p.read_bytes() else "LF"
    mark = "✅" if e1 == e2 else "❌"
    if e1 != e2:
        bad("%s 行尾从 %s 变成了 %s" % (p.name, e1, e2))
    out.append("  %s %-38s %s" % (mark, p.name, e2))

# —— C. 附录结构 ——
EXPECT = [28, 24, 13, 15, 17, 26, 5]      # 去重后的行数（同一引文一章只列一行）
out.append("")
out.append("## C. 附录表结构（每章行数 / 每行管道数 / 原文列是否带反引号）")


def appendix_rows(lines):
    """→ [[row,...], ...]，按「引文对照」标题切出每张表的正文行。"""
    tabs, i = [], 0
    while i < len(lines):
        if core.APPENDIX_TITLE in lines[i]:
            rows = []
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("|"):
                    rows.append(lines[j])
                elif rows:
                    break
            tabs.append(rows)
            i = j
        i += 1
    return tabs


for p in ALL:
    if p in core.TITLE_ONLY:
        continue
    tabs = appendix_rows(read_now(p))
    kind = dict(core.TARGETS)[p]
    if kind == "chapter":
        tabs = [tabs[0]] if tabs else []
    got = [len(t) - 2 for t in tabs]          # 减去表头两行
    want = EXPECT[:len(tabs)] if kind != "chapter" else [EXPECT[CH.index(p)]]
    if got != want:
        bad("%s 附录行数 %s != 期望 %s" % (p.name, got, want))
    npipe = 0
    for t in tabs:
        for r in t:
            if r.count("|") != 5:
                npipe += 1
    if npipe:
        bad("%s 有 %d 行管道数 != 5（表格会被撕裂）" % (p.name, npipe))
    out.append("  ✅ %-38s 附录 %s 行，管道数全部为 5" % (p.name, got))

# —— D. 标题翻译 ——
out.append("")
out.append("## D. 第 4 章标题翻译")
old, new = core.load_trans().TITLE_FIX
for p in ALL:
    t = (p.read_bytes().decode("utf-8"))
    n_old, n_new = t.count(old), t.count(new)
    want = core.TITLE_EXPECT.get(p.name, 0)
    if n_old or n_new != want:
        bad("%s 旧标题残留 %d / 新标题 %d（期望 %d）" % (p.name, n_old, n_new, want))
    out.append("  ✅ %-38s 旧 0 / 新 %d" % (p.name, n_new))

# —— E. 残留英文散文 ——
out.append("")
out.append("## E. 正文残留的英文（≥2 个 ASCII 词的串，排除 wikilink 与表格原文列）")
EN = re.compile(r"\b[A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){1,}\b")
resid = {}
for p in [x for x in ALL if x not in core.TITLE_ONLY]:
    hits = []
    lines = read_now(p)
    in_appendix = False
    for n, l in enumerate(lines, 1):
        if core.APPENDIX_TITLE in l:
            in_appendix = True
        if in_appendix:
            continue
        if l.startswith("- [[") or "]]" in l and l.startswith("-"):
            continue
        stripped = re.sub(r"`[^`]*`", " ", l)
        for m in EN.finditer(stripped):
            hits.append(m.group(0))
    resid[p.name] = hits
    uniq = sorted(set(hits))
    out.append("  %s：%d 处，去重 %d 种" % (p.name, len(hits), len(uniq)))
    for u in uniq:
        out.append("      · %s" % u)

# —— F. 各章 4 份副本一致 ——
out.append("")
out.append("## F. 每章 4 份副本的附录表逐字一致")
for ch in range(1, 8):
    tabsets = {}
    tabsets["chapter:" + CH[ch - 1].name] = appendix_rows(read_now(CH[ch - 1]))[0]
    for p in MULTI:
        tabsets[p.name] = appendix_rows(read_now(p))[ch - 1]
    vals = {k: "\n".join(v) for k, v in tabsets.items()}
    if len(set(vals.values())) != 1:
        bad("ch%d 的 4 份副本附录表不一致" % ch)
    out.append("  ✅ ch%d %d 行，4 份副本逐字相同" % (ch, len(tabsets["chapter:" + CH[ch - 1].name]) - 2))

# —— G. callout ——
out.append("")
out.append("## G. 组装本的「关于引文」callout")
for p in MULTI:
    if dict(core.TARGETS)[p] != "assembled":
        continue
    t = p.read_bytes().decode("utf-8")
    n = t.count(core.CALLOUT[0])
    if n != 1:
        bad("%s callout 出现 %d 次（期望 1）" % (p.name, n))
    out.append("  ✅ %-38s callout %d 次" % (p.name, n))

# —— H. 「中文 空格 中文」 ——
out.append("")
out.append("## H. 夹在两个汉字之间的空格（英译中留下的空隙）")
GAP = re.compile(r"[一-鿿][ \t]+[一-鿿]")
LABEL = re.compile(r"第 [0-9]+ [章层]$")
gap_bad = 0
for p in [x for x in ALL if x not in core.TITLE_ONLY]:
    for n, l in enumerate(read_now(p), 1):
        for m in GAP.finditer(l):
            if LABEL.search(l[:m.start() + 1]):
                continue        # 「第 1 层 本地 CLI 阵营」这类刻意的标签空格
            gap_bad += 1
            bad("%s:%d 汉字之间有空隙：…%s…" % (p.name, n, l[max(0, m.start() - 12):m.end() + 8]))
if not gap_bad:
    out.append("  ✅ 除「第 N 章/层 」这种刻意的标签空格外，没有其它汉字间空格")

out.append("")
out.append("---")
out.append("")
out.append("## 总判定")
out.append("")
if fails:
    out.append("**❌ 有 %d 项不合格**" % len(fails))
    for f in fails:
        out.append("- %s" % f)
else:
    out.append("**✅ 全部通过**")

(HERE / "verify_report.md").write_bytes(("\n".join(out) + "\n").encode("utf-8"))
print("verify_report.md ->", "FAIL %d" % len(fails) if fails else "ALL OK")
for f in fails:
    print("  ", f.encode("ascii", "replace").decode("ascii"))
