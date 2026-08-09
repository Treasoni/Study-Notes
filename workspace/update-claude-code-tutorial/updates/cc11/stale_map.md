# cc11 过时点映射

> note_id: cc11
> 笔记: Claude Code 插件系统使用指南
> 更新目标: 同步 2026-07/08 插件系统安全与来源变化
> 资料来源: SB-19（共享 source bank，v2.1.207 / v2.1.224）+ update_goal 专项补充
> 日期: 2026-08-10

## 过时点清单

| # | 位置（原文件行） | 现状 | 过时原因 | 处理 |
|---|-----------------|------|---------|------|
| S1 | 第 4-5 行（frontmatter） | `updated: 2026-07-12` | 笔记更新日期落后于本次同步 | 改为 `updated: 2026-08-10`；status 保持 `updated` |
| S2 | 第 143-162 行（§3 用户可配置选项 userConfig） | 未提及 `${user_config.*}` 注入风险 | SB-19：插件 shell 形式 `headersHelper:${user_config.*}` 被拒绝（shell 注入修复） | 加 `[!warning]`，指引环境变量/对象形式传参 |
| S3 | 第 205-215 行（§3 插件默认设置） | 原文「用户可在项目或用户配置中覆盖这些设置」 | SB-19：`pluginConfigs` 不再从项目级 `.claude/settings.json` 读取 | 修正为仅用户级覆盖 + 加 `[!warning]` |
| S4 | 第 277-297 行（§4 安装方法） | 仅市场/本地/Git/运行时 4 种来源 | SB-19：新增 `archive` 来源（HTTPS zip + 可选 SHA-256 固定） | 补充 archive 安装命令与 SHA-256 示例 |
| S5 | 第 417-441 行（§6 企业管理设置） | 有 `strictKnownMarketplaces`/`extraKnownMarketplaces`，缺 `blockedMarketplaces` | update_goal：marketplace 配置可补 `blockedMarketplaces` 与 owner 通配符 | 补表格行 + owner 通配符说明 + 示例 |
| S6 | 第 443-451 行（§6 插件安全限制） | 缺少安装同意与注入修复说明 | SB-19：外部插件只由项目设置启用时，每个加载路径要求明确安装同意（防自批准） | 新增「安装同意」小节 + shell 注入 warning |
| S7 | 第 478-483 行（§7 FAQ 插件安全吗？） | 安全建议未覆盖 archive/SHA-256/安装同意 | 与 S4/S6 同源更新 | 补充 SHA-256 校验与安装同意提醒 |
| S8 | 全篇核心概念 | 缺少白话讲解 | update_goal：核心概念加 `[!tip] 大白话` | 在 §1 核心概念、§4 安装、§6 安全补充 tip |

## 无需变更的章节

- §2 插件结构（目录结构、plugin.json、Agent 格式）——无对应变更。
- §3 持久化数据目录 / 内联插件定义 / LSP——无对应变更。
- §5 创建自己的插件——结构未变；安全最佳实践随 §6/§7 同步。
- §8 故障排除——命令仍有效，无对应变更。

## 风险与备注

- SB-19 未逐条标注版本（v2.1.207 与 v2.1.224 对应关系需对照 changelog 复核）。
- 原文 `headersHelper` 的推荐替代写法（对象形式）未在 SB-19 中给出具体 schema，正文仅给出方向性建议。
