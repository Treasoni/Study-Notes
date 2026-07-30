---
title: "Codex 完整配置体系"
tags: [codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# 第三章：指令与规则 —— AGENTS.md 分层体系
前两章我们分别建立了 Codex 配置体系的全局图景，并深入解读了 `config.toml` 的每个区块。但是，`config.toml` 控制的是"骨架"——安全策略、模型选择、功能开关。真正决定 Codex agent **如何理解你的项目、遵循什么工作规范、使用什么工作协议**的，是指令与规则系统。本章将深入 Codex 的指令文件 `AGENTS.md` 的分层级联机制——这是它与 Claude Code 的 `CLAUDE.md` 最核心的差异之一——以及独特的 `Starlark` 规则引擎。

### 1. AGENTS.md 是什么？

`AGENTS.md` 是 Codex 的指令文件，相当于 Claude Code 的 `CLAUDE.md`。它的作用是告诉 Codex agent：这个项目是什么、有什么规范、应该遵循什么工作方式。

但 Codex 在设计上做了一个关键的差异化选择：**`AGENTS.md` 不是单文件，而是一套分层级联的指令链**。这意味着，你可以为整个组织设定一套全局指令，为每个项目设定一套项目指令，甚至为项目中的不同子目录设定更细粒度的指令——所有指令最终会被拼接合并，形成一个完整的上下文。

> **Claude Code 对照**：Claude Code 的 `CLAUDE.md` 是单文件，放在项目根目录。虽然可以通过 `.claude/rules/` 目录添加额外规则，但这些规则是通过路径作用域加载的，而不是分层级联拼接。这是两种完全不同的设计哲学。

### 2. 发现机制与分层级联

#### 2.1 发现路径

构建过程分为两个阶段：

```
阶段 1：全局层
  ~/.codex/AGENTS.override.md  ── 如果存在，优先使用
  ~/.codex/AGENTS.md            ── 否则使用此文件

阶段 2：项目层（从 Git 根目录向下遍历到当前目录）
  每级目录检查（按优先级从高到低）：
    1. AGENTS.override.md ── 如果存在，使用此文件
    2. AGENTS.md           ── 否则检查此文件
    3. 回退文件名          ── project_doc_fallback_filenames 中配置的文件
```

#### 2.2 合并规则：从根到叶拼接

找到所有指令文件后，Codex 按照**从根到叶**的顺序拼接：

```text
最终指令文档的内容顺序：
┌──────────────────────────────────┐
│  ~/.codex/AGENTS.md              │  ← 全局指令
│  /repo/AGENTS.md                 │  ← 项目根指令
│  /repo/src/AGENTS.md             │  ← 子目录指令
│  /repo/src/components/AGENTS.md  │  ← 当前目录指令（最后加载，优先覆盖）
└──────────────────────────────────┘
```

#### 2.3 文件优先级

在每个目录层级，Codex 按照以下优先级查找指令文件：

| 优先级 | 文件名 | 说明 |
|--------|--------|------|
| 1（最高） | `AGENTS.override.md` | 强制覆盖级指令 |
| 2 | `AGENTS.md` | 标准指令文件 |
| 3（回退） | `project_doc_fallback_filenames` 中的文件名 | 兼容其他工具的指令文件 |

### 3. 与 CLAUDE.md 的兼容：fallback 机制

对于从 Claude Code 迁移过来的用户，Codex 提供了兼容性机制：**通过 `project_doc_fallback_filenames` 配置，让 Codex 在找不到 `AGENTS.md` 时回退读取 `CLAUDE.md`**。

```toml
# .codex/config.toml
project_doc_fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]
```

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

### 4. 容量限制与最佳实践

Codex 对 AGENTS.md 链有硬性的容量限制：

- **默认上限**：**32 KiB**（`project_doc_max_bytes` 配置项控制）
- **超过上限**：超过的部分会被截断，不会加载
- **空文件跳过**：找到的指令文件如果是空文件，直接跳过

分层策略的最佳实践：

```text
~/.codex/AGENTS.md           ← 全局指令：不超过 8 KiB
  ├── 通用行为规范
  ├── 默认编码规范
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

### 5. 特殊段落

`AGENTS.md` 支持两种具有特殊含义的段落：

**Code Review Rules** —— 针对 GitHub PR 审查的定制规则：

```markdown
# Code Review Rules

- 每次审查最多加载 400 行代码，超过时分批审查
- 重点检查：安全漏洞、性能问题、类型错误
- 每个问题必须标注严重等级（critical / major / minor）
```

**Working Agreements** —— 标准工作协议，自动化行为约定：

```markdown
# Working Agreements

- 修改 JavaScript 文件后运行 `npm test`
- 修改 Go 文件后运行 `go vet ./...`
- 在提交前运行 `npx prettier --write .`
```

> **区分建议**：Code Review Rules 仅在代码审查场景触发；Working Agreements 在任何会话中都可能触发，是日常行为约束。

### 6. Starlark 规则系统

如果说 `AGENTS.md` 是 Codex 的"宪法"，那么 **Starlark 规则系统**就是它的"刑法"——可执行的低层级工具行为控制。

```text
<project>/.codex/rules/
├── safety.rules
├── network.rules
└── file-access.rules
```

三种操作类型：

| 操作 | 含义 | 效果 |
|------|------|------|
| `allow` | 自动允许 | agent 可以直接执行，不通知用户 |
| `prompt` | 提示用户 | agent 执行前询问用户是否批准 |
| `forbidden` | 禁止执行 | agent 无法执行该操作 |

一个完整的 Starlark 规则文件示例：

```python
# .codex/rules/safety.rules
def evaluate(ctx):
    tool = ctx.tool_name
    args = ctx.tool_args

    if tool == "Read" and ".env" in args.get("path", ""):
        return {"decision": "forbidden", "reason": "禁止读取 .env 文件"}

    if tool == "Edit" and "package.json" in args.get("path", ""):
        return {"decision": "prompt", "reason": "修改 package.json 需要确认"}

    if tool == "Bash" and "npm test" in args.get("command", ""):
        return {"decision": "allow", "reason": "测试命令自动放行"}

    return {"decision": "allow"}
```

规则评估逻辑：`forbidden` > `prompt` > `allow`

| 维度 | Codex `.rules`（Starlark） | Claude Code `.claude/rules/*.md` |
|------|---------------------------|----------------------------------|
| 语言 | Starlark（Python 子集，可编程） | Markdown（自然语言描述） |
| 执行方式 | 自动评估 + 决策执行 | 作为上下文提供给 agent，由 agent 自行判断 |
| 决策类型 | `allow` / `prompt` / `forbidden` | 无结构化决策 |
| 确定性 | 高（规则逻辑明确） | 低（依赖 LLM 理解） |

> **核心差异一句话总结**：Codex 的 `.rules` 是**可编程的自动化决策引擎**，而 Claude Code 的 `.claude/rules/` 是**自然语言的行为指南**。

### 7. 验证工具

```bash
# 查看当前工作区状态
codex status

# 审计指令加载
codex --cd src/api "请列出你加载的所有指令文件"
```

> **本章小结**：AGENTS.md 是分层级联的指令链，从全局到子目录逐级拼接。fallback 机制实现了与 CLAUDE.md 的单向兼容。容量限制为 32 KiB。Starlark 规则系统是 Codex 独有的确定性自动化决策引擎。验证工具 `codex status` + `codex --cd` 可以审计指令加载情况。

---


---

> [!note] 导航
> [[02 config.toml 核心配置|← 上一章]] | [[04 Skills 技能系统|下一章 →]]



