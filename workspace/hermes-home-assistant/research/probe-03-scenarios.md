# 探测原始记录 03：LLM Agent 控制 / 自动化 Home Assistant 的真实用例

> **性质**：原始证据记录，**不是**阶段 1 的交付物 `01_explore_result.md`，不推进任何阶段状态。
> **来源**：后台核验子代理（场景探测），核对日期 2026-09-18。已先读 probe-01 / probe-02 与 `workspace/hermes-agent/research/`（HA 专页缺失，仅 3 处零散提及）。
> **引用纪律**：写入正文前逐条回源比对；标「二次来源」与「待核对」的内容不得直接引用。

## 场景清单

| 场景名 | 一句话机制 | 需要哪些能力（HA 侧 + agent 侧） | 来源 | 原文关键句 |
|---|---|---|---|---|
| 语音控制（Assist） | 实体暴露给 Assist 后，语音经 conversation agent 转成 intent，由 LLM 决定调哪个 service | HA：Assist 管道 + 实体 expose + conversation agent；Agent：LLM tool-calling | 官方 /voice_control/、/voice_control/voice_remote_expose_devices/、HA 博客 2025-09-11 | "Assist is the voice assistant built into Home Assistant." / "To be able to control your devices over a voice command, you must expose your entities to Assist." |
| 自然语言控制与批量操作 | 一个 service call 用 `target` 同时命中多个 entity/area/device，LLM 只需生成一次调用 | HA：`target` 支持 `entity_id`/`area_id`/`device_id` 列表、`entity_id: all`、light group；Agent：`ha_call_service` 的 `entity_id`+`data` | 官方 /docs/scripts/service-calls/；Hermes docs homeassistant.md | "A `target` is a map that contains at least one of the following: `area_id`, `device_id`, `entity_id`." / "You can also use `entity_id: all` and it will turn on all possible entities." |
| 事件驱动的主动响应 | HA 侧 `state_changed` 经 WebSocket 推给 agent，命中白名单的事件被当作一条用户消息投递，agent 自行决定动作 | HA：WebSocket `subscribe_events`、自动化可先做粗筛；Agent：事件订阅 + 过滤白名单 + cooldown | Hermes docs user-guide/messaging/homeassistant.md | "connects via WebSocket and subscribes to `state_changed` events" / "When a device state changes and matches your filters, it's forwarded to the agent as a message." / "By default, **no events are forwarded**." |
| HA 自己发起对话（官方对照路线） | HA 主动向用户发起对话，把「车库门开着，要不要关」这类判断交给 LLM | HA：2025.9+ 主动对话能力 + conversation agent；Agent：可被 HA 反向调用 | HA 博客 2025-09-11「AI in Home Assistant」 | "you can now have Home Assistant initiate conversations." / "you could set up an automation that detects when the garage door is open and asks if you'd like to close it" |
| 日报与巡检 | 定时触发器（或 cron）跑一次只读巡检，产出文本后经 notify/persistent_notification 送达 | HA：`time`/`time_pattern` 触发器、`notify.*`、`persistent_notification.create`、`sensor.*` 暴露结果；Agent：cron 调度 + 只读工具白名单 | 项目一手 cnc-lasercraft/haclaude（README，德文）；Hermes docs features/cron；官方 /integrations/persistent_notification/ | haclaude: "zeit- und ereignisgesteuerte Analysen (nächtlicher Systemcheck, Abwesenheitskontrolle)"；Hermes cron 投递目标表含 `"homeassistant"` |
| 日报（无 LLM 的对照实现） | 同一场景可完全确定性地拼装文本，再由自动化定时推送 | HA：service 返回 `response data`、`sensor.household_briefing` 属性、`household_briefing_generated` 事件 | 项目一手 archieboy-holdings/ha-household-briefing（README） | "weather, today's calendar, who's home, what's open, unlocked, or left on" / "No cloud. No API keys. No LLM. No subscription." |
| 异常告警（电池 / 漏水 / 离线） | HA 侧用 `numeric_state` 阈值或 Alert 集成做确定性判定与重复提醒，LLM 只做措辞/分级 | HA：Alert 集成（`repeat`、`can_acknowledge`）、`numeric_state`/`template` 触发器；Agent：写自动化或生成通知文案 | 官方 /integrations/alert/ | "This is also used for low battery sensors, water leak sensors, or any condition that may need your attention." / "Number of minutes before the notification should be repeated." |
| 异常告警（LLM 学基线，而非阈值） | 每夜对历史状态做 z-score（均值+标准差）重算基线，只有持续偏离才报，避免一小时抖动误报 | HA：recorder 历史数据 + 实体状态流；Agent：持久记忆、夜间批处理、per-device 基线 | 项目一手 Oasis-Enterprise/mylo（README，Apache-2.0） | "a z-score check against a 7-day baseline (mean + standard deviation), recomputed nightly" / "one-hour blips don't alert" / "Mylo never sends push or HA notifications." |
| 场景联动（离开家 / 回家） | `zone` 触发器在 person/device_tracker 进入或离开时触发自动化；巡检类 agent 用它当触发条件 | HA：`zone` 触发器（entity 为 `person` 或 `device_tracker`）、`person`/`device_tracker` 集成；Agent：被自动化以 service 唤起 | 官方 /docs/automation/trigger/；haclaude README | "Zone trigger fires when an entity is entering or leaving the zone." / "The entity can be either a person or a device tracker."；haclaude 触发条件含 "alle weg" |
| 跨平台遥控（手机 IM 遥控家居） | 手机 IM 双向管道：入站文本 → LLM → 工具 → HA REST/MCP；出站走 notify | HA：Telegram 集成（long polling 无需公网）、`telegram_text`/`telegram_command` 事件、chat ID 白名单；Agent：IM 平台适配器 + 工具调用 | 官方 /integrations/telegram_bot/；社区帖 1003703 | "Use Telegram on your mobile or desktop device to send and receive messages or commands to/from your Home Assistant." / "You must allowlist the chat ID for the Telegram bot before it can send/receive messages for that chat." / 社区："control your home in plain English via Telegram or a web interface — no voice, no app, just chat" |
| 跨平台遥控 + 危险操作闸门 | 会话里可读可调光；写配置/删自动化/重启 HA 这类持久化动作必须口头确认，且由确定性 hook 拦工具调用 | HA：MCP server 或 REST；Agent：MCP 工具过滤（include/exclude）、`trust: untrusted`、Approval 面 | Hermes toolsets-reference / mcp-config-reference；社区帖 1003803 | Hermes 官方: "On an `untrusted` server, every write-capable tool call ... requires user approval through the standard approval surface" / 社区："a deterministic `PreToolUse` approval hook blocks the actual destructive tool call unless the user's latest message is an explicit confirmation" |
| 结合传感器历史的建议 | 用 `recorder.get_statistics` 取长期聚合（周最高温、平均温），把数学交给工具而不是模型心算 | HA：recorder 长期统计 + `recorder.get_statistics` service；Agent：把统计封成工具/脚本供模型调用 | 官方 /integrations/recorder/；社区帖 908474 | 官方: "`recorder.get_statistics` — Retrieves long-term statistics for one or more entities."；社区："The reason for this are usually mathematical correlations" / "Always, really always use the tools provided when possible to get the solution." |
| 自然语言生成并注册自动化 | 模型产出 automation YAML，由 agent 写回 HA 配置；可靠性靠挂载真实沙箱验证而非「能加载」 | HA：`ha_config_set_automation` 类工具 / config API；Agent：写工具 + 验证回路 | 项目一手 goruck/home-generative-agent；社区帖 1003803 | "Describe what you want in chat and the agent writes and registers the HA automation."；社区："create automations from natural language" |
| 结构化数据 / 摄像头判断 | `ai_task.generate_data` 在自动化、脚本、模板实体里直接调 AI，可带 `structure` 字段与 camera 附件 | HA：AI Task 集成（`ai_task.generate_data`、`generate_image`）、`media-source://camera/...`；Agent：被 HA 当作子任务调用 | 官方 /integrations/ai_task/；HA 博客 2025-09-11 | "Uses AI to run a task that generates data, such as text or structured output." / "its true superpower is making AI easy to use in templates, scripts, and automations." / "An automation triggers an AI Task to identify what caused motion on a camera." |
| 对话式建议按钮 | 在自动化编辑界面用 Suggest 生成名称/描述/分类/标签，依赖已配置 AI Tasks 实体 | HA：AI Tasks 实体 + Suggest 按钮 | HA 博客 2025-09-11 | "users can now leverage the new Suggest button" / "If you don't configure an AI Tasks entity, the Suggest button will not be visible." |

## 本轮最重要的结构性结论

**全部场景在 Hermes 侧只落在 4 个内置工具内。**「历史/统计」「写自动化」「摄像头」三类场景在 Hermes 内置工具下**无对应工具**，必须靠 MCP 或自定义 plugin 才能落地。

## 待核对

1. Hermes HA 平台页**未文档化** cron 投递到 HA，也未给报告类用例——「日报与巡检」的 Hermes 侧只由 `cron.md` 的 `"homeassistant"` 目标支撑，未在同一页看到端到端示例
2. Hermes 官方页只写 `persistent_notification.create`；`notify.notify` 只见于源码 `_standalone_send()`，页面无对应语句（probe-02 同此）
3. `xda-developers`、`hasspodcast.io`、SkillsMP、hacf/hassbian 论坛均属**二次来源**，本表未据其立论
4. Oasis-Enterprise/mylo 的 z-score / 14 天行为模式细节来自 README 自述，未审源码
5. archieboy-holdings/ha-household-briefing 明确「无 LLM」，仅作同场景的确定性对照
6. haclaude 工具白名单 README 未逐项列出，"strikt lesend (Tool-Allowlist)" 无法核对具体工具集
7. 社区帖 1003703 / 1003803 的「可用性、延迟、安全」均为作者自报，无第三方复现
8. HA 博客 2025-09-11 中「HA 主动发起对话」「Suggest」的确切版本门槛来自二次检索摘要，需回 release notes 逐版比对
9. 「历史/统计」「写自动化」「摄像头」三类场景需 MCP 或自定义 plugin 才能落地（同 probe-02 待核对第 4 条）

## 来源 URL 汇总

- https://www.home-assistant.io/voice_control/
- https://www.home-assistant.io/voice_control/voice_remote_expose_devices/
- https://www.home-assistant.io/docs/scripts/service-calls/
- https://www.home-assistant.io/docs/automation/trigger/
- https://www.home-assistant.io/integrations/alert/
- https://www.home-assistant.io/integrations/recorder/
- https://www.home-assistant.io/integrations/ai_task/
- https://www.home-assistant.io/integrations/telegram_bot/
- https://www.home-assistant.io/integrations/persistent_notification/
- https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/
- https://developers.home-assistant.io/docs/core/llm/
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://github.com/cnc-lasercraft/haclaude
- https://github.com/goruck/home-generative-agent
- https://github.com/Oasis-Enterprise/mylo
- https://github.com/archieboy-holdings/ha-household-briefing
- https://community.home-assistant.io/t/.../1016481 （Hestia）
- https://community.home-assistant.io/t/.../908474 （cheap models + tools）
- https://community.home-assistant.io/t/.../1003703 （Telegram OpenClaw skill）
- https://community.home-assistant.io/t/.../1003803 （SmartHub）
