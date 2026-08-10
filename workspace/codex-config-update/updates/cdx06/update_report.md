# cdx06 更新报告：Hooks 与插件

## 概述

将 Codex 系列第 6 篇笔记（`AI学习/Codex/06 Hooks 与插件.md`）按「Claude Code 教程」模板（`AI学习/Claude Code 教程/03-进阶应用/Claude Code Hooks 使用指南.md`）重构为独立教程风格。**全部技术内容（代码块、表格、Callout、对比表）原样保留**，仅重排布局并补齐教程型分节。

## 变更摘要

- **重命名**：`# 第六章：Hooks 生命周期钩子与插件体系` → `# Hooks 与插件`；frontmatter 更新为 `title: Hooks 与插件`、`tags: [codex, ai, 工具使用, 进阶应用, hooks]`、`updated: 2026-08-10`、`status: updated`、`source_project: codex-config`。
- **重排**：Part 1 / Part 2 编号小节（`### Part 1` / `#### 1.1`…）转换为 `##` / `###` 主题分节；去除编号前缀。
- **新增分节**：`> [!info] 文档定位`（紧随 H1）、`## 常见问题`（3 条 FAQ，源自内容）、`## 最佳实践`（Do's / Don'ts）、`## 小结`、`## 相关文档`（表格）、`## 参考资料`（官方 Codex 链接）、`## 更新记录`。
- **移除**：旧的书本式导航块（`> [!note] 导航` / `[[xx|← 上一章]]`），由 `## 相关文档` 表格替代。
- **内容完整性**：未删除、未改写任何代码块、表格、Callout 或技术细节；`> **本章小结**` 原文并入 `## 小结` 的 Callout。

## 结构布局（最终）

```
H1 + 文档定位 → Hooks 生命周期钩子系统（6 子节）→ 插件体系（3 子节）
→ 常见问题 → 最佳实践 → 小结 → 相关文档 → 参考资料 → 更新记录
```

## 目标位置

- 已写入（patch-in-place）：`AI学习/Codex/03-进阶应用/Hooks 与插件.md`
- 工作区副本：`workspace/codex-config-update/updates/cdx06/updated_note.md`
- 结构映射：`workspace/codex-config-update/updates/cdx06/stale_map.md`
