# 探测原始记录 06：三方对照轴（HA 内建 LLM / 外部 agent / 纯确定性自动化）

> **性质**：原始证据记录，**不是**阶段 2 的交付物 `02_deep_research.md`，不推进任何阶段状态。
> **来源**：P2 精读子代理 C「three-way comparison axis」，检索日期 2026-09-18。
> **引用纪律**：标 **【子代理采集】** 的条目子代理未二次回源；写入正文前必须直读核验。
> 本轮记录含两处**推翻上一阶段结论**的更正，见文末「矛盾与存疑」第 3、8 条与「对上一阶段记录的更正」节。

本地快照目录：`D:\Study-Notes\workspace\hermes-home-assistant\sources\`（按页面分子目录，避免覆盖）；GitHub README 存于 `sources\gh\`。

---

## 待确认项 1 | HA 内建 LLM 的边界

**HA-01** | Conversation - Home Assistant | https://www.home-assistant.io/integrations/conversation/ | 官方文档 | 无显式更新日期（抓取 2026-09-17T16:37Z） | 页首 intro / `## Sentence triggers` | 该页**通篇没有**「LLM 只能控制 exposed 实体」这类边界语句——它描述的是**内建非 LLM** conversation agent（`conversation:` + 社区句子）。唯一与 LLM 相关的边界为逐字原文：「Sentence triggers start an automation when Assist matches a sentence. They use the default conversation agent and work with Home Assistant Assist. External conversation agents, such as OpenAI Conversation or Google Generative AI Conversation, only use sentence triggers when **Prefer handling commands locally** is enabled.」本地路径 `sources\conversation\` | 2026-09-18

**HA-02** | OpenAI - Home Assistant | https://www.home-assistant.io/integrations/openai_conversation/ | 官方文档 | 无显式更新日期 | `## Prerequisites` > Important（第 13 行）；配置项 `Control Home Assistant` 说明（第 52 行）；`## Known limitations`（第 9 行） | 逐字原文三条：①「This integration works only with the official OpenAI API endpoint and does not support OpenAI-API-compatible third-party services, proxies, or alternative backends. If you need support for other providers, consider using the [OpenRouter integration] as an alternative.」②配置项说明「If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed] to it.」③「This integration does not integrate with [sentence triggers].」本地路径 `sources\openai_conversation\` | 2026-09-18

**HA-03** | Anthropic - Home Assistant | https://www.home-assistant.io/integrations/anthropic/ | 官方文档 | 无显式更新日期 | intro（第 8 行）；`Control Home Assistant` 配置项（第 50 行）；`## Known limitations`（第 163 行） | 三条逐字原文：①「Controlling Home Assistant is done by providing the AI access to the Assist API of Home Assistant. You can control what devices and entities it can access from the [exposed entities page]. The AI can provide you information about your devices and control them.」②「If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed] to it.」③「This integration does not integrate with [sentence triggers].」另附成本提示「This is a paid service, we advise you to monitor your costs in the [Anthropic portal] closely.」本地路径 `sources\anthropic\` | 2026-09-18

**HA-04** | Google Generative AI - Home Assistant | https://www.home-assistant.io/integrations/google_generative_ai_conversation/ | 官方文档 | 无显式更新日期 | intro（第 8 行）；`Control Home Assistant` 配置项（第 40 行）；Known limitations（第 9 行） | 与 HA-03 同构：intro 逐字「Controlling Home Assistant is done by providing the AI access to the Assist API of Home Assistant.…The AI can provide you information about your devices and control them.」；配置项逐字「If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed] to it.」；「This integration does not integrate with [sentence triggers].」本地路径 `sources\google_genai\` | 2026-09-18

**HA-05** | Ollama - Home Assistant | https://www.home-assistant.io/integrations/ollama/ | 官方文档 | 无显式更新日期 | intro（第 8 行）；配置项（第 39 行）；`## Controlling Home Assistant`（第 49–55 行） | 全部**逐字确认**且**比上一阶段报告更完整**：①「Controlling Home Assistant is **an experimental feature that** provides the AI access to the Assist API of Home Assistant.」（原文是整句，非截断的 "Controlling Home Assistant is an experimental feature"）②「If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed] to it. This feature is considered experimental and see [Controlling Home Assistant] below for details on model limitations.」③「If you want to experiment with local LLMs using Home Assistant, we recommend exposing fewer than 25 entities. Note that smaller models are more likely to make mistakes than larger models.」④「Only models that support [Tools] may control Home Assistant.」⑤「Smaller models may not [reliably maintain a conversation] when controlling Home Assistant is enabled.」⑥官方给出的降级方案：同一模型跑两个 Ollama 配置，一个不启用控制、一个启用控制。本地路径 `sources\ollama\` | 2026-09-18

**HA-06** | Exposing entities to Assist | https://www.home-assistant.io/voice_control/voice_remote_expose_devices/ | 官方文档 | 无显式更新日期 | 全文（该页仅 1187 字） | 边界的设计意图逐字原文：「To be able to control your devices over a voice command, you must expose your entities to Assist. This is to avoid that sensitive devices, such as locks and garage doors, can inadvertently be controlled by voice commands.」操作路径逐字：**Settings** > **Voice assistants** > **Expose** tab；可分别 expose 给 "Assist, Google Assistant, and/or Alexa"；批量入口为 **Expose entities** 按钮。本地路径 `sources\expose_devices\` | 2026-09-18

**HA-07** | Assist - Talk to your smart home | https://www.home-assistant.io/voice_control/ | 官方文档 | 无显式更新日期 | intro（第 7–9 行）、文末（第 128 行） | 该页**不含**任何 exposed-entity 控制边界语句（边界在 HA-06）。可用的官方定位口径逐字：「Assist is the voice assistant built into Home Assistant. It lets you control your smart home with natural language, and it can run fully on your own hardware, so your voice commands stay private.」「It can work locally or, if you prefer, use one of the latest large language models to handle more conversational requests.」实体内建句子/自定义句子入口为 `builtin_sentences` / `custom_sentences`；「_Assist was introduced in Home Assistant 2023.2._」本地路径 `sources\voice_control\` | 2026-09-18

> **待确认项 1 结论**：四条引用全部回源成功，但**归属需修正**——「It can only control or provide information about entities that are exposed to it.」不是 intro 段落，而是四个 LLM 集成页上 **`Control Home Assistant` 配置项的说明文字**，且原文前还有一句「If the model is allowed to interact with Home Assistant.」；该句**不在** `/integrations/conversation/`，也**不在** `/voice_control/`。

---

## 待确认项 2 | HA 给 LLM 的开发者接口（`developers.home-assistant.io/docs/core/llm/`）

**DEV-01** | Home Assistant API for Large Language Models | https://developers.home-assistant.io/docs/core/llm/ | 官方文档（开发者文档） | 无显式更新日期（抓取 2026-09-17T16:39Z） | intro + `## Built-in Assist API` | 抽象的总体口径逐字：「By exposing a Home Assistant API to an LLM, the LLM can fetch data or control Home Assistant to better assist the user. Home Assistant comes with a built-in LLM API, but custom integrations can register their own to provide additional functionality.」内建 API 的边界逐字：「Home Assistant has a built-in API which exposes the Assist API to LLMs. This API allows LLMs to interact with Home Assistant via [intents], and can be extended by registering intents.」「The Assist API is equivalent to the capabilities and exposed entities that are also accessible to the built-in conversation agent. **No administrative tasks can be performed.**」本地路径 `sources\dev-llm\` | 2026-09-18

**DEV-02** | 同上 · `## Contributing tools` | 同上 | 官方文档 | 同上 | 第 14–15 行 | 工具暴露机制逐字：`llm` 集成发现 `<integration>/llm.py` 平台，暴露 `async_get_tools` 钩子；「The platform is imported lazily and queried only when an LLM request needs its tools.」「`async_get_tools` is a callback that is evaluated for each request with the request's `LLMContext` and the `api_id` of the API being assembled.」返回 `llm.LLMTools`，可按请求返回不同工具集。签名逐字：`def async_get_tools(hass: HomeAssistant, llm_context: LLMContext, api_id: str) -> llm.LLMTools | None` | 2026-09-18

**DEV-03** | 同上 · `### Tools` / `#### async_call` | 同上 | 官方文档 | 同上 | 第 489–630 行（Tool / ToolInput / LLMContext 属性表） | 抽象对象逐字：`API`（`hass` / `id` / `name`，仅关键字参数）、`APIInstance`（`api` / `api_prompt` / `llm_context` / `tools` / `custom_serializer`）、`Tool.async_call(hass, tool_input: ToolInput, llm_context: LLMContext)`。上下文模型逐字：`LLMContext` 字段为 `platform`（「The DOMAIN of the conversation agent handling the LLM request」）、`context`（HA core `Context`）、`language`、`assistant`（「The assistant name used to control exposed entities. Currently, only `conversation` is supported.」）、`device_id`。错误约定逐字：「Errors must be raised as `HomeAssistantError` exceptions (or its subclasses). The response data should not contain error codes used for error handling.」`ToolInput` 含 `external` 字段：「Whether the tool call is executed outside of Home Assistant (for example by the model provider). External tool calls are not dispatched to the API's tools.」 | 2026-09-18

**DEV-04** | 同上 · `## Exposing an API over MCP` | 同上 | 官方文档 | 同上 | 第 794–810 行 | 这是「第三方 agent 与内建路线差距」的关键接口面，逐字：「Once the user sets up the [MCP Server integration], **every registered LLM API is automatically served over MCP.**」端点形态：`/api/mcp/<API ID>`（内置 Assist 为 `/api/mcp/assist`）；「These per-API endpoints require an admin access token, **except for the Assist API**.」另有枚举接口 `llm/api/list`（WebSocket）。本地路径 `sources\dev-llm\` | 2026-09-18

---

## 待确认项 3 | 纯确定性自动化的惯用法

**AUTO-01** | Automating Home Assistant | https://www.home-assistant.io/docs/automation/ | 官方文档 | 无显式更新日期 | 全文（仅 1636 字） | 该页是**入口路由页**，不含 trigger/condition/action 定义，逐字：「Automations are how you make your home work for you.」「You build automations in Home Assistant with the visual automation editor, so no coding is required.」「If you are just starting out, we recommend that you start with blueprint automations.」实际结构定义在 `/docs/automation/basics/`（见 AUTO-02）。本地路径 `sources\automation\` | 2026-09-18

**AUTO-02** | Automation basics | https://www.home-assistant.io/docs/automation/basics/ | 官方文档 | 无显式更新日期 | 第 7 行、`### Trigger part` / `### Condition part` / `### Action part` | 确定性自动化的三段结构逐字：「All automations are made of at least a [trigger] and an [action]. Optionally combined with a [condition].」示例逐字：「(trigger part) When Paulus enters home / (condition part) and it is after sunset / (action part) turn on the lights in the living room」。语义逐字：「### Trigger part … When the trigger part is verified, the automation starts.」「### Condition part … If the condition is verified, the action part takes place.」「### Action part … The action part will be performed only if the trigger and condition parts are met.」本地路径 `sources\automation_basics\` | 2026-09-18

**AUTO-03** | Service calls / actions | https://www.home-assistant.io/docs/scripts/service-calls/ | 官方文档 | 无显式更新日期 | `### Use templates to handle response data`（第 112–145 行） | 服务返回数据的官方术语与用法逐字：「Some actions may respond with data that can be used in automation. This data is called _action response data_.」「The action can specify a `response_variable`. This is the variable that contains the response data. You can define any name for your `response_variable`.」官方示例逐字（`action: calendar.get_events` / `target.entity_id: calendar.school` / `data.duration.hours: 24` / `response_variable: agenda`），随后用 `notify.gmail_com` + `data.target` / `data.title` / `data.message` 消费 `agenda['calendar.school'].events`。注意逐字警示：「Which data fields can be used in an action depends on the type of notification that is used.」本地路径 `sources\service-calls\` | 2026-09-18

**AUTO-04** | Persistent Notification | https://www.home-assistant.io/integrations/persistent_notification/ | 官方文档 | 无显式更新日期 | intro、`## Automation`、`## List of actions`、`## Use as a notifier` | 三个 action 逐字：`persistent_notification.create`（「Creates a persistent notification in the Home Assistant frontend.」）、`persistent_notification.dismiss`、`persistent_notification.dismiss_all`。触发方式逐字：「Triggers can be limited to a specific notification by providing an ID for `notification_id`, or when this value is omitted the automation will trigger for any notification ID. If no `update_type` is provided, the automation will trigger for the following update types: `added`, `removed`, `updated`, or `current`.」notify 互通逐字：「It is available as `notify.persistent_notification`.」「You can place the following attribute inside `data` … `notification_id`: When a notification ID is given, it overwrites the notification if one with that ID already exists.」本地路径 `sources\persistent_notification\` | 2026-09-18

**AUTO-05** | Notify integration | https://www.home-assistant.io/integrations/notify/ | 官方文档 | 无显式更新日期 | 全文（8160 字，本地已存） | 作为「同一件事用自动化怎么做」的 notify 侧底稿已落盘；本次未逐段引用（超出本轴最小必要范围），需要时可定向读取 `sources\notify\01_www_home-assistant_io.md`。 | 2026-09-18

---

## 待确认项 4 | 一级项目案例（一手 README / 源码）

**GH-01** | homeassistant-ai/ha-mcp（`README.md`，42671 B） | https://github.com/homeassistant-ai/ha-mcp | 一手项目 README | 无单条发布日期；GitHub API 快照 2026-09-18：stars `4762`、`pushed_at` `2026-09-17T01:34:01Z`、license `MIT` | `## ✨ Features` 表（第 205–213 行）、`<details> Complete Tool List`（第 224 行起）、`### Read-only HTTP connections`（第 379–399 行）、`## 🆚 ha-mcp vs. HA's built-in MCP Server`（第 262–282 行） | **工具分组**（6 类）逐字：`🔍 Search`（Fuzzy entity search, deep config search, system overview）/ `🏠 Control`（Any service, bulk device control, real-time states）/ `🔧 Manage`（Automations, scripts, helpers, dashboards, areas, zones, groups, calendars, blueprints）/ `📊 Monitor`（History, statistics, camera snapshots, automation traces, ZHA devices）/ `💾 System`（Backup/restore, updates, apps, device registry）/ `🔒 Safety`（Read Only Mode toggle, per-tool enable/disable, tool security policies (user approval), automatic edit backups）。**read-only 设计**逐字：「Append `/readonly` to the server's HTTP MCP endpoint to restrict that connection to the existing Read Only Mode while other clients keep normal access」「Read-only connections hide write tools and block write calls, including calls through cached tools or search proxies.」「This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint.」**工具数三处口径不一致**（同一 README 内）：badge `tools-87-blue` 但 alt 文本为 `95+ Tools`；章节标题 `Complete Tool List (87 tools)`；正文 `the full tool catalog (~84 tools)`。**作用域对比**逐字：Entity scope — 内置服务器 `Only entities exposed to Assist` vs ha-mcp `Everything in Home Assistant`。 | 2026-09-18

**GH-02** | goruck/home-generative-agent（`README.md` 22531 B + `docs/configuration.md` + `CHANGELOG.md`） | https://github.com/goruck/home-generative-agent | 一手项目 README / 一手项目变更日志 | README 无日期；CHANGELOG 含 `[3.27.0] - 2026-08-09`、`[3.26.1] - 2026-08-09`、`[3.26.0] - 2026-08-05`、`[3.25.1] - 2026-08-03` | README 第 13/17/21/28 行；`docs/configuration.md` 第 408 行；CHANGELOG `[3.26.0] - 2026-08-05` > `### Security` 与 `### Known limitations` | **「挂载真实沙箱」这一说法在 README、CHANGELOG、docs/architecture.md、docs/configuration.md、CONTRIBUTING.md、AGENTS.md、.github/workflows/validate.yml 中均未出现——回源失败**（唯一 `sandbox` 命中是 CHANGELOG 第 531 行谈 `python_script`：「`python_script` (whose sandbox permits `hass.services.call`)」）。**实际验证机制是静态筛查，逐字**：`docs/configuration.md`「**Automation screening.** Automations are screened after Home Assistant validates them, so blueprint inputs are resolved and every nested branch (`choose`, `if`/`then`/`else`, `repeat`, `parallel`, `sequence`) is inspected. Nothing is written to `automations.yaml` and no reload happens until the PIN is confirmed.」CHANGELOG 3.26.0 逐字：「Screening is an allowlist over Home Assistant's own action taxonomy, not a list of blocked service names.」「Every step is now classified with `cv.determine_script_action` and waved through only when it is provably inert or resolves to something no rule matches.」「Screening fails closed on anything it cannot resolve」。**官方自陈的验证缺口逐字**（Known limitations）：「Raw protocol writes are not screened.」（点名 `mqtt.publish`、`zwave_js.set_value`、`zha.issue_zigbee_cluster_command`）；「Targets that resolve at run time cannot be inspected.」；蓝图型自动化「the PIN attests to what the blueprint did **at approval time**」。**踩坑自述逐字**：「the first version of this gate — which only understood `action:`/`service:` steps — was defeated by four verified bypasses during pre-landing review, each confirmed against a real Home Assistant install by two independent reviewers.」（这句是「真实」二字的唯一可能来源：指的是**发布前人工复核**，不是运行时沙箱）。此外 README 第 21 行给出与 LLM 路线的定位差异逐字：「its Sentinel anomaly engine keeps safety decisions deterministic, with the LLM advising but never actuating.」 | 2026-09-18

**GH-03** | Oasis-Enterprise/mylo（`README.md` 23747 B） | https://github.com/Oasis-Enterprise/mylo | 一手项目 README | 无发布日期；README 自述 `Status: v1.4.0`、245 commits | 第 207 行（Sensor anomalies）、第 228 行（`anomaly` 抑制类型）、`## Safety model`（第 338–360 行）、`session_budget_usd` 表（第 330–333 行） | **z-score 实现细节逐字（比上一阶段报告更完整）**：「**Sensor anomalies** — a z-score check against a 7-day baseline (mean + standard deviation), recomputed nightly — but a finding fires only on a strong deviation (3.5σ) sustained across two consecutive checks, so one-hour blips don't alert.」**确定性基线 + LLM 分工的其余口径逐字**：`Duration anomalies`（「far longer than *its own* history」，锁与门 margin 更紧）、`On while away`（「only when that's unusual for that entity」）、`Behavioral patterns`（nightly，从 14 天 transitions 学）、`Availability sweep`（hourly，stale automation >48h）；「A device earns the right to be alerted on — it stays quiet until Mylo has watched it long enough (~2 weeks)」。**权限三层逐字**：Tier 1 Read（无需批准）/ Tier 2 Modify（`Yes (dry-run first)`）/ Tier 3 Action（`Yes (explicit confirmation)`）；**硬阻断**逐字：`homeassistant/restart`、`homeassistant/stop`、`hassio/host_reboot`、`hassio/host_shutdown`、`hassio/supervisor_reload`；受限服务为解锁、撤防警报、开门/窗帘。**预算做成显式配置键**：`session_budget_usd` 默认 `0.50`、`monthly_budget_usd` 默认 `15.00`。**回滚**逐字：「Tier-2 file writes use atomic write → reload → verify → rollback-on-failure.」 | 2026-09-18

---

## 待确认项 5 | 社区长期实践（成本 / 误报 / 权限）

> 标注 **【直读核验】** 的条目由子代理本人回源确认；标注 **【子代理采集】** 的条目由并行子代理抓取并返回逐字引用与 URL，**主流程未全部二次回源，引用时需自行复核**。

**C-01** | MCP Server / GetLiveContext: area-scoped queries silently exclude entities with no area assigned (#177476) | https://github.com/home-assistant/core/issues/177476 | 一手 issue（用户 incident 报告） | 开于 2026-07-28；**closed as `completed`，2026-09-08**；label `integration: mcp_server` | 正文 | **【直读核验】** 误报的最硬证据：原文逐字「When an MCP client (e.g. Claude via the Model Context Protocol Server integration) calls GetLiveContext with an area filter, entities that are exposed to Assist but have no area assigned are silently absent from the result. The response gives no indication that exposed entities were skipped — it looks like a complete answer for that area.」「This is worse than an error, because the …」结论：症状不是报错而是 LLM 得出自信的错误结论。**注：上一阶段子代理称「已 closed」属实，但漏记其为 `completed`（即已被修复）。** | 2026-09-18

**C-02** | Ollama Integration is controlling entities that aren't exposed to Assist (#133460) | https://github.com/home-assistant/core/issues/133460 | 一手 issue | 开于 2024-12-18；**closed as `not_planned`，2025-04-12**；labels `stale`、`integration: ollama` | 正文 | **【直读核验】** 权限边界被穿透的直接证据，原文逐字：「I recently started toying around with using a local Ollama 3.2 LLM as my conversation agent, but I've noticed a very odd behavior. When I interact with the agent, such as asking it if a light is on in the house, it will [toggle a specific Input Boolean] helper called "Good night toggle". The wild thing is, that entity is not even [exposed to Assist]…」即「只读提问 → 未暴露实体被 toggle」，且 issue 以 not_planned 关闭、无维护者解释。 | 2026-09-18

**C-03** | New assist with LLM combination, lot of tokens? | https://community.home-assistant.io/t/new-assist-with-llm-combination-lot-of-tokens/736566 | 社区帖（HA 官方论坛） | 2024-06-06 ~ 2024-06-13 | 帖内实测回帖 | **【子代理采集】** 成本数据（含暴露实体数）：skycryer「I had now 36 api request with got-4o and a usage of 339.000 context tokens and 1800 generated tokens.」「I have around 230 entities open to assist for usage」；Ollijung「13 API requests / 130,000 tokens / totalling 0.66$」、换 gpt-3.5-turbo 后「Even with 1/10 of the price it's still 0.6 Cent per command.」「yeah it still uses 10000 tokens for turning on a light.」；kolossboss「Still Using 5000 Tokens for a simple request.」「I reduced my exposed entities from 340 to 100.」；skycryer 预警「my monthly limit of 20$ will be gone after a short time」。缓解手段原文涉及模板 `{% for entity in exposed_entities -%}`，字段 `entity_id,name,state,aliases`。 | 2026-09-18

**C-04** | Ha-mcp macht den Kontext voll | https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707 | 社区帖（simon42 社区，德语） | 2026-07-06（帖内时间戳与截图 `Bildschirmfoto 2026-07-06 um 09.34.51`） | 帖内实测 | **【子代理采集】** MCP 工具 schema 的 token 实测：「Die MCP Tools verbrauchen schon über 60k Tokens.」「Dein Home Assistant MCP-Server ballert Claude mit stolzen 77 Tools zu」「Summiert über 77 Tools kommen die 60,3k zusammen」「Die teuersten Einzeltools lagen bei 1,8k–3,4k Tokens」，最贵工具点名 `ha_config_set_helper`、`ha_get_integration`、`ha_config_set_dashboard`、`ha_config_set_automation`；对比基线「bei anderen MCP-Servern mit 5–15 Tools sieht man das selten in dieser Größenordnung」；配置面为 `claude_desktop_config.json`。 | 2026-09-18

**C-05** | My Journey to a reliable and enjoyable locally hosted voice assistant | https://community.home-assistant.io/t/my-journey-to-a-reliable-and-enjoyable-locally-hosted-voice-assistant/944860 | 社区帖（HA 官方论坛，长周期复盘） | 2025-10-27 ~ 2026-01-05 | 楼主自述与回帖 | **【子代理采集】** 最接近「长期实践复盘」的一条。延迟数据：RTX 3090 24GB / RX 7900XTX 24GB「1 - 2 seconds」、RTX 5060Ti 16GB「1.5 - 3 seconds」、RTX 3050 8GB「3 seconds」。实体数：作者「Right now I have 32.」；回帖「exposing just 53 entities makes it behave very unreliable」。误报原话：「sometimes turns on a light in another room, or also a fan or socket」「anytime there was a false activation the LLM would always end the response with a question, which created a loop」；天气 intent 无对应实体时「the LLM was apparently just making up values based on the sensors it had access to」。结论口径：「I definitely would not recommend this for the average Home Assistant user」。 | 2026-09-18

**C-06** | Brand New Claude.ai & ChatGPT integration (ha-mcp) | https://community.home-assistant.io/t/brand-new-claude-ai-chatgpt-integration-ha-mcp/937847 | 社区帖（HA 官方论坛） | 2025-10-07 ~ 2026-01-06 | 用户事故报告与作者回复 | **【子代理采集】** 权限层被 agent 写坏的实测事故：「`ha_assign_label` replaces all labels rather than adding to existing ones」、称「corrupted my entity registry」、标签 UI 消失；作者回滚建议「Claude or Gemini read automations before they modify… Just ask to rollback what they did.」；示例配置 `claude_desktop_config.json`，`mcpServers` 键 `home-assistant`、`command` 为 `mcp-proxy`、`args` 为 `["http://192.168.52.53:9583/private_redacted"]`。**无 token / 成本数据。** | 2026-09-18

**C-07** | New dedicated Home Assistant Setup - for AI? | https://community.home-assistant.io/t/new-dedicated-home-assistant-setup-for-ai/927713 | 社区帖（HA 官方论坛） | 2025-09-05 | 用户自述 | **【子代理采集】** 硬件约束口径：「I can burn approx 20/usd/mo on openai」；本地路线「That takes a modern GPU with 16GB VRam at a MINIMUM」「At 16GB you can run an 8-16 K context window」「8k is very small if you have any number of controlled entities」；eGPU 投入「approx $1200 usd for the setup」。 | 2026-09-18

**C-08** | Inconsistent brightness interactions using llm.py exposed_entities and built-in intents (#134848) | https://github.com/home-assistant/core/issues/134848 | 一手 issue | 开于 2025-01-06；closed as `not_planned`（`stale`） | 正文 | **【子代理采集】** 误报归因到单位不一致：`homeassistant/helpers/llm.py#L471` 给 LLM 的是「the 0-255 "brightness value"」，而 `HassTurnOn` intent 期望「a 0-100 range for the brightness parameter」，「Then LLMs will often provide an inconsistent change (e.g. setting the brightness to 100%, instead of ≈38%)」；环境 `core-2024.10.4`。 | 2026-09-18

**C-09** | LLM command goes strange | https://community.home-assistant.io/t/llm-command-goes-strange/930648 | 社区帖（HA 官方论坛，含原始日志） | 2025-09-14 ~ 2025-09-15 | 楼主日志 | **【子代理采集】** 误报的具体形态是「模型输出工具调用 JSON 但未执行」：Ollama `llama3.1` 生成 `{"name": "HassSet", "parameters": {"area": "Landing", "domain": "input_number", …, "value": "25"}}`；日志侧 `registry.ollama.ai/library/llama2:13b does not support tools`、`Unexpected error during intent recognition`，来源 `components/assist_pipeline/pipeline.py:1267`。 | 2026-09-18

**C-10** | [Custom Component] extended_openai_conversation | https://community.home-assistant.io/t/custom-component-extended-openai-conversation-lets-control-entities-via-chatgpt/636500 | 社区帖（HA 官方论坛） | 2023-11-05 ~ 2023-12-12（首屏） | 用户回帖 | **【子代理采集】** 最早一批「只读询问导致误动作」报告：「Occasionally if asking for which lights are on, it will make a service call to do so, but also turn on certain lights.」「I haven't been able to narrow down exactly what's happening here.」；复现者归因模型 `gpt-3.5-turbo-1106`。**该帖另有成本子线（称 27ct/query、125 exposed entities）子代理未取得直读证据，已列为存疑。** | 2026-09-18

**C-11** | ha-mcp-assist（`Moballo-LLC/ha-mcp-assist`） | https://github.com/Moballo-LLC/ha-mcp-assist | 一手项目 README | 无日期；664 commits | README | **【子代理采集】** 权限与成本同一类解法（动态发现替代全量注入）：「solves entity context limitations through dynamic discovery instead of full entity dumps」；全量推送的后果「gets expensive, slow, and unreliable as your home grows」；权限口径「MCP Assist follows Home Assistant's conversation exposure model」「the assistant only discovers and controls entities you expose」，设置路径 **Settings → Voice Assistants**；要求 Home Assistant 2024.1+ / Python 3.11+。**无 token 数字。** | 2026-09-18

**C-12** | extended_deepseek_conversation（`XtracT/extended_deepseek_conversation`） | https://github.com/XtracT/extended_deepseek_conversation | 一手项目 README（FAQ） | 无日期 | README FAQ | **【子代理采集】** 显式承认「暴露列表」是软约束：「Can gpt query data that is not exposed?」「Yes, it is hard to validate whether a query is only using exposed entities.」折中方案为 `is_exposed_entity_in_query` 配 `raise`，模板 `{%- if is_exposed_entity_in_query(query) -%}` … `{{ raise("entity_id should be exposed.") }}`，自评「minimum validation」「not secured enough, but flexible」。配置键：`Attach Username`、`Maximum Function Calls Per Conversation`、`Base Url`。 | 2026-09-18

---

## 矛盾与存疑

1. **「It can only control or provide information about entities that are exposed to it.」的页面归属被上一阶段报告搞混。** 该句只出现在四个 **LLM 集成页**（OpenAI / Anthropic / Google / Ollama），且是 `Control Home Assistant` **配置项的描述**，前面还有一句「If the model is allowed to interact with Home Assistant.」；`/integrations/conversation/` 与 `/voice_control/` **都没有**这句。写正文时若按上一阶段报告的页面列表引用，会指向错误页面。
2. **HA 官方文档内部就 sentence triggers 自相矛盾。** 四个 LLM 集成页均写「This integration does not integrate with [sentence triggers].」；而 `/integrations/conversation/` 写「External conversation agents … only use sentence triggers when **Prefer handling commands locally** is enabled.」后者给出了条件性的例外，前者是绝对否定。**在四个 LLM 集成页与 voice_control 页全文检索 `Prefer handling commands locally` 均无命中**，该开关在 LLM 集成页未被记录——两者无法在官方文档内对齐，存疑。
3. **`goruck/home-generative-agent` 的「挂载真实沙箱」未能回源，疑为上一阶段报告失实。** README 无此说法；全仓 `sandbox` 唯一命中是 CHANGELOG 谈 `python_script` 沙箱。该项目的真实机制是 `cv.determine_script_action` 静态筛选 + PIN 门禁，官方自陈有三类无法覆盖的漏洞（raw protocol writes / run-time 解析目标 / 蓝图事后被改）。「真实」二字可能源自其「confirmed against a real Home Assistant install by two independent reviewers」——那指**发布前人工复核**，不是运行时沙箱。
4. **ha-mcp 的工具有效数量同一 README 内三处不一致**：badge `87`、alt 文本 `95+`、章节标题 `87 tools`、正文 `~84 tools`。上一阶段报告的「87 tools」确为其中一处口径，但不应作为唯一事实。
5. **「暴露列表 = 安全边界」的说法在来源间互相冲突。** 官方口径（HA-06）把它当设计意图；C-02 有未暴露实体被控制的官方 issue（closed as not_planned，无解释）；C-12 作者直言「it is hard to validate whether a query is only using exposed entities」；而 GH-01 / C-11 都把「仅暴露实体」当安全保证来陈述。**且 GH-01 恰恰以「Everything in Home Assistant」为卖点**——两条路线的实体作用域差异是官方明文的。
6. **社区成本数据不同源、不可对账。** C-03 同一帖内 242 exposed entities 报「0.6 Cent per command」，而同帖 340→100 entities 的用户仍报「Still Using 5000 Tokens for a simple request.」——实体数不是成本的单调解释变量。
7. **本地推理 ≠ 免费。** C-07 给出门槛（16GB VRAM 起、仅 8–16K context）；C-03/C-05 的延迟与误报数据均为本地模型。GH-03 把 ollama 计为 `$0` 因而自动禁用预算告警，是可复核的设计取舍，但不是 TCO 口径。
8. **C-01 已修复。** 该 issue 2026-09-08 closed as `completed`；引用时须注明这是已修补的历史缺陷，不是当下行为。

## 未解决项

1. **`/integrations/conversation/` 的 `Prefer handling commands locally` 究竟在哪个集成页有文档**——四个 LLM 集成页全文均无此串，需查 release notes 或 UI 实体属性。
2. **HA 官方文档页均无显式「最后更新」时间戳**（crawl 只给出 `scraped_at`）。本报告所有 HA 文档条目的「发布或更新日期」只能记为空缺 + 抓取时间；若要判断时效需回溯 `home-assistant/home-assistant.io` 仓库的 git 历史。
3. **`ha-mcp` 的 `ENABLE_TOOL_SEARCH` 量化节省无官方数字。** README 只定性写「the full catalog has no idle cost there」，反而与 C-04 实测的 60.3k tokens 常驻形成张力，README 未给任何节省百分比。
4. **`goruck/home-generative-agent` 的自动化验证到底有无运行时校验**——本次只确认了「静态筛查 + HA 自身 validate」；是否存在测试态实例/回放验证未查到（`.github/workflows/validate.yml` 仅 `Hassfest` 与 `HACS` 两项校验）。
5. **误报率无任何来源给出分母。** 所有误报记录（C-01/02/05/08/09/10）都是单次事件叙述，无法计算比率。
6. **Reddit 未被覆盖。** 子代理四轮检索未返回任何 reddit.com 结果，「Reddit 带评论区数据」这一要求本轮未满足。
7. **无任何来源同时给出「月度账单 + 暴露实体数 + 模型名」三者齐全的长期（>6 个月）记录**；C-03 有 token 数无月账单，C-07 有 $20/mo 无实体数。
8. **未找到 HA 社区侧 prompt injection / 恶意实体名触发 agent 的实测帖**（仅媒体定性警告，属二手，未采信）。
9. **C-04（德语帖）与 C-03、C-05、C-06、C-07 为子代理采集，主流程未逐条回源**；这些条目在写入正文前需按同样标准做一次直读核验，尤其是被当成「成本量级」或「实测数字」引用的 C-04 与 C-03。

---

## 对上一阶段记录的更正（写正文前必须替换）

| 更正项 | 上一阶段说法 | 本轮回源结果 | 处置 |
|---|---|---|---|
| 边界句页面归属 | 见 `01_explore_result.md` F5 / probe 记录所引页面列表 | 只在四个 LLM 集成页的 `Control Home Assistant` 配置项描述中，且前面还有一句「If the model is allowed to interact with Home Assistant.」 | 引用时改指 LLM 集成页 + 补前一句 |
| home-generative-agent「挂载真实沙箱」 | 作为「可靠性靠沙箱验证」的证据 | **回源失败**，真实机制是静态筛查 + PIN，官方自陈三类漏洞 | **删除该说法**，不得写进正文 |
| C-01 issue 状态 | 「已 closed」 | `completed`，2026-09-08 已修复 | 注明为已修补的历史缺陷 |
| ollama 边界句 | 截断引用「Controlling Home Assistant is an experimental feature」 | 原文为整句「Controlling Home Assistant is an experimental feature that provides the AI access to the Assist API of Home Assistant.」 | 用整句 |

## 新增来源 ID（续编）

| ID | 来源 |
|---|---|
| HAS-17 | https://www.home-assistant.io/integrations/conversation/ |
| HAS-18 | https://www.home-assistant.io/integrations/openai_conversation/ |
| HAS-19 | https://www.home-assistant.io/integrations/anthropic/ |
| HAS-20 | https://www.home-assistant.io/integrations/google_generative_ai_conversation/ |
| HAS-21 | https://www.home-assistant.io/integrations/ollama/ |
| HAS-22 | https://www.home-assistant.io/docs/automation/ |
| HAS-23 | https://www.home-assistant.io/docs/automation/basics/ |
| HAS-24 | https://www.home-assistant.io/integrations/notify/ |
| HAS-25 | https://www.home-assistant.io/integrations/mcp_server/（`## Exposing an API over MCP` 端点面，与 HAS-01 同页不同节） |
| COM-11 | https://github.com/Moballo-LLC/ha-mcp-assist |
| COM-12 | https://github.com/XtracT/extended_deepseek_conversation |
| COM-13 | https://github.com/home-assistant/core/issues/177476（area 过滤静默漏实体；已修复） |
| COM-14 | https://github.com/home-assistant/core/issues/133460（未暴露实体被控制；not_planned） |
| COM-15 | https://github.com/home-assistant/core/issues/134848（brightness 单位不一致） |
| COM-16 | https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707（MCP 工具 schema 60.3k tokens，德语） |
| COM-17 | https://community.home-assistant.io/t/944860（本地语音助手长期复盘） |
| COM-18 | https://community.home-assistant.io/t/937847（ha-mcp 写坏 label 事故） |
| COM-19 | https://community.home-assistant.io/t/927713（本地推理硬件门槛） |
| COM-20 | https://community.home-assistant.io/t/930648（工具调用 JSON 未执行） |
| COM-21 | https://community.home-assistant.io/t/636500（extended_openai_conversation 误动作） |
| COM-22 | https://community.home-assistant.io/t/736566（Assist + LLM token 消耗实测） |
