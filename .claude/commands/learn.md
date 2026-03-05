---
description: "学习新知识点并创建笔记"
argument-hint: "主题名称"
allowed-tools: ["WebSearch", "Write", "Grep", "Read", "Glob", "mcp__browsermcp__browser_navigate", "mcp__browsermcp__browser_snapshot", "mcp__browsermcp__browser_screenshot", "mcp__browsermcp__browser_click", "mcp__browsermcp__browser_type", "mcp__browsermcp__browser_wait", "mcp__browsermcp__browser_go_back", "mcp__browsermcp__browser_go_forward"]
---

# 学习新知识点：$ARGUMENTS

## 执行步骤

### 1. 搜索官方资源
首先使用 WebSearch 搜索 "$ARGUMENTS official documentation 2026"

**如果 WebSearch 无结果或结果不理想**，使用 browsermcp 直接浏览网页：

1. 使用 `mcp__browsermcp__browser_navigate` 导航到已知的官方文档 URL
2. 使用 `mcp__browsermcp__browser_snapshot` 获取页面可访问性快照
3. 根据页面内容导航到相关章节
4. 使用 `mcp__browsermcp__browser_click` 点击展开内容（如需要）
5. 使用 `mcp__browsermcp__browser_wait` 等待动态内容加载（如需要）
6. 提取所需信息后记录来源 URL

### 2. 创建笔记
在合适的目录下创建笔记文件，使用以下标准模板：

```markdown
---
tags: [主题标签]
created: {日期}
updated: {日期}
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
**🎯 比喻**：{用日常生活中的例子类比}

**📦 示例**：
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

## 个人笔记
> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

## 相关文档
- [[索引文件]]

## 参考资料
### 官方资源
- [官方文档](链接) - 完整技术文档
- [GitHub 仓库](链接) - 源代码

### 社区资源
- [教程文章](链接) - 来源网站
- [实战指南](链接) - 来源网站

### 第三方文档
- [相关服务API](链接) - 服务名称官方
```

### 2.5. 添加来源引用
从 WebSearch 结果中提取来源链接，按以下规则添加到文档中：

**内联引用**：在相关章节（核心概念、技术细节、最佳实践等）末尾添加来源 callout：
```markdown
> [!info] 来源
> - [文档标题](链接) - 来源网站
> - [相关教程](链接) - 来源网站
```

### 2.6. 优先使用官方资源
当学习新知识点时，必须按以下顺序获取信息：
1. **官方文档** - 使用 WebSearch 搜索 "xxx official documentation"
2. **官方 GitHub** - 查找最新的 API 变更和示例
3. **权威博客** - 官方博客或核心维护者的文章
4. **社区资源** - 仅作为补充

**参考资料章节**：将所有来源整理到文档末尾，按类别分组：
```markdown
## 参考资料
### 官方资源
- [官方文档](链接) - 完整技术文档
- [GitHub 仓库](链接) - 源代码

### 社区资源
- [教程文章](链接) - 来源网站
- [实战指南](链接) - 来源网站

### 第三方文档
- [相关服务API](链接) - 服务名称官方
```

### 3. 建立知识关联
搜索知识库中相关内容，添加双向 wikilink

### 4. 更新 MOC 索引
在相关索引文件中添加新笔记的链接
