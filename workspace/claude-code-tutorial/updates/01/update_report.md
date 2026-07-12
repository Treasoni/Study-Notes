# 更新报告：如何使用Claude code.md

| 项目 | 内容 |
|------|------|
| **文件** | 如何使用Claude code.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、版本号、命令表、模型名、参考链接 |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`updated`、`status`、`source_project` |
| 2 | 版本号 | v2.1.131 (2026-05-06) → v2.1.207 (2026-07-11) |
| 3 | 启动命令表 | 补充 `claude -p`、`claude -c`、`claude --resume`、`claude agents`、`--safe-mode`、`--worktree` |
| 4 | Slash 命令表 | 从 8 条扩展到 22 条，补充 `/cd`、`/code-review`、`/usage`、`/effort`、`/checkup`、`/fast`、`/plan`、`/todos`、`/goal`、`/memory`、`/compact`、`/cost`、`/rewind`、`/fork`、`/diff`、`/init` |
| 5 | 模型名称 | `claude-sonnet-4` → `claude-sonnet-5`，`claude-opus-4` → `claude-opus-4.8` |
| 6 | CLAUDE.md 章节 | 补充 200 行限制、子目录 CLAUDE.md、`@import`、路径规则建议 |
| 7 | 参考资料 | 补充官方 What's New、Changelog、Subagents/Dynamic Workflows 博客 |
| 8 | 补丁范围 | ~15% 内容更新（patch 层面，非重写） |

## 风险等级
- **低** — 未改变原有结构和主要内容，仅在过时区域做局部替换和补充。
