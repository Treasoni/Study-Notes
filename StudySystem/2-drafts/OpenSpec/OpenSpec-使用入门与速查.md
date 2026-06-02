---
type: hybrid
topic: OpenSpec
difficulty: beginner-intermediate
tags:
  - openspec
  - sdd
  - ai-coding
  - spec-driven-development
  - fission-ai
  - claude-code
created: 2026-06-01
updated: 2026-06-01
sources:
  - R01: README (Official)
  - R02: Getting Started Guide (Official)
  - R03: CLI Reference (Official)
  - R04: Commands Reference (Official)
  - R05: Workflows (Official)
  - R06: Concepts (Official)
  - R07: Customization (Official)
  - R08: Installation Guide (Official)
  - R09: Supported Tools (Official)
  - R10: Multi-Language Support (Official)
  - R11: Release Notes (Official)
  - R12: Gigazine Kitchen Timer Walkthrough (Community)
  - R13: SDD Guide TC (Community)
  - R14: Initial Guide CN (Community)
  - R15: Reddit OpenSpec + Beads Experience (Community)
  - R16: SDD Comparison (Community)
concepts:
  - Spec-Driven Development (SDD)
  - Delta Specs
  - OPSX Workflow
  - Artifact State Machine
---

# OpenSpec 使用入门与速查

## 核心概念

### 什么是 Spec-Driven Development（SDD）？

想象一下这样的场景：你让 AI "给应用加个登录功能"，AI 直接就开始写代码。你发现它用了 Passport.js，但你其实想用 Auth0。于是你说 "换 Auth0"，AI 重写了一遍。运行起来发现 UI 样式不匹配，再改一轮。几次迭代后，代码里充满了补丁，最初的架构设计早已面目全非。

这就是典型的 **AI 编程混乱**——需求和实现纠缠在一起，每一次理解偏差都导致返工。

**SDD（规范驱动开发）** 的核心思想很简单：**先写规范，再写代码**。在 AI 动手之前，人类和 AI 先用一份清晰的规范达成共识——"我们要做什么"、"边界在哪里"、"验收条件是什么"。规范写好了，AI 再去实现，方向就不会跑偏。[来源: R01, R06, R14]

OpenSpec 是将 SDD 落地为实际工具的框架。它在 AI 编程助手之上增加了一层轻量级规范层，确保人类和 AI 在编写任何代码之前就"要构建什么"达成一致。[来源: R01, R06]

### 解决了什么问题？

| 问题 | 表现 | OpenSpec 的做法 |
|------|------|-----------------|
| **架构漂移** | AI 生成的代码偏离整体系统设计 | 规范作为"真相源"，所有修改都基于规范进行 |
| **上下文丢失** | 前一轮的需求只存在于聊天记录中 | 规范文件持久化存储在 `openspec/specs/` 中 |
| **技术债务** | 缺乏规范导致代码质量不一致 | 每次变更都有清晰的增量规范，可追溯 |
| **频繁返工** | 误解需求->改代码->再误解->再改 | 先在 proposal 阶段澄清，再动手实现 |

[来源: R14]

### 设计哲学

OpenSpec 的四个设计原则：[来源: R01, R06]

**1. 流动而非僵化 (Fluid not rigid)**
传统规范系统将你锁定在各个阶段中（必须先完成设计才能编码）。OpenSpec 允许你按任何有意义的顺序创建工件。你可以先写 proposal，也可以先写个草稿 design，边做边完善。

**2. 迭代而非瀑布 (Iterative not waterfall)**
需求会变化，理解会加深。OpenSpec 接受这一现实。规范的严格度可以渐进调整——小改动就用轻量规范，高风险变更再用完整规范。不需要一开始就把所有细节写死。[来源: R06]

**3. 简单而非复杂 (Easy not complex)**
不是所有规范框架都像 UML 或形式化方法那么重。OpenSpec 保持轻量：`npm install -g @fission-ai/openspec`，然后 `openspec init`，几秒钟就能开始工作。[来源: R08]

**4. 棕地优先 (Brownfield-first)**
大多数软件开发工作是修改现有系统（棕地），而不是从零开始（绿地）。OpenSpec 的**增量规范（Delta Specs）** 正是为此设计的——你只需要描述"什么在变化"，而不是重写整个系统规范。[来源: R06]

### 核心术语

| 术语 | 含义 | 类比 |
|------|------|------|
| **Spec（规范）** | 描述系统**当前**行为的契约，不是实现计划 | 产品的用户手册——它说"这个按钮做什么"，而不是"按钮的 onClick 怎么写" |
| **Change（变更）** | 对系统的一个提议修改，打包成一个独立文件夹 | 一个 PR 的"设计文档 + 实现计划"打包在一起 |
| **Delta Spec（增量规范）** | 只描述"相对于当前规范，什么发生了变化"，分为 ADDED / MODIFIED / REMOVED | 代码 diff，但针对的是行为规范而非代码 |
| **Artifact（工件）** | 变更文件夹中的文档——proposal、specs、design、tasks | 每个阶段的"交付物" |
| **Archive（归档）** | 变更完成后，将增量规范合并到主规范，并将变更文件夹移至 `archive/` 目录 | 合入 PR 后关闭分支 |
| **Workspace（工作区）** | 跨多个仓库的协调视图（Beta） | 在多个项目间建立"全局视野" |

[来源: R01, R02, R06]

### 与 Chat-based AI 开发相比

| 维度 | 普通聊天式 AI 开发 | OpenSpec SDD |
|------|---------------------|--------------|
| 需求定义 | 在聊天中自然语言描述，容易遗漏和模糊 | 通过 proposal 和 specs 结构化定义，清晰可审查 |
| 上下文持久化 | 仅存在于聊天窗口，关闭即丢失 | 保存在 `openspec/specs/` 文件中，跨会话可用 |
| 变更追溯 | PR commit message，粒度粗糙 | 每个变更文件夹完整记录"为什么做、怎么做、做了哪些任务" |
| 返工成本 | 低（随便改）但累计成本高（架构混乱） | 中（需要先更新规范再改代码），但累计成本低 |
| 学习曲线 | 零 | 低（约5分钟上手） |
| 适合场景 | 简单脚本、一次性任务 | 结构化功能开发、复杂变更、团队协作 |

[来源: R13, R16]

### 目录结构

初始化后，项目下会生成 `openspec/` 目录：

```
openspec/
├── specs/              # 真相源——系统当前行为，按领域组织
│   └── <domain>/
│       └── spec.md
├── changes/            # 所有提议的修改
│   └── <change-name>/
│       ├── proposal.md   # 为什么做、做什么（意图、范围、方法）
│       ├── design.md     # 怎么做（技术方法、架构决策）
│       ├── tasks.md      # 实现检查清单
│       └── specs/        # 增量规范
│           └── <domain>/
│               └── spec.md
└── config.yaml         # 项目配置（可选）
```

[来源: R01, R02, R06]

这里有两个关键目录：
- **`specs/`** —— 真相源。描述了系统当前应有的行为，按领域（auth、payments、ui 等）组织，是整个 SDD 流程的基础。
- **`changes/`** —— 每个变更都有自己的独立文件夹。完成后归档到 `changes/archive/`，同时其增量规范合并到主 `specs/` 中。[来源: R06]

---

## 快速开始

### 安装

前提条件：Node.js >= 20.19.0 [来源: R08]

```bash
# 推荐：全局安装
npm install -g @fission-ai/openspec@latest

# 或使用 npx（无需安装，运行一次即可）
npx @fission-ai/openspec@latest init

# 确认安装成功
openspec --version
```

### 初始化一个项目

进入你的项目目录，运行：

```bash
cd your-project
openspec init
```

初始化过程会：
1. 创建 `openspec/` 目录结构（`specs/` + `changes/` + `config.yaml`）
2. 检测你的 AI 编程工具（Cursor / Claude Code / Windsurf 等），自动生成对应的技能/命令文件
3. 引导式地创建第一个 `spec.md`（描述项目的"当前状态"）

[来源: R08]

> 如果你使用 npx 方式，记得在项目目录下运行 `npx @fission-ai/openspec@latest init`。

### 第一个工作流：添加深色模式

这是 OpenSpec 官方文档中最经典的入门示例。假设你有一个 Web 应用，想在项目中添加深色模式。[来源: R02]

#### 第一步：提议 (Propose)

在你的 AI 编程助手聊天框中输入：

```
/opsx:propose add-dark-mode
```

AI 会自动在 `openspec/changes/add-dark-mode/` 下生成四个工件：
- **proposal.md** —— 意图、范围和方法
- **specs/** —— 增量规范（ADDED / MODIFIED / REMOVED）
- **design.md** —— 技术方案
- **tasks.md** —— 实现检查清单

生成的 proposal.md 内容大致如下：[来源: R02]

```markdown
# Proposal: Add Dark Mode

## Intent
用户请求了一个深色模式选项以减少夜间使用时的眼睛疲劳。

## Scope
- 在设置中添加主题切换
- 支持系统偏好检测
- 在 localStorage 中持久化偏好

## Approach
使用 CSS 自定义属性进行主题化，配合 React Context 管理状态。
```

生成的 tasks.md 内容大致如下：[来源: R02]

```markdown
# Tasks

## 1. 主题基础设施
- [ ] 1.1 创建带 light/dark 状态的 ThemeContext
- [ ] 1.2 添加颜色的 CSS 自定义属性
- [ ] 1.3 实现 localStorage 持久化

## 2. UI 组件
- [ ] 2.1 创建 ThemeToggle 组件
- [ ] 2.2 将切换添加到设置页面
- [ ] 2.3 更新 Header 包含快速切换

## 3. 样式
- [ ] 3.1 定义深色主题配色方案
- [ ] 3.2 更新组件使用 CSS 变量
```

**审查建议：** 仔细阅读 proposal.md 和 design.md，确保 AI 的方案和你的想法一致。跳过这个验证步骤是常见的踩坑点。[来源: R15]

#### 第二步：实现 (Apply)

确认计划没问题后，告诉 AI：

```
/opsx:apply
```

AI 会按照 tasks.md 的清单，逐项实现代码。每完成一项就标记一个 `[x]`。

```
AI:  Working through tasks...
     ✓ 1.1 Created ThemeContext with light/dark state
     ✓ 1.2 Added CSS custom properties to globals.css
     ✓ 1.3 Implemented localStorage persistence
     ✓ 2.1 Created ThemeToggle component
     ...
     All tasks complete!
```

如果在实现过程中发现设计需要调整，直接告诉 AI 更新相关工件再继续即可。[来源: R02]

#### 第三步：归档 (Archive)

实现完成并测试通过后：

```
/opsx:archive
```

AI 会自动完成两件事：
1. 将 `changes/add-dark-mode/specs/` 中的增量规范**合并**到主 `specs/ui/spec.md` 中（ADDED 的需求被追加，MODIFIED 的替换原有内容）
2. 将 `changes/add-dark-mode/` 整个文件夹移动到 `changes/archive/2025-01-24-add-dark-mode/`

```
AI:  Archiving add-dark-mode...
     ✓ Merged specs into openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
     Done! Ready for the next feature.
```

至此，一个完整的 SDD 循环完成。[来源: R02]

---

## 命令速查表

### 斜杠命令（在 AI 工具聊天中使用）

所有 `/opsx:*` 命令都需要在 AI 编程助手的聊天界面中输入。

#### 核心流程命令

| 命令 | 用途 | 典型用法 |
|------|------|---------|
| `/opsx:propose` | 创建新的变更并生成所有计划工件（proposal + specs + design + tasks） | `/opsx:propose add-dark-mode` |
| `/opsx:explore` | 在提交正式 proposal 之前，探索和思考某个想法的可行性 | `/opsx:explore 我们是否需要迁移到微服务？` |
| `/opsx:apply` | 按 tasks.md 的清单逐项实现代码 | `/opsx:apply` |
| `/opsx:sync` | 将变更中的增量规范合并到主 spec 中（不归档） | `/opsx:sync` |
| `/opsx:archive` | 合并增量规范到主 spec，并将变更文件夹移入 archive/ | `/opsx:archive` |

[来源: R01, R04]

#### 扩展工作流命令

| 命令 | 用途 | 典型用法 |
|------|------|---------|
| `/opsx:new` | 启动一个新的变更（只创建文件夹脚手架，不生成内容） | `/opsx:new add-dark-mode` |
| `/opsx:continue` | 增量创建下一个工件（当你只想逐个生成而非一次生成全部时） | `/opsx:continue` |
| `/opsx:ff` | 一次创建所有计划工件（fast-forward，跳过中间步骤） | `/opsx:ff` |
| `/opsx:verify` | 验证已实现的代码是否与规范匹配 | `/opsx:verify` |
| `/opsx:bulk-archive` | 一次归档多个已完成变更（带冲突检测） | `/opsx:bulk-archive` |
| `/opsx:onboard` | 引导式教程，适合新手 | `/opsx:onboard` |

[来源: R01, R04]

### CLI 命令（在终端中使用）

| 命令 | 用途 | 示例 |
|------|------|------|
| `openspec init` | 初始化项目，创建 openspec/ 目录和对应的工具集成文件 | `openspec init` |
| `openspec list` | 列出所有活跃变更 | `openspec list` / `openspec list --json` |
| `openspec show <change>` | 查看某个变更的详细信息 | `openspec show add-dark-mode` |
| `openspec validate <change>` | 验证变更文件夹中的规范格式是否正确 | `openspec validate add-dark-mode` |
| `openspec status` | 显示当前变更的工件状态（BLOCKED / READY / DONE） | `openspec status` / `openspec status --json` |
| `openspec view` | 启动交互式仪表盘，浏览所有变更 | `openspec view` |
| `openspec config` | 显示或编辑项目配置 | `openspec config` |
| `openspec schema` | 管理自定义 Schema（子命令见下表） | `openspec schema fork spec-driven my-workflow` |
| `openspec workspace` | 管理跨仓库工作区（Beta） | `openspec workspace setup` |
| `openspec update` | 更新 OpenSpec CLI 到最新版本 | `openspec update` |
| `openspec version` | 显示版本信息 | `openspec --version` |

[来源: R03]

#### Schema 子命令

| 命令 | 用途 |
|------|------|
| `openspec schema fork <source> <name>` | 从已有 schema fork 一份新的 |
| `openspec schema init <name>` | 从零创建新的 schema（交互式） |
| `openspec schema validate <name>` | 验证 schema 结构 |
| `openspec schema which <name>` | 调试 schema 解析路径 |
| `openspec schema which --all` | 列出所有可用 schema |

[来源: R03, R07]

#### Workspace 子命令 (Beta)

| 命令 | 用途 |
|------|------|
| `openspec workspace setup` | 交互式设置工作区 |
| `openspec workspace list` | 列出已知工作区 |
| `openspec workspace doctor` | 诊断工作区问题 |
| `openspec workspace open` | 打开链接的工作集（可指定 agent） |

[来源: R03]

### 不同工具的命令语法差异

OpenSpec 在不同 AI 工具中的命令语法略有不同：[来源: R04, R09]

| 工具 | 语法示例 |
|------|----------|
| Claude Code | `/opsx:propose` |
| Cursor | `/opsx-propose` |
| Windsurf | `/opsx-propose` |
| GitHub Copilot | `/opsx-propose` |
| Gemini CLI | `/opsx:propose` |
| Cline | `/opsx:propose` |
| Kimi CLI | `/skill:openspec-propose` |
| Trae | `/openspec-propose` |

> **注意：** 如果看到 `/openspec-proposal` 这样的旧版语法，说明是旧版 OpenSpec。新版统一使用 `/opsx:` 前缀。示例中的厨房计时器教程 [来源: R12] 就是使用的旧版语法。

---

## 实战示例：从零到一运行 OpenSpec

这个示例用一个更具体的场景——**"给待办事项应用添加标签分类功能"**——来完整展示 OpenSpec 工作流。假设你有一个 React + TypeScript 的待办事项应用，初始规范已在 `openspec/specs/todos/spec.md` 中定义。

### 前提：初始化项目并建立初始规范

如果你的项目还没有规范，先用 `openspec init` 初始化，然后手动创建一个初始规范：

```bash
cd my-todo-app
openspec init
```

初始规范模板：

```markdown
<!-- openspec/specs/todos/spec.md -->
## Purpose
待办事项应用：用户可以创建、查看、完成和删除待办事项。

### Requirement: 创建待办事项
用户可以输入文本并创建一个新的待办事项。
- #### Scenario: 用户创建待办事项
  GIVEN 用户打开应用
  WHEN 用户在输入框中输入"买牛奶"并按下回车
  THEN 列表中应出现"买牛奶"的待办事项

### Requirement: 完成待办事项
用户可以将待办事项标记为已完成。
- #### Scenario: 用户完成待办事项
  GIVEN 列表中有"买牛奶"待办事项
  WHEN 用户点击该事项的复选框
  THEN 该事项显示为已完成状态
```

### 阶段一：提出变更

```bash
# 在 AI 工具（如 Claude Code）中输入：
/opsx:propose add-tag-support
```

AI 会生成以下变更文件夹：

```
openspec/changes/add-tag-support/
├── proposal.md       # 为什么、做什么
├── design.md         # 怎么做
├── tasks.md          # 具体任务
└── specs/
    └── todos/
        └── spec.md   # 增量规范
```

**proposal.md 示例内容：**

```markdown
# Proposal: Add Tag Support

## Intent
用户需要为待办事项添加标签分类功能，以便按标签筛选和整理任务。

## Scope
- 每个待办事项可以附加多个标签
- 用户可以通过标签筛选待办事项列表
- 标签以自由文本形式输入（非预设标签列表）
- 标签在待办事项旁以 badge 形式显示

## Out of Scope
- 标签管理界面（创建/编辑/删除标签）
- 标签颜色自定义

## Approach
在 Todo 类型中添加 tags 数组字段，筛选时匹配标签内容。
```

**增量规范 specs/todos/spec.md 示例内容：**

```markdown
## ADDED Requirements

### Requirement: 为待办事项添加标签
用户可以为一个待办事项添加一个或多个自由文本标签。
- #### Scenario: 添加标签
  GIVEN 用户正在创建待办事项
  WHEN 用户在标签输入框中输入"工作"并按回车
  THEN 该待办事项应包含标签"工作"

### Requirement: 按标签筛选待办事项
用户可以通过标签来筛选待办事项列表，只显示包含指定标签的事项。
- #### Scenario: 按标签筛选
  GIVEN 列表中有"买牛奶(标签: 生活)"和"写报告(标签: 工作)"
  WHEN 用户选择筛选标签"工作"
  THEN 列表只显示"写报告"
```

### 阶段二：审查并调整

**关键步骤——不要跳过审查！** [来源: R15]

阅读 proposal.md，检查范围和方法的合理性。比如 AI 可能建议用预设标签，但你想用自由标签。告诉 AI：

```
我看了一下 proposal.md，标签需要是自由文本形式，不要预设标签列表。
请更新 proposal.md 和 specs。
```

AI 会更新相关工件。直到你满意为止。

### 阶段三：实现

```
/opsx:apply
```

AI 会按 tasks.md 逐项实现。如果实现过程中发现设计需要调整：

```
等一下，标签的 CSS 样式需要调整，使用 outline 风格的 badge。
请先更新 design.md，再继续 apply。
```

### 阶段四：验证

```
/opsx:verify
```

AI 会检查代码实现是否与增量规范一致。如果发现问题，会列出差异，需要修正后再归档。

### 阶段五：归档

```
/opsx:archive
```

归档后：
1. `specs/todos/spec.md` 中会增加 ADDED 部分的内容
2. `changes/add-tag-support/` 整体移至 `changes/archive/` 下
3. 该变更的历史完整保留，可供后续查阅

### 验证归档

```bash
# 查看所有活跃变更（此时应为空）
openspec list

# 查看已归档变更
ls openspec/changes/archive/

# 验证主规范已更新
cat openspec/specs/todos/spec.md
```

---

## 进阶技巧

### 1. 自定义 Schema（三级定制）

OpenSpec 的定制系统分为三个层级，从简单到复杂：[来源: R07]

#### 第一级：项目配置（config.yaml）

最简单的定制方式。在 `openspec/config.yaml` 中设置上下文和规则：

```yaml
# openspec/config.yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js, PostgreSQL
  API style: RESTful, documented in docs/api.md
  Testing: Jest + React Testing Library
  我们重视所有公共 API 的后向兼容性

rules:
  proposal:
    - 包含回滚计划
    - 确定受影响的团队
  specs:
    - 使用 Given/When/Then 格式
    - 在发明新模式前引用现有模式
```

- **Context** 出现在**所有**工件的提示中
- **Rules** **仅**出现在匹配的工件提示中

#### 第二级：自定义 Schema

如果要定义完全不同的工作流，可以创建自定义 schema：[来源: R07]

```bash
# Fork 默认 schema 作为起点
openspec schema fork spec-driven my-workflow

# 或从零创建
openspec schema init research-first
```

Schema 文件结构：

```
your-project/
├── openspec/
│   ├── config.yaml
│   ├── schemas/
│   │   └── my-workflow/
│   │       ├── schema.yaml
│   │       └── templates/
│   │           ├── proposal.md
│   │           ├── design.md
│   │           └── tasks.md
│   └── changes/
```

Schema 定义示例：[来源: R07]

```yaml
# openspec/schemas/my-workflow/schema.yaml
name: my-workflow
version: 1
description: My team's custom workflow

artifacts:
  - id: proposal
    generates: proposal.md
    description: Initial proposal document
    template: proposal.md
    instruction: |
      Create a proposal that explains WHY this change is needed.
    requires: []

  - id: design
    generates: design.md
    description: Technical design
    template: design.md
    requires:
      - proposal

  - id: tasks
    generates: tasks.md
    description: Implementation checklist
    template: tasks.md
    requires:
      - design

apply:
  requires: [tasks]
  tracks: tasks.md
```

#### 第三级：全局覆盖

在 `~/.config/openspec/schemas/` 下放置 schema，所有项目可见。[来源: R07]

#### Schema 解析顺序

当 OpenSpec 需要决定使用哪个 schema 时，按以下优先级检查：[来源: R07]

1. CLI 标志：`--schema <name>`
2. 变更元数据（变更文件夹中的 `.openspec.yaml`）
3. 项目配置（`openspec/config.yaml` 中的 `schema:` 字段）
4. 默认值（`spec-driven`）

### 2. 多语言支持

OpenSpec 支持用非英语语言生成计划工件。原理是通过**指令丰富管道（Instruction Enrichment Pipeline）**将语言指令注入到 AI 提示中。[来源: R10]

配置示例（中文项目）：

```yaml
# openspec/config.yaml
context: |
  所有文档必须使用中文编写。
  技术术语（如 middleware、endpoint、payload）保留英文。
  Proposal 使用正式语气，tasks 使用简洁的命令式。
```

其他语言配置示例：[来源: R10]

| 语言 | 配置指令 |
|------|----------|
| 日语 | `All artifacts MUST be written in Japanese. Use "Desu/Masu" tone for proposals.` |
| 西班牙语 | `Escribe todos los documentos en espanol.` |
| 法语 | `Redigez tous les documents en francais.` |
| 繁体中文 | `所有文件必須使用繁體中文編寫。` |

验证指令是否生效：

```bash
openspec instructions --change <change-id> --artifact proposal
```

此命令会显示发送给 AI 的完整原始指令，可以确认语言上下文和规则是否正确注入。[来源: R10]

### 3. Workspace 模式（Beta）

适用于跨多个仓库的大型项目协作。Workspace 是一个**机器本地的协调视图**，将多个仓库链接在一起。[来源: R03, R06]

```
workspace = 在 context store、initiative、仓库和文件夹之上的私有本地视图
context store = 持久化的共享上下文容器
initiative = context store 内的持久化协调上下文
```

设置示例：

```bash
# 交互式设置
openspec workspace setup

# 非交互式设置
openspec workspace setup --no-interactive --name platform \
  --link /repos/api --link web=/repos/web

# 用特定 AI 工具打开
openspec workspace open platform --agent github-copilot

# 为某个 initiative 打开
openspec workspace open --initiative billing-launch --store platform
```

目录结构：

```
~/.local/share/openspec/workspaces/<workspace-name>/
├── workspace.yaml       # 私有本地视图记录
├── AGENTS.md            # 生成的运行时指南
└── <workspace-name>.code-workspace  # 生成的编辑器工作区文件
```

[来源: R06]

### 4. 工具特定命令格式

不同 AI 工具的命令语法不同。如果你是 Cursor 用户，记得用 `/opsx-propose` 而非 `/opsx:propose`。[来源: R04, R09]

另外，OpenSpec 通过两层架构支持多工具：
1. **Skills 层** —— 通用、跨编辑器的 `SKILL.md` 文件，任何兼容工具都可以发现
2. **Commands 层** —— 针对每个助手原生格式的特定工具调用文件 [来源: R09]

### 5. OPSX 工作流引擎详解

在 OpenSpec v1.0+ 中，核心引擎迁至 OPSX（OpenSpec eXperience），从"阶段锁定"变为"基于动作"的工作流。[来源: R05]

**状态机：** 变更目录中的每个工件存在于三种状态之一：

| 状态 | 含义 |
|------|------|
| BLOCKED | 依赖关系尚未满足（如 design 依赖 proposal） |
| READY | 所有依赖存在，可以创建工件 |
| DONE | 文件已存在于输出路径 |

**状态转换：**

```
[*] --> BLOCKED: Schema 中定义了工件
BLOCKED --> READY: 所有依赖都存在
READY --> DONE: 文件在 outputPath 创建
DONE --> READY: 文件被删除
DONE --> [*]: 变更已归档
```

[来源: R05]

`openspec status` 命令会显示此状态，AI 代理可以据此智能地建议下一步操作。

---

## 速查参考

### 变更文件夹结构

```
openspec/changes/<change-name>/
├── proposal.md           # 为什么做、做什么（意图、范围、方法）
├── design.md             # 怎么做（技术方法、架构决策）
├── tasks.md              # 实现检查清单
└── specs/                # 增量规范
    └── <domain>/
        └── spec.md       # 增量规范内容（ADDED/MODIFIED/REMOVED）
```

归档后，整个文件夹移至 `openspec/changes/archive/<timestamp>-<change-name>/`。增量规范合并到主 `specs/` 中相应领域下。[来源: R02, R06]

### 规范编写要点

**Good spec 包含：**[来源: R06]
- 用户或下游系统依赖的可观察行为
- 输入、输出和错误条件
- 外部约束（安全性、隐私性、可靠性、兼容性）
- 可测试或可显式验证的场景

**避免在 spec 中包含：**
- 内部类/函数名称
- 库或框架选择
- 逐步实现细节
- 详细的执行计划（这些属于 design.md 或 tasks.md）

### 常见配置文件

`openspec/config.yaml` 完整选项：

```yaml
# openspec/config.yaml
schema: spec-driven          # 使用的 schema 名称

context: |                   # 注入到所有工件的上下文
  Tech stack: TypeScript, React, Node.js, PostgreSQL

rules:                       # 特定工件的规则
  proposal:
    - 包含回滚计划
  specs:
    - 使用 Given/When/Then 格式

delivery: both               # 集成层：skills / commands / both
```

[来源: R05, R07]

### 支持的工具一览

OpenSpec 支持 29+ 种 AI 编程助手。以下是主要支持的工具：[来源: R09]

| 工具 | 命令语法 | 支持级别 |
|------|----------|----------|
| Claude Code | `/opsx:propose` | 完整适配 |
| Cursor | `/opsx-propose` | 完整适配 |
| Windsurf | `/opsx-propose` | 完整适配 |
| GitHub Copilot | `/opsx-propose` | 完整适配 |
| Gemini CLI | `/opsx:propose` | 完整适配 |
| Cline | `/opsx:propose` | 完整适配 |
| Continue | `/opsx:propose` | 完整适配 |
| Kimi CLI | `/skill:openspec-propose` | 仅 Skills |

### 最佳实践汇总

**规范编写：**[来源: R14]

| 正确的做法 | 错误的做法 |
|------------|------------|
| 关注"做什么"而非"怎么做" | 描述实现细节 |
| 使用 GIVEN-WHEN-THEN 场景 | 使用模糊的需求描述 |
| 确保可测试性 | 编写不可验证的需求 |
| 保持简洁，一次一个变更 | 一次做太多事情 |

**变更管理：**[来源: R14]
1. 保持每个变更作为一个逻辑单元
2. 使用清晰名称如 `add-dark-mode`，避免 `feature-1`
3. 及时归档已完成的变更，保持活跃变更列表整洁
4. 初始规范不需要完美；边进行边迭代

**团队协作：**[来源: R14]
- 将 `openspec/` 目录纳入版本控制，在仓库中共享
- 在实现前审查 proposal.md 和 design.md（和审查 PR 一样重要）
- 定期使用 `/opsx:sync` 保持规范同步

**可用性提示：**[来源: R12, R13]
- OpenSpec 最适合**结构化功能和修复**，不适合改一行 CSS 或修一个打字错误
- 可以只在需要保留历史记录的项目部分使用 OpenSpec，其他部分继续用常规方法
- **验证（verify）步骤不可跳过**——这是确保规范与实现一致的最后防线 [来源: R15]

---

## 学习检验

以下问题用于检查你对 OpenSpec 的理解。

**问题 1：** 规范（Spec）和设计文档（Design）的区别是什么？什么时候应该把内容放在 specs/ 而非 design.md 中？

<details>
<summary>查看提示</summary>
Spec 描述"系统应该做什么"——可观察的行为、输入输出、约束条件。Design 描述"怎么做"——技术方案、架构决策、库的选择。如果你写的是"用户点击按钮后显示提示"，那是 spec。如果你写的是"用 React 的 useState 管理弹窗状态"，那是 design。[来源: R06]
</details>

**问题 2：** 如果一个变更需要在实现中途修改设计方案，正确的 OpenSpec 流程是什么？

<details>
<summary>查看提示</summary>
应该先更新 design.md，再继续实现。OpenSpec 的工作流允许在任何时候更新工件——使用 `/opsx:continue` 可以增量地创建或更新下一个工件。不要跳过更新直接改代码。[来源: R02, R05]
</details>

**问题 3：** 什么时候应该使用 Delta Specs 的 ADDED / MODIFIED / REMOVED 标记？举一个 MODIFIED 的实际场景。

<details>
<summary>查看提示</summary>
- ADDED：全新的功能或行为，之前不存在
- MODIFIED：现有行为需要改变（例如"用户注册需要邮箱验证"从"可选"改为"必需"）
- REMOVED：行为被废弃或删除（例如"支持短信登录"下线了）
</details>

**问题 4：** OpenSpec 的"棕地优先"原则在实际工作流中是如何体现的？与"绿地优先"的框架相比，OpenSpec 的设计有什么不同？

<details>
<summary>查看提示</summary>
OpenSpec 的增量规范（Delta Specs）系统是其棕地优先设计的核心体现。传统框架在修改现有系统时通常需要重新定义整个规范或重写文档。OpenSpec 只要求描述"发生了什么变化"（ADDED / MODIFIED / REMOVED），不需要每次都重写完整规范。这使得对现有系统的渐进式修改成本大大降低。[来源: R06]
</details>

**问题 5：** 结合 OpenSpec 的四个设计哲学（Fluid / Iterative / Easy / Brownfield-first），思考：如果你的项目已经用开了 chat-based AI 开发半年，代码质量还不错，你有什么理由切换到 OpenSpec？又有什么理由不切换？

<details>
<summary>查看提示</summary>
切换的理由：如果项目规模在增长、需要多人协作、跨会话工作频繁、或者遇到了"AI 改了一个功能却破坏了另一个"的情况，OpenSpec 的规范持久化和变更追溯能力会很有价值。不切换的理由：如果项目是简单的个人脚本、一次性任务、或者你的工作流中几乎不需要跨会话的上下文维护，那么 OpenSpec 带来的规范维护成本可能超过收益。[来源: R13, R16]
</details>

---

> **笔记说明：** 本文档是 OpenSpec 的使用入门与速查笔记，综合了官方文档和社区资源编写而成。涉及 OpenSpec 内部架构、CI/CD 集成、大规模项目性能等话题，当前资料覆盖不足，标注为 [待补充]。如有新的研究发现，欢迎扩展相应章节。
