# Comet Design Handoff

- Change: token-cost-optimization
- Phase: design
- Mode: compact
- Context hash: c312c233f3be160c957bc2d4264043433580732f157a5b806cddb1ba1ec5d2d4

Generated-by: comet-handoff.sh

OpenSpec remains the canonical capability spec. This handoff is a deterministic, source-traceable context pack, not an agent-authored summary.

## openspec/changes/token-cost-optimization/proposal.md

- Source: openspec/changes/token-cost-optimization/proposal.md
- Lines: 1-65
- SHA256: 8c0f20661c0bad01be55daf7686cafcf6d8a433ad3e1e7dcb30154f3cf7894d1

```md
## Why

Subagent 中的串行工具调用（WebFetch ×20+、Read ×23）导致 Token 消耗呈二次增长（N(N+1)/2），每次笔记生成消耗 200K+ Token。失败请求还会击穿 Prompt Cache，导致全额重算。根本原因：确定性 I/O 操作（抓取网页、读取文件）被交给 LLM Agent 串行执行，而这些操作本不需要推理能力。

## What Changes

- **新增 `scripts/batch_fetch.py`**：并发网页抓取脚本，支持重试、超时、HTML→Markdown 转换、失败报告
- **新增 `scripts/merge_sources.py`**：多文件合并脚本，将 N 个 curated 文件合并为 1 个带分隔标记的文件
- **修改 collector subagent**：用 `batch_fetch.py` 替代串行 WebFetch 调用，Agent 只做搜索+评分
- **修改 writer subagent**：用 `merge_sources.py` 替代串行 Read，Agent 只读 1 个合并文件
- **修改 curator subagent**：用 `merge_sources.py` 替代串行 Read raw 文件
- **修改 collect skill**：在 dispatch collector 时传递脚本路径参数

## Capabilities

### New Capabilities
- `batch-io`: 批量 I/O 脚本层——并发抓取、文件合并、错误处理、结果报告

### Modified Capabilities
- `subagent-orchestration`: subagent 不再串行调用 WebFetch/Read，改为调用脚本层完成确定性 I/O

## 维护与错误处理

### 脚本维护
- 脚本放在 `scripts/` 目录，跟随项目 git 版本控制
- Python 依赖通过 `requirements.txt` 管理（aiohttp、readability-lxml 等）
- 脚本可独立测试（不依赖 LLM），写单元测试即可验证核心逻辑

### 运行时错误处理
- 脚本失败时返回非零退出码 + JSON 错误报告（写入 `{topic}/fetch-report.json`）
- 脚本内置重试机制（指数退避，最多 3 次），大部分网络错误自动恢复
- 部分 URL 失败时，用成功的结果继续流程，失败的记录到 metadata.yaml
- 脚本不存在或 Python 不可用时，自动回退到原有 Agent 串行方式

### Agent 自修复策略
脚本失败时，Agent 按以下分级处理：

| 错误级别 | 示例 | Agent 行为 |
|---------|------|-----------|
| L1: 环境问题 | Python 不存在、依赖缺失 | 提示用户安装，不修改脚本 |
| L2: 脚本 bug | 语法错误、API 变更、逻辑错误 | Agent 读取错误报告 + 脚本源码，诊断并修复，然后重试 |
| L3: 外部问题 | 网站反爬、403/504、超时 | 记录失败，跳过该 URL，用其余结果继续 |
| L4: 脚本不存在 | 首次运行或文件被删 | Agent 根据 specs 创建脚本，然后执行 |

L2 修复流程：
1. Agent 读取 `fetch-report.json` 中的错误信息
2. Agent 读取 `scripts/batch_fetch.py` 源码
3. Agent 定位问题并修复（Edit 工具）
4. 重试脚本
5. 如果修复后仍失败，降级到原有方式并提示用户

L4 创建流程：
1. Agent 检查 `scripts/` 目录下目标脚本是否存在
2. 不存在 → Agent 根据 `openspec/specs/batch-io/spec.md` 中的接口规范创建脚本
3. 安装缺失的 Python 依赖（`pip install -r scripts/requirements.txt`）
4. 执行脚本

## Impact

- **Agent 定义文件**：`.claude/agents/collector.md`、`writer.md`、`curator.md`
- **Skill 文件**：`.claude/skills/collect/SKILL.md`
- **新增脚本**：`scripts/batch_fetch.py`、`scripts/merge_sources.py`、`scripts/requirements.txt`
- **依赖**：Python 3.8+、aiohttp（并发抓取）、readability-lxml/html2text（HTML 清洗）
- **Token 消耗**：预计从 ~200K/次 降至 ~35K/次（节省 ~80%）
- **向后兼容**：脚本层为新增，不破坏现有流程；subagent 修改为内部行为变更；脚本失败时自动降级
```

## openspec/changes/token-cost-optimization/design.md

- Source: openspec/changes/token-cost-optimization/design.md
- Lines: 1-74
- SHA256: bc898fccddf1ac40729ba9e9301c41fbcedc0d5827c04c7fc8bd78f6f7a2e87a

```md
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
```

## openspec/changes/token-cost-optimization/tasks.md

- Source: openspec/changes/token-cost-optimization/tasks.md
- Lines: 1-22
- SHA256: c3849c60446fa18f3d6c0ab43abf47cab82869116c3882a99e2214b6855748ed

```md
# Tasks

## Phase 1: 脚本层

- [ ] 创建 `scripts/batch_fetch.py` — 并发网页抓取脚本
- [ ] 创建 `scripts/merge_sources.py` — 多文件合并脚本
- [ ] 创建 `scripts/requirements.txt` — Python 依赖清单
- [ ] 编写脚本单元测试

## Phase 2: Subagent 修改

- [ ] 修改 `.claude/agents/collector.md` — 用 batch_fetch.py 替代串行 WebFetch
- [ ] 修改 `.claude/agents/writer.md` — 用 merge_sources.py 替代串行 Read
- [ ] 修改 `.claude/agents/curator.md` — 用 merge_sources.py 替代串行 Read
- [ ] 修改 `.claude/skills/collect/SKILL.md` — 传递脚本路径参数

## Phase 3: 验证

- [ ] 端到端测试：收集阶段 Token 消耗对比
- [ ] 端到端测试：写作阶段 Token 消耗对比
- [ ] 错误处理测试：脚本失败降级
- [ ] 错误处理测试：Agent 自修复 L2/L4
```

