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
- **参数**:
  - `query`: 搜索关键词（必填）
  - `allowed_domains`: 限制搜索域名（可选）
  - `blocked_domains`: 排除域名（可选）
- **示例**: WebSearch(query="Obsidian 使用技巧")

#### WebFetch
- **功能**: 获取 URL 内容并转为 Markdown
- **使用场景**: 提取网页正文、阅读文章
- **调用方式**: 使用 WebFetch 工具
- **参数**:
  - `url`: 目标 URL（必填）
  - `prompt`: 提取内容的指令（必填）
- **示例**: WebFetch(url="https://example.com", prompt="提取文章正文")
- **限制**: 无法访问需要认证的私有 URL

### MCP 工具

#### MiniMax web_search
- **功能**: 网页搜索，返回结构化 JSON 结果
- **使用场景**: 实时信息搜索，类似 Google Search
- **调用方式**: 使用 mcp__MiniMax__web_search 工具
- **返回格式**:
  ```json
  {
    "organic": [
      {
        "title": "标题",
        "link": "URL",
        "snippet": "摘要",
        "date": "日期"
      }
    ],
    "related_searches": [
      {"query": "相关搜索建议"}
    ]
  }
  ```

#### MiniMax understand_image
- **功能**: 分析图片内容，提取文字或描述
- **使用场景**: 提取图片中的文字、描述图片内容
- **调用方式**: 使用 mcp__MiniMax__understand_image 工具
- **参数**:
  - `prompt`: 分析指令（必填）
  - `image_source`: 图片路径或 URL（必填）
- **支持格式**: JPEG, PNG, WebP
- **示例**: mcp__MiniMax__understand_image(prompt="提取图片中的文字", image_source="photo.png")

### Skills

#### defuddle
- **功能**: 从网页提取正文内容，去除广告、导航等干扰元素
- **使用场景**: 提取网页、网页正文
- **调用方式**: 使用 Skill 工具调用 defuddle
- **触发词**: 提取网页、网页正文、defuddle

---

## 工作流建议

### 简单搜索流程
```
1. WebSearch/MiniMax web_search → 获取搜索结果
2. 选择相关链接
3. WebFetch/defuddle → 提取内容
```

### 深度研究流程
```
1. 多次搜索不同关键词
2. 提取多个来源的内容
3. 整理和归纳信息
4. 生成结构化笔记
```

### 图片分析流程
```
1. MiniMax understand_image → 分析图片
2. 提取文字或获取描述
3. 整理到笔记中
```

---

## 工具选择指南

| 需求 | 推荐工具 | 原因 |
|------|----------|------|
| 快速搜索 | WebSearch | 内置工具，响应快 |
| 实时搜索 | MiniMax web_search | 结构化结果，包含日期 |
| 提取网页正文 | defuddle | 专业提取，去除干扰 |
| 提取简单网页 | WebFetch | 内置工具，简单直接 |
| 图片文字提取 | MiniMax understand_image | OCR 功能 |
| 图片内容描述 | MiniMax understand_image | 视觉分析 |

---

## 最佳实践

1. **组合使用**: 搜索 + 提取是基本模式
2. **多源验证**: 重要信息从多个来源确认
3. **保存原文**: 提取内容时保留原始 URL 以便溯源
4. **格式统一**: 使用 Obsidian Markdown 格式保存笔记
