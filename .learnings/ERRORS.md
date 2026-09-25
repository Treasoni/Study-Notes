# ERRORS.md

活跃错误记录。当前 **5** 条（`ERR-20260918-008` / `-009` / `-010` / `-011` / `ERR-20260924-012`，均已 fixed，待 `/maintain-learnings` 复核后归档）。

本机最近一次维护：2026-09-18（`/digest`）。本轮新增 3 条，全部来自 `learning-note-flow / hermes-home-assistant`
的 P5–P7 收尾轮：归一层错位（发布件漏归一）、归一脚本两处缺陷（插入点 + 非幂等）、记录数字取自历史输出。

**源头修复状态（未全部完成，需 `/maintain-learnings` 接手）**：

- `-008` / `-009`：本轮的直接修复是新建 `workspace/hermes-home-assistant/normalize_chapters.py`（把归一做在源文件上、
  连跑三遍验证幂等），但**项目级 skill 还没改**——`note-beautifier` 的分册发布自检节应补「单一归一层 + 幂等验收（跑两遍 diff 为空）」两项。
- `-010`：处置办法已写进 `.learnings/RULES.md` 的 Do 节，**尚未**落到任何 skill 或 workflow 的产出记录模板。
- `-011`（python 文本模式写盘把 state file 转成 CRLF）：两条预防措施已收进 `.learnings/RULES.md` 的 Don't 节（① 禁止用文本模式重写按行解析的文件 ② 禁止手工改 `> [PN]` 阶段行）；**尚未**落到 `todo-state.sh` 与项目级规则文件。
  与 `RULES.md` 同属「按行解析的文件不得用 `read_text`/`write_text`」这一类，建议 `/maintain-learnings` 一并收成一条规则。
- **压缩阈值已破**：本文件现 175 行（阈值 100）。本轮不压缩，因为三条新错误都是**未在源头修复**的活跃条目，
  归档等于把未修的问题埋掉。请下一轮 `/maintain-learnings` 先做源头修复（改 `note-beautifier` 分册发布自检节 +
  产出记录模板），验证后再连 `LRN-20260912-012` 一起评估归档。
- 注意：`-008` / `-009` 与 RULES.md 既有的「拼接式文档生成：追加前先对既有尾部做幂等归一」属**同一类**，
  说明该条规则**在真实运行里没有拦住**（规则存在≠会被读到）。这属于「同类错误复发 + 已有规则仍失效」，
  按 `digest` 的规定应转 `maintain-learnings` 做源头修复，而不是就地再压一遍。

另一台机器上的一轮维护：2026-09-23（`/maintain-learnings`）。本轮归档三条 2026-09-23 错误记录，
均在源头修复（原文摘要、修复路径与验证方式见 `.learnings/archive/2026-09-23-maintenance.md`）：

- `note-assembler：章标题降级未级联到子标题` → Step 4 改为「子树下沉 + 重新解析标题树断言层级」
- `todo-state.sh：workflow 定义调用了未实现的动作` → 脚本补齐 `mode` / `confirm`，并新增探针式动作守卫
- `chapter-writer：官方引文被串成 828 字符引文墙` → 写作规范新增引文摆放阈值与反例边界

上一次维护：2026-09-14（`/maintain-learnings`）。本轮两条活跃错误均已在源头修复后归档：
`learning-note-flow / P6 分册发布脚本自造 4 处文本缺陷` → 落到 `note-beautifier` 的
「分册 / 长文档发布」自检节；`workflow state file 手工改写阶段行` → 落到
`workflow-todo-state` State Rules 的硬约束。修复路径、验证方式与处理结果见
`.learnings/archive/2026-09-14-maintenance.md`。

更早一轮的 `ERR-20260911-007`（父 agent 转述来源论断导致伪引证）已在源头修复——
`.agents/skills/research-collector/SKILL.md` 的 Source policy 增加「不得转述论断」硬约束，
详见 `.learnings/archive/2026-09-11-maintenance.md`。

新增错误请按 `digest` 的格式追加到本文件末尾（错误 / 触发场景 / 根因 / 修复 / 预防措施）；
修复落到机制并验证通过后，才可移入 `.learnings/archive/`。

---

## [ERR-20260918-008] learning-note-flow / P6 — 归一动作落在下游产物层，发布件根本没被归一

**Logged**: 2026-09-18T01:21:05+0800
**Priority**: high
**Status**: fixed（已上移到源文件层并验证）
**Area**: note-beautifier / publish_volume.py

### Summary
尾部导航的「归一」只写在 `assemble_note.py`（合并件）里，而发布器 `publish_volume.py` 是**直接读 `chapters/` 源文**的——于是出现了「合并件是齐的、发布件是花的」：合并件归一好了，10 篇发布件发出去的仍是未归一的原始写法（粗体引导词 / 裸段落 / `###` 三种混用）。

### Error
```
(无报错) 发布脚本两条断言全绿、退出码 0，成品却是未归一的原文
```
这类错误**不会自己报出来**：断言校验的是「发布件与其源文件逐字可逆」，源文件本身就是花的，所以逆变换当然成立。

### Context
同一份单源内容有两条下游（合并件 + 分册发布件），清洗规则被放在了其中一条下游里。发布脚本改用 `chapters/` 而不是合并件取值后，规则对第二条下游完全失效。

### 修复
- 把归一提炼到 `workspace/hermes-home-assistant/normalize_chapters.py`，**做在源文件（`chapters/`）上**，且只做一次。
- 下游（`assemble_note.py` / `publish_volume.py`）只做机械变换，不再各自持有一套规则。
- 重跑组装 + 发布，并对 10 篇逐行复核（剥掉标题行两侧对比）确认 10/10 一致。

### 预防措施
- 单源多下游的管道里，「归一 / 清洗」只能有**一个归属层**，且必须在**最上游的源文件**上；任何下游脚本里出现的改写规则，都要问一句「另一条下游有没有这份规则」。
- 断言「发布件 == 源文件」**不能**证明发布件正确——它只证明变换可逆。要么再加一条「源文件本身满足最终形态」的断言，要么人工读一遍成品（见 RULES：跑绿 ≠ 正确）。

---

## [ERR-20260918-009] learning-note-flow / P6 — normalize_chapters.py 两处缺陷：插入点取「第一条脚注定义」、规则非幂等

**Logged**: 2026-09-18T01:21:05+0800
**Priority**: high
**Status**: fixed（已改并连跑三遍验证幂等）
**Area**: learning-note-flow / P6 归一脚本

### Summary
同一轮里发现两处独立缺陷：(a) 体例说明块的插入点用「文件中第一个脚注定义」定位，结果插进了**正文中段**；(b) 一条零宽前瞻规则不消费文本，重复运行会重复插标题并每轮累积一个空行。

### Error
```
(a) `### 本章来源` 出现在第 4、5 章正文中间，而不是文末脚注定义块之前
(b) 第二次运行：`### 下一章预告` 出现两次，且两标题之间多一个空行
```
第一次修复用的是「事后折叠重复标题」（后置 `DUP_NAV` 正则），**不充分**：`git diff` 显示每次运行仍稳增一个空行（`348a349 >`、`254a255 >`）。

### Context
第 4、5 章的脚注定义是**分散写的**——正文前中段散着几条（跟在被引段落后面），文末另有一个密集块。「第一个定义」≠「文末那个块」。另一处：`^(?=下一章换)` 是零宽前瞻，匹配成功但 `m.end()` 仍在行首，于是每轮都在同一位置再插一次标题。

### 修复
- (a) 改为 `trailing_def_start()`：从**最后一个非空行**向上走，只要该行是 `^\[\^…\]:` 或空行就继续，得到的才是尾部连续定义块的起点；找不到就报错退出、不写盘。
- (b) 改为**前置判定**：处理每行时先看「上一个非空行」是否已经是该标题，是则只保留其后的段落、不再插标题；后置折叠只留作兜底。
- 配 `strip_signpost()` 先移除任何既有说明块（含此前插错位置的那份）再重插，使脚本对新旧两种历史形态都收敛。
- 验收方式：连跑**三遍**，后两遍对 10 个文件全部报「无变化」。

### 预防措施
- 任何「重复运行」的脚本，幂等性的验收方式是**跑两遍 + diff 为空**，不是「看着不会重复」；只做一类「事后折叠」而不改前置判定，通常只是把重复变成另一种形式的累积。
- 定位插入点要用**语义稳定的锚**（尾部连续块、最后一个匹配项），不要用「第一个匹配项」——同一种标签在文件里可能有多处不同语义的实例。
- 脚本要能对**历史遗留的错误形态**收敛（先清理再重写），而不是只对「干净输入」正确。

---

## [ERR-20260918-010] learning-note-flow / P5+P7 — 工作记录里的数字取自历史输出，与当前产物不一致

**Logged**: 2026-09-18T01:21:05+0800
**Priority**: medium
**Status**: fixed（已当场重新取数并订正）
**Area**: workflow state file / 记录纪律

### Summary
workflow state file 里写下的成品数字与产物实际不符：记录「271094 B / 正文 44457 汉字」，当前成品实为 **271254 B / 44499 汉字**；P5 段记录「`### 本章来源` 仅 7 章、`### 本章小结` 仅 4 章」，实际是 **9 章 / 7 章**。

### Error
```
(无报错) state file 记录与 workspace/…/output/final_note.md 实测值不符，差 160 B / 42 汉字
```

### Context
数字是**凭上下文里的历史脚本输出**写的，而 P6 又给第 4、5 章补了两个「本章来源」体例说明块（成品变大 ~870 B），我写记录时没有重新取数。计数错误同源：把「Callout 形态的 `> [!summary] 本章小结`」算成了标题。

### 修复
- 当场重跑 `assemble_note.py` 取数（并确认脚本幂等：连跑两次 md5 相同，`ac94dcc6…`）。
- state file 两处订正：P5 段标注「本段数字为 P5 时点值」并补当前值；「最终产出」段改为 271254 B / 44499 汉字（另注含代码块为 45521）。
- 分册体积重新逐文件统计（10 篇 + README = 277014 B / 46238 汉字），第一次手算错写 268964 B，当场按 `ls -l` 复核改正。

### 预防措施
- 写进「最终产出 / 组装记录」的体积、字数、章数、脚注数，必须**当场重新运行取数或重新计数**，并把命令一起留着；不要从上下文里的旧输出誊抄。
- 产物在记录之后又被改动时，同一组数字的所有出现处都要一并 grep 更新（本轮 state file 的 P5 段与「最终产出」段就是两处）。
- 手算的合计值不算数：体积/字数用工具算（`ls -l` / python 计数），算完再复核一遍。

---

## ERR-20260918-011 — python 文本模式写盘把 state file 整篇转成 CRLF，静默打穿 todo-state 守卫

**Date**: 2026-09-18
**Status**: fixed
**Area**: workflow state file / 行尾纪律 / 状态机守卫

### Summary
用 python 的 `Path.read_text()` / `write_text()` 改 workflow state file 的一行状态，
在 Windows 上会把**整篇**文件的 LF 换成 CRLF（176 行）。`todo-state.sh` 用 perl 逐行正则判定
「前置阶段是否已关闭」，行尾多出的 `\r` 让 `\{(?:complete|skipped)\}$` 失配，于是**已完成的 P0 被判为未关闭**，
`complete P3` 直接失败。守卫本身没坏，行尾把它骗过了。

### Error
```
todo-state: previous phase is not complete or skipped: P0
todo-state: phase must be in progress before complete: P3
```

### Context
两处叠加：

1. **行尾**：`read_text(encoding="utf-8")` 默认 `newline=None`，读取时把 CRLF 折成 LF；
   写回时 `open(..., "w")` 同样 `newline=None`，又把 `
` 按 `os.linesep` 展开成 CRLF。
   于是一次「只改一行」的编辑变成全文件行尾重写，且**没有任何输出提示**。
2. **越权改状态行**：同一轮里我先是**手工**把 `> [P3] 🔲 进行中 {in_progress}` 改成 `{complete}`——
   而阶段状态行按项目规则只能由 `todo-state.sh` 写。脚本读到 `{complete}` 后拒绝再 complete，
   报「phase must be in progress before complete」，把行尾问题掩盖了一层，多花了一轮才定位到真因。

### 修复
```python
b = p.read_bytes()
b = b.replace(b"\r\n", b"\n")
p.write_bytes(b)          # CRLF 176 -> 0，LF 176
```
归一后 `.claude/scripts/todo-state.sh … complete P3` 一次通过。

### 预防措施
- 改 workflow state file（以及任何会被 shell / perl / awk **按行解析**的文件）一律用
  `read_bytes()` / `write_bytes()`，或 `open(..., newline="")`；**不要**用 `read_text` / `write_text`。
- 改完当场数一遍行尾：python `b.count(b"\r\n") == 0`。别靠肉眼看 `file` 输出的 "UTF-8 text"
  （CRLF 文件同样是 "UTF-8 text"，看不出区别）。
- **不要手工碰 `> [PN] …` 阶段行**。要改状态就调 `todo-state.sh`；
  要先写产物再推进状态的话，顺序是「先写说明段落与复选框 → 再 `todo-state.sh complete PN`」，
  阶段行留给脚本写。手工写进去的 `{complete}` 会让脚本的 `phase_has_status "in_progress"` 预检失败。
- 排查这类「脚本说前置阶段没完成」时，**先验行尾再查内容**：这类假阴性只有一个来源，
  而内容层面的原因往往要读全脚本才排除得掉。

---

## [ERR-20260924-012] learning-note-flow / P0 — workflow.md 记载的 `confirm` / `mode` 两个 todo-state 动作在脚本里不存在

### Summary
`.claude/workflows/learning-note-flow/workflow.md` 的用户确认检查点表写明用
`todo-state.sh <state> confirm P0` 记录确认、用 `mode` 动作切换大纲/随性模式；
但 `.claude/scripts/todo-state.sh` 只实现了 `start|complete|skip|block` 四个动作，
执行 `confirm P0` 直接报 `unknown action: confirm` 并非零退出。
状态文件里的 `mode: outline` 是我手工写进去的，不是脚本写的。

### Error
```
$ bash .claude/scripts/todo-state.sh "workspace/workflow-runs/....workflow.md" confirm P0
todo-state: unknown action: confirm
```

### Context
- 运行：`vps-node-panel-tutorial`（learning-note-flow，P0 检查点）。
- workflow.md 是 canonical 工件（`.codex/` 侧），todo-state.sh 同属 scripts 区域，
  两者分属不同 canonical 目录、由不同 profile 路径同步，**没有任何校验会发现二者口径不一致**。
- 同类风险面：workflow.md 里凡出现"用某某动作"的句子，都要与脚本的 action 白名单对齐。

### 修复
本轮改为**手工**在 state file 的「用户确认记录」表追加确认行（python 写入，
`assert t.count(old)==1` 保证插入点唯一，`newline=''` 防 CRLF 回归），
并在推进状态时只用脚本支持的 `complete`。**未修源头。**

### 预防措施
- 源头修复二选一：① 给 `todo-state.sh` 补 `confirm` / `mode` 动作；
  ② 改 workflow.md，把确认记录改为「由父流程写表格 + 用 `complete` 推进状态」。
  **推荐 ②**，因为确认记录本质是自由文本表格，脚本化收益低。
- 在 `.claude/scripts/sync-workflow-routing.sh --check` 之外，增加一项
  「workflow.md 提到的 todo-state 动作 ⊆ 脚本白名单」的一致性检查，
  否则这类跨 canonical 目录的文档漂移会一直靠人工撞出来。
- 保持既有做法：**凡在文档里看到脚本动作，先在脚本源码里 grep 白名单再执行**，
  不要照文档直接跑。

### 补记（2026-09-26 合并 `origin/main` 时）

另一台机器在 2026-09-23 的 `/maintain-learnings` 轮里独立撞上同一事故，并**修了源头**；本次合并已把那部分改动
（连同 `.learnings/archive/2026-09-23-maintenance.md`）落进本机：

- `.claude/scripts/todo-state.sh` / `.codex/scripts/todo-state.sh` 动作白名单补上 `mode` / `confirm`，各自带处理器（`mode` 只改 frontmatter `mode` 键，`confirm` 只追加 `## 用户确认记录`）。
- `.claude/scripts/workflow-health-check.sh` / `.codex/scripts/workflow-health-check.sh` 新增**探针式动作守卫**：解析每个 workflow 定义里对 `todo-state.sh` 的调用并按实际探针逐个执行，带控制组探针与「空绿」保护；已在 `sync-workflow.md` 注册调用点。
- `.learnings/RULES.md` 的 Watch For 里那条「`todo-state.sh` 只有 `start|complete|skip|block`（没有 `confirm`）」的绕行规则，已随合并改写为现行语义。

因此本条按「已源头修复」处理，与本机其余 4 条一并等 `/maintain-learnings` 复核后归档。

---
