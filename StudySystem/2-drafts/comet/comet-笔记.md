---
type: concept + practice
topic: "Comet — OpenSpec + Superpowers 双星开发工作流"
difficulty: intermediate
tags: [comet, openspec, superpowers, sdd, ai-development-workflow]
created: 2026-06-01
updated: 2026-06-01
sources:
  - "Comet GitHub README"
  - "Comet GitHub README (中文)"
  - "腾讯云：OpenSpec + Superpowers 实战指南"
  - "SDD Tools Comparison (spec-coding.dev)"
concepts: [双星架构, 五阶段流水线, 状态机, Spec驱动开发, TDD, 子代理驱动开发]
---

# Comet: OpenSpec + Superpowers 双星开发工作流

## 核心概念

### 一句话解释

Comet 是一个将 **OpenSpec**（规格管理）和 **Superpowers**（TDD 执行）串联为五阶段自动化流水线的 AI 开发工作流工具——从创意到归档，一条命令搞定。 [来源: 1][来源: 2]

### 为什么存在？（解决什么问题）

在没有 Comet 之前，同时使用 OpenSpec 和 Superpowers 的开发流程存在三个痛点：

1. **OpenSpec 擅长管理需求**，但它的提案和 Task 不够细致，缺少头脑风暴式的深度设计 [来源: 2]
2. **Superpowers 产出细致的 Spec 文档**，但这些文档没有状态化设计——做完需求后只在文档上打勾（甚至 Agent 还会忘记打勾），导致断点续传时 Agent 要重新读代码猜进度，浪费大量 Token [来源: 2]
3. **文档同步靠人工提醒**："记得更新 design doc""记得同步 spec""记得归档 change"，这些提示需要反复说 [来源: 2]

Comet 的核心思路是：**把两套工具的优点组合起来，再加一层自动化编排**。 [来源: 1][来源: 2]

### 双星架构

Comet 的核心设计叫做"双星架构"，由三层组成：

| 层级 | 工具 | 角色 | 职责 |
|------|------|------|------|
| **WHAT 层** | OpenSpec | 规格管理 | 大纲、提案、spec 生命周期、归档 |
| **HOW 层** | Superpowers | 工程执行 | 技术设计、规划、TDD 执行、收尾 |
| **编排层** | Comet | 流程编排 | 状态管理、阶段流转、文档同步、断点续传 |

用一句话区分：OpenSpec 决定"做什么"，Superpowers 决定"怎么做"，Comet 把它们串起来自动跑。 [来源: 1][来源: 2]

### 五阶段流水线

Comet 将开发流程组织为 5 个阶段：

```mermaid
graph LR
    A[Open<br/>开启变更] --> B[Design<br/>深度设计]
    B --> C[Build<br/>计划与构建]
    C --> D[Verify<br/>验证与收尾]
    D --> E[Archive<br/>归档变更]
```

每个阶段的详细职责：

| 阶段 | 命令 | 核心活动 |
|------|------|----------|
| **Open** | `/comet-open` | 执行 OpenSpec propose，生成 proposal/spec/design/tasks |
| **Design** | `/comet-design` | 触发 Superpowers brainstorming，产出 Design Doc 和 delta spec |
| **Build** | `/comet-build` | 制定计划并用 subagent 执行 TDD 开发 |
| **Verify** | `/comet-verify` | 验证实现符合设计，处理开发分支 |
| **Archive** | `/comet-archive` | 同步 delta spec 到主 spec，归档 change |

> **关键特性**：主入口 `/comet` 支持状态检测。关闭会话后回来只需再次 `/comet`，它会自动读取活跃 Spec，动态识别当前执行到哪个阶段，继续往下执行。 [来源: 1][来源: 2]

### 状态机机制

Comet 通过 `.comet.yaml` 文件实现状态化管理：

- 记录当前 phase、执行模式
- 记录验证结果和归档状态
- Agent 中断后可自动恢复，无需重新检查代码和文档

这与传统方案的本质区别：传统方案的 Spec 只是静态 Markdown，AI 每次重启都得从头理解上下文。Comet 的状态文件让 AI 知道"我上次做到哪了，接下来该做什么"。 [来源: 1][来源: 2]

### 守护条件（Guard Conditions）

Comet 不信任 Agent 口头说"完成了"，而是用脚本验证阶段退出条件：

| 脚本 | 职责 |
|------|------|
| `comet-guard.sh` | 检查任务是否全部完成 |
| `comet-yaml-validate.sh` | 验证 .comet.yaml 字段完整性 |
| `comet-state.sh` | 检查验证证据和归档条件是否满足 |

只有这些脚本全部通过，才允许推进到下一阶段。 [来源: 1][来源: 2]

### 关键要点

- **Comet ≠ OpenSpec + Superpowers 的简单叠加**，而是一层编排层，加上了状态管理和自动化文档同步 [来源: 1]
- **双星架构的核心分工**：OpenSpec 管 WHAT，Superpowers 管 HOW，Comet 管串联 [来源: 1][来源: 2]
- **断点续传**是核心价值点——关闭会话后回来只需 `/comet`，自动恢复 [来源: 2]
- **Guard 脚本**确保阶段退出的可靠性，不依赖 Agent 自觉 [来源: 1]
- Comet **跳过 OpenSpec 的 `/opsx:apply`**，用 Superpowers 的 TDD 执行替代 [来源: 4]

### 常见误区

- **误区：Comet 是 OpenSpec 或 Superpowers 的替代品** → 正解：Comet 是编排层，它依赖两者作为底层能力，不是替代关系 [来源: 4]
- **误区：Comet 只是一个 CLI 工具** → 正解：Comet 是 CLI + 技能（Skills）+ 状态机 + Guard 脚本的组合，核心是工作流编排 [来源: 1]
- **误区：用 Comet 就必须用全套 OpenSpec + Superpowers 功能** → 正解：Comet 只使用各自的最强能力（OpenSpec 的 propose/archive，Superpowers 的 TDD 执行），可以自由组合 [来源: 2]

### 与其他概念的关系

- [[Superpowers]] - Comet 的 HOW 层，负责技术设计、TDD 执行和代码审查 [来源: 7]
- `[待创建: OpenSpec]` - Comet 的 WHAT 层，负责规格定义和变更管理 [来源: 6]
- `[待创建: Spec-Driven Development]` - Comet 所属的更大范式：规范驱动开发 [来源: 3]
- `[待创建: Subagent-Driven Development]` - Superpowers 的核心执行模式，Comet Build 阶段使用 [来源: 4]

## 实战示例

### 目标

在实际项目中安装 Comet，走完一次完整的五阶段工作流，从创意到归档。

### 前置知识

- 了解 [[Superpowers]] 的基本概念（brainstorming → TDD 执行）
- 了解 `[待创建: OpenSpec]` 的基本工作流（propose → apply → archive）
- Node.js 20+ 环境
- Git 项目

### 环境准备

```bash
# 前置要求
node --version  # >= 20
npm --version   # 随 Node 安装
git --version

# 全局安装 Comet
npm install -g @rpamis/comet
```

### 步骤

#### 步骤 1：初始化 Comet

```bash
cd your-project
comet init
```

`comet init` 会交互式引导你完成：
1. 选择 AI 平台（自动检测已有配置）
2. 选择安装范围：项目级（当前目录）或全局（用户主目录）
3. 选择技能语言：English 或 中文
4. 安装 OpenSpec 技能
5. 安装 Superpowers 技能
6. 部署 Comet 技能到所选平台
7. 创建 `docs/superpowers/specs/` 和 `docs/superpowers/plans/` 工作目录

[来源: 1][来源: 2]

#### 步骤 2：开启变更（Open）

在 AI 编码会话中，输入 Comet 主入口：

```
/comet
```

Comet 检测到没有活跃 Spec，进入 Open 阶段，触发 OpenSpec 的 proposal 流程。你需要描述你的需求，例如"为项目添加用户认证功能"。

OpenSpec 会自动生成：
- `proposal.md` — 为什么要做、做什么
- `specs/` — 具体的需求规格（Given/When/Then 格式）
- `design.md` — 技术方案和架构决策
- `tasks.md` — 任务清单

[来源: 5]

#### 步骤 3：深度设计（Design）

Comet 自动进入 Design 阶段，触发 Superpowers 的 brainstorming，生成详细的 Design Doc。

此时你需要审查设计方案，确认没有问题后批准进入下一阶段。

#### 步骤 4：计划与构建（Build）

Comet 进入 Build 阶段，Superpowers 的 **SDD（Subagent-Driven Development）** 模式启动：

1. **Implementer（实现者）** — 按任务清单逐个实现，先写测试再写代码（TDD）
2. **Spec Compliance Reviewer（规格审查员）** — 逐行对比代码和规格是否一致
3. **Code Quality Reviewer（质量审查员）** — 规格通过后审查代码质量

执行循环遵循 TDD 铁律：**没有失败测试，就不写生产代码**。 [来源: 4]

#### 步骤 5：验证与收尾（Verify）

Comet 运行 Guard 脚本验证：
- 所有任务是否完成
- 状态字段是否正确
- 验证证据是否齐全

满足条件后才允许推进到归档。

#### 步骤 6：归档（Archive）

Comet 自动归档变更：
- 将 delta spec 同步到主 spec
- 标记 change 为已归档
- 更新 `.comet.yaml` 状态

### 完整流程示意

```bash
# 1. 安装
npm install -g @rpamis/comet
cd your-project && comet init

# 2. 在 AI 编码会话中
/comet                    # 主入口，自动检测阶段
# Comet 会自动串联：
#   Open → Design → Build → Verify → Archive

# 或按阶段手动执行
/comet-open
/comet-design
/comet-build
/comet-verify
/comet-archive
```

### 踩坑记录

> [!warning] 坑点 1：环境要求
> **现象**：`comet init` 失败或脚本执行异常
> **原因**：缺少 Node.js 20+、npm 或 Git
> **解决**：确保前置要求齐全。Windows 用户需使用 Git Bash 或等价的 bash 环境。

> [!warning] 坑点 2：断点续传
> **现象**：重新打开会话后，Agent 不知道做到哪了
> **原因**：旧的工作流没有状态持久化
> **解决**：用 Comet 后只需 `/comet`，它会自动读取 `.comet.yaml` 恢复进度。

## 常见模式

### 模式 1：Comet 作为技能组合参考

Comet 项目本身是一个很好的参考案例，展示了如何：
- **稳定触发嵌套 Skill**：不是让 Agent 靠文档描述做"看起来像 Skill 触发"的操作，而是真正触发（CC 上显示 Skill 触发的打印） [来源: 2]
- **让组合 Skill 自动流转**：5 阶段流程除必要用户选择外，核心流程自动触发 [来源: 2]
- **Shell 脚本作为工作流基础设施**：Guard 脚本兼容 macOS/Linux/Windows Git Bash [来源: 1]

### 模式 2：自由组合 Skill

Comet 展示了 AI 开发工具链的**组合哲学**：
- 用 OpenSpec 的 Spec 管理能力（提案 + 归档）
- 用 Superpowers 的 TDD 驱动编码
- 跳过不需要的部分（如 OpenSpec 的 apply）

这种"取各工具最强项"的思路可以推广到其他 AI 开发工具的组合使用中。 [来源: 2]

### 模式 3：状态化工作流设计

将文档从"静态记录"变为"状态驱动"：
- 传统方式：Spec 写完后就是死的，状态只在人脑中
- Comet 方式：`.comet.yaml` 跟踪阶段、进度、验证状态，AI 可读可写

这是让 AI 能自主推进长任务的关键模式。 [来源: 1][来源: 2]

## 思考题

1. **概念理解**：Comet 为什么选择跳过 OpenSpec 的 `/opsx:apply`，改用 Superpowers 的 TDD 执行？这两种实现方式的核心区别是什么？

2. **应用场景**：在你的实际项目中，哪些类型的开发任务最适合用 Comet 的五阶段工作流？哪些类型不适合（如修一个简单 typo）？

3. **边界情况**：如果 Comet 的 Guard 脚本检测到某个阶段的退出条件不满足，应该怎么做？设计一个合理的降级策略。

4. **架构对比**：Comet 的"双星架构"和传统的 CI/CD 流水线（如 GitHub Actions）有什么本质区别？两者可以如何互补？

5. **扩展思考**：Comet 的模式（编排层 + 状态机 + Guard 脚本）能否推广到非 AI 开发场景？例如项目管理、文档协作等？
