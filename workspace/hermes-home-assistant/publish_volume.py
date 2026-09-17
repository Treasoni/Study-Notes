#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6 发布：把 chapters/ 的 10 个源文件发布成 vault 里的一个分册。

目标形态严格对齐 `AI学习/Hermes Agent/` 下既有四分册的惯例：
    <vault>/AI学习/Hermes Agent/Hermes × Home Assistant 实战/
        README.md
        01-…md … 10-附录-核对清单与延伸阅读.md

每篇结构：frontmatter → 上一章/返回目录/下一章 导航行 → `# 标题` → 正文。

层级变换：源文件按「并入合集」的层级写（`## 第 N 章：标题` / `### N.x 小节` /
`### 本章小结`），发布成单篇要**整体升一级**（`# 标题` / `## N.x` / `## 本章小结`）。

设计约束：
- 正文只做「标题升一级」这一种变换，且必须可逆；脚本用逆变换断言逐字一致。
- 不改写任何正文句子、不动脚注机制、不新增来源论断。
- 双链落地前逐条校验：目标必须在 vault 中真实存在且唯一解析。
"""

import re
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "chapters"
VAULT = pathlib.Path(r"D:\Study-Notes")
VOL = "Hermes × Home Assistant 实战"
RELDIR = "AI学习/Hermes Agent/" + VOL
DEST = VAULT / RELDIR

# 链接一律用 vault 全文路径，不用短链。
# 原因：本 vault 的 `workspace/` 也在 vault 内部且被 Obsidian 索引，
# 章节源文件与发布件同名（`README` 更是有 30 处同名），短链解析到哪一个是不确定的。
LINK = RELDIR + "/"

CREATED = "2026-09-18"
TAGS = ["AI学习", "Agent", "Hermes", "HomeAssistant"]

# (源文件名, 目标文件名)
CH = [
    ("01-结论先行与能力地图.md", "01-结论先行与能力地图.md"),
    ("02-三方对照轴.md", "02-三方对照轴.md"),
    ("03-路线选型.md", "03-路线选型.md"),
    ("04-落地-社区ha-mcp.md", "04-落地-社区ha-mcp.md"),
    ("05-落地-官方mcp_server.md", "05-落地-官方mcp_server.md"),
    ("06-事件驱动与定时任务.md", "06-事件驱动与定时任务.md"),
    ("07-安全与限界.md", "07-安全与限界.md"),
    ("08-文档与代码不一致.md", "08-文档与代码不一致.md"),
    ("09-成本与可靠性.md", "09-成本与可靠性.md"),
    ("10-附录.md", "10-附录-核对清单与延伸阅读.md"),
]

# README 目录里的短标题（人工拟定，只用于目录显示，不进入正文）
SHORT = {
    "01-结论先行与能力地图.md": "结论先行与能力地图：4 个内置工具的天花板",
    "02-三方对照轴.md": "三方对照轴：什么该交给 agent，什么本来就该用自动化",
    "03-路线选型.md": "路线选型：自建 skill / MCP server / 自定义 plugin 何时用",
    "04-落地-社区ha-mcp.md": "落地（一）：用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）",
    "05-落地-官方mcp_server.md": "落地（二）：用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）",
    "06-事件驱动与定时任务.md": "事件驱动与定时任务：白名单过滤、逐实体限流、投递两条分支与 4096 截断",
    "07-安全与限界.md": "安全与限界：LLT 权限真相、暴露列表的真实效力、最小化清单",
    "08-文档与代码不一致.md": "文档与代码不一致：12 条实例与自查方法",
    "09-成本与可靠性.md": "成本与可靠性：工具 schema 常驻开销、误报机理、没有分母的误报率",
    "10-附录.md": "附录：实机核对清单、未解决问题与延伸阅读",
}

def _shift(text, delta):
    """fence 之外的标题层级平移 delta（负数为升一级）。"""
    out, infence = [], False
    for l in text.split("\n"):
        if l.lstrip().startswith("```"):
            infence = not infence
            out.append(l)
            continue
        if not infence:
            m = re.match(r"^(#{1,6})(\s+)(.*)$", l)
            if m:
                n = len(m.group(1)) + delta
                if n < 1:
                    raise SystemExit("!! 标题层级升过头：{!r}".format(l))
                out.append("#" * n + m.group(2) + m.group(3))
                continue
        out.append(l)
    return "\n".join(out)


def promote(text):
    return _shift(text, -1)


def unpromote(text):
    return _shift(text, +1)


def headings_outside_fences(text):
    """返回 fence 之外的标题行原文。"""
    out, infence = [], False
    for l in text.split("\n"):
        if l.lstrip().startswith("```"):
            infence = not infence
            continue
        if not infence and re.match(r"^#{1,6} ", l):
            out.append(l)
    return out


def split_title(raw, name):
    """拆出章标题行，返回 (纯标题, 剩余正文)。"""
    lines = raw.split("\n")
    if not lines[0].startswith("## ") or lines[0].startswith("### "):
        raise SystemExit("!! {} 首行不是 `## ` 标题：{!r}".format(name, lines[0][:60]))
    head = lines[0][3:].strip()
    title = re.sub(r"^第\s*[0-9一二三四五六七八九十]+\s*章[：:]\s*", "", head)
    return title, "\n".join(lines[1:]).strip("\n")


def frontmatter(title):
    return (
        "---\n"
        'title: "{}"\n'.format(title)
        + "tags:\n"
        + "".join("  - {}\n".format(t) for t in TAGS)
        + "created: {}\n".format(CREATED)
        + "updated: {}\n".format(CREATED)
        + "status: 已完成\n"
        + "source_project: hermes-home-assistant\n"
        + "---\n\n"
    )


def scan_vault():
    """vault 内所有 md 的 stem → 路径列表，用于双链唯一性校验。"""
    table = {}
    for p in VAULT.rglob("*.md"):
        posix = p.as_posix()
        if "/.obsidian/" in posix or "/.trash/" in posix or "/.claude/" in posix:
            continue
        table.setdefault(p.stem, []).append(p)
    return table


def main():
    outnames = [out for _, out in CH]
    stems = [out[:-3] for out in outnames]

    problems = []
    written = {}

    for i, (src_name, out_name) in enumerate(CH):
        raw = (SRC / src_name).read_text(encoding="utf-8").rstrip("\n")
        title, rest = split_title(raw, src_name)

        # 守卫：标题行之后不该再出现 `## ` 级标题，否则升级后会与篇标题撞级
        # （必须 fence 感知：第 3 章的 SKILL.md 示例代码里就有 `## When to Use`）
        stray = [l for l in headings_outside_fences(rest) if l.startswith("## ")]
        if stray:
            problems.append("{} 标题行之后仍有 `## ` 级标题：{}".format(src_name, stray[:2]))

        body_src = rest
        body = promote(body_src)
        fm = frontmatter(title)

        nav = []
        if i > 0:
            nav.append("[[{}{}|⬅ 上一章]]".format(LINK, stems[i - 1]))
        nav.append("[[{}README|📖 返回目录]]".format(LINK))
        if i < len(CH) - 1:
            nav.append("[[{}{}|下一章 ➡]]".format(LINK, stems[i + 1]))
        navline = "> " + " · ".join(nav)

        text = fm + navline + "\n\n# " + title + "\n\n" + body + "\n"

        # ---- 断言 1：层级平移必须可逆，保证正文一字未动 ----
        if unpromote(body) != body_src:
            problems.append("{} 标题层级变换不可逆（正文可能被改动）".format(src_name))

        # ---- 断言 2：标题清单（层级与文字）只允许整体升一级 ----
        # 必须 fence 感知：第 3 章的 SKILL.md 示例代码里含 `## When to Use`，
        # 朴素正则会把它算作标题，导致两侧层级比对错位。
        def hlevels(t):
            return [(len(l) - len(l.lstrip("#")), l.lstrip("# ").rstrip())
                    for l in headings_outside_fences(t)]

        if hlevels(body_src) != [(n + 1, s) for n, s in hlevels(body)]:
            problems.append("{} 标题清单不一致：{} vs {}".format(
                src_name, hlevels(body_src)[:3], hlevels(body)[:3]))

        # ---- 断言 3：脚注定义与引用数不变 ----
        d_src = re.findall(r"^\[\^([^\]]+)\]:", body_src, re.M)
        d_out = re.findall(r"^\[\^([^\]]+)\]:", body, re.M)
        r_src = re.findall(r"\[\^([^\]]+)\](?!:)", body_src)
        r_out = re.findall(r"\[\^([^\]]+)\](?!:)", body)
        if d_src != d_out:
            problems.append("{} 脚注定义在变换后变化：{} → {}".format(
                src_name, len(d_src), len(d_out)))
        if r_src != r_out:
            problems.append("{} 脚注引用在变换后变化：{} → {}".format(
                src_name, len(r_src), len(r_out)))

        # ---- 断言 4：fence 必须闭合 ----
        nf = sum(1 for l in body.split("\n") if l.lstrip().startswith("```"))
        if nf % 2:
            problems.append("{} fence 未闭合（{} 行）".format(src_name, nf))

        written[out_name] = (title, text, body_src)

    # ---- 全局断言：脚注 ID 不得跨章撞号 ----
    seen = {}
    for out_name, (_, text, _) in written.items():
        for d in re.findall(r"^\[\^([^\]]+)\]:", text, re.M):
            if d in seen:
                problems.append("脚注 ID 撞号：{}（{} 与 {}）".format(d, seen[d], out_name))
            seen[d] = out_name
    print("== 脚注 ==")
    print("  定义 {} 条（全局唯一）".format(len(seen)))

    # ---- 全局断言：双链目标必须存在且唯一解析 ----
    # 先把「本次将要写出的文件」并入视野，再校验——否则会误报新文件不存在。
    stem_table = scan_vault()
    planned = {out_name for _, out_name in CH} | {"README.md"}

    # 全部待发布文本都参与链接收集——README 也必须扫，否则「相关笔记」那几条
    # 跨界链接（最该验的一批）会整批漏检。
    all_texts = {out_name: text for out_name, (_, text, _) in written.items()}
    all_texts["README.md"] = readme(outnames)

    link_report = []
    targets = {}
    for out_name, text in all_texts.items():
        for t in re.findall(r"\[\[([^\]|#]+)", text):
            targets.setdefault(t.strip(), set()).add(out_name)

    for target in sorted(targets):
        where = ",".join(sorted(targets[target]))
        if "/" in target:
            rel = target + ".md"
            ok = (VAULT / rel).is_file() or rel in planned
            link_report.append((target, "全文路径", "OK" if ok else "缺失", where))
            if not ok:
                problems.append("双链目标不存在：[[{}]]（出自 {}）".format(target, where))
        else:
            hits = stem_table.get(target, [])
            if len(hits) == 1:
                link_report.append((target, "短链", "OK", where))
            elif not hits:
                link_report.append((target, "短链", "缺失", where))
                problems.append("双链目标不存在：[[{}]]（出自 {}）".format(target, where))
            else:
                link_report.append((target, "短链", "歧义 {} 处".format(len(hits)), where))
                problems.append("双链 [[{}]] 在 vault 中 {} 处同名，解析不确定（出自 {}）".format(
                    target, len(hits), where))

    # ---- 写盘 ----
    DEST.mkdir(parents=True, exist_ok=True)
    for out_name, (_, text, _) in written.items():
        (DEST / out_name).write_text(text, encoding="utf-8", newline="\n")
    (DEST / "README.md").write_text(readme(outnames), encoding="utf-8", newline="\n")

    # ---- 回读校验 ----
    for out_name, (_, text, _) in written.items():
        if (DEST / out_name).read_text(encoding="utf-8") != text:
            problems.append("{} 回读不一致".format(out_name))

    print()
    print("== 发布 ==")
    print("  目标目录  {}".format(DEST))
    print("  文件      {} 篇 + README.md".format(len(CH)))
    print()
    print("== 双链目标校验（{} 个去重目标，含 README） ==".format(len(link_report)))
    for target, kind, status, where in link_report:
        mark = "  OK  " if status == "OK" else "  !!  "
        short = target if len(target) <= 62 else "…" + target[-61:]
        print("{}{:<64} {:<8} {}".format(mark, short, kind, status))
    print()
    if problems:
        print("!! 断言未通过：")
        for p in problems:
            print("   - {}".format(p))
        raise SystemExit(1)
    print("所有断言通过。")


def readme(outnames):
    fm = frontmatter("Hermes × Home Assistant 实战")
    toc = "\n".join(
        "{}. [[{}{}|{}]]".format(i + 1, LINK, outnames[i][:-3], SHORT[src])
        for i, (src, _) in enumerate(CH)
    )
    return fm + """# Hermes × Home Assistant 实战

你已经让 Hermes 连上了 Home Assistant——`HASS_TOKEN` 配好、会话里四个 `ha_*` 工具能正常调用。这份分册回答的是下一步：**这四个工具究竟能把你带到哪儿、从哪一步开始必须换一条路走、换路之后哪条更值得走**。

全篇按「能力地图 → 选型 → 两条落地路线 → 事件与定时 → 安全 → 文档与代码不一致 → 成本」的顺序展开，九章正文加一个附录。两条 MCP 路线是分开写的：社区 ha-mcp 有官方模板可以照抄，HA 官方 `mcp_server` 没有 Hermes 示例、那份配置是按端点规格拼的，**性质差异在正文里逐处标注**。

## 目录

{toc}

## 怎么读

- **只想看结论**：第 1 章给全部结论，第 2 章给「什么该交给 agent、什么该留给确定性自动化」的判据表。
- **准备动手**：第 3 章定路线，第 4 章（照抄）或第 5 章（拼接，需自行验证）落地。
- **已经跑起来了**：第 6 章讲事件与定时任务里三个文档没写透的坑；第 7 章是最小化清单。
- **在意可信度**：第 8 章把 12 处「文档和代码不一致」逐条举证；第 9 章把成本与误报率的举证性质标回原样。

关于引用纪律：每条事实性结论都标注来源档位（官方文档 / 一手源码 / 社区自报），官方原文、源码事实与本册推论分开写。附录 B 集中列出全部未解决问题及其分级——**没写死的地方没有被写死**。

## 相关笔记

- [[AI学习/Hermes Agent/Hermes Agent 上手实战/06-多平台接入与定时任务|上手实战 06：Home Assistant 双向接入]] —— LLT 怎么建、四个 `ha_*` 工具怎么用、`watch_domains` 白名单、事件转发默认全关。本册不重述，只引用。
- [[AI学习/Hermes Agent/Hermes Tool 配置指南/README|Hermes Tool 配置指南]] —— 工具怎么配、MCP 怎么接、Tool Gateway 与权限审批。
- [[AI学习/Hermes Agent/Hermes Agent MOC|Hermes Agent MOC]] —— Hermes 系列全部分册的索引。
- [[homeassistant/Home Assistant MOC|Home Assistant MOC]] —— HA 侧的部署、集成与自动化笔记。
- [[homeassistant/ai-smart-home-system/06_AI智能体FastAPI与DeepSeek|自建 AI 智能体（FastAPI + DeepSeek）]] —— 除 Hermes 与 HA 内建 LLM 之外的第三条 agent 路线，可作第 2 章对照轴的实例。
""".format(toc=toc)


if __name__ == "__main__":
    main()
