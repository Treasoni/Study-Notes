# 实战示例汇总

## 示例 1: 零样本情感分类

**提示词**:
```
Classify the text into neutral, negative or positive.
Text: I think the vacation is okay.
Sentiment:
```

**输出**:
```
Neutral
```

**适用**: 简单分类任务、明确指令

---

## 示例 2: 少样本学习（1-shot）

**提示词**:
```
A 'farduddle' means to jump up and down really fast.
Word: farduddle
Use in a sentence:
```

**输出**:
```
When we won the game, we all started to farduddle in celebration.
```

**适用**: 学习新词汇、特定格式输出

---

## 示例 3: 零样本思维链

**提示词**:
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?
A: Let's think step by step.
```

**效果**: 添加 "Let's think step by step" 可显著改善数学推理

---

## 示例 4: 角色提示

**场景**: 黑洞解释

| 角色 | 输出风格 |
|------|----------|
| AI 研究助手 | 技术性、科学性 |
| 小学教师 | 简单易懂 |

**提示词示例**:
```
你是一位AI研究助手，用技术性和科学性的语调回答问题。
```

---

## 示例 5: 上下文工程分层架构

| 层级 | 内容 |
|------|------|
| 系统层 | 基础角色和能力定义 |
| 任务层 | 具体任务指令 |
| 工具层 | API 和工具描述 |
| 记忆层 | 历史交互和状态 |

---

## 示例 6: 搜索规划 Agent

**结构化输出示例**:
```json
{
  "search_task": "搜索任务描述",
  "priority": 1,  // 1(最高) 到 5(最低)
  "date_range": "2024-01-01 to 2024-12-31",
  "expected_results": 10
}
```

**要点**: 显式定义字段类型和约束，减少模型假设
