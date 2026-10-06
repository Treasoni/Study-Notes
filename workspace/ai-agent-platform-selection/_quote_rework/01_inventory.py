"""步骤 1：把 vault 成品笔记里的反引号片段做成清单，供人工判类与翻译。

用真正的反引号 tokenizer（支持 ``X`` 这种 N 反引号定界），不要用
`([^`]+)` 的简单正则——后者在 ``**By default, ...**`` 上会错配、
留下孤立反引号。

输出：
  quotes.tsv        —— 全部唯一片段（cite / code / prose 三分类）
  prose_review.tsv  —— 只含 prose，带所在行上下文，供人工翻译
"""
import re
import pathlib
import collections

ROOT = pathlib.Path(".")
NOTE = ROOT / "AI学习" / "04-项目实践" / "自托管 Agent 选型" / "自托管 Agent 平台选型.md"
OUT = ROOT / "workspace" / "ai-agent-platform-selection" / "_quote_rework"
OUT.mkdir(parents=True, exist_ok=True)

CITE = re.compile(r"^(research|workspace)/|:\d+([-,]\d+)*$")
CODE = re.compile(r"[=(){}\[\];|]|-->|://|_|\$|^[a-z_.]+$|--[a-z]|\.py\b")


def spans(line):
    """→ [(start, end, text, n_backticks)]，正确处理 ``X``。"""
    out, i, n = [], 0, len(line)
    while i < n:
        if line[i] == "`":
            k = 1
            while i + k < n and line[i + k] == "`":
                k += 1
            m = re.search(r"`{%d,}" % k, line[i + k:])
            if not m:
                break
            j = i + k + m.start()
            out.append((i, j + m.end() - m.start(), line[i + k:j], k))
            i = j + m.end() - m.start()
        i += 1
    return out


def kind_of(s):
    s = s.strip("*")
    if CITE.search(s):
        return "cite"
    if CODE.search(s) or len(s) < 12:
        return "code"
    return "prose"


text = NOTE.read_bytes().decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")

chap_of, cur = {}, 0
for i, l in enumerate(lines, 1):
    m = re.match(r"^## 第 (\d) 章", l)
    if m:
        cur = int(m.group(1))
    chap_of[i] = cur


def is_english(s):
    return len(re.findall(r"[A-Za-z]{2,}", s)) >= 4


occ = []
for i, l in enumerate(lines, 1):
    for a, b, s, k in spans(l):
        if is_english(s):
            occ.append({"line": i, "chap": chap_of[i], "text": s, "a": a, "b": b})

uniq = collections.OrderedDict()
for o in occ:
    uniq.setdefault(o["text"], {"kind": kind_of(o["text"]), "n": 0,
                               "line": o["line"], "chap": o["chap"], "text": o["text"]})
    uniq[o["text"]]["n"] += 1

with (OUT / "quotes.tsv").open("w", encoding="utf-8", newline="\n") as f:
    f.write("id\tkind\tchap\tn\tfirst_line\ttext\n")
    for i, d in enumerate(uniq.values(), 1):
        f.write("%03d\t%s\t%d\t%d\t%d\t%s\n" %
                (i, d["kind"], d["chap"], d["n"], d["line"], d["text"].replace("\t", " ")))

# prose 复核件：按章分组，每条带上所在行上下文
prose = [o for o in occ if uniq[o["text"]]["kind"] == "prose"]
byid = {d["text"]: i for i, d in enumerate(uniq.values(), 1)}
with (OUT / "prose_review.tsv").open("w", encoding="utf-8", newline="\n") as f:
    f.write("id\tchap\tline\tquote\tbefore\tafter\n")
    for o in sorted(prose, key=lambda x: (x["chap"], x["line"], x["a"])):
        ln = lines[o["line"] - 1]
        before = ln[max(0, o["a"] - 90):o["a"]]
        after = ln[o["b"]:o["b"] + 90]
        f.write("%03d\t%d\t%d\t%s\t%s\t%s\n" %
                (byid[o["text"]], o["chap"], o["line"],
                 o["text"].replace("\t", " "), before.replace("\t", " "), after.replace("\t", " ")))

kinds = collections.Counter(d["kind"] for d in uniq.values())
print("unique:", len(uniq), dict(kinds))
print("occurrences:", len(occ), "| prose occurrences:", len(prose))
print("prose by chap:", dict(sorted(collections.Counter(o["chap"] for o in prose).items())))
print("prose chars:", sum(len(o["text"]) for o in prose))
print("wrote quotes.tsv / prose_review.tsv")
