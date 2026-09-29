# -*- coding: utf-8 -*-
"""方案 A 的共用内核：正文英译中的替换引擎 + 每章「引文对照」表生成器。

`04_count.py`（预检，只算不写）与 `05_apply.py`（落盘）都调用这里，保证
"量的" 和 "写的" 是同一套逻辑。

不变量（任一不成立就抛错，绝不静默跳过）：

- `TRANS` 的每个键必须在某个文件里至少以**反引号 span** 的形态命中一次；
  命中 0 次说明键写错了或分类判断错了。
- `FIXES` 里期望次数非 0 的条目，必须精确命中该次数。
- `TITLE_FIX` 的旧标题在每个目标文件里必须精确命中给定期望次数。
- 「原文（逐字）」与「中译」两列都不得含 `|`（会撕裂 Markdown 表格）。

行尾：逐文件保留原样（有 CRLF 就写 CRLF，全 LF 就写 LF）。
见 `.learnings/RULES.md`：不做 `read_text`/`write_text` 的隐式归一。
"""
import re
import pathlib
import importlib.util

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
assert (ROOT / "CLAUDE.md").is_file(), "ROOT 解析错了：%s" % ROOT

PROJ = ROOT / "workspace" / "ai-agent-platform-selection"
CH_DIR = PROJ / "chapters"
OUT_DIR = PROJ / "output"
VAULT_NOTE = ROOT / "AI学习" / "04-项目实践" / "自托管 Agent 选型" / "自托管 Agent 平台选型.md"
OUTLINE = PROJ / "03_outline.md"
PRISTINE = HERE / "pristine"

CITE = re.compile(r"^(research|workspace)/|:\d+([-,]\d+)*$")
CH_HEAD = re.compile(r"^(#{1,3}) 第 (\d) 章")

# 目标文件：(路径, 类型, 章标题层级) —— 类型决定附录插到哪
#   chapter   单章文件，附录追加到 EOF
#   merged    拼接本，附录插到本章的 <!-- END: ... --> 之前
#   assembled 组装本，附录插到下一章标题（或 ## 参考文档）之前
TARGETS = [
    (CH_DIR / "01_为什么感觉都一样是范畴错误.md", "chapter"),
    (CH_DIR / "02_多用户一词三义.md", "chapter"),
    (CH_DIR / "03_隔离强度梯度.md", "chapter"),
    (CH_DIR / "04_同层内部怎么分.md", "chapter"),
    (CH_DIR / "05_Octop回答的是不是另一个问题.md", "chapter"),
    (CH_DIR / "06_谁把谁当参照.md", "chapter"),
    (CH_DIR / "07_选型框架与决策树.md", "chapter"),
    (CH_DIR / "_merged.md", "merged"),
    (OUT_DIR / "final_note.md", "assembled"),
    (VAULT_NOTE, "assembled"),
]
# 只改章标题、不做正文替换的文件（提纲与成品保持一致，避免计划里还写着旧标题）
TITLE_ONLY = [OUTLINE]

# 章标题里那句英文，以及它的中文（03_trans.py 的 TITLE_FIX 提供）
TITLE_EXPECT = {
    "01_为什么感觉都一样是范畴错误.md": 0,
    "02_多用户一词三义.md": 0,
    "03_隔离强度梯度.md": 0,
    "04_同层内部怎么分.md": 1,
    "_merged.md": 1,
    "final_note.md": 2,
    "自托管 Agent 平台选型.md": 2,
    "03_outline.md": 1,
}

APPENDIX_TITLE = "引文对照（原文 / 中译）"
APPENDIX_LEAD = "本章正文里出现过的英文引文，逐字原文与中译对照如下。出处与正文同源。"
CALLOUT = [
    "> [!note] 关于引文",
    "> 正文里凡是**成句的英文**都给了中译；**代码、命令、配置键、路径、文件名、产品名与单个技术术语**保留原文。"
    "每处引文的**逐字原文**见该章末尾的「引文对照」表。",
    ">",
]


def load_trans():
    """把 03_trans.py 当数据模块读进来（文件名以数字开头，不能直接 import）。"""
    spec = importlib.util.spec_from_file_location("trans03", HERE / "03_trans.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_trans(trans):
    """→ [(问题, 键)]。空列表才算过。

    译文里出现反引号是最容易犯、后果最隐蔽的一条：原 span 大多只有 1 个
    反引号定界，1 个反引号的 span 内部不能再出现反引号，否则 Markdown 会在
    那里提前闭合，把后半句漏到代码格式外面（还要连带吃掉后面的 cite）。
    """
    bad = []
    for k, v in trans.TRANS.items():
        if "\n" in k:
            bad.append(("键里有换行", k))
        if "`" in v:
            bad.append(("译文里有反引号", k))
        if "|" in v:
            bad.append(("译文里有竖线", k))
        if "\n" in v:
            bad.append(("译文里有换行", k))
        if k != k.strip():
            bad.append(("键首尾有空白", k))
    for k in trans.VERBATIM_FIX:
        if k not in trans.TRANS:
            bad.append(("VERBATIM_FIX 的键不在 TRANS 里", k))
    for old, _new, want in trans.FIXES:
        if "\n" in old:
            bad.append(("FIXES 旧串里有换行", old))
        if want < 0:
            bad.append(("FIXES 期望次数为负", old))
    return bad


def read(path):
    """→ (lines, eol)。行尾按文件现状保留。"""
    raw = path.read_bytes()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n").split("\n"), eol


def write(path, lines, eol):
    # 逐文件回填原行尾：不做全局归一，避免把 LF 文件变成 CRLF（或反之）。
    path.write_bytes(eol.join(lines).encode("utf-8"))


def spans(line):
    """→ [(start, end, text, n_backticks)]，正确处理 ``X``（N 个反引号须由 >= N 个闭合）。"""
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
            end = j + m.end() - m.start()
            out.append((i, end, line[i + k:j], k))
            i = end
        i += 1
    return out


def ticks(text):
    """给 text 套一对比它内部最长反引号串更长的反引号。"""
    longest = 0
    for m in re.finditer(r"`+", text):
        longest = max(longest, len(m.group(0)))
    t = "`" * (longest + 1)
    return t + text + t


CITE_FULL = re.compile(r"^(research|workspace)/\S+\.md(:[\d,\-]+)*$")
CITE_NAME = re.compile(r"^[A-Za-z0-9_\-]+\.md(:[\d,\-]+)*$")
CITE_BARE = re.compile(r"^[^/]{0,10}[:：]\s*[\d][\d,\-、:：]*$")
STRIP_LINENO = re.compile(r":[\d,\-、:：]+$")


def cite_kind(s):
    """→ ("full"|"bare"|None, 文本)。full = 自带文件名，可原样当出处；
    bare = 只有行号（`同文件 :378` 这种），要回填最近一次出现的文件名。"""
    s = s.strip("*").strip()
    if CITE_FULL.match(s) or CITE_NAME.match(s):
        return "full", s
    if CITE_BARE.match(s):
        return "bare", s
    return None, s


def last_path_by_line(lines):
    """→ [path or None]，第 i 项 = 第 0..i 行里最后出现的完整文件名。"""
    out, cur = [], None
    for l in lines:
        for _a, _b, s, _k in spans(l):
            kind, txt = cite_kind(s)
            if kind == "full":
                cur = txt
        out.append(cur)
    return out


def _path_before(sp, pos, prior):
    cur = prior
    for a, b, s, _k in sp:
        if b <= pos:
            kind, txt = cite_kind(s)
            if kind == "full":
                cur = txt
    return cur


def cite_for(line, a, b, prior):
    """给引用 span [a, b) 找出处：先看同一行其后，再看同一行其前，最后放弃。

    `同文件 :N` 用「本行该位置之前最后出现过的文件名」回填；找不到文件名
    就返回 None（宁可空着，也不猜一个错的出处）。
    """
    sp = spans(line)
    for _a2, b2, s2, _k in sp:
        if _a2 < b:
            continue
        kind, txt = cite_kind(s2)
        if kind == "full":
            return txt
        if kind == "bare":
            base = _path_before(sp, _a2, prior)
            if base:
                return STRIP_LINENO.sub("", base) + ":" + txt.split("：")[-1].split(":")[-1]
    for _a2, b2, s2, _k in reversed(sp):
        if b2 > a:
            continue
        kind, txt = cite_kind(s2)
        if kind == "full":
            return txt
        if kind == "bare":
            base = _path_before(sp, _a2, prior)
            if base:
                return STRIP_LINENO.sub("", base) + ":" + txt.split("：")[-1].split(":")[-1]
    return None


def split_sections(lines, kind):
    """→ [(chap, start, stop)]，stop 是该章附录的插入位置（行下标）。"""
    if kind == "chapter":
        m = CH_HEAD.match(lines[0])
        return [(int(m.group(2)) if m else 0, 0, len(lines))]

    heads = [(int(m.group(2)), i) for i, l in enumerate(lines) if (m := CH_HEAD.match(l))]
    out = []
    for n, (chap, start) in enumerate(heads):
        if n + 1 < len(heads):
            stop = heads[n + 1][1]
        elif kind == "merged":
            stop = len(lines)
            for i in range(start, len(lines)):
                if lines[i].startswith("<!-- END:"):
                    stop = i
                    break
        else:  # assembled：最后一章的正文到「参考文档」为止
            stop = len(lines)
            for i in range(start, len(lines)):
                if lines[i].startswith("## 参考文档"):
                    stop = i
                    break
        out.append((chap, start, stop))
    return out


def appendix_rows(lines, start, stop, trans, lp):
    """扫描 [start, stop) 里的 span，收集本章被翻译过的引文。"""
    rows = []
    for i in range(start, stop):
        prior = lp[i - 1] if i else None
        for a, b, s, _k in spans(lines[i]):
            if s not in trans.TRANS:
                continue
            verbatim = trans.VERBATIM_FIX.get(s, s)
            if "|" in verbatim or "|" in trans.TRANS[s]:
                raise AssertionError("引文/译文含 '|'，会撕裂表格：%r" % s)
            rows.append({
                "verbatim": verbatim,
                "zh": trans.TRANS[s],
                "src": cite_for(lines[i], a, b, prior),
            })
    return rows


def render_appendix(rows, level):
    if not rows:
        return []
    out = ["", level + " " + APPENDIX_TITLE, "", APPENDIX_LEAD, "",
           "| # | 原文（逐字） | 中译 | 出处 |", "| --- | --- | --- | --- |"]
    for i, r in enumerate(rows, 1):
        src = ticks(r["src"]) if r["src"] else "—"
        out.append("| %d | %s | %s | %s |" % (i, ticks(r["verbatim"]), r["zh"], src))
    out.append("")
    return out


def transform(text_lines, trans, stats, tag):
    """就地语义：返回新行表。stats 收集命中账。"""
    # 1) 章标题里的英文（纯字面）
    old, new = trans.TITLE_FIX
    hits = sum(l.count(old) for l in text_lines)
    stats["title"][tag] = hits
    if hits:
        text_lines = [l.replace(old, new) for l in text_lines]

    # 2) span 内的成句英文 → 中译（保留反引号定界符）
    for i, line in enumerate(text_lines):
        if "`" not in line:
            continue
        picked = [(a, b, s, k) for a, b, s, k in spans(line) if s in trans.TRANS]
        if not picked:
            continue
        buf, cur = [], 0
        for a, b, s, k in picked:
            t = "`" * k
            buf.append(line[cur:a])
            buf.append(t + trans.TRANS[s] + t)
            cur = b
            stats["span"].setdefault(s, {"n": 0, "tags": []})
            stats["span"][s]["n"] += 1
            if tag not in stats["span"][s]["tags"]:
                stats["span"][s]["tags"].append(tag)
        buf.append(line[cur:])
        text_lines[i] = "".join(buf)

    # 3) 周边字面替换（顺序敏感，自上而下）
    text = "\n".join(text_lines)
    for old, new, want in trans.FIXES:
        got = text.count(old)
        stats["fix"].setdefault(old, {"want": want, "got": 0, "tags": []})
        stats["fix"][old]["got"] += got
        if got and tag not in stats["fix"][old]["tags"]:
            stats["fix"][old]["tags"].append(tag)
        if got:
            text = text.replace(old, new)
    return text.split("\n")


def run(trans, write_files=False):
    """跑全部目标文件。write_files=False 时只算与排版，不落盘。"""
    stats = {"span": {}, "fix": {}, "title": {}, "appendix": {}, "src_missing": 0}
    results = {}
    for path, kind in TARGETS:
        lines, eol = read(path)
        tag = path.name
        # 先把引文账从**改之前**的正文上收下来：替换之后 span 已经变中文，
        # 再按 TRANS 键回查就一条都查不到了。TRANS/FIXES 都不增减行数，
        # 所以这里算出来的章边界在替换之后依然有效。
        sections = split_sections(lines, kind)
        lp = last_path_by_line(lines)
        rows_by_chap = {c: appendix_rows(lines, s, e, trans, lp) for c, s, e in sections}
        lines = transform(lines, trans, stats, tag)
        # 附录：逐章插到该章末尾（自后向前插，避免下标位移）
        for chap, start, stop in reversed(sections):
            rows = rows_by_chap[chap]
            stats["appendix"][tag] = stats["appendix"].get(tag, {})
            stats["appendix"][tag][chap] = len(rows)
            stats["src_missing"] += sum(1 for r in rows if not r["src"])
            level = CH_HEAD.match(lines[start]).group(1) + "#"
            block = render_appendix(rows, level)
            if not block:
                continue
            tail = stop
            while tail > start and lines[tail - 1].strip() == "":
                tail -= 1
            head = lines[:tail] + block
            if kind == "chapter":
                lines = head                      # EOF 追加
            else:
                lines = head + lines[stop:]       # 保持后续内容（含 <!-- END --> / 下一章）
        if kind == "assembled" and not callout_already(lines):
            lines = insert_callout(lines)
        results[str(path)] = (lines, eol)

    if write_files:
        for path, _kind in TARGETS:
            lines, eol = results[str(path)]
            write(path, lines, eol)

    # 只改标题的文件
    for path in TITLE_ONLY:
        lines, eol = read(path)
        lines = transform_title_only(lines, trans, stats, path.name)
        if write_files:
            write(path, lines, eol)
    return stats, results


def transform_title_only(lines, trans, stats, tag):
    old, new = trans.TITLE_FIX
    hits = sum(l.count(old) for l in lines)
    stats["title"][tag] = hits
    return [l.replace(old, new) for l in lines]


def callout_already(lines):
    return any(APPENDIX_TITLE in l or "关于引文" in l for l in lines)


def insert_callout(lines):
    """把「关于引文」callout 插到组装本的目录之后。"""
    for i, l in enumerate(lines):
        if l.startswith("## 参考文档"):
            return lines
    # 目录之后 = 第一个 `## 第 1 章` 之前
    for i, l in enumerate(lines):
        if re.match(r"^## 第 1 章", l):
            return lines[:i] + CALLOUT + lines[i:]
    return lines
