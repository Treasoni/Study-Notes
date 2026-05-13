# 核心概念

## 1. 缓存命中 (Cache Hit)

### 定义
当请求的数据可以在缓存中找到时，称为**缓存命中**。系统直接从缓存读取数据，而不需要访问原始存储或重新计算。

**来源**: Wikipedia

> "Cache hit occurs when the requested data can be found in a cache"

### 关键特性
- 响应速度更快
- 计算成本更低
- 性能提升显著

---

## 2. 缓存未命中 (Cache Miss)

### 定义
当请求的数据不在缓存中时，称为**缓存未命中**。系统必须从慢速存储读取数据或重新执行计算。

**来源**: Wikipedia

> "Cache miss occurs when it cannot [be found in cache] — requires the more expensive access to the backing store"

### 关键特性
- 延迟增加
- 成本上升
- 需要将数据写入缓存供后续使用

### 未命中类型
| 类型 | 说明 |
|------|------|
| Compulsory Miss | 首次访问，必然未命中 |
| Capacity Miss | 缓存容量不足导致 |
| Conflict Miss | 多数据竞争同一缓存位置 |

---

## 3. KV Cache

### 定义
在 LLM 推理过程中，Transformer 计算 Query、Key、Value 向量。KV Cache 将 Key 和 Value 张量保存在推理服务器内存中，避免重复计算。

**来源**: Daily Dose of DS - Avi Chawla

> "The Key and Value tensors are persisted on inference servers, indexed by a cryptographic hash."

### 工作原理
1. **Prefill 阶段**: 处理输入 Prompt，计算所有 Token 的 KV 向量
2. **Decode 阶段**: 生成输出 Token 时，直接从缓存读取 KV 向量
3. **复杂度**: 从 O(n²) 降至 O(n)

---

## 4. Prompt Caching

### 定义
一种基于前缀匹配的缓存策略。当新请求与历史请求共享相同前缀时，复用已计算的缓存结果。

**来源**: Anthropic Claude API 文档

### 静态前缀 vs 动态后缀
| 类型 | 内容 | 变化频率 |
|------|------|----------|
| 静态前缀 | 系统指令、工具定义、项目上下文 | 不变 |
| 动态后缀 | 用户消息、助手回复、工具输出 | 每次变化 |

### 哈希约束
> "If anything in that sequence changes, even just the order of two elements, the hash changes."
— Avi Chawla

---

## 5. 命中率 (Hit Rate)

### 定义
缓存命中次数占总请求次数的百分比。

### 计算公式
```
命中率 = 命中次数 / 总请求次数 × 100%
```

### 实际案例
Claude Code 在 30 分钟编码会话中：
- **命中率**: 92%
- **成本降低**: 81%

**来源**: Daily Dose of DS

---

## 6. 缓存失效场景

### Claude API 中导致缓存失效的操作
| 操作 | 效果 |
|------|------|
| 工具定义变更 | ❌ 缓存失效 |
| 模型切换 | ❌ 缓存失效 |
| 开关 Web 搜索/引用 | ❌ 缓存失效 |
| 速度设置变更 | ❌ 缓存失效 |
| 添加/移除图片 | ❌ 缓存失效 |
| Thinking 参数变更 | ❌ 缓存失效 |

**来源**: Anthropic Claude API 文档
