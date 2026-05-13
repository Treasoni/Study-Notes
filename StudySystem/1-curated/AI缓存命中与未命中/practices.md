# 实战示例

## Claude API 提示缓存使用

### 基础配置

```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # 自动缓存
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Analyze this document."}
    ]
)
```

### 精细化缓存断点

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert software engineer...",  # 会被缓存
            "cache_control": {"type": "ephemeral", "ttl": "1h"}
        },
    ],
    messages=[
        {"role": "user", "content": "warmup"}  # 这部分每次不同
    ]
)
```

**来源**: Anthropic Claude API 文档

---

## 缓存预热 (Cache Pre-Warming)

消除首次请求延迟：

```python
# 使用 max_tokens=0 预热缓存
prewarm = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=0,
    system=[{
        "type": "text",
        "text": "You are an expert software engineer...",
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": "warmup"}]
)
# 返回空的 content 和填充的 usage
```

**来源**: Anthropic Claude API 文档

---

## 追踪缓存性能

```python
response = client.messages.create(...)

# 查看缓存指标
cache_read = response.usage.cache_read_input_tokens      # 从缓存读取的 Token 数
cache_write = response.usage.cache_creation_input_tokens # 写入缓存的 Token 数
input_tokens = response.usage.input_tokens              # 缓存断点后的 Token 数

total_tokens = cache_read + cache_write + input_tokens
```

**来源**: Anthropic Claude API 文档

---

## 最佳实践：Prompt 结构化

推荐 Prompt 顺序：
1. 系统指令
2. 工具定义
3. 参考上下文
4. 对话历史

```python
system=[
    {"type": "text", "text": "系统提示...", "cache_control": {...}},
    {"type": "text", "text": "工具定义...", "cache_control": {...}},
],
messages=[...]
```

**来源**: Daily Dose of DS - Avi Chawla

---

## 成本计算示例

| 阶段 | Token 数 | 单价 | 费用 |
|------|----------|------|------|
| 首次请求 (Cache Write) | 10,000 | $6.25/MTok | $0.0625 |
| 后续命中 (Cache Read) | 10,000 | $0.50/MTok | $0.005 |
| 未命中 (正常) | 10,000 | $5/MTok | $0.05 |

**节省比例**: 90% (命中时)

**来源**: Anthropic Claude API 文档

---

## 应避免的操作

| ❌ 错误做法 | ✅ 正确做法 |
|------------|-------------|
| 中途修改工具定义 | 提前规划好工具 |
| 切换模型 | 保持同一模型 |
| 在前缀中更新状态 | 附加提醒标签 |
| 每次请求改顺序 | 保持相同顺序 |

**来源**: Daily Dose of DS - Avi Chawla
