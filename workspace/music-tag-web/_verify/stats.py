import sys, pathlib, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

C = pathlib.Path("workspace/music-tag-web/chapters")
HAN = re.compile(r"[一-鿿]")


def split_fences(t):
    """返回 (开围栏列表, 去掉代码块后的正文)。按出现顺序交替判定开/闭。"""
    lines = t.splitlines()
    opens, body, in_code, lang = [], [], False, None
    for ln in lines:
        if ln.startswith("```"):
            if not in_code:
                in_code = True
                lang = ln[3:].strip()
            else:
                in_code = False
            continue
        if in_code:
            continue
        body.append(ln)
    # 重新扫一遍收集开围栏语言（上面只记了最后一个）
    opens = []
    in_code = False
    for ln in lines:
        if ln.startswith("```"):
            if not in_code:
                opens.append(ln[3:].strip())
                in_code = True
            else:
                in_code = False
    return opens, "\n".join(body)


rows = []
tot_h = tot_b = 0
for f in sorted(C.glob("*.md")):
    t = f.read_text(encoding="utf-8")
    opens, body = split_fences(t)
    h = len(HAN.findall(t))
    b = f.stat().st_size
    no_lang = [x for x in opens if not x]
    fns = set(re.findall(r"^\[\^([^\]]+)\]:", t, re.M))
    refs = set(re.findall(r"\[\^([^\]]+)\](?!:)", t))
    h1 = len(re.findall(r"^# ", body, re.M))
    rows.append((f.name, h, b, len(opens), len(no_lang), len(fns),
                 sorted(refs - fns), sorted(fns - refs), h1))
    tot_h += h
    tot_b += b

print("%-32s %6s %7s %6s %6s %6s %4s" % ("file", "汉字", "bytes", "代码块", "无标识", "脚注", "H1"))
for r in rows:
    print("%-32s %6d %7d %6d %6d %6d %4d" % (r[0], r[1], r[2], r[3], r[4], r[5], r[8]))
    if r[6]:
        print("      !! 引用了未定义脚注:", r[6])
    if r[7]:
        print("      ·  定义了未引用脚注:", r[7])
print("-" * 74)
print("合计 汉字 %d / bytes %d / 文件 %d" % (tot_h, tot_b, len(rows)))
print("拆分判据：>30KB = %s ; 章节数 >3 = %s" % (tot_b > 30720, len(rows) > 3))
