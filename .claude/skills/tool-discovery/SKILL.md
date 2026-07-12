---
name: tool-discovery
description: 查看当前环境中可用于资料收集的工具，包括内置工具、MCP 工具和已安装的 skills。当用户想了解有哪些工具可以用来搜索、提取、分析资料时使用此技能。触发词：可用工具、有哪些工具、工具列表、收集工具、search tools、available tools。
---

# Tool Discovery - 资料收集工具发现

帮助用户了解当前环境中可用于资料收集的工具，并生成规则文档。

## 触发条件

当用户提出以下类型的请求时，调用此技能:

- "有哪些工具可以收集资料"
- "查看可用的资料收集工具"
- "当前环境有什么搜索工具"
- "列出所有可以用来研究的工具"
- "help me find tools for research"
- 任何涉及发现、列出、查看可用工具的请求

## 工作流程

### Step 1: 收集工具信息

扫描以下来源，列出所有可用工具：

#### 1. 内置工具

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `WebSearch` | 搜索网页，返回结果列表 | 快速查找信息、获取最新资讯 |
| `WebFetch` | 获取 URL 内容并转为 Markdown | 提取网页正文、阅读文章 |

#### 2. MCP 工具

检查 `mcp__` 开头的工具，例如：

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `mcp__MiniMax__web_search` | 网页搜索（类似 Google） | 实时信息搜索 |
| `mcp__MiniMax__understand_image` | 分析图片内容 | 提取图片中的文字、描述图片 |

#### 3. 已安装的 Skills

检查 `.claude/skills/` 目录下与资料收集相关的技能：

| 技能 | 功能 | 触发词 |
|------|------|--------|
| `defuddle` | 从网页提取正文内容 | 提取网页、网页正文 |

### Step 2: 生成规则文档

将发现的工具信息整理成规则文档，保存到 `.claude/rules/research-tools.md`：

```markdown
---
paths:
  - ".claude/rules"
---

# 资料收集工具指南

## 可用工具列表

### 内置工具

#### WebSearch
- **功能**: 搜索网页，返回标题、URL、摘要
- **使用场景**: 快速查找信息、获取最新资讯
- **调用方式**: 直接使用 WebSearch 工具
- **示例**: WebSearch(query="Obsidian 使用技巧")

#### WebFetch
- **功能**: 获取 URL 内容并转为 Markdown
- **使用场景**: 提取网页正文、阅读文章
- **调用方式**: 使用 WebFetch 工具
- **参数**:
  - `url`: 目标 URL
  - `prompt`: 提取内容的指令
- **示例**: WebFetch(url="https://example.com", prompt="提取文章正文")

### MCP 工具

#### MiniMax web_search
- **功能**: 网页搜索，返回结构化结果
- **使用场景**: 实时信息搜索
- **调用方式**: 使用 mcp__MiniMax__web_search 工具

#### MiniMax understand_image
- **功能**: 分析图片内容
- **使用场景**: 提取图片中的文字、描述图片
- **调用方式**: 使用 mcp__MiniMax__understand_image 工具
- **参数**:
  - `prompt`: 分析指令
  - `image_source`: 图片路径或 URL

### Skills

#### defuddle
- **功能**: 从网页提取正文内容
- **使用场景**: 提取网页、网页正文
- **调用方式**: 使用 Skill 工具调用 defuddle

## 工作流建议

### 简单搜索
1. 使用 `WebSearch` 或 `mcp__MiniMax__web_search` 搜索
2. 从结果中选择相关链接
3. 使用 `WebFetch` 或 `defuddle` 提取内容

### 深度研究
1. 多次搜索不同关键词
2. 提取多个来源的内容
3. 整理和归纳信息

### 图片分析
1. 使用 `mcp__MiniMax__understand_image` 分析图片
2. 提取图片中的文字或描述
```

### Step 3: 返回结果

向用户展示：

1. **工具概览** - 当前可用的所有资料收集工具
2. **规则文档** - 已生成的规则文件路径
3. **使用建议** - 根据用户需求推荐合适的工具组合

## 输出格式

```
## 当前可用的资料收集工具

### 内置工具
- **WebSearch**: 搜索网页
- **WebFetch**: 提取网页内容

### MCP 工具
- **MiniMax web_search**: 网页搜索
- **MiniMax understand_image**: 图片分析

### Skills
- **defuddle**: 网页正文提取

---
规则文档已保存到: .claude/rules/research-tools.md
```

## 注意事项

- 工具列表可能随环境变化，建议定期运行此技能更新规则
- 不同工具适合不同场景，根据需求选择合适的工具
- 组合使用多个工具可以提高资料收集的效率和质量
