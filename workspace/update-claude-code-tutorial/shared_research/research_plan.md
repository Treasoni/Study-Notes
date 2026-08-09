# 共享资料研究计划 — Claude Code 2026-08 现状

> 创建：2026-08-10
> 更新目标：同步 19 篇 Claude Code 教程到 2026-08 最新版
> 适用范围：cc01–cc19（全部笔记共享「Claude Code 2026-08 现状」基线）

## 研究范围

只收集与「Claude Code 2026-07/08 变化」直接相关的最小资料，不保存网页全文。每篇笔记的独有细节由 note-updater 在 P4 逐篇补充。

### 优先级主题

| 主题 | 适用笔记 | 来源类型 |
|------|----------|---------|
| 模型变化（Sonnet 5 / Opus 5 / 1M 上下文） | cc01, cc05, cc12, cc19 | 官方 changelog / what's-new |
| 权限模式重命名（Default→Manual） | cc02, cc03, cc06 | 官方 changelog |
| Subagents 行为变化（后台/并发/嵌套/子任务） | cc10, cc04, cc12 | 官方 changelog |
| 新命令与别名（/fork /doctor /review=/code-review） | cc13, cc02, cc04 | 官方 changelog |
| settings.json 新配置键 | cc06 | 官方 changelog + 官方 docs |
| Auto mode / 沙盒 / 无障碍 | cc12 | 官方 what's-new（w28/w29） |
| Hooks 更新 | cc08 | 官方 changelog |
| MCP 更新 | cc14 | 官方 changelog |
| Skills 更新 | cc15, cc13 | 官方 changelog |
| CLAUDE.md / 会话 / Checkpoints / Caching | cc16, cc04, cc07, cc19 | 官方 changelog |
| 插件系统安全变化 | cc11 | 官方 changelog |

### 采集方式

- 一手来源：`anthropics/claude-code` CHANGELOG.md、官方 docs `code.claude.com/docs/en/changelog` 与 `whats-new` 周刊。
- 次选：classmethod DevelopersIO 中文/日文发布摘要（版本行为佐证）。
- 高时效结论以官方 changelog 原句为准；多个信源冲突时官方优先。

## 产出

- `source_bank.md`：每条含 URL、日期、适用笔记范围、100–200 字摘要。
- 提交给 P4 的每篇 note-updater 作为公共基线，避免逐篇重复检索。

## 边界

- 不收集与本次更新目标无关的 Claude Code 历史功能。
- 不保存网页全文；只留结构化摘要。
