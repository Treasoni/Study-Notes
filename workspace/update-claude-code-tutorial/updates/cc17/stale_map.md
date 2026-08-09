# cc17 — Claude Code 定时任务自动化指南 — Stale Map

> 更新基线：2026-08-10（覆盖 v2.1.193 ~ v2.1.226）
> 核对来源：SB-14、SB-06、SB-10（shared_source_bank）+ 官方 changelog / scheduled-tasks / env-vars 专项资料

## 保留（KEEP）
- 前置准备、基础定时脚本、launchd/cron 配置示例、plist 参数表、launchctl 命令 —— 系统级调度概念未过时
- 实用自动化模式（备份/依赖监控/重构）、高级技巧（条件执行/锁）、错误处理与通知 —— 未过时
- Hooks 集成章节 —— 未过时（本笔记不深挖 Hooks）
- launchd 替代 cron 的休眠补偿机制 —— 仍正确
- 非交互模式权限问题的方案一~四（`--dangerously-skip-permissions`、`--allowedTools`、settings.json 预设、Docker 隔离）—— 仍是有效手段
- 完整模板、调试技巧、常见问题（除 `/loop` 相关 2 条）—— 未过时

## 更新（UPDATE）
1. frontmatter `updated: 2026-07-12` → `2026-08-10`（status 保持 `updated`）
2. 顶部「更新说明」tip：`/loop` 最长运行 **3 天 → 7 天**；调度描述「cron 风格调度」→「固定间隔或自定节奏（self-paced）」；锚点 `#10-官方方案-loop-命令推荐` → `#9-官方方案-loop-命令推荐`（实际标题为 9）
3. 核心概念「是什么」对照表 `/loop` 行：最长运行 3 天 → 7 天；cron 风格调度 → 固定间隔或自定节奏【官方 scheduled-tasks 专项】
4. §9 `/loop` 核心特性表：最长运行 3 天 → 7 天；「调度方式：Cron 风格时间表达式」→「间隔 token（s/m/h/d）或让 Claude 自定节奏」；「运行范围：会话结束终止」→ 补充后台化会话延续、`--resume` 恢复；新增「别名 `/proactive`」行
5. §9 `/loop` 基本语法：`/loop <cron表达式> <任务描述>` → `/loop [间隔] [提示词]`，三种组合（固定间隔 / 自定节奏 / 内置维护 prompt）+ 间隔单位说明
6. §9 `/loop` 实用示例：cron 表达式参数 → 间隔 token 参数（`5m`、`30m` 等）
7. §9 `/loop` vs 系统级调度对照表：最长运行 3 天 → 7 天；会话依赖行补充「后台化可延续、`--resume` 可恢复」；新增「调度方式」行
8. §9 最佳实践组合示例：`/loop "*/30 * * * *"` → `/loop 30m`
9. §9 注意事项：会话限制补充后台化会话延续、`--resume`/`--continue` 恢复、Routines/Desktop 兜底；「3 天限制」→「7 天限制」+ `CLAUDE_CODE_DISABLE_CRON=1`
10. 常见问题 `/loop` 相关 2 条：最长 3 天 → 7 天；「会话关闭后任务终止」→「默认终止，但后台化可延续、resume 可恢复」
11. 参考资料 `/loop` 区：补充官方 scheduled-tasks、env-vars 链接，标注别名 `/proactive`

## 新增（ADD）
1. §核心概念 大白话 `[!tip] 大白话`（是什么 / `/loop` 两种模式）
2. §8 Hooks 事件列表：补充 `Notification` 行（`agent_needs_input` / `agent_completed`），与无人值守通知相呼应【SB-16 语境】
3. §非交互模式权限 新小节「2026 年无人值守相关行为变化（重要）」：
   - AskUserQuestion 默认不再自动继续（v2.1.200），无人值守任务会卡在提问对话框 → 结合 `--dangerously-skip-permissions` 或 `askUserQuestionTimeout`；`CLAUDE_AFK_TIMEOUT_MS` / `CLAUDE_AFK_COUNTDOWN_MS`【SB-14 / SB-21 + 官方 env-vars】
   - 后台代理后台自动升级（v2.1.206）【专项】
   - 后台任务通知明确声明「尚未发生人工输入」，防止伪造批准（v2.1.205）+ `Notification` hook（`agent_needs_input`/`agent_completed`）【专项 / SB-16 语境】
   - 空闲后台 shell 命令在内存压力下自动回收；`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` 可关（v2.1.193）【专项】
   - `/status` 显示会话类型 interactive / attached / unattended（v2.1.221）【SB-10】
4. `## 更新记录` 章节

## 删除（DELETE）
- 无整段删除；仅局部替换过时的 `/loop` 时长（3 天）、调度语法（cron 表达式）与运行范围描述（会话结束即终止）。
