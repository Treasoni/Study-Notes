# -*- coding: utf-8 -*-
import io, re, collections

OUT = "workspace/smb-cifs-mount-linux/output/final_note.md"
MERGED = "workspace/smb-cifs-mount-linux/chapters/_merged.md"

def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

out = read(OUT)
merged = read(MERGED)

def strip_fences(t):
    """去掉围栏代码块内容，便于统计真实标题"""
    lines = t.split("\n")
    keep, infence = [], False
    for ln in lines:
        if ln.lstrip().startswith("```"):
            infence = not infence
            keep.append("")
            continue
        keep.append("" if infence else ln)
    return "\n".join(keep)

out_nof = strip_fences(out)

print("== 规模 ==")
print("final_note bytes =", len(out.encode("utf-8")))
print("final_note chars =", len(out))
print("final_note cn    =", len(re.findall(r"[一-鿿]", out)))

print()
print("== 标题层级（已剔除代码块）==")
for lvl in range(1, 7):
    pat = r"^#{%d} " % lvl
    print("h%d =" % lvl, len(re.findall(pat, out_nof, re.M)))

print()
print("== 标注零损失 ==")
for mark in ["[社区]", "[推断]", "[缺口]"]:
    print(mark, "merged =", merged.count(mark), " final =", out.count(mark))

print()
print("== H1 行 ==")
for i, ln in enumerate(out_nof.split("\n"), 1):
    if ln.startswith("# "):
        print(" line", i, "->", ln)

print()
print("== 重复标题（Obsidian 锚点冲突）==")
heads = re.findall(r"^(#{2,4}) (.+)$", out_nof, re.M)
c = collections.Counter(h[1].strip() for h in heads)
dups = {k: v for k, v in c.items() if v > 1}
for k, v in sorted(dups.items(), key=lambda x: -x[1]):
    print("  x%d  %s" % (v, k))
print("  (empty = none)")

print()
print("== 目录小节 ==")
lines = out_nof.split("\n")
try:
    s = next(i for i, l in enumerate(lines) if l.strip() == "## 目录")
    e = next(i for i, l in enumerate(lines[s + 1:], s + 1) if l.startswith("## "))
    for l in lines[s:e]:
        print("   ", l)
except StopIteration:
    print("    [目录小节未找到]")
