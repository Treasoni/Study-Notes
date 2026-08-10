---
title: AGENTS.md 分层体系
tags: [codex, ai, 工具使用, 进阶应用, 指令]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# AGENTS.md 分层体系

> [!info] 文档定位
> **一句话定位** - 本篇覆盖 Codex 的指令与规则系统：`AGENTS.md` 的分层级联机制、与 CLAUDE.md 的 fallback 兼容、容量限制、特殊段落、Starlark 规则引擎与验证工具。`config.toml` 控制的是"骨架"——安全策略、模型选择、功能开关；真正决定 Codex agent **如何理解你的项目、遵循什么工作规范、使用什么工作协议**的，是指令与规则系统。适合从 Claude Code 迁移过来的用户，以及想为组织 / 项目 / 子目录建立分级指令体系的开发者。

---

## AGENTS.md 是什么

`AGENTS.md` 是 Codex 的指令文件，相当于 Claude Code 的 `CLAUDE.md`。它的作用是告诉 Codex agent：这个项目是什么、有什么规范、应该遵循什么工作方式。

但 Codex 在设计上做了一个关键的差异化选择：**`AGENTS.md` 不是单文件，而是一套分层级联的指令链**。这意味着，你可以为整个组织设定一套全局指令，为每个项目设定一套项目指令，甚至为项目中的不同子目录设定更细粒度的指令——所有指令最终会被拼接合并，形成一个完整的上下文。

> [!note] Claude Code 对照
> Claude Code 的 `CLAUDE.md` 是单文件，放在项目根目录。虽然可以通过 `.claude/rules/` 目录添加额外规则，但这些规则是通过路径作用域加载的，而不是分层级联拼接。这是两种完全不同的设计哲学。

---

## 发现机制与分层级联

### 发现路径

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

### 合并规则：从根到叶拼接

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

### 文件优先级

在每个目录层级，Codex 按照以下优先级查找指令文件：

| 优先级 | 文件名 | 说明 |
|--------|--------|------|
| 1（最高） | `AGENTS.override.md` | 强制覆盖级指令 |
| 2 | `AGENTS.md` | 标准指令文件 |
| 3（回退） | `project_doc_fallback_filenames` 中的文件名 | 兼容其他工具的指令文件 |

---

## 与 CLAUDE.md 的兼容：fallback 机制

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

---

## 容量限制与最佳实践

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

---

## 特殊段落

`AGENTS.md` 支持两种具有特殊含义的段落：

### Code Review Rules

针对 GitHub PR 审查的定制规则：

```markdown
# Code Review Rules

- 每次审查最多加载 400 行代码，超过时分批审查
- 重点检查：安全漏洞、性能问题、类型错误
- 每个问题必须标注严重等级（critical / major / minor）
```

### Working Agreements

标准工作协议，自动化行为约定：

```markdown
# Working Agreements

- 修改 JavaScript 文件后运行 `npm test`
- 修改 Go 文件后运行 `go vet ./...`
- 在提交前运行 `npx prettier --write .`
```

> [!note] 区分建议
> Code Review Rules 仅在代码审查场景触发；Working Agreements 在任何会话中都可能触发，是日常行为约束。

---

## Starlark 规则系统

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

> [!note] 核心差异一句话总结
> Codex 的 `.rules` 是**可编程的自动化决策引擎**，而 Claude Code 的 `.claude/rules/` 是**自然语言的行为指南**。

---

## 验证工具

```bash
# 查看当前工作区状态
codex status

# 审计指令加载
codex --cd src/api "请列出你加载的所有指令文件"
```

---

## 常见问题

### Q: AGENTS.md 和 CLAUDE.md 有什么区别？

**回答**：`AGENTS.md` 是 Codex 的指令文件，`CLAUDE.md` 是 Claude Code 的指令文件。核心差异在于：Codex 的 `AGENTS.md` 是**分层级联的指令链**，可以从全局（`~/.codex/`）到项目根再到子目录逐级拼接合并；而 Claude Code 的 `CLAUDE.md` 是单文件，虽然可通过 `.claude/rules/` 目录按路径作用域加载额外规则，但不是级联拼接。Codex 通过 `project_doc_fallback_filenames` 提供单向兼容：找不到 `AGENTS.md` 时回退读取 `CLAUDE.md`。

### Q: AGENTS.md 有容量限制吗？超了会怎样？

**回答**：有。默认上限是 **32 KiB**（由 `project_doc_max_bytes` 配置项控制）。超过上限的部分会被截断，不会加载。最佳实践是控制各层体积：全局指令不超过 8 KiB、项目指令不超过 16 KiB、模块指令不超过 8 KiB。另外，找到的指令文件如果是空文件会直接跳过。

### Q: 如何确认 Codex 实际加载了哪些指令文件？

**回答**：使用验证工具审计指令加载：`codex status` 查看当前工作区状态；`codex --cd src/api "请列出你加载的所有指令文件"` 可查看指定目录下加载的指令链。

---

## 最佳实践

### Do's

- **分层放置指令**：全局指令放 `~/.codex/AGENTS.md`，项目指令放 `<repo>/AGENTS.md`，模块指令放 `<repo>/src/AGENTS.md`，按从根到叶的级联顺序组织。
- **控制单层体积**：全局 ≤ 8 KiB、项目 ≤ 16 KiB、模块 ≤ 8 KiB，避免触发 32 KiB 硬上限导致截断。
- **使用 override 做强制覆盖**：需要覆盖指定层级时使用 `AGENTS.override.md`（同目录优先级最高）。
- **善用 fallback 兼容**：从 Claude Code 迁移时通过 `project_doc_fallback_filenames = ["CLAUDE.md", "TEAM_GUIDE.md"]` 让 Codex 回退读取既有文件。
- **区分特殊段落**：Code Review Rules 用于代码审查场景，Working Agreements 作为日常行为约束。
- **用 Starlark 规则做确定性控制**：对需要硬性拦截 / 放行的操作（如禁止读取 `.env`）用 `.codex/rules/` 的 `allow` / `prompt` / `forbidden`。
- **定期审计**：用 `codex status` 和 `codex --cd` 检查实际加载的指令链是否符合预期。

### Don'ts

- **不要把全部指令塞进单个文件**：超过 32 KiB 的部分会被截断且不加载，导致规则静默失效。
- **不要滥用 `AGENTS.override.md`**：它是强制覆盖级指令，应只用于确实需要覆盖的目录层级。
- **不要把两种特殊段落混用**：Code Review Rules 只在代码审查时触发，不要用它承载日常行为约束。
- **不要依赖 LLM 自行理解关键安全约束**：需要确定性决策（如禁止读取 `.env`）时应使用 Starlark 规则，而非自然语言描述。

---

## 小结

AGENTS.md 是 Codex 分层级联的指令链，从全局到子目录逐级拼接，最终合并成完整上下文。它通过 `AGENTS.override.md` / `AGENTS.md` / fallback 文件名三级优先级查找，并以 `project_doc_fallback_filenames` 实现了与 CLAUDE.md 的单向兼容。默认容量上限为 32 KiB，空文件会被跳过。特殊段落（Code Review Rules、Working Agreements）提供按场景触发的行为约束，而 Starlark 规则系统则是 Codex 独有的确定性自动化决策引擎（`allow` / `prompt` / `forbidden`）。验证工具 `codex status` + `codex --cd` 可以审计指令加载情况。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[Codex 配置哲学概览]] | 配置体系全景 |
| [[Skills 技能系统]] | 可复用能力包 |
| [[对照表与迁移实战]] | CLAUDE.md → AGENTS.md 迁移 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
