# 更新清单 - Codex 笔记重构为 Claude Code 教程风格

> 工作流：batch-note-update-flow
> 运行标识：update-codex-config
> 项目标识：codex-config-update
> 创建时间：2026-08-10
> 扫描范围：`AI学习/Codex/*.md`

## 扫描说明

- 共扫描到 **10 个 Markdown 文件**（8 章 + 1 附录 + 1 MOC）。
- 所有笔记 frontmatter `title` 均为 `"Codex 完整配置体系"`（MOC 为 `"Codex 配置体系 MOC"`），正文为"书章"式结构，缺少教程式区块（文档定位、常见问题、最佳实践、小结、相关文档、参考资料、更新记录）。
- 更新目标：镜像 `AI学习/Claude Code 教程/` 子目录结构 + 完整套用教程模板。内容保留，仅重排结构与排版。
- **全部 10 篇标记 `ready`**，进入更新计划。

## 清单

| # | 当前路径 | 当前标题 | updated | 目标路径（新） | 动作 | 说明 |
|---|---------|---------|---------|----------------|------|------|
| 1 | `AI学习/Codex/01 配置哲学概览.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/01-入门/Codex 配置哲学概览.md` | update | 重排套模板，去序号改名 |
| 2 | `AI学习/Codex/02 config.toml 核心配置.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/02-基础功能/config.toml 核心配置.md` | update | 重排套模板，去序号改名 |
| 3 | `AI学习/Codex/03 AGENTS.md 分层体系.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/03-进阶应用/AGENTS.md 分层体系.md` | update | 重排套模板，去序号改名 |
| 4 | `AI学习/Codex/04 Skills 技能系统.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/03-进阶应用/Skills 技能系统.md` | update | 重排套模板，去序号改名 |
| 5 | `AI学习/Codex/05 Agents 与 MCP.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/03-进阶应用/Agents 与 MCP.md` | update | 重排套模板，去序号改名 |
| 6 | `AI学习/Codex/06 Hooks 与插件.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/03-进阶应用/Hooks 与插件.md` | update | 重排套模板，去序号改名 |
| 7 | `AI学习/Codex/07 CLI 与调试.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/02-基础功能/Codex CLI 与调试.md` | update | 重排套模板，去序号改名 |
| 8 | `AI学习/Codex/08 对照表与迁移实战.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/04-高级功能/对照表与迁移实战.md` | update | 重排套模板，去序号改名 |
| 9 | `AI学习/Codex/附录 快速参考卡片.md` | Codex 完整配置体系 | 2026-07-31 | `AI学习/Codex/04-高级功能/快速参考卡片.md` | update | 重排套模板，去序号改名 |
| 10 | `AI学习/Codex/Codex 配置体系 MOC.md` | Codex 配置体系 MOC | 2026-07-31 | `AI学习/Codex/Codex MOC.md` | update | 重命名 + 按 Claude Code MOC 模板重写 |

## 关键词命中

- 全部 10 篇命中：缺 `文档定位`、`常见问题`、`最佳实践`、`小结`、`相关文档`、`更新记录` 教程区块。
- 9 篇正文命中"书章"式标题（第一章…第八章 / 附录）。
- 8 篇含 `> [!note] 导航` 旧 wikilink（指向旧文件名），需替换为新文件名。
- 5 篇含 Claude Code 对照表，需保留。

## 结论

全部 10 篇 `ready`，无 `needs-review` / `skip`。进入 P2 批量更新计划。
