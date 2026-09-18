# -*- coding: utf-8 -*-
"""P6：把组装稿切分成 SMB挂载 系列分册，写入 Obsidian vault。

纪律（每条都有断言，绿灯不代表产物正确，最后仍逐行读成品）：
- 正文逐字搬运：demote 只允许「去掉一个 #」，其余行必须逐字不变（proven, not assumed）。
- 写盘后读回，断言字节级一致（防编码/换行破坏）。
- 每个分册的 [社区]/[推断]/[缺口] 计数与源章节相等。
- 每条 [[双链]] 目标文件在 vault 里真实存在（生成侧与校验侧共用同一个命名函数）。
- 目标目录用「前缀白名单删除 + 外来文件即失败退出」，不用 rm -rf。
"""
import io, os, re, sys, glob, hashlib

SRC = "workspace/smb-cifs-mount-linux/output/final_note.md"
DEST_DIR = "linux/SMB挂载"
PREFIX = "SMB挂载-"
SERIES = u"SMB/CIFS 共享文件夹挂载到 Linux 服务器"
PROJECT = u"smb-cifs-mount-linux"
DATE = u"2026-09-18"

VOLS = [
    dict(
        num=1, slug=u"协议选型",
        title=u"第一章：协议选型：什么时候该用 SMB/CIFS",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 1 册 协议选型",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"协议选型", u"实战笔记", u"SMB挂载"],
        related=[
            (u"网络协议详解-WebDAV_Samba_FTP_iSCSI", u"WebDAV / Samba / FTP / iSCSI 一族协议的横向对比，本册选型的上游背景"),
            (u"OpenList网盘挂载-00-总目录", u"另一条「挂载」路线：WebDAV + rclone 把网盘挂成宿主机目录"),
        ],
    ),
    dict(
        num=2, slug=u"手动挂载",
        title=u"第二章：手动挂载：从零到挂上",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 2 册 手动挂载",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"cifs-utils", u"NAS", u"飞牛FNOS", u"Windows", u"实战笔记", u"SMB挂载"],
        related=[
            (u"Linux的文件系统结构", u"先看懂「挂载点」在本机文件系统里是什么，再理解 CIFS 挂载点属主的特殊性"),
            (u"linux磁盘相关的知识", u"分区、格式化与 mount 的基础语义"),
            (u"linux的文件权限", u"本地 `chown`/`chmod` 的直觉，与 CIFS 挂载点权限规则的差异对照"),
            (u"软路由教程/飞牛安装配置iStoreOS旁路由", u"飞牛 FNOS 作为共享端的环境背景（本册 2.5.2 的 FNOS 例子）"),
        ],
    ),
    dict(
        num=3, slug=u"凭据与开机自动挂载",
        title=u"第三章：凭据文件与开机自动挂载",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 3 册 凭据与开机自动挂载",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"fstab", u"systemd", u"凭据管理", u"实战笔记", u"SMB挂载"],
        related=[
            (u"linux的文件权限", u"凭据文件 `chmod 600` 与目录 700 的权限模型"),
            (u"Linux的文件系统结构", u"`/etc/fstab` 在本机文件系统里的角色"),
        ],
    ),
    dict(
        num=4, slug=u"排错",
        title=u"第四章：排错：从错误码回到证据链",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 4 册 排错",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"排错", u"errno", u"SMB签名", u"实战笔记", u"SMB挂载"],
        related=[
            (u"网络协议详解-WebDAV_Samba_FTP_iSCSI", u"想换协议栈时，先看这份横向对比"),
        ],
    ),
    dict(
        num=5, slug=u"容器内挂载",
        title=u"第五章：容器内挂载",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 5 册 容器内挂载",
        tags=[u"Docker", u"SMB", u"CIFS", u"Linux", u"挂载", u"容器", u"实战笔记", u"SMB挂载"],
        related=[
            (u"Docker容器服务访问宿主机文件", u"容器读写宿主机文件的挂载选型、权限对齐与安全边界"),
            (u"OpenList网盘挂载-00-总目录", u"同一条思路的另一种实现：宿主机挂载 → 映射给容器"),
        ],
    ),
]

MARKS = [u"[社区]", u"[推断]", u"[缺口]"]


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


def vol_stem(v):
    """分册文件名的唯一来源：生成侧与校验侧都调用它。"""
    return u"%s%02d-%s" % (PREFIX, v["num"], v["slug"])


def vol_index_stem():
    return u"%s00-总目录" % PREFIX


def link_target_exists(target):
    return bool(glob.glob(target + u".md") or glob.glob(u"**/" + target + u".md", recursive=True))


def headings(bl):
    """围栏代码块感知的标题扫描：返回 [(行号, 级数, 文字)]。"""
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


# ---------------------------------------------------------------- 切分源稿件
text = read(SRC).replace(u"\r\n", u"\n")
lines = text.split(u"\n")

chap_starts = []
for i, ln in enumerate(lines):
    m = re.match(u"^## (第[一二三四五]章：.+)$", ln)
    if m:
        chap_starts.append((i, m.group(1)))
assert len(chap_starts) == 5, u"chapter heading count = %d" % len(chap_starts)
appx = next(i for i, ln in enumerate(lines) if ln.startswith(u"## 附录"))
assert appx > chap_starts[-1][0]

src_chaps = []
for k, (start, title) in enumerate(chap_starts):
    end = chap_starts[k + 1][0] if k + 1 < len(chap_starts) else appx
    body = lines[start + 1:end]
    while body and body[-1].strip() == u"":
        body.pop()
    src_chaps.append(dict(title=title, body=body))

for v, sc, (start, _) in zip(VOLS, src_chaps, chap_starts):
    assert v["title"] == sc["title"], u"%s != %s" % (v["title"], sc["title"])
    # 源章节标题行本身就是 H1 的唯一来源（## 降为 #，文字零改动）
    assert lines[start] == u"## " + sc["title"], u"第 %d 行不是预期的章节标题" % start
    sc["h1"] = u"# " + sc["title"]
    assert sc["h1"] == lines[start][1:], u"第 %d 行降级后不等于 H1" % start


def demote(body):
    """返回 (新正文, 被改动行的下标)。只允许「去掉一个 #」。"""
    out, changed, infence = [], [], False
    for i, ln in enumerate(body):
        if ln.lstrip().startswith(u"```"):
            infence = not infence
            out.append(ln)
            continue
        if not infence:
            m = re.match(u"^(#{2,4}) (.*)$", ln)
            if m:
                out.append(u"#" * (len(m.group(1)) - 1) + u" " + m.group(2))
                changed.append(i)
                continue
        out.append(ln)
    return out, changed


# ------------------------------------------------------- 目标目录：前缀白名单
# 本脚本只拥有 5 个分册；总目录由人工撰写，视为已知共存文件，绝不删除。
OWNED = [vol_stem(v) + u".md" for v in VOLS]
KNOWN_OTHER = {vol_index_stem() + u".md"}
if os.path.isdir(DEST_DIR):
    existing = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DEST_DIR, u"*")))
    foreign = [f for f in existing if f not in OWNED and f not in KNOWN_OTHER]
    if foreign:
        print(u"[FAIL] 目标目录存在未知文件，拒绝写入：%s" % u", ".join(foreign))
        sys.exit(1)
    for f in existing:
        if f in OWNED:
            os.remove(os.path.join(DEST_DIR, f))
    print(u"已清理旧分册 %d 个（总目录保留）" % len([f for f in existing if f in OWNED]))
else:
    os.makedirs(DEST_DIR)
    print(u"已创建目录 %s" % DEST_DIR)


def vol_nav(cur):
    parts = [u"总目录：[[%s]]" % vol_index_stem()]
    if cur > 1:
        parts.append(u"上一册：[[%s]]" % vol_stem(VOLS[cur - 2]))
    if cur < len(VOLS):
        parts.append(u"下一册：[[%s]]" % vol_stem(VOLS[cur]))
    return u"> 🧭 分册导航 ｜ " + u" ｜ ".join(parts)


fail = []
for v, sc in zip(VOLS, src_chaps):
    dbody, changed = demote(sc["body"])

    # --- 断言 1：行数不变
    assert len(dbody) == len(sc["body"]), u"%s 行数变化" % vol_stem(v)
    # --- 断言 2：未标为 changed 的行逐字不变
    for i, ln in enumerate(sc["body"]):
        if i not in changed:
            assert dbody[i] == ln, u"%s 第 %d 行被改动: %r" % (vol_stem(v), i, dbody[i])
    # --- 断言 3：changed 行只少了一个 #
    for i in changed:
        h = len(sc["body"][i]) - len(sc["body"][i].lstrip(u"#"))
        assert sc["body"][i][h] == u" " and 2 <= h <= 4, u"%s 第 %d 行不是 2-4 级标题" % (vol_stem(v), i)
        assert dbody[i] == u"#" * (h - 1) + sc["body"][i][h:], u"%s 第 %d 行标题文字被改" % (vol_stem(v), i)
    # --- 断言 4：标注计数
    for mk in MARKS:
        a = u"\n".join(sc["body"]).count(mk)
        b = u"\n".join(dbody).count(mk)
        assert a == b, u"%s 标注 %s 计数 %d != %d" % (vol_stem(v), mk, a, b)

    head = [u"---", u"title: %s" % v["vol_title"], u"tags:"] + \
           [u"  - %s" % t for t in v["tags"]] + \
           [u"created: %s" % DATE, u"updated: %s" % DATE, u"status: 已完成",
            u"source_project: %s" % PROJECT, u"series: %s" % SERIES,
            u"volume: %d/%d" % (v["num"], len(VOLS)), u"---", u""]
    rel = [u"", u"## 相关笔记", u""] + [u"- [[%s]] —— %s" % (t, d) for t, d in v["related"]]
    tail = [u"", u"---", u"", vol_nav(v["num"]), u""]
    body_lines = list(dbody)
    while body_lines and body_lines[0].strip() == u"":
        body_lines.pop(0)

    content = u"\n".join(head + [sc["h1"], u"", vol_nav(v["num"]), u""] + body_lines + rel + tail)
    path = os.path.join(DEST_DIR, vol_stem(v) + u".md")
    write(path, content)

    # --- 断言 5：读回逐字节一致
    back = read(path)
    assert back == content, u"%s 读回与写入不一致" % path
    assert hashlib.sha256(back.encode(u"utf-8")).hexdigest() == \
           hashlib.sha256(content.encode(u"utf-8")).hexdigest(), u"%s 哈希不一致" % path

    # --- 断言 6：结构小标题出现次数 == 期望值（不是 ≥1）
    bl = back.split(u"\n")
    hs = headings(bl)
    lvl = {}
    for _, n, _ in hs:
        lvl[n] = lvl.get(n, 0) + 1
    assert lvl.get(1, 0) == 1, u"%s H1 数量 %d != 1" % (path, lvl.get(1, 0))
    exp_lvl = {}
    for _, n, _ in headings([sc["h1"]] + body_lines):
        exp_lvl[n] = exp_lvl.get(n, 0) + 1
    exp_lvl[2] = exp_lvl.get(2, 0) + 1          # ## 相关笔记
    assert lvl == exp_lvl, u"%s 标题级数分布 %s != %s" % (path, lvl, exp_lvl)
    assert back.count(vol_nav(v["num"])) == 2, u"%s 导航条出现次数 != 2" % path
    assert [t for _, n, t in hs].count(u"相关笔记") == 1, u"%s 相关笔记小节 != 1" % path
    assert [l for l in bl if l == u"---"].__len__() == 3, u"%s 分隔线数量 != 3" % path
    # 断言 7：本文件内 H2 不重复（重复锚点会让 TOC/双链跳错）
    h2 = [t for _, n, t in hs if n == 2]
    dup = sorted(set(x for x in h2 if h2.count(x) > 1))
    assert not dup, u"%s 有重复 H2：%s" % (path, dup)
    print(u"写出 %s（%d 字符 / %d 中文字 / 标题 %d 个）" %
          (vol_stem(v) + u".md", len(back), len(re.findall(u"[一-鿿]", back)), len(changed)))

# ------------------------------------------ 断言 8（第二遍）：全部文件写完后校验双链
all_files = sorted(glob.glob(os.path.join(DEST_DIR, u"*.md")))
for p in all_files:
    b = read(p)
    for tgt in sorted(set(re.findall(u"\\[\\[([^\\]|#]+)", b))):
        if not link_target_exists(tgt.strip()):
            fail.append((os.path.basename(p), tgt.strip()))
if len(all_files) != len(OWNED) + 1:
    print(u"[WARN] 目录内 md 文件数 %d，期望 %d（5 分册 + 1 总目录）" % (len(all_files), len(OWNED) + 1))

# ------------------------------------------------------------------ 附录导出
write(u"workspace/smb-cifs-mount-linux/.cache/_appendix.md", u"\n".join(lines[appx:]))

if fail:
    print(u"[FAIL] 缺失目标 %d 条：%s" % (len(fail), fail))
    sys.exit(1)
print(u"全部断言通过：5 个分册 + 附件导出；总目录待写")
