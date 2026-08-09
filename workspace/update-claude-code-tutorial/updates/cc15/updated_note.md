---
title: Skills 编写实战指南
tags: [ai, 进阶应用, skills]
created: 2026-04-05
updated: 2026-08-10
status: updated
source_project: claude-code-tutorial
---

# Skills 编写实战指南

> **前置知识**：[[Skills 是什么]] - Skills 基础概念

> [!info] 概述
> **编写 Skills = 写好 Prompt + 规范文档 + 持续迭代**。就像写菜谱：食材准备（输入要求）、烹饪步骤（执行流程）、成品标准（输出规范）、注意事项（禁忌提示）。

## 核心概念 💡

### 当前 Skills 格式（2026-08 现行规范）

> [!note] 2026 年格式变更
> Skills 已采用 **Agent Skills 开放标准**，格式从旧的 `metadata.json` + `skill.md` 双文件结构简化为单一的 `SKILL.md` 文件，通过 YAML frontmatter 声明元数据。

> [!tip] 大白话
> SKILL.md 就是「带说明书的提示词文件」。正文写「怎么做」，frontmatter 写「什么时候用（description）」。Claude 会在合适时机自动把它调出来；如果你不想让它自动触发，就在 frontmatter 加 `disable-model-invocation: true`，改成自己手动 `/skill-name` 运行。

**标准结构**：
```
.claude/skills/
└── sql-generator/          ← Skill 文件夹（kebab-case）
    └── SKILL.md            ← 核心指令文件（含 YAML frontmatter）
```

### SKILL.md Frontmatter

**是什么**：SKILL.md 的 YAML 头部，替代了旧版的 metadata.json，以更低 token 成本实现能力匹配

**关键字段**：

| 字段 | 说明 | 必填 |
|------|------|------|
| `name` | 显示名（默认取目录名；命令名来自目录/文件名） | ❌ |
| `description` | 描述（最重要——决定自动触发率；未写则取正文首段） | ✅ 推荐 |
| `when_to_use` | 补充触发场景/示例请求，追加到 description 后 | ❌ |
| `allowed-tools` | 允许的工具列表（免确认） | ❌ |
| `disallowed-tools` | 禁止的工具列表（v2.1.199+） | ❌ |
| `context: fork` | 在子代理中隔离执行 | ❌ |
| `model` | 指定使用的模型 | ❌ |
| `argument-hint` | 自动补全时的参数提示（仅提示，不定义参数） | ❌ |
| `arguments` | 命名位置参数，正文用 `$参数名` 引用 | ❌ |
| `user-invocable` | 设为 `false` 时从 `/` 菜单隐藏，仅 Claude 可调用 | ❌ |
| `disable-model-invocation` | 设为 `true` 时禁止 Claude 自动触发，仅用户手动运行 | ❌ |

**描述要"pushy"**：
> [!tip] 描述原则
> description 字段要列出具体触发词，提高自动调用率。例如："当用户说'简化这段代码'或'重构优化'时触发。"
> 参考：[[Claude Code Slash Commands 完整参考]]
>
> 注意：这是「想让它自动触发」时的写法。若你想让用户**手动运行**（比如部署、发消息这类有副作用的操作），就在 frontmatter 加 `disable-model-invocation: true`——Claude 不会自动加载该 skill，只保留 `/skill-name` 手动入口。

> [!tip] 大白话（谁可以调用）
> 谁调用 skill 由两个开关决定：`disable-model-invocation: true` = 「只有我能手动用」，`user-invocable: false` = 「只让 Claude 自动用」。默认两者都能用。

### 调用控制（谁可以触发）

默认你和 Claude **都能**调用任意 skill；两个 frontmatter 字段可限制：

| Frontmatter | 用户可调用 | Claude 可调用 | description 进上下文 |
|------|------|------|------|
| （默认） | ✅ | ✅ | ✅ 始终加载 |
| `disable-model-invocation: true` | ✅ | ❌ | ❌ 只在手动调用时加载 |
| `user-invocable: false` | ❌ | ✅ | ✅ 始终加载 |

> [!warning] 拦截行为
> 对带 `disable-model-invocation: true` 的 skill，即使 Claude 尝试自动调用，Claude Code 也会拦截，并提示你不要用其他方式复刻其步骤——Claude 通常会建议你自己运行 `/skill-name`。

### Slash / Skill 叠加调用（v2.1.199+）

一条消息开头可以连续输入多个 skill 命令**叠加加载**：

```
/skill-a /skill-b do XYZ
```

- 尾部文本 `do XYZ` 会作为 `$ARGUMENTS` **同时传给每个**被加载的 skill。
- 第一个 skill 之后最多再叠加 **5 个**（合计最多 6 个），如 `/a /b /c /d /e /f 任务内容`。
- 展开在遇到「非内联用户可调用」的 skill 时停止（如以子代理运行的 `/code-review`、参数可能以 `/` 开头的 `/loop`），该 skill 及其后的文本都作为参数。
- v2.1.199 之前只有第一个 skill 会加载，其余会变成字面参数文本。

> [!tip] 大白话（叠加）
> 一次能叠好几个 skill：`/a /b 做XXX` 会把「做XXX」同时交给 a 和 b。适合「先加载几个前置知识，再开始干活」的场景。

### 与旧格式对比（2026 年前）

| 维度 | 旧格式 | 当前格式 |
|------|--------|---------|
| 文件 | `metadata.json` + `skill.md` | `SKILL.md`（单文件） |
| 元数据 | 独立的 JSON 文件 | YAML frontmatter |
| 目录 | `~/.claude/skills/` | `.claude/skills/<name>/` |
| 可移植性 | Claude Code 专属 | Agent Skills 开放标准 |
| 参数传递 | 字符串 | 命名参数（`arguments` + `$name`，v2.1.199+） |

## 操作步骤

### 步骤 1：创建文件结构

```bash
# 创建 skills 目录
mkdir -p ~/.claude/skills

# 创建你的 skill 文件夹（kebab-case 命名）
mkdir -p ~/.claude/skills/sql-generator

# 创建 SKILL.md
touch ~/.claude/skills/sql-generator/SKILL.md
```

### 步骤 2：编写 SKILL.md（含 Frontmatter）

当前格式使用 YAML frontmatter 替代了旧版的 metadata.json：

```markdown
---
name: sql-generator
description: "根据自然语言描述生成 SQL 查询语句。当用户说'写查询'、'查数据库'、'SQL'时触发。"
allowed-tools: Read, Bash
model: claude-sonnet-5
argument-hint: [database_type, query_description]
---

# SQL 查询生成器

## 角色
你是一个专业的 SQL 数据库查询编写专家，精通 MySQL、PostgreSQL、SQLite 等主流数据库的语法特性。

## 能力
你能够根据用户的自然语言描述，生成准确、高效、安全的 SQL 查询语句。

## 工作流程

### 步骤 1：分析需求
- 仔细阅读用户的查询需求
- 识别涉及的表名、字段名
- 确定查询类型（SELECT/INSERT/UPDATE/DELETE）
- 理解筛选条件和排序要求

### 步骤 2：构建查询
- 根据分析结果构建 SQL 语句
- 使用适当的 JOIN 处理关联表
- 添加必要的 WHERE 条件
- 按要求添加 ORDER BY 或 LIMIT

### 步骤 3：优化查询
- 检查是否可以优化性能
- 避免不必要的列查询
- 使用索引友好的条件

### 步骤 4：生成输出
- 输出格式化的 SQL 语句
- 添加简洁的注释说明

## 输出规范

```sql
-- 查询说明
SELECT id, name, email
FROM users
WHERE status = 'active'
  AND created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 100;
```

## 约束条件
- 必须使用参数化查询（用 $1, $2 占位符）
- 永远不要生成没有 WHERE 条件的 UPDATE/DELETE
- 添加适当的注释说明查询目的
- SQL 语句格式化，便于阅读
```

> [!tip] 命名参数（v2.1.199+）
> 用 `arguments` 字段在 frontmatter 声明命名参数，正文用 `$参数名` 引用（如 `arguments: [database_type]` → `$database_type`）；`argument-hint` 只负责自动补全时的提示，不定义参数。按位置取参用 `$ARGUMENTS[N]` 或 `$N`，取全部用 `$ARGUMENTS`。

### 步骤 3：测试验证

在 Claude Code 中测试：
```
查询所有活跃用户，按注册时间倒序排列，只返回前100条
```

## 注意事项 ⚠️

### 常见错误

**Skill 不被识别**：
- ❌ SKILL.md frontmatter 格式错误
- ❌ 文件夹名与 frontmatter 的 name 不一致
- ❌ description 描述太模糊

**输出不符合预期**：
- ❌ skill.md 描述不清
- ❌ 约束条件不够强
- ❌ 缺少具体示例

**AI 不调用 Skill**：
- ❌ 关键词设置不准确
- ❌ 触发条件不明确
- ❌ 与用户问题匹配度低

> 若你根本不想让模型自动触发（比如部署、发消息这类有副作用的操作），直接加 `disable-model-invocation: true`，改由用户手动 `/skill-name` 运行——不要靠「写模糊 description」来阻止触发。

### 关键配置点

**命名规范**：
- ✅ `sql-generator` - 清晰描述功能
- ✅ `code-reviewer` - 明确用途
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义

**关键词选择**：
- ✅ 在 description 中包含专业术语：`"当用户提到 SQL、PostgreSQL、MySQL 时触发"`
- ✅ 包含常见动词：`"查询"`、`"检索"`、`"写入"`
- ❌ 避免太泛的词：`"帮助"`、`"工具"`

**description 要具体（pushy）**：
- ❌ 模糊：`"用户需要帮助时"`
- ✅ 具体：`"当用户问题包含'表'、'查询'、'SQL'等关键词时"`

## 常见问题 ❓

**Q: 如何组织复杂的 Skill？**

A: SKILL.md 推荐控制在 **500 行以内**。过长时可拆分成多个文件：
```
sql-generator/
├── SKILL.md             # 主入口（含 frontmatter）
├── examples.md          # 示例集合
└── scripts/
    └── validate.sh      # 可执行脚本
```

**Q: 如何让 Skill 支持参数？**

A: 当前格式支持命名参数（v2.1.199+）：用 `arguments` 字段在 frontmatter 声明，正文用 `$参数名` 引用（`argument-hint` 仅作自动补全提示）：
```markdown
---
name: sql-generator
arguments: [database_type]
---
使用 $database_type 数据库类型生成查询。
```

**Q: 如何调试 Skill？**

A:
1. 检查 SKILL.md 的 YAML frontmatter 格式（格式错误时 skill 会用空元数据加载，`/name` 可用但无 description 匹配）；可用 `claude --debug` 查看解析错误
2. 确认文件结构完整（目录名 + SKILL.md）
3. 在 Claude Code 中测试触发：`/skill-name` 手动触发，或问一个匹配 description 的问题
4. 根据输出优化 SKILL.md

**Q: 一个 Skill 文件太长怎么办？**

A: SKILL.md 推荐控制在 500 行以内。参考资料、示例可以拆到独立的 `.md` 文件中，主文件通过路径引用。

**Q: 如何防止 Claude 自动触发 Skill？**

A: 在 frontmatter 加 `disable-model-invocation: true`。设置后 Claude 不会自动加载/调用该 skill（description 也不进上下文），Claude 会请你手动运行 `/skill-name`；适合部署、发消息等需要你控制时机的操作。相对的，`user-invocable: false` 则是从 `/` 菜单隐藏、只让 Claude 调用。

**Q: Skills 和 Subagents 有什么区别？**

A: 核心区别在于**执行方式**：
- **Skills**：在主线程执行，Claude 可观察其全过程
- **Subagents**：在隔离上下文中执行，不污染主上下文
- Skills 适合提示词注入；Subagents 适合独立任务委派

**Q: Skills 和 Dynamic Workflows 有什么区别？**

A: Skills 跑在前台（在主上下文或 forked subagent 里）；workflow 跑在后台（独立运行时 + 隔离脚本）。

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 同步 2026-08 Skills 规范：新增 `disable-model-invocation`（禁止模型自动调用，仅用户手动运行）与 `user-invocable`（仅 Claude 调用）说明；新增 Slash/Skill 叠加调用（`/a /b do XYZ`，第一个之后最多 5 个）；修正 frontmatter 必填列（`name` 默认取目录名、`description` 未写取正文首段）；命名参数改用 `arguments` + `$name`（`argument-hint` 仅作提示）；调试步骤不再引用 metadata.json；新增多处 `[!tip] 大白话` |

## 相关文档
[[Skills 是什么]] | [[Claude Code Subagents 完整指南]] | [[Claude Code 高级功能]]
