# -*- coding: utf-8 -*-
import os, re, io, sys

VAULT = u"D:/Study-Notes"
DIR = os.path.join(VAULT, u"linux", u"SMB挂载")

VOLS = [
    u"SMB挂载-01-协议选型.md",
    u"SMB挂载-02-手动挂载.md",
    u"SMB挂载-03-凭据与开机自动挂载.md",
    u"SMB挂载-04-排错.md",
    u"SMB挂载-05-容器内挂载.md",
]
INDEX = u"SMB挂载-00-总目录.md"


def read(p):
    with io.open(p, encoding=u"utf-8") as f:
        return f.read()


def headings(text):
    """fence-aware: '#' lines inside ``` blocks are shell/python comments, not headings."""
    out = []
    fence = False
    for i, ln in enumerate(text.split(u"\n")):
        if ln.lstrip().startswith(u"```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(u"^(#{1,6})\s+(\S.*)$", ln)
        if m:
            out.append((i + 1, len(m.group(1)), m.group(2).strip()))
    return out


rep = []
fails = []

# ---- 1. per-volume structure ----
tot = {u"[社区]": 0, u"[推断]": 0, u"[缺口]": 0}
for v in VOLS:
    p = os.path.join(DIR, v)
    t = read(p)
    hs = headings(t)
    h1 = [h for h in hs if h[1] == 1]
    h2 = [h[2] for h in hs if h[1] == 2]
    h3 = [h[2] for h in hs if h[1] == 3]
    dup2 = sorted(set(x for x in h2 if h2.count(x) > 1))
    dup3 = sorted(set(x for x in h3 if h3.count(x) > 1))
    c = t.count(u"[社区]")
    d = t.count(u"[推断]")
    g = t.count(u"[缺口]")
    tot[u"[社区]"] += c
    tot[u"[推断]"] += d
    tot[u"[缺口]"] += g
    rep.append(u"=== %s ===" % v)
    rep.append(u"  H1 x%d: %s" % (len(h1), h1[0][2] if h1 else u"(none)"))
    rep.append(u"  H2 x%d  H3 x%d" % (len(h2), len(h3)))
    rep.append(u"  重复 H2: %s" % (u", ".join(dup2) if dup2 else u"无"))
    rep.append(u"  重复 H3: %s" % (u", ".join(dup3) if dup3 else u"无"))
    rep.append(u"  字面量 社区=%d 推断=%d 缺口=%d" % (c, d, g))
    if len(h1) != 1:
        fails.append(u"%s H1 数量 %d != 1" % (v, len(h1)))
    if dup2:
        fails.append(u"%s 重复 H2: %s" % (v, dup2))
    if dup3:
        fails.append(u"%s 重复 H3: %s" % (v, dup3))

rep.append(u"")
rep.append(u"5 册合计（字面量，含元提及）: 社区=%d 推断=%d 缺口=%d"
           % (tot[u"[社区]"], tot[u"[推断]"], tot[u"[缺口]"]))

# ---- 2. wikilink landing check over all 6 files ----
rep.append(u"")
rep.append(u"=== 双链落地检查 ===")
allmd = {}
for root, dirs, files in os.walk(VAULT):
    dirs[:] = [x for x in dirs if x not in (u".git", u".claude", u".obsidian", u"node_modules")]
    for fn in files:
        if fn.endswith(u".md"):
            allmd.setdefault(fn[:-3], []).append(os.path.join(root, fn))

link_re = re.compile(u"\\[\\[([^\\[\\]]+)\\]\\]")
bad = []
nlink = 0
files = [INDEX] + VOLS
for v in files:
    t = read(os.path.join(DIR, v))
    for raw in link_re.findall(t):
        target = raw.split(u"|")[0].split(u"#")[0].strip()
        if not target:
            continue
        nlink += 1
        rel = os.path.join(DIR, target + u".md")
        base = os.path.basename(target)
        if os.path.exists(rel) or base in allmd:
            continue
        bad.append(u"%s -> [[%s]]" % (v, raw))
rep.append(u"双链总数 %d，未落地 %d" % (nlink, len(bad)))
for b in bad:
    rep.append(u"  [FAIL] " + b)
if bad:
    fails.append(u"未落地双链 %d 条" % len(bad))

# ---- 3. the two edited regions, verbatim ----
rep.append(u"")
rep.append(u"=== 本次新增区域 ===")
t3 = read(os.path.join(DIR, VOLS[2]))
lines3 = t3.split(u"\n")
for i, ln in enumerate(lines3):
    if ln.strip().startswith(u"### 3.1.1"):
        rep.append(u"--- vol3 L%d 起 ---" % (i + 1))
        rep.append(u"\n".join(lines3[i:i + 32]))
        break
t2 = read(os.path.join(DIR, VOLS[1]))
lines2 = t2.split(u"\n")
for i, ln in enumerate(lines2):
    if u"FNOS 侧的凭据怎么填" in ln:
        rep.append(u"--- vol2 L%d 起 ---" % (i + 1))
        rep.append(u"\n".join(lines2[max(0, i - 2):i + 4]))
        break

rep.append(u"")
rep.append(u"FAILURES: %d" % len(fails))
for f in fails:
    rep.append(u"  [FAIL] " + f)
rep.append(u"RESULT: %s" % (u"ALL PASS" if not fails else u"FAILED"))

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), u"_verify_edit.txt"),
             u"w", encoding=u"utf-8") as f:
    f.write(u"\n".join(rep))

print("failures=%d links=%d" % (len(fails), nlink))
