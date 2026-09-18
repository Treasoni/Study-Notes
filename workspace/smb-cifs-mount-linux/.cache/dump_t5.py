# -*- coding: utf-8 -*-
import io, re

OUT = "workspace/smb-cifs-mount-linux/output/final_note.md"
with io.open(OUT, encoding="utf-8") as f:
    lines = f.read().split("\n")

buf = []
def w(s=""):
    buf.append(s)

# 目录区尾部
s = next(i for i, l in enumerate(lines) if l.strip() == "## 目录")
e = next(i for i, l in enumerate(lines[s + 1:], s + 1) if l.startswith("## "))
w("=== 目录区 行 %d-%d ===" % (s + 1, e))
for l in lines[s + 40:e]:
    w(l)

# 附录区
a = next(i for i, l in enumerate(lines) if l.startswith("## 附录"))
w("")
w("=== 附录区 行 %d-%d ===" % (a + 1, len(lines)))
for l in lines[a:a + 30]:
    w(l)

# 所有 h2/h3 标题清单
w("")
w("=== 全部 h2 / h3 标题（含行号）===")
infence = False
for i, l in enumerate(lines, 1):
    if l.lstrip().startswith("```"):
        infence = not infence
        continue
    if infence:
        continue
    if re.match(r"^#{2,3} ", l):
        w("%4d  %s" % (i, l))

with io.open("workspace/smb-cifs-mount-linux/.cache/_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(buf))
print("dumped", len(buf), "lines")
