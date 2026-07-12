# 更新报告：如何编写Skills.md

| 项目 | 内容 |
|------|------|
| **文件** | 如何编写Skills.md |
| **动作** | patch-in-place |
| **更新范围** | frontmatter、核心格式（旧 metadata.json→新 SKILL.md）、操作步骤、FAQ |
| **完成时间** | 2026-07-12 |

## 修改记录

| # | 修改项 | 旧值 → 新值 |
|---|--------|-------------|
| 1 | Frontmatter | 补充 `title`、`created`、`updated`、`status`、`source_project` |
| 2 | 核心概念 | 旧格式（metadata.json + skill.md）→ 新格式（SKILL.md + YAML frontmatter） |
| 3 | 操作步骤 | 创建 metadata.json + skill.md → 创建 SKILL.md（含 frontmatter 示例） |
| 4 | 注意事项 | `metadata.json` 检查 → `SKILL.md frontmatter` 检查 |
| 5 | 关键配置 | `when_to_use` → `description`（pushy 原则） |
| 6 | FAQ | 补充 Skills vs Subagents vs Dynamic Workflows 对比 |
| 7 | 补丁范围 | ~30% 核心格式更新（patch 层面，保留原有示例框架） |

## 风险等级
- **低** — 技能编写概念保持，仅格式从旧版更新到当前 Agent Skills 开放标准。
