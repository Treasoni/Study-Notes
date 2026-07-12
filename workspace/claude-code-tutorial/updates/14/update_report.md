# 更新报告：CLAUDE.md 使用指南.md

| 项目 | 内容 |
|------|------|
| **文件** | CLAUDE.md 使用指南.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、文件优先级表、新功能补充 |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`created`、`updated`、`status`、`source_project` |
| 2 | 文件优先级表 | 新增 `.claude/rules/`、子目录 CLAUDE.md |
| 3 | 最佳实践 | 补充 200 行限制、`@import` 语法 |
| 4 | 新增子目录 CLAUDE.md | Monorepo 场景说明 |
| 5 | 新增 `.claude/rules/` 章节 | 路径范围规则、加载优先级 |
| 6 | 补丁范围 | ~15% 内容补充（patch 层面，非重写） |

## 风险等级
- **低** — 仅补充新功能信息，未改变原有核心内容和结构。
