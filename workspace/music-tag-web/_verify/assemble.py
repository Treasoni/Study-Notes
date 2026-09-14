"""P5 组装：把 8 个章节文件拼成 output/final_note.md。
- 代码块外的标题统一降一级（第 1 级留给整篇标题）
- 各章末的过渡语已是自包含的，不再新增散文
- 脚注 ID 已按章命名空间化，此处校验全文引用/定义配对与重复
"""
import sys, pathlib, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("workspace/music-tag-web")
CH = ROOT / "chapters"
OUT = ROOT / "output" / "final_note.md"

ORDER = [
    ("01-project-positioning.md", "第一章 项目定位与能力边界", "它解决什么问题、V1/V2 定位差别、能力边界与许可证要点。"),
    ("02-deployment.md", "第二章 部署（以 Docker Compose 为主）", "三个挂载卷、端口、重启策略、默认凭据，以及 NAS 差异小节（2.6）。"),
    ("03-first-login-activation.md", "第三章 首次登录、改密与 V2 激活", "打开界面、改默认密码、设 Subsonic 密码，以及 V2 激活这个必过门槛。"),
    ("04-tagging-workflow.md", "第四章 刮削与标签编辑主线", "写元数据还是写数据库、三种刮削、手动与批量改标签、变量与正则。"),
    ("05-organize-batch.md", "第五章 整理与批处理", "整理文件夹、简繁体转换、拆分文件名、切割音轨、批量重命名。"),
    ("appendix-a-playback.md", "附录 A 播放侧与生态（可跳读）", "Subsonic 服务端与客户端、Navidrome 联动、小爱音箱、网盘音乐、智能歌单。"),
    ("appendix-b-advanced-config.md", "附录 B 进阶配置（可跳读）", "MySQL、外置 Redis、自定义端口、自动更新与升级、多目录挂载、升级前检查清单。"),
    ("appendix-c-troubleshooting.md", "附录 C 排错 FAQ 与已知文档缺陷（可跳读）", "按故障簇排的排错、FAQ 精选、官方没说清的、官方文档自身缺陷清单。"),
]

TITLE = "如何使用 Music Tag Web（自托管音乐标签编辑器）"


def demote(text):
    """代码块外的标题降一级。"""
    out, in_code = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if not in_code:
            m = re.match(r"^(#{1,5})(\s)", ln)
            if m:
                ln = "#" + ln
        out.append(ln)
    return "\n".join(out)


def strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 3)
        if end != -1:
            return text[end + 5:].lstrip("\n")
    return text


def first_heading_level_note(text):
    return len(re.findall(r"^## ", text, re.M))


toc = ["## 目录", ""]
for i, (fn, heading, desc) in enumerate(ORDER, 1):
    toc.append("%d. [[#%s]] —— %s" % (i, heading, desc))
toc += [
    "",
    "> [!tip] 怎么读",
    "> 顺序读者走 1 → 5；NAS 用户把 2.6 插在 2.5 之后。附录按需跳读：**A** 播放与生态、**B** 进阶配置、**C** 排错。",
    "> 正文只讲「顺利用下去」，出错时直接翻附录 C。",
]

parts = [
    "---",
    "title: %s" % TITLE,
    "tags:",
    "  - 工具/music-tag-web",
    "  - 音乐管理",
    "  - Docker",
    "created: 2026-09-14",
    "updated: 2026-09-14",
    "status: draft",
    "source_project: workspace/music-tag-web",
    "---",
    "",
    "# %s" % TITLE,
    "",
    "> [!summary] 这篇笔记是什么",
    "> 一份面向**使用者**的上手/操作指南：怎么把这个自托管的音乐标签编辑器跑起来、登进去、把标签刮好改好、把文件整理归档。",
    "> 读者画像：**有 Docker 基础、但没用过这个项目**；深度到「上手」为止，不做源码剖析。",
    "> 它只编辑**本地已有**音乐文件的元数据，**不提供音乐下载**——这是项目自述的能力边界，细节见第一章。",
    "",
] + toc + ["", "---", ""]

for fn, heading, _ in ORDER:
    p = CH / fn
    body = strip_frontmatter(p.read_text(encoding="utf-8")).strip("\n")
    demoted = demote(body)
    parts.append(demoted)
    parts.append("")
    parts.append("---")
    parts.append("")

doc = "\n".join(parts).rstrip("\n") + "\n"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(doc, encoding="utf-8")

# ---- 校验 ----
han = len(re.findall(r"[一-鿿]", doc))
fns = re.findall(r"^\[\^([^\]]+)\]:", doc, re.M)
refs = re.findall(r"\[\^([^\]]+)\](?!:)", doc)
dup = sorted({f for f in fns if fns.count(f) > 1})
h1 = len(re.findall(r"^# ", doc, re.M))
h2 = len(re.findall(r"^## ", doc, re.M))
print("写出: %s" % OUT)
print("汉字 %d / bytes %d / H1 %d / H2 %d" % (han, len(doc.encode("utf-8")), h1, h2))
print("脚注定义 %d 个（唯一 %d）/ 引用 %d 处" % (len(fns), len(set(fns)), len(refs)))
if dup:
    print("!! 重复脚注定义:", dup)
print("引用但未定义:", sorted(set(refs) - set(fns)) or "无")
print("定义但未引用:", sorted(set(fns) - set(refs)) or "无")
