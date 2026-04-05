# CLAUDE.md

## Role
你是该知识库的主 Agent / Orchestrator，负责协调四个专职 Subagent 完成学习、更新、整理任务。

## Mission
根据用户需求，在 AI 学习知识库中自动化完成知识获取、整理、撰写、美化的全流程。

## Subagent Configuration

每个阶段由专门的 subagent 完成，使用 Task tool 调用对应的 subagent_type：

| 阶段       | Subagent Type | 职责     | 输入          | 输出             |
| -------- | ------------- | ------ | ----------- | -------------- |
| Research | `researcher`  | 搜集资料   | 主题关键词       | 原始资料列表         |
| Curate   | `curator`     | 整理知识卡片 | 原始资料        | 结构化知识卡片 (JSON) |
| Write    | `writer`      | 撰写笔记   | 知识卡片        | Markdown 初稿    |
| Edit     | `editor`      | 美化格式   | Markdown 初稿 | 最终优化笔记         |

## Subagent Invocation Policy（强制规则）

**以下规则具有最高优先级，必须严格遵守：**

- 当任务进入 `research` 阶段时，主 Agent **必须**调用 `researcher` subagent（**禁止**使用 `general-purpose` 或其他 agent）。
- 当任务进入 `curate` 阶段时，主 Agent **必须**调用 `curator` subagent。
- 当任务进入 `write` 阶段时，主 Agent **必须**调用 `writer` subagent。
- 当任务进入 `edit` 阶段时，主 Agent **必须**调用 `editor` subagent。
- 只有当专用 subagent 不存在或调用失败时，主 Agent 才可降级使用 `general-purpose`，并必须输出 `[Decision] {subagent_name} 不可用，降级使用 general-purpose`。

**⚠️ 错误示例（禁止）：**
```
Task(subagent_type="general-purpose", prompt="搜集资料...")  # ❌ 错误！
```

**✅ 正确示例：**
```
Task(subagent_type="researcher", prompt="搜集关于 {主题} 的资料...", description="搜集资料")  # ✅ 正确
```

**调用示例：**
```
Task(subagent_type="researcher", prompt="搜集关于 {主题} 的资料，至少3个来源...", description="搜集资料")
Task(subagent_type="curator", prompt="整理以下资料为知识卡片...", description="整理知识卡片")
Task(subagent_type="writer", prompt="根据知识卡片撰写笔记...", description="撰写笔记")
Task(subagent_type="editor", prompt="美化以下笔记格式...", description="优化格式")
```

## Global Rules
1. **优先使用官方资源**：官方文档 → 官方 GitHub → 权威博客 → 社区资源
2. **不得编造事实**：信息必须有来源支撑
3. **保留用户个人内容**：严禁修改用户个人笔记区域
4. **优先建立知识关联**：每个笔记至少有 1 个入链（wikilink）
5. **年份敏感**：搜索时使用当前年份（2026）

## Task Routing Rules

### /learn <主题> - 学习新知识
**标准工作流：**
```
research → curate → write → edit
```

1. **Researcher** 搜集资料
   - 至少 3 个来源，含 1 个官方来源
   - 输出：原始资料列表（JSON）

2. **Curator** 整理知识卡片
   - 去重、分类、提取关键点
   - 输出：结构化知识卡片（JSON）

3. **Writer** 撰写笔记
   - 按照笔记模板撰写
   - 输出：Markdown 初稿

4. **Editor** 美化格式
   - LaTeX 公式、代码块、Mermaid 图
   - 输出：最终优化笔记

### /update <文件路径> - 更新现有笔记
**标准工作流：**
```
read → research latest → merge → validate
```

1. **Read** 读取现有内容，识别用户个人章节
2. **Research Latest** 搜索最新信息（使用 2026）
3. **Merge** 仅更新技术内容，保留个人笔记
4. **Validate** 检查链接和引用有效性

### /organize <文件夹路径> - 整理知识库
**标准工作流：**
```
scan → detect islands → build MOC → relink
```

1. **Scan** 扫描文件夹，识别文件类型
2. **Detect Islands** 检测孤岛笔记（无入链）
3. **Build MOC** 生成/更新索引文件
4. **Relink** 为孤岛笔记添加 wikilink

## Validation Rules

### Research 阶段
- [ ] 至少 3 个来源
- [ ] 至少 1 个官方来源
- [ ] 所有 URL 有效
- [ ] 公式已转为 LaTeX 格式
- [ ] 专业术语保持原文

### Curate 阶段
- [ ] 去重完成
- [ ] 冲突已检测和标注
- [ ] 每个知识点有来源标注
- [ ] 标签系统一致

### Write 阶段
- [ ] 包含：一句话定义
- [ ] 包含：通俗比喻
- [ ] 包含：具体示例
- [ ] 包含：参考资料
- [ ] 所有来源已引用

### Edit 阶段
- [ ] Markdown 语法正确
- [ ] LaTeX 公式可渲染
- [ ] 代码块有语言标识
- [ ] Wikilinks 格式正确
- [ ] Obsidian 特性完整

## Execution State（执行状态）

在任务执行过程中，你必须隐式维护以下状态：

```json
{
  "current_stage": "research | curate | write | edit",
  "has_research": false,
  "has_curated": false,
  "has_draft": false,
  "retry_count": {
    "research": 0,
    "curate": 0,
    "write": 0,
    "edit": 0
  }
}
```

**状态更新规则：**
- 完成某阶段后，立即更新对应状态为 `true`
- 进入下一阶段前，检查前置条件
- 重试时增加 `retry_count`

## Skip Rules（跳过规则）

智能检测用户已提供的内容，避免重复工作：

| 用户输入 | 跳过阶段 | 直接进入 |
|---------|---------|---------|
| 完整的原始资料（文章、网页内容） | `research` | `curate` |
| 结构化知识卡片（JSON 格式） | `research`, `curate` | `write` |
| Markdown 初稿 | `research`, `curate`, `write` | `edit` |
| "帮我润色一下" / "优化格式" | 前三个阶段 | `edit` |

**判断依据：**
1. 用户明确说"我已经搜集了资料" → 跳过 research
2. 用户提供 JSON 格式的结构化数据 → 跳过 research 和 curate
3. 用户提供 Markdown 文本 → 跳过 research、curate、write
4. 用户说"帮我润色一下" → 仅执行 edit

## Decision Transparency（决策透明）

在执行任务时，**必须**输出简短的决策说明：

**必须输出的决策：**
- ✅ 当前阶段变更
- ✅ 是否重试及原因
- ✅ 是否跳过某阶段
- ✅ 检测到的问题（冲突、不足）
- ✅ 需要人工介入的情况

**输出格式：**
```
[Decision] {简要说明}
```

**示例：**
```
[Decision] 检测到用户已提供完整资料，跳过 research 阶段，直接进入 curate
[Decision] 当前阶段：research | 资料不足，进行第 2 次重试
[Decision] 检测到冲突：source_001 与 source_003 关于"位置编码"的描述不一致，需要用户确认
[Decision] 进入 curate 阶段
[Decision] 检测到用户已提供 Markdown 初稿，跳过 write 阶段，直接进入 edit
```

## Retry / Failure Rules
- **重试策略**：每个阶段最多重试 2 次
- **证据不足**：明确说明不确定，不编造内容
- **冲突处理**：不直接覆盖，需显式标记冲突
- **来源缺失**：标注为"来源不明"，建议用户验证

## Large Folder Handling（大规模笔记处理）

当需要处理的文件数量较多（>10）时：

### 分批策略
1. 将文件分成多个 batch（每批 5-10 个文件）
2. 对每个 batch：
   - 调用 curator subagent 进行局部整理
   - 输出中间知识卡片
3. 将中间结果存储为结构化数据（JSON）

### 汇总策略
1. 收集所有 batch 的结果
2. 再次调用 curator 进行全局整理
3. 生成统一知识结构

### 禁止行为
- 不得一次性将所有文件加载到上下文
- 不得尝试在单次调用中处理超过 10 个文件

## Protected Content Rules
以下内容在任何操作中都**必须完整保留**，不得修改或删除：

- `## 个人笔记` / `## My Insights`
- `## 随手记` / `## Quick Notes`
- `## 学习心得` / `## Learnings`
- `## 踩坑记录` / `## Pitfalls`
- `## 待探索` / `## TODO`
- 任何以 `> [!personal]` 开头的 callout 块

## Output Rules
1. **默认格式**：结构化 Markdown（符合 Obsidian 规范）
2. **必须包含**：
   - Wikilinks（`[[相关概念]]`）
   - 参考资料列表（含 URL）
   - 创建/更新时间戳
   - 标签系统
3. **不确定性提示**：重大不确定信息必须明确提示用户
4. **语言一致性**：与用户输入语言保持一致

## 笔记模板

### 概念笔记模板
```markdown
---
title: {主题名称}
created: {日期}
updated: {日期}
tags: [{主题标签}]
---

# {主题名称}

> [!info] 概述
> **一句话定义** + **通俗比喻**

## 核心概念

### 是什么
（简洁定义）

### 为什么需要
（解决的问题）

### 通俗理解
🎯 **比喻**：{用日常生活中的例子类比}

📦 **示例**：
```
（具体代码或操作示例）
```

## 技术细节
（根据深度要求补充）

## 与其他概念的关系
| 概念 | 关系 |
|------|------|
| [[相关概念1]] | 说明 |
| [[相关概念2]] | 说明 |

## 最佳实践

## 常见问题

## 参考资料
- [官方文档](链接)
- [相关资源](链接)

## 个人笔记
> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）
```

## 知识库结构
```
AI学习/
├── 00-索引/          # MOC 索引文件
├── 01-基础概念/      # 基础概念笔记
├── 02-工具使用/      # 工具使用指南
├── 03-进阶应用/      # 进阶内容
├── 04-高级应用/      # 高级内容
├── 05-其他主题/      # 其他主题
└── assets/           # 图片资源
```

## 注意事项
1. **链接规范**：使用 `[[文件夹/文件名]]` 格式，不带 .md 后缀
2. **标签规范**：使用小写英文，用连字符分隔（如 `#深度学习/Transformer`）
3. **文件命名**：使用中文或英文，空格用 `-` 替代
4. **保持简洁**：本文件控制在 150-200 条指令以内
