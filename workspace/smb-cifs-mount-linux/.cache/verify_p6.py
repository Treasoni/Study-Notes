# -*- coding: utf-8 -*-
"""P6 独立校验：不复用生成脚本的索引算术，改用「子序列回溯」证明成品正文可逐字追回源章节。

输出写到 UTF-8 文件再读，避免本机 stdout 的 gbk 编码问题。
"""
import io, os, re, glob

SRC = "workspace/smb-cifs-mount-linux/output/final_note.md"
DEST_DIR = "linux/SMB挂载"
INDEX = u"SMB挂载-00-总目录"
MARKS = [u"[社区]", u"[推断]", u"[缺口]"]
log = []


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read().replace(u"\r\n", u"\n")


def headings(bl):
    out, infence = [], False
    for i, ln in enumerate(bl):
        if ln.lstrip().startswith(u"```"):
            infence = not infence
            continue
        if not infence:
            m = re.match(u"^(#{1,6}) (.*)$", ln)
            if m:
                out.append((i, len(m.group(1)), m.group(2)))
    return out


def exists(t):
    return bool(os.path.exists(t + u".md") or glob.glob(u"**/" + t + u".md", recursive=True))


src = read(SRC)
slines = src.split(u"\n")
starts = [(i, re.match(u"^## (第[一二三四五]章：.+)$", ln).group(1))
          for i, ln in enumerate(slines) if re.match(u"^## (第[一二三四五]章：.+)$", ln)]
appx = next(i for i, ln in enumerate(slines) if ln.startswith(u"## 附录"))
chaps = []
for k, (s, t) in enumerate(starts):
    e = starts[k + 1][0] if k + 1 < len(starts) else appx
    b = slines[s + 1:e]
    while b and b[-1].strip() == u"":
        b.pop()
    chaps.append((t, b))

# 分册文件名：与生成侧同一个命名函数
slug = [u"协议选型", u"手动挂载", u"凭据与开机自动挂载", u"排错", u"容器内挂载"]
VF = [u"%s-%02d-%s" % (u"SMB挂载", i + 1, s) for i, s in enumerate(slug)]

files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DEST_DIR, u"*.md")))
expected_files = sorted([x + u".md" for x in VF] + [INDEX + u".md"])
log.append(u"目录内文件：%s" % files)
log.append(u"期望文件  ：%s" % expected_files)
log.append(u"[%s] 文件清单一致" % (u"OK" if files == expected_files else u"FAIL"))

nofail = 0

for vi, (vf, (title, body)) in enumerate(zip(VF, chaps)):
    p = os.path.join(DEST_DIR, vf + u".md")
    t = read(p)
    bl = t.split(u"\n")

    # 1) H1 唯一，且文字 == 源章节标题
    hs = headings(bl)
    h1 = [x for x in hs if x[1] == 1]
    ok = len(h1) == 1 and h1[0][2] == title
    if not ok:
        nofail += 1
    log.append(u"[%s] %s H1 == 源章节标题（%s）" % (u"OK" if ok else u"FAIL", vf, title[:14]))

    # 2) 子序列回溯：源章节每一行都要在成品里按序被追回；
    #    标题行允许「少一个 #」，其余行必须逐字相等。
    i = 0
    gaps = []
    for ln in body:
        found = -1
        j = i
        while j < len(bl):
            if bl[j] == ln:
                found = j
                break
            m = re.match(u"^(#{2,4}) (.*)$", ln)
            if m and bl[j] == u"#" * (len(m.group(1)) - 1) + u" " + m.group(2):
                found = j
                break
            j += 1
        if found < 0:
            gaps.append(u"追不回：%r" % ln[:60])
        else:
            i = found + 1
    if gaps:
        nofail += 1
    log.append(u"[%s] %s 正文 %d 行全部按序追回（缺口 %d）" %
               (u"OK" if not gaps else u"FAIL", vf, len(body), len(gaps)))
    for g in gaps[:5]:
        log.append(u"      %s" % g)

    # 3) 标注计数
    for mk in MARKS:
        a, b = u"\n".join(body).count(mk), t.count(mk)
        if a != b:
            nofail += 1
        log.append(u"[%s] %s 标注 %s %d/%d" % (u"OK" if a == b else u"FAIL", vf, mk, b, a))

    # 4) 双链目标存在
    bad = [x for x in set(re.findall(u"\\[\\[([^\\]|#]+)", t)) if not exists(x.strip())]
    if bad:
        nofail += 1
    log.append(u"[%s] %s 双链全部存在（%d 条）%s" %
               (u"OK" if not bad else u"FAIL", vf, len(set(re.findall(u"\\[\\[([^\\]|#]+)", t))),
                (u" 缺失：" + u", ".join(bad)) if bad else u""))

    # 5) 文件内 H2/H3 不重复
    for lvl in (2, 3):
        names = [x[2] for x in hs if x[1] == lvl]
        dup = sorted(set(n for n in names if names.count(n) > 1))
        if dup:
            nofail += 1
        log.append(u"[%s] %s %d 级标题无重复%s" %
                   (u"OK" if not dup else u"FAIL", vf, lvl, (u" 重复：" + u", ".join(dup)) if dup else u""))

# 6) 总目录
it = read(os.path.join(DEST_DIR, INDEX + u".md"))
ib = it.split(u"\n")
vols_in_index = [v for v in VF if u"[[" + v + u"]]" in it]
ok = len(vols_in_index) == 5
if not ok:
    nofail += 1
log.append(u"[%s] 总目录链接全 5 册（找到 %d）" % (u"OK" if ok else u"FAIL", len(vols_in_index)))
rows = [l for l in ib if l.startswith(u"| 1 |") or l.startswith(u"| 2 |") or l.startswith(u"| 3 |")
        or l.startswith(u"| 4 |") or l.startswith(u"| 5 |")]
log.append(u"[%s] 分册导航表 %d 行" % (u"OK" if len(rows) == 5 else u"FAIL", len(rows)))
log.append(u"[%s] mermaid 图存在" % (u"OK" if u"```mermaid" in it else u"FAIL"))
log.append(u"[%s] 附录来源表 19 行" %
           (u"OK" if len([l for l in ib if re.match(u"^\\| S\\d", l)]) == 19 else u"FAIL"))
log.append(u"[%s] 总目录双链全部存在" %
           (u"OK" if not [x for x in set(re.findall(u"\\[\\[([^\\]|#]+)", it)) if not exists(x.strip())] else u"FAIL"))
log.append(u"")
tot = {mk: sum(read(os.path.join(DEST_DIR, v + u".md")).count(mk) for v in VF) for mk in MARKS}
src_tot = {mk: src.count(mk) for mk in MARKS}
for mk in MARKS:
    ok = tot[mk] == src_tot[mk]
    if not ok:
        nofail += 1
    log.append(u"[%s] 五册合计 %s = %d（组装稿 %d）" % (u"OK" if ok else u"FAIL", mk, tot[mk], src_tot[mk]))
log.append(u"")
log.append(u"失败项合计：%d" % nofail)

io.open(u"workspace/smb-cifs-mount-linux/.cache/_verify.txt", "w", encoding="utf-8").write(
    u"\n".join(log) + u"\n")
print(u"done, fails=%d" % nofail)
