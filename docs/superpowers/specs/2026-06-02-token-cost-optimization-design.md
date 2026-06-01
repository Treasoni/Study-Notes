---
comet_change: token-cost-optimization
role: technical-design
canonical_spec: openspec
archived-with: 2026-06-02-token-cost-optimization
status: final
---

# Token Cost Optimization — Design Doc

## Problem

Subagent 中的串行工具调用（WebFetch ×20+、Read ×23）导致 Token 消耗呈二次增长。每次笔记生成消耗 ~200K Token。根本原因：确定性 I/O 操作被交给 LLM Agent 串行执行。

## Solution

新增 Python 脚本层，将确定性 I/O 操作下沉到脚本，Agent 只做需要推理的工作。

```
┌─────────────────────────────────────────────────────┐
│                  Main Agent (PM)                     │
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
└─────────────────────────────────────────────────────┘
```

## Architecture Decision

**选择：独立脚本 + Agent 调用（方案 A）**

- 脚本独立可测试，不依赖 LLM 环境
- Agent 只需读退出码和报告，Token 消耗极低
- 失败时 Agent 可读脚本源码自修复

## batch_fetch.py 设计

### 接口

**输入**：`urls.json`（Agent 写入）
```json
{
  "output_dir": "0-inbox/topic/raw",
  "urls": [
    {"url": "https://...", "title": "...", "index": 1}
  ],
  "concurrency": 5,
  "timeout": 30,
  "cache_file": ".fetch-cache.json"
}
```

**输出**：
- `raw/doc-NN.md`：每个文件带 YAML frontmatter（source_url, title, fetched_at, status）
- `fetch-report.json`：成功/失败/缓存统计

**退出码**：0=全部成功, 1=部分失败, 2=脚本错误

### 核心流程

1. 读取 urls.json
2. 检查缓存，跳过已抓取的 URL
3. asyncio 并发抓取（aiohttp）
4. HTML → Markdown（readability-lxml + html2text）
5. 写入 doc-NN.md + 更新缓存
6. 生成 fetch-report.json
7. 输出退出码

### 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| concurrency | 5 | 并发抓取数 |
| timeout | 30 | 单个 URL 超时（秒） |
| max_retries | 3 | 最大重试次数 |
| retry_base_delay | 1 | 重试基础延迟（秒） |

## merge_sources.py 设计

### 接口

**输入**：命令行参数
```bash
python merge_sources.py \
  --input-dir 0-inbox/topic/raw \
  --output merged-sources.md \
  --format html-comment
```

**输出**：`merged-sources.md`，用 HTML 注释分隔每个源文件
```markdown
<!-- SOURCE: doc-01.md | url: https://... | score: 4.2 -->
[内容]
<!-- END: doc-01.md -->

<!-- SOURCE: doc-02.md | url: https://... | score: 3.8 -->
[内容]
<!-- END: doc-02.md -->
```

**退出码**：0=成功, 1=无文件, 2=脚本错误

### 特殊处理

- 跳过空文件
- 跳过 status: failed 的 doc-NN.md
- input-dir 不存在时退出码 1 + 空输出

## Subagent 行为变更

### Collector Subagent

**旧流程**：WebSearch ×5 → WebFetch ×20 → 评分 → 写入
**新流程**：
1. WebSearch ×5（保留，需要推理）
2. 写入 urls.json
3. 检查 Python + 脚本存在性
   - 通过 → `Bash: python scripts/batch_fetch.py --input-file urls.json --output-dir raw/`
   - 失败 → 回退到 WebFetch ×N
4. 读取 fetch-report.json（1 次 Read）
5. 评分+去重+分类（基于 URL 列表+报告）
6. 写入 metadata.yaml

**效果**：工具调用 ~26→10 次（↓62%），Token ~170K→25K（↓85%）

### Writer Subagent

**旧流程**：Read ×4 curated → Read template → 写作
**新流程**：
1. 检查脚本可用性
   - 通过 → `Bash: merge_sources.py --input-dir curated/ --output merged.md`
   - 失败 → 回退到 Read ×4
2. Read merged-sources.md（1 次）
3. Read template（1 次）
4. 写作

**效果**：工具调用 5→3 次（↓40%），Token ~25K→17K（↓32%）

### Curator Subagent

**旧流程**：Read raw/*.md ×N → 评分 → 分类
**新流程**：
1. 检查脚本可用性
   - 通过 → `Bash: merge_sources.py 合并 raw/ → merged.md`
   - 失败 → 回退到 Read ×N
2. Read merged-sources.md（1 次）
3. 评分+分类+去重
4. 写入 curated/

**效果**：工具调用 N+1→5 次

## Agent 自修复策略

| 错误级别 | 示例 | Agent 行为 |
|---------|------|-----------|
| L1: 环境问题 | Python 不存在、依赖缺失 | 提示用户安装 |
| L2: 脚本 bug | 语法错误、API 变更 | Agent 读源码+报告，诊断修复，重试 |
| L3: 外部问题 | 403/504、超时 | 记录失败，跳过，用其余结果继续 |
| L4: 脚本不存在 | 首次运行或文件被删 | Agent 根据 spec 创建脚本 |

**L2 修复流程**：
1. 读取 fetch-report.json 错误信息
2. 读取脚本源码
3. 诊断并修复（Edit 工具）
4. 重试
5. 仍失败 → 降级到原有方式 + 提示用户

**L4 创建流程**：
1. 检查脚本是否存在
2. 不存在 → 根据 `openspec/specs/batch-io/spec.md` 接口规范创建
3. 安装依赖 `pip install -r scripts/requirements.txt`
4. 执行

## 降级策略

- 脚本失败时自动回退到原有 Agent 串行方式
- 保证向后兼容
- Agent 检测顺序：先检查环境 → 再检查脚本 → 最后执行

## 依赖

- Python 3.8+
- aiohttp（并发抓取）
- readability-lxml（HTML 清洗）
- html2text（HTML→Markdown）

## Data Flow

### 收集阶段
```
Agent WebSearch → URL 列表
    ↓
batch_fetch.py (并发抓取)
    ↓
raw/doc-NN.md + fetch-report.json
    ↓
Agent 评分+去重+分类 (读报告，不读全文)
```

### 写作阶段
```
merge_sources.py (合并 curated 文件)
    ↓
merged-sources.md (带 HTML 注释分隔)
    ↓
Agent 读 1 个合并文件 + 模板 → 撰写笔记
```

## Testing Strategy

### 单元测试（不依赖 LLM）
- `test_batch_fetch.py`：并发抓取、缓存、HTML 转换、重试、退出码
- `test_merge_sources.py`：多文件合并、分隔标记、空文件处理、退出码

### 集成测试（需要网络）
- 真实 URL 抓取
- 缓存命中
- 部分失败场景

### 端到端测试（需要 LLM）
- 收集阶段 Token 消耗对比
- 写作阶段 Token 消耗对比
- 脚本失败降级测试
