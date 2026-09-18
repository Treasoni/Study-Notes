# -*- coding: utf-8 -*-
import io

OUT = "workspace/smb-cifs-mount-linux/output/final_note.md"
R02 = "workspace/smb-cifs-mount-linux/02_deep_research.md"
R01 = "workspace/smb-cifs-mount-linux/01_explore_result.md"

def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def write(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)

# ---------- 1. final_note.md 目录修复 ----------
t = read(OUT)
changes = 0

for label in ["本章小结", "本章来源"]:
    line = u"  - [%s](#%s)\n" % (label, label)
    n = t.count(line)
    assert n == 5, u"%s TOC line count = %d (expect 5)" % (label, n)
    t = t.replace(line, "")
    changes += n
    print(u"removed TOC line: %s x%d" % (label, n))

# 目录末尾补附录条目
anchor_line = u"  - [本章来源](#本章来源)\n"
assert t.count(anchor_line) == 0

# 定位目录区最后一行（第五章的本章来源行已被删，改用 5.2 行作锚）
last_toc = u"  - [5.2 更稳妥的替代路径](#52-更稳妥的替代路径)\n"
assert t.count(last_toc) == 1, "toc tail anchor count = %d" % t.count(last_toc)
appendix_entry = u"- [附录：来源总表](#附录来源总表)\n"
t = t.replace(last_toc, last_toc + appendix_entry)
changes += 1
print(u"added TOC entry: 附录：来源总表")

write(OUT, t)
print(u"final_note.md: %d edits; bytes=%d" % (changes, len(t.encode("utf-8"))))

# ---------- 2. 02 头部计数与阶段标注 ----------
t2 = read(R02)

old_scope = u"来源规模**: 16 条（official 11 ／ secondary 1 ／ community 3 ／ 历史一手 1）"
new_scope = u"来源规模**: 19 条（official 14 ／ secondary 1 ／ community 3 ／ 历史一手 1）"
assert t2.count(old_scope) == 1, "scope row count = %d" % t2.count(old_scope)
t2 = t2.replace(old_scope, new_scope)

old_stage = u"阶段**: P2 深度收集（未完成，等待用户确认素材质量与执行模式）"
new_stage = u"阶段**: P2 深度收集（已完成；用户 2026-09-18 确认素材质量，执行模式 = 大纲模式）"
assert t2.count(old_stage) == 1, "stage row count = %d" % t2.count(old_stage)
t2 = t2.replace(old_stage, new_stage)

write(R02, t2)
print(u"02_deep_research.md: 2 edits")

# ---------- 3. 01 阶段标注 ----------
t1 = read(R01)
old1 = u"阶段**: P1 探测式收集（未完成，等待用户选定方向）"
new1 = u"阶段**: P1 探测式收集（已完成；用户 2026-09-18 选定方向 A 均衡实战）"
assert t1.count(old1) == 1, "01 stage row count = %d" % t1.count(old1)
t1 = t1.replace(old1, new1)
write(R01, t1)
print(u"01_explore_result.md: 1 edit")
