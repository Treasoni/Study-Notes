#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""引文纪律的统一校验器：逐字回源 / 引文体例 / 多副本一致。

## 为什么要有这个脚本

引文类缺陷在本项目已经跨 3 个项目复发，每一轮都**现写一个校验器放在项目工作区里**
（`music-tag-web/_verify/sweep_quotes.py`、`ai-agent-platform-selection/_quote_rework/05_apply.py`），
随项目一起废弃；下一轮没有工具可用，只能靠人读，于是同类缺陷再犯。
机制落在「文字要求」上、没落在「可复用的可执行校验器」上——这就是本脚本存在的理由。

用法（在项目根目录运行）：

    # 组装前：单章的文本级检查（V + S，不含跨副本——此时一章只有一份副本）
    python .codex/scripts/note-citation-check.py workspace/<project-slug> --mode text

    # 收集阶段：核对自己的中间产物有没有把来源引错（ERR-20260929-013 的源头）
    python .codex/scripts/note-citation-check.py workspace/<project-slug> \
        --mode verbatim --file 02_deep_research.md

    # 组装 / 发布后：三族全跑
    python .codex/scripts/note-citation-check.py workspace/<project-slug> \
        [--vault-note "AI学习/.../某篇.md"]

## 三类检查

- **V 逐字回源**：正文引用过的英文整句，必须在语料里**逐字**出现（归一化后比较）。
  捕获「引文带来源 ID、句子也在，但一个代词被换掉」这类骗过所有「有没有挂来源」检查的缺陷。
  三态：原始来源命中（通过）/ 只在自己的中间产物里命中（默认**失败**，中间件自己
  可能已经错了一手）/ 未命中（**失败**）。引文省略处按省略号切段，逐段回源。
- **S 引文体例**（引文类缺陷的第二族，原文是英文时都看不出来）：
  - `S1 边界叠字`：中译引文的首字 == 紧邻其前的末字（`合计约 `约 1,300 token``）
  - `S2 LCS 撞车`：引导语尾部与中译的**最长公共汉字子串 >= 5**（引导语把引文又说了一遍）
  - `S3 ASCII 残留`：正文里仍有的「>= 2 个 ASCII 词」串，逐个确认属于保留类
  - `S4 对照表结构`：每章「引文对照」表的行数与管道数、出处列取值域是否合法
- **C 多副本一致**：章文件 → `chapters/_merged.md` → `output/final_note.md` → vault 成品，
  逐章逐字比对（改一份就发布，副本必然漂移）。

S1/S2/S3 是**候选清单**（要人工判，不自动判罪）；V 的未命中与本中间产物命中、S4、C
是**硬失败**。退出码：0 = 无硬失败；1 = 有硬失败；2 = 用法或路径错误。

**`--mode text`** = V + S，不含跨副本比对：一章刚写完时只有一份章文件，跑 C 会
「一组都没比」（反静默通过会判失败），所以交章时用 `text`，组装 / 发布后再跑 `all`。

**`--file`** = 额外要逐字回源的文件（相对项目目录解析），只喂给 V。用途：核对
**自己的中间产物**（`02_deep_research.md`）有没有把来源引错。ERR-20260929-013 的源头
就是它——中间件把来源的 `and argue that` 写成 `we argue that`，下游照抄，而下游
「挂着来源 ID、句子也在」，所有形式检查都过得去。不查 `--file`，这个错误要等
user 读出来的那一刻才被发现。
"""
import argparse
import html as htmllib
import pathlib
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 章标题的两种写法都要认：`第 1 章` / `第一章`（有无空格、阿拉伯或汉字数字），
# 外加 `附录 A` / `Appendix A`。基准是 `第 N 章`，换成别的写法就比不到任何一章，
# 副本比对会「一章都没比就报通过」（第二项目实测：8 个章文件全没匹配上）。
CH_HEAD = re.compile(
    r"^(#{1,4})\s*(?:第\s*([0-9一二三四五六七八九十百]+)\s*章|(?:附录|Appendix)\s*([A-Za-z0-9]+))")
FOOTER = re.compile(r"^## (参考文档|相关文档|参考资料)")
END_MARK = re.compile(r"^<!--\s*(END|SOURCE):")
CJK = re.compile(r"[一-鿿]")
ASCII_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'’\-]*")
# 相邻的 ASCII 词串（>= 2 个词，只隔空格）——「该译没译」的可疑形态。
ASCII_PHRASE = re.compile(r"[A-Za-z][A-Za-z0-9'’\-]*(?:\s+[A-Za-z][A-Za-z0-9'’\-]*)+")
CITE_FULL = re.compile(r"^(research|workspace|sources|docs)/\S+\.md(:[\d,\-]+)*$")
CITE_NUM_ARTIFACT = re.compile(r"^\d\d_[A-Za-z0-9_\-]+\.md(:[\d,\-]+)*$")
# 指针形态：`research/octop/src/octop/api/deps.py:65-89`、`02_deep_research.md:313`。
# 反引号里的**路径 + 行号**是出处指针，不是引文——它本来就不该在语料里出现。
# 不含 CJK、不含空格，所以不会误吞真正的句子。
CITE_PATH = re.compile(r"^[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+(?::[\d,\-]+)*$")
# 英文散文的虚词标记——用来把命令片段 / 路径 / URL 从「英文整句」里筛出去。
PROSE_MARK = re.compile(
    r"\b(?:the|and|is|are|was|were|be|been|of|to|not|no|with|without|from|for|"
    r"in|on|into|that|this|these|those|or|as|it|its|by|at|has|have|had|can|"
    r"could|will|would|should|must|may|might|only|never|always|every|all|any|"
    r"one|two|each|other|than|then|when|while|if|but|so|there|their|your)\b",
    re.I)
ELISION = re.compile(r"(?:\.{2,}|。{2,}|…+)")
# 引号成对（中文引号 + ASCII 直引号）
QUOTE_PAIRS = [("「", "」"), ("“", "”")]


# --------------------------------------------------------------------------- 工具

def read_text(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def denoise(t):
    """去掉 Markdown 装饰与 HTML 实体，**保留空白与省略号**。

    必须先做这一步再按省略号切段：`[comparison table](...)` 里的 `...` 是链接的
    省略写法，不是引文自己的省略；先切段就会把 `(` 和 `)` 切成两段，第二段
    `) condenses the source-verified contrast with Hermes.` 永远查不到。
    """
    t = htmllib.unescape(t)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)      # 链接 / 图片
    t = re.sub(r"</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^>]*)?/?>", "", t)
    t = re.sub(r"<https?://[^>]*>", "", t)
    # 抓回来的原料常是 PDF / arxiv 提取件，**LaTeX 会漏进正文**：语料里写的是
    # `ℒ\mathcal{L}`，笔记侧写的是干净的 `ℒ`——一个字都对不上，真引文被判 weak
    # （实测 `13_arxiv_2606.20683v1_fulltext.md:98`，覆盖率 0.77）。
    # 必须先剥 LaTeX 命令、再做 markdown 反斜杠转义：顺序反了，`\mathcal{L}` 里的
    # 反斜杠会被当转义吃掉，变成 `mathcal{L}`，永远对不上。
    t = re.sub(r"\\[a-zA-Z]+\s*\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)
    t = re.sub(r"\\(.)", r"\1", t)
    t = t.replace("&#x20;", " ").replace("&nbsp;", " ")
    for m in ("**", "__", "*", "`", "[", "]"):
        t = t.replace(m, "")
    return t


def norm(t):
    """比对用归一化：去装饰 + 去空白 + 去省略号，只留实义字符。

    与 `music-tag-web/_verify/sweep_quotes.py` 的 normalize 保持一致——那个脚本
    是这套判据的源头，别在两边分别演化。

    额外做一次 **NFKC**：PDF / arxiv 提取件里的兼容字符与笔记侧的正常字符编码不同，
    同一句话会变成两串（`ℒ` U+2112 vs `L`、`ﬁ` vs `fi`、全角括号 vs 半角）。
    NFKC 只影响 V 的比对（S1/S2 走原始文本的 `cjk_only`），不会掩盖改字：
    `and argue that` 与 `we argue that` 这类字母差异 NFKC 一概不动。
    """
    return ELISION.sub("", re.sub(r"[\s　]+", "", unicodedata.normalize("NFKC", denoise(t))))


def spans(line):
    """→ [(start, end, text)]，N 个反引号须由 >= N 个闭合。"""
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
            out.append((i, end, line[i + k:j]))
            i = end
        i += 1
    return out


def quotes_in_line(line):
    """→ [(quote_text, kind)]，正文里的引文：中文引号对 + 含 ASCII 词的反引号 span。"""
    out = []
    for op, cl in QUOTE_PAIRS:
        for m in re.finditer(re.escape(op) + r"([^" + re.escape(op + cl) + r"]{4,})" + re.escape(cl), line):
            out.append((m.group(1), "bracket"))
    for _a, _b, s in spans(line):
        if ASCII_WORD.search(s):
            out.append((s, "span"))
    return out


def cjk_only(s):
    return "".join(CJK.findall(s))


def lcs(a, b):
    """→ (长度, 子串)。最长公共**连续**子串。"""
    if not a or not b:
        return 0, ""
    prev = [0] * (len(b) + 1)
    best, bend = 0, 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, bend = cur[j], j
        prev = cur
    return best, b[bend - best:bend]


def chap_key(m):
    """→ 跨副本统一的章标识：`第1章` / `附录A`。"""
    return ("第%s章" % m.group(2)) if m.group(2) else ("附录" + m.group(3).upper())


def split_chapters(lines, kind):
    """→ [(章标识, start, stop)]。stop 取「下一章标题」与「本章 END 标记」中靠前者。"""
    heads = []
    for i, l in enumerate(lines):
        m = CH_HEAD.match(l)
        if m:
            heads.append((chap_key(m), i))
    if kind == "chapter" and not heads:
        return []
    out = []
    for n, (chap, start) in enumerate(heads):
        stop = heads[n + 1][1] if n + 1 < len(heads) else len(lines)
        for i in range(start, stop):
            if END_MARK.match(lines[i]):
                stop = i
                break
        out.append((chap, start, stop))
    return out


def chapter_block(lines, start, stop):
    """取一章的正文（去首尾空行、去章标题层级的 #、去 END/SOURCE 标记）。"""
    body = [l for l in lines[start:stop] if not END_MARK.match(l)]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    m0 = CH_HEAD.match(body[0]) if body else None
    if m0:
        body[0] = chap_key(m0) + body[0][m0.end():]
    out = []
    for l in body:
        l = l.rstrip()
        # 组装件 / 已发布件相对章文件多出来的合法装饰，比对时抹掉，否则每一份都比
        # 不同：① 章末追加的 `## 相关文档`（组装阶段才加）；② 分章之间的 `---`；
        # ③ 表格对齐填充（Obsidian 编辑表格时会把单元格补空格、把分隔行的短横线
        # 拉长）；④ 标题层级下沉。
        if FOOTER.match(l):
            break
        if len(l) >= 3 and set(l) == {"-"}:
            continue
        if l.startswith("#"):
            l = "§ " + l.lstrip("#").strip()
        elif l.startswith("|"):
            if re.fullmatch(r"\|[\s:\-|]+\|", l):
                l = "|-|-|"                   # 分隔行短横线长度无语义
            else:
                l = re.sub(r"[ \t]+", "", l)
        out.append(l)
    # 空行数量无语义（组装与编辑器都会增删），压成「有 / 无段落分隔」
    res, prev_blank = [], False
    for l in out:
        blank = not l.strip()
        if blank and prev_blank:
            continue
        prev_blank = blank
        res.append(l)
    while res and not res[-1].strip():
        res.pop()
    while res and not res[0].strip():
        res.pop(0)
    return res


def collect_corpus(project, extra):
    """→ (primary, derived) 两组 [(名字, 文本)]。

    **primary** = 抓回来的原始来源（`research/`、`sources/`、`--corpus` 指定的东西）。
    **derived** = 本项目自己的中间产物（`0N_intent|explore|research|outline.md`）——
    引文只在 derived 里命中，说明它是**从自己的中间件抄来的**，而中间件本身可能已经
    错了一手（`ERR-20260929-013` 就是这么发生的：`02_deep_research.md:313` 把来源的
    `and argue that` 写成 `we argue that`，下游照抄）。这类命中要单独报出来回原料核。
    """
    ext_doc = (".md", ".txt", ".html", ".json", ".rst")
    # 抓回来的原料常常是**源码**：Octop 那句 `Read access and agent use in chat are
    # never gated.` 出自 `research/octop/src/octop/infra/users/permissions.py:3-4`。
    # 只扫文档扩展名，这类引文就只能在**自己的中间产物**里命中，被判成 weak——
    # 而 weak 的语义正是「去回原料核」，等于把校验器该做的事丢回给人。
    ext_code = (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".sh", ".sql",
                ".yaml", ".yml", ".toml", ".cfg", ".ini", ".java", ".rb", ".c", ".h")
    primary, derived = [], []
    for p in extra:
        p = pathlib.Path(p)
        if p.is_file():
            primary.append((p.name, read_text(p)))
        elif p.is_dir():
            for q in sorted(p.rglob("*")):
                if q.is_file() and q.suffix.lower() in ext_doc + ext_code:
                    primary.append((q.as_posix(), read_text(q)))
    for d in ("research", "sources", "docs", "web"):
        q = project / d
        if q.is_dir():
            for r in sorted(q.rglob("*")):
                if r.is_file() and r.suffix.lower() in ext_doc + ext_code:
                    primary.append((r.as_posix(), read_text(r)))
    for r in sorted(project.glob("[0-9][0-9]_*.md")):
        derived.append((r.name, read_text(r)))
    return primary, derived


def is_verbatim_candidate(q):
    """这条引文是否值得拿去逐字回源？

    只挑**英文整句**：译完之后正文里的中文引文在英文语料里必然查不到（那不是缺陷，
    是设计——中译在正文、逐字原文在章末对照表）。代码片段、路径、单术语也排除。
    """
    nq = norm(q)
    if CJK.search(nq):
        return False
    if len(nq) < 25:
        return False
    if len(ASCII_WORD.findall(q)) < 4:   # 句子至少 4 个词；代码标识符/路径够不上
        return False
    if re.search(r"[=<>{}@$|]", q):
        return False
    # 还要有一个**虚词**才算散文。命令片段、挂载参数、URL 都有 4 个以上的「词」，
    # 却一个虚词也没有：`-v /app/media:/volume1/music`、`https://ifdian.net/a/x`、
    # `/volume/music_tag_web/data/bin/ffmpeg`——实测这三个就是第二项目里的全部误报。
    return bool(PROSE_MARK.search(q))


# --------------------------------------------------------------------------- 检查

def verbatim_segments(q):
    """把一条引文按省略号切成段——引文省略中间段落是常规写法，省掉的部分当然
    查不到，硬拿整条去比对必然误报（`**What the tiers gate today:** … Plain chat
    is not affected —…` 就是这么被判未命中的）。逐段回源，每段都得查到。"""
    return [s for s in ELISION.split(denoise(q)) if is_verbatim_candidate(s)]


def corpus_norm(t):
    """语料侧归一化：先把**行首注释符**去掉，再走通用 norm。

    源码里的句子常跨两行、第二行带注释符：
        # `hermes claw migrate` flags/defaults. Secrets are never included implicitly: --migrate-secrets
        # is required even under --preset full (OpenClaw's two-phase posture); …
    那个行首 `#` 是注释语法不是内容；不去掉，整句在语料里就永远不相邻，引文会被
    误判成「只在自己的中间产物里命中」（实测 `research/hermes/src/claw.py:33-34`）。
    只用在**语料侧**，笔记侧的行首 `#` 是真标题。
    """
    return norm(re.sub(r"(?m)^[ \t]*#+[ \t]?", "", t))


def check_verbatim(files, primary, derived):
    """三态判定：ok（在原始来源里命中）/ weak（只在自己的中间产物里命中）/ miss。"""
    pb = corpus_norm("\n".join(t for _n, t in primary))
    db = corpus_norm("\n".join(t for _n, t in derived))
    total = 0
    weak, miss = [], []
    for path in files:
        for i, line in enumerate(read_text(path).splitlines(), 1):
            for q, kind in quotes_in_line(line):
                # 出处指针（`research/.../deps.py:65-89`、`02_deep_research.md:313`）
                # 是**指针**不是引文，它本来就不该在语料里。
                qs = q.strip()
                if CITE_PATH.match(qs) or CITE_NUM_ARTIFACT.match(qs) or CITE_FULL.match(qs):
                    continue
                for seg in verbatim_segments(q):
                    total += 1
                    # 笔记侧也要去**行首注释 / 标题符**：引文里被引的常常正是来源文档的
                    # 一行标题或一行注释（`#### 1. Secondary profiles must not start
                    # their own gateway`、`# Paths that bypass JWT middleware …`）。
                    # 语料侧走了 corpus_norm、笔记侧却只走 norm，同一个 `#` 一边被去掉
                    # 一边留着，两条真引文被误判成 weak（实测覆盖率 0.92 / 0.98）。
                    nq = corpus_norm(seg)
                    if nq in pb:
                        continue
                    (weak if nq in db else miss).append((path.name, i, kind, seg[:150]))
    return total, weak, miss, [n for n, _ in primary] + [n for n, _ in derived]


def check_style(files, appendix_title):
    boundary, collide, ascii_left, table_bad = [], [], [], []
    for path in files:
        lines = read_text(path).splitlines()
        chaps = split_chapters(lines, "assembled")
        appendix_spans = []
        for chap, start, stop in chaps:
            for i in range(start, stop):
                if appendix_title in lines[i]:
                    # 附录从本行起，到下一章标题 / 文末
                    for j in range(i, stop):
                        appendix_spans.append(j)
                    break
        for i, line in enumerate(lines, 1):
            if "`" not in line:
                continue
            sp = spans(line)
            for si, (a, b, s) in enumerate(sp):
                if i - 1 in appendix_spans:
                    continue                    # 对照表是留档区，不做体例判定
                zh = cjk_only(s)
                if not zh:
                    continue
                # 引导语 = 本条 span 之前、**上一条 span 之后**的文字，且不跨表格单元
                # （`|`）。不定这个界，表格行里前一个单元的引文会被当成后一个单元的
                # 「引导语」，撞车判据立刻误报（实测 3 处全是这么来的）。
                lo = sp[si - 1][1] if si else 0
                lo = max(lo, line.rfind("|", 0, a) + 1)
                lead_raw = line[lo:a]
                # S1 边界叠字：译文首字 == 紧邻其前的末字
                k = a - 1
                while k >= lo and line[k] in "「」（）、，。：；—… \t":
                    k -= 1
                if k >= lo and CJK.match(line[k]) and line[k] == zh[0]:
                    boundary.append((path.name, i, line[k], line[max(0, a - 40):b + 6]))
                # S2 LCS 撞车：只对中译 >= 5 个汉字的引文
                if len(zh) >= 5:
                    lead = cjk_only(lead_raw)[-30:]
                    k2, sub = lcs(lead, zh)
                    if k2 >= 5:
                        collide.append((path.name, i, k2, sub, line[max(0, a - 40):b + 6]))
            # S3 ASCII 残留：只数**反引号之外**的 ASCII 词。引文与出处本来就在反引号
            # 里，把它们算进来，每一行带出处的正文都会变成候选（实测 408 处，绝大
            # 多数是 `research/...` 路径与产品名）；反引号外还剩 >= 2 个 ASCII 词，
            # 才是「该译没译」的可疑串。
            residual, prev_end = [], 0
            for a, b, _s in sp:
                residual.append(line[prev_end:a])
                prev_end = b
            residual.append(line[prev_end:])
            if not line.lstrip().startswith("|"):
                # 只要**相邻**的 ASCII 词串（`plain chat`、`the whole stack`）——
                # 单蹦的产品名/工具名（OpenClaw、Hermes、Wails）是保留类，不该报。
                for m in ASCII_PHRASE.finditer("".join(residual)):
                    ascii_left.append((path.name, i, m.group(0), line.strip()[:110]))
        # S4 对照表结构
        for chap, start, stop in chaps:
            rows = []
            inside = False
            for i in range(start, stop):
                if appendix_title in lines[i]:
                    inside = True
                    continue
                if inside:
                    if lines[i].startswith("#"):
                        break
                    if lines[i].lstrip().startswith("|"):
                        rows.append((i + 1, lines[i]))
            for lineno, row in rows[2:]:        # 跳表头 + 分隔行
                if row.count("|") != 5:
                    table_bad.append((path.name, lineno, "管道数 %d != 5" % row.count("|"), row[:110]))
                    continue
                cells = [c.strip() for c in row.split("|")]
                src = cells[4].strip("`").strip() if len(cells) == 6 else ""
                ok = (not src) or src == "—" or CITE_FULL.match(src) or CITE_NUM_ARTIFACT.match(src)
                if not ok:
                    table_bad.append((path.name, lineno, "出处列非法：%r" % src, row[:110]))
    return boundary, collide, ascii_left, table_bad


def check_copies(copies):
    """copies: [(标签, path, kind)] → (差异列表, 每份副本认到的章, 实际比了几组)。

    第三个返回值是**反静默通过**用的：一章都没认出来时 compared == 0，调用方必须
    判定失败。只报「0 处差异」很容易被读成「副本一致」，实际上是什么都没比。
    """
    data, order = {}, []
    for tag, path, kind in copies:
        lines = read_text(path).replace("\r\n", "\n").split("\n")
        blocks = {}
        for chap, start, stop in split_chapters(lines, kind):
            blocks[chap] = chapter_block(lines, start, stop)
            if chap not in order:
                order.append(chap)
        data[tag] = blocks
    diffs, compared = [], 0
    for chap in order:
        present = [t for t in data if chap in data[t]]
        if len(present) < 2:
            continue
        base = present[0]
        for other in present[1:]:
            compared += 1
            a, b = data[base][chap], data[other][chap]
            if a == b:
                continue
            if len(a) != len(b):
                diffs.append((chap, base, other, "行数 %d vs %d" % (len(a), len(b)), ""))
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    diffs.append((chap, base, other, "第 %d 行" % (i + 1), "%r  <>  %r" % (x[:90], y[:90])))
                    break
    return diffs, {t: [c for c in order if c in b] for t, b in data.items()}, compared


# --------------------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(add_help=True, description="引文纪律统一校验器")
    ap.add_argument("project", help="项目工作区目录，如 workspace/<slug>")
    ap.add_argument("--vault-note", default=None, help="发布到 vault 的成品文件")
    ap.add_argument("--corpus", action="append", default=[], help="逐字回源的语料（文件或目录，可重复）")
    ap.add_argument("--file", action="append", default=[],
                    help="额外逐字回源的文件（相对项目目录解析，可重复），只用于 V；"
                         "典型用途是核对 `02_deep_research.md` 这类自己的中间产物")
    ap.add_argument("--mode", default="all", choices=["all", "text", "verbatim", "style", "copies"],
                    help="all=V+S+C；text=V+S（组装前单章用）；copies 需要同一章 >=2 份副本")
    ap.add_argument("--appendix-title", default="引文对照")
    ap.add_argument("--allow-weak", action="store_true",
                    help="把「仅在自己的中间产物里命中」降级为提醒（默认按硬失败处理）")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    project = pathlib.Path(args.project)
    if not project.is_dir():
        print("项目目录不存在：%s" % project)
        return 2

    # 章节文件的命名各项目不一：`01_为什么….md`、`01-project-positioning.md`、
    # `appendix-a-playback.md`。都收，否则副本比对会静默地只比一份（第二项目就
    # 一个章文件都没匹配到，C 检查等于没跑）。
    ch_dir = project / "chapters"
    chapter_files = sorted({p for pat in ("[0-9][0-9]*.md", "appendix*.md", "*_appendix*.md")
                            for p in ch_dir.glob(pat)}) if ch_dir.is_dir() else []
    merged = project / "chapters" / "_merged.md"
    final = project / "output" / "final_note.md"
    vault = pathlib.Path(args.vault_note) if args.vault_note else None

    # `--file` 相对**项目目录**解析（调用方常在仓库根运行，写 `02_deep_research.md`
    # 的意图是「项目里那份」，不是仓库根那份）。只进 V 的检查集，不进 S/C。
    extra_files, missing = [], []
    for f in args.file:
        q = pathlib.Path(f)
        q = q if q.is_absolute() else (project / f)
        (extra_files if q.is_file() else missing).append(q)
    if missing:
        print("--file 指定的文件不存在：%s" % ", ".join(str(m) for m in missing))
        return 2

    body_files = list(chapter_files)
    if merged.is_file():
        body_files.append(merged)
    if final.is_file():
        body_files.append(final)
    if vault and vault.is_file():
        body_files.append(vault)
    if not body_files:
        print("没找到任何待检查文件（%s/chapters/*.md）" % project)
        return 2

    print("=" * 72)
    print("引文纪律校验  project=%s  mode=%s" % (project.as_posix(), args.mode))
    print("待检查 %d 个文件；章文件 %d 个%s"
          % (len(body_files), len(chapter_files),
             ("；额外逐字回源 %d 个（%s）" % (len(extra_files), ", ".join(p.name for p in extra_files)))
             if extra_files else ""))
    print("=" * 72)

    hard_fail = 0
    report = {}

    if args.mode in ("all", "text", "verbatim"):
        primary, derived = collect_corpus(project, args.corpus)
        total, weak, miss, names = check_verbatim(body_files + extra_files, primary, derived)
        print("\n[V] 逐字回源：英文整句引文 %d 处；原始来源命中 %d / 仅自己中间产物命中 %d / 未命中 %d"
              % (total, total - len(weak) - len(miss), len(weak), len(miss)))
        print("    语料 %d 个文件（primary %d / derived %d）" % (len(names), len(primary), len(derived)))
        print("    ⚠ 只在自己的中间产物里命中——中间件本身可能错了一手（ERR-20260929-013），回原料核：")
        for tag, line, kind, q in weak[:20]:
            print("    · %-28s L%-5d %s" % (tag, line, q))
        print("    ✗ 未命中：")
        for tag, line, kind, q in miss[:40]:
            print("    · %-28s L%-5d [%s] %s" % (tag, line, kind, q))
        if len(miss) > 40:
            print("    ... 另有 %d 处" % (len(miss) - 40))
        report["verbatim"] = {"total": total, "weak": weak, "miss": miss}
        # 未命中就是硬失败——这是 ERR-20260929-013 那一类（引文带来源 ID、句子也在，
        # 但字面被改过）。「只在自己的中间产物里命中」默认也算失败：中间件本身可能
        # 已经错了一手，要么把语料补全让它逐字命中原始来源，要么人工回原料核。
        # 确属语料拿不到（比如没抓 `research/`）时用 --allow-weak 显式降级。
        if miss:
            print("    → 判定：未命中按硬失败处理")
            hard_fail += 1
        if weak and not args.allow_weak:
            print("    → 判定：仅中间产物命中按硬失败处理（--allow-weak 可降级为提醒）")
            hard_fail += 1

    if args.mode in ("all", "text", "style"):
        boundary, collide, ascii_left, table_bad = check_style(body_files, args.appendix_title)
        print("\n[S1] 边界叠字候选：%d 处（人工判：真叠字 / 巧合）" % len(boundary))
        for tag, line, ch, ctx in boundary[:20]:
            print("    · %-28s L%-5d 叠字「%s」 %s" % (tag, line, ch, ctx.strip()[:80]))
        print("\n[S2] LCS 撞车候选（>= 5 个汉字）：%d 处（人工判；表格「语义列 vs 逐字列」不算）" % len(collide))
        for tag, line, k, sub, ctx in collide[:20]:
            print("    · %-28s L%-5d LCS=%d 「%s」 %s" % (tag, line, k, sub, ctx.strip()[:70]))
        phrases = {}
        for tag, line, words, ctx in ascii_left:
            phrases.setdefault(words, (tag, line, ctx))
        print("\n[S3] 反引号外的相邻 ASCII 词串：%d 处，去重后 %d 个（逐个确认属于保留类）"
              % (len(ascii_left), len(phrases)))
        for words, (tag, line, ctx) in phrases.items():
            print("    · %-28s L%-5d %-30s %s" % (tag, line, words, ctx[:66]))
        print("\n[S4] 引文对照表结构：%d 处不合格" % len(table_bad))
        for tag, line, why, row in table_bad[:20]:
            print("    · %-28s L%-5d %s | %s" % (tag, line, why, row[:80]))
        hard_fail += 1 if table_bad else 0
        report["style"] = {"boundary": boundary, "collide": collide,
                           "ascii": ascii_left, "table_bad": table_bad}

    if args.mode in ("all", "copies"):
        copies = []
        for i, p in enumerate(chapter_files):
            copies.append((p.name, p, "chapter"))
        if merged.is_file():
            copies.append(("_merged.md", merged, "merged"))
        if final.is_file():
            copies.append(("final_note.md", final, "assembled"))
        if vault and vault.is_file():
            copies.append((vault.name, vault, "assembled"))
        diffs, inventory, compared = check_copies(copies)
        print("\n[C] 多副本一致：%d 份副本，实际比对 %d 组（章 × 副本对），发现 %d 处差异"
              % (len(copies), compared, len(diffs)))
        for tag, chaps in inventory.items():
            print("    · %-32s 认到 %d 章：%s" % (tag, len(chaps), ",".join(chaps) or "（无）"))
        for chap, base, other, why, ctx in diffs[:30]:
            print("    ! %s  %s <> %s  %s  %s" % (chap, base, other, why, ctx))
        if compared == 0:
            print("    ! 一章都没认出来——**不能算通过**：章节标题写法没被识别，检查 CH_HEAD")
            hard_fail += 1
        else:
            hard_fail += 1 if diffs else 0
        report["copies"] = {"diffs": [(c, a, b, w, x) for c, a, b, w, x in diffs],
                            "inventory": inventory}

    if args.json:
        import json
        pathlib.Path(args.json).write_bytes(
            json.dumps(report, ensure_ascii=False, indent=1).encode("utf-8"))

    print("\n" + "=" * 72)
    if hard_fail:
        print("判定：❌ 有硬失败（V 逐字回源 / S4 对照表结构 / C 多副本一致）")
        return 1
    print("判定：✅ 无硬失败（S1/S2/S3 是候选清单，仍需人工判）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
