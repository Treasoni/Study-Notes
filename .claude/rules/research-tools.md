---
paths:
  - ".claude/skills/tool-discovery"
---

# 资料收集工具指南

## 工具选型

| 需求 | 推荐工具 | 说明 |
|------|----------|------|
| 快速搜索 | WebSearch | 内置，响应快 |
| 实时搜索 | MiniMax web_search | 结构化 JSON 结果，含日期 |
| 提取网页正文 | defuddle | 专业提取，去广告和导航 |
| 提取简单网页 | WebFetch | 内置，直接转 Markdown |
| 图片 OCR/描述 | MiniMax understand_image | 支持 JPEG/PNG/WebP |

## 核心规则

1. **组合使用**: 搜索 → 提取是基本模式，多源交叉验证
2. **保留溯源**: 提取内容时保留原始 URL，以便回查
3. **格式统一**: 使用 Obsidian Markdown 格式保存
