# cc01 过时点地图（stale map）

> 笔记：Claude Code 使用指南（入门篇）· note_id：cc01
> 核对基线：`shared_research/source_bank.md`（SB-01/02/04/08/09/10）+ 官方 changelog 截至 2026-08-10
> 生成日期：2026-08-10

## 更新（UPDATE）

| # | 位置 | 原内容 | 过时原因 | 改为 |
|---|------|--------|---------|------|
| U1 | frontmatter `updated` | 2026-08-07 | 本次更新日期 | 2026-08-10 |
| U2 | 一、快速安装 · 1️⃣ 原生安装器 tip | latest v2.1.224（2026-08-07）/ stable v2.1.220 | source_bank 覆盖至 v2.1.226（2026-08-10） | latest v2.1.226（2026-08-10）；stable 通常滞后约一周 |
| U3 | 一、快速安装 · allow-scripts FAQ 示例 | `@anthropic-ai/claude-code@2.1.224`（2 处） | 示例版本过时 | `@anthropic-ai/claude-code@2.1.226` |
| U4 | 二、跳过登录 · 方式四 permissions 可选值 | `"default"` — 每次操作都询问 | SB-04：权限模式 Default 改名 Manual | `"manual"` — 每次操作都询问 |
| U5 | 五、日常速查 · 启动命令 | `claude --model claude-sonnet-5`（默认 Sonnet 5）缺上下文 | SB-01：Sonnet 5 原生 1M 上下文、促销价 | 追加「2026-08 模型现状」callout（默认 Sonnet 5 + 1M + 促销价 + 默认 Opus 5） |
| U6 | 五、日常速查 · `/` 命令表 | `/model claude-opus-4.8` | SB-02：默认 Opus 为 Opus 5 | `/model claude-opus-5`（默认 Opus 5） |
| U7 | 五、日常速查 · `/` 命令表 | `/code-review` — 报告正确性错误 | SB-09：不再自动运行；`/review` 是别名 | 代码审查（`/review` 别名；手动调用；`--fix` 修复） |
| U8 | 五、日常速查 · `/` 命令表 | `/checkup` — 自诊断工具 | SB-10：`/doctor` 为全量环境体检，`/checkup` 是别名 | 改为 `/doctor` 行 |
| U9 | 五、日常速查 · `/` 命令表 | `/fork` — 创建临时会话分支 | SB-08：复制当前对话到新后台会话 | 复制当前对话到新后台会话 |
| U10 | 五、日常速查 · 2026 新增命令 tip | 未含 `/doctor` `/subtask`；`/checkup` 视为独立新命令 | SB-08/10 | 补 `/doctor` `/subtask`；注明 `/checkup`、`/review` 别名关系 |
| U11 | 五、日常速查 · 启动命令表 | 无权限模式入口 | SB-04：CLI `--permission-mode manual` | 新增行 `claude --permission-mode manual` |

## 新增（ADD）

| # | 位置 | 新增内容 |
|---|------|---------|
| A1 | 五、日常速查 · 启动命令表 | `claude --permission-mode manual` 行 |
| A2 | 五、日常速查 · 启动命令表后 | `[!tip] 2026-08 模型现状` callout（Sonnet 5 默认/1M/促销价、Opus 5 默认） |
| A3 | 五、日常速查 · `/` 命令表 | `/subtask` 行（会话内子代理，取代旧 in-session 子代理） |
| A4 | 八、更新记录 | 2026-08-10 变更行 |

## 保留（KEEP）

- 安装章节（方案 A/B/C/D、需放行域名表、Node 22+、ECONNREFUSED / native binary / allow-scripts FAQ）—— 仍有效
- 跳过登录章节（apiKeyHelper、env、hasCompletedOnboarding、setup-token、CC-Switch、Desktop 第三方配置）—— 仍有效
- 配置章节（providers/defaultProvider 非官方警告、`--settings` 多文件切换、第三方平台表）—— 已是最新
- 代理配置章节 —— 仍有效
- CLAUDE.md 章节 —— 仍有效
- 记忆系统章节（三层记忆、Auto Memory、.claudeignore、settings 记忆配置）—— 仍有效
- 常见问题与坑、安全建议、关联文档、参考资料 —— 仍有效

## 删除（DELETE）

无。未发现被废弃且需整段删除的内容。
