# 知识地图：AI缓存命中与未命中

## 主题层级

```
AI 缓存命中与未命中
├── 基础概念
│   ├── 缓存定义
│   ├── 缓存命中 (Cache Hit)
│   └── 缓存未命中 (Cache Miss)
├── 缓存机制原理
│   ├── 缓存结构 (Tag + Data)
│   ├── 命中率计算
│   └── 替换策略 (LRU等)
└── AI/LLM中的应用
    ├── KV Cache
    │   ├── Prefill 阶段
    │   ├── Decode 阶段
    │   └── 哈希索引
    ├── Prompt Caching
    │   ├── 静态前缀 vs 动态后缀
    │   ├── 缓存断点设置
    │   └── 价格机制
    └── 实战优化
        ├── 缓存命中率优化
        ├── 最佳实践
        └── 失效场景规避
```

## 核心概念关联

| 概念 | 说明 | 关联 |
|------|------|------|
| Cache Hit | 数据在缓存中找到 | → 降低延迟，节省成本 |
| Cache Miss | 数据不在缓存中 | → 需要重新计算或访问慢速存储 |
| KV Cache | 保存 Key-Value 向量 | → 避免重复注意力计算 |
| Prompt Caching | 缓存提示词前缀 | → 降低 Token 成本 |
| Hit Rate | 命中率 = 命中数 / 总请求数 | → 衡量缓存效率 |

## 关键公式

- **总 Token 数** = `cache_read + cache_creation + input_tokens`
- **命中率** = `命中次数 / 总请求次数`
- **复杂度节省** (KV Cache): 从 O(n²) 降至 O(n) 每生成 Token
