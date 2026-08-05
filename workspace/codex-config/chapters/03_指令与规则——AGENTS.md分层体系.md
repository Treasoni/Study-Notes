---
title: 指令与规则 —— AGENTS.md 分层体系
tags: [codex, agents, rules, instructions, starlark, agenfs, claude-code]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# 指令与规则 —— AGENTS.md 分层体系

前两章我们分别建立了 Codex 配置体系的全局图景，并深入解读了 `config.toml` 的每个区块。但是，`config.toml` 控制的是"骨架"——安全策略、模型选择、功能开关。真正决定 Codex agent **如何理解你的项目、遵循什么工作规范、使用什么工作协议**的，是指令与规则系统。本章将深入 Codex 的指令文件 `AGENTS.md` 的分层级联机制——这是它与 Claude Code 的 `CLAUDE.md` 最核心的差异之一——以及独特的 `Starlark` 规则引擎。

## 1. AGENTS.md 是什么？

`AGENTS.md` 是 Codex 的指令文件，相当于 Claude Code 的 `CLAUDE.md`。它的作用是告诉 Codex agent：这个项目是什么、有什么规范、应该遵循什么工作方式。

但 Codex 在设计上做了一个关键的差异化选择：**`AGENTS.md` 不是单文件，而是一套分层级联的指令链**。这意味着，你可以为整个组织设定一套全局指令，为每个项目设定一套项目指令，甚至为项目中的不同子目录设定更细粒度的指令——所有指令最终会被拼接合并，形成一个完整的上下文。

> **Claude Code 对照**：Claude Code 的 `CLAUDE.md` 是单文件，放在项目根目录。虽然可以通过 `.claude/rules/` 目录添加额外规则，但这些规则是通过路径作用域（仅对匹配路径生效）加载的，而不是分层级联拼接。这是两种完全不同的设计哲学。

## 2. 发现机制与分层级联

AGENTS.md 的发现机制是 Codex 指令系统的核心设计。每次 Codex 启动一个新会话时，它会从头构建一个指令链。

### 2.1 发现路径

构建过程分为两个阶段：

```
阶段 1：全局层
  ~/.codex/AGENTS.override.md  ── 如果存在，优先使用
  ~/.codex/AGENTS.md            ── 否则使用此文件
  
阶段 2：项目层（从 Git 根目录向下遍历到当前目录）
  每级目录检查（按优先级从高到低）：
    1. AGENTS.override.md ── 如果存在，使用此文件
    2. AGENTS.md           ── 否则检查此文件
    3. 回退文件名          ── project_doc_fallback_filenames 中配置的文件，如 CLAUDE.md
```

整个过程可以想象成：

```text
~/.codex/AGENTS.md                          ← 全局指令（最基础）
.git/ 不存在，继续向上（或从仓库根开始）
/path/to/repo/AGENTS.md                    ← 仓库根指令
/path/to/repo/src/AGENTS.md                ← 子目录指令（如果存在）
/path/to/repo/src/components/AGENTS.md     ← 更深的子目录指令（如果存在）
```

### 2.2 合并规则：从根到叶拼接

找到所有指令文件后，Codex 按照**从根到叶**的顺序拼接：

1. **全局层**（`~/.codex/AGENTS.md`）最先加载
2. **项目根目录**的指令文件其次加载
3. **子目录逐级深入**，越靠近当前工作目录的指令文件越靠后加载

这种拼接方式产生了一个关键的覆盖效果：**越靠近当前目录的指令，在最终文档中的位置越靠后，因此在上下文中越晚出现，起到了"覆盖"的作用**。

```text
最终指令文档的内容顺序：
┌──────────────────────────────────┐
│  ~/.codex/AGENTS.md              │  ← 全局指令
│  /repo/AGENTS.md                 │  ← 项目根指令
│  /repo/src/AGENTS.md             │  ← 子目录指令
│  /repo/src/components/AGENTS.md  │  ← 当前目录指令（最后加载，优先覆盖）
└──────────────────────────────────┘
```

> **实战意义**：这种设计让你可以在全局层设定通用的行为准则（如"不允许删除文件"），在项目层设定项目规范（如"使用 TypeScript"），在特定子目录层设定更具体的规则（如"这个目录下的组件必须使用 React Hook Form"）。上层指令不会被下层覆盖消失——只是下层指令在合并后的文档中更靠后，对 agent 的影响更大。

### 2.3 文件优先级

在每个目录层级，Codex 按照以下优先级查找指令文件（取第一个非空的）：

| 优先级 | 文件名 | 说明 |
|--------|--------|------|
| 1（最高） | `AGENTS.override.md` | 强制覆盖级指令，用于需要绕过常规 AGENTS.md 的特殊场景 |
| 2 | `AGENTS.md` | 标准指令文件 |
| 3（回退） | `project_doc_fallback_filenames` 中的文件名 | 兼容其他工具的指令文件 |

### 2.4 发现流程的完整示例

假设你的项目结构如下：

```text
~/.codex/                             ← 全局配置目录
└── AGENTS.md                         ← 全局指令
    
~/code/my-project/                    ← Git 仓库根
├── AGENTS.md                         ← 仓库根指令
├── src/
│   ├── AGENTS.md                     ← src 目录指令
│   └── api/
│       └── AGENTS.override.md        ← api 目录覆盖指令
└── docs/
    └── README.md                     ← 没有 AGENTS.md，跳过
```

当你运行 `codex --cd ~/code/my-project/src/api` 时，最终的指令链是：

```text
1. ~/.codex/AGENTS.md                 ← 全局层
2. ~/code/my-project/AGENTS.md        ← 项目根层
3. ~/code/my-project/src/AGENTS.md    ← src 层
4. ~/code/my-project/src/api/AGENTS.override.md  ← api 层（用 override 版本）
```

而如果你运行 `codex --cd ~/code/my-project/docs`，指令链是：

```text
1. ~/.codex/AGENTS.md                 ← 全局层
2. ~/code/my-project/AGENTS.md        ← 项目根层
   （docs 目录没有 AGENTS.md，也没有 fallback 文件，所以停止）
```

## 3. 与 CLAUDE.md 的兼容：fallback 机制

对于从 Claude Code 迁移过来的用户，Codex 提供了兼容性机制：**通过 `project_doc_fallback_filenames` 配置，让 Codex 在找不到 `AGENTS.md` 时回退读取 `CLAUDE.md`**。

### 3.1 配置方式

```toml
# .codex/config.toml
project_doc_fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
```

这个配置告诉 Codex：在每个目录层级，如果找不到 `AGENTS.override.md` 或 `AGENTS.md`，就尝试这个列表中的文件名，取第一个非空文件。

### 3.2 工作流程

```text
每级目录的查找顺序：
         ┌─────────────┐
         │ AGENTS      │
         │ .override   │ ← 最高优先级
         │ .md         │
         └──────┬──────┘
                │ 不存在？
         ┌──────v──────┐
         │             │
         │ AGENTS.md   │ ← 标准指令
         └──────┬──────┘
                │ 不存在？
         ┌──────v──────┐
         │ fallback 列表 │ ← CLAUDE.md / TEAM_GUIDE.md
         │             │
         └─────────────┘
```

### 3.3 迁移场景

如果你有一个已有的 Claude Code 项目，只需要在 `.codex/config.toml` 中添加一行，就可以让 Codex 直接读取现有的 `CLAUDE.md`：

```toml
# .codex/config.toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

这样，Codex 在启动时会自动找到项目根目录的 `CLAUDE.md` 并加载它。你不需要立即重写为 `AGENTS.md` 格式，可以逐步过渡。

> **关键限制**：fallback 机制只在**当前目录没有 `AGENTS.md` 或 `AGENTS.override.md`** 时才会触发。如果你在某级目录下存在 `AGENTS.md`，该目录的 fallback 文件不会被读取。此外，回退文件名不支持动态目录名自动补全，需要显式列出。

### 3.4 与 Claude Code 的双向兼容性

值得注意的是，这种兼容是**单向**的：

| 方向 | 是否兼容 | 原因 |
|------|---------|------|
| Codex 读取 CLAUDE.md | 是（通过 fallback） | `project_doc_fallback_filenames` 配置 |
| Claude Code 读取 AGENTS.md | 否 | Claude Code 没有对应的 fallback 机制 |

这也意味着，如果你想在两个工具之间共享项目指令文件，最佳做法是**维护一份 `CLAUDE.md`**（因为 Claude Code 只认它），然后让 Codex 通过 fallback 读取它。或者，你也可以维护两份文件，让它们通过符号链接保持同步。

## 4. 容量限制与最佳实践

### 4.1 默认上限：32 KiB

Codex 对 AGENTS.md 链有硬性的容量限制：

- **默认上限**：**32 KiB**（`project_doc_max_bytes` 配置项控制）
- **超过上限**：超过的部分会被截断，不会加载
- **空文件跳过**：找到的指令文件如果是空文件，直接跳过，不会影响指令链

这意味着，如果你的分层指令链中所有 `AGENTS.md` 文件合起来超过 32 KiB，只有前 32 KiB 的内容会被加载到上下文中。

### 4.2 调整上限

```toml
# .codex/config.toml
project_doc_max_bytes = 65536  # 调整为 64 KiB
```

但需要注意：**AGENTS.md 的内容会占用模型的上下文窗口**。模型的总上下文窗口是有限的（通常是 128K 或 200K tokens），AGENTS.md 越大，留给对话和任务内容的 token 就越少。建议：

- 除非确实需要，否则不要大幅调高 `project_doc_max_bytes`
- 将通用性弱、引用频率低的内容拆分为独立文件，通过其他机制（如 skills）加载
- 核心指令保持精炼，将详细文档放到 `references/` 目录或外部文档中

### 4.3 分层策略的最佳实践

利用分层级联的特性，可以设计高效的指令分层策略：

```text
~/.codex/AGENTS.md           ← 全局指令：不超过 8 KiB
  ├── 通用行为规范（禁止删除、必须确认等）
  ├── 默认编码规范（如果有）
  └── 工具使用规则

<repo>/AGENTS.md             ← 项目指令：不超过 16 KiB
  ├── 项目描述和技术栈
  ├── 架构约定和命名规范
  ├── 测试要求
  └── 工作流程

<repo>/src/AGENTS.md         ← 模块指令：不超过 8 KiB
  ├── 模块特定规范
  └── 注意事项
```

总容量控制在 32 KiB 以内。这样的分层策略的好处是：

1. **全局指令**可以在所有项目中复用，不需要在每个项目中重复写
2. **项目指令**聚焦在项目独有规范，不混入通用内容
3. **模块指令**只处理最细粒度的特殊规则，保持极短
4. **修改任意一层**不会影响其他层级（除了该层以下）

### 4.4 容量对照：Codex vs Claude Code

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| 默认上限 | 32 KiB（`project_doc_max_bytes` 可调） | 无硬性上限，约 200-300 行推荐 |
| 超出处理 | 截断（静默，不报错） | 无特别处理（尽可能加载） |
| 空文件处理 | 跳过 | 加载空文件 |
| 上下文影响 | 占用模型上下文窗口 | 同样占用上下文 |
| 分层影响 | 多层文件容量累加 | 单文件，无分层累加 |

## 5. 特殊段落

`AGENTS.md` 支持两种具有特殊含义的段落，这些段落会被 Codex 解析为特定的行为约束，而不仅仅是指令文本。

### 5.1 Code Review Rules（代码审查规则）

当 `AGENTS.md` 中包含 `# Code Review Rules` 章节时，Codex 会将其识别为针对 GitHub PR 审查的定制规则。

```markdown
# Code Review Rules

- 每次审查最多加载 400 行代码，超过时分批审查
- 重点检查：安全漏洞、性能问题、类型错误
- 每个问题必须标注严重等级（critical / major / minor）
- 对于 critical 问题，必须提供修复建议代码
- 不要对代码风格提出非功能性建议
- 先理解整体变更目的，再逐文件审查
```

当 Codex 被用于代码审查时（例如通过 GitHub 集成），它会自动识别这个章节，并按照其中的规则执行审查。

### 5.2 Working Agreements（工作协议）

`Working Agreements` 是 Codex 的标准工作协议，通常用于定义自动化行为约定：

```markdown
# Working Agreements

- 修改 JavaScript 文件后运行 `npm test`
- 修改 Go 文件后运行 `go vet ./...`
- 在提交前运行 `npx prettier --write .`
- 不要修改 `dist/` 目录下的文件
- 如果测试失败，优先修复测试而不是跳过
```

Working Agreements 的特点是**频繁触发、自动执行**——Codex 会在每次匹配的操作后自动运行这些协议。它不是一句"记得测试"的提醒，而是一个可执行的约定。

> **区分建议**：
> - **Code Review Rules** 仅在代码审查场景触发，是审查专属规则
> - **Working Agreements** 在任何会话中都可能触发，是日常行为约束
> - 普通行为规范（非自动化约定）应该放在 `AGENTS.md` 的正文中，不需要使用特殊标题

### 5.3 与 Claude Code 的对比

Claude Code 没有硬编码的特殊段落机制。在 Claude Code 中，所有内容都写在 `CLAUDE.md` 中，作为统一的自然语言指令。如果你希望有类似"代码审查时只关注安全问题"这样的行为，你需要在 `CLAUDE.md` 中用自然语言说明，或者通过 `.claude/rules/` 中的规则文件来实现路径作用域的约束。

Codex 的特殊段落机制更像是一种**结构化行为约束**——agent 知道特定标题下的内容具有特定的行为语义，可以据此自动化决策。

## 6. Starlark 规则系统

如果说 `AGENTS.md` 是 Codex 的"宪法"（高层次原则和行为规范），那么 **Starlark 规则系统** 就是它的"刑法"（可执行的低层级工具行为控制）。

### 6.1 位置与命名

```text
<project>/.codex/rules/
├── safety.rules
├── network.rules
└── file-access.rules
```

所有的 `.rules` 文件使用 **Starlark** 语言编写。Starlark 是 Python 的一个确定性子集，由 Google 为 Bazel 构建系统开发。它的语法类似 Python，但移除了 `for`、`while`、递归等可能导致非确定性的特性。

### 6.2 三种操作类型

每个规则最终定义对一个工具操作的响应策略，分为三种：

| 操作 | 含义 | 效果 |
|------|------|------|
| `allow` | 自动允许 | agent 可以直接执行，不通知用户 |
| `prompt` | 提示用户 | agent 执行前询问用户是否批准 |
| `forbidden` | 禁止执行 | agent 无法执行该操作 |

### 6.3 一个完整的 Starlark 规则文件

```python
# .codex/rules/safety.rules

# Block access to sensitive files (Python syntax, Starlark dialect)
def evaluate(ctx):
    # ctx 提供了当前工具调用的上下文信息
    tool = ctx.tool_name
    args = ctx.tool_args
    
    # 如果正在读取 .env 文件，禁止
    if tool == "Read" and ".env" in args.get("path", ""):
        return {"decision": "forbidden", "reason": "禁止读取 .env 文件"}
    
    # 如果正在修改 package.json，需要审批
    if tool == "Edit" and "package.json" in args.get("path", ""):
        return {"decision": "prompt", "reason": "修改 package.json 需要确认"}
    
    # 在 src/ 目录下运行测试，自动允许
    if tool == "Bash" and "npm test" in args.get("command", ""):
        return {"decision": "allow", "reason": "测试命令自动放行"}
    
    # 默认不拦截（交由其他规则或默认策略处理）
    return {"decision": "allow"}
```

### 6.4 规则评估逻辑

多个 `.rules` 文件之间的评估遵循以下逻辑：

1. 所有 `.rules` 文件都会被加载并按文件名排序
2. 每个工具调用触发时，逐个评估所有规则
3. 如果任何一个规则返回 `forbidden`，该操作被阻止
4. 如果没有任何规则返回 `forbidden`，但有规则返回 `prompt`，则提示用户
5. 如果所有规则都返回 `allow`，则自动放行

```text
规则评估优先级：forbidden > prompt > allow

         ┌──────────────┐
         │ 有 forbidden？│──→ 阻止操作
         └──────┬───────┘
                │ 没有
         ┌──────v───────┐
         │ 有 prompt？  │──→ 询问用户
         └──────┬───────┘
                │ 没有
         ┌──────v───────┐
         │ 自动放行      │
         └──────────────┘
```

### 6.5 常见规则场景示例

**场景 1：保护敏感文件**

```python
# .codex/rules/protect-secrets.rules
def evaluate(ctx):
    sensitive_patterns = [".env", "credentials.json", "*.pem", "id_rsa"]
    path = ctx.tool_args.get("path", "")
    
    for pattern in sensitive_patterns:
        if pattern in path or path.endswith(pattern.replace("*", "")):
            return {"decision": "forbidden", "reason": f"禁止访问敏感文件: {pattern}"}
    
    return {"decision": "allow"}
```

**场景 2：网络请求审批**

```python
# .codex/rules/network.rules
def evaluate(ctx):
    if ctx.tool_name in ["Bash", "Edit"]:
        cmd = ctx.tool_args.get("command", "")
        if "curl" in cmd or "wget" in cmd or "npm install" in cmd:
            return {"decision": "prompt", "reason": "网络操作需要确认"}
    
    return {"decision": "allow"}
```

**场景 3：生产环境操作保护**

```python
# .codex/rules/production.rules
def evaluate(ctx):
    cwd = ctx.cwd
    if "/production/" in cwd or "/prod/" in cwd:
        if ctx.tool_name in ["Bash", "Edit", "Write"]:
            return {"decision": "prompt", "reason": "生产环境操作需要确认"}
    
    return {"decision": "allow"}
```

### 6.6 与 Claude Code 的 Markdown 规则对比

这是 Codex 和 Claude Code 在"规则"维度上最根本的差异：

| 维度 | Codex `.rules`（Starlark） | Claude Code `.claude/rules/*.md` |
|------|---------------------------|----------------------------------|
| **语言** | Starlark（Python 子集，可编程） | Markdown（自然语言描述） |
| **执行方式** | 自动评估 + 决策执行 | 作为上下文提供给 agent，由 agent 自行判断 |
| **决策类型** | `allow` / `prompt` / `forbidden` | 无结构化决策，依赖 agent 理解 |
| **作用域** | 规则文件级别（按文件名排序） | 文件级别 + 路径作用域（通过 frontmatter） |
| **确定性** | 高（规则逻辑明确） | 低（依赖 LLM 理解自然语言） |
| **灵活度** | 高（条件判断、模式匹配） | 中（自然语言可以描述复杂场景，但执行不确定） |
| **学习门槛** | 需要了解 Starlark 语法 | 仅需 Markdown |
| **调试难度** | 逻辑可追踪 | 难以确定 agent 是否遵循了规则 |
| **适用场景** | 工具级自动化决策（放行/阻止/审批） | 行为级指导（编码规范、架构约定） |

> **核心差异一句话总结**：Codex 的 `.rules` 是**可编程的自动化决策引擎**，而 Claude Code 的 `.claude/rules/` 是**自然语言的行为指南**。前者适合"什么操作允许/禁止"这种确定性控制，后者适合"代码应该怎么写"这种风格性指导。

### 6.7 实际配合使用

在实际项目中，AGENTS.md 和 .rules 文件各司其职：

```text
AGENTS.md（行为规范层）
├── 项目描述和技术栈
├── 编码规范和架构约定
├── 测试策略
└── 工作流程

.codex/rules/（工具控制层）
├── safety.rules       ← 禁止删除文件、禁止读取 .env
├── network.rules      ← 网络操作需要审批
└── review.rules       ← 审查模式下的额外约束
```

- `AGENTS.md` 告诉 agent **行为期望**（"应该怎么做"）
- `.rules` 告诉系统 **操作边界**（"什么能做、什么不能"）

## 7. 验证工具

Codex 提供了两个主要的命令来验证指令和规则的加载状态。

### 7.1 `codex status` —— 查看工作区状态

在项目根目录下运行：

```bash
codex status
```

这个命令会显示当前工作区的状态概览，包括已加载的指令文件。如果指令文件没有按预期加载，这是第一排查步骤。

### 7.2 `codex --cd` —— 审计指令加载

这是更强大的审计工具。通过 `--cd` 参数指定不同目录，可以查看在不同目录下 Codex 会加载哪些指令：

```bash
# 查看在 workspace 根目录下会加载什么指令
codex --cd . "请列出你加载的所有指令文件"

# 查看在子目录下会额外加载什么
codex --cd src/api "请列出你加载的所有指令文件"

# 验证特定目录的指令链
codex --cd src/api "你从哪些 AGENTS.md 文件中获取了指令？"
```

运行后，Codex agent 会列出它加载的所有指令文件及其来源路径，包括：

- 全局 `~/.codex/AGENTS.md`（如果存在）
- 项目根 `AGENTS.md`
- 各层级的 `AGENTS.md` / `AGENTS.override.md`
- fallback 读取的文件（如 `CLAUDE.md`）

### 7.3 与 Claude Code 的验证对比

| 验证方式 | Codex | Claude Code |
|---------|-------|-------------|
| 状态命令 | `codex status` | 无专用命令 |
| 指令审计 | `codex --cd DIR "列出指令来源"` | N/A（单文件，路径固定） |
| 规则验证 | 通过 `--cd` + 询问间接验证 | 需手动检查 `.claude/rules/` 目录 |
| 配置文件验证 | `codex -c key=value` 测试覆盖 | 手动查看 settings.json |

> **实战技巧**：如果发现指令没有按预期生效，先用 `codex status` 确认 Codex 运行正常，然后用 `codex --cd` 在不同目录层级询问已加载的指令文件列表。这能快速定位是全局层没配置、项目层没找到，还是 fallback 没有触发。

## 8. 对照总结：AGENTS.md 分层体系 vs CLAUDE.md + .claude/rules/

作为全章核心，这里给出两张对照表。第一张是宏观维度的对比，第二张是具体机制层面的逐项比较。

### 8.1 宏观维度对照

| 维度 | Codex | Claude Code |
|------|-------|-------------|
| **指令文件名** | `AGENTS.md`（全局 + 多级级联） | `CLAUDE.md`（项目根，单文件） |
| **兼容性** | 可通过 fallback 读取 CLAUDE.md | 不读取 AGENTS.md |
| **分层机制** | 全局 → 项目根 → 逐级到当前目录，拼接合并 | 单文件，通过 `.claude/rules/` 路径作用域补充 |
| **容量控制** | 默认 32 KiB，`project_doc_max_bytes` 可调 | 约 200-300 行最佳实践，无硬性限制 |
| **风格倾向** | 偏可执行约束和自动化行为定义 | 偏行为风格和个性化项目指南 |
| **规则系统** | `.codex/rules/*.rules`（Starlark 编程语言） | `.claude/rules/*.md`（Markdown + frontmatter） |
| **规则作用** | 工具级自动化决策（allow/prompt/forbidden） | 行为级上下文指导（agent 自行判断） |
| **特殊段落** | Code Review Rules / Working Agreements 有语义识别 | 无特殊段落，全为自然语言指令 |
| **验证手段** | `codex status` + `codex --cd DIR` 审计 | N/A |

### 8.2 机制级对照

| 具体机制 | Codex | Claude Code |
|---------|-------|-------------|
| 文件覆盖 | `AGENTS.override.md` > `AGENTS.md` > fallback | 单文件，无覆盖机制 |
| 全局指令 | `~/.codex/AGENTS.md` | 无（仅在 settings.json 中可配置有限全局行为） |
| 目录遍历 | 从 Git 根向下到当前目录，每级检查 | 不自动遍历 |
| 空文件处理 | 跳过 | 加载空文件（不做特殊处理） |
| 超额截断 | 静默截断，不报错 | 无截断机制 |
| 规则优先级 | `forbidden` > `prompt` > `allow` | 按文件名排序 + 路径作用域匹配 |
| 规则判定方式 | 确定性编程判定 | LLM 理解自然语言判定 |
| 多规则合并 | 所有 `.rules` 文件加载，按文件名排序评估 | 所有 `.md` 文件加载，按路径匹配筛选 |

### 8.3 选择建议

**如果你主要使用 Codex**，建议：
1. 在 `~/.codex/AGENTS.md` 中写通用行为规范（全局生效）
2. 在项目根 `AGENTS.md` 中写项目专属规范
3. 复杂项目的子模块考虑使用分层指令
4. 工具级操作控制（文件读写、网络访问）用 `.rules` 文件
5. 通过 `project_doc_fallback_filenames` 兼容旧有 CLAUDE.md

**如果你在两个工具之间切换**，建议：
1. 维护一份 `CLAUDE.md` 作为主指令文件
2. Codex 通过 fallback 读取 `CLAUDE.md`
3. 对于 Codex 特有的 Starlark 规则，创建一个基础的 `safety.rules`
4. 核心 Skills 通过符号链接共享（下一章会详细讲解）

## 本章小结

- **AGENTS.md 是分层级联的指令链**，从全局 `~/.codex/AGENTS.md` 到项目根，再到子目录逐级拼接。越靠近当前工作目录的指令文件在合并后文档中越靠后，起到覆盖效果。这与 Claude Code 的 `CLAUDE.md` 单文件模式完全不同。
- **fallback 机制实现了与 CLAUDE.md 的兼容**。通过设置 `project_doc_fallback_filenames = ["CLAUDE.md"]`，Codex 可以在找不到 AGENTS.md 时读取 CLAUDE.md。但这是"单向兼容"——Claude Code 无法读取 AGENTS.md。
- **容量限制为 32 KiB**（可通过 `project_doc_max_bytes` 调整），超额部分静默截断。分层策略可以有效利用容量：全局 8 KiB + 项目 16 KiB + 模块 8 KiB 是比较合理的分配。
- **Code Review Rules 和 Working Agreements** 是具有特殊语义的结构化段落，Codex 会据此做出行为决策。前者在代码审查场景触发，后者在任何会话中作为自动化约定执行。
- **Starlark 规则系统（`.codex/rules/*.rules`）**是 Codex 独有的确定性自动化决策引擎，支持 `allow` / `prompt` / `forbidden` 三种操作。与 Claude Code 的 `.claude/rules/*.md` 自然语言指南有本质差异——前者是"可编程的工具控制"，后者是"描述性的行为指南"。
- **验证工具 `codex status` + `codex --cd`** 可以审计指令加载情况，是排查指令不生效问题的第一步。

## 下一章预告

指令与规则系统定义了 Codex agent 如何理解项目和遵循规范。但最强大的行为扩展方式不是写更长的指令文件，而是创建可复用的 **Skills（技能）**。下一章我们将全面对比 Codex 与 Claude Code 的技能系统——从 Skills 目录结构、发现路径、渐进式延迟加载机制，到跨工具共享方案。你会看到，尽管两套工具在绝大多数配置维度上都有差异，但 Skills 标准是**完全兼容的**，这是目前两套体系之间最无缝的桥梁。
