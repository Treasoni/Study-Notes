# cc03 Stale Map — Claude Code CLI 完整参考

> note_id: cc03
> 检查日期: 2026-08-10
> 更新目标: 同步到 Claude Code v2.1.226（2026-08）

## 保留（Keep）

| 区块 | 理由 |
|------|------|
| 核心概念 / 两种核心模式 | 交互模式与 Print 模式定义未变化 |
| CLI 命令速查 - 基础命令 | `-p` / `-c` / `-r` / `update` 等仍有效 |
| 模型配置 | 未在本轮更新目标范围内（见报告风险项） |
| 系统提示词定制 | `--system-prompt*` 行为未变 |
| 输出格式（除 max-budget 行外） | `--output-format` / `--input-format` / `--json-schema` 仍有效 |
| MCP 配置 / 高级功能（大部分） | 未过时 |
| 高价值用例 / 常用命令组合 | 基于仍有效的标志 |
| 故障排除 / 与其他概念的关系 / 学习路线图 / 参考资料 | 无过时点 |

## 更新（Update）

| # | 位置 | 现状 | 目标 |
|---|------|------|------|
| U1 | 概述-版本行 | v2.1.207（2026-07-11） | v2.1.226（2026-08-10） |
| U2 | 权限标志 `--permission-mode` | 描述「以指定权限模式开始」，示例 `auto` | 说明 `default` 已改名 `manual`，示例 `--permission-mode manual` |
| U3 | 输出标志 `--max-budget-usd` | 「Print 模式的最大花费」 | 「最大花费预算；达到上限时停止后台子代理」 |
| U4 | 管理命令 `claude agents` | 「列出所有配置的子代理」 | 补充 `/status` 显示会话类型（interactive / attached / unattended） |
| U5 | 关键环境变量表 | 12 个变量 | 新增 5 个环境变量 |
| U6 | frontmatter | `updated: 2026-07-12` | `updated: 2026-08-10` |

## 删除（Delete）

无。本轮未发现已失效需删除的段落。

## 新增（Add）

| # | 位置 | 内容 |
|---|------|------|
| A1 | 权限标志表后 | `[!tip] 大白话` 解释 default→manual 改名 |
| A2 | 输出格式表 | `--forward-subagent-text`（stream-json 透传子代理文本） |
| A3 | 高级标志表 | `--ax-screen-reader`（屏幕阅读器模式） |
| A4 | 代理配置节 | `[!note]` 会话类型说明（`/status` 显示 interactive / attached / unattended） |
| A5 | 关键环境变量表 | 5 个新变量（见 U5） |
| A6 | 文末 | `## 更新记录` 变更日志 |
