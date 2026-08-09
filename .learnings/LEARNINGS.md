# LEARNINGS.md

## [2026-07-31] Codex 配置笔记 — 笔记拆分策略

### 大笔记必须主动建议拆分

**类别**：best_practice
**优先级**：high
**状态**：pending
**范围**：note-beautifier / note-assembler / workflow

**摘要**：长篇笔记（>~30KB 或多章节）默认不应输出为单一 Monolithic 文件；应在组装或美化阶段主动向用户建议拆分方案。

**详情**：
- 事实：用户要求写 Codex 配置笔记，完整流程生成了 75KB / 1876 行的单文件笔记。用户反问"你不拆分吗？"
- 根因：工作流默认产出单一 final_note.md，note-beautifier 和 note-assembler 均未检测文件大小或多章节结构并提示拆分
- 下次做法：P5 组装后 / P6 美化前，检测笔记是否 > 30KB 或包含 3+ 章节；若是，主动给出拆分方案（独立章节 + 前后导航 + MOC 索引），让用户选择

---

## [2026-06-01] OpenSpec 学习笔记 - Session Learnings

### 流程方面
- Phase 0 需求发现：对于 GitHub 项目类主题，先快速了解项目基本信息再问问题，能提出更精准的需求问题
- 混合笔记类型 concept + cheat_sheet 适合"入门 + 速查"场景，实战示例部分用教学性场景更灵活
- Canvas 知识地图对项目类笔记很有价值，能直观展示概念关系

### 工具方面
- 对于 GitHub 项目无法用 WebFetch 时，可通过 GitHub API (`api.github.com/repos/...`) 获取项目信息
- opencli 提供丰富的搜索源（google/search, github 等），但 collector subagent 需要明确指定可用源
- beautify 阶段应主动询问用户是否需要 Canvas/Base 作为可选配置

### 内容方面
- OpenSpec 的核心是 Spec-Driven Development（SDD），与当前 Study System 的 phase-based workflow 有理念上的共鸣
- OpenSpec 对比线：vs Spec Kit（重但灵活度低）、vs Kiro（锁定生态）、vs 无规范（不可预测）

## [2026-07-11] Codex 手动配置指南 - Session Learnings

### 流程方面
- `practice + compare` 混合笔记类型在工具对比类主题中效果很好——每个领域同时提供实操步骤和对比表，特别适合有同类工具经验的读者
- Codex 相关资料分布在 `learn.chatgpt.com` 域名下（已从 `developers.openai.com` 迁移），收集时需注意域名变更

### 工具方面
- Codex 官方 hooks 文档缺失，需依赖社区资源（GitHub 仓库），这个缺口应在前置搜索策略中就考虑进去

### 内容方面
- Codex 与 Claude Code 的核心差异：TOML vs JSON 配置格式、AGENTS.md vs CLAUDE.md、不支持自定义 slash 命令、内置 OS 级 sandbox
- Codex 的 Skills 与 Claude Code 格式兼容（Agent Skills 开放标准），这是迁移的重要优势

## [2026-07-31] 虚拟机教程修表 - Session Learnings

### Obsidian 兼容性

**类别**：knowledge_gap
**优先级**：medium
**状态**：pending
**范围**：Obsidian 笔记编写

**摘要**：Obsidian 的 Markdown 解析器不支持在编号/项目列表内渲染表格，嵌套在列表中的表格会显示异常（变成纯文本或错乱）。

**详情**：
- 事实：[[虚拟机/VMware Workstation Player 安装 Windows 虚拟机.md]] 中步骤 3 后面的表格因有 3 空格缩进被解析为列表嵌套，预览模式不渲染为表格
- 根因：CommonMark / Obsidian 规范中列表项内的内容如果有缩进会被视为列表项的延续，而表格语法在列表项内不被识别
- 下次做法：所有表格必须放在列表之外（无缩进），列表项中需要引用表格时用"见下方表格"过渡

---

## [2026-08-08] GHCR 推送镜像权限配置 - Session Learnings

### 用户偏好：笔记默认加"大白话"通俗解释

**类别**：best_practice
**优先级**：high
**状态**：pending
**范围**：note-beautifier / chapter-writer / workflow

**摘要**：用户明确要求"以后生成笔记都这样"——学习笔记为每个核心概念添加 `[!tip] 大白话` Callout + 打比方类比，正文技术讲解保留。

**详情**：
- 事实：GHCR 笔记（4 章 / 51KB）技术性较强，用户问"这些概念可不可以写的通俗易懂一点？"，随后要求"以后生成笔记都这样"
- 根因：默认输出面向"有了解"读者，缺少面向普通读者的通俗解释层
- 下次做法：写作每章时为核心概念预留 `[!tip] 大白话` 通俗解释（可用类比：临时工牌 / 授权清单 / 门禁卡 / 保险箱 / 双保险 / 装修死结）

---

### GitHub Packages 认证只支持 Classic PAT

**类别**：knowledge_gap
**优先级**：high
**状态**：pending
**范围**：research-collector / 内容领域

**摘要**：GitHub Packages（含 GHCR）只支持 Classic PAT 认证（`write:packages` 等 scope）；Fine-grained PAT 没有 packages 权限项，无法用于推镜像。

**详情**：
- 事实：用户原指南用 Fine-grained PAT + "Packages: Read and Write"；P1 探测一度误判"2026 已支持"，P2 深读 + 直接核实官方文档后确认仅 Classic PAT 可用
- 根因：Fine-grained PAT 于 2025-03-18 GA，当时明确 Packages/Checks API 为缺口；截至 2026-08 仍未落地（roadmap#558）；部分旧资料/教程误导
- 依据：官方文档原句 "GitHub Packages only supports authentication using a personal access token (classic)"；docker/login-action#331 实证（全权限 fine-grained 仍报 scope 不匹配）；github/docs#33900
- 下次做法：涉及 GitHub 能力支持问题，先查官方文档原句 + 可复现 Issue；多信源冲突时以官方文档和实测为准

---

### 并行章节写作的衔接竞态 + 状态机确认顺序

**类别**：workflow
**优先级**：medium
**状态**：pending
**范围**：chapter-writer / note-assembler / todo-state.sh

**摘要**：并行派发 chapter-writer 时，后续章节读不到"上一章文件"（竞态）；todo-state.sh 完成阶段前必须先记录用户确认。

**详情**：
- 事实：并行写 3 章，第 3/4 章作者报"上一章文件不存在"，只能按大纲写过渡；另一次直接 `complete P4` 被 todo-state.sh 拒绝（需先 confirm）
- 根因：章节间有内容依赖（"上一章讲了 X"），并行时读取依赖文件存在竞态；状态机强制"已记录用户确认才可完成"
- 下次做法：① 并行章节写作时明确要求各章过渡语自包含、不依赖读取上一章文件（或改为串行）；② 用户整体授权时先 `todo-state.sh confirm PN "…"` 再 `complete PN`

---
