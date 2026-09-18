# -*- coding: utf-8 -*-
"""P6：把组装稿切分成 SMB挂载 系列分册，写入 Obsidian vault。

纪律：
- 正文逐字搬运，只改标题前的 # 数量（## → #，### → ##，#### → ###），标题文字零改动。
- 发送前断言：每个分册的非标题行序列与源章节逐字一致。
- 断言：三个标注 [社区]/[推断]/[缺口] 每个分册的计数与源章节相等。
- 断言：每条 [[双链]] 的目标文件在 vault 里真实存在。
- 目标目录用「前缀白名单删除 + 外来文件即失败退出」，不用 rm -rf。
"""
import io, os, re, sys, glob

SRC = "workspace/smb-cifs-mount-linux/output/final_note.md"
DEST_DIR = "linux/SMB挂载"
PREFIX = "SMB挂载-"
SERIES = u"SMB/CIFS 共享文件夹挂载到 Linux 服务器"
PROJECT = u"smb-cifs-mount-linux"
DATE = u"2026-09-18"

VOLS = [
    dict(
        num=1, slug=u"协议选型", fname=u"SMB挂载-01-协议选型.md",
        title=u"第一章：协议选型：什么时候该用 SMB/CIFS",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 1 册 协议选型",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"协议选型", u"实战笔记", u"SMB挂载"],
        solves=u"动手前先判断：该不该走 SMB/CIFS、共享端支持哪一版方言、挂上以后谁来管权限",
        outcome=u"说清「方言」是协商结果而非固定版本，并知道为什么不该把 `vers=` 写死",
        related=[
            (u"网络协议详解-WebDAV_Samba_FTP_iSCSI", u"WebDAV / Samba / FTP / iSCSI 一族协议的横向对比，本册选型的上游背景"),
            (u"OpenList网盘挂载-00-总目录", u"另一条「挂载」路线：WebDAV + rclone 把网盘挂成宿主机目录"),
        ],
    ),
    dict(
        num=2, slug=u"手动挂载", fname=u"SMB挂载-02-手动挂载.md",
        title=u"第二章：手动挂载：从零到挂上",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 2 册 手动挂载",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"cifs-utils", u"NAS", u"飞牛FNOS", u"Windows", u"实战笔记", u"SMB挂载"],
        solves=u"装 `cifs-utils`、挂载前用 `smbclient` 探测、写出并读懂 `mount -t cifs` 的每个选项",
        outcome=u"挂上共享，并说清 `uid`/`gid`、`file_mode`、`iocharset`、`vers`、`sec` 各自管什么、边界在哪",
        related=[
            (u"Linux的文件系统结构", u"先看懂「挂载点」在本机文件系统里是什么，再理解 CIFS 挂载点属主的特殊性"),
            (u"linux磁盘相关的知识", u"分区、格式化与 mount 的基础语义"),
            (u"linux的文件权限", u"本地 `chown`/`chmod` 的直觉，与 CIFS 挂载点权限规则的差异对照"),
            (u"软路由教程/飞牛安装配置iStoreOS旁路由", u"飞牛 FNOS 作为共享端的环境背景（本册 2.5.2 的 FNOS 例子）"),
        ],
    ),
    dict(
        num=3, slug=u"凭据与开机自动挂载", fname=u"SMB挂载-03-凭据与开机自动挂载.md",
        title=u"第三章：凭据文件与开机自动挂载",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 3 册 凭据与开机自动挂载",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"fstab", u"systemd", u"凭据管理", u"实战笔记", u"SMB挂载"],
        solves=u"把密码收进权限正确的凭据文件，写对 `/etc/fstab` 行，并搞懂 systemd 的开机顺序",
        outcome=u"服务器离线时开机不被卡住，并能在三条回落路线之间做出选择",
        related=[
            (u"linux的文件权限", u"凭据文件 `chmod 600` 与目录 700 的权限模型"),
            (u"Linux的文件系统结构", u"`/etc/fstab` 在本机文件系统里的角色"),
        ],
    ),
    dict(
        num=4, slug=u"排错", fname=u"SMB挂载-04-排错.md",
        title=u"第四章：排错：从错误码回到证据链",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 4 册 排错",
        tags=[u"SMB", u"CIFS", u"Linux", u"挂载", u"排错", u"errno", u"SMB签名", u"实战笔记", u"SMB挂载"],
        solves=u"`mount error(13)` 的完整证据链、errno 数值与易错点、方言协商的核对方法、Windows 侧签名导致的连不上",
        outcome=u"拿到一个错误码时能判断问题落在认证、网络还是方言协商上，而不是去背错误码清单",
        related=[
            (u"网络协议详解-WebDAV_Samba_FTP_iSCSI", u"想换协议栈时，先看这份横向对比"),
        ],
    ),
    dict(
        num=5, slug=u"容器内挂载", fname=u"SMB挂载-05-容器内挂载.md",
        title=u"第五章：容器内挂载",
        vol_title=u"SMB/CIFS 挂载到 Linux · 第 5 册 容器内挂载",
        tags=[u"Docker", u"SMB", u"CIFS", u"Linux", u"挂载", u"容器", u"实战笔记", u"SMB挂载"],
        solves=u"容器里直接 `mount` CIFS 为什么不稳，以及更稳妥的两条替代路径",
        outcome=u"知道该在宿主机挂好再 bind mount 进容器，而不是给容器加权限（全册为社区经验）",
        related=[
            (u"Docker容器服务访问宿主机文件", u"容器读写宿主机文件的挂载选型、权限对齐与安全边界"),
            (u"OpenList网盘挂载-00-总目录", u"同一条思路的另一种实现：宿主机挂载 → 映射给容器"),
        ],
    ),
]

fail = []


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def write(p, t):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(t)


text = read(SRC)
# 统一行尾，避免 CRLF/LF 混用
text = text.replace(u"\r\n", u"\n")
lines = text.split(u"\n")

# ---- 定位各章起始与附录 ----
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
    # 去掉尾部空行（章节之间用于分隔的空白）
    while body and body[-1].strip() == u"":
        body.pop()
    src_chaps.append(dict(title=title, body=body))

for v, sc in zip(VOLS, src_chaps):
    assert v["title"] == sc["title"], u"%s != %s" % (v["title"], sc["title"])
print(u"已定位 5 章，标题逐一对齐")


def demote(body):
    """## → #，### → ##，#### → ###；仅行首、且在围栏代码块外"""
    out, infence = [], False
    for ln in body:
        if ln.lstrip().startswith(u"```"):
            infence = not infence
            out.append(ln)
            continue
        if not infence:
            m = re.match(u"^(#{2,4}) (.*)$", ln)
            if m:
                out.append(u"#" * (len(m.group(1)) - 1) + u" " + m.group(2))
                continue
        out.append(ln)
    return out


# ---- 目标目录：前缀白名单清理 ----
if os.path.isdir(DEST_DIR):
    existing = sorted(os.path.basename(p) for p in glob.glob(os.path.join(DEST_DIR, u"*")))
    foreign = [f for f in existing if not f.startswith(PREFIX)]
    if foreign:
        print(u"[FAIL] 目标目录存在非本系列文件，拒绝写入：%s" % u", ".join(foreign))
        sys.exit(1)
    for f in existing:
        os.remove(os.path.join(DEST_DIR, f))
    print(u"已清理旧的分册文件 %d 个" % len(existing))
else:
    os.makedirs(DEST_DIR)
    print(u"已创建目录 %s" % DEST_DIR)

MARKS = [u"[社区]", u"[推断]", u"[缺口]"]


def vol_nav(cur):
    parts = [u"总目录：[[SMB挂载-00-总目录]]"]
    if cur > 1:
        parts.append(u"上一册：[[%s]]" % os.path.splitext(VOLS[cur - 2]["fname"])[0])
    if cur < len(VOLS):
        parts.append(u"下一册：[[%s]]" % os.path.splitext(VOLS[cur]["fname"])[0])
    return u"> 🧭 分册导航 ｜ " + u" ｜ ".join(parts)


for v, sc in zip(VOLS, src_chaps):
    dbody = demote(sc["body"])

    # --- 断言 1：标题文字集合不变 ---
    src_heads = [re.sub(u"^#{2,4} ", u"", l) for l in sc["body"] if re.match(u"^#{2,4} ", l)]
    out_heads = [re.sub(u"^#{1,3} ", u"", l) for l in dbody if re.match(u"^#{1,3} ", l)]
    assert src_heads == out_heads, u"%s 标题文字被改动" % v["fname"]

    # --- 断言 2：非标题行逐字一致 ---
    src_plain = [l for l in sc["body"] if not re.match(u"^#{1,4} ", l)]
    out_plain = [l for l in dbody if not re.match(u"^#{1,4} ", l)]
    assert src_plain == out_plain, u"%s 非标题行不一致" % v["fname"]

    # --- 断言 3：标注计数 ---
    for mk in MARKS:
        a = u"\n".join(sc["body"]).count(mk)
        b = u"\n".join(dbody).count(mk)
        assert a == b, u"%s 标注 %s 计数 %d != %d" % (v["fname"], mk, a, b)

    head = [
        u"---",
        u"title: %s" % v["vol_title"],
        u"tags:",
    ] + [u"  - %s" % t for t in v["tags"]] + [
        u"created: %s" % DATE,
        u"updated: %s" % DATE,
        u"status: 已完成",
        u"source_project: %s" % PROJECT,
        u"series: %s" % SERIES,
        u"volume: %d/%d" % (v["num"], len(VOLS)),
        u"---",
        u"",
    ]
    # H1 取源章节标题（仅把 ## 降为 #）
    tail = [u"", u"---", u"", vol_nav(v["num"]), u""]
    rel = []
    if v["related"]:
        rel = [u"## 相关笔记", u""] + [u"- [[%s]] —— %s" % (t, d) for t, d in v["related"]] + [u""]

    content = u"\n".join(head + dbody[:1] + [u"", vol_nav(v["num"]), u""] + dbody[1:] + rel + tail)
    write(os.path.join(DEST_DIR, v["fname"]), content)
    print(u"写出 %s（%d 字符 / %d 中文）" % (v["fname"], len(content), len(re.findall(u"[一-鿿]", content))))

# ---- 断言 4：双链目标真实存在 ----
links = set()
for v in VOLS:
    for t, _ in v["related"]:
        links.add(t)
for name in sorted(links):
    if glob.glob(name + u".md") or glob.glob(u"**/" + name + u".md", recursive=True):
        print(u"[OK]   双链目标存在：%s" % name)
    else:
        fail.append(name)
        print(u"[FAIL] 双链目标缺失：%s" % name)

# ---- 导出附录，供总目录内联 ----
appx_text = u"\n".join(lines[appx:])
write(u"workspace/smb-cifs-mount-linux/.cache/_appendix.md", appx_text)
print(u"附录导出：%d 行" % appx_text.count(u"\n"))

if fail:
    print(u"[FAIL] %d 条双链目标缺失，请先修正" % len(fail))
    sys.exit(1)
print(u"全部断言通过")
