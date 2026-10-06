"""P6 分册发布：把 output/final_note.md 切成 9 个册文件（总目录 + 8 册），
写入项目 output/series/ 暂存，再复制到 vault 的 docker/MusicTagWeb音乐标签/。

体例对齐 vault 内既有分册 docker/OpenList网盘挂载/：
  - 册文件 frontmatter: title / tags / created / updated / status / source_project / series / volume
  - 正文首行 H1，紧跟 `> 🧭 分册导航` 一行
  - 册尾统一：`## 下一册预告` + 过渡段 → `## 参考来源` + 脚注定义 → `---` → 分册导航
  - 总目录 `MusicTagWeb-00-总目录`：一句话 + 分册导航表
不变式：
  - 各册正文必须与 output/final_note.md 的对应切片逐字一致（只做标题降级还原 + 尾部分节标题）
  - 第 1 册的行内引注 [D6](url) 转成与其余各册一致的脚注体例，URL 逐字保留
  - 本地清理只删本脚本自己产出的 MusicTagWeb-*.md
  - 所有 wikilink 目标必须先验存在
"""
import re, sys, pathlib, shutil, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("workspace/music-tag-web")
FINAL = ROOT / "output" / "final_note.md"
STAGE = ROOT / "output" / "series"
VAULT_DIR = pathlib.Path("docker/MusicTagWeb音乐标签")
CH_DIR = ROOT / "chapters"

SERIES = "MusicTagWeb音乐标签"
SERIES_LONG = "MusicTagWeb 自托管音乐标签编辑器实战"
PREFIX = "MusicTagWeb"
DATE = "2026-09-14"
BASE_TAGS = ["Docker", "MusicTagWeb", "音乐管理", "实战笔记", SERIES]

# (序号, 文件名短名, 册标题, 总目录一句话, chapters 源, 相关笔记, 末段小标题)
VOLS = [
    ("01", "项目定位与能力边界", "项目定位与能力边界",
     "它解决什么问题、V1/V2 定位差别、能力边界与许可证要点。",
     "01-project-positioning.md",
     ["[[Docker MOC]] —— 本分册的上级索引"], "下一册预告"),
    ("02", "部署", "部署（以 Docker Compose 为主）",
     "三个挂载卷、端口、重启策略、默认凭据，以及 NAS 差异小节（2.6）。",
     "02-deployment.md",
     ["[[Docker与DockerCompose命令速查]] —— 本册用到的 Compose 字段在这里查",
      "[[Docker网络结构详解]] —— 端口映射与 bridge/host 的网络模型",
      "[[docker里的GID和UID]] —— 挂载目录读写权限对不上时看这篇",
      "[[Docker容器服务访问宿主机文件]] —— 把音乐目录映射进容器的两种做法"], "下一册预告"),
    ("03", "首次登录与激活", "首次登录、改密与 V2 激活",
     "打开界面、改默认密码、设 Subsonic 密码，以及 V2 激活这个必过门槛。",
     "03-first-login-activation.md",
     ["[[Docker网络结构详解]] —— 激活失败时「换 host 网络」背后的模型"], "下一册预告"),
    ("04", "刮削与标签编辑", "刮削与标签编辑",
     "写元数据还是写数据库、三种刮削、手动与批量改标签、变量与正则。",
     "04-tagging-workflow.md",
     ["[[docker里的GID和UID]] —— 写回元数据时文件属主不对会静默失败"], "下一册预告"),
    ("05", "整理与批处理", "整理与批处理",
     "整理文件夹、简繁体转换、拆分文件名、切割音轨、批量重命名。",
     "05-organize-batch.md",
     ["[[docker里的GID和UID]] —— 批量移动/重命名后的属主问题"], "下一册预告"),
    ("06", "附录A-播放侧与生态", "附录 A 播放侧与生态",
     "Subsonic 服务端与客户端、Navidrome 联动、小爱音箱、网盘音乐、智能歌单。",
     "appendix-a-playback.md",
     ["[[qBittorrent的使用]] —— 同为自托管媒体服务，下载侧的对照读物",
      "[[Docker与DockerCompose命令速查]] —— 联动容器时的编排字段"], "下一册预告"),
    ("07", "附录B-进阶配置", "附录 B 进阶配置",
     "MySQL、外置 Redis、自定义端口、自动更新与升级、多目录挂载、升级前检查清单。",
     "appendix-b-advanced-config.md",
     ["[[docker容器如何更新]] —— 本册「自动更新与升级」一节的展开版",
      "[[Docker与DockerCompose命令速查]] —— MySQL/Redis 的编排写法"], "下一册预告"),
    ("08", "附录C-排错与FAQ", "附录 C 排错与 FAQ",
     "按故障簇排的排错、FAQ 精选、官方没说清的、官方文档自身缺陷清单。",
     "appendix-c-troubleshooting.md",
     ["[[docker容器搭建错误的知识讲解]] —— 容器起不来时的通用排查思路",
      "[[docker镜像拉取DNS解析超时排错]] —— 拉镜像阶段的网络故障",
      "[[docker里的GID和UID]] —— 权限类故障的通用解法"], "写在最后"),
]

C1_NAMES = {
    "d1": "V2 项目介绍（官方）",
    "d5": "V2 名词解释（官方）",
    "d6": "V1 项目介绍（官方）",
    "f4": "V2 怎么更新升级版本呢（官方）",
    "t17": "V1 手册页面树（llms.txt）",
    "t18": "V2 手册页面树（llms.txt）",
}
CITE_RE = re.compile(r"\[([A-Za-z]+\d+)\]\((https?://[^)\s]+)\)")
TOC = "MusicTagWeb-00-总目录"


def stem(num, short):
    return "%s-%s-%s" % (PREFIX, num, short)


def demote(text):
    out, in_code = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            out.append(ln); continue
        if not in_code and re.match(r"^(#{1,5})(\s)", ln):
            ln = "#" + ln
        out.append(ln)
    return "\n".join(out)


def promote(text):
    out, in_code = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            out.append(ln); continue
        if not in_code and re.match(r"^(#{2,6})(\s)", ln):
            ln = ln[1:]
        out.append(ln)
    return "\n".join(out)


def split_body_and_footnotes(text):
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if re.match(r"^\[\^[^\]]+\]:", ln):
            return "\n".join(lines[:i]).rstrip("\n"), "\n".join(lines[i:]).strip("\n")
    return text, ""


def prep_target_dirs():
    """只清掉本脚本自己产出的文件。"""
    for d in (STAGE, VAULT_DIR):
        if not d.exists():
            continue
        foreign = [p for p in d.iterdir() if p.suffix == ".md" and not p.name.startswith(PREFIX)]
        if foreign:
            raise SystemExit("!! %s 内有非本脚本产物，拒绝清理：%s" % (d, [p.name for p in foreign]))
        for p in d.glob("%s-*.md" % PREFIX):
            p.unlink()
    STAGE.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)


prep_target_dirs()

# ---------- 1. 读组装稿，按章标题切片 ----------
final = FINAL.read_text(encoding="utf-8")
doc_body = final[final.index("\n---\n", final.index("# 如何使用")) + len("\n---\n"):]
marks = list(re.finditer(r"^## (第[一二三四五]章 .+|附录 [ABC] .+)$", doc_body, re.M))
if len(marks) != 8:
    raise SystemExit("!! 切片锚点数 %d != 8" % len(marks))
slices = {}
for i, m in enumerate(marks):
    end = marks[i + 1].start() if i + 1 < len(marks) else len(doc_body)
    slices[i] = re.sub(r"\n---\s*$", "", doc_body[m.start():end].rstrip("\n")).rstrip("\n")

# ---------- 2. 与章节源文件逐字校对 ----------
print("=== 组装稿切片 vs 章节源文件 ===")
for i, (num, short, title, desc, src, rel, th) in enumerate(VOLS):
    src_text = (CH_DIR / src).read_text(encoding="utf-8")
    if src_text.startswith("---\n"):
        src_text = src_text[src_text.index("\n---\n", 3) + 5:].lstrip("\n")
    if demote(src_text.strip("\n")).strip() != slices[i].strip():
        raise SystemExit("!! 第 %s 册切片与源文件不一致，停止发布" % num)
    print("  %s %-22s 一致" % (num, title))

# ---------- 3. 生成各册 ----------
written, total_han = [], 0
prev_link = "[[%s]]" % TOC

for i, (num, short, title, desc, src, rel, tail_head) in enumerate(VOLS):
    body = promote(slices[i])
    h1 = body.splitlines()[0]
    if not h1.startswith("# "):
        raise SystemExit("!! 第 %s 册首行不是 H1: %s" % (num, h1))
    body = "# " + h1[2:].replace("（可跳读）", "") + body[len(h1):]

    if num == "01":
        codes = collections.OrderedDict((c.lower(), u) for c, u in CITE_RE.findall(body))
        n_ref = len(CITE_RE.findall(slices[i]))
        body, _ = split_body_and_footnotes(body)
        body = CITE_RE.sub(lambda m: "[^c1-%s]" % m.group(1).lower(), body)
        defs = ["[^c1-%s]: %s — <%s>" % (k, C1_NAMES[k], codes[k]) for k in sorted(codes)]
        body = body.rstrip("\n") + "\n\n" + "\n".join(defs)
        print("\n第 1 册引注转换：%d 处行内引注 → %d 个脚注定义" % (n_ref, len(defs)))

    # 尾部统一：过渡段 + 恰好一个 ## 参考来源
    core, foot = split_body_and_footnotes(body)
    core = re.sub(r"(\n\s*## 参考来源\s*)+$", "", core.rstrip("\n"))
    paras = [p for p in re.split(r"\n\s*\n", core) if p.strip()]
    if paras and not paras[-1].lstrip().startswith(("#", ">", "|", "-", "[^")):
        trans = paras[-1]
        head = core[: core.rindex(trans)].rstrip("\n")
        core = "%s\n\n## %s\n\n%s" % (head, tail_head, trans.strip())
        note = "过渡段 → 「## %s」" % tail_head
    else:
        note = "无独立过渡段"
    if foot:
        core = core.rstrip("\n") + "\n\n## 参考来源"
        note += "；补「## 参考来源」"
    body = core.rstrip("\n") + ("\n\n" + foot if foot else "")
    print("  %s %s" % (num, note))

    nxt = ("[[%s]]" % stem(VOLS[i + 1][0], VOLS[i + 1][1])) if i + 1 < len(VOLS) else None
    bits = ["总目录：[[%s]]" % TOC]
    if i > 0:
        bits.append("上一册：%s" % prev_link)
    if nxt:
        bits.append("下一册：%s" % nxt)
    nav = "> 🧭 分册导航 ｜ " + " ｜ ".join(bits)

    fm = ["---", "title: %s · 第 %s 册 %s" % (PREFIX, num.lstrip("0"), title), "tags:"] \
        + ["  - %s" % t for t in BASE_TAGS] \
        + ["created: %s" % DATE, "updated: %s" % DATE, "status: 已完成",
           "source_project: workspace/music-tag-web", "series: %s" % SERIES_LONG,
           "volume: %s/8" % num.lstrip("0"), "---", ""]
    first, rest = body.split("\n", 1)
    rel_block = ("\n\n## 相关笔记\n\n" + "\n".join("- %s" % r for r in rel)) if rel else ""
    doc = "\n".join(fm) + first + "\n\n" + nav + "\n\n" + rest.lstrip("\n")
    doc = doc.rstrip("\n") + rel_block + "\n\n---\n\n" + nav + "\n"

    path = STAGE / ("%s.md" % stem(num, short))
    path.write_text(doc, encoding="utf-8")
    shutil.copyfile(path, VAULT_DIR / path.name)
    han = len(re.findall(r"[一-鿿]", doc))
    total_han += han
    written.append((path.name, han, len(doc.encode("utf-8"))))
    prev_link = "[[%s]]" % stem(num, short)

# ---------- 4. 总目录 ----------
rows = ["| 册 | 标题 | 解决什么问题 |", "|---|---|---|"]
for num, short, title, desc, _, _, _ in VOLS:
    rows.append("| %s | [[%s]] | %s |" % (num.lstrip("0"), stem(num, short), desc))
toc_doc = ["---", "title: %s · 总目录" % PREFIX, "tags:"] \
    + ["  - %s" % t for t in BASE_TAGS] + ["  - 索引",
      "created: %s" % DATE, "updated: %s" % DATE, "status: 已完成",
      "source_project: workspace/music-tag-web", "series: %s" % SERIES_LONG, "---", "",
      "# Music Tag Web 自托管音乐标签编辑器实战", "",
      "> **一句话**：在自己机器上跑一个网页版的音乐标签编辑器，把已有音乐文件的标题、艺术家、专辑、封面、歌词批量刮削和整理好——**它只改你已有的文件，不提供音乐下载**。",
      "",
      "本分册共 8 册：**5 册正文**按第一次上手的操作顺序编排，**3 册附录**按需跳读。",
      "读者画像：有 Docker 基础、但没用过这个项目；深度到「上手」为止，不做源码剖析。",
      "",
      "> [!tip] 怎么读",
      "> 顺序读者走 1 → 5；NAS 用户把第 2 册的 2.6 小节插在 2.5 之后看。",
      "> 附录按需翻：**A** 播放与生态、**B** 进阶配置、**C** 排错 FAQ。正文只讲「顺利用下去」，出错时直接跳第 8 册。",
      "", "---", "", "## 分册导航", ""] + rows + [
      "", "---", "", "## 能力边界（先记住这一条）", "",
      "> [!warning] 它不做什么",
      "> 只编辑**本地已有**音乐文件的元数据，**不提供音乐下载**。这是项目自述的能力边界，细节见第 1 册。",
      "", "---", "", "## 相关笔记", "", "- [[Docker MOC]] —— 本分册的上级索引",
      "", "---", "", "> 🧭 分册导航 ｜ 下一册：[[%s]]" % stem("01", VOLS[0][1]), ""]
toc_path = STAGE / ("%s.md" % TOC)
toc_path.write_text("\n".join(toc_doc) + "\n", encoding="utf-8")
shutil.copyfile(toc_path, VAULT_DIR / toc_path.name)

# ---------- 5. 校验 ----------
print("\n=== 写出 ===")
toc_han = len(re.findall(r"[一-鿿]", toc_path.read_text(encoding="utf-8")))
print("  %-42s 汉字 %5d / %6d bytes" % (toc_path.name, toc_han, toc_path.stat().st_size))
for n, han, b in written:
    print("  %-42s 汉字 %5d / %6d bytes" % (n, han, b))
print("  册文件合计汉字 %d（组装稿 %d，差 %+d = 新增标题/导航）"
      % (total_han, len(re.findall(r"[一-鿿]", final)),
         total_han - len(re.findall(r"[一-鿿]", final))))

print("\n=== 各册脚注配对 / 结尾体例 ===")
bad = 0
for p in sorted(STAGE.glob("*.md")):
    t = p.read_text(encoding="utf-8")
    fns = re.findall(r"^\[\^([^\]]+)\]:", t, re.M)
    refs = re.findall(r"\[\^([^\]]+)\](?!:)", t)
    und, unr, dup = sorted(set(refs) - set(fns)), sorted(set(fns) - set(refs)), sorted({f for f in fns if fns.count(f) > 1})
    navs = re.findall(r"^> 🧭 分册导航 ｜ .+$", t, re.M)
    tail_ok = (p.stem == TOC) or (len(navs) == 2 and t.rstrip().endswith(navs[-1]))
    n_ref = t.count("\n## 参考来源")
    ref_ok = (n_ref == 0) if p.stem == TOC else (n_ref == 1 and fns)
    gap_ok = ("\n\n## 相关笔记" in t) and ("\n\n## 参考来源" in t or p.stem == TOC)
    if und or unr or dup or not tail_ok or not ref_ok or not gap_ok:
        bad += 1
    print("  %-42s 定义%2d 引用%2d 未定义%s 未引用%s 重复%s 导航%d 参考来源%d 尾对齐%s 空行%s"
          % (p.name, len(fns), len(refs), und or "-", unr or "-", dup or "-",
             len(navs), n_ref, "OK" if tail_ok else "!!",
             "OK" if (gap_ok and ref_ok) else "!!"))
print("  异常册数：%d" % bad)

print("\n=== wikilink 目标存在性 ===")
skip = (".git", ".obsidian", ".claude", ".codex", ".agents", "workspace", ".smart-env", ".llm")
vault_md = {p.stem for p in pathlib.Path(".").rglob("*.md") if not any(s in p.parts for s in skip)}
missing = []
for p in sorted(list(STAGE.glob("*.md")) + list(VAULT_DIR.glob("*.md"))):
    for tgt in set(re.findall(r"\[\[([^\]|#]+)", p.read_text(encoding="utf-8"))):
        if tgt.strip().rstrip(".md") not in vault_md:
            missing.append((p.name, tgt))
print("  死链：%s" % (sorted(set(missing)) or "无"))
print("\n暂存：%s\n发布：%s" % (STAGE, VAULT_DIR))
