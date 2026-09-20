#!/usr/bin/env python3
"""确定性地把 chapters/ 拼成 output/final_note.md。

规则（来自 note-assembler 的交接报告，见同目录 .assembly_handoff.md）：
  1) 头部块 + 目录（取自 .assembly_handoff.md 的 ```markdown 代码块）
  2) 各章正文：标题整体降一级（无 #### 以上），删除 <!-- SOURCE/END --> 分隔注释
  3) 结语
全程 LF；代码围栏内的 # 行不参与降级。
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CH = ROOT / "chapters"
OUT = ROOT / "output" / "final_note.md"

# ---------- 1. 从交接报告里取出头部块 / 目录 / 结语 ----------
handoff = (ROOT / ".assembly_handoff.md").read_text(encoding="utf-8", newline="")
blocks = []
cur, in_fence = None, False
for line in handoff.split("\n"):
    if line.startswith("```"):
        if not in_fence:
            in_fence, cur = True, []
        else:
            in_fence = False
            blocks.append("\n".join(cur))
        continue
    if in_fence:
        cur.append(line)

def pick(pred, label):
    hit = [b for b in blocks if pred(b)]
    assert len(hit) == 1, f"{label}: 期望 1 块，实得 {len(hit)}"
    return hit[0].rstrip("\n")

header = pick(lambda b: b.startswith("# Jev 决策模型"), "头部块")
toc    = pick(lambda b: b.startswith("## 目录"), "目录")
tail   = pick(lambda b: b.startswith("## 结语"), "结语")
assert "口径纪律声明" in header and "3. **官方博客" in header, "头部块内容不符"

# 锚点归一：标题去掉标点后会留下连续空白，Obsidian 与 GFM 都把连续连字符折叠为一个。
# 组装器原稿在 3 条含 `≠` / `/` 的标题（4.2、4.5、6.4）上留下了 `--`，这里统一折叠。
toc, n_anchor_fix = re.subn(r"\]\(#([^)]*)\)", lambda m: "](#" + re.sub("-{2,}", "-", m.group(1)) + ")", toc)
leftover = [a for a in re.findall(r"\]\(#([^)]*)\)", toc) if "--" in a]
assert not leftover, f"目录仍有未折叠的连续连字符: {leftover}"
print(f"锚点归一：处理 {n_anchor_fix} 条目录链接")

# ---------- 2. 逐章降级 + 去注释 ----------
chapters = sorted(p for p in CH.glob("*.md") if p.name != "_merged.md")
assert len(chapters) == 7, f"章节数应为 7，实得 {len(chapters)}"

levels_before, dropped, bodies, in_fence = {}, 0, [], False
for p in chapters:
    out = []
    for line in p.read_text(encoding="utf-8", newline="").split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if not in_fence:
            if line.startswith("<!--") and ("SOURCE:" in line or "END:" in line):
                dropped += 1; continue
            n = len(line) - len(line.lstrip("#"))
            if n and line[n:n+1] == " ":
                levels_before[n] = levels_before.get(n, 0) + 1
                assert n <= 3, f"{p.name}: 出现 {n} 级标题，降级规则未覆盖 -> {line[:60]}"
                line = "#" + line
        out.append(line)
    body = "\n".join(out).rstrip("\n")
    assert body.strip(), f"{p.name} 正文为空"
    bodies.append(body)
assert not in_fence, "存在未闭合代码围栏"
# 那 14 行 <!-- SOURCE/END --> 只存在于 merge_files.py 产出的 _merged.md，原章文件里没有；
# 本脚本直接以原章文件为输入，故期望为 0（保留剥离逻辑以防后续改用 _merged.md）。
assert dropped == 0, f"原章文件不应含分隔注释，实删 {dropped}"
print("删除分隔注释:", dropped, "| 原标题级别分布:", dict(sorted(levels_before.items())))

# ---------- 3. 拼装 ----------
doc = "\n\n".join([header, toc] + bodies + [tail]) + "\n"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(doc, encoding="utf-8", newline="")

# ---------- 4. 校验 ----------
t = OUT.read_text(encoding="utf-8")
lines = t.split("\n")
assert t.count("```") % 2 == 0, "代码围栏不配对"

# 围栏感知扫描：代码块内的 # 行（python 注释）不是标题
prose, fence_langs, fenced = [], [], False
for l in lines:
    if l.startswith("```"):
        if not fenced:
            fence_langs.append(l[3:].strip())
        fenced = not fenced
        continue
    if not fenced:
        prose.append(l)
h1 = [l for l in prose if l.startswith("# ")]
h2 = [l for l in prose if l.startswith("## ")]
assert len(h1) == 1 and h1[0].startswith("# Jev 决策模型"), f"H1 应唯一，实得 {h1}"
assert not [l for l in prose if l.startswith("#####")], "出现 5 级以上标题"
assert all(fence_langs), f"存在无语言标识的代码块: {fence_langs}"

# 目录契约：收录「章」(H2) 与「编号小节」(H3)；不收录 N.M.K 子节(H4)与章末小结/预告
toc_texts = re.findall(r"^\s*(?:[-*]\s+)?\d*\.?\s*\[([^\]]+)\]\(#", toc, re.M)
heads = set(l.lstrip("#").strip() for l in prose if re.match(r"^#{2,4} ", l))
missing = [x for x in toc_texts if x not in heads]
assert not missing, f"目录条目不存在的标题: {missing}"

toc_set = set(toc_texts)
opt_out = {"本章小结", "下一章预告"}
h3 = [l[4:].strip() for l in prose if l.startswith("### ")]
untoc = [h for h in h3 if h not in toc_set and h not in opt_out]
assert not untoc, f"H3 小节未进目录: {untoc}"
h4 = [l for l in prose if l.startswith("#### ")]
print(f"目录收录 {len(toc_texts)} 条 | 未收录：H4 子节 {len(h4)} 个、章末小结/预告 {len(h3)-len([h for h in h3 if h in toc_set])} 个（目录策略如此）")

# 脚注配对
refs = re.findall(r"\[\^(c\d+-\d+)\](?!:)", t)
defs = re.findall(r"^\[\^(c\d+-\d+)\]:", t, re.M)
assert set(refs) == set(defs), f"孤立引用={sorted(set(refs)-set(defs))} 孤立定义={sorted(set(defs)-set(refs))}"

items = re.findall(r"^\[(\^c\d+-\d+)\]:", t, re.M)
seen = {}
for i in items:
    assert i not in seen, f"重复脚注定义: {i}"
    seen[i] = 1
assert t.count("[^c1-1]") >= 10, "第一章脚注引用数异常"
assert all(x in t for x in ["## 结语", "## 目录", "口径纪律声明"]), "首尾块缺失"
# 代码块首行的「非官方原文」提示：ch3 四处（结构示意）+ ch5 两处（形状示意）
n_notice = t.count("非官方原文，需回官网核对")
assert n_notice == 6, f"代码块「非官方原文」提示应为 6 处，实得 {n_notice}"
assert "结构示意" in t and "形状示意" in t
assert t.count("\r") == 0, "成品含 CRLF"
# 「确定性」只允许以否定形式出现（写作禁令 ④：绝不写「输出是确定性的」）
for m in re.finditer("确定性", t):
    assert re.search(r"(没有|无)任何「?$", t[max(0, m.start()-12):m.start()]), \
        f"出现未加否定的「确定性」: ...{t[max(0,m.start()-40):m.end()+20]}..."

print(f"OK -> {OUT}")
print(f"  字节 {len(t.encode('utf-8'))} | 行 {len(lines)} | H1 {len(h1)} | H2 {len(h2)}")
print(f"  中文字数 {len(re.findall(r'[一-鿿]', t))}")
print(f"  脚注 定义 {len(items)} 条 / 引用 {len(refs)} 处 | 目录条目 {len(toc_texts)} 条")
print(f"  代码块 {len(fence_langs)} 个 | 语言 {sorted(set(fence_langs))}")
