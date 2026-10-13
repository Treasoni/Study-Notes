#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6 发布：把 chapters/0*.md 发布成 vault 分册（README + 编号章节）。

本脚本是**纯机械变换层**：不改内容、不改引文、不改措辞，只做三件事
  1) 每个章文件前加 frontmatter + 导航行；
  2) 正文 ATX 标题层级整体下移一级（`## 第 N 章` → `# 第 N 章`，`### N.M` → `## N.M`），
     与 vault 既有分册一致（该层级差异正是校验器 chapter_block 明示抹平的「④ 标题层级下沉」）；
  3) 由 output/final_note.md 的前言切片生成 README 入口页。
代码围栏内的 `#` 注释不参与层级变换（按围栏状态判定）。

自检（任一失败即抛错、不产出文件）：
  A 变换可逆：把成品正文逆向还原（标题各加回一个 `#`）后与源章文件逐字相等；
  B 源文件本身满足最终形态：正文标题只出现 `##` / `###`，无 `####`；
  C 引文对照数据行数在源/成品两侧一致（8/5/5/5/6/4）；
  D 每个成品的导航与 README 目录指向的目标文件真实存在。
"""
import pathlib, re, sys

ROOT = pathlib.Path("/Users/zhqznc/Documents/项目")
PROJ = ROOT / "workspace/searxng-hermes"
CH_DIR = PROJ / "chapters"
FINAL = PROJ / "output/final_note.md"
VAULT_DIR = ROOT / "AI学习/Hermes Agent/SearXNG 自托管指南"

TODAY = "2026-10-07"
SOURCE_PROJECT = "searxng-hermes"
TAGS = ["AI学习", "Agent", "Hermes", "SearXNG", "自托管"]

# (章号, 源文件, 成品文件名, 引文对照数据行数)
CH = [
    (1, "01_searxng-what.md",        "01-SearXNG是什么与隐私模型",        8),
    (2, "02_docker-setup.md",        "02-动手用Docker把SearXNG跑起来",   5),
    (3, "03_enable-json.md",         "03-开启JSON-API",                  5),
    (4, "04_hermes-integration.md",  "04-接入Hermes",                    5),
    (5, "05_verify-troubleshoot.md", "05-验证与排错",                    6),
    (6, "06_advanced.md",            "06-进阶可选",                      4),
]

FENCE = re.compile(r"^\s*(```|~~~)")
HEAD = re.compile(r"^(#{2,3})\s+(.*)$")
ROW = re.compile(r"^\|\s*\d+\s*\|")


def shift_headings(lines):
    """正文标题层级下移一级；代码围栏内的行不动。返回 (新行列表, 变换行数)。"""
    out, in_fence, n = [], False, 0
    for l in lines:
        if FENCE.match(l):
            in_fence = not in_fence
            out.append(l)
            continue
        m = None if in_fence else HEAD.match(l)
        if m:
            out.append(l[1:])           # 去掉一个 '#'
            n += 1
        else:
            out.append(l)
    return out, n


def unshift_headings(lines):
    """逆向：对同样的标题行加回一个 '#'。"""
    out, in_fence = [], False
    for l in lines:
        if FENCE.match(l):
            in_fence = not in_fence
            out.append(l)
            continue
        m = None if in_fence else HEAD.match(l)
        out.append("#" + l if m else l)
    return out


def fm(title):
    return ("---\n"
            'title: "%s"\n'
            "tags:\n" % title
            + "".join("  - %s\n" % t for t in TAGS)
            + "created: %s\nupdated: %s\nstatus: 已完成\nsource_project: %s\n---\n"
            % (TODAY, TODAY, SOURCE_PROJECT))


def main():
    fails = []

    # ---------- 读源章 ----------
    src = {}
    for num, fn, outname, rows in CH:
        p = CH_DIR / fn
        if not p.is_file():
            print("缺少源章文件：%s" % p); return 2
        src[num] = p.read_text(encoding="utf-8")

    # ---------- 自检 B：源文件标题只到 ### ----------
    for num, fn, outname, rows in CH:
        if re.search(r"^#{4,}\s", src[num], re.M):
            fails.append("B 源章 %s 出现 >=#### 标题" % fn)

    # ---------- 构造成品 ----------
    titles, bodies, files = {}, {}, {}
    for i, (num, fn, outname, exp_rows) in enumerate(CH):
        lines = src[num].split("\n")
        h1 = lines[0]                       # `## 第 N 章：…`
        assert h1.startswith("## 第"), (fn, h1)
        titles[num] = h1[3:]                # 去 '## ' → `第 N 章：…`
        body = lines[1:]
        # 去掉紧跟标题的空行，统一由拼装时补一个空行
        while body and not body[0].strip():
            body.pop(0)

        shifted, n_shift = shift_headings(body)

        # 自检 A（正向即逆向）：还原后必须与源正文逐字相等
        if unshift_headings(shifted) != body:
            fails.append("A 章 %d 标题层级变换不可逆" % num)

        # 自检 C：引文对照数据行数
        n_rows = sum(1 for l in body if ROW.match(l))
        if n_rows != exp_rows:
            fails.append("C 章 %d 引文对照数据行数 %d != %d" % (num, n_rows, exp_rows))

        nav = []
        if i > 0:
            nav.append("[[%s|⬅ 上一章]]" % CH[i - 1][2])
        nav.append("[[README|📖 返回目录]]")
        if i + 1 < len(CH):
            nav.append("[[%s|下一章 ➡]]" % CH[i + 1][2])
        navline = "> " + " · ".join(nav)

        text = (fm(titles[num]) + "\n" + navline + "\n\n# " + titles[num] + "\n\n"
                + "\n".join(shifted).rstrip("\n") + "\n")
        files[outname + ".md"] = text
        bodies[num] = shifted

    # ---------- README ----------
    final_lines = FINAL.read_text(encoding="utf-8").split("\n")
    i0 = next(i for i, l in enumerate(final_lines) if l.startswith("> [!summary]"))
    i1 = next(i for i, l in enumerate(final_lines) if l.strip() == "## 目录")
    preface = "\n".join(final_lines[i0:i1]).rstrip("\n")

    toc = "\n".join(
        "%d. [[%s|%s]]" % (num, outname, titles[num])
        for num, fn, outname, rows in CH)

    readorder = """```
01 是什么 → 02 搭起来 → 03 开 JSON → 04 接 Hermes → 05 验证排错 → 06 进阶可选
```

- **只想尽快接上 Hermes（最省事）**：01 → 02 的**路径①** → 03 → 04 → 05。
- **想跟着上游官方走**：02 的**路径②**（双服务 `core` + `valkey`）+ 06 的升级与钉版本。
- **想调引擎/端口/公共实例**：直接看 06，前五章跑通后它是可选的。
- **只想知道为什么值得自托管**：01 + 05.4（`web_extract` 不走 SearXNG 的边界）。"""

    rel = """| 分册 | 主题 | 入口 |
|------|------|------|
| [[Hermes Agent 上手实战/README|上手实战]] | 定位、安装、模型、记忆、技能、多平台、委派、Docker 部署 | 10 章 + 附录 |
| [[Hermes Docker 部署指南/README|Docker 部署]] | Hermes 自身怎么用 Docker 常驻，以及国内消息平台接入 | 11 章 |
| **本册（SearXNG 自托管）** | 把**搜索后端**换成本地自托管实例：是什么、怎么搭、怎么接、怎么验证 | 6 章 |

本册只解决「搜索这一条链路」：SearXNG 提供搜索，Hermes 通过 `SEARXNG_URL` 消费它。它与《Docker 部署指南》互补——那册讲 Hermes 自身怎么容器化，本册讲 Hermes **依赖的一个外部服务**怎么容器化。"""

    quick = """```bash
docker compose up -d                       # 起 SearXNG 实例；配置目录已挂到宿主（第 2 章）
# 直接编辑宿主上的 settings.yml，在 search.formats 里补上 json，再重启容器（第 3 章）
curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c \\
  "import sys,json; print(len(json.load(sys.stdin)[\\"results\\"]), 'results')"   # 第 5 章自检
# Hermes 侧：设 SEARXNG_URL 指向宿主端口，web.search_backend 设为 searxng（第 4 章）
```"""

    hist = """- **2026-10-07**：新分册《SearXNG 自托管指南》发布，6 章独立笔记 + README 入口；由 `learning-note-flow` 工作流产出（run `searxng-hermes`），并同步更新 [[Hermes Agent MOC]]。"""

    readme = (fm("SearXNG 自托管指南") + "\n# SearXNG 自托管指南\n\n"
              + "本册讲一件事：**把 SearXNG 这个元搜索引擎自托管在你自己的机器上，再用一个环境变量 `SEARXNG_URL` 把它接给 Hermes Agent**。六章从「它是什么」一路走到「接通了、验证过、出问题知道怎么查」。\n\n"
              + preface + "\n\n## 目录\n\n" + toc + "\n\n## 阅读顺序\n\n" + readorder
              + "\n\n## 与其他分册的关系\n\n" + rel
              + "\n\n## 快速上手\n\n" + quick
              + "\n\n## 更新记录\n\n" + hist)
    files["README.md"] = readme

    # ---------- 自检 D：导航 / TOC 目标存在 ----------
    targets = set(files)          # 键已是含扩展名的文件名
    for name, text in files.items():
        for link in re.findall(r"\[\[([^\]|#]+)", text):
            if link == "Hermes Agent MOC":
                if not (ROOT / "AI学习/Hermes Agent/Hermes Agent MOC.md").is_file():
                    fails.append("D README 指向的 MOC 不存在")
                continue
            if "/" in link:      # 指向其它分册
                if not (ROOT / "AI学习/Hermes Agent" / (link.split("|")[0] + ".md")).is_file():
                    fails.append("D %s 指向的分册不存在：%s" % (name, link))
                continue
            if link + ".md" not in targets:
                fails.append("D %s 导航目标不存在：%s" % (name, link))

    if fails:
        print("❌ 自检未通过，未写出任何文件：")
        for f in fails:
            print("  -", f)
        return 1

    # ---------- 写出 ----------
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    print("源章 → 成品（字节数）")
    for outname, text in files.items():
        p = VAULT_DIR / outname
        if p.exists():
            print("⚠ 已存在，覆盖：%s" % p)
        p.write_text(text, encoding="utf-8")
        print("  %-42s %6d B" % (outname, len(text.encode("utf-8"))))

    print("\n✅ 自检全过：A 可逆 / B 源形态 / C 引文对照行数 / D 导航目标")
    print("预期引文对照行数：", " / ".join("ch%d=%d" % (n, r) for n, _, _, r in CH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
