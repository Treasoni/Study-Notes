#!/usr/bin/env python3
"""把 output/final_note.md 切成 Obsidian 分册发布集（章文件 + MOC + sortspec）。

对齐全 vault 既有先例 `AI学习/REA 逆向工程/`：
  01-….md … NN-….md + `<主题> MOC.md` + sortspec.md

变换是**纯包装**：章正文逐字不变，只在每份章文件前后加「frontmatter + 顶部导航栏」，
末尾加「分隔线 + 底部导航尾行」（`> 📖 …`，校验器 `FOOTER` 认得，比对时截断）。
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
TAGS = ["AI学习", "AI安全", "破甲", "越狱", "LLM安全"]


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


def slug(subtitle):
    """副标题 → 文件名片段：去掉空格与标点，保留中文/字母/数字/连字符/点。"""
    s = subtitle.split("——")[0]          # 「主标题——副标题」只取主标题
    s = s.split("：")[0]
    return re.sub(r"[\s，。、；：（）()《》「」【】·/\\|?*\"'<>]+", "", s)


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


def nav(items, idx, moc):
    """顶部 / 底部导航。items: [(文件名, 标题)]。"""
    top = ["[[%s|📖 返回目录]]" % moc]
    if idx > 0:
        top.append("[[%s|⬅ %s]]" % (items[idx - 1][0], items[idx - 1][1]))
    if idx + 1 < len(items):
        top.append("[[%s|%s ➡]]" % (items[idx + 1][0], items[idx + 1][1]))
    return "> " + " · ".join(top)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topic", default="AI 破甲")
    ap.add_argument("--date", default="2026-10-13")
    ap.add_argument("--project", default="ai-jailbreak")
    ap.add_argument("--check-only", action="store_true", help="只打印将要写出的文件，不落盘")
    a = ap.parse_args()

    src = pathlib.Path(a.src)
    if not src.is_file():
        sys.exit("源文件不存在：%s" % src)
    chapters = split_chapters(src.read_text(encoding="utf-8"))
    if not chapters:
        sys.exit("一章都没认出来——检查 H1 写法 `# 第 N 章：…`")

    items = [("%02d-%s" % (n, slug(sub)), "第 %d 章 %s" % (n, sub)) for n, sub, _ in chapters]
    moc = "%s MOC" % a.topic
    out = pathlib.Path(a.out)
    written = []

    for i, (n, sub, body) in enumerate(chapters):
        title = "第 %d 章 %s" % (n, sub)
        text = (
            fm(title, a.date, a.project)
            + "\n"
            + nav(items, i, moc)
            + "\n\n"
            + body
            + "\n\n---\n\n> 📖 [[%s|返回目录]]" % moc
        )
        if i + 1 < len(items):
            text += " · [[%s|%s ➡]]" % (items[i + 1][0], items[i + 1][1])
        text += "\n"
        p = out / (items[i][0] + ".md")
        written.append(p)
        if not a.check_only:
            out.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

    # MOC
    rows = "\n".join("| %s | %s |" % (items[i][1], sub) for i, (_, sub, _) in
                     enumerate([(n, s, b) for n, s, b in chapters]))
    toc = "\n".join("%d. [[%s|%s]]" % (i + 1, items[i][0], items[i][1])
                    for i in range(len(items)))
    moc_text = (
        fm("%s MOC" % a.topic, a.date, a.project)
        + "\n# %s MOC\n\n" % a.topic
        + "> [!summary] 一句话看懂\n"
        + "> **AI 破甲（jailbreak，也译「越狱」）** 就是想办法让一个被训练成「危险内容不开口」的模型，"
        + "把那些它本该拒绝的话**说出来**。本册子从安全视角回答三个问题——它是什么、为什么防不住、"
        + "在机制层是怎么被绕过的；**只讲机制、分类、原理与防御，不含任何可照做的载荷或配方**。\n\n"
        + "## 这本册子讲什么\n\n"
        + "| 章 | 讲什么 |\n| --- | --- |\n" + rows + "\n\n"
        + "## 目录\n\n" + toc + "\n\n"
        + "## 建议阅读顺序\n\n"
        + "- **只想搞懂概念**：第 1 章 → 第 2 章 → 第 5 章速查表。\n"
        + "- **完整走一遍**：第 1 → 2 → 3 → 4 → 5 章（第 3 章只讲机制，不含载荷）。\n"
        + "- **只关心怎么防**：第 2 章 → 第 4 章 → 第 5 章。\n\n"
        + "## 关于本册子\n\n"
        + "- 笔记类型：概念 + 安全视角分析（入门 → 上手）。\n"
        + "- 引文纪律：正文里的英文整句引文一律配中译，逐字原文留档在各章末「引文对照（原文 / 中译 / 出处）」表；"
        + "出处写 `sources/<文件>:<行号>`。\n"
        + "- 安全边界：本册子只写机制 / 分类 / 统计 / 评测 / 防御 / 治理，不产出可执行载荷。\n\n"
        + "## 更新记录\n\n"
        + "- %s 首次创建（由 learning-note-flow 生成，共 %d 章）。\n" % (a.date, len(chapters))
    )
    moc_path = out / (moc + ".md")
    written.append(moc_path)
    if not a.check_only:
        moc_path.write_text(moc_text, encoding="utf-8")

    spec = "\n".join("  " + n for n, _ in items)
    spec_text = "---\nsorting-spec: |\n  %s\n%s\n---\n" % (moc, spec)
    spec_path = out / "sortspec.md"
    written.append(spec_path)
    if not a.check_only:
        spec_path.write_text(spec_text, encoding="utf-8")

    for p in written:
        print("写出" if not a.check_only else "将写出", p)
    print("章数 %d；文件名映射：%s" % (len(chapters), [i[0] for i in items]))


if __name__ == "__main__":
    main()
