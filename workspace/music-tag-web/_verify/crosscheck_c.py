"""附录 C 的引用逐条回 02 文档核对：每个引号片段是否逐字出现在 02_deep_research.md。"""
import sys, pathlib, re, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("workspace/music-tag-web")
TWO = (ROOT / "02_deep_research.md").read_text(encoding="utf-8")
SRC = ROOT / "_verify" / "src"

corpus = TWO
for p in sorted(SRC.glob("*.md")):
    corpus += "\n" + p.read_text(encoding="utf-8", errors="replace")
for p in sorted(SRC.glob("*.html")):
    corpus += "\n" + p.read_text(encoding="utf-8", errors="replace")
i546 = ROOT / "_verify" / "i546.html"
if i546.exists():
    corpus += "\n" + i546.read_text(encoding="utf-8", errors="replace")


def norm(t):
    t = t.replace("**", "").replace("`", "").replace("\\", "")
    return re.sub(r"[\s　]+", "", t)


N = norm(corpus)
f = ROOT / "chapters" / "appendix-c-troubleshooting.md"
text = f.read_text(encoding="utf-8")
# 只取正文（脚注定义之前），排除脚注 URL 里的内容
lines = text.splitlines()
SPAN = re.compile(r"""[「“"]([^」”"_]{8,})[」”"]""")
ok = bad = 0
for i, ln in enumerate(lines, 1):
    if ln.startswith("[^"):
        continue
    for m in SPAN.finditer(ln):
        key = norm(m.group(1))
        if len(key) < 8:
            continue
        if key in N:
            ok += 1
        else:
            bad += 1
            print("未见于 02/语料  L%-4d %r" % (i, m.group(1)[:120]))
print("\n逐字命中 %d / 未命中 %d" % (ok, bad))
