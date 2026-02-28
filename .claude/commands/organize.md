---
description: "整理文件夹并生成/更新 MOC"
argument-hint: "文件夹路径"
allowed-tools: ["Glob", "Grep", "Read", "Write"]
---

# 整理文件夹：$ARGUMENTS

## 执行步骤

### 1. 扫描指定文件夹
使用 Glob 扫描指定文件夹下的所有文件

### 2. 分析文件类型和内容
识别每个文件的类型和主题

### 3. 孤岛检测（Island Detection）
扫描整个知识库，识别没有任何入链（Inbound links）的笔记

### 4. 生成/更新 MOC
创建或更新文件夹的 MOC 索引：
- 按主题分类整理
- 添加快速查找表
- 将孤岛笔记优先展示在 MOC 中

### 5. 建立文档关联
- 识别相关文档
- 添加双向 wikilink
- 更新标签分类
