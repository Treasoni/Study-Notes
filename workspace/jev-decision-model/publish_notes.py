#!/usr/bin/env python3
"""P6 分册发布：按 vault 惯例发布为「主题目录 + 主题 MOC + 7 篇分册」。

发布契约（来自 note-beautifier SKILL.md Step 4）：
  - 每篇分册的正文与源章文件**逐字一致**（断言；全部校验通过前不写任何文件）
  - 结构小标题（分册导航 callout）出现次数 == 期望值 2（顶部 + 尾部）
  - 生成侧与校验侧共用同一个命名函数 note_stem()，禁止一处带 .md、一处不带
  - 分册导航与双链的目标文件逐条断言真实存在（vault 全库解析）
  - 重发时用「前缀白名单删除」，目录里出现非本次产物即失败退出，不用 rm -rf
排版遵循 vault 惯例：frontmatter → H1 → `> [!info]` 导航 callout → 正文。
全程 LF。头部块 / 结语取自 output/final_note.md（P5 成品），正文取自 chapters/。
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent            # workspace/jev-decision-model
VAULT = ROOT.parents[1]                           # vault 根，从脚本位置推导，不写死
DEST = VAULT / "AI学习" / "03-技术专题" / "Jev 决策模型"
PROJECT_SLUG = "jev-decision-model"
DATE = "2026-09-20"
TAGS_CH = "[ai, jev, 决策模型, typesafe-ai]"
TAGS_MOC = "[ai, jev, 决策模型, typesafe-ai, moc, 索引]"

# (章号, 文件名短名, 完整章标题, 一句话说明) —— 短名同时供文件名与双链使用
CH = [
    (1, "决策模型的位置", "第一章：决策模型的位置——Jev 与 LLM 的分工",
     "Jev 被厂商定义成什么、它和文本模型差在哪、该放在你系统的哪一层"),
    (2, "性能与定价", "第二章：厂商自报的性能与定价（速查表）",
     "端到端延迟、相对速度、token 价格三条厂商自报数字，以及各自的限定条件"),
    (3, "三原语与最小调用", "第三章：三原语与一次最小调用",
     "Noul / Choice / Score 的语义与一次调用的形状（代码全部标注为结构示意）"),
    (4, "读结果与阈值设计", "第四章：读结果——probability、confidence 与阈值设计",
     "一个答案里三种「看起来都像置信度」的数字怎么分工，阈值从哪起步"),
    (5, "接入与设计模式", "第五章：接入与设计模式——成本、SDK、三种官方模式",
     "输入 token 是唯一付费项、三个官方模式、生态接入点各包了什么"),
    (6, "独立实测", "第六章：独立实测——三方数据与它们各自的口径",
     "品玩 / Wunderlandmedia / jev-decision-bench 三份数据各自能说明什么"),
    (7, "适用边界与已知弱项", "第七章：适用边界与已知弱项",
     "不要在 Jev 里做什么、漂移怎么处理、未解与待补清单"),
]
N_CH = len(CH)

def note_stem(i: int) -> str:
    """唯一命名函数：文件名与双链目标都由它产出。"""
    assert 1 <= i <= N_CH, i
    return f"Jev {i:02d} {CH[i - 1][1]}"

def moc_stem() -> str:
    return "Jev 决策模型 MOC"

def prose(doc: str) -> list:
    """围栏感知：代码块里的 `#` 行（python 注释）不是标题。"""
    out, fenced = [], False
    for l in doc.split("\n"):
        if l.startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(l)
    return out

# ---------- 1. 头部块 / 结语：与单文件版同源（取自 P5 成品） ----------
final_lines = (ROOT / "output" / "final_note.md").read_text(encoding="utf-8").split("\n")
assert final_lines[0].startswith("# Jev 决策模型"), "final_note.md 首行不是笔记标题"
head_block = "\n".join(final_lines[1:final_lines.index("## 目录")]).strip()
tail_block = "\n".join(final_lines[final_lines.index("## 结语"):]).strip()
assert "口径纪律声明" in head_block and tail_block.startswith("## 结语")

# ---------- 2. 内存中构建全部 8 个成品 ----------
def nav_callout(i: int) -> str:
    parts = []
    if i > 1:
        parts.append(f"← [[{note_stem(i-1)}|第 {i-1} 章 · {CH[i-2][1]}]]")
    parts.append(f"🗂 [[{moc_stem()}|目录]]")
    if i < N_CH:
        parts.append(f"[[{note_stem(i+1)}|第 {i+1} 章 · {CH[i][1]}]] →")
    return "> [!info] 分册导航\n> " + " · ".join(parts)

srcs = sorted(p for p in (ROOT / "chapters").glob("*.md") if p.name != "_merged.md")
assert len(srcs) == N_CH, len(srcs)

docs = {}          # 文件名 -> {doc, body, head, rest, h1, foot}
for i, src in enumerate(srcs, 1):
    body = src.read_text(encoding="utf-8", newline="").rstrip("\n")
    h1, rest = body.split("\n", 1)                       # h1 + "\n" + rest == body
    fm = ("---\n"
          f'title: "{CH[i-1][2]}"\n'
          f"tags: {TAGS_CH}\n"
          f"created: {DATE}\nupdated: {DATE}\nstatus: new\nsource_project: {PROJECT_SLUG}\n"
          "---\n")
    nav = nav_callout(i)
    head, foot = f"{fm}\n{h1}\n\n{nav}\n", f"\n\n---\n\n{nav}\n"
    docs[f"{note_stem(i)}.md"] = {
        "doc": head + rest + foot, "body": body, "head": head, "rest": rest, "h1": h1, "foot": foot}

related = [
    ("Agent智能体", "Jev 在 agent 分层架构里的位置（第一章 1.8）"),
    ("AI工程范式演进-Prompt到Harness", "「慢思考模型 + 快判断层 + 普通代码 + Harness 调度」这套分工的来路（第一章 1.8）"),
    ("AI上下文工程", "第五章的上下文压缩实例，正是把每个 tool call 交给 Jev 判断保留 / 截断"),
]
moc_nav = "> [!info] 目录导航\n> 共 7 篇，建议按顺序读；每篇顶部与末尾都有上一章 / 下一章导航。"
moc = (
    "---\n"
    f'title: "{moc_stem()}"\n'
    f"tags: {TAGS_MOC}\n"
    f"created: {DATE}\nupdated: {DATE}\nstatus: new\nsource_project: {PROJECT_SLUG}\n"
    "---\n\n"
    f"# {moc_stem()}\n\n"
    f"{moc_nav}\n\n"
    f"{head_block}\n\n"
    "---\n\n## 📖 学习路径\n\n"
    + "\n".join(f"{i}. [[{note_stem(i)}]] - {CH[i-1][3]}" for i in range(1, N_CH + 1))
    + "\n\n## 🔗 相关笔记\n\n"
    + "\n".join(f"- [[{t}]] - {why}" for t, why in related)
    + "\n\n---\n\n"
    f"{tail_block}\n"
).replace("\r", "")
docs[f"{moc_stem()}.md"] = {"doc": moc, "body": None, "head": None, "rest": None, "h1": None, "foot": None}

# ---------- 3. 落盘前全量校验（任一失败则不写任何文件） ----------
new_stems = {note_stem(i) for i in range(1, N_CH + 1)} | {moc_stem()}
for name, d in docs.items():
    doc = d["doc"]
    assert "\r" not in doc, f"{name}: 含 CRLF"
    assert sum(1 for l in prose(doc) if l.startswith("# ")) == 1, f"{name}: H1 不唯一"
    assert sum(1 for l in prose(doc) if l.startswith("#####")) == 0, f"{name}: 出现 5 级以上标题"
    if d["body"] is not None:                               # 分册
        assert doc[len(d["head"]):-len(d["foot"])] == d["rest"], f"{name}: 正文中段与源章不一致"
        assert d["h1"] + "\n" + d["rest"] == d["body"], f"{name}: 切分未还原源正文"
        assert doc.count("[!info] 分册导航") == 2, f"{name}: 导航 callout 应出现在顶尾两处"
        assert doc.count("[!info] 目录导航") == 0, f"{name}: 分册不应含目录导航 callout"
        assert len(re.findall(r"^\[\^[\w-]+\]:", doc, re.M)) == \
               len(re.findall(r"^\[\^[\w-]+\]:", d["body"], re.M)), f"{name}: 脚注定义数变化"
        assert doc.index("[!info] 分册导航") > doc.index("\n# "), f"{name}: 导航 callout 应在 H1 之后"
    else:                                                   # 主题 MOC
        assert doc.count("[!info] 目录导航") == 1, f"{name}: 目录导航 callout 应恰好 1 处"
        assert doc.count("[!info] 分册导航") == 0, f"{name}: MOC 不应含分册导航 callout"

vault_stems = {p.stem for p in VAULT.rglob("*.md")
               if ".git" not in p.parts and "node_modules" not in p.parts}
dead = []
for name, d in docs.items():
    for m in re.finditer(r"\[\[([^\]]+)\]\]", d["doc"]):
        tgt = m.group(1).split("|")[0].split("#")[0].strip()
        if tgt in new_stems:
            continue
        if tgt.endswith(".md") or "/" in tgt:
            if not (VAULT / (tgt if tgt.endswith(".md") else tgt + ".md")).exists():
                dead.append((name, tgt, "路径不存在"))
        elif tgt not in vault_stems:
            dead.append((name, tgt, "vault 内无此笔记"))
assert not dead, f"死链：{dead}"
print(f"落盘前校验通过：{len(docs)} 个文件 / 正文逐字一致 / 无死链")

# ---------- 4. 清理上一版（前缀白名单） + 落盘 + 回读复验 ----------
if DEST.exists():
    foreign = sorted(p.name for p in DEST.iterdir() if p.is_dir() or p.name not in docs)
    assert not foreign, f"目标目录含非本次产物，拒绝清理：{foreign}"
    for p in DEST.iterdir():
        p.unlink()
    DEST.rmdir()
    print(f"已清理上一版 {len(docs)} 个本次产物（白名单内，无外来文件）")

DEST.mkdir(parents=True, exist_ok=False)
pre = {DEST / n: d["doc"] for n, d in docs.items()}
for p, content in pre.items():
    p.write_text(content, encoding="utf-8", newline="")
for p, content in pre.items():
    back = p.read_text(encoding="utf-8", newline="")
    assert back == content, f"{p.name}: 回读不一致"
    assert "\r" not in back, f"{p.name}: 含 CRLF"

n_links = sum(len(re.findall(r"\[\[", c)) for c in pre.values())
print(f"OK 发布 {len(pre)} 个文件 / 双链 {n_links} 条全部有效 / 合计 "
      f"{sum(len(c.encode()) for c in pre.values())} 字节")
print(f"   目录：{DEST.relative_to(VAULT)}")
for p in sorted(pre):
    print(f"   {p.name}  ({len(pre[p].encode())} B)")
