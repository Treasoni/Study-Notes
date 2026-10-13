#!/usr/bin/env python3
"""把 output/final_note.md 切成 Obsidian 分册发布集（章文件 + MOC + sortspec）。

对齐全 vault 既有先例 `AI学习/REA 逆向工程/`：
  01-….md … NN-….md + `<主题> MOC.md` + sortspec.md

变换是**纯包装**：章正文自 H1 起逐字不变；每份章文件只在其**前后**加包装——
  frontmatter + 顶部导航栏（H1 之前，落在比对切片之外）
  末尾「---  + `> 📖 返回目录` 导航尾行」（校验器 `FOOTER` 认得 `> 📖`，比对时截断）
因此 `note-citation-check.py` 的 C 门仍应判「章文件 == 分册成品」。

用法：
  python3 publish_split.py --src workspace/ai-jailbreak/output/final_note.md \
                           --out <发布目录> [--topic "AI 破甲"] [--date 2026-10-13]
"""
import argparse
import pathlib
import re
import sys

CHAPTER_HEAD = re.compile(r"^# 第\s*(\d+)\s*章[：:]\s*(.+?)\s*$")
PAREN = re.compile(r"[（(][^（()）]*[）)]")
TAGS = ["AI学习", "AI安全", "破甲", "越狱", "LLM安全"]

# 每章一句「讲什么」，取自 final_note 目录行（不新造论断）
ABOUT = {
    1: "给「破甲」下定义，并把它和提示注入、红队、对齐三个近邻切开",
    2: "解释对齐为什么挡不住破甲——它只是「轻推一把」，不是「上锁」",
    3: "从机制层把破甲归成几类，只讲「凭什么能钻空子」，不含任何可照做的载荷",
    4: "讲防御——检测、训练期与运行期护栏、评测口径与治理",
    5: "全篇术语、判据、数字与出处的回查页，不引入新概念",
}
SUMMARY = (
    "**AI 破甲（jailbreak，也译「越狱」）** 就是想办法让一个被训练成「危险内容不开口」的模型，"
    "把那些它本该拒绝的话**说出来**。本册子从安全视角依次回答三个问题——它是什么、为什么防不住、"
    "在机制层是怎么被绕过的；**只讲机制、分类、原理与防御，不含任何可照做的载荷或配方**。"
)


def split_chapters(text):
    """→ [(编号, 副标题, 正文含 H1)]，正文逐字保留。"""
    lines = text.split("\n")
    heads = [(i, CHAPTER_HEAD.match(l)) for i, l in enumerate(lines)]
    heads = [(i, m) for i, m in heads if m]
    out = []
    for n, (i, m) in enumerate(heads):
        stop = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        body = lines[i:stop]
        while body and not body[-1].strip():          # 去掉尾部空行
            body.pop()
        while body and not body[0].strip():           # 去掉首部空行
            body.pop(0)
        out.append((int(m.group(1)), m.group(2).strip(), "\n".join(body)))
    return out


def stem(sub):
    """副标题 → 文件名主体：去掉括号注释；`——`→`-`；去空格；保留 `、`。"""
    s = PAREN.sub("", sub)
    s = s.replace("——", "-").replace("：", "-").replace(":", "-")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def fm(title, date, project):
    tags = "\n".join("  - %s" % t for t in TAGS)
    return (
        "---\n"
        'title: "%s"\n'
        "tags:\n%s\n"
        "created: %s\n"
        "updated: %s\n"
        "status: 已完成\n"
        "source_project: %s\n"
        "---\n" % (title, tags, date, date, project)
    )


def nav_bar(items, idx, moc, tail=False):
    parts = []
    if tail:
        parts.append("[[%s|返回目录]]" % moc)
        if idx + 1 < len(items):
            parts.append("[[%s|下一章 ➡]]" % items[idx + 1][0])
        return "> 📖 " + " · ".join(parts)
    parts.append("[[%s|📖 返回目录]]" % moc)
    if idx > 0:
        parts.append("[[%s|⬅ 上一章]]" % items[idx - 1][0])
    if idx + 1 < len(items):
        parts.append("[[%s|下一章 ➡]]" % items[idx + 1][0])
    return "> " + " · ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topic", default="AI 破甲")
    ap.add_argument("--date", default="2026-10-13")
    ap.add_argument("--project", default="ai-jailbreak")
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    if not src.is_file():
        sys.exit("源文件不存在：%s" % src)
    chapters = split_chapters(src.read_text(encoding="utf-8"))
    if not chapters:
        sys.exit("一章都没认出来——检查 H1 写法 `# 第 N 章：…`")

    items = [("%02d-%s" % (n, stem(sub)), n) for n, sub, _ in chapters]
    titles = {n: "第 %d 章 %s" % (n, sub) for n, sub, _ in chapters}
    moc = "%s MOC" % a.topic
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    for i, (n, sub, body) in enumerate(chapters):
        text = (
            fm(titles[n], a.date, a.project)
            + "\n"
            + nav_bar(items, i, moc)
            + "\n\n"
            + body
            + "\n\n---\n\n"
            + nav_bar(items, i, moc, tail=True)
            + "\n"
        )
        (out / (items[i][0] + ".md")).write_text(text, encoding="utf-8")

    rows = "\n".join("| %s | %s |" % (titles[n], ABOUT.get(n, "")) for _, n in items)
    toc = "\n".join("%d. [[%s|%s]]" % (i + 1, items[i][0], titles[items[i][1]])
                    for i in range(len(items)))
    moc_text = (
        fm(moc, a.date, a.project)
        + "\n# %s\n\n" % moc
        + "> [!summary] 一句话看懂\n"
        + "".join("> " + ln + "\n" for ln in [SUMMARY]) + "\n"
        + "## 这本册子讲什么\n\n"
        + "| 章 | 这一章讲什么 |\n| --- | --- |\n" + rows + "\n\n"
        + "## 目录\n\n" + toc + "\n\n"
        + "## 建议阅读顺序\n\n"
        + "- **只想搞懂概念**：第 1 章 → 第 2 章 → 第 5 章速查表。\n"
        + "- **完整走一遍**：第 1 → 2 → 3 → 4 → 5 章（第 3 章只讲机制，不含载荷）。\n"
        + "- **只关心怎么防**：第 2 章 → 第 4 章 → 第 5 章。\n\n"
        + "## 关于本册子\n\n"
        + "- 笔记类型：概念 + 安全视角分析（入门 → 上手，面向零基础）。\n"
        + "- 引文纪律：正文里的英文**成句**引文一律配中译（代码、命令、配置键、路径、文件名、产品名保留原文），"
        + "逐字原文留档在各章末「引文对照（原文 / 中译 / 出处）」表，出处写 `sources/<文件>:<行号>`。\n"
        + "- 安全边界：只写机制 / 分类 / 统计 / 评测 / 防御 / 治理，不产出可执行载荷。\n\n"
        + "## 更新记录\n\n"
        + "- %s 首次创建（由 learning-note-flow 生成，共 %d 章）。\n" % (a.date, len(chapters))
    )
    (out / (moc + ".md")).write_text(moc_text, encoding="utf-8")

    spec = "".join("  %s\n" % items[i][0] for i in range(len(items)))
    (out / "sortspec.md").write_text(
        "---\nsorting-spec: |\n  %s\n%s---\n" % (moc, spec), encoding="utf-8")

    for i in range(len(items)):
        print("写出", out / (items[i][0] + ".md"))
    print("写出", out / (moc + ".md"))
    print("写出", out / "sortspec.md")
    print("章数 %d；文件名：%s" % (len(chapters), [i[0] for i in items]))


if __name__ == "__main__":
    main()
