"""步骤 2：在动手改文之前，先把「正文里还剩哪些英文」问清楚。

`01_inventory.py` 的两条分类规则已知会有假阳性/假阴性：

- 假阳性（把散文当代码）：含有 `()`、`|`、`$` 的英文句子会被 CODE 规则吃掉，
  例如 `Everything runs in a single Python process ... (Redis, RabbitMQ, Celery), ...`
  和 `Run it on a $5 VPS, ...`。这些其实是要翻译的散文。
- 假阴性（短英文被漏掉）：`is_english` 要求 >= 4 个 ASCII 词，所以
  `Observation interface`、`coding agents`、`verification/governance`
  这类两三个词的英文片段根本没进清单。

本脚本**不修改任何笔记**，只产出一份 `leak_report.md`，供人工决定
「翻 / 不翻」，之后写进 `03_trans.py` 的 TRANS / FORCE / PHRASES。

输出：_quote_rework/leak_report.md
"""
import re
import pathlib
import collections

# 本脚本可能从任意 cwd 调用，所以锚在自身位置而不是 cwd：
#   <vault>/workspace/ai-agent-platform-selection/_quote_rework/02_plan.py
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NOTE = ROOT / "AI学习" / "04-项目实践" / "自托管 Agent 选型" / "自托管 Agent 平台选型.md"
OUT = HERE
assert (ROOT / "CLAUDE.md").is_file(), "ROOT 解析错了：%s" % ROOT

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


def words(s):
    return re.findall(r"[A-Za-z][A-Za-z'’.-]*", s)


text = NOTE.read_bytes().decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")

chap_of, cur = {}, 0
for i, l in enumerate(lines, 1):
    m = re.match(r"^## 第 (\d) 章", l)
    if m:
        cur = int(m.group(1))
    chap_of[i] = cur

uniq = collections.OrderedDict()
for i, l in enumerate(lines, 1):
    for a, b, s, k in spans(l):
        d = uniq.setdefault(s, {"n": 0, "line": i, "chap": chap_of[i], "k": max(k, 0)})
        d["n"] += 1
        d["k"] = max(d["k"], k)

# A. cite 型（原样保留）——只报数量
cites = [s for s, d in uniq.items() if CITE.search(s.strip("*"))]

# B. code 型里「长得像散文」的：>= 6 个 ASCII 词
bigcode = [(i, s, d) for i, (s, d) in enumerate(uniq.items(), 1)
           if not CITE.search(s.strip("*"))
           and (CODE.search(s.strip("*")) or len(s.strip("*")) < 12)
           and len(words(s)) >= 6]

# C. 反引号之外的英文串（>= 2 个 ASCII 词）
RUN = re.compile(r"[A-Za-z][A-Za-z0-9'’./+-]*(?:[ \t]+[A-Za-z][A-Za-z0-9'’./+-]*)+")
outside = collections.OrderedDict()
for i, l in enumerate(lines, 1):
    stripped = l
    for a, b, s, k in reversed(spans(l)):
        stripped = stripped[:a] + " " + stripped[b:]
    for m in RUN.finditer(stripped):
        s = m.group(0)
        d = outside.setdefault(s, {"n": 0, "line": i, "chap": chap_of[i]})
        d["n"] += 1

# D. 标题行里的英文
heads = [(i, l) for i, l in enumerate(lines, 1)
         if l.startswith("#") and re.search(r"[A-Za-z]{3,}", l)]

rep = []
rep.append("# 英文残留勘查报告（只读，不改笔记）\n")
rep.append("源文件：`%s`（%d 行）\n" % (NOTE.as_posix().replace("../", ""), len(lines)))
rep.append("唯一反引号片段：%d（cite %d / 疑似代码散文 %d / 其余 %d）\n"
           % (len(uniq), len(cites), len(bigcode),
              len(uniq) - len(cites) - len(bigcode)))

rep.append("\n## A. 反引号内「疑似散文但被判为代码」——需人工确认是否翻译\n")
rep.append("\n| # | 首次行 | 章 | 次数 | 词数 | 片段 |\n| --- | --- | --- | --- | --- | --- |\n")
for i, s, d in sorted(bigcode, key=lambda x: (x[2]["chap"], x[2]["line"])):
    rep.append("| %d | %d | %d | %d | %d | `%s` |\n"
               % (i, d["line"], d["chap"], d["n"], len(words(s)), s.replace("|", "\\|")))

rep.append("\n## B. 反引号之外的英文串（>= 2 词）——全部\n")
rep.append("\n| # | 串 | 次数 | 首次行 | 章 |\n| --- | --- | --- | --- | --- |\n")
for j, (s, d) in enumerate(sorted(outside.items(), key=lambda x: (-x[1]["n"], x[1]["line"])), 1):
    rep.append("| %d | %s | %d | %d | %d |\n"
               % (j, s.replace("|", "\\|"), d["n"], d["line"], d["chap"]))

rep.append("\n## C. 含英文的标题行\n")
rep.append("\n| 行 | 章 | 标题 |\n| --- | --- | --- |\n")
for i, l in heads:
    rep.append("| %d | %d | %s |\n" % (i, chap_of[i], l.replace("|", "\\|")))

(OUT / "leak_report.md").write_bytes("".join(rep).encode("utf-8"))
print("wrote leak_report.md: uniq=%d cites=%d bigcode=%d outside=%d heads=%d"
      % (len(uniq), len(cites), len(bigcode), len(outside), len(heads)))
