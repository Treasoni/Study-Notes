import sys, pathlib, re, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

t = pathlib.Path("workspace/music-tag-web/_verify/i546.html").read_bytes().decode("utf-8", "replace")

pat = re.compile(r'"body":"((?:[^"\\]|\\.)*)"')
bodies = pat.findall(t)
print("body 字段数:", len(bodies))

seen = []
for b in bodies:
    try:
        s = json.loads('"' + b + '"')
    except Exception:
        s = b
    if s not in seen:
        seen.append(s)

for i, s in enumerate(seen, 1):
    print("[%d] %r" % (i, s[:400]))
print()
print("去重条数:", len(seen))

# 全页是否出现目标短语（含 HTML 转义变体）
for kw in ["这个啊", "算了", "重新导入收藏", "导入收藏", "检查是否删除"]:
    print("  含 %r : %d" % (kw, t.count(kw)))

# HTML 里是否有 "load more" / pagination 迹象
for kw in ["Load more", "load_more", "pagination", "hasNextPage"]:
    print("  标记 %r : %d" % (kw, t.count(kw)))
