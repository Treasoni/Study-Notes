# 英文残留勘查报告（只读，不改笔记）
源文件：`D:/Study-Notes/AI学习/04-项目实践/自托管 Agent 选型/自托管 Agent 平台选型.md`（703 行）
唯一反引号片段：274（cite 90 / 疑似代码散文 21 / 其余 163）

## A. 反引号内「疑似散文但被判为代码」——需人工确认是否翻译

| # | 首次行 | 章 | 次数 | 词数 | 片段 |
| --- | --- | --- | --- | --- | --- |
| 7 | 53 | 1 | 1 | 11 | `Manage the Octop system service (systemd on Linux, launchd on macOS).` |
| 43 | 129 | 1 | 2 | 6 | `The recurring comparison is [Hermes Agent]` |
| 61 | 177 | 2 | 3 | 10 | `Sender routing selects a profile; it is not deny-by-default authorization.` |
| 81 | 201 | 2 | 2 | 15 | `Every allowed user falls into one of two tiers per scope (DM vs group/channel):` |
| 118 | 312 | 3 | 1 | 9 | `row.user_id is not None and row.user_id == user.id` |
| 121 | 312 | 3 | 1 | 8 | `row.user_id is None or row.user_id != user.id` |
| 150 | 368 | 4 | 1 | 23 | `Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop` |
| 163 | 382 | 4 | 1 | 16 | `With gateway.multiplex_profiles: true one process serves the default profile plus every live directory under profiles/` |
| 165 | 384 | 4 | 1 | 14 | `The model only remembers what gets saved to disk; there is no hidden state.` |
| 176 | 432 | 5 | 1 | 7 | `**Octop** — self-hosted AI assistant platform (multi-user, multi-agent).` |
| 181 | 453 | 5 | 1 | 22 | `Everything runs in a single Python process served by uvicorn. There is no external queue (Redis, RabbitMQ, Celery), no separate worker process` |
| 190 | 459 | 5 | 1 | 8 | `\| OCTOP_DATABASE_DRIVER \| sqlite \| postgresql \| sqlite \| Storage backend \|` |
| 197 | 476 | 5 | 1 | 8 | `- Single active Octop writer; no multi-instance write promise.` |
| 210 | 497 | 5 | 1 | 8 | `- Control plane SQLite → agent memory stays {workspace}/memory.sqlite` |
| 224 | 537 | 6 | 1 | 9 | `The [comparison table](...) condenses the source-verified contrast with Hermes.` |
| 231 | 541 | 6 | 1 | 19 | `Use one cell for each tenant trust boundary; do not use one shared Gateway as a hostile multi-tenant boundary.` |
| 236 | 545 | 6 | 1 | 22 | `The comparison below reflects source at 6defe7eb6c (reviewed August 27, 2026), not a live adversarial test or a guarantee about every deployment.` |
| 250 | 557 | 6 | 1 | 18 | `**During first-time setup:** The setup wizard (hermes setup) automatically detects ~/.openclaw and offers to migrate before configuration begins.` |
| 252 | 558 | 6 | 1 | 6 | `_OPENCLAW_DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot")` |
| 264 | 561 | 6 | 1 | 12 | `Secrets are never included implicitly: --migrate-secrets is required even under --preset full` |
| 267 | 569 | 6 | 1 | 12 | `\| **Outbound** \| OpenCode, CodeBuddy, … \| Octop (acp_runner tool) \| Octop agent delegates coding tasks \|` |

## B. 反引号之外的英文串（>= 2 词）——全部

| # | 串 | 次数 | 首次行 | 章 |
| --- | --- | --- | --- | --- |
| 1 | ACP runner | 5 | 145 | 1 |
| 2 | vs Hermes | 2 | 19 | 0 |
| 3 | It's not tied to your laptop | 2 | 19 | 0 |
| 4 | AI Agent | 1 | 7 | 0 |
| 5 | Claude Code | 1 | 41 | 1 |
| 6 | Codex CLI | 1 | 41 | 1 |
| 7 | Observation interface | 1 | 96 | 1 |
| 8 | Context manager | 1 | 97 | 1 |
| 9 | Control loop | 1 | 98 | 1 |
| 10 | Action interface | 1 | 99 | 1 |
| 11 | State and artifact store | 1 | 100 | 1 |
| 12 | Verification and governance layer | 1 | 101 | 1 |
| 13 | OpenHands issue | 1 | 149 | 1 |
| 14 | session ownership | 1 | 184 | 2 |
| 15 | participant history | 1 | 184 | 2 |
| 16 | live presence | 1 | 184 | 2 |
| 17 | owner filtering | 1 | 184 | 2 |
| 18 | Slack workspace | 1 | 238 | 2 |
| 19 | agent id | 1 | 239 | 2 |
| 20 | tenant id | 1 | 239 | 2 |
| 21 | agent X | 1 | 312 | 3 |
| 22 | List installed plugins | 1 | 316 | 3 |
| 23 | list users | 1 | 317 | 3 |
| 24 | list role templates | 1 | 317 | 3 |
| 25 | agent runtime | 1 | 457 | 5 |
| 26 | Zero external dependencies | 1 | 470 | 5 |
| 27 | Vertical scaling only | 1 | 470 | 5 |
| 28 | one machine | 1 | 470 | 5 |
| 29 | Simple deployment | 1 | 471 | 5 |
| 30 | one process | 1 | 471 | 5 |
| 31 | one port | 1 | 471 | 5 |
| 32 | Heavy CPU tasks block the event loop | 1 | 471 | 5 |
| 33 | Fast local dev | 1 | 472 | 5 |
| 34 | No horizontal worker scaling | 1 | 472 | 5 |
| 35 | MCP servers | 1 | 559 | 6 |
| 36 | Approval rules | 1 | 559 | 6 |
| 37 | vs docs | 1 | 580 | 6 |
| 38 | plain chat | 1 | 636 | 7 |
| 39 | openclaw/OpenClaw MOC | 1 | 699 | 7 |
| 40 | Hermes Agent/Hermes Agent MOC | 1 | 701 | 7 |
| 41 | Hermes Agent | 1 | 701 | 7 |

## C. 含英文的标题行

| 行 | 章 | 标题 |
| --- | --- | --- |
| 7 | 0 | # 自托管 AI Agent 平台选型（Octop / OpenClaw / Hermes） |
| 131 | 1 | ### 1.5 为什么不能拿 Star 数当依据 |
| 182 | 2 | ### 2.2 OpenClaw：同一信任域内的协作 |
| 197 | 2 | ### 2.3 Hermes：准入与很窄的分级 |
| 212 | 2 | ### 2.4 Octop：行级归属 |
| 230 | 2 | ### 2.6 两个边界：多用户平台 ≠ 多租户平台，以及两处 tenant 假阳性 |
| 276 | 3 | ### 3.2 弱档：OpenClaw 明确声明不提供隔离 |
| 287 | 3 | ### 3.3 中档：Hermes 准入与很窄的分级 |
| 302 | 3 | ### 3.4 强档：Octop 行级归属 |
| 328 | 3 | ### 3.5 强档也有例外：隔离可由 owner 主动放宽 |
| 344 | 4 | ## 第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」vs Hermes「It's not tied to your laptop」 |
| 417 | 5 | ## 第 5 章 Octop 回答的是不是另一个问题 —— 单实例多用户平台，家庭与小团队 |
| 439 | 5 | ### 5.2 官方 Scope 限定：家庭与小团队 |
| 532 | 6 | ### 6.2 OpenClaw 侧：有官方对照专页，README 却零提及 |
| 552 | 6 | ### 6.3 Hermes 侧：迁移命令是双向同层的铁证 |
| 565 | 6 | ### 6.4 Octop 侧：双向零提及，参照物不在这一桌 |
| 671 | 7 | ### 7.7 换一个新 agent 时的提问清单 |
