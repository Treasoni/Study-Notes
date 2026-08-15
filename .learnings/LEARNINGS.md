# LEARNINGS.md

## [LRN-20260815-001] correction — 教程章节结构「一章一节一文件」

**Logged**: 2026-08-15T23:21:14+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
教程类笔记章节必须「一章一节一文件」：顶级小节只对应一个文件/产物；同一文件的多个字段（如 package.json 的 name / dependencies / files）只能是该文件小节下的子节（####），不能升格成与文件平级的顶级小节。

### Details
- 事实：用户指出 §6.2（依赖双份）和 §6.4（files 白名单）本质是 `package.json` 的字段，却被设成与 §6.1 package.json 平级的顶级小节，破坏「一个顶级小节对应一个文件」的结构。同样逻辑下 §6.2 应在 §6.1 之下。
- 根因：组织章节时按「主题」而非「产物（文件）」切分，把字段级内容当独立主题展开，导致读者目录里「文件」与「文件的字段」层级混乱。
- 正确做法：写/改教程时先列出「本章涉及哪些文件/产物」，以文件为顶级小节；文件内的字段/子主题用 `####` 子节（如 6.1.1 最小字段 / 6.1.2 依赖双份 / 6.1.3 files 白名单）。

### Suggested Action
- 每次教程章节结构定稿前自检：每个顶级 `###` 是否都对应一个文件/命令/产物？凡属同一文件的字段一律收进该文件小节的 `####`。

---

## [LRN-20260815-002] best_practice — 代码片段标注文件 + 先完整后分块

**Logged**: 2026-08-15T23:21:14+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
教程里的每个代码块必须标明所属文件/目录（文件头注释），且先展示完整文件（先睹为快）再逐段讲解，不让读者猜「这段代码放哪个文件夹」。

### Details
- 事实：用户对 §3.3/§3.4 只给零散片段提出：「这里的 3.3 和 3.4 中的代码放哪个文件夹你不说？不先把完整代码给我再解释？」
- 根因：默认按「讲解顺序」切代码块，忽略读者需要先见全貌、再入细节，也需要知道每个片段在文件里的落点。
- 正确做法：① 代码块首行加文件路径注释（`// git-log-plugin/src/tools/git-log.ts`）；② 讲解多段前先整文件展示一次；③ 文件归属变化处（新建/切换文件）用命令或文字点明。

### Suggested Action
- 写或更新教程代码段落时套用「先完整文件 → 标注路径 → 逐段拆讲」三步；代码块归属不明的，先补路径再继续。

---

## [LRN-20260815-003] correction — 修复命令类错误先核实再改笔记

**Logged**: 2026-08-15T23:21:14+0800
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
用户报命令/路径错误时，先沿真实代码路径核实「路径相对哪里解析、文件实际在哪」，一次改对再写入笔记；不要凭 shell 直觉假设、改一次错一次。

### Details
- 事实：`pnpm dsh web --patch` ENOENT 修复中，我第一轮把笔记改成「patch 文件在仓库根、用 `./dev-cordis.patch.yml`」，用户在仓库根复跑仍 ENOENT；第二轮才按用户纠正改为「文件在 `git-log-plugin/`，仓库根执行 `./git-log-plugin/dev-cordis.patch.yml`」。
- 根因：`loadOverlayPatches` 直接把 `--patch` 的 overlay 路径当文件系统路径解析（相对 dsh 仓库根，而非 shell 当前目录）；我此前没读源码、也没确认 patch 文件实际所在目录就下笔。
- 正确做法：① 先读命令实现源码确认路径解析基准；② 确认被引用文件真实位置；③ 再统一改写笔记全文（含标题、表格、示例命令的所有副本）。

### Suggested Action
- 任何「命令应该怎么写」的断言进入笔记前，用源码 + 文件系统实况验证一次；改动涉及多处引用时，改完 grep 全文确认无残留旧表述。

---

## [LRN-20260816-001] best_practice — 用户决策用紧凑文本菜单，不用多问题对话框

**Logged**: 2026-08-16
**Priority**: high
**Status**: pending
**Area**: workflow

### Summary
需要用户做方向/选项决策时，用带推荐默认值的紧凑文本菜单；不要用多问题 AskUserQuestion 对话框。确认偏好简短（「可以」级）。

### Details
- 事实：learning-note-flow P0 我弹出 4 问对话框被用户直接拒绝；用户随后一句话「概念理解+上手」给方向。之后全部阶段门都用「可以」「直接写完」等简短确认通过。
- 根因：默认套用结构化提问工具，没意识到该用户偏好低摩擦文本交互、靠推荐默认值收敛。
- 下次做法：方向选择用 1-3 行文本菜单 + 标注推荐项；每次只问一个必要问题；确认后不再复述。

### Suggested Action
- 需要用户决策的检查点，优先文本菜单 + 默认值；仅在真正分叉且文本无法表达时才用对话框。

---

## [LRN-20260816-002] knowledge_gap — dsh 文档 canonical 源在 GitHub 仓库，github.io 镜像 404

**Logged**: 2026-08-16
**Priority**: medium
**Status**: pending
**Area**: research

### Summary
DeepSeek-Harness 的 github.io 扩展 Cookbook URL 返回 404；canonical 在仓库内 `docs/cookbook/extension-cookbook.md`，经 raw.githubusercontent.com 访问成功。

### Details
- 事实：`deepseek-harness.github.io/deepseek-harness/cookbook/extension-cookbook` 404；改用 `raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/docs/cookbook/extension-cookbook.md` 后成功。
- 根因：项目只发布部分文档到 Pages 镜像，深层路径未同步；仓库 blob/raw 是唯一权威。
- 下次做法：GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}`；github.io 只在确认可用时用。

### Suggested Action
- research-collector / WebFetch 阶段，GitHub 项目文档先试仓库 raw 路径。

---

## [LRN-20260816-003] best_practice — 独立章节合并必须按章命名空间化脚注 ID

**Logged**: 2026-08-16
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
多篇由并行/串行 writer 独立写作的章节合并成一个 Markdown 文档时，各章重复的脚注 ID 会互相覆盖（后定义胜出），必须统一加章节前缀（`[^cN-ID]`）。

### Details
- 事实：7 章合并后出现 19 个重复脚注 ID（S2/S3/S5/S6/S7/S8/6.3 等），合并文档里后定义覆盖先定义，引用错位。
- 根因：每章都从同一批来源（S1-S10）编号，独立写作时不知道其他章已占用同名脚注。
- 下次做法：① 写作阶段约定每章脚注前缀；② 或组装阶段统一 perl 命名空间化 `[^cN-ID]` 并全文档核对 ref/def 配对（74 对、0 重复）。

### Suggested Action
- P5 组装检查清单加一条：合并后 grep 重复脚注 ID 并命名空间化。

---

## [LRN-20260816-004] knowledge_gap — 本机 perl 处理中文必须显式 utf8，否则字符类正则静默失败

**Logged**: 2026-08-16
**Priority**: high
**Status**: pending
**Area**: scripts

### Summary
Windows/Git Bash 下 python/python3 是商店存根不可用，用 perl 处理含中文 Markdown 时，字符类正则必须 `use utf8;` + `use open ":std", ":encoding(UTF-8)"`，否则按字节匹配导致脚本静默 no-op。

### Details
- 事实：第一次 perl 拆分脚本只加 `-CSD`，`[一二三四五六七]` 匹配不到，输出「无变化」且无报错；补 `use utf8;` 后才真正执行（8 段、74 defs、0 重复）。
- 根因：perl 默认把源码字面量当字节串，中文字符类不匹配 UTF-8 字节序列；且无报错，是静默失败。
- 下次做法：perl 处理非 ASCII 文本，脚本开头固定三件套：`use utf8;`、`use open ":std", ":encoding(UTF-8)"`、文件句柄加 `:encoding(UTF-8)`；先小样本验证匹配数>0。

### Suggested Action
- 需要文本处理脚本时优先考虑 perl/node；perl 处理中文必须带 utf8 三件套并先小样本验证。

---
