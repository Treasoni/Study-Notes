---
tags: [ai]
---

# Skills 编写实战指南

> [!info] 概述
> **编写 Skills = 写好 Prompt + 规范文档 + 持续迭代**。就像写菜谱：食材准备（输入要求）、烹饪步骤（执行流程）、成品标准（输出规范）、注意事项（禁忌提示）。

## 核心概念 💡

### 文件结构

**标准结构**：
```
skills/
└── sql_generator/          ← Skill 文件夹（与命名一致）
    ├── skill.md            ← 核心逻辑文件
    └── metadata.json       ← 能力描述文件
```

### metadata.json

**是什么**：Skill 的"简历"，用于低 token 成本的能力匹配

**为什么需要**：
- 让 AI 快速了解 Skill 能力
- 避免 loading 所有 skill.md
- 节省 90% 以上 token

**关键字段**：
| 字段 | 说明 | 必填 |
|------|------|------|
| name | 唯一标识符 | ✅ |
| description | 一句话描述功能 | ✅ |
| use_cases | 使用场景列表 | ✅ |
| keywords | 关键词用于匹配 | ✅ |
| when_to_use | 触发条件描述 | ✅ |
| category | 分类标签 | ❌ |

### skill.md

**是什么**：完整的 Prompt 定义文件

**核心结构**：
1. **角色设定** - "你是什么专家"
2. **能力描述** - "你能做什么"
3. **工作流程** - "按什么步骤执行"
4. **输出规范** - "输出什么格式"
5. **约束条件** - "注意什么限制"

## 操作步骤

### 步骤 1：创建文件结构

```bash
# 创建 skills 目录
mkdir -p ~/.claude/skills

# 创建你的 skill 文件夹
mkdir -p ~/.claude/skills/sql_generator

# 创建必需文件
touch ~/.claude/skills/sql_generator/skill.md
touch ~/.claude/skills/sql_generator/metadata.json
```

### 步骤 2：编写 metadata.json

```json
{
  "name": "sql_generator",
  "description": "根据自然语言描述生成 SQL 查询语句",
  "use_cases": [
    "用户需要查询数据库时",
    "用户需要编写复杂 SQL 时",
    "用户需要优化 SQL 查询时"
  ],
  "keywords": ["SQL", "数据库", "查询", "SELECT", "表"],
  "when_to_use": "当用户的问题涉及数据库查询、数据检索或 SQL 语句编写时",
  "category": "code_generation"
}
```

### 步骤 3：编写 skill.md

```markdown
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

### 步骤 4：测试验证

在 Claude Code 中测试：
```
查询所有活跃用户，按注册时间倒序排列，只返回前100条
```

## 注意事项 ⚠️

### 常见错误

**Skill 不被识别**：
- ❌ metadata.json 格式错误
- ❌ 文件夹名与 metadata.name 不一致
- ❌ when_to_use 描述太模糊

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
- ✅ `sql_generator` - 清晰描述功能
- ✅ `code_reviewer` - 明确用途
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义

**关键词选择**：
- ✅ 包含专业术语：`["SQL", "PostgreSQL", "MySQL"]`
- ✅ 包含常见动词：`["查询", "检索", "写入"]`
- ❌ 避免太泛的词：`["帮助", "工具"]`

**when_to_use 要具体**：
- ❌ 模糊：`"用户需要帮助时"`
- ✅ 具体：`"当用户问题包含'表'、'查询'、'SQL'等关键词时"`

## 常见问题 ❓

**Q: 如何组织复杂的 Skill？**

A: 当 skill.md 太长时，可以拆分成多个文件：
```
sql_generator/
├── skill.md          # 主入口
├── metadata.json
├── examples.md       # 示例集合
└── best_practices.md # 最佳实践
```

**Q: 如何让 Skill 支持参数？**

A: 在文档中说明参数：
```markdown
## 参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| --database | 数据库类型 | PostgreSQL |
```

**Q: 如何调试 Skill？**

A:
1. 检查 metadata.json 格式：`cat metadata.json | jq .`
2. 确认文件结构完整
3. 在 Claude Code 中测试触发
4. 根据输出优化 skill.md

**Q: metadata 和 skill.md 的关系？**

A: metadata 是"简历"用于快速匹配，skill.md 是"详细指南"用于执行。AI 先看 metadata 决定是否用，再加载 skill.md 执行任务。

## 相关文档
[[Skills 是什么]] | [[Prompt, Agent, MCP 是什么]] | [[Claude Code 常用功能]]
