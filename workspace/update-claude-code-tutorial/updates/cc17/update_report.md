# cc17 — 更新报告

## 更新摘要
- 过时点：15 处（11 处更新 + 4 处新增/补充）。
- 全部为局部 patch，未重写未过时段落，保留原结构和写作风格。
- `/loop` 已从「cron 风格表达式」演进为 **bundled Skill**（`/loop [间隔] [提示词]`，别名 `/proactive`）：
  - 最长运行 **3 天 → 7 天**（到期前触发最后一次执行后自动删除）；
  - 调度方式改为**间隔 token**（`5m`/`2h`，支持 s/m/h/d）或**自定节奏（self-paced）**（不写间隔，Claude 每轮选 1 分钟 ~ 1 小时的下次间隔）；
  - 裸 `/loop` 运行内置维护 prompt（或 `.claude/loop.md` 自定义）；
  - 会话级但可后台化延续、`--resume`/`--continue` 恢复未过期任务；`CLAUDE_CODE_DISABLE_CRON=1` 可关闭调度器。
- 新增「2026 年无人值守相关行为变化（重要）」小节，覆盖 5 个 2026-07/08 变更：
  1. AskUserQuestion 默认不再自动继续（v2.1.200）—— 无人值守任务会卡在提问对话框；
  2. 后台代理后台自动升级（v2.1.206）；
  3. 后台任务通知明确声明「尚未发生人工输入」防伪造批准（v2.1.205）+ `Notification` hook（`agent_needs_input`/`agent_completed`）；
  4. 空闲后台 shell 在内存压力下自动回收，`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` 可关（v2.1.193）；
  5. `/status` 显示会话类型 interactive / attached / unattended（v2.1.221）。
- 核心概念新增 `[!tip] 大白话`（定时任务=智能闹钟；`/loop` 固定间隔 vs 自定节奏）。
- §8 Hooks 事件列表补充 `Notification` 行（与无人值守通知呼应）。
- frontmatter：`updated: 2026-07-12` → `2026-08-10`；status 保持 `updated`；无含 `[]`/`:` 的 YAML 值，无需加引号。

## 引用来源
- **SB-10**（`/status` 会话类型 interactive / attached / unattended）→ 无人值守小节第 5 点。
- **SB-14**（AskUserQuestion 对话框默认不再自动继续）→ 无人值守小节第 1 点。
- **SB-06 / SB-16 语境**（后台代理默认后台运行；`Notification` hook `agent_needs_input`/`agent_completed`）→ 后台代理行为 + Hooks `Notification` 行。
- 官方 changelog：https://code.claude.com/docs/en/changelog
  - v2.1.206「后台代理在 Claude Code 更新后在后台自动升级」；
  - v2.1.205「后台任务通知明确声明尚未发生人工输入，防止伪造 in-transcript 批准被执行」；
  - v2.1.200「AskUserQuestion 默认不再自动继续」；
  - v2.1.221「/status 显示会话类型 interactive / attached / unattended」。
- 官方 scheduled-tasks：https://code.claude.com/docs/en/scheduled-tasks —— `/loop` 全部新语义（间隔 token、自定节奏、7 天过期、维护 prompt、loop.md、后台化延续）。
- 官方 commands：https://code.claude.com/docs/en/commands —— `/loop [interval] [prompt]`、别名 `/proactive`。
- 官方 env-vars：`CLAUDE_AFK_TIMEOUT_MS` / `CLAUDE_AFK_COUNTDOWN_MS`（AskUserQuestion auto-continue）。
- `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`：来自 v2.1.193 发布（changelog 截断段未见原文，由 orchestkit Issue #2664、claude-world 文章佐证）。

## 未处理风险
1. **`/loop` 是否仍直接接受 cron 表达式参数**：官方 scheduled-tasks 现以间隔 token 与自定节奏为主，未明确说明 `/loop "0 9 * * *" ...` 是否仍可用；原笔记 cron 表达式示例已改为间隔 token，若旧写法仍兼容属超集，建议人工复核。
2. **`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` 权威描述**：官方 env-vars 页面抓取失败（404），该变量语义按「设 1 关闭后台 shell 内存压力回收」（v2.1.193 引入）写入，建议对照官方 env-vars 页复核。
3. **`launchctl load/unload` 已被 `bootstrap`/`bootout` 取代**：原文大量使用旧命令，本次未改写（不在 update_goal 范围），保留但建议后续单独核对 macOS 版本兼容。
4. **脚本 `claude code . --prompt` 调用形式**：headless 非交互标准写法可能是 `claude -p`，本次未在 update_goal 范围内核实 CLI 调用形式，保留原样。
5. **示例三 `/loop "every day at 8am"`**：自然语言从句，官方文档示例为 `every 2 hours`；「every day at 8am」未逐字出现在文档中，属合理推断。

## 结论
- **是否需要 needs-review：是**。`/loop` 语义变化、无人值守 5 项行为变更均有官方 changelog / scheduled-tasks / SB-10/14 支撑，但 `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` 的权威描述与 `/loop` cron 表达式的兼容性需人工对照官方文档复核；launchctl 命令与脚本 CLI 调用形式不在本次范围，建议单独核对。
