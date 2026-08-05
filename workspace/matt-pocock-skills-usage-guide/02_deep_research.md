# 如何使用 Matt Pocock Skills - 深度研究素材（P2）

> 收集时间: 2026-08-01
> 项目源: https://github.com/mattpocock/skills（官方 README + plugin.json v1.2.0 + 原始 SKILL.md + 官方 Claude Code 插件文档 + 社区评测）
> 学习目标: 写一篇「如何使用 Matt Pocock Skills」的实操使用指南（安装、触发、配置、工作流、排错）

---

## 第一部分：安装与接入

### 1.1 两种互斥安装方式

| 方式 | 命令 | 特点 | 触发方式 |
|------|------|------|---------|
| **npx skills 安装器** | `npx skills@latest add mattpocock/skills` | 可编辑普通文件写入仓库 `.claude/`；`npx skills update` 拉更新 | `/skill-name` 斜杠命令 |
| **Claude Code Plugin** | `/plugin marketplace add <owner/repo>` + `/plugin install <名>@<市场>` | 只读、自动更新、命名空间触发 | `/插件名:skill名` |

> [!warning] 二选一，不要混用
> 两种机制会重复安装同类 skill。npx 路线是「可编辑副本」，Plugin 路线是「只读自动更新」。

### 1.2 npx skills 安装器步骤

1. `npx skills@latest add mattpocock/skills` — 安装，勾选 `/setup-matt-pocock-skills`
2. skill 写入仓库 `.claude/` 目录，以斜杠命令触发
3. 后续更新：`npx skills update`
4. 局限：CLI 只下载最新版，**无法回退旧版**（需手动定位旧版复制）

### 1.3 Claude Code Plugin 安装步骤（官方）

1. 官方市场通常自动添加；否则 `/plugin marketplace add anthropics/claude-plugins-official`
2. 安装：`/plugin install mattpocock-skills@<market>`（或 `/plugin install` 交互）
3. 生效：`/reload-plugins`
4. 作用域三选一：**User**（所有项目）/ **Project**（团队共享，写 `.claude/settings.json`）/ **Local**（仅本库本人）
5. 触发：skill 以插件名命名空间调用，如 `/commit-commands:commit`

> [!note] 团队市场
> 团队私有市场通过 `extraKnownMarketplaces` 写入 `.claude/settings.json` 分发。

### 1.4 安装后初始化（每次新仓库必做）

每个仓库运行一次 `/setup-matt-pocock-skills`：
- 探索仓库（issue tracker：GitHub/Linear/本地、标签、文档布局）
- 分段确认后把 `## Agent skills` 块写入 CLAUDE.md / AGENTS.md 及 `docs/agents/`
- 配置 to-tickets / triage / to-spec 依赖的 issue tracker 与标签

### 1.5 升级与版本管理

- npx 路线：`npx skills update`
- Plugin 路线：改仓库后推送，用户 `/plugin marketplace update <市场名>` 拉新
- 无法回退旧版本（Issue #274）

---

## 第二部分：完整 skill 清单与逐个用法

### 2.1 总览（plugin.json v1.2.0，共 22 个）

**Engineering（17 个）**：

| Skill | 触发 | 作用 |
|-------|------|------|
| ask-matt | user | 中央路由器，推荐最合适的 skill/flow |
| grill-with-docs | user | 有状态盘问，副产品产出 ADR + 词汇表 |
| triage | user | issue/PR 分类状态机，产出 agent-ready brief |
| to-spec | user | 把对话合成 PRD spec，发布到 issue tracker |
| to-tickets | user | 把 plan/spec 拆成纵向切片 tickets |
| implement | user | 基于 spec/tickets 实现，驱动 tdd → code-review → commit |
| setup-matt-pocock-skills | user | 初始化仓库配置（一次） |
| diagnosing-bugs | model | 建反馈回路诊断 bug |
| tdd | model | 红-绿-重构，一次一个纵向切片 |
| code-review | model | 双路并行子代理审查 diff |
| domain-modeling | model | 敲定术语，写 CONTEXT.md 词汇表 + ADR |
| prototype | model | 一次性原型回答单一设计问题（LOGIC/UI 分支） |
| improve-codebase-architecture | model | 霰弹式给出架构改进方案 |
| wayfinder | model | 拆 Decision ticket（决策而非构建） |
| research | model | 研究类工作 |
| codebase-design | model | 深模块词汇表（共享参考） |
| resolving-merge-conflicts | model | 解决合并冲突 |

**Productivity（5 个）**：

| Skill | 触发 | 作用 |
|-------|------|------|
| grill-me | user | 无状态盘问，委托 grilling |
| teach | user | workspace 内持续教师，维护学习状态 |
| writing-great-skills | user | skill 写作原则参考（纯参考） |
| grilling | model | 核心盘问原语（触发词 "grill me"） |
| handoff | model | 压缩会话为交接文档到系统临时目录 |

> [!warning] compact 技能
> 全仓库树扫描确认 `compact` **不存在**（已删除/更名）。「同会话继续」用内置 compact，跨会话用 `/handoff`。

### 2.2 核心 user-invoked skills 逐个用法

**`/setup-matt-pocock-skills`** — 首次使用 engineering skills 前运行一次
- 步骤：Explore → Present findings and ask → Confirm and edit → Write → Done
- 产出：CLAUDE.md/AGENTS.md 的 `## Agent skills` 块 + `docs/agents/`

**`/ask-matt`** — 路由器
- 用户不需要记住所有 skill，只记 `/ask-matt`
- 根据当前情境推荐最合适的 skill 或 flow

**`/grill-with-docs`** — 有状态盘问
- 委托 `/grilling` + `/domain-modeling`
- 副产品：CONTEXT.md 词汇表 + ADR

**`/grill-me`** — 无状态盘问（3 行）
- 委托 `/grilling`，跑完即止，不留痕迹

**`/to-spec`** — 合成 spec
- 步骤：Explore repo → Sketch seams → Write spec → Publish
- 模板：Problem / Solution / User Stories / Implementation / Testing / Out of Scope
- 发布到 issue tracker 并打 `ready-for-agent` 标签

**`/to-tickets`** — 拆 tickets
- 步骤：Gather context → Explore codebase → Draft vertical slices → Quiz the user → Publish
- 纵向切片（tracer bullet），每个声明阻塞边；quiz 用户确认后发布

**`/implement`** — 执行实现
- 内部驱动 `/tdd` → 完成后 `/code-review` → commit
- 是「手不是头」——思考已在 grilling + to-spec 完成

**`/triage`** — issue 分类
- 步骤：Show attention buckets → Triage specific item (Gather/Recommend/Verify/Grill/Apply) → Quick override → Resume

### 2.3 核心 model-invoked skills 逐个用法

**`/grilling`** — 盘问原语（触发词 "grill me"）
- 一次一问，带推荐答案；走决策树分支；事实查环境、决策问用户；达成共识才行动

**`/tdd`** — 测试驱动（触发词 "test-first"、"red-green-refactor"）
- Red before green、一次一个切片、重构不进循环
- 期望值须来自独立真值源避免循环论证

**`/code-review`** — 双路审查
- 步骤：Pin fixed point → Identify spec source → Identify standards sources → Spawn both sub-agents → Aggregate
- 一路对照编码标准、一路对照 issue/PRD，并排报告 `## Standards` / `## Spec`

**`/domain-modeling`** — 术语敲定
- 步骤：Challenge → Sharpen fuzzy language → Discuss scenarios → Cross-reference with code → Update CONTEXT.md → Offer ADRs

**`/prototype`** — 一次性原型
- 两分支：LOGIC.md（终端逻辑 app）或 UI.md（多 UI 变体）
- 规则：一条命令可跑、内存态、最少打磨、跑在 throwaway branch

**`/handoff`** — 交接文档
- 保存到系统临时目录（非工作区）；含 suggested skills；引用而非复制工件；脱敏
- 支持参数：描述下个会话焦点

### 2.4 触发方式速查

```
user-invoked（人类触发）: /setup-matt-pocock-skills, /ask-matt, /grill-with-docs,
  /grill-me, /to-spec, /to-tickets, /implement, /triage, /teach, /writing-great-skills
model-invoked（模型自动）: /grilling, /tdd, /code-review, /domain-modeling,
  /prototype, /diagnosing-bugs, /improve-codebase-architecture, /wayfinder,
  /research, /codebase-design, /resolving-merge-conflicts, /handoff
```

> [!note] 调用边界
> user-invoked → model-invoked → 共享参考，不可逆向。user-invoked 不能调用另一个 user-invoked。

---

## 第三部分：配置与定制

### 3.1 配置文件体系

| 文件 | 作用 | 用户需要改吗 |
|------|------|-------------|
| `CLAUDE.md` | 结构规则 + `## Agent skills` 块（setup 写入） | 由 `/setup-matt-pocock-skills` 管理 |
| `AGENTS.md` | Codex 跨平台契约，与 CLAUDE.md 一致 | 同上 |
| `CONTEXT.md` | 项目术语词汇表 | 由 `/domain-modeling`、`/grill-with-docs` 更新 |
| `.agents/adr/` | 架构决策记录 | 有决策时由 domain-modeling 写 |

### 3.2 调用模型（.agents/invocation.md）

- **User-invoked**: `disable-model-invocation: true` + `policy.allow_implicit_invocation: false`，description 面向人类（一行摘要，无触发词）
- **Model-invoked**: 默认，description 面向模型、含 "Use when..." 触发短语
- 依赖通过 `/skill` 散文式引用表达，非深度交叉引用

### 3.3 自定义 skill 接入

- skill 是「指令集」，不是插件——不增强模型，只结构化对话
- 质量关卡：description 含触发词 / SKILL.md ≤100 行 / 无时间敏感信息 / 术语一致 / 含具体示例 / 引用仅一级深度
- 发布到 Plugin 需 `.claude-plugin/marketplace.json`（name、owner、plugins[]）

---

## 第四部分：工作流实战

### 4.1 ask-matt 主流程（idea → ship）

```
1. /grill-with-docs   盘问打磨（有状态，留 CONTEXT.md/ADR 痕迹）
2. 分支：需要原型？
   ├── 是 → /handoff → /prototype → /handoff 返回
   └── 否 → 继续
3. 分支：多会话构建？
   ├── 是 → /to-spec → /to-tickets → 每 ticket 一次 /implement（新会话）
   └── 否 → 同一上下文直接 /implement
4. /implement 内部: /tdd → /code-review → commit
```

### 4.2 上下文卫生（Context Hygiene）

- 步骤 1-3 在同一上下文窗口完成，不 compact 不清除直到 `/to-tickets`
- 每个 `/implement` 从新会话开始
- Smart Zone：约 12 万 token，超限用 `/handoff` 分叉后开新会话

### 4.3 社区最佳实践

- 只装 4 个核心 skill 即可覆盖大部分工作流（grill-with-docs、tdd、diagnose、code-review）
- 28 个一次全装太多；从核心开始逐步扩展

---

## 第五部分：常见问题与排错

### 5.1 安装与触发排错

| 现象 | 处理 |
|------|------|
| plugin "not found" | `/plugin marketplace update <市场名>` 再重装 |
| skill 不出现 | `rm -rf ~/.claude/plugins/cache` 后重启重装 |
| 两种方式 skill 重复 | 二选一，删除其中一种 |
| URL 型市场相对路径插件报 "path not found" | 改 Git 源规避 |

### 5.2 行为类问题

- **grill 话痨**：简单问题可能触发 10-100 个追问。规避：直接告诉 agent "我时间不够"，让它跳过高频提问；或把 grill 改 opt-in
- **模型差异大**：同一 skill 在不同模型表现不同（社区反馈 Opus 4.6 正常、4.7 表现差）
- **CONTEXT.md 漂移**：项目变化后需重跑 grill 更新词汇表

### 5.3 Skill vs Plugin 区别（高频混淆）

| | Skill | Plugin |
|--|-------|--------|
| 本质 | 单个能力模块（SKILL.md + 可选 reference/scripts） | 分发容器，打包 skills/commands/hooks/MCP |
| 范围 | 跨 Claude.ai / API / Code | 仅 Claude Code |
| 触发 | 按上下文自动触发 | 需安装、命名空间调用 |
| 适用 | 单人自用，流程/SOP | 团队 3 人以上统一分发/版本一致 |

> [!tip] 决策框架
> 流程/SOP 用 Skill；外部数据连接用 MCP；生命周期自动化用 Hook；团队统一分发才用 Plugin。

### 5.4 版本管理限制

- `npx skills` 只下载最新版，无法回退；需手动复制旧版自建
- Plugin 自动更新，团队版本由 marketplace 控制

---

## 素材索引

| 编号 | 内容 | 来源 |
|------|------|------|
| [U1] | 完整 skill 清单 | plugin.json v1.2.0（raw.githubusercontent.com） |
| [U2] | 各 SKILL.md 用法（ask-matt/implement/grill-with-docs/grilling/handoff/setup/to-spec/to-tickets/tdd/code-review/domain-modeling/triage/prototype/teach/writing-great-skills） | github.com/mattpocock/skills |
| [U3] | 安装插件官方文档 | https://code.claude.com/docs/en/discover-plugins |
| [U4] | 插件市场官方文档 | https://code.claude.com/docs/en/plugin-marketplaces |
| [U5] | 中文安装教程 | https://cloud.tencent.com.cn/developer/article/2697381 |
| [U6] | 社区实测 | https://dev.to/evan-dong/i-tried-the-claude-code-skills-repo-that-got-77k-stars-here-is-what-works-and-what-does-not-57a4 |
| [U7] | Issue #274 grill 话痨 + 版本回退 | https://github.com/mattpocock/skills/issues/274 |
| [U8] | Skills vs Plugins | https://github.com/johnlarkin1/claude-code-extensions/blob/main/claude-docs/skills-vs-plugins.md |
| [U9] | Skills vs MCP vs Plugins | https://www.morphllm.com/claude-code-skills-mcp-plugins |
| [复用] | 设计原理（writing-great-skills 理论） | workspace/matt-pocock-skills/02_deep_research.md |

---

## 待澄清/注意

- 部分 skill 的 user/model 触发标记来自 SKILL.md frontmatter 实测（可靠）；plugin.json 表格中个别标记可能不精确，写正文时以实测为准。
- `compact` 在仓库中不存在（已删除/更名），正文勿提 `/compact` 为独立 skill。
- 社区提到的 `caveman` 非官方 skill，正文谨慎引用。
