---
curated:
  date: 2026-06-01
  topic: OpenSpec
  sources:
    - R01: README (Official)
    - R04: Commands Reference (Official)
    - R06: Concepts (Official)
    - R08: Installation Guide (Official)
    - R09: Supported Tools (Official)
    - R14: Initial Guide CN (Community)
  category: 核心概念
---

# OpenSpec 核心概念

## 1. 什么是 OpenSpec

OpenSpec 是一个开源的、AI 原生的**规范驱动开发（Spec-Driven Development, SDD）**框架。它在 AI 编程助手之上增加了一层轻量级规范层，确保人类和 AI 在编写任何代码之前就"要构建什么"达成一致。[来源: R01, R06, R14]

- **许可证:** MIT
- **npm 包:** `@fission-ai/openspec`
- **最新稳定版:** v1.3.1（截至 2026 年 6 月）
- **要求:** Node.js 20.19.0+
- **GitHub Stars:** 28k+ [来源: R01]

### 解决的问题

| 问题 | 描述 |
|------|------|
| 架构漂移 | AI 生成的代码偏离整体系统设计 |
| 上下文丢失 | 需求仅存在于聊天记录中，难以追踪 |
| 技术债务 | 缺乏规范导致代码质量不一致 |
| 频繁返工 | 误解导致反复修改 [来源: R14] |

---

## 2. 核心哲学

OpenSpec 建立在四个原则之上：[来源: R01, R06]

### 2.1 流动而非僵化 (Fluid not rigid)
传统规范系统将你锁定在各个阶段中。OpenSpec 更加灵活 —— 你可以按任何有意义的顺序创建工件。

### 2.2 迭代而非瀑布 (Iterative not waterfall)
需求会变化，理解会加深。OpenSpec 接受这一现实。

### 2.3 简单而非复杂 (Easy not complex)
某些规范框架需要大量设置。OpenSpec 保持轻量。数秒内完成初始化，立即开始工作。

### 2.4 棕地优先 (Brownfield-first)
大多数软件工作是在修改现有系统。OpenSpec 的基于增量的方法使得描述对现有行为的更改变得容易。

---

## 3. 项目结构

```
openspec/
├── specs/              # 真相源（系统当前行为）
│   └── <domain>/
│       └── spec.md
├── changes/            # 提出的修改
│   └── <change-name>/
│       ├── proposal.md   # 为什么做、做什么（意图、范围、方法）
│       ├── design.md     # 怎么做（技术方法、架构决策）
│       ├── tasks.md      # 实现检查清单
│       └── specs/        # 增量规范
│           └── <domain>/
│               └── spec.md
└── config.yaml         # 项目配置（可选）[来源: R01, R02, R06]
```

### 两个关键目录

- **`specs/`** — 真相源，描述当前系统行为，按领域组织（如 `specs/auth/`、`specs/payments/`）
- **`changes/`** — 每个提议的修改都有自己的文件夹，包含所有相关工件。完成后，该变更的增量规范会被合并到主 `specs/` 目录中 [来源: R02, R06]

---

## 4. 规范（Specs）

规范是描述系统行为的**行为契约**，不是实现计划。[来源: R06]

### 4.1 规范结构

按领域组织规范：

```
openspec/specs/
├── auth/           # 认证行为规范
├── payments/       # 支付处理规范
├── notifications/  # 通知系统规范
└── ui/             # UI 行为规范 [来源: R06]
```

### 4.2 规范格式

| 元素 | 用途 |
|------|------|
| `## Purpose` | 该规范领域的高级描述 |
| `### Requirement:` | 系统必须具有的特定行为 |
| `#### Scenario:` | 需求的具体示例 |
| SHALL/MUST/SHOULD | RFC 2119 关键词，表示需求强度 [来源: R06] |

### 4.3 规范的边界

**Good spec 的内容：** [来源: R06]
- 用户或下游系统依赖的可观察行为
- 输入、输出和错误条件
- 外部约束（安全性、隐私性、可靠性、兼容性）
- 可测试或可显式验证的场景

**避免在规范中出现的内容：**
- 内部类/函数名称
- 库或框架选择
- 逐步实现细节
- 详细的执行计划（这些属于 `design.md` 或 `tasks.md`）

### 4.4 渐进式严格度

- **轻量规范（默认）：** 简短的行为优先需求、清晰的范围内/范围外、一些具体的验收检查
- **完整规范（高风险时）：** 跨团队或跨仓库变更、API/契约变更、迁移、安全/隐私问题 [来源: R06]

---

## 5. 变更（Changes）

一个变更是对系统的提议修改，打包成一个文件夹，包含理解和实现它所需的一切。[来源: R06]

### 为什么变更是文件夹

1. **一切在一起。** 提案、设计、任务和规范都在一个地方
2. **并行工作。** 多个变更可以同时存在而不会冲突
3. **干净的历史。** 归档时，变更移到 `changes/archive/` 并保留完整上下文
4. **便于审查。** 一个变更文件夹很容易审查 [来源: R06]

### 增量规范（Delta Specs）

增量规范是 OpenSpec 用于棕地开发的核心创新，描述**什么在变化**而不是重述整个规范。[来源: R06]

**格式：**
```markdown
## ADDED Requirements    # 新需求
## MODIFIED Requirements # 变更的需求
## REMOVED Requirements  # 被删除的需求
```

**归档时的行为：**
| 部分 | 含义 | 归档操作 |
|------|------|----------|
| ADDED | 新需求 | 添加到主规范 |
| MODIFIED | 现有需求变更 | 替换主规范中的版本 |
| REMOVED | 被删除的需求 | 从主规范中删除 [来源: R02, R06] |

---

## 6. 工件（Artifacts）

工件是变更文件夹中的文档，指导工作。[来源: R06]

### 工件流程

```
proposal --> specs --> design --> tasks --> implement
  |           |          |          |
 why        what       how        steps
+scope     changes   approach    to take
```

| 工件 | 文件 | 用途 |
|------|------|------|
| Proposal | `proposal.md` | 意图、范围和方法 |
| Specs | `specs/` | 增量规范（ADDED/MODIFIED/REMOVED） |
| Design | `design.md` | 技术方法和架构决策 |
| Tasks | `tasks.md` | 实现检查清单 [来源: R02, R06] |

---

## 7. 斜杠命令（Slash Commands）

OpenSpec 通过斜杠命令驱动工作流，支持 25+ 种 AI 工具。[来源: R01, R04]

### 快速路径（core 配置文件）

| 命令 | 用途 |
|------|------|
| `/opsx:propose` | 创建变更并生成计划工件 |
| `/opsx:explore` | 提交前思考想法 |
| `/opsx:apply` | 实现任务 |
| `/opsx:sync` | 将增量规范合并到主规范 |
| `/opsx:archive` | 归档已完成的变更 [来源: R01, R04] |

### 扩展工作流命令

| 命令 | 用途 |
|------|------|
| `/opsx:new` | 启动新的变更脚手架 |
| `/opsx:continue` | 增量创建下一个工件 |
| `/opsx:ff` | 一次创建所有计划工件 |
| `/opsx:verify` | 验证实现是否匹配规范 |
| `/opsx:bulk-archive` | 一次归档多个变更 |
| `/opsx:onboard` | 引导式教程 [来源: R01, R04] |

---

## 8. 安装

### 前提条件
- Node.js >= 20.19.0
- npm、pnpm、yarn、bun 或 nix [来源: R08]

### 安装方法

```bash
# 推荐：全局安装
npm install -g @fission-ai/openspec@latest

# 或使用 npx（无需安装）
npx @fission-ai/openspec@latest init

# 项目内初始化
cd your-project
openspec init
```

初始化后，OpenSpec 会创建 `openspec/` 目录结构和特定工具的技能/命令文件。[来源: R08]

---

## 9. 支持的 AI 工具

OpenSpec 集成 29+ 种 AI 编程助手。[来源: R09]

### 主要支持工具

| 工具 | 支持级别 |
|------|----------|
| Claude Code | 完整适配 |
| Cursor | 完整适配 |
| Windsurf | 完整适配 |
| GitHub Copilot | 完整适配 |
| Gemini CLI | 完整适配 |
| Cline | 完整适配 |
| Continue | 完整适配 |
| Kimi CLI | 仅 Skills |

### 命令语法差异

| 工具 | 语法示例 |
|------|----------|
| Claude Code | `/opsx:propose` |
| Cursor | `/opsx-propose` |
| Kimi CLI | `/skill:openspec-propose` |
| Trae | `/openspec-propose` [来源: R04, R09] |

### 集成架构

1. **Skills 层** — 通用、跨编辑器的 `SKILL.md` 文件，任何兼容工具都可以发现
2. **Commands 层** — 针对每个助手原生格式的特定工具调用文件 [来源: R09]
