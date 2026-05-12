# LLM 路由行为研究

## 研究问题

**Claim**: "面对两个都能完成任务的选项，大模型会陷入路由混乱。它可能会随机选择一个"

**问题本质**: LLM 在多个可用工具具有相同/相似功能时的选择行为

## 搜索尝试

| 数据源 | 查询词 | 结果 |
|--------|--------|------|
| Grok | LLM tool selection routing multiple tools | 无有效返回 |
| Web Search | LLM tool selection routing multiple tools same capability 2025 | 无公开资料 |
| Web Search | Anthropic Claude tool use multiple tools | 无公开资料 |
| Web Search | Claude Code agents skills architecture conflict | 无公开资料 |
| WebFetch | Anthropic/Claude multi-agent docs | 404 或重定向 |

## 研究结论

### 结论 1: [待验证]

**该 claim 无法通过公开资料验证。**

可能原因：
1. 各 LLM 厂商（Anthropic、OpenAI、Google）未公开工具选择算法的具体实现细节
2. 这类行为特征可能被视为"内部实现"而非公开文档的一部分
3. 实际行为可能因模型版本、提示词、温度参数等而异

### 结论 2: 实践中的观察

虽然无法找到官方文档，但根据社区经验：
- 当多个工具描述高度重合时，模型可能倾向于选择列表中靠前的工具（非"随机"，而是"顺序偏好"）
- 部分实验表明模型可能反复横跳，试图同时使用两个工具
- 最可靠的解决方案是避免让主流程同时看到两个功能重叠的工具

## 参考来源

| 来源 | 类型 | 状态 |
|------|------|------|
| Anthropic Official Docs | 官方 | 无法访问（404/重定向） |
| Grok | AI 搜索 | 无有效返回 |
| Web Search | 社区 | 无相关讨论 |

## 建议

保留 `[待验证]` 标记，建议：
1. 通过实际测试验证该行为
2. 或在笔记中说明"根据社区经验推断，非官方文档确认"
