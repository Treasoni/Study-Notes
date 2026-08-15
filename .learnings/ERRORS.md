# ERRORS.md

## [2026-06-01] OpenSpec 学习笔记 - Session Errors

### 问题记录
- 无重大错误。WebFetch 无法访问 github.com，需改用 GitHub API 替代方案

## [2026-07-11] Codex 手动配置指南 - Session Errors

### 问题记录
- beautify 阶段 YAML frontmatter 中 `sources` 字段的 `[来源: doc-XX]` 标记未正确引用，导致 Obsidian 解析失败。修复方法：将整个值用双引号包裹，或改用纯字符串列表格式。教训：YAML frontmatter 中所有含特殊字符（`[]`, `:`）的值都必须正确引用

## [2026-07-31] 虚拟机教程表格嵌套

### 错误：表格嵌套在编号列表中导致 Obsidian 不渲染

**错误**：用户反馈 Obsidian 中某表格"显示有问题"——表格在预览模式下没有被渲染为表格，而是显示为纯文本或错乱。

**触发场景**：在 `### 3.1 新建虚拟机向导` 中，步骤 3 的选择安装方式表格有 3 空格缩进，被认为是编号列表项的一部分。

**根因**：Obsidian 的 Markdown 解析器不支持在列表（有序或无序）内渲染表格。带缩进的表格被视为列表项的继续内容，而不是独立的表格块。

**修复**：
- 去掉表格前的缩进
- 将步骤 3 改为 `3. 选择安装方式（参考下方表格）：` 把表格变成独立段落

**预防措施**：
- 编写或修改笔记时，表格前面不要有任何缩进
- 如果表格在逻辑上属于某个列表步骤，用文字过渡而非缩进嵌套

## [2026-08-08] 并行章节写作：后续章节读不到上一章文件

### 错误：并行派发 chapter-writer，第 3/4 章作者读取"上一章文件"时报文件不存在

**错误**：并行写 GHCR 笔记的 3 个章节时，第三章作者报告 `chapters/02_...` 不存在、第四章报告 `chapters/03_...` 不存在，只能按大纲写过渡语，章节边界衔接有失配风险。

**触发场景**：同一消息并行启动多个 chapter-writer，每个都要求先读"上一章文件"以保持衔接。

**根因**：章节间存在内容依赖（"上一章讲了 X"），并行写独立文件时读取依赖文件存在竞态——上一章文件此刻尚未生成。

**修复**：
- P5 note-assembler 通读全部章节后核对并修正了边界过渡（本次未产生错误衔接）
- 对确实失配的过渡语进行了统一

**预防措施**：
- 并行章节写作时，明确要求各章作者"过渡语自包含、按大纲写，不读取上一章文件"
- 或改为串行派发，保证每章都能读到已完成的上一章
- P5 组装阶段必须复核章节边界衔接

## [ERR-20260815-002] 教程更新：patch 路径修复一次改错

### 错误：`pnpm dsh web --patch` 修复时未核实文件位置，改完仍 ENOENT

**错误**：用户报在 `git-log-plugin/` 里跑 `pnpm dsh web --patch ./dev-cordis.patch.yml` 报 ENOENT（`/home/zhq/deepseek-harness/dev-cordis.patch.yml` 不存在）。我未核实 patch 文件真实位置，第一轮把笔记改成「patch 文件在仓库根、用 `./dev-cordis.patch.yml`」，用户从仓库根复跑仍 ENOENT。

**Logged**: 2026-08-15T23:21:14+0800
**Priority**: high
**Status**: pending
**Area**: docs

**触发场景**：更新教程命令章节，用户贴出首个报错，我直接改笔记而非先核实。

**根因**：凭 shell 直觉假设 `--patch` 路径相对 shell 当前目录解析；实际 `loadOverlayPatches` 把 overlay 路径当文件系统路径、相对 dsh 仓库根解析，且 patch 文件实际在 `git-log-plugin/`。没读源码、没确认文件实况就下笔。

**修复**：
- 用户纠正后改为：文件在 `git-log-plugin/`，仓库根执行 `pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml`。
- 全文统一该命令（标题、正文、表格、示例），并回滚第一轮错误表述（保留 §2.4 中作为「错误做法」对比示例的一处）。

**预防措施**：
- 命令/路径断言进入笔记前，先读命令实现源码确认路径解析基准，并确认被引用文件真实位置；一次改对。
- 涉及多处引用时，改完 `grep` 全文确认无残留旧表述。

## [ERR-20260816-001] P5 组装：note-assembler 无 Bash/Edit 且 Write 有输出上限，产物被拆分

### 错误：note-assembler 组装 135KB 长笔记时 Write 输出上限，产物被拆成 final_note.md + final_note_part2.md

**错误**：P5 组装时 note-assembler（工具集仅 Read/Write/Glob）写 `output/final_note.md` 触发 Write 输出上限，自行把内容拆到 `final_note_part2.md`，留下两个文件和一个 `.write-test.tmp` 测试文件。

**触发场景**：长章节（7 章）合并组装，总产物 >130KB。

**根因**：agent 工具约束（无 Bash/Edit、Write 输出 cap），子 agent 无法自行合并或追加。

**修复**：
- 父进程用 Bash `cat final_note_part2.md >> final_note.md` 合并。
- 删除 `final_note_part2.md` 与 `.write-test.tmp`。

**预防措施**：
- 组装前预判产物大小；长文档要求 writer 分章写入，由父进程/脚本合并。
- 派发 note-assembler 时提示「Write 有输出上限，超长拆文件后由父进程合并」。

---

## [ERR-20260816-002] P5 组装：合并文档脚注 ID 冲突，后定义覆盖先定义

### 错误：7 章合并后 19 个重复脚注 ID，引用错位

**错误**：合并后的 final_note.md 里 S2/S3/S5/S6/S7/S8/6.3 等脚注 ID 在多个章节重复，Markdown 语义下后定义覆盖先定义，导致前文引用指向错误来源。

**触发场景**：独立写作的章节各自从同一来源集编号，P5 拼接。

**根因**：无全局脚注命名空间约定。

**修复**：
- perl 脚本按章命名空间化：第 N 章全部 `[^ID]` → `[^cN-ID]`。
- 全文档核对 ref/def 配对：74 对，0 重复。

**预防措施**：
- 章节写作模板加「脚注用 `[^cN-...]` 前缀」约定，或在组装阶段固定加命名空间化步骤并 grep 校验。

---

## [ERR-20260816-003] 文本处理：perl 中文正则静默失败（no-op 无报错）

### 错误：perl 脚本按中文章节号拆分文档，执行后报告无变化，实为字符类未匹配

**错误**：第一次 perl 拆分脚本用 `-CSD` 但未 `use utf8`，`[一二三四五六七]` 字符类按字节匹配，匹配数为 0，脚本无任何报错地空跑。

**触发场景**：用 perl 处理含中文的 Markdown 文本拆分。

**根因**：perl 源码字面量默认按字节处理；中文字符类匹配不到 UTF-8 字节流；脚本逻辑在「匹配为 0」时输出无变化并成功退出。

**修复**：
- 脚本头部加 `use utf8;` 与 `use open ":std", ":encoding(UTF-8)"`。
- 文件句柄显式 `:encoding(UTF-8)`。
- 成功：8 段、74 defs、0 重复。

**预防措施**：
- perl 处理非 ASCII：必须 `use utf8` + 标准 IO/句柄 `:encoding(UTF-8)`；对含中文的脚本先跑小样本断言匹配数>0。

---

## [ERR-20260816-004] P4 并行写作：多个 chapter-writer 直接手改共享 workflow state file

### 错误：5 个并行 chapter-writer 各自直接编辑同一份 state file 的章节 checklist

**错误**：P4「直接写完」并行派发后，多个 writer 同时编辑 `workspace/workflow-runs/deepseek-harness-subagent.workflow.md`，章节完成状态乱序写入（1,2,3,5,6,7,4）。

**触发场景**：同一消息并行启动多个 chapter-writer，每个被告知完成后更新状态文件。

**根因**：状态变更规则（只能经 todo-state.sh）没有同步到子 agent 提示；并行写同一文件天然竞态。

**修复**：
- 本次各 writer 恰好都先读后写、保留了他人修改，无实际丢失。
- orchestrator 事后统一核对 7/7 完成状态。

**预防措施**：
- 子 agent 提示里明确「不修改 workflow state file；章节状态由 orchestrator 集中更新」。
- 并行写作时父进程收集各章完成回执，一次性用 todo-state.sh 更新状态。

## [ERR-20260816-005] P6 发布：135KB 单文件未按 RULES.md 主动拆分

### 错误：发布 135KB / 7 章单文件，违反「>30KB 或 >3 章主动建议拆分」规则，用户事后指出

**错误**：P6 note-beautifier 把 7 章合并后的 135KB 长文直接发布为单个 `DeepSeek-Harness Subagent 开发.md`，未按 RULES.md 既有规则主动建议拆分为独立章节文件 + 导航双链 + MOC 索引页。

**触发场景**：learning-note-flow P6 Obsidian 发布阶段，产物 135KB / 7 章。

**根因**：RULES.md 有规则但无执行检查点——P6 发布前没有「校验最终笔记体积/章节数并触发拆分」的强制步骤，beautifier 直接按单文件输出。

**修复**：
- 用户指出后按方案 A 拆分：`DeepSeek-Harness Subagent 教程/` 子目录 = README 首页 + 7 章独立文件。
- 每章补 frontmatter + 前后导航双链 + 返回首页链接；MOC 索引项改指向分册 README。
- 拆分后脚本校验：74 条脚注逐章配对、Callout 61+7、7 个章节 H1、全部 wikilink 可解析。

**预防措施**：
- P6 发布前必须检查最终产物大小与章节数：>30KB 或 >3 章，先拆分再发布（把 RULES.md Do 规则落成 beautifier 的硬检查点）。
- 拆分方案固定为「分册子目录 + README 首页 + 每章独立文件 + 前后导航 + MOC 指向 README」。

---
