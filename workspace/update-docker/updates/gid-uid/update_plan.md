# update_plan — docker里的GID和UID

> 日期：2026-08-04
> 动作：update（仅 frontmatter）

## 计划变更

1. **补齐 frontmatter**：新增 `title`、`created`、`updated`、`status`、`source_project`，保留原 `tags`。
2. **追加 `## 更新记录`**：记录日期与变更摘要。
3. 正文不动。

## 理由

- 该笔记是 docker 目录内唯一同时缺 `created`/`updated` 的 2 篇之一，P1 清单标记为低优先级仅补 frontmatter，用户确认。
- 正文 UID/GID 概念为稳定知识，无需内容更新。

## 不做的事

- 不重写正文。
- 不修复正文疑似损坏行（超出本次范围，仅记录）。
