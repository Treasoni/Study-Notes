# -*- coding: utf-8 -*-
"""把方案 A 落到 11 个目标文件上（10 个笔记副本 + 03_outline.md 只改标题）。

跑之前必须先让 `04_count.py` 退出码为 0——它会把「有键没命中」「FIXES 次数
对不上」「标题对不上」「译文里有反引号或竖线」全部拦下。

回滚：所有目标文件在改动前逐字节复制到 `_quote_rework/pristine/`，
其中 README.txt 记着每个文件的行尾与字节数。要回滚就把 pristine 里的
文件按原名写回原路径（路径清单在 05_apply.py 的 TARGETS 里）。
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rework_core as core

trans = core.load_trans()

bad = core.validate_trans(trans)
if bad:
    print("译文数据不合法，已中止：")
    for what, key in bad:
        print("  - %s: %r" % (what, key))
    sys.exit(1)

# —— 0. 幂等闸：已经改过的文件不许再改一遍 ——
# 第二遍跑不会「什么都不做」：附录的「原文（逐字）」列本身就是英文，
# FIXES 里的字面替换会把它一起改掉，逐字原文就毁了。必须在写之前拦住。
# 用附录标题判、不用「关于引文」callout 判：callout 只加在组装本上，
# 分章文件没有，拿它当闸会让改过的分章文件溜过去。
already = [p.name for p, _k in core.TARGETS
           if core.APPENDIX_TITLE in p.read_bytes().decode("utf-8")]
if already:
    print("这些文件已经有了「%s」，说明本脚本已经跑过：" % core.APPENDIX_TITLE)
    for n in already:
        print("  - %s" % n)
    print("拒绝重复落盘。要重跑请先从 _quote_rework/pristine/ 回滚。")
    sys.exit(1)

# —— 1. 回滚点（只写一次，不覆盖已有的 pristine） ——
pristine = core.PRISTINE
pristine.mkdir(exist_ok=True)
manifest = []
for path, _kind in core.TARGETS + [(p, "title_only") for p in core.TITLE_ONLY]:
    raw = path.read_bytes()
    eol = "CRLF" if b"\r\n" in raw else "LF"
    dst = pristine / path.name
    if dst.exists():
        print("回滚点已存在，保持不动（不会用改后的内容覆盖原始备份）：%s" % dst.name)
    else:
        shutil.copyfile(path, dst)
    manifest.append("%-44s %-4s %7d bytes  %s"
                    % (path.name, eol, len(raw), path))
(core.PRISTINE / "README.txt").write_bytes(
    ("改动前逐字节备份（%d 个文件）\n\n" % len(manifest) + "\n".join(manifest) + "\n")
    .encode("utf-8"))
print("回滚点 -> %s（%d 个文件）" % (pristine, len(manifest)))

# —— 2. 落盘 ——
stats, _results = core.run(trans, write_files=True)

# —— 3. 断言：每个键都命中过，且没有译文里的反引号混进正文 ——
missed = [k for k in trans.TRANS if stats["span"].get(k, {}).get("n", 0) == 0]
badfix = [(o, w, g) for o, d in stats["fix"].items() for w, g in [(d["want"], d["got"])]
          if w and w != g]
badtit = [(t, n) for t, n in stats["title"].items()
          if n != core.TITLE_EXPECT.get(t, n)]
assert not missed, "有 %d 个键一次都没命中：%r" % (len(missed), missed[:5])
assert not badfix, "FIXES 次数不符：%r" % badfix
assert not badtit, "标题命中数不符：%r" % badtit

# —— 4. 报告 ——
lines = ["# 落盘报告", "",
         "回滚点：`_quote_rework/pristine/`（%d 个文件，逐字节）" % len(manifest), ""]
lines.append("合计（11 个文件累加，含 4 份副本的重复）：")
lines.append("")
lines.append("- 正文引文中译：**%d** 处 = 引文总出现次数 × 4 份副本。"
             % sum(d["n"] for d in stats["span"].values()))
lines.append("- 字面改写：**%d** 处。" % sum(d["got"] for d in stats["fix"].values()))
lines.append("- 章标题翻译：**%d** 处（第 4 章标题，4 份笔记 + 提纲）。"
             % sum(stats["title"].values()))
lines.append("- 出处未解析的表格行：**%d** 条（跨 4 份副本累加，除以 4 即每份的行数）。"
             % stats["src_missing"])
lines.append("- 附录表按「逐字原文」去重：同一句话在一章里出现多次只列一行，"
             "出处取该组里第一个解析出来的。")
lines += ["", "## 逐文件", "",
          "| 文件 | 类型 | 行尾 | 标题命中 | 附录行数（按章） |",
          "| --- | --- | --- | --- | --- |"]
for path, kind in core.TARGETS:
    raw = path.read_bytes()
    eol = "CRLF" if b"\r\n" in raw else "LF"
    ap = stats["appendix"].get(path.name, {})
    lines.append("| %s | %s | %s | %d | %s |"
                 % (path.name, kind, eol, stats["title"].get(path.name, 0),
                    "、".join("%d:%d" % (c, ap[c]) for c in sorted(ap))))
for path in core.TITLE_ONLY:
    lines.append("| %s | title_only | %s | %d | — |"
                 % (path.name, "CRLF" if b"\r\n" in path.read_bytes() else "LF",
                    stats["title"].get(path.name, 0)))
lines += ["", "（不在表里逐文件列引文中译数：每个键的计数是全局的，"
          "按文件列会把同一个数重复计到它的 4 份副本上，是假精度。）"]
(HERE / "apply_report.md").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
print("报告 -> apply_report.md")
for l in lines:
    print(l.encode("ascii", "replace").decode("ascii"))
