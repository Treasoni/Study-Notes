import sys, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = pathlib.Path("workspace/music-tag-web/_verify/i546.html").read_bytes().decode("utf-8", "replace")

for kw in ["hasNextPage", "totalCount", "commentCount", "first:", "last:", "discussion"]:
    print("== %r ==" % kw, t.count(kw))

for m in re.finditer(r'hasNextPage', t):
    s = max(0, m.start() - 120)
    e = min(len(t), m.end() + 120)
    print(repr(t[s:e]))
    print("-" * 30)

for m in re.finditer(r'"totalCount":\s*\d+', t):
    print("totalCount ->", m.group(0))

for m in re.finditer(r'("comments"|"numberOfComments"|"commentCount")\s*:\s*\d+', t):
    print(m.group(0))
