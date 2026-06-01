---
name: collect
description: 收集并整理学习资料阶段（Phase 1+2 合并）。读取工具注册表选择搜索/抓取工具，与用户讨论收集范围，调度 collector subagent 搜索、抓取、评分、去重、分类，输出整理后的资料和 metadata.yaml。触发时机：用户确认学习计划后，Phase 1。
---

# Skill: collect（收集并整理资料）

## 触发时机

用户确认学习计划后。

## 输入

- `topic`: 学习主题
- `direction`: 概念理解 / 实战上手 / 体系梳理 / 问题排查
- `depth`: 入门 / 进阶 / 深入原理
- `SYSTEM_ROOT`: 系统根目录

## 执行模型

本 skill 合并了原 Phase 1（collect）和 Phase 2（curate）的职责，一次调度完成收集与整理。

```
主 Agent (PM)                    Collector Subagent (专员)
    │                                  │
    ├─ 读取工具注册表                   │
    ├─ 讨论收集范围（阻塞）             │
    ├─ 动态选择工具                     │
    ├─ 调度收集+整理 ─────────────────►│
    │                                  ├─ 搜索官方文档
    │                                  ├─ 抓取内容
    │                                  ├─ 搜索社区
    │                                  ├─ 评分 (1-5)
    │                                  ├─ 去重 & 分类
    │                                  ├─ 删除低质量文件
    │                                  ├─ 写入 metadata.yaml
    │◄──── 整理结果摘要 ──────────────┤
    │                                  │
    ├─ 展示给用户                      │ (销毁)
```

**核心原则**：主 Agent 不直接执行搜索/抓取/读取原始文件，避免上下文污染。

## 执行步骤

### Step 1: 读取工具注册表

读取 `~/.claude/rules/tool-registry.yaml`，检查是否可用且未过期。

**自动刷新逻辑**：

1. 文件不存在 → 调用 `Skill(skill="tool-registry")` 生成注册表，然后继续
2. `metadata.generated_at` 超过 `metadata.ttl_days`（默认 7 天） → 调用 `Skill(skill="tool-registry")` 刷新，然后继续
3. 文件存在且新鲜 → 直接使用

```powershell
# PowerShell: 检查注册表有效期
$regPath = "$env:USERPROFILE\.claude\rules\tool-registry.yaml"
if (Test-Path $regPath) {
    $content = Get-Content $regPath -Raw
    if ($content -match 'generated_at:\s*"([^"]+)"') {
        $generated = [DateTime]::Parse($Matches[1])
        $age = (Get-Date) - $generated
        if ($age.TotalDays -gt 7) { "STALE" } else { "FRESH" }
    } else { "STALE" }
} else { "MISSING" }
```

从注册表中提取：
- `search_tools`：按 `priority` 升序排列，仅保留 `status: available`
- `fetch_tools`：按 `priority` 升序排列，仅保留 `status: available`

**WebSearch/WebFetch 始终可用**（内置工具），作为兜底方案。

### Step 2: 用户范围讨论（阻塞步骤）

在调度 collector 之前，与用户确认收集范围。这是一个 **阻塞步骤**，必须等待用户回复。

向用户提问（可一次提出，也可分步）：

> 为了高效收集资料，请确认以下范围：
>
> **1. 来源数量**
> - 少量（3-5 篇）：快速概览
> - 中等（8-12 篇）：标准调研 ← 推荐
> - 大量（15+ 篇）：深度调研
>
> **2. 来源类型**（可多选）
> - 官方文档
> - 博客/教程
> - 视频教程
> - 社区讨论（StackOverflow / V2EX 等）
>
> **3. 收集深度**
> - 快速概览：只抓核心文档和入门教程
> - 标准调研：覆盖核心概念 + 常见实践 + 已知坑点 ← 推荐
> - 深度调研：全面覆盖，包括进阶原理和边缘案例

**默认值**（用户说"跳过"或"用默认"时使用）：
- 数量：中等（8-12 篇）
- 类型：官方文档 + 博客/教程
- 深度：标准调研

记录用户选择，传递给 collector subagent。

### Step 3: 动态工具选择

根据 Step 1 的注册表和 Step 2 的用户范围，选择工具组合：

**搜索工具选择**：
1. 从 `search_tools` 中按 `priority` 升序选取
2. 优先选择 `capabilities` 包含 `general_search` 或 `web_search` 的工具
3. 如果用户选择了"视频教程"类型，优先选择 `capabilities` 包含视频搜索的工具
4. 记录最终选择的搜索工具名列表

**抓取工具选择**：
1. 从 `fetch_tools` 中按 `priority` 升序选取
2. 优先选择 `capabilities` 包含 `content_extraction` 的工具
3. 记录最终选择的抓取工具名列表

**兜底策略**：
- 如果注册表中没有可用的搜索工具 → 使用 WebSearch
- 如果注册表中没有可用的抓取工具 → 使用 WebFetch
- 如果首选工具在 collector 执行中失败 → collector 自动降级到下一优先级工具

将选定的工具列表传递给 collector。

### Step 4: 调度 Collector Subagent

> **路径传递**：collect 是第一个 phase，无上游路径。完成后应在 TODO.md 中记录 output 路径供后续 phase 使用。

使用 Agent 工具调度 collector subagent，传入结构化信息：

```typescript
Agent({
  subagent_type: "collector",
  prompt: `
Topic: {topic}
Direction: {direction}
Depth: {depth}
Search Tools: {逗号分隔的搜索工具列表，按优先级排列}
Fetch Tools: {逗号分隔的抓取工具列表，按优先级排列}
Source Scope:
  Count: {few|medium|many}
  Types: {technical_docs|blog_posts|videos|forum_discussions}
  Research Depth: {quick|standard|deep}
Output Dir: {SYSTEM_ROOT}/0-inbox/{topic}/
Script Context:
  Batch Fetch: scripts/batch_fetch.py
  Merge Sources: scripts/merge_sources.py
  Requirements: scripts/requirements.txt
  `,
  label: `collect:${topic}`,
  phase: "Phase 1: Collect + Curate"
})
```

Collector subagent 执行以下工作（在 subagent 内部完成）：

#### 4a. 搜索与抓取

根据传入的工具和范围参数：
- 使用选定的搜索工具搜索官方文档和社区内容
- 使用选定的抓取工具抓取页面内容
- 保存原始文件到 `{SYSTEM_ROOT}/0-inbox/{topic}/raw/`
- 创建 `sources.md` 记录所有来源元数据

#### 4b. 评分（内联 curate 逻辑）

对每个收集到的文件进行四维度评分。评分标准见 `.claude/agents/collector.md` Step 2。

**综合得分** = 四个维度的平均值（四舍五入到一位小数）。

#### 4c. 去重

- 比较文件标题和内容摘要
- 如果两个文件覆盖相同内容且角度相似，标记得分较低的为重复
- 重复文件不删除，但在 metadata.yaml 中标记 `duplicate_of: "doc-NN.md"`

#### 4d. 分类

将每个文件分类到以下类别之一：

| 类别 | 说明 | 典型内容 |
|------|------|----------|
| `core_concepts` | 核心概念和基础知识 | 官方文档、入门教程、概念解释 |
| `practical_examples` | 实战示例和最佳实践 | 代码示例、实战教程、经验分享 |
| `advanced` | 进阶原理和深度分析 | 架构设计、源码分析、性能优化 |

#### 4e. 清理低质量文件

- 综合得分 < 3 的文件：从 `raw/` 目录中删除
- 综合得分 >= 3 的文件：保留在 `raw/` 目录中，等待主 Agent 后续使用

#### 4f. 生成 metadata.yaml

写入 `{SYSTEM_ROOT}/0-inbox/{topic}/metadata.yaml`：

```yaml
topic: "{topic}"
collected_at: "{ISO 8601 timestamp}"
scope:
  count: {few|medium|many}
  types: [{selected types}]
  research_depth: {quick|standard|deep}
tools_used:
  search: "{tool_name}"
  fetch: "{tool_name}"
  fallback_used: {true|false}

files:
  - filename: "doc-01.md"
    title: "{title}"
    url: "{source_url}"
    authority: 5
    freshness: 4
    completeness: 4
    readability: 5
    score: 4.5
    classification: core_concepts
    duplicate_of: null

  - filename: "doc-02.md"
    title: "{title}"
    url: "{source_url}"
    authority: 3
    freshness: 3
    completeness: 2
    readability: 3
    score: 2.8
    classification: practical_examples
    duplicate_of: null
    removed: true  # 低于阈值 3，已删除

summary:
  total_collected: {N}
  total_kept: {N}
  total_removed: {N}
  by_classification:
    core_concepts: {N}
    practical_examples: {N}
    advanced: {N}
  by_authority:
    official_docs: {N}
    tech_blogs: {N}
    community: {N}
    videos: {N}
  gaps: ["{gap1}", "{gap2}"]
```

### Step 5: 展示结果

collector subagent 返回精简摘要后，向用户展示：

- **收集统计**：收集了 X 篇，保留 Y 篇，删除 Z 篇（低于质量阈值）
- **分类概览**：核心概念 X 篇 / 实战示例 X 篇 / 进阶 X 篇
- **来源类型分布**：官方文档 X / 博客 X / 视频 X / 社区 X
- **覆盖的子主题**
- **明显缺口**：哪些方面缺乏足够资料
- **使用的工具**：搜索用 {tool}，抓取用 {tool}（是否使用了兜底方案）

### Step 6: 硬停止

**严禁进入 Phase 2。Phase 2 已合并到本 skill 中。**
必须等待用户明确确认（"继续" / "进入下一阶段" / "开始写笔记"）后才能进入 write。

## 输出目录结构

```
{SYSTEM_ROOT}/0-inbox/{topic}/
├── raw/                  # 保留的原始文件（得分 >= 3）
│   ├── doc-01.md
│   ├── doc-02.md
│   └── ...
├── sources.md            # 来源元数据表
└── metadata.yaml         # 评分、分类、统计信息
```

## 禁止行为

- 主 Agent 不要直接执行搜索/抓取命令（交给 collector）
- 不要跳过用户范围讨论直接开始收集
- 不要跳过 subagent 调度直接手动收集
- 不要编造 URL 或来源信息
- 不要硬编码工具名称 — 始终从注册表读取
- 不要跳过评分/去重/分类步骤
- 不要在展示结果前自动进入下一阶段
