"""逐条精核：附录 C 里所有成对引号内容，必须在 02 文档或语料中逐字出现。"""
import sys, pathlib, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("workspace/music-tag-web")
parts = [(ROOT / "02_deep_research.md").read_text(encoding="utf-8")]
for p in sorted((ROOT / "_verify" / "src").glob("*")):
    if p.is_file():
        parts.append(p.read_text(encoding="utf-8", errors="replace"))
for extra in ["i546.html"]:
    q = ROOT / "_verify" / extra
    if q.exists():
        parts.append(q.read_text(encoding="utf-8", errors="replace"))


def norm(t):
    t = t.replace("**", "").replace("`", "").replace("\\", "")
    return re.sub(r"[\s　]+", "", t)


N = norm("\n".join(parts))

text = (ROOT / "chapters" / "appendix-c-troubleshooting.md").read_text(encoding="utf-8")
# 严格成对：先 「…」 再 “…” 再 "…"
pairs = []
for op, cl in [("「", "」"), ("“", "”"), ('"', '"')]:
    for m in re.finditer(re.escape(op) + r"([^" + re.escape(op + cl) + r"]{8,})" + re.escape(cl), text):
        if op == '"':
            # ASCII 引号成对：按出现顺序两两配对
            continue
        pairs.append((m.start(), m.group(1)))
for m in re.finditer(r'"([^"]{8,})"', text):
    pairs.append((m.start(), m.group(1)))

line_of = lambda pos: text.count("\n", 0, pos) + 1
bad = 0
for pos, frag in sorted(pairs):
    if norm(frag) in N:
        continue
    bad += 1
    print("L%-4d 未命中 %r" % (line_of(pos), frag[:130]))
print("\n成对引号共 %d 处；未命中 %d 处" % (len(pairs), bad))
