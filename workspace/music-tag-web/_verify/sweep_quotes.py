"""逐字引用清扫 v3：覆盖 「」/“”/ASCII " 三种引号，只审带引用标记的行。"""
import sys, pathlib, re, html as htmllib, json

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path("workspace/music-tag-web/_verify/src")
CH = pathlib.Path("workspace/music-tag-web/chapters")
EXTRA = pathlib.Path("workspace/music-tag-web/_verify")

CITE = re.compile(r"\[\^|\[[^\]]*\]\(http|官方(?:说|写|称|口径|原文|定义)|原文|原话|照录|逐字")
SPAN = re.compile(r"""[「“"]([^」”"_]{6,})[」”"]""")


def normalize(t):
    t = htmllib.unescape(t)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^>]*)?/?>", "", t)
    t = re.sub(r"<https?://[^>]*>", "", t)
    t = re.sub(r"\\(.)", r"\1", t)
    t = t.replace("&#x20;", " ").replace("&nbsp;", " ")
    t = t.replace("**", "").replace("__", "").replace("*", "").replace("`", "")
    t = re.sub(r"[\s　]+", "", t)
    t = t.replace("……", "").replace("…", "")
    return t


corpus = {}
for p in sorted(SRC.glob("*")):
    if p.name.startswith("_"):
        continue
    corpus[p.name] = normalize(p.read_text(encoding="utf-8", errors="replace"))

blob = "\n".join(corpus.values())
for name in ["i546.html"]:
    p = EXTRA / name
    if p.exists():
        blob += "\n" + normalize(p.read_text(encoding="utf-8", errors="replace"))

print("语料文件数:", len(corpus) + 1, "总字符:", len(blob))
total = 0
report = []
for f in sorted(CH.glob("*.md")):
    lines = f.read_text(encoding="utf-8").splitlines()
    misses, hits = [], 0
    for i, ln in enumerate(lines, 1):
        if not CITE.search(ln):
            continue
        for m in SPAN.finditer(ln):
            key = normalize(m.group(1))
            if len(key) < 8:
                continue
            if key in blob:
                hits += 1
                continue
            parts = [x for x in re.split(r"[。；，、！？]", key) if len(x) >= 8]
            if parts and all(x in blob for x in parts):
                hits += 1
                continue
            misses.append((i, m.group(1)))
    total += len(misses)
    report.append((f.name, hits, [{"line": i, "frag": g} for i, g in misses]))
    print("=" * 72)
    print("%s  命中 %d / 待核 %d" % (f.name, hits, len(misses)))
    for i, frag in misses:
        print("   L%-4d %r" % (i, frag[:130]))

pathlib.Path("workspace/music-tag-web/_verify/quote_sweep.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n合计待核", total)
