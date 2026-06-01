## Architecture

在现有 subagent 架构上新增脚本层，确定性 I/O 操作下沉到 Python 脚本。

```
┌─────────────────────────────────────────────────────┐
│                  Main Agent (PM)                     │
│  协调阶段流转，不直接执行 I/O                         │
└──────────────┬──────────────────────────────────────┘
               │ dispatch
    ┌──────────┼──────────┬──────────────┐
    ▼          ▼          ▼              ▼
┌────────┐ ┌────────┐ ┌────────┐  ┌────────────┐
│collect │ │curate  │ │writer  │  │beautifier  │
│subagent│ │subagent│ │subagent│  │subagent    │
└───┬────┘ └───┬────┘ └───┬────┘  └────────────┘
    │          │          │
    │ 调用     │ 调用     │ 调用
    ▼          ▼          ▼
┌─────────────────────────────────────────────────────┐
│              脚本层 (Python)                          │
│  batch_fetch.py    merge_sources.py                  │
│  并发抓取+重试      多文件合并+分隔标记                │
└─────────────────────────────────────────────────────┘
```

## Key Decisions

### 1. 脚本语言选择：Python
- asyncio + aiohttp 实现并发抓取
- readability-lxml 做 HTML→Markdown 清洗
- 跨平台兼容（Windows/Linux/macOS）

### 2. 并发策略
- 默认并发数：5（可配置）
- 指数退避重试：最多 3 次
- 单个 URL 超时：30 秒

### 3. 错误处理分级
- L1 环境问题 → 提示用户
- L2 脚本 bug → Agent 自修复
- L3 外部问题 → 跳过+记录
- L4 脚本不存在 → Agent 创建

### 4. 降级策略
- 脚本失败时自动回退到原有 Agent 串行方式
- 保证向后兼容

## Data Flow

### 收集阶段（优化后）
```
Agent WebSearch → URL 列表
    ↓
batch_fetch.py (并发抓取 20 个 URL)
    ↓
raw/doc-01.md ~ doc-20.md + fetch-report.json
    ↓
Agent 评分+去重+分类 (读 URL 列表 + 报告，不读网页全文)
```

### 写作阶段（优化后）
```
merge_sources.py (合并 4 个 curated 文件)
    ↓
merged-sources.md (带分隔标记)
    ↓
Agent 读 1 个合并文件 + 模板 → 撰写笔记
```

## Open Questions

- 是否需要缓存机制（避免重复抓取同一 URL）？
- 合并文件的分隔标记格式用什么？（HTML comment? YAML block?）
