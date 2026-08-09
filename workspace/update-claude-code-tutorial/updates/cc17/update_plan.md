# cc17 — 更新计划（update_goal 对齐）

## 过时点清单

| # | 位置 | 过时内容 | 更新动作 | 来源 |
|---|------|----------|----------|------|
| 1 | frontmatter | `updated: 2026-07-12` | 改为 `2026-08-10`；status 保持 `updated` | — |
| 2 | 顶部「更新说明」tip | `/loop` 最长运行 3 天、cron 风格调度；锚点 `#10-` | 改为 7 天、固定间隔/自定节奏；锚点改 `#9-` | scheduled-tasks 官方文档 |
| 3 | 核心概念「是什么」表 | `/loop` 行「最长运行 3 天、cron 风格调度」 | 改为「最长 7 天、固定间隔或自定节奏」 | scheduled-tasks 官方文档 |
| 4 | 核心概念 | 缺大白话 | 新增 `[!tip] 大白话`（定时任务=智能闹钟；`/loop` 固定间隔 vs 自定节奏） | — |
| 5 | §9 核心特性表 | 最长 3 天；调度=Cron 风格；运行范围=会话结束终止 | 改为 7 天；间隔 token/自定节奏；后台化可延续、`--resume` 恢复；新增别名 `/proactive` | scheduled-tasks 官方文档 |
| 6 | §9 基本语法 | `/loop <cron表达式> <任务描述>` | 改为 `/loop [间隔] [提示词]` + 三种组合行为表 + 间隔单位（s/m/h/d）说明 | scheduled-tasks 官方文档 |
| 7 | §9 实用示例 | 三个示例用 cron 表达式 | 改为间隔 token（`5m`/`30m`/`every 2 hours`） | scheduled-tasks 官方文档 |
| 8 | §9 `/loop` vs 系统级对照表 | 最长 3 天；缺调度方式维度 | 改为 7 天；新增「调度方式」行；会话依赖行补充后台化延续 | scheduled-tasks 官方文档 |
| 9 | §9 最佳实践组合示例 | `/loop "*/30 * * * *"` | 改为 `/loop 30m` | scheduled-tasks 官方文档 |
| 10 | §9 注意事项 | 「会话结束后终止」「3 天限制」 | 补充后台化会话延续、`--resume`/`--continue` 恢复、Routines/Desktop 兜底；3 天→7 天 + `CLAUDE_CODE_DISABLE_CRON=1` | scheduled-tasks 官方文档 |
| 11 | 非交互模式权限节 | 缺 2026 无人值守行为变化 | 新增小节：AskUserQuestion 不再自动继续（v2.1.200）；后台代理后台自动升级（v2.1.206）；后台通知声明「尚未发生人工输入」（v2.1.205）+ Notification hook；内存压力回收 + `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`（v2.1.193）；`/status` 会话类型（v2.1.221） | SB-14 / SB-06 / SB-10 + changelog 专项 |
| 12 | 常见问题 | `/loop` 最长 3 天；「会话关闭后不会继续运行」 | 改为 7 天；补充后台化延续、resume 恢复 | scheduled-tasks 官方文档 |
| 13 | 参考资料 | `/loop` 区缺官方当前文档 | 补 scheduled-tasks、env-vars 链接，标注别名 `/proactive` | scheduled-tasks 官方文档 |
| 14 | 结尾 | 无更新记录 | 追加 `## 更新记录` | — |

## 核对结论
- `/loop` 已从「cron 风格表达式」演化为 **bundled skill**：`/loop [interval] [prompt]`，间隔 token（`5m`/`2h`，s/m/h/d）或让 Claude 自定节奏（1 分钟 ~ 1 小时）；最长运行 **7 天**（原 3 天）；别名 `/proactive`。原笔记的 cron 表达式示例与 3 天限制全部过时。
- AskUserQuestion（v2.1.200）默认不再自动继续 —— 对 cron/launchd 无人值守调度是**新的卡死风险**，需在权限方案中提示结合 `--dangerously-skip-permissions` 或 `askUserQuestionTimeout`。
- 后台任务行为新增 3 点（后台自动升级 v2.1.206 / 通知声明「无人工输入」v2.1.205 / 内存压力回收 v2.1.193）与 `/status` 会话类型（v2.1.221），均为 2026-07/08 变更，原笔记完全未覆盖。

## 不做（刻意排除）
- `launchd`/`cron`/`launchctl` 系统级配置细节：本笔记更新目标不含系统级调度的改写（`launchctl load` 仍兼容但已被 `bootstrap`/`bootout` 取代，见报告风险）。
- Hooks 事件列表深挖：属于 cc08 更新范围，本笔记仅引用不扩展。
- 不重写全部 Shell 脚本的 `claude code . --prompt` 调用形式（非本次 update_goal 范围，见报告风险）。
