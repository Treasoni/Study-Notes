import re, sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = pathlib.Path(".")
merged = (BASE / "chapters/_merged.md").read_text(encoding="utf-8")
note = (BASE / "output/final_note.md").read_text(encoding="utf-8")


def hanzi(t):
    return len(re.findall(r"[一-鿿]", t))


def anchors(t):
    return re.findall(r"`research/[^`]+`", t)


def codespans(t):
    return re.findall(r"`[^`\n]+`", t)


def tablerows(t):
    return [l for l in t.splitlines() if l.strip().startswith("|")]


def callouts(t):
    return re.findall(r"^>\s*\[![a-z]+\][^\n]*", t, re.M)


print("=== 规模 ===")
print(f"  _merged.md  汉字 {hanzi(merged)}  字节 {len(merged.encode('utf-8'))}")
print(f"  final_note  汉字 {hanzi(note)}  字节 {len(note.encode('utf-8'))}")
print(f"  汉字差 {hanzi(note) - hanzi(merged)}")

print("\n=== 结构 ===")
for pat, name in [(r"^# ", "H1"), (r"^## ", "H2"), (r"^### ", "H3"), (r"^#### ", "H4")]:
    print(f"  {name}: {len(re.findall(pat, note, re.M))}")

print("\n=== 保真度（以 _merged.md 为准） ===")
for fn, name in [(anchors, "research 锚点"), (callouts, "Callout 头")]:
    a, b = fn(merged), fn(note)
    sa, sb = set(a), set(b)
    print(f"  {name}: merged {len(a)} / note {len(b)}  丢失 {len(sa - sb)}  新增 {len(sb - sa)}")
    for x in sorted(sa - sb)[:5]:
        print(f"     - 丢失: {x}")

tr_m, tr_n = tablerows(merged), tablerows(note)
print(f"  表格行: merged {len(tr_m)} / note {len(tr_n)}")
if tr_m != tr_n:
    sm, sn = set(tr_m), set(tr_n)
    print(f"     丢失 {len(sm - sn)} 行, 新增 {len(sn - sm)} 行")
    for x in sorted(sm - sn)[:5]:
        print(f"     - 丢失: {x[:100]}")

# 正文段落级比对：抽出行数 与 逐行在 note 中的存在性
miss = 0
for line in merged.splitlines():
    s = line.strip()
    if len(s) < 12 or s.startswith("<!--"):
        continue
    if s not in note:
        # 允许标题降级
        core = re.sub(r"^#+\s*", "", s)
        if core not in note:
            miss += 1
            if miss <= 8:
                print(f"  ! 正文行未在成品中找到: {s[:90]}")
print(f"\n  正文实义行缺失（含标题降级宽免后）: {miss}")
