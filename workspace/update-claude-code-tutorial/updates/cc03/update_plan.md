# cc03 更新计划 — Claude Code CLI 完整参考

## 过时点（对应 stale_map 更新项）

1. **版本行过时**：笔记标注 v2.1.207（2026-07-11），共享来源库已覆盖到 v2.1.226（2026-08-10）。
2. **权限模式名过时**：`default` 权限模式改名 `manual`（SB-04），`--permission-mode` 描述与示例需更新。
3. **`--max-budget-usd` 语义过时**：SB-05 明确该标志达到上限会停止后台子代理，原描述只提「Print 模式最大花费」。
4. **`claude agents` / `/status` 缺失**：SB-10/SB-21，`/status` 显示会话类型（interactive / attached / unattended）。
5. **环境变量缺新项**：SB-05/SB-06/SB-13/SB-15，新增 5 个环境变量。

## 更新计划

| 步骤 | 动作 | 说明 |
|------|------|------|
| 1 | 更新 frontmatter `updated`、`status` | 设为 2026-08-10 / updated |
| 2 | 更新概述版本行 | v2.1.226（2026-08-10） |
| 3 | 更新 `--permission-mode` 行 + 大白话 | 说明 default→manual（SB-04） |
| 4 | 更新 `--max-budget-usd` 行 | 补充停止后台子代理语义（SB-05） |
| 5 | 新增 `--forward-subagent-text`、`--ax-screen-reader` | 输出格式表 / 高级标志表（SB-05/SB-15） |
| 6 | 更新 `claude agents` 行 + 代理配置节说明 | `/status` 会话类型（SB-10） |
| 7 | 环境变量表新增 5 项 | 并发、嵌套深度、1M 压缩、屏读、鼠标点击（SB-05/SB-06/SB-13/SB-15） |
| 8 | 追加 `## 更新记录` | 日期 + 变更摘要 |

## 核对项（无变更）

- **管道模式**：`-p` / `--input-format` / `--output-format` 描述与 2026-08 现状一致，无过时。
- **启动参数**：`claude` / `-n` / `-c` / `-r` 等仍有效。
- **退出码**：笔记仅有 `claude auth status`（已登录 0 / 未登录 1），仍有效；笔记无独立退出码章节，无需改动。
