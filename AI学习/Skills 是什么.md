---
tags: [ai]
---

# Skills 技能系统

> [!info] 概述
> **Skills 是 AI 的"快捷键"** - 预定义的可重用任务模块，通过斜杠命令（如 `/commit`）一键触发。就像点外卖套餐，一键包含主食+饮料+甜点，无需每次重新描述需求。

## 核心概念 💡

### 什么是 Skills

**是什么**：预定义的完整任务工作流，可重复使用

**为什么需要**：
- 快速执行常用操作
- 保证执行一致性
- 降低 token 消耗
- 模块化管理能力

**与其他概念关系**：
- vs Prompt：Skills 是高质量的 Prompt 模块
- vs Agent：Skills 是预定义流程，Agent 是动态决策
- vs MCP：Skills 是用户层，MCP 是工具层

### Skills 的特点

| 特点 | 说明 | 比喻 |
|------|------|------|
| **命令式调用** | 通过 `/command` 触发 | 快捷键 |
| **预定义行为** | 完整的执行流程 | 套餐 |
| **可组合性** | 可互相调用 | 加菜 |
| **可配置参数** | 支持参数定制 | 微辣不要香菜 |

## 操作步骤

### 使用 Skills 的方式

#### 方式一：斜杠命令
```bash
/commit
/commit -m "修复登录bug"
/review-pr 123
```

#### 方式二：自然语言触发
```bash
帮我画一个用户注册流程图
创建一个 Excalidraw 思维导图
生成一个表格视图
```

### Skills 工作流程

```
┌─────────────────────────────────────────────┐
│  1. 用户触发 Skill（如 /commit）            │
│       ↓                                     │
│  2. Skill 解析器识别命令                     │
│       ↓                                     │
│  3. 加载 Skill 定义（metadata + skill.md）  │
│       ↓                                     │
│  4. AI 执行预设工作流程                      │
│       ↓                                     │
│  5. 返回执行结果                            │
└─────────────────────────────────────────────┘
```

### Skill 选择机制

1. **初始阶段**：只提供所有 skill 的 metadata 列表
2. **匹配阶段**：AI 根据 metadata 判断需要哪个 skill
3. **加载阶段**：读取对应的 skill.md 完整内容
4. **生成阶段**：基于完整 Prompt 生成回复

## 注意事项 ⚠️

### 常见错误

**Skill 不被识别**：
- metadata.json 格式错误
- 文件夹名与 metadata.name 不一致
- when_to_use 描述不明确

**输出不符合预期**：
- skill.md 描述不清
- 约束条件不够强
- 缺少具体示例

**AI 不调用 Skill**：
- 关键词设置不准确
- 触发条件太模糊
- 与用户问题匹配度低

### 关键配置点

**metadata.json 编写**：
```json
{
  "name": "sql_generator",
  "description": "根据自然语言生成 SQL",
  "use_cases": ["查询数据", "优化SQL"],
  "keywords": ["SQL", "数据库", "查询"],
  "when_to_use": "涉及数据库查询时"
}
```

**skill.md 结构**：
1. 角色设定 - "你是什么专家"
2. 能力描述 - "你能做什么"
3. 工作流程 - "按什么步骤执行"
4. 输出规范 - "输出什么格式"
5. 约束条件 - "注意什么限制"

**命名规范**：
- ✅ `sql_generator` - 清晰描述功能
- ✅ `code_reviewer` - 明确用途
- ❌ `helper` - 太泛
- ❌ `my_agent` - 无意义

## 常见问题 ❓

**Q: Skills 和 MCP 有什么区别？**

A: Skills 是用户交互层的"快捷键"，通过命令触发完整任务；MCP 是工具服务层的"后厨厨师"，提供可调用的函数。Skills 可以调用 MCP 工具。

**Q: 什么时候应该创建 Skill？**

A: 当你发现某个操作需要经常重复执行，且步骤固定时。比如代码提交、PR 审查、特定格式生成等。

**Q: metadata 为什么很重要？**

A: metadata 是"简历"，让 AI 快速了解 Skill 能力，避免加载所有 skill.md 内容，节省 90% 以上 token。

**Q: 一个 Skill 可以调用另一个 Skill 吗？**

A: 可以。Skills 可以互相调用或与普通 Prompt 混合使用，实现复杂的工作流。

**Q: 如何调试 Skill？**

A:
1. 检查 metadata.json 格式是否正确
2. 确认 when_to_use 描述是否明确
3. 在 Claude Code 中测试触发
4. 根据输出质量优化 skill.md

## 相关文档
[[Prompt, Agent, MCP 是什么]] | [[如何编写Skills]] | [[Claude Code 常用功能]]
