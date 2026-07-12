---
title: Skills 编写实战指南
tags: [ai, 进阶应用, skills]
created: 2026-04-05
updated: 2026-07-12
status: updated
source_project: claude-code-tutorial
---

# Skills 编写实战指南

> **前置知识**：[[01-基础概念/Skills 是什么]] - Skills 基础概念

> [!info] 概述
> **编写 Skills = 写好 Prompt + 规范文档 + 持续迭代**。就像写菜谱：食材准备（输入要求）、烹饪步骤（执行流程）、成品标准（输出规范）、注意事项（禁忌提示）。

## 核心概念 💡

### 当前 Skills 格式（v2.1.207）

> [!note] 2026 年格式变更
> Skills 已采用 **Agent Skills 开放标准**，格式从旧的 `metadata.json` + `skill.md` 双文件结构简化为单一的 `SKILL.md` 文件，通过 YAML frontmatter 声明元数据。

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
| `name` | 唯一标识符 | ✅ |
| `description` | 描述（最重要——决定自动触发率） | ✅ |
| `allowed-tools` | 允许的工具列表 | ❌ |
| `disallowed-tools` | 禁止的工具列表（v2.1.199+） | ❌ |
| `context: fork` | 在子代理中隔离执行 | ❌ |
| `model: haiku` | 指定使用的模型 | ❌ |
| `argument-hint` | 参数提示 | ❌ |
| `disable-model-invocation` | 禁止 Claude 自动触发 | ❌ |

**描述要"pushy"**：
> [!tip] 描述原则
> description 字段要列出具体触发词，提高自动调用率。例如："当用户说'简化这段代码'或'重构优化'时触发。"
> 参考：[[Claude Code Slash Commands 完整参考]]

### 与旧格式对比（2026 年前）

| 维度 | 旧格式 | 当前格式 |
|------|--------|---------|
| 文件 | `metadata.json` + `skill.md` | `SKILL.md`（单文件） |
| 元数据 | 独立的 JSON 文件 | YAML frontmatter |
| 目录 | `~/.claude/skills/` | `.claude/skills/<name>/` |
| 可移植性 | Claude Code 专属 | Agent Skills 开放标准 |
| 参数传递 | 字符串 | 命名参数（v2.1.199+） |

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
description: 根据自然语言描述生成 SQL 查询语句。当用户说"写查询"、"查数据库"、"SQL"时触发。
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
> 支持在 description 中定义命名参数，通过 `$ARGUMENTS.param_name` 引用，取代旧版的 `$ARGUMENTS` 字符串拼接。

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

A: 当前格式支持命名参数（v2.1.199+），在 frontmatter 中声明，通过 `$ARGUMENTS.param_name` 引用：
```markdown
---
name: sql-generator
argument-hint: [database_type]
---
使用 $ARGUMENTS.database_type 数据库类型生成查询。
```

**Q: 如何调试 Skill？**

A:
1. 检查 metadata.json 格式：`cat metadata.json | jq .`
2. 确认文件结构完整
3. 在 Claude Code 中测试触发
4. 根据输出优化 skill.md

**Q: 一个 Skill 文件太长怎么办？**

A: SKILL.md 推荐控制在 500 行以内。参考资料、示例可以拆到独立的 `.md` 文件中，主文件通过路径引用。

**Q: Skills 和 Subagents 有什么区别？**

A: 核心区别在于**执行方式**：
- **Skills**：在主线程执行，Claude 可观察其全过程
- **Subagents**：在隔离上下文中执行，不污染主上下文
- Skills 适合提示词注入；Subagents 适合独立任务委派

**Q: Skills 和 Dynamic Workflows 有什么区别？**

A: Skills 跑在前台（在主上下文或 forked subagent 里）；workflow 跑在后台（独立运行时 + 隔离脚本）。

## 相关文档
[[01-基础概念/Skills 是什么]] | [[Claude Code Subagents 完整指南]] | [[Claude Code 高级功能]]
