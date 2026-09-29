# -*- coding: utf-8 -*-
"""给 canonical 的 note-beautifier SKILL.md 补一节「引文中译」验收清单。

用 read_bytes/write_bytes 手工拼 CRLF：该文件是 CRLF，`Edit` 工具可能把它
归一成 LF（内容对，行尾变），而 `.agent-sync --check` 对行尾不敏感、不会报，
于是 canonical 与镜像长期一个 LF 一个 CRLF。（见 .learnings/RULES.md 的
「不要用 read_text/write_text 改被按行解析的文件」。）
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("D:/Study-Notes")
P = ROOT / ".agents/skills/note-beautifier/SKILL.md"
raw = P.read_bytes()
crlf = b"\r\n" in raw
t = raw.decode("utf-8")
print("行尾:", "CRLF" if crlf else "LF", "| 字节:", len(raw))
t = t.replace("\r\n", "\n") if crlf else t     # 先在 LF 上做替换，最后按原行尾回填

ANCHOR = "- [ ] 发布后**逐行读一遍成品**：校验绿灯 ≠ 产物正确\n"
assert t.count(ANCHOR) == 1, "锚点命中 %d 次" % t.count(ANCHOR)

BLOCK = """- [ ] **引文中译（把正文里的成句英文引文换成中译时）**：
      中译只覆盖**成句英文**；**代码、命令、配置键、路径、文件名、产品名、单个技术术语**
      保留原文。改完扫一遍残留的「≥2 个 ASCII 词」串，逐个确认属于保留类。
      逐字原文**必须留档**——章末加「引文对照（原文 / 中译 / 出处）」表，只换不留档
      等于把引用链剪断，读者再也无法回源核对。
      **四份副本一起改、改完逐字比对**（章文件 → 拼接件 → 组装件 → vault 成品）：
      改一份就发布，四份必然漂移。译完还要查两件事，它们在原文是英文时都看不出来：
      ① 引导语 / 括注与中译**撞车**（引导语与引文变成同一句话），判据 = 两者
      **最长公共汉字子串 ≥ 5**，挑出来逐条人工判（表格「语义列 vs 逐字列」的天然重字
      不算），改法二选一：引导语缩成话题标签，或括注里那截中译删掉只留出处；
      ② 「出处」列**宁空不猜**——正文列举的**产品文件名**（`SOUL.md`、`MEMORY.md`）
      不是来源件，当出处会让读者去查错文件，**错的出处比空着更糟**；查不到就写 `—`
      并在表格引导句里说明 `—` 的含义。
      逐文件保留原行尾（`read_bytes`/`write_bytes` + 手工嗅探），改正文前先落一份
      **逐字节回滚点**，并写一个能执行的回滚脚本（用 `git show <基线提交>:<路径>` 对照验证）。
"""

# 注意：这一节要嵌在 ```markdown 围栏内的清单里，所以每条以 `- [ ]` 起头。
t = t.replace(ANCHOR, ANCHOR + BLOCK)
out = t.encode("utf-8") if not crlf else t.replace("\n", "\r\n").encode("utf-8")
P.write_bytes(out)
print("写入:", len(out), "字节 | 行尾:", "CRLF" if b"\r\n" in out else "LF")
