---
name: research-collector
description: 使用多策略进行高效资料收集：Fork Subagent 隔离收集、两阶段粗筛+精读、格式约束优化 token 消耗、本地缓存复用。触发词：收集资料、研究资料、搜集信息、资料整理、research、gather information、collect资料。
---

# Research Collector - 高效资料收集器

使用多种策略进行高效资料收集，优化 token 消耗并支持本地缓存复用。

## 前置依赖（一次性安装）

Phase 2 精读主路径依赖 **Crawl4AI**（渲染 JS 动态页面、输出干净 Markdown、批量并发、本地缓存）。使用前需先安装一次环境：

```bash
bash .claude/skills/research-collector/scripts/setup.sh
```

脚本会创建 conda env `crawl4ai`（python 3.12），安装 `crawl4ai` 与 Playwright Chromium（约 150MB），可重复执行、幂等。

> 若未安装或 `crawl.sh` 失败，精读自动回退到 **WebFetch** 深读，功能不中断。

## 触发条件

当用户提出以下类型的请求时，调用此技能:

- "帮我收集关于 XX 的资料"
- "搜集 XX 领域的信息"
- "研究 XX 主题"
- "XX 相关的资料有哪些"
- "帮我调研 XX"
- 任何涉及批量搜索、系统性资料收集的请求

## 核心策略

### 策略 1: Fork Subagent 隔离收集

**原理**: 主 Agent 派发多个 fork subagent 并行搜索不同关键词/信源，每个 subagent 只返回结构化摘要，避免原始网页全文污染主上下文。

**实现**:
```
主 Agent
  ├── Fork Subagent 1: 搜索 "关键词 A + 来源1"
  ├── Fork Subagent 2: 搜索 "关键词 B + 来源2"
  ├── Fork Subagent 3: 搜索 "关键词 C + 来源3"
  └── ...
       ↓
  每个 Subagent 返回：结构化摘要（<150 字）
       ↓
  主 Agent 聚合：提炼后的结果
```

**优势**:
- Token 消耗极低：每个 subagent 独立上下文，不共享原始内容
- 并行执行：多路搜索同时进行
- 隔离安全：一个 subagent 失败不影响其他

### 策略 2: 两阶段收集法

**第一阶段: 批量粗筛**
- 并行搜索多个关键词
- 每个结果只返回：标题 + URL + 一句话摘要 + 相关性评分 (1-5)
- 目标：快速发现候选资料

**第二阶段: 定向精读**
- 主 Agent 根据评分筛选 3-5 篇核心资料
- **主路径（Crawl4AI）**：批量跑 `crawl.sh` 并发抓取，输出干净 Markdown 到 `--output-dir`，再读取生成的 `.md` 提取内容
- **回退路径（WebFetch）**：`crawl.sh` 失败（未安装 / 网络失败 / 反爬拦截）时，改用 `WebFetch` 定向深读
- 提取：核心观点、关键数据、引用来源
- 目标：获取高质量详细内容

### 策略 3: 强制输出格式约束

给 subagent 的 prompt 中严格限定输出格式，避免冗余:

```markdown
## 返回格式（严格遵守）

每条资料格式：
- **标题**: [文章标题]
- **URL**: [链接]
- **摘要**: [核心观点，不超过 150 字]
- **相关性评分**: [1-5，5 为高度相关]
- **关键数据**: [如有，列出 1-3 个关键数据点]
- **来源类型**: [官方文档/技术博客/学术论文/社区讨论/新闻报道]

禁止返回:
- ❌ 完整段落
- ❌ 页面导航信息
- ❌ 广告内容
- ❌ Cookie 提示
- ❌ 无关的侧边栏内容
```

### 策略 4: 本地缓存复用

**缓存目录**: `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/`（项目专属文件夹）

**文件命名**: `02_deep_research.md`（固定命名，供下游组件读取）

**缓存结构**:
```markdown
# {主题} - 资料收集

收集时间: YYYY-MM-DD HH:MM
搜索关键词: [关键词列表]

## 第一阶段: 粗筛结果

| # | 标题 | URL | 相关性 | 摘要 |
|---|------|-----|--------|------|
| 1 | ... | ... | 5/5 | ... |

## 第二阶段: 精读笔记

### 资料 1: {标题}
- **URL**: ...
- **核心观点**: ...
- **关键数据**: ...
- **我的笔记**: ...

## 综合分析

[总结关键发现、趋势、共识与分歧]
```

## 工作流程

### Step 0: 读取 workflow state file（必须执行）

**启动时必须确定当前命名 workflow state file 并读取它：**

```bash
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"
WORKFLOW_STATE_FILE="${WORKFLOW_STATE_FILE:-${RUN_STATE_FILE:-}}"

if [ -z "$WORKFLOW_STATE_FILE" ]; then
  echo "请提供 WORKFLOW_STATE_FILE，路径应位于 workspace/workflow-runs/*.workflow.md"
  exit 1
fi

if [ ! -f "$WORKFLOW_STATE_FILE" ]; then
  echo "workflow state file 不存在：$WORKFLOW_STATE_FILE"
  exit 1
fi

cat "$WORKFLOW_STATE_FILE"

PROJECT_SLUG="$(awk -F': *' '/^project_slug:/ {gsub(/^"|"$/, "", $2); print $2; exit}' "$WORKFLOW_STATE_FILE")"
PROJECT_DIR="${WORKSPACE_PATH}/${PROJECT_SLUG}"
```

**状态检查：**
- 如果 workflow state file 不存在：提示用户先运行 `/research-planner` 创建运行状态文件。
- 如果阶段 0 未 `✅ 已完成`：提示用户先完成 `/research-planner`。
- 如果阶段 1 为 `⬜ 未开始`：允许执行探测式收集，并用状态脚本启动 P1。
- 如果阶段 1 已 `✅ 已完成` 且阶段 2 为 `⬜ 未开始`：允许执行深度收集，并用状态脚本启动 P2。

**更新 workflow state：**
```bash
# 将当前阶段标记为进行中（根据实际执行的阶段选择 [P1] 或 [P2]）
# 阶段 1（探测式收集）：
.claude/scripts/todo-state.sh "$WORKFLOW_STATE_FILE" start P1
# 阶段 2（深度收集）：
.claude/scripts/todo-state.sh "$WORKFLOW_STATE_FILE" start P2
```

**完成后更新状态：**
```bash
# 将当前阶段标记为完成（根据实际执行的阶段选择 [P1] 或 [P2]）
# 阶段 1 完成：
.claude/scripts/todo-state.sh "$WORKFLOW_STATE_FILE" complete P1
# 阶段 2 完成：
.claude/scripts/todo-state.sh "$WORKFLOW_STATE_FILE" complete P2
```

---

### Step 1: 理解需求

1. 识别用户的**研究主题**
2. 确定**搜索关键词** (3-5 个不同角度)
3. 选择**信源偏好** (官方文档/博客/论文/社区)
4. 确认**输出格式**要求

### Step 2: 两阶段并行收集

**Phase 1: 粗筛 (并行)**

使用 `Agent` 工具创建多个 subagent，每个负责不同搜索维度:

```
Subagent 1: 搜索 "{关键词1} site:官方文档"
Subagent 2: 搜索 "{关键词2} 最佳实践"
Subagent 3: 搜索 "{关键词3} 教程 入门"
Subagent 4: 搜索 "{关键词4} 常见问题 问题排查"
```

每个 subagent 的 prompt 模板:
```
你是一个资料收集助手。只返回关于指定主题的结构化资料摘要。

返回格式（严格遵守，每条不超过 150 字）:
1. **标题**: ...
   **URL**: ...
   **摘要**: [核心观点，150 字内]
   **相关性评分**: [1-5]
   **关键数据**: [1-3 个]
   **来源类型**: [官方文档/博客/论文/社区/新闻]

禁止返回: 完整段落、导航、广告、Cookie 提示。

请搜索并返回 3-5 条最相关的资料。

参数：
- 主题: {主题}
- 搜索关键词: {关键词}
- 信源限制: {信源类型}
```

**Phase 2: 精读 (按需)**

从粗筛结果中筛选评分 ≥4 的 3-5 篇核心资料，**优先用 Crawl4AI 批量并发抓取**：

```bash
# 1) 主路径：Crawl4AI 批量精读（渲染 JS、输出干净 Markdown，默认重抓并刷新缓存）
CRAWL_DIR="${PROJECT_DIR:-${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG:-.}}/deep_read"
bash .claude/skills/research-collector/scripts/crawl.sh \
  --url "<URL1>" --url "<URL2>" --url "<URL3>" \
  --output-dir "$CRAWL_DIR"
# 可选 --cache：复用本地缓存（crawl4ai 0.9.x 缓存只存 raw，命中可能含导航噪声）

# 2) 每篇 .md 带 YAML frontmatter（url / title / scraped_at）用于溯源；
#    正文在 `---` 之后，读取时跳过 frontmatter。

# 3) 用 fork subagent 逐篇提炼——主 agent 不读全文，保持上下文干净：
#    每个 .md 派一个 subagent，读文件 → 返回结构化摘要（≤150 字）。
```

**Subagent 提炼模板**（每篇 .md 一个，隔离上下文）：
```
你是一个精读助手。读取文件 {DEEP_READ_FILE}（跳过开头的 YAML frontmatter，只读正文），
按以下格式返回结构化摘要（每条 ≤150 字）：
- **标题**: ...
- **URL**: {frontmatter 里的 url}
- **核心观点**: ...
- **关键数据**: [1-3 个]
- **主要结论**: ...
- **我的笔记**: ...
禁止返回: 完整段落、导航、广告、侧边栏。
```

> **回退到 WebFetch（按退出码区分）**：
> - `crawl.sh` **exit 2**（参数 / 环境问题，含「请先运行 setup.sh」）→ 先执行 `bash .claude/skills/research-collector/scripts/setup.sh` 再重试；仍失败则全部改用 WebFetch。
> - **exit 1**（部分 URL 失败）→ 从 stderr 的 `[失败]` 行取出失败 URL，**只对失败项**用 WebFetch 补读，已成功的 `.md` 保留。
> - 正文为空（可能反爬拦截）同样视为失败项，用 WebFetch 补读。
> ```
> WebFetch 深读（仅失败的 URL）:
> - URL: {失败的 URL}
> - Prompt: "提取文章的核心观点、关键数据、主要结论。忽略广告、导航、侧边栏。"
> ```

**注意**：
- 把精读素材作为背景，正文仍按 ≤150 字摘要约束回写 `02_deep_research.md`，不要整篇搬运。
- Crawl4AI 0.9.x 缓存只保存 raw markdown；默认总是重抓（WRITE_ONLY），产出干净 fit 正文。显式加 `--cache` 复用缓存时，命中输出可能含少量导航噪声。

### Step 3: 结果整合

1. 聚合所有 subagent 返回的结构化摘要
2. 按相关性评分排序
3. 对高评分资料进行精读
4. 生成综合分析

### Step 4: 缓存写入

将结果写入本地文件:
```
${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/02_deep_research.md
```

**注意**: 使用固定文件名 `02_deep_research.md`，方便下游组件（outline-generator、chapter-writer）直接读取。

**更新 workflow state：**
```bash
# 将当前阶段标记为完成，推进到下一阶段
.claude/scripts/todo-state.sh "$WORKFLOW_STATE_FILE" complete P2
```

## 输出示例

```
## 📚 资料收集完成

### 第一阶段: 粗筛结果 (共发现 12 条)

| # | 标题 | 评分 | 来源 |
|---|------|------|------|
| 1 | React 18 新特性详解 | 5/5 | 官方文档 |
| 2 | React 并发模式最佳实践 | 4/5 | 技术博客 |
| 3 | React 18 迁移指南 | 4/5 | 官方博客 |
| ... | ... | ... | ... |

### 第二阶段: 精读笔记

#### 1. React 18 新特性详解 (官方文档)
- **核心观点**: React 18 引入并发渲染、自动批处理、Suspense 改进
- **关键数据**:
  - 性能提升 2-3 倍 (复杂应用)
  - 自动批处理减少 60% 渲染次数
- **我的笔记**: [根据精读内容生成]

### 综合分析

[总结关键发现、最佳实践、常见问题]

---
✅ 资料已缓存到: ${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/02_deep_research.md
```

## 高级用法

### 1. 递归深入收集

```bash
# 第一轮: 宏观了解
/research-collector "React 状态管理"

# 第二轮: 针对特定工具深入
/research-collector "Zustand vs Jotai vs Redux Toolkit 对比"

# 第三轮: 实战案例
/research-collector "React 状态管理 项目实战 最佳实践"
```

### 2. 多维度并行

同时从多个维度收集:
- **维度 1**: 官方文档 (权威性)
- **维度 2**: 技术博客 (实践经验)
- **维度 3**: GitHub Issues (常见问题)
- **维度 4**: Stack Overflow (社区解答)

### 3. 缓存复用

```bash
# 检查是否已有相关缓存
ls research_notes/*react*

# 读取已有缓存
cat research_notes/react-2025-01-15.md

# 基于缓存补充收集
/research-collector "React 性能优化" (补充之前未覆盖的方面)
```

## 注意事项

1. **相关性评分**: 严格按 1-5 评分，避免所有资料都标高分
2. **摘要字数**: 每条摘要控制在 150 字内，超长会截断
3. **缓存命名**: 使用有意义的文件名，便于后续查找
4. **并行限制**: 同时最多 5 个 subagent，避免过载
5. **源质量**: 优先官方文档 > 技术博客 > 社区讨论 > 新闻报道
6. **时效性**: 标注资料发布日期，优先选择近 2 年的内容
