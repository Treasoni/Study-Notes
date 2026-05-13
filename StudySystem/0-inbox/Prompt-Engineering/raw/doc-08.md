# Anthropic Claude 模型

- **Source**: 官方文档 + WebFetch
- **Author**: Anthropic
- **Date**: 2024-2025
- **Type**: official

---

## 主要模型系列

| 模型 | 定位 | 特点 |
|------|------|------|
| **Claude 3.5 Sonnet** | 平衡性能与成本 | 最佳性价比 |
| **Claude 3.5 Haiku** | 快速轻量 | 低延迟、低成本 |
| **Claude 3 Opus** | 最高智能 | 复杂推理任务 |

## 核心能力

- **长上下文**：支持 200K tokens
- **代码生成**：优秀的编程辅助能力
- **多语言支持**：支持中文等100+语言
- **工具使用**：Function Calling / Tool Use
- **视觉理解**：图像输入支持（部分模型）

## 提示词技巧

### 使用系统提示词
明确角色和约束

### 提供具体示例
帮助模型理解期望格式

### 分步骤提问
复杂问题时

### 明确输出格式
要求

### XML标签分隔
Anthropic推荐使用XML标签分隔内容：

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "请解释<topic>闭包</topic>的概念"}
    ]
)
```

## 关键优势

1. **写作质量**：擅长长文本创作和分析
2. **代码理解**：深度理解代码逻辑和架构
3. **安全对齐**：内置安全策略，减少有害输出
4. **工具调用**：优秀的Function Calling能力
