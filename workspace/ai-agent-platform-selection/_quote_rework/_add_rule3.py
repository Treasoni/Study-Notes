# -*- coding: utf-8 -*-
"""把「短引文边界叠字」这条补丁写进 canonical skill 与 RULES.md。

两个文件都是 CRLF。替换前先归一到 LF 再写回 CRLF——不要用 Edit 工具，
它可能把整文件悄悄转成 LF，而 `.agent-sync --check` 对行尾不敏感、不会报。
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
assert (ROOT / "CLAUDE.md").is_file()

PATCHES = [
    (
        ROOT / ".agents/skills/note-beautifier/SKILL.md",
        "      **最长公共汉字子串 ≥ 5**，挑出来逐条人工判（表格「语义列 vs 逐字列」的天然重字\n"
        "      不算），改法二选一：引导语缩成话题标签，或括注里那截中译删掉只留出处；\n",
        "      **最长公共汉字子串 ≥ 5**，挑出来逐条人工判（表格「语义列 vs 逐字列」的天然重字\n"
        "      不算），改法二选一：引导语缩成话题标签，或括注里那截中译删掉只留出处。\n"
        "      **该判据只覆盖长引文**（中译 ≥ 5 个汉字）——短引文整条被跳过，要另扫一遍\n"
        "      **边界叠字**（译文首字 == 紧邻其前的末字）：引导语写「合计约」、紧接的中译又以\n"
        "      「约」开头，里外两个「约」就是这么漏掉的。窄判据误报少（「其一，一个 Gateway…」\n"
        "      的「一」是巧合、\n"
        "      「找到它——`它在云上…`」两边都是指代同一对象的主语，都判为不动），\n"
        "      仍要逐条人工判；\n",
    ),
    (
        ROOT / ".learnings/RULES.md",
        "① 引导语 / 括注与中译**撞车**（变成了同一句话。判据：两者最长公共汉字子串 ≥ 5；",
        "① 引导语 / 括注与中译**撞车**（变成了同一句话。判据：两者最长公共汉字子串 ≥ 5，**只覆盖中译 ≥ 5 个汉字的长引文**；短引文另扫**边界叠字**——译文首字 == 紧邻其前的末字，如「合计约 `约 1,300 token`」的里外两个「约」；",
    ),
]

for path, old, new in PATCHES:
    raw = path.read_bytes()
    text = raw.decode("utf-8").replace("\r\n", "\n")
    n = text.count(old)
    assert n == 1, "%s：锚点命中 %d 次（期望 1）" % (path.name, n)
    text = text.replace(old, new)
    path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    print("[OK] %-24s %d -> %d bytes" % (path.name, len(raw), len(path.read_bytes())))
