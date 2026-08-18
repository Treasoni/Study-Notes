# 归档：2026-08-16 maintain-learnings 维护

> 由 maintain-learnings 于 2026-08-16 维护后归档。每条记录均已对应到可执行源头机制（SKILL.md / agent / workflow / 项目规则），经验证后从活跃文件移除。短铁律保留在 `.learnings/RULES.md`。

---

## LRN-20260815-001 教程章节结构「一章一节一文件」

**类别**：correction | docs | high
**摘要**：教程类笔记顶级小节只对应一个文件/产物；同一文件的多个字段只能是该文件小节下的 `####` 子节，不能升格为与文件平级的顶级小节。
**修复路径**：`.claude/agents/outline-generator.md` Step 3 新增规则 6「教程/实战笔记按「文件/产物」组织」——顶级章节对应一个文件/产物，同一文件字段收进该文件章节子节。
**验证方式**：outline-generator.md 工作树含规则 6 原文；skill/agent 前置依赖未被破坏。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## LRN-20260815-002 代码片段标注文件 + 先完整后分块

**类别**：best_practice | docs | high
**摘要**：教程每个代码块必须标明所属文件/目录（文件头注释），且先展示完整文件（先睹为快）再逐段拆讲，不让读者猜代码放哪。
**修复路径**：`.claude/agents/chapter-writer.md`「Code Examples (when applicable)」新增：代码块首行加文件路径注释（`// src/foo.ts`）；讲解多段前先完整展示一次再逐段拆讲。
**验证方式**：chapter-writer.md 工作树含该行原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## LRN-20260815-003 修复命令类错误先核实再改笔记

**类别**：correction | docs | high
**摘要**：用户报命令/路径错误时，先沿真实代码路径核实「路径相对哪里解析、文件实际在哪」，一次改对再写入笔记；改完全文 grep 确认无残留旧表述。
**修复路径**：`.claude/skills/note-updater/SKILL.md` Workflow step 4「局部更新」新增：涉及命令/路径断言的更新，先读命令实现源码或确认文件系统实况，核实路径解析基准与文件真实位置再改，一次改对；多处引用改动后 `grep` 确认无残留旧表述。
**验证方式**：note-updater/SKILL.md 工作树含该行原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## LRN-20260816-001 用户决策用紧凑文本菜单，不用多问题对话框

**类别**：best_practice | workflow | high
**摘要**：需要用户做方向/选项决策时，用带推荐默认值的紧凑文本菜单；不要用多问题 AskUserQuestion 对话框。
**修复路径**：`.claude/skills/research-planner/SKILL.md` 注意事项 3 改写为「用紧凑文本菜单 + 推荐默认值，不用多问题 AskUserQuestion 对话框（用户偏好低摩擦文本交互）」。
**验证方式**：research-planner/SKILL.md 工作树含该句原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## LRN-20260816-002 dsh 文档 canonical 源在 GitHub 仓库，github.io 镜像 404

**类别**：knowledge_gap | research | medium
**摘要**：GitHub 项目取文档优先 `raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}`；github.io Pages 镜像可能只发布部分页面（深层路径 404）。
**修复路径**：`.claude/skills/research-collector/SKILL.md` Source policy 新增 raw.githubusercontent 优先原则。
**验证方式**：research-collector/SKILL.md 工作树含该原则原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## LRN-20260816-003 独立章节合并必须按章命名空间化脚注 ID

**类别**：best_practice | docs | high
**摘要**：多篇独立写作章节合并成一个 Markdown 文档时，重复脚注 ID 会互相覆盖，必须统一加章节前缀 `[^cN-ID]`。
**修复路径**：`.claude/agents/chapter-writer.md` Source Citations 新增脚注前缀约定 `[^cN-ID]`；`.claude/agents/note-assembler.md` Step 4 新增 Footnotes 配对检查 + 质量清单「脚注 ID 全文档唯一，重复则命名空间化」；`.claude/workflows/learning-note-flow/workflow.md` P5 清单新增「脚注 ID 已命名空间化并 grep 校验无重复」。
**验证方式**：三个文件工作树均含对应行原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## [2026-06-01] OpenSpec 学习笔记 - Session Errors

**类别**：knowledge_gap | research
**摘要**：WebFetch 无法访问 github.com，需改用 GitHub API 替代方案获取项目信息。
**修复路径**：RULES.md Do「GitHub 项目类主题，先通过 API 获取基本信息再进 Phase 0 提问」（既有铁律）；learning 侧已于 2026-08-15 归档。
**验证方式**：该问题为非活跃工具限制，有既定替代方案，学习侧已归档，未再复发。
**处理结果**：已归档；RULES.md Do 保留。

---

## [2026-07-11] Codex 手动配置指南 - YAML frontmatter sources 引用失败

**类别**：correction | markdown | high
**摘要**：`sources` 字段中 `[来源: doc-XX]` 含特殊字符未正确引用，Obsidian 解析失败。
**修复路径**：`.claude/skills/note-beautifier/SKILL.md` Step 3.1 新增「frontmatter 引用校验」+ Step 4 表格/frontmatter 验证清单；`.claude/rules/obsidian/note-system.md` 规则 1 补 `sources` 特殊字符引用要求（跨 skill 铁律）。
**验证方式**：两个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Watch For 保留。

---

## [2026-07-31] 虚拟机教程表格嵌套列表不渲染

**类别**：correction | markdown | high
**摘要**：Obsidian 不支持在列表内渲染表格；带缩进的表格被视为列表项继续内容。
**修复路径**：`.claude/skills/note-beautifier/SKILL.md` Step 3.1「表格格式优化」新增「表格不得嵌套在列表项内」+ Step 4 表格/frontmatter 验证清单；`.claude/rules/obsidian/note-system.md` 新增规则 5「表格不得嵌套在列表项内（带缩进）」（跨 skill 铁律）。
**验证方式**：两个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Don't 保留。

---

## [2026-08-08] 并行章节写作：后续章节读不到上一章文件

**类别**：workflow | high
**摘要**：并行派发 chapter-writer 时，后续章节读取「上一章文件」存在竞态，文件尚未生成。
**修复路径**：`.claude/agents/chapter-writer.md` Step 1.4 新增「并行派发时不要读取上一章文件（存在竞态），过渡语按 `03_outline.md` 自包含撰写」+ Step 5 串行/并行衔接说明；`.claude/workflows/learning-note-flow/workflow.md` P4 清单新增「并行写作时各章过渡语自包含（按大纲），不读取上一章文件」。
**验证方式**：两个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Watch For 保留。

---

## ERR-20260815-002 教程更新：patch 路径修复一次改错

**类别**：correction | docs | high
**摘要**：`pnpm dsh web --patch` 修复时未核实文件位置与路径解析基准，改完仍 ENOENT。
**修复路径**：`.claude/skills/note-updater/SKILL.md` Workflow step 4 新增「先读命令实现源码或确认文件系统实况，核实路径解析基准与文件真实位置再改，一次改对；多处引用改动后 grep 确认无残留旧表述」。
**验证方式**：note-updater/SKILL.md 工作树含该行原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## ERR-20260816-001 P5 组装：note-assembler 无 Bash/Edit 且 Write 有输出上限

**类别**：workflow | high
**摘要**：note-assembler 组装 135KB 长笔记触发 Write 输出上限，自行拆成 final_note_part2.md 留垃圾文件。
**修复路径**：`.claude/agents/note-assembler.md` 错误处理「Large files」改写为「超过 Write 输出上限（~100KB）时 STOP 并报告父进程合并，不自行创建 part2/tmp 文件」+ 质量清单「预判输出大小」；`.claude/workflows/learning-note-flow/workflow.md` P5 清单新增「产物大小已预判；>100KB 由父进程拆分合并」。
**验证方式**：两个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Watch For 保留。

---

## ERR-20260816-002 P5 组装：合并文档脚注 ID 冲突

**类别**：correction | markdown | high
**摘要**：7 章合并后 19 个重复脚注 ID，后定义覆盖先定义，引用错位。
**修复路径**：`.claude/agents/chapter-writer.md` Source Citations 脚注前缀约定 + `.claude/agents/note-assembler.md` Footnotes 配对检查 + `.claude/workflows/learning-note-flow/workflow.md` P5 脚注命名空间化清单。
**验证方式**：三个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Do 保留。

---

## ERR-20260816-004 P4 并行写作：多个 chapter-writer 直接手改共享 workflow state file

**类别**：workflow | high
**摘要**：并行 writer 各自直接编辑同一份 state file 的章节 checklist，完成状态乱序写入。
**修复路径**：`.claude/agents/chapter-writer.md`「After Each Chapter Completion」改写为「Do NOT edit the workflow state file yourself…orchestrator 收集回执后集中经 todo-state.sh 更新」；`.claude/workflows/learning-note-flow/workflow.md` P4 清单新增「子 agent 未直接修改 workflow state file（章节状态由 orchestrator 集中更新）」。
**验证方式**：两个文件工作树均含对应规则原文。
**处理结果**：已修复归档；RULES.md Watch For 保留。

---

## ERR-20260816-005 P6 发布：135KB 单文件未按 RULES.md 主动拆分

**类别**：correction | workflow | high
**摘要**：P6 发布把 7 章 135KB 长文直接发布为单文件，未按规则主动拆分。
**修复路径**：`.claude/skills/note-beautifier/SKILL.md` Step 3.2 Vault 发布新增硬检查点「发布前先校验最终笔记体积与章节数：>30KB 或多于 3 章必须拆分后再发布（分册子目录 + README 首页 + 每章独立文件 + 前后导航双链 + MOC 指向 README）」。
**验证方式**：note-beautifier/SKILL.md 工作树含该检查点原文。
**处理结果**：已修复归档；RULES.md Do + Watch For 保留。

---

## 保留未归档（无源头机制，仍需观察）

- LRN-20260816-004：perl 处理含中文必须 `use utf8;` 三件套——已写入 RULES.md Do，但尚无 SKILL.md/脚本强制步骤，待源头机制落地后再归档。
- ERR-20260816-003：perl 中文正则静默失败——同 LRN-20260816-004 根因，保留活跃。
