---
description: "更新现有笔记"
argument-hint: "文件路径"
allowed-tools: ["Read", "WebSearch", "Edit", "Grep", "mcp__browsermcp__browser_navigate", "mcp__browsermcp__browser_snapshot", "mcp__browsermcp__browser_screenshot", "mcp__browsermcp__browser_click", "mcp__browsermcp__browser_type", "mcp__browsermcp__browser_wait", "mcp__browsermcp__browser_go_back", "mcp__browsermcp__browser_go_forward"]
---

# 更新笔记：$ARGUMENTS

## 执行步骤

### 1. 读取现有内容
读取指定文件，分析当前结构和内容

### 2. 识别用户自定义章节
**必须完整保留以下章节，不得修改或删除**：
- `## 个人笔记` / `## My Insights`
- `## 随手记` / `## Quick Notes`
- `## 学习心得` / `## Learnings`
- `## 踩坑记录` / `## Pitfalls`
- `## 待探索` / `## TODO`
- 任何以 `> [!personal]` 开头的 callout 块

### 3. 获取最新信息与来源整理

#### 3.1 信息获取优先级
按以下顺序获取信息，确保来源权威可靠：
1. **官方文档** - 使用 WebSearch 搜索 "xxx official documentation"
2. **官方 GitHub** - 查找最新的 API 变更和示例
3. **权威博客** - 官方博客或核心维护者的文章
4. **社区资源** - 仅作为补充

#### 3.2 搜索与浏览方法
识别笔记主题，使用 WebSearch 搜索官方最新文档

**如果 WebSearch 无结果或结果不理想**，使用 browsermcp 直接浏览网页：
1. 使用 `mcp__browsermcp__browser_navigate` 导航到已知的官方文档 URL
2. 使用 `mcp__browsermcp__browser_snapshot` 获取页面结构
3. 查找 Changelog、Release Notes 或更新日志
4. 使用 `mcp__browsermcp__browser_click` 展开相关章节（如需要）
5. 提取更新内容并记录来源

#### 3.3 来源链接处理原则

**就近放置原则**：来源链接应放在相关内容附近，方便读者追溯
- 代码示例后紧跟来源
- API 说明后添加参考链接
- 具体操作步骤后标注出处

**来源放置位置**（按优先级）：

**位置 A - 章节末尾 callout（推荐）**：
```markdown
## 2. 安装配置

具体内容...

> [!info] 📚 来源
> - [官方文档 - 安装指南](链接)
> - [GitHub - 配置示例](链接)
```

**位置 B - 行内链接**：
```markdown
根据 [官方文档](链接) 的说明，推荐使用以下配置...
```

**位置 C - 文档末尾参考资料章节**：
- 仅用于汇总所有来源
- 作为全局索引，不替代就近链接

**来源格式规范**：
```markdown
> [!info] 📚 来源
> - [官方文档](链接) - 简要说明
> - [社区教程](链接) - 来源网站
```

**WebSearch 结果处理**：
- 提取搜索结果中的来源链接
- 按可信度排序：官方 > GitHub > 权威博客 > 社区
- 在对应章节末尾添加来源 callout
- 同时更新文档末尾的 `参考资料` 汇总

**参考资料章节格式**（文档末尾汇总）：
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

### 4. 增量更新
**仅更新**：
- 技术参数
- API 变更
- 最佳实践
- 参考资料

**禁止修改**：
- 用户自定义章节（见保护列表）

### 5. 检查双向链接
扫描知识库中引用此文件的其他笔记，确保链接正确，添加新的关联链接
