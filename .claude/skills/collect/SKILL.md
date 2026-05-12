---
name: collect
description: 收集学习资料阶段。根据用户的学习主题，使用 opencli 适配器搜索官方文档和社区内容，抓取并保存原始资料。触发时机：用户确认学习计划后，Phase 1。
---

# Skill: collect（收集资料）

## 触发时机
用户确认学习计划后。

## 输入
- `topic`: 学习主题
- `direction`: 概念理解 / 实战上手 / 体系梳理 / 问题排查
- `depth`: 入门 / 进阶 / 深入原理

## 前置：确认可用适配器

每次执行前先运行 `opencli list -f json` 确认当前可用的搜索源，以下为常用源（以 live registry 为准）：

### 搜索源
| 站点 | 用途 | 命令示例 |
|------|------|----------|
| `google` | 通用搜索 | `opencli google search "<query>" -f json` |
| `github` | 代码仓库 / 开源项目 | 使用 `mcp__github__search_code` 或 `mcp__github__search_repositories` |
| `mdn` | Web 标准文档 | `opencli mdn search "<query>" -f json` |
| `stackoverflow` | 编程问题 / 报错 | `opencli stackoverflow search "<query>" -f json` |
| `reddit` | 社区讨论 / 经验 | `opencli reddit search "<query>" -f json` |
| `hackernews` | 技术社区讨论 | `opencli hackernews search "<query>" -f json` |
| `medium` | 技术博客 | `opencli medium search "<query>" -f json` |
| `devto` | 开发者社区 | `opencli devto search "<query>" -f json` |
| `arxiv` | 学术论文 | `opencli arxiv search "<query>" -f json` |
| `linux-do` | 中文技术社区 | `opencli linux-do search "<query>" -f json` |
| `v2ex` | 中文技术社区 | `opencli v2ex search "<query>" -f json` |
| `wikipedia` | 概念定义 / 背景 | `opencli wikipedia search "<query>" -f json` |
| `youtube` | 视频教程 | `opencli youtube search "<query>" -f json` |
| `bilibili` | 中文视频教程 | `opencli bilibili search "<query>" -f json` |

### AI 辅助源（三选一）
| 站点 | 适用场景 |
|------|----------|
| `grok` | 英文互联网、Twitter/X 语境、热点追踪 |
| `gemini` | 全球网页、英文资料、背景综述 |
| `doubao` | 中文语境、中文热点与问答 |

### 内容抓取
| 工具 | 用途 |
|------|------|
| `defuddle parse <url> --md` | 提取网页正文 Markdown，去广告去导航 |
| `opencli web read --url <url>` | 备选方案，一次性的页面 Markdown 读取 |

## 执行步骤

### Step 1: 搜索官方文档

1. `opencli google search "{topic} official documentation" -f json`
2. `opencli google search "{topic} official guide tutorial" -f json`

根据 depth 调整搜索词：
- 入门: `{topic} getting started tutorial`
- 进阶: `{topic} advanced guide best practices`
- 深入原理: `{topic} deep dive internals architecture`

锁定官方文档入口 URL（从搜索结果中提取）。

### Step 2: 抓取官方文档

用 `defuddle parse` 抓取官方文档关键页面，保存为 `raw/doc-NN.md`。

至少覆盖：
- 概览 / 介绍页
- 入门 / Quick Start 页
- 核心概念页

```bash
defuddle parse "<url>" --md -o "{SYSTEM_ROOT}/0-inbox/{topic}/raw/doc-01.md"
```

### Step 3: 搜索社区内容

根据主题类型选择合适的源。每次搜索前先运行 `<site> -h` 确认参数：

**技术类主题**：
```bash
# 近期教程
opencli google search "{topic} tutorial 2025 2026" -f json
# GitHub 项目
github__search_repositories({query: "{topic} stars:>100"})
# 最佳实践
opencli google search "{topic} best practices" -f json
# 常见陷阱
opencli google search "{topic} common pitfalls mistakes" -f json
# 深度解析
opencli google search "{topic} deep dive advanced guide" -f json
# 社区问答（中英文各一）
opencli stackoverflow search "{topic}" -f json
opencli v2ex search "{topic}" -f json
```

**非技术类主题**：用 `smart-search` skill 路由到合适的专用源。

**视频内容**（实战上手方向优先）：
```bash
opencli youtube search "{topic} tutorial" -f json
opencli bilibili search "{topic} 教程" -f json
```

### Step 4: 过滤

- 优先级：官方文档 > 知名作者 > 社区
- 时效性：优先近 2 年内的内容
- 唯一性：同一内容保留质量最高的来源
- 多样性：保留有独特视角的资料

### Step 5: 保存

对每个入选来源，用 `defuddle parse` 抓取并保存：

```bash
defuddle parse "<url>" --md -o "{SYSTEM_ROOT}/0-inbox/{topic}/raw/doc-NN.md"
```

## 产出

写入 `{SYSTEM_ROOT}/0-inbox/{topic}/`：

### sources.md
```markdown
# Sources for {topic}

| # | Title | URL | Author | Date | Type | Notes |
|---|-------|-----|--------|------|------|-------|
```

### raw/doc-NN.md
```markdown
# {Title}
- **Source**: {URL}
- **Author**: {name}
- **Date**: {date}
- **Type**: {official|blog|tutorial|discussion}

---
{raw content}
```

## 禁止行为
- 不要整理或总结内容（curate 的事）
- 不要评判资料好坏（只记录元数据）
- 不要跳过低热度但有独特视角的资料
- 不要编造 URL 或来源信息
- 不要硬编码 opencli 命令签名 —— 每次执行前通过 `-h` 确认

## 硬停止 (Hard Stop)

本阶段任务完成。向用户展示收集结果摘要（来源数量、覆盖的子主题、明显缺口）。

**严禁调用 `/curate`。严禁进入 Phase 2。**
必须等待用户明确确认（"继续" / "进入下一阶段" / "开始整理"）后才能进入 curate。
