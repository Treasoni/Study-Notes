---
curated:
  date: 2026-06-01
  topic: OpenSpec
  sources:
    - R03: CLI Reference (Official)
    - R05: Workflows (Official)
    - R07: Customization (Official)
    - R10: Multi-Language Support (Official)
    - R11: Release Notes (Official)
    - R13: SDD Guide TC (Community)
    - R16: SDD Comparison (Community)
  category: 进阶原理
---

# OpenSpec 进阶原理

## 1. OPSX 工作流引擎

OPSX（OpenSpec eXperience）工作流系统是 OpenSpec 的核心引擎，提供基于动作的规范驱动开发范式。[来源: R05]

### 1.1 哲学：动作而非阶段

从传统 OpenSpec 到 OPSX 的转变是从"阶段锁定"到"基于动作"的工作流。[来源: R05]

| 方面 | 旧版 (Legacy) | OPSX (1.0+) |
|------|---------------|-------------|
| **结构** | 线性：Proposal -> Apply -> Archive | 灵活：随时执行任何动作 |
| **指令** | 硬编码在 TypeScript 中 | 从 config.yaml 动态组装 |
| **灵活性** | 全有或全无的工件创建 | 通过 `/opsx:continue` 增量创建 |
| **定制化** | 固定结构 | Schema 驱动 (schema.yaml) [来源: R05] |

### 1.2 工件图与状态机

变更目录中的每个工件存在于三种状态之一：[来源: R05]

| 状态 | 含义 |
|------|------|
| BLOCKED | 依赖关系尚未满足 |
| READY | 所有依赖存在，可以创建工件 |
| DONE | 文件已存在于输出路径 |

**状态转换：**
```
[*] --> BLOCKED: Schema 中定义了工件
BLOCKED --> READY: 所有依赖都存在
READY --> DONE: 文件在 outputPath 创建
DONE --> READY: 文件被删除
DONE --> [*]: 变更已归档 [来源: R05]
```

`openspec status` 命令将此状态提供给 AI 代理，使其能够智能地建议下一步操作。

### 1.3 动态指令组装

OPSX 指令从三个层次组装：[来源: R05]

1. **Context（上下文）**：项目范围的背景信息（技术栈、约定），来自 `openspec/config.yaml`
2. **Rules（规则）**：特定工件的约束，例如"需求使用 SHALL/MUST"
3. **Template（模板）**：AI 必须填充的结构化 Markdown，从 schema 目录加载

这些指令使用 XML 标签格式化以分隔关注点：

```xml
<context>
技术栈：TypeScript, React, Node.js, PostgreSQL
...
</context>

<rules>
- 包含回滚计划
- 确定受影响的团队
</rules>

<template>
[Schema 的内置模板]
</template> [来源: R07]
```

---

## 2. 定制化系统

OpenSpec 提供三个层级的定制：[来源: R07]

| 层级 | 功能 | 适用场景 |
|------|------|----------|
| **项目配置** | 设置默认值、注入上下文/规则 | 大多数团队 |
| **自定义 Schema** | 定义自己的工作流工件 | 有独特流程的团队 |
| **全局覆盖** | 在所有项目间共享 schema | 高级用户 |

### 2.1 项目配置

`openspec/config.yaml` 是定制化 OpenSpec 的最简单方式：[来源: R07]

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

**工作原理：**
- **Context** 出现在**所有**工件中
- **Rules** **仅**出现在匹配的工件中 [来源: R07]

### 2.2 Schema 解析顺序

当 OpenSpec 需要 schema 时，按以下顺序检查：[来源: R07]

1. CLI 标志：`--schema <name>`
2. 变更元数据（变更文件夹中的 `.openspec.yaml`）
3. 项目配置（`openspec/config.yaml`）
4. 默认（`spec-driven`）

### 2.3 自定义 Schema

自定义 schema 位于项目的 `openspec/schemas/` 目录中，与代码一起进行版本控制。[来源: R07]

```
your-project/
├── openspec/
│   ├── config.yaml
│   ├── schemas/
│   │   └── my-workflow/
│   │       ├── schema.yaml
│   │       └── templates/
│   └── changes/
```

**创建方式：**
```bash
# Fork 现有 schema
openspec schema fork spec-driven my-workflow

# 从零创建
openspec schema init research-first
```

**Schema 结构示例：**

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
  tracks: tasks.md [来源: R07]
```

### 2.4 Schema 命令

```bash
# Fork 现有 schema
openspec schema fork spec-driven my-workflow

# 从零初始化
openspec schema init research-first

# 验证 schema
openspec schema validate my-workflow

# 调试 schema 解析
openspec schema which my-workflow

# 列出所有可用 schema
openspec schema which --all [来源: R03, R07]
```

### 2.5 社区 Schema

| Schema | 维护者 | 仓库 | 描述 |
|--------|--------|------|------|
| `superpowers-bridge` | @JiangWay | JiangWay/openspec-schemas | 将 OpenSpec 的工件治理与 obra/superpowers 执行技能集成 [来源: R07] |

---

## 3. 多语言支持

OpenSpec 支持生成非英语的计划工件，通过其**指令丰富管道（Instruction Enrichment Pipeline）**实现。[来源: R10]

### 3.1 工作原理

该功能利用 AI 的自然语言能力，通过将语言指令注入到提示中。当执行 `/opsx:continue` 或 `/opsx:propose` 等命令时，CLI 组装一个提示，将基础工件模板与项目级上下文和工件特定规则结合。[来源: R10]

### 3.2 配置示例（日语）

```yaml
# openspec/config.yaml
context: |
  Language Requirements:
  - All artifacts (proposals, specs, designs, tasks) MUST be written in Japanese.
  - Use "Desu/Masu" (polite) tone for proposals and designs.
  - Use "Da/Dearu" (plain/formal) tone for technical specifications.
  - Keep technical terms (e.g., "middleware", "endpoint", "payload") in English.
```

### 3.3 支持的语言

| 语言 | 上下文指令示例 |
|------|---------------|
| 西班牙语 | `Escribe todos los documentos en espanol.` |
| 法语 | `Redigez tous les documents en francais.` |
| 德语 | `Alle Dokumente mussen auf Deutsch verfasst sein.` |
| 简体中文 | `所有文档必须使用中文编写。` |
| 日语 | `All artifacts MUST be written in Japanese.` |
| 繁体中文 | `所有文件必須使用繁體中文編寫。` [来源: R10] |

### 3.4 验证输出

```bash
openspec instructions --change <change-id> --artifact proposal
```

此命令显示发送给 AI 的原始指令，确认语言上下文和规则正确注入。[来源: R10]

---

## 4. 命令行高级功能

### 4.1 Schema 命令

```bash
# Fork 现有 schema
openspec schema fork spec-driven my-workflow

# 从零创建（交互式）
openspec schema init research-first

# 从零创建（非交互式）
openspec schema init rapid \
  --description "Rapid iteration workflow" \
  --artifacts "proposal,tasks" \
  --default

# 验证 schema 结构
openspec schema validate my-workflow

# 调试 schema 解析
openspec schema which my-workflow
openspec schema which --all [来源: R03]
```

### 4.2 Workspace（工作区）命令（Beta）

支持跨仓库协作的机器本地协调视图：[来源: R03]

```bash
# 交互式设置
openspec workspace setup

# 非交互式设置
openspec workspace setup --no-interactive --name platform \
  --link /repos/api --link web=/repos/web

# 列出已知工作区
openspec workspace list

# 诊断
openspec workspace doctor

# 打开链接的工作集
openspec workspace open
openspec workspace open platform --agent github-copilot
openspec workspace open --initiative billing-launch --store platform
```

**工作区心智模型：**
```
workspace = 在上下文存储、倡议、仓库和文件夹之上的私有本地视图
context store = 持久化的共享上下文容器
initiative = context store 内的持久化协调上下文
link = 工作区可以本地解析的仓库或文件夹的稳定名称 [来源: R06]
```

**工作区目录结构：**
```
~/.local/share/openspec/workspaces/<workspace-name>/
├── workspace.yaml       # 私有本地视图记录
├── AGENTS.md            # 生成的运行时指南
└── <workspace-name>.code-workspace  # 生成的编辑器工作区文件 [来源: R06]
```

### 4.3 输出格式

CLI 命令支持 JSON 输出，便于脚本化：

```bash
openspec list --json
openspec status --json [来源: R03]
```

---

## 5. SDD 工具对比分析

### 5.1 OpenSpec vs SuperPowers

**来源:** cnblogs.com/kybs0（2026 年 3 月）[来源: R16]

| 方面 | OpenSpec | SuperPowers |
|------|----------|-------------|
| 方法 | 规范驱动的变更管理 | 多代理（控制器 + 实现者 + 审查者） |
| AI 模型 | 单代理 | 多代理编排 |
| 测试 | 手动验证 | 强制执行 TDD |
| Git 策略 | 标准 Git | git worktree |
| 优势 | 决策可追溯性、知识积累 | 审查自动化、TDD 强制执行 |

**结论：** 两者互补。使用 OpenSpec 进行规范管理，借用 SuperPowers 的审查和 TDD 模式。

### 5.2 OpenSpec vs Spec Kit (GitHub)

**来源:** wnote.com（2026 年）[来源: R16]

| 方面 | OpenSpec | Spec Kit |
|------|----------|----------|
| 重量 | 轻量 | 重量级 |
| 阶段门控 | 无（流动） | 严格的阶段门控 |
| 棕地支持 | 原生（增量规范） | 需要完全重写 |
| 生态系统 | 工具无关（30+ 工具） | 绑定到 GitHub |
| 成本 | 免费（MIT） | GitHub 生态系统部分 |
| 学习曲线 | 低 | 较高 |

### 5.3 OpenSpec vs Kiro (AWS)

| 方面 | OpenSpec | Kiro |
|------|----------|------|
| IDE 锁定 | 无 | 绑定到 Kiro IDE |
| 模型锁定 | 任何模型 | 有限的模型选择 |
| 棕地支持 | 原生 | 有限 |
| 成本 | 免费（MIT） | 与 AWS 绑定 [来源: R16] |

### 5.4 OpenSpec vs 无 SDD（"Vibe Coding"）

| 方面 | OpenSpec | 无 SDD |
|------|----------|--------|
| AI 行为 | 可预测、有范围 | 不可预测、漂移 |
| 跨会话上下文 | 持久化（specs/） | 在聊天历史中丢失 |
| 变更可追溯性 | 完整审计轨迹 | 不存在 |
| 返工频率 | 低 | 高 |
| 设置时间 | ~5 分钟 | 无 |
| 认知开销 | 中等（编写规范） | 初期低，后期高 [来源: R16] |

---

## 6. 版本演进

### v1.0.0（约 2025 年末）
首个稳定版本。核心工作流：proposal -> apply -> archive。支持 Claude Code、Cursor、Windsurf、GitHub Copilot。引入增量规范系统。[来源: R11]

### v1.2.0（2026 年 2 月）
引入 OPSX 工作流系统：
- 工件图和状态机（BLOCKED/READY/DONE）
- 动态指令组装
- 新命令：`/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:verify` 等
- 自定义 schema 和 schema forking
- 跨仓库协调工作区（Beta）
- 多语言支持
- 28k+ GitHub Stars [来源: R11]

### v1.3.0（约 2026 年 Q2）
新增工具集成：Junie、Lingma IDE、ForgeCode、IBM Bob。修复多个适配器问题。[来源: R11]

### v1.3.1（约 2026 年 5 月）
路径和遥测修复：规范路径解析、通配符工件输出、隐藏规范需求检测、`--json` 输出清理、防火墙网络中的静默遥测。[来源: R11]
