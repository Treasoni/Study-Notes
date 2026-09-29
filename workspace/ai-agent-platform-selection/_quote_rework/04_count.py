# -*- coding: utf-8 -*-
"""步骤 4：预检（只算不写）。

把 `03_trans.py` 的替换表 + `rework_core.py` 的引擎在内存里跑一遍，报出：

1. 每个 `TRANS` 键在哪些文件里以 span 形态命中了几次（0 次 = 键写错，报错）。
2. 每个 `FIXES` 条目的实际命中次数 vs 期望次数（对不上 = 报错）。
3. `TITLE_FIX` 旧标题在每个目标文件里的命中次数 vs 期望（对不上 = 报错）。
4. 每章「引文对照」表行数，以及出处解析不出来的行数（不报错，供人工看）。
5. 改完之后正文里还剩哪些英文（沿用 02_plan 的扫描口径），确认没有漏翻。

产出：_quote_rework/count_report.md
不产出：任何笔记文件。
"""
import re
import sys
import collections
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

trans = core.load_trans()
bad_table = core.validate_trans(trans)
stats, results = core.run(trans, write_files=False)

rep = []
w = rep.append

# ---------------------------------------------------------------- 0. 替换表自检
w("# 预检报告（只算不写）\n")
w("替换表自检问题：%d 条。\n" % len(bad_table))
for what, k in bad_table:
    w("- %s：`%s`\n" % (what, k[:80]))

# ---------------------------------------------------------------- 1. TRANS 命中
miss = [k for k in trans.TRANS if stats["span"].get(k, {}).get("n", 0) == 0]
w("# 预检报告（只算不写）\n")
w("TRANS 键 %d 个；未命中 %d 个。\n" % (len(trans.TRANS), len(miss)))
w("\n## 1. TRANS span 命中\n")
w("\n| 键（截断 60） | 次数 | 命中文件 |\n| --- | --- | --- |\n")
for k in trans.TRANS:
    d = stats["span"].get(k, {"n": 0, "tags": []})
    w("| `%s` | %d | %s |\n" % (k[:60].replace("|", "\\|"), d["n"], ", ".join(d["tags"])))

# ---------------------------------------------------------------- 2. FIXES
bad_fix = []
w("\n## 2. FIXES 命中（期望 / 实际）\n")
w("\n| 旧串（截断 50） | 期望 | 实际 | 文件 |\n| --- | --- | --- | --- |\n")
for old, _new, want in trans.FIXES:
    d = stats["fix"].get(old, {"want": want, "got": 0, "tags": []})
    flag = "" if (want == 0 or want == d["got"]) else " ❌"
    if flag:
        bad_fix.append((old, want, d["got"]))
    w("| `%s` | %d | %d%s | %s |\n"
      % (old[:50].replace("|", "\\|"), want, d["got"], flag, ", ".join(d["tags"])))

# ---------------------------------------------------------------- 3. 标题
bad_title = []
w("\n## 3. TITLE_FIX 命中（期望 / 实际）\n")
w("\n| 文件 | 期望 | 实际 |\n| --- | --- | --- |\n")
for name, want in core.TITLE_EXPECT.items():
    got = stats["title"].get(name, 0)
    flag = "" if want == got else " ❌"
    if flag:
        bad_title.append((name, want, got))
    w("| %s | %d | %d |%s\n" % (name, want, got, flag))

# ---------------------------------------------------------------- 4. 附录
w("\n## 4. 每章「引文对照」表行数（未解析出处 %d 行）\n" % stats["src_missing"])
w("\n| 文件 | " + " | ".join("第 %d 章" % c for c in range(1, 8)) + " |\n")
w("| --- |" + " --- |" * 7 + "\n")
for path, _kind in core.TARGETS:
    d = stats["appendix"].get(path.name, {})
    w("| %s | %s |\n" % (path.name, " | ".join(str(d.get(c, 0)) for c in range(1, 8))))

# ---------------------------------------------------------------- 5. 残留英文
RUN = re.compile(r"[A-Za-z][A-Za-z0-9'’./+-]*(?:[ \t]+[A-Za-z][A-Za-z0-9'’./+-]*)+")
w("\n## 5. 改完之后正文里剩下的英文串（>= 2 词，已排除反引号 span 内的 cite）\n")
w("\n| 文件 | 串 | 次数 |\n| --- | --- | --- |\n")
for path, _kind in core.TARGETS:
    if path.name in ("自托管 Agent 平台选型.md", "final_note.md"):
        lines, _eol = results[str(path)]
        cnt = collections.OrderedDict()
        for l in lines:
            bare = l
            for a, b, s, _k in reversed(core.spans(l)):
                bare = bare[:a] + " " + bare[b:]
            for m in RUN.finditer(bare):
                cnt[m.group(0)] = cnt.get(m.group(0), 0) + 1
        for s, n in sorted(cnt.items(), key=lambda x: -x[1]):
            w("| %s | %s | %d |\n" % (path.name, s, n))

(HERE / "count_report.md").write_bytes("".join(rep).encode("utf-8"))

print("table=%d TRANS keys=%d missed=%d | FIXES mismatch=%d | TITLE mismatch=%d | src missing=%d"
      % (len(bad_table), len(trans.TRANS), len(miss), len(bad_fix), len(bad_title),
         stats["src_missing"]))
for old, want, got in bad_fix:
    print("  FIX  %r want=%d got=%d" % (old[:60], want, got))
sys.exit(1 if (bad_table or miss or bad_fix or bad_title) else 0)
