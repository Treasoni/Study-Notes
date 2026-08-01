# 学习笔记大纲：《如何使用 Matt Pocock Skills（Agent Skills 实操使用指南）》

> 笔记类型：实战笔记（实操使用指南）
> 预计总篇幅：约 1.5 万～1.8 万字
> 章节数：8 章 + 1 附录

---

## 第一章：快速上手 — 安装与初始化

> 覆盖要点：两条互斥安装路线怎么选、npx skills 与 Plugin 各自步骤、新仓库初始化
> 章素材：[U3][U4][U5][U7]

### 1.1 两条互斥安装路线怎么选

- 对比 npx skills 安装器（可编辑副本、写入仓库 `.claude/`、斜杠命令触发）与 Claude Code Plugin（只读自动更新、命名空间触发）
- 触发方式差异：`/skill-name` vs `/插件名:skill名`
- 二选一，不要混用的原因与后果

【篇幅】约 500 字
【素材】[U3][U4]
【示例】有（两条路线的触发命令对比）

### 1.2 npx skills 安装器逐步操作

- `npx skills@latest add mattpocock/skills` → 勾选 `/setup-matt-pocock-skills`
- 后续更新 `npx skills update`
- 局限：只能下载最新版，无法回退旧版

【篇幅】约 400 字
【素材】[U3][U5][U7]
【示例】有（安装 / 更新命令）

### 1.3 Claude Code Plugin 安装逐步操作

- 官方市场自动添加，否则 `/plugin marketplace add anthropics/claude-plugins-official`
- `/plugin install` + `/reload-plugins`
- 作用域三选一：User / Project（`.claude/settings.json`）/ Local
- 团队私有市场 `extraKnownMarketplaces` 分发

【篇幅】约 600 字
【素材】[U3][U4][U5]
【示例】有（插件系列命令）

### 1.4 新仓库初始化：/setup-matt-pocock-skills

- 每个新仓库运行一次的前提与产出（`## Agent skills` 块写入 CLAUDE.md / AGENTS.md + `docs/agents/`）
- Explore → Present → Confirm → Write 流程
- 配置 issue tracker 与标签（to-tickets / triage / to-spec 的硬依赖）

【篇幅】约 500 字
【素材】[U2][U5]
【示例】有（初始化命令）

---

## 第二章：完整 skill 清单与触发方式总览

> 覆盖要点：22 个 skill 全景、user-invoked / model-invoked 分组、调用边界
> 章素材：[U1][U2]

### 2.1 22 个 skill 全景总表

- Engineering（17 个）+ Productivity（5 个），逐个列出触发类型与一句话作用
- 说明以 plugin.json v1.2.0 为准，个别触发标记以 SKILL.md frontmatter 实测为准

【篇幅】约 800 字（含表格）
【素材】[U1][U2]
【示例】无

### 2.2 user-invoked vs model-invoked 分组

- 两组分别列出全部成员
- 触发差异：斜杠命令（人类显式调用）vs description 触发词（模型自动按上下文调用）

【篇幅】约 400 字
【素材】[U1][U2]
【示例】无

### 2.3 调用边界与依赖规则

- user-invoked → model-invoked → 共享参考，不可逆向
- user-invoked 不能调用另一个 user-invoked
- 依赖用 `/skill` 散文式引用表达，非深度交叉引用

【篇幅】约 400 字
【素材】[U2][复用]
【示例】无

---

## 第三章：user-invoked skills 逐个使用详解

> 覆盖要点：盘问类、规划类、执行类、治理辅助类的每个 skill 的触发与步骤
> 章素材：[U2][U6]

### 3.1 盘问类：/grill-with-docs 与 /grill-me

#### 3.1.1 /grill-with-docs 有状态盘问

- 委托 `/grilling` + `/domain-modeling`；副产品 CONTEXT.md 词汇表 + ADR
- 适用场景与执行流程

【篇幅】约 500 字
【素材】[U2][U6]
【示例】无

#### 3.1.2 /grill-me 无状态盘问

- 3 行薄封装，跑完即止、不留痕迹；与 grill-with-docs 的取舍

【篇幅】约 300 字
【素材】[U2]
【示例】无

### 3.2 规划类：/to-spec 与 /to-tickets

#### 3.2.1 /to-spec 合成 spec

- Explore repo → Sketch seams → Write spec → Publish
- 模板：Problem / Solution / User Stories / Implementation / Testing / Out of Scope
- 发布到 issue tracker 并打 `ready-for-agent` 标签

【篇幅】约 500 字
【素材】[U2]
【示例】有（spec 模板结构）

#### 3.2.2 /to-tickets 拆 tickets

- Gather context → Explore codebase → Draft vertical slices → Quiz the user → Publish
- 纵向切片（tracer bullet）与 quiz 确认机制

【篇幅】约 500 字
【素材】[U2]
【示例】无

### 3.3 执行类：/implement 与 /ask-matt

#### 3.3.1 /implement 实现

- 内部驱动 `/tdd` → 完成后 `/code-review` → commit
- "手不是头"的定位；从新会话开始执行

【篇幅】约 400 字
【素材】[U2]
【示例】无

#### 3.3.2 /ask-matt 中央路由器

- 只记一个命令，根据当前情境推荐最合适的 skill / flow

【篇幅】约 300 字
【素材】[U2]
【示例】无

### 3.4 治理与辅助类：/triage、/teach、/writing-great-skills

#### 3.4.1 /triage issue 分类

- Show attention buckets → Triage specific item（Gather/Recommend/Verify/Grill/Apply）→ Quick override → Resume

【篇幅】约 400 字
【素材】[U2]
【示例】无

#### 3.4.2 /teach 持续教师

- workspace 内维护学习状态，持续教学

【篇幅】约 250 字
【素材】[U2]
【示例】无

#### 3.4.3 /writing-great-skills 写作参考

- 纯参考 skill；引出质量关卡（description 触发词 / ≤100 行 / 术语一致 / 含示例 / 引用仅一级深度）

【篇幅】约 350 字
【素材】[U2][复用]
【示例】无

---

## 第四章：model-invoked skills 逐个使用详解

> 覆盖要点：核心工程原语、架构术语类、决策研究类、协作交接类
> 章素材：[U2][U6]

### 4.1 核心工程原语：/grilling、/tdd、/code-review、/diagnosing-bugs

#### 4.1.1 /grilling 盘问原语

- 触发词 "grill me"；一次一问带推荐答案；走决策树；事实查环境、决策问用户；达成共识才行动

【篇幅】约 400 字
【素材】[U2][U6]
【示例】无

#### 4.1.2 /tdd 测试驱动

- 触发词 "test-first"、"red-green-refactor"；Red before green、一次一个切片、重构不进循环
- 期望值须来自独立真值源，避免循环论证

【篇幅】约 350 字
【素材】[U2]
【示例】有（红绿重构步骤示例）

#### 4.1.3 /code-review 双路审查

- Pin fixed point → Identify spec source → Identify standards sources → Spawn 两个子代理 → Aggregate
- 并排 `## Standards` / `## Spec` 报告

【篇幅】约 400 字
【素材】[U2]
【示例】无

#### 4.1.4 /diagnosing-bugs

- 90% 工作在建反馈回路；诊断流程要点

【篇幅】约 300 字
【素材】[U2][U6]
【示例】无

### 4.2 架构与术语类：/domain-modeling、/codebase-design、/improve-codebase-architecture

#### 4.2.1 /domain-modeling 术语敲定

- Challenge → Sharpen fuzzy language → Discuss scenarios → Cross-reference with code → Update CONTEXT.md → Offer ADRs

【篇幅】约 400 字
【素材】[U2]
【示例】无

#### 4.2.2 /codebase-design 深模块词汇表

- Module / Interface / Depth / Seam / Adapter 五个术语与删除测试

【篇幅】约 350 字
【素材】[U2][复用]
【示例】无

#### 4.2.3 /improve-codebase-architecture

- 霰弹式给出架构改进方案；适用场景与边界

【篇幅】约 250 字
【素材】[U2]
【示例】无

### 4.3 决策与研究类：/wayfinder、/research

- wayfinder 拆 Decision ticket（决策而非构建）
- research 处理研究类工作

【篇幅】约 350 字
【素材】[U2]
【示例】无

### 4.4 协作与交接类：/prototype、/handoff、/resolving-merge-conflicts

#### 4.4.1 /prototype 一次性原型

- LOGIC.md（终端逻辑 app）与 UI.md（多 UI 变体）两分支
- 规则：一条命令可跑、内存态、最少打磨、跑在 throwaway branch

【篇幅】约 400 字
【素材】[U2]
【示例】有（LOGIC / UI 分支说明）

#### 4.4.2 /handoff 跨会话交接

- 保存到系统临时目录（非工作区）；含 suggested skills；引用而非复制工件；脱敏
- 与内置 compact 的分工说明（注意：仓库中已无 `/compact` 独立 skill，同会话继续用内置 compact，跨会话用 `/handoff`）

【篇幅】约 400 字
【素材】[U2][复用]
【示例】有（handoff 文档模板结构）

#### 4.4.3 /resolving-merge-conflicts

- 解决合并冲突的触发方式与使用要点

【篇幅】约 200 字
【素材】[U2]
【示例】无

---

## 第五章：配置与定制

> 覆盖要点：配置文件体系、调用模型 frontmatter、自定义 skill 接入
> 章素材：[U2][U4][U8][复用]

### 5.1 配置文件体系怎么改

- CLAUDE.md / AGENTS.md / CONTEXT.md / `.agents/adr/` 各自的职责与管理者
- 哪些文件由 `/setup-matt-pocock-skills`、`/domain-modeling`、`/grill-with-docs` 自动维护，哪些需要手动改

【篇幅】约 500 字
【素材】[U2][复用]
【示例】有（CLAUDE.md `## Agent skills` 块结构）

### 5.2 调用模型：user-invoked 与 model-invoked 的 frontmatter

- `disable-model-invocation: true` + `policy.allow_implicit_invocation: false` 的含义
- description 面向人类（一行摘要、无触发词）vs 面向模型（含 "Use when..." 触发短语）

【篇幅】约 400 字
【素材】[U2][复用]
【示例】有（SKILL.md frontmatter 示例）

### 5.3 自定义 skill 接入本框架

- SKILL.md 模板与 ≤100 行约束
- 质量关卡六项（trigger / 篇幅 / 无时间敏感 / 术语一致 / 具体示例 / 一级引用）
- 发布到 Plugin 需 `.claude-plugin/marketplace.json`（name、owner、plugins[]）

【篇幅】约 700 字
【素材】[U2][U4][U8][复用]
【示例】有（SKILL.md 模板 + marketplace.json）

---

## 第六章：工作流实战演练

> 覆盖要点：idea→ship 主流程、上下文卫生、原型绕行、社区最佳实践
> 章素材：[U2][U6][U7]

### 6.1 ask-matt 主流程：idea → ship 全演练

- `/grill-with-docs` → 原型分支 → 多会话分支 → `/implement`
- 单会话 vs 多会话的决策依据

【篇幅】约 800 字
【素材】[U2][U6]
【示例】有（完整流程命令序列）

### 6.2 上下文卫生（Context Hygiene）策略

- 步骤 1-3 在同一上下文窗口完成，不 compact 不清除直到 `/to-tickets`
- 每个 `/implement` 从新会话开始
- Smart Zone 约 12 万 token，超限用 `/handoff` 分叉

【篇幅】约 500 字
【素材】[U2][U6]
【示例】无

### 6.3 原型绕行与多会话构建演练

- `/handoff` 出去 → `/prototype` → `/handoff` 回来
- 每个 ticket 一个 `/implement`（新会话）的拆分方式

【篇幅】约 500 字
【素材】[U2]
【示例】有（会话分叉示例）

### 6.4 社区最佳实践：从 4 个核心 skill 起步

- grill-with-docs、tdd、diagnosing-bugs、code-review 即可覆盖大部分工作流
- 一次全装太多的问题与按需扩展策略

【篇幅】约 300 字
【素材】[U6]
【示例】无

---

## 第七章：常见问题与排错

> 覆盖要点：安装与触发排错、行为类问题、Skill vs Plugin vs MCP vs Hook、版本管理限制
> 章素材：[U5][U6][U7][U8][U9]

### 7.1 安装与触发排错

- plugin "not found" → `/plugin marketplace update <市场名>` 再重装
- skill 不出现 → `rm -rf ~/.claude/plugins/cache` 后重启重装
- 两种方式 skill 重复 → 二选一删除其中一种
- URL 型市场相对路径插件报 "path not found" → 改 Git 源规避

【篇幅】约 500 字
【素材】[U5][U7]
【示例】有（排错命令）

### 7.2 行为类问题

- grill 话痨（Issue #274）：简单问题可能触发 10-100 个追问；规避方法（声明时间不够 / 改 opt-in）
- 模型差异大（社区反馈 Opus 4.6 正常、4.7 表现差）
- CONTEXT.md 漂移 → 重跑 grill 更新词汇表
- 识别非官方 skill（如社区流传的 `caveman`），正文谨慎引用

【篇幅】约 500 字
【素材】[U6][U7]
【示例】无

### 7.3 Skill vs Plugin vs MCP vs Hook：怎么选

- Skill（流程/SOP）、Plugin（团队分发与版本一致）、MCP（外部数据连接）、Hook（生命周期自动化）
- 决策框架表与选型建议

【篇幅】约 500 字
【素材】[U8][U9]
【示例】无

### 7.4 版本管理限制

- `npx skills` 只下载最新版、无法回退；需手动复制旧版自建
- Plugin 自动更新，团队版本由 marketplace 控制

【篇幅】约 250 字
【素材】[U7]
【示例】无

---

## 第八章（可选）：把 skills 应用到自己的项目

> 覆盖要点：选型裁剪、编写自己的 skill、与本地框架集成
> 章素材：[U2][U4][U8][复用]

### 8.1 为自己的项目挑选与裁剪 skill

- 按工作流选型，从核心 skill 开始，避免全盘照搬

【篇幅】约 400 字
【素材】[U6][U8]
【示例】无

### 8.2 编写自己的第一个 skill 并接入

- 结合 5.3 的 SKILL.md 结构与 frontmatter
- 用 writing-great-skills 的质量关卡自查
- 分发方式：直接放仓库 `.claude/` / skills.sh / 发布 Plugin

【篇幅】约 500 字
【素材】[U2][复用]
【示例】有（自定义 skill 实例）

### 8.3 与本地/现有框架集成注意事项

- 双分发机制、AGENTS.md 跨平台契约（Codex）、与 Codex 同步的差异点

【篇幅】约 300 字
【素材】[U2][U4]
【示例】无

---

## 附录：命令速查卡

- 安装 / 更新 / 初始化 / 触发 / 排错命令清单
- 22 个 skill 的触发方式速查表
- 常用配置项速查

【篇幅】约 800 字
【素材】[U1][U2][U3]
【示例】有（全部命令）

---

## 学习路径说明

### 前置要求

- 已通读深度解析笔记《Matt Pocock Skills — Agent 框架设计深度解析》，理解设计原理（"为什么"）
- 已安装 Claude Code 并有基本使用经验
- 准备一个可练习的 Git 仓库（用于初始化与实战演练）

### 学完能做什么

- 独立用任一路线安装、更新、初始化 skills，理解两条路线的差异与互斥
- 熟练触发全部 22 个 skill，知道每个 skill 的适用场景与产出
- 按 idea → ship 主流程完成一次真实功能交付（含原型绕行与多会话构建）
- 配置 CLAUDE.md / CONTEXT.md / ADR，并能自定义 skill 接入自己的项目
- 排查常见安装、触发、行为类问题，并在 Skill / Plugin / MCP / Hook 间做正确选型

### 建议学习顺序

- 第 1-2 章（安装 + 总览）约 1 小时，搭好环境、建立全局地图
- 第 3-4 章（逐个 skill）建议随用随查，先读盘问类、规划类、实现类
- 第 5-6 章（配置 + 实战演练）边做边学，约 2-3 小时，完成一次端到端演练
- 第 7 章 排错与第 8 章 自建按需阅读；附录作为日常速查常备

---

> 结构说明：为平衡章节篇幅，将建议结构中的「第 3 章 逐个核心 skill 详解」拆为「第三章 user-invoked」与「第四章 model-invoked」两章，后续章节顺延，共 8 章 + 1 附录。`/compact` 已确认从仓库删除，仅在 4.4.2 handoff 处以更正说明形式出现，不设独立章节。
