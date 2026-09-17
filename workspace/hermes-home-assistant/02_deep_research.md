# 阶段 2 深度素材：用 Hermes Agent 控制 Home Assistant

> 生成时间：2026-09-18 ｜ 运行：`hermes-home-assistant` ｜ 方向：A 能力地图 + B 路线选型
> 主题：用 Hermes Agent 控制 Home Assistant：能力地图与实现路线
> **本文件是阶段 2 交付物，P3/P4 的唯一素材入口。**
> 原始证据按批次存于 `research/probe-01..08-*.md`；页面快照存于 `sources/`。本文件只做**汇总、定论与指向**，不复制原文长段落。

---

## 一、范围与阶段说明

### 1.1 本篇要回答什么

用户已完成 Hermes ↔ HA 接入（LLT + `HASS_TOKEN`/`HASS_URL`，四个 `ha_*` 工具可用），问题是：

1. 用 Hermes 控制 HA，**能实现什么**（能力地图）
2. **走哪条路**实现（路线选型）

### 1.2 P2 的收口目标

P1 交付 `01_explore_result.md`，留下 **8 个缺口**。P2 派 3 组精读代理分别补：

| 组 | 精读目标 | 产物 | 结案 |
|---|---|---|---|
| A | MCP 接线层（缺口 1/2/3/8） | `research/probe-07-mcp-wiring.md` | 4/4 |
| B | 文档化程度与版本门槛（缺口 4/5/6/7） | `research/probe-08-docs-version-gates.md` | 4/4 |
| C | 三方对照轴（P1 增补 ① 的素材） | `research/probe-06-threeway-axis.md` | — |

**8 个缺口全部有结论**，其中 2 个是「否定结论」（官方确实没写），1 个由**源码定论**（不再依赖实机），1 个是「文档与代码对不上，且代码里查无此项」。

### 1.3 不做什么

- 不重复收集 probe-01..05 已覆盖的事实
- 不替官方补它没写的例子（缺口 5 就是这种情况，见 §6.3）
- 不把子代理的转述当原文（引用纪律见 §8）

---

## 二、来源总表（P3/P4 的 canonical 注册表）

### 2.1 编号体系说明

P1 用 `HAS-/HMS-/COM-`，P2 三组精读各自带回了**局部编号**（`H-*` / `HA-*` / `HMS-M*` / `HAS-M*` / `COM-M*`）。**以本节为唯一 canonical 注册表**；下表给出局部编号到 canonical 的映射。P3/P4 引用只用本表 ID。

新增 `SRC-` 前缀：P1 的 `HMS-*` 混装了「官方文档」与「源码文件」，P2 又大量补了 HA core 与 Hermes 仓库的一手源码，故把**源码类**独立成 `SRC-`。

### 2.2 HAS — Home Assistant 官方（27 条 + 1 组排除项）

| ID | 来源 | 档位 | P2 核验 |
|---|---|---|---|
| HAS-01 | https://www.home-assistant.io/integrations/mcp_server/ | 官方文档 | **已回源**（含 `## Configuration options`、6 个 client 示例、IndieAuth 段） |
| HAS-02 | https://www.home-assistant.io/integrations/mcp/ （HA 作 MCP client，与 HAS-01 是两页） | 官方文档 | 未复核 |
| HAS-03 | https://developers.home-assistant.io/docs/api/rest/ | 官方文档 | 未复核 |
| HAS-04 | https://developers.home-assistant.io/docs/api/websocket/ | 官方文档 | 未复核 |
| HAS-05 | https://developers.home-assistant.io/docs/auth_api/ | 官方文档 | 未复核 |
| HAS-06 | https://developers.home-assistant.io/docs/auth_permissions/ | 官方文档 | 未复核 |
| HAS-07 | https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/ | 官方博客 | **已回源**（两句结论确证；**通篇无版本号**） |
| HAS-08 | https://www.home-assistant.io/integrations/ai_task/ | 官方文档 | 未复核 |
| HAS-09 | https://www.home-assistant.io/voice_control/voice_remote_expose_devices/ | 官方文档 | **已回源**（全文仅 1187 字） |
| HAS-10 | https://www.home-assistant.io/docs/scripts/service-calls/ | 官方文档 | **已回源**（`response_variable` / action response data） |
| HAS-11 | https://www.home-assistant.io/docs/automation/trigger/ | 官方文档 | 未复核 |
| HAS-12 | https://www.home-assistant.io/integrations/alert/ | 官方文档 | 未复核 |
| HAS-13 | https://www.home-assistant.io/integrations/recorder/ | 官方文档 | 未复核 |
| HAS-14 | https://www.home-assistant.io/integrations/telegram_bot/ | 官方文档 | 未复核 |
| HAS-15 | https://www.home-assistant.io/integrations/persistent_notification/ | 官方文档 | **已回源** |
| HAS-16 | https://developers.home-assistant.io/docs/core/llm/ | 官方文档（开发者） | **已回源**（含 `API/APIInstance/Tool/LLMContext` 属性表、`## Exposing an API over MCP`） |
| HAS-17 | https://www.home-assistant.io/integrations/conversation/ | 官方文档 | **已回源** |
| HAS-18 | https://www.home-assistant.io/integrations/openai_conversation/ | 官方文档 | **已回源** |
| HAS-19 | https://www.home-assistant.io/integrations/anthropic/ | 官方文档 | **已回源** |
| HAS-20 | https://www.home-assistant.io/integrations/google_generative_ai_conversation/ | 官方文档 | **已回源** |
| HAS-21 | https://www.home-assistant.io/integrations/ollama/ | 官方文档 | **已回源**（含 25 实体建议、Tools 要求） |
| HAS-22 | https://www.home-assistant.io/docs/automation/ | 官方文档 | **已回源**（入口路由页，无结构定义） |
| HAS-23 | https://www.home-assistant.io/docs/automation/basics/ | 官方文档 | **已回源**（trigger/condition/action 三段） |
| HAS-24 | https://www.home-assistant.io/integrations/notify/ | 官方文档 | **已回源**（`notify.notify` 语义警告） |
| HAS-25 | HAS-01 同页 `## Exposing an API over MCP` 锚点（`/api/mcp/<API ID>`、admin 要求） | 官方文档 | **已回源** |
| HAS-26 | https://www.home-assistant.io/blog/2025/07/02/release-20257/ | 官方 release notes | **已回源**（`assist_satellite.ask_question`） |
| HAS-27 | https://www.home-assistant.io/blog/2025/08/06/release-20258/ | 官方 release notes | **已回源**（Suggest 按钮首发） |
| HAS-28 | release notes 2025.09 / 2025.10 / 2025.11（三份，**仅用于排除**） | 官方 release notes | **已检索，无命中** |

### 2.3 HMS — Hermes 官方文档（12 条）

| ID | 来源 | P2 核验 |
|---|---|---|
| HMS-01 | `tools/homeassistant_tool.py`（P1 归入 HMS，实为源码 → 见 SRC-01） | — |
| HMS-02 | `plugins/platforms/homeassistant/adapter.py`（→ SRC-02） | — |
| HMS-03 | `website/docs/reference/toolsets-reference.md` | 未复核 |
| HMS-04 | `website/docs/reference/mcp-config-reference.md` | **已回源**（`mcp__<server>__<tool>` **正确**） |
| HMS-05 | `website/docs/user-guide/features/skills.md` | **已回源**（L0/L1/L2、运行时目录树；字段表与 HMS-12 冲突） |
| HMS-06 | `website/docs/user-guide/features/plugins.md` + `developer-guide/plugins/index.md` | 未复核 |
| HMS-07 | `website/docs/reference/cli-commands.md` | **已回源**（`hermes mcp` 全部子命令、`--version`） |
| HMS-08 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant | **已回源**（**只写 `persistent_notification.create` 一条路**） |
| HMS-09 | `website/docs/user-guide/features/cron.md`（67495 字节） | **已回源**（`homeassistant` 全文仅 1 次命中，Example 列空） |
| HMS-10 | `website/docs/guides/use-mcp-with-hermes.md` | **已回源**（前缀写法**过期**） |
| HMS-11 | `website/docs/user-guide/features/mcp.md` + 发布站同名页 | **已回源**（前缀写法**过期**） |
| HMS-12 | `website/docs/developer-guide/creating-skills.md`（20113 字节） | **已回源**（frontmatter 逐字清单） |

> **路径更正**：`creating-skills.md` 在 `developer-guide/` 下，**不在** `user-guide/features/` 下（P1 记的路径在仓库中不存在，站点上返 404）。

### 2.4 SRC — 一手源码（14 条）

| ID | 文件 | 关键内容 |
|---|---|---|
| SRC-01 | Hermes `tools/homeassistant_tool.py` | 4 个内置工具、正则校验、blocked domains 黑名单、`_check_ha_available()` gating |
| SRC-02 | Hermes `plugins/platforms/homeassistant/adapter.py` | `watch_*` 过滤、per-entity `cooldown_seconds`、事件模板、**出站两条分支**、4096 硬截断 |
| SRC-03 | Hermes `plugins/platforms/homeassistant/plugin.yaml` | description：两条出站路并存，**未给触发条件** |
| SRC-04 | Hermes `tools/mcp_tool_schema.py` | **`MCP_TOOL_NAME_PREFIX = "mcp__"`（前缀定论）**、`sanitize_mcp_name_component`、64 字符截断 |
| SRC-05 | Hermes `agent/anthropic_adapter.py` | `_MCP_TOOL_PREFIX = "mcp__"`、`_normalize_to_mcp_wire()`；**docstring 已过期** |
| SRC-06 | Hermes `tests/agent/test_anthropic_mcp_prefix_strip.py` | 测试 docstring 亦过期；断言无法区分两种命名 |
| SRC-07 | Hermes `hermes_cli/mcp_config.py` | `hermes mcp test` 打印**原生工具名**；`tools.include` 用原生名 |
| SRC-08 | Hermes `cron/scheduler_delivery.py` | `_deliver_result` docstring：**分支条件唯一权威表述** |
| SRC-09 | Hermes `gateway/platform_registry.py` | `standalone_sender_fn` 字段声明 |
| SRC-10 | Hermes `gateway/platforms/base.py` + 各平台 adapter | `splits_long_messages` 基线：HA 未设 → 硬截断；Telegram/Discord/Slack/Signal 均分片 |
| SRC-11 | HA core `components/mcp_server/` @ `master`/`rc`（=2026.9） | **无** `CONF_REQUIRE_ADMIN`；docstring 明说 `/api/mcp` 不要求 admin |
| SRC-12 | HA core `components/mcp_server/` @ `dev`（=2026.10） | `CONF_REQUIRE_ADMIN`、UI 文案 `Require an administrator account`、`_validate_admin`、迁移默认 `False` |
| SRC-13 | HA core `mcp_server` 提交史（44 条，至 2026-09-13） | `#180713`（require admin）、`#180629`（options flow）；**无任何 control/read-only 类选项** |
| SRC-14 | HA core `auth/__init__.py` + `components/auth/__init__.py` | LLT：无 scope claim、`ws_require_user`（非 admin 可创建）、revoke 语义 |

### 2.5 COM — 社区 / 第三方 / issue（23 条）

| ID | 来源 | 档位 | 备注 |
|---|---|---|---|
| COM-01 | https://github.com/homeassistant-ai/ha-mcp （README 42671 B） | 一手项目 README | 4762★、MIT；**工具数同一 README 内三处不一致（87 / 95+ / ~84）** |
| COM-02 | https://github.com/voska/hass-mcp | 一手项目 | 342★，走 HA WebSocket |
| COM-03 | https://github.com/archieboy-holdings/ha-household-briefing | 一手项目 | **无 LLM** 的确定性对照 |
| COM-04 | https://github.com/cnc-lasercraft/haclaude | 一手项目 | 夜间巡检 + 只读工具白名单（德文 README） |
| COM-05 | https://github.com/Oasis-Enterprise/mylo | 一手项目 | z-score 3.5σ × 连续两次；三层权限；`session_budget_usd`；atomic write → reload → verify → rollback |
| COM-06 | https://github.com/goruck/home-generative-agent | 一手项目 | **「真实沙箱」回源失败**（见 §5.3）；真实机制为静态筛查 + PIN |
| COM-07 | https://github.com/tevonsb/homeassistant-mcp | 一手项目 | 576★，最后 push 2026-01（滞后） |
| COM-08 | https://github.com/ganhammar/hass-mcp-server | 一手项目 | 69★，HACS 组件，OAuth 2.0 |
| COM-09 | https://github.com/allenporter/mcp-server-home-assistant | 一手项目 | **已归档，勿选** |
| COM-10 | 社区帖 1003703 / 1003803 / 908474 / 1016481 | 社区帖 | 作者自报，无第三方复现 |
| COM-11 | https://github.com/Moballo-LLC/ha-mcp-assist | 一手项目 README | 动态发现替代全量注入；跟随 HA conversation exposure model |
| COM-12 | https://github.com/XtracT/extended_deepseek_conversation | 一手项目 README | **作者自认「暴露列表」是软约束** |
| COM-13 | https://github.com/home-assistant/core/issues/177476 | 一手 issue | area 过滤**静默**漏掉无 area 的已暴露实体；**closed as `completed`，2026-09-08 已修复** |
| COM-14 | https://github.com/home-assistant/core/issues/133460 | 一手 issue | **未暴露实体被 toggle**；`not_planned` 关闭、无维护者解释 |
| COM-15 | https://github.com/home-assistant/core/issues/134848 | 一手 issue | brightness 0–255 vs 0–100 单位不一致致误动作 |
| COM-16 | https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707 | 社区帖（德语） | 77 工具 schema 常驻 **60.3k tokens**，最贵单工具 1.8k–3.4k |
| COM-17 | https://community.home-assistant.io/t/944860 | 社区帖 | 本地语音长期复盘：延迟、32/53 实体、误报形态 |
| COM-18 | https://community.home-assistant.io/t/937847 | 社区帖 | `ha_assign_label` 覆写致 entity registry 损坏 |
| COM-19 | https://community.home-assistant.io/t/927713 | 社区帖 | 本地推理硬件门槛：16GB VRAM 起、8–16K context |
| COM-20 | https://community.home-assistant.io/t/930648 | 社区帖 | 模型输出工具调用 JSON 但未执行（`llama2:13b does not support tools`） |
| COM-21 | https://community.home-assistant.io/t/636500 | 社区帖 | 最早一批「只读询问导致误动作」报告 |
| COM-22 | https://community.home-assistant.io/t/736566 | 社区帖 | Assist + LLM token 实测（230/340/100 实体对照） |
| COM-23 | https://homeassistant-ai.github.io/ha-mcp/setup/ | 一手项目文档 | **Setup Wizard 含 Hermes Agent**：专属 YAML 模板、`/reload-mcp`、`mcp__home_assistant__<tool>` |

### 2.6 局部编号 → canonical 映射

| 局部编号 | 出处 | canonical |
|---|---|---|
| `H-01` | probe-08 | **HMS-12** |
| `H-02` | probe-08 | HMS-05 |
| `H-03` | probe-08 | HMS-09 |
| `H-04` `H-05` | probe-08 | **SRC-02** / **SRC-03** |
| `H-06` | probe-08 | HMS-08 |
| `H-07` `H-08` | probe-08 | **SRC-08** / **SRC-09** |
| `HA-01` `HA-02` | probe-08 | HAS-15 / HAS-24 |
| `HA-03` | probe-08 | HAS-07 |
| `HA-04` `HA-05` | probe-08 | **HAS-26** / **HAS-27** |
| `HMS-M1` `HMS-M8` | probe-07 | HMS-11 |
| `HMS-M2` `HMS-M3` | probe-07 | HMS-04 / HMS-10 |
| `HMS-M4..M7` `HMS-M9` | probe-07 | **SRC-04..SRC-07** |
| `HMS-M10` | probe-07 | HMS-07 |
| `HAS-M1..M13` | probe-07 | HAS-01（同页不同锚点） |
| `HAS-M14..M18` | probe-07 | **SRC-11 / SRC-12** |
| `HAS-M19` `HAS-M20` | probe-07 | **SRC-13** |
| `COM-M1` | probe-07 | **COM-23** |
| `COM-M2..M8` | probe-07 | COM-01 |
| `COM-M9..M11` | probe-07 | COM-23 |

---

## 三、主张 → 来源映射（按笔记骨架分组）

> 本节每条都带 canonical ID + 锚点。**P4 写作时对任何「官方口径是 / 原文」类断言，必须按 ID 回原文逐字比对，不得只凭本表转述。**

### 3.1 A 能力地图：内置能力的真实天花板

| # | 主张 | 来源 + 锚点 |
|---|---|---|
| A-1 | Hermes 内置 HA 工具**恰好 4 个**：`ha_list_entities` / `ha_get_state` / `ha_list_services` / `ha_call_service` | SRC-01（docstring） |
| A-2 | 工具集由 `bool(get_secret("HASS_TOKEN"))` 开关 | SRC-01 |
| A-3 | 缺三块能力：**历史/统计**、**写配置（自动化）**、**摄像头/结构化 AI 任务** | SRC-01（工具清单）+ probe-03 场景表 |
| A-4 | 全部 14 个场景都落在 4 个内置工具内，凡涉 A-3 三类的场景必须换路线 | probe-03（结构性结论） |
| A-5 | 硬防线：blocked domains = `shell_command` / `command_line` / `python_script` / `pyscript` / `hassio` / `rest_command`；先格式校验后黑名单 | SRC-01 |
| A-6 | `ha_list_entities` 的 `area` 参数匹配 friendly_name / area 属性，**不是** HA area registry | SRC-01 |
| A-7 | 事件驱动：默认**一条都不转发**；`watch_domains` / `watch_entities` / `ignore_entities` / `watch_all` | SRC-02 |
| A-8 | `cooldown_seconds`（默认 30）是**逐实体**限流，非全局 | SRC-02 |
| A-9 | 出站 HA 通道**硬切 4096 不分片**（`content[:MAX_MESSAGE_LENGTH]`）；Telegram/Discord/Slack/Signal 均分片 | SRC-02 + SRC-10 |
| A-10 | 平台适配器熔断后不自动恢复，需 `/platform resume` | SRC-02（既有笔记 06 已写，不重复） |

### 3.2 B 路线选型

| # | 主张 | 来源 + 锚点 |
|---|---|---|
| B-1 | 「装个现成 skill」在 HA 场景**不存在**：bundled + optional skills 中 smart-home 类只有 `openhue` 一个 | HMS-05 |
| B-2 | 三条路线：自建 SKILL.md / MCP server / 自定义 plugin；**互补而非替代** | HMS-05、HMS-04、HMS-06 |
| B-3 | MCP 与内置 toolset **同名不遮蔽**：解析为内置 4 个 + server 工具**叠加** | HMS-03 |
| B-4 | MCP 工具注册名 = **`mcp__<server>__<tool>`**（双下划线） | **SRC-04**（`MCP_TOOL_NAME_PREFIX = "mcp__"`） |
| B-5 | server 名/工具名中的 `-`、`.` → `_`；超 64 字符截断 + 8 位 sha256 后缀 | SRC-04 |
| B-6 | `tools.include` / `tools.exclude` 用**原始 MCP 工具名**（带连字符/点），不是注册名；`include` 优先 | SRC-04 → HMS-04；COM-23 同 |
| B-7 | `trust: untrusted` 下，凡无 `readOnlyHint: true` 的写工具**都需审批**；未识别值按 `untrusted` 处理（fail-closed） | HMS-04 |
| B-8 | `readOnlyHint` 只是**服务端自报**的提示；「a lying server can at most skip approval for tools it claims are read-only, never gain extra access」 | HMS-04 |
| B-9 | 自定义 plugin 最小示例与 `ctx.register_tool(name=, toolset=, schema=, handler=)`；plugins **默认 opt-in**，须 `hermes plugins enable` | HMS-06 |
| B-10 | `hermes mcp add/test/login`、会话内 `/reload-mcp` | HMS-07、HMS-10 |
| B-11 | **ha-mcp 的 Setup Wizard 支持 Hermes**，给专属 YAML 模板 + `${env:VAR}` 从 `~/.hermes/.env` 解析 + `/reload-mcp` 提示 | **COM-23** |
| B-12 | ha-mcp 端点是 **Streamable HTTP only**（POST-only），SSE 预检返 **405** | COM-23 |
| B-13 | ha-mcp `/readonly` 后缀是**连接级**模式，不是凭证级权限（同凭证在正常端点仍可写） | COM-01 |
| B-14 | `hermes mcp test` 打印**原生**工具名，不能用来验证注册名前缀 | SRC-07 |

### 3.3 ① 三方对照轴

| # | 主张 | 来源 + 锚点 |
|---|---|---|
| C-1 | HA 内建 LLM 的边界句是四个 LLM 集成页 `Control Home Assistant` **配置项描述**：「If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed] to it.」**不在** HAS-17，**不在** HAS-09 | HAS-18/19/20/21（**归属已更正**） |
| C-2 | 官方开发者口径：「The Assist API is equivalent to the capabilities and exposed entities that are also accessible to the built-in conversation agent. **No administrative tasks can be performed.**」 | HAS-16 |
| C-3 | 暴露的设计意图原文：「This is to avoid that sensitive devices, such as locks and garage doors, can inadvertently be controlled by voice commands.」 | HAS-09 |
| C-4 | 四个 LLM 集成页均写「This integration does not integrate with [sentence triggers].」 | HAS-18/19/20/21 |
| C-5 | 而 HAS-17 写外部 agent「only use sentence triggers when **Prefer handling commands locally** is enabled」——**与 C-4 无法在官方文档内对齐** | HAS-17 |
| C-6 | Ollama 路线官方限制最全：实验性、建议暴露 **<25** 实体、**只支持有 Tools 的模型**、小模型对话不可靠、官方给「同模型两份配置（一开一不开控制）」的降级法 | HAS-21 |
| C-7 | 纯确定性自动化的三段结构：「All automations are made of at least a [trigger] and an [action]. Optionally combined with a [condition].」 | HAS-23 |
| C-8 | action response data 与 `response_variable` 是「不靠 LLM 也能出日报」的官方机制 | HAS-10 |
| C-9 | `persistent_notification.create` / `dismiss` / `dismiss_all`；并以 `notify.persistent_notification` 暴露 | HAS-15 |
| C-10 | `notify.notify` 官方警告：「shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect.」 | HAS-24 |
| C-11 | 无 LLM 对照实现确实存在：`No cloud. No API keys. No LLM. No subscription.` | COM-03 |
| C-12 | 确定性基线 + LLM 分工的一手实现：z-score 7 天基线（3.5σ × 连续两次）、三层权限、预算做成配置键 | COM-05 |
| C-13 | 另有定位相反的实现：`Sentinel anomaly engine keeps safety decisions deterministic, with the LLM advising but never actuating.` | COM-06 |
| C-14 | 「HA 主动发起对话」= **2025.7** 的 `assist_satellite.ask_question` | **HAS-26** |
| C-15 | 「自动化编辑器 Suggest 按钮」= **2025.8**，且默认不可见，需在「AI suggestions」设置里开启 | **HAS-27** |
| C-16 | 博客 HAS-07 通篇**无版本号**；对 (a) 甚至给的是 blueprint 链接而非功能文档链接 | HAS-07 |

### 3.4 ② 安全与限界

| # | 主张 | 来源 + 锚点 |
|---|---|---|
| D-1 | LLT **不带 scope claim**（`async_create_access_token` 只编码 `iss`/`iat`/`exp`），权限来自**用户上下文** | SRC-14 |
| D-2 | 「token 权限 = 创建它的用户」属**源码级推论**，HA 文档从未明文写 | SRC-14 + probe-04 |
| D-3 | LLT **有效期 10 年**；吊销 = revoke refresh token，立即连带撤销其签发的全部 access token | HAS-05 + SRC-14 |
| D-4 | **non-admin 也能创建 LLT**（`@websocket_api.ws_require_user()`，非 `@require_admin`） | SRC-14 |
| D-5 | 想做细粒度只读只能靠**受限用户/组**（entity/domain/area/device 粒度，是**用户属性不是 token 属性**） | HAS-06 |
| D-6 | Assist 暴露粒度 = 逐实体 + 多选批量，**无 domain/area 批量** | HAS-09 |
| D-7 | mcp_server：`/api/mcp/assist` 恒可用；**其他 API ID 要求 admin** | HAS-01 / HAS-25 |
| D-8 | **暴露列表是软约束**：COM-14 记录「只读提问 → 未暴露实体被 toggle」，`not_planned` 关闭；COM-12 作者直言「it is hard to validate whether a query is only using exposed entities」 | COM-14、COM-12 |
| D-9 | ha-mcp 的实体作用域是 **`Everything in Home Assistant`**（官方内建为 `Only entities exposed to Assist`）——这是**官方明文的路线差异** | COM-01 |
| D-10 | MCP 工具 schema 本身有 token 代价：77 工具 ≈ **60.3k tokens** 常驻 | COM-16 |
| D-11 | 成本不随暴露实体数单调变化：同帖内 242 实体报 0.6 分/次，而 340→100 实体仍报「简单请求 5000 tokens」 | COM-22 |
| D-12 | 本地推理非免费：16GB VRAM 起、仅 8–16K context | COM-19 |
| D-13 | 误报的具体机理有来源：只读询问触发写动作（COM-21）、brightness 单位不一致（COM-15）、模型不支持 tools 却输出 JSON（COM-20） | COM-15 / COM-20 / COM-21 |
| D-14 | 写权限事故有实例：`ha_assign_label` 覆写导致 entity registry 损坏 | COM-18 |
| D-15 | **误报率无任何来源给出分母**，全部是单次事件叙述 | probe-06 未解决项 5 |

### 3.5 ③ 文档与代码不一致（本篇最稀缺的一类结论）

| # | 文档怎么说 | 代码/实际情况 | 来源 |
|---|---|---|---|
| E-1 | MCP 工具前缀 `mcp_<server>_<tool>`（HMS-11、HMS-10 及**发布站**） | 实为 **`mcp__<server>__<tool>`**；`mcp_<server>_<tool>` 是 #33533 改名前的旧写法 | SRC-04 vs HMS-11 / HMS-10 |
| E-2 | — | **改名不彻底**：`agent/anthropic_adapter.py` 与 `tests/…test_anthropic_mcp_prefix_strip.py` 的 **docstring 仍写旧写法** | SRC-05、SRC-06 |
| E-3 | mcp_server 配置项 `Control Home Assistant`（三段历史快照逐字未变） | **任何分支、任何历史版本都没有对应代码键**；44 条提交里从无 control/read-only 类选项；首版起只有 `CONF_LLM_HASS_API` | HAS-01 vs SRC-11/12/13 |
| E-4 | — | dev（2026.10）真正的开关叫 `require_admin`，UI 文案 `Require an administrator account`——**名称与语义都不是 `Control Home Assistant`** | SRC-12 |
| E-5 | 文档与 `master`/`rc`(2026.9) docstring：`/api/mcp` 「does not require admin access」 | dev(2026.10) 改为「requires admin access **when the config entry is configured to require it**」——**同一端点跨版本行为相反** | SRC-11 vs SRC-12 |
| E-6 | — | `require_admin` **同版本内默认值不一致**：新装 `True`，1.1→1.2 迁移 `False`（源码注释自认 `Endpoints served before this option existed stay open.`） | SRC-12 |
| E-7 | HMS-08：「Outbound messages from the agent are delivered as Home Assistant persistent notifications」（无条件陈述） | 出站有**两条**分支，走哪条由 cron 进程里**有没有活的 gateway adapter** 决定；脱 gateway 路径改用 `notify.notify` | HMS-08 vs **SRC-08** / SRC-02 |
| E-8 | HMS-09 cron 页 `homeassistant` 投递目标**Example 列为空**（对比 telegram 等均有值） | 目标名在代码里合法（`_KNOWN_DELIVERY_PLATFORMS` 含 `"homeassistant"`），但**文档层止于一行表项** | HMS-09 + SRC-08 |
| E-9 | `plugin.yaml` description 提了 `notify.notify` 但**未定义 "out-of-process" 的判定条件** | 条件只在源码 docstring 里 | SRC-03 vs SRC-08 |
| E-10 | SKILL.md frontmatter：HMS-12 与 HMS-05 **给出两套互不覆盖的字段表** | 无「本表为准」措辞，仓库内也**未找到 frontmatter schema 文件** | HMS-12 vs HMS-05 |
| E-11 | mcp_server 代码里 `MORE_INFO_URL = "...mcp_server/#configuration"` | 文档实际锚点是 `## Configuration options` → `#configuration-options`，`#configuration` **在文档中不存在** | SRC-11 |
| E-12 | workflow 文档自身：`todo-state.sh … confirm P2` / `mode P2 freeform` | 脚本实际只接受 `start\|complete\|skip\|block` | `.claude/workflows/learning-note-flow/workflow.md` vs `.claude/scripts/todo-state.sh` |

> E-12 与主题无关，但属同类现象，作为「本项目内也发生过」的注脚可选引用。

---

## 四、矛盾清单（写正文时必须择一并标注）

1. **MCP 前缀：三处官方文档两种写法**。源码（SRC-04）与 ha-mcp 的 Setup Wizard（COM-23）一致指向 `mcp__<server>__<tool>`；HMS-10 / HMS-11 与发布站为旧写法。**结论：以 `mcp__` 为准，把旧写法作为「文档漂移案例」引用。**
2. **`Control Home Assistant` 究竟存在与否**：官方 markdown 有三段历史快照佐证其长期存在，但代码侧查无对应键。**结论：不判定其真伪，写成「文档有、代码无对应项」并给两侧证据。**
3. **`/api/mcp` 的 admin 要求跨版本相反**（2026.9 vs 2026.10）。**结论：正文必须带版本号。**
4. **sentence triggers**：四个 LLM 集成页绝对否定 vs HAS-17 给条件性例外；`Prefer handling commands locally` 在四个 LLM 集成页全文无命中。**结论：如实并列，标注为官方文档内部冲突。**
5. **「暴露列表 = 安全边界」说法互相冲突**：官方当设计意图（HAS-09）、官方 issue 记录穿透（COM-14，not_planned 无解释）、第三方作者自认无法校验（COM-12），而 COM-01 / COM-11 把它当安全保证来陈述。**结论：写成「官方设计意图 ≠ 运行期强制边界」。**
6. **ha-mcp 工具数同一 README 内三处不一致**（87 / 95+ / ~84）。**结论：不给单值，写成「README 自述 ~84–95，口径不一」。**
7. **ha-mcp 客户端清单：README 不含 Hermes，Setup Wizard 含 Hermes**。**结论：写「受支持但 README 未列」。**
8. **`home-generative-agent` 的「真实沙箱」**：子代理 C 跨 README/CHANGELOG/docs/CI **回源失败**，全仓 `sandbox` 唯一命中是谈 `python_script` 沙箱；真实机制是 `cv.determine_script_action` 静态筛查 + PIN。**结论：该说法不得进入正文**（详见 §5.3）。
9. **SKILL.md frontmatter 两套字段表**，且 `related_skills` 疑似悬空（仅 HMS-12 出现 1 次、无消费方说明）。**结论：写字段时以 HMS-12 为主表，标注 HMS-05 的差异（尤其 `category`）。**
10. **C-4 与 C-5（sentence triggers）** 与第 4 条同源，写作时合为一处「官方文档内部冲突」。

---

## 五、对 P1 记录的更正（P4 写作前必须替换）

### 5.1 边界句的页面归属

P1 的 F5 把「只控制已暴露实体」这句挂在了错误页面上。回源结果：该句只出现在 **HAS-18/19/20/21 四个 LLM 集成页**的 `Control Home Assistant` **配置项描述**里，且前面还有一句「If the model is allowed to interact with Home Assistant.」；**HAS-17 与 HAS-09 都没有这句**。

### 5.2 `GetLiveContext` issue 的状态

P1 记为「已 closed」。实为 **closed as `completed`，2026-09-08**，即**已被修复**。引用时必须写成「已修补的历史缺陷」，不能当当下行为。

### 5.3 `home-generative-agent` 的「挂载真实沙箱」——回源失败

- **回源范围**：README、CHANGELOG、`docs/architecture.md`、`docs/configuration.md`、`CONTRIBUTING.md`、`AGENTS.md`、`.github/workflows/validate.yml`
- **结果**：无「真实沙箱」类说法；全仓 `sandbox` 唯一命中是 CHANGELOG 第 531 行谈 `python_script`
- **真实机制**：`cv.determine_script_action` **静态筛查**（allowlist over HA 的 action taxonomy；`Screening fails closed on anything it cannot resolve`）+ PIN 门禁
- **官方自陈的三类漏洞**：`Raw protocol writes are not screened.`（点名 `mqtt.publish` / `zwave_js.set_value` / `zha.issue_zigbee_cluster_command`）；`Targets that resolve at run time cannot be inspected.`；蓝图型自动化「the PIN attests to what the blueprint did **at approval time**」
- **「真实」二字的可能来源**：「confirmed against a real Home Assistant install by two independent reviewers」——指**发布前人工复核**，不是运行时沙箱
- **处置**：**该说法不得进入正文**；如要再引，需重新回源

### 5.4 ollama 边界句的截断

P1 引为「Controlling Home Assistant is an experimental feature」。原文为整句：「Controlling Home Assistant is an experimental feature that provides the AI access to the Assist API of Home Assistant.」

### 5.5 `creating-skills.md` 的路径

P1 记 `user-guide/features/creating-skills.md`，仓库中不存在（站点 404）。实为 **`developer-guide/creating-skills.md`**。

### 5.6 对 P1 结论的确认（未变）

- `LLT 无 scope claim` / `权限 = 创建者用户` —— **维持**（源码级推论，非官方明文）
- `cooldown_seconds 逐实体` —— **维持**
- `HA 出站 4096 硬截断` —— **维持**
- `MCP 与内置 toolset 同名叠加不遮蔽` —— **维持**（HMS-03，本轮未复核）
- `HA 侧无现成 HA skill` —— **维持**（HMS-05）

---

## 六、实战指导（可直接写进正文的结论）

### 6.1 默认路线建议

**首选：MCP server**（而非自建 SKILL.md、也非自定义 plugin），理由与边界：

1. **自建 SKILL.md 表达不了新能力**——它只能教 agent 怎么调已有 CLI/工具；HA 场景下不存在可调的 `ha` CLI（B-1、B-2）。只有当你已经用别的方式（如 `curl` + HA REST）提供了能力，SKILL.md 才有意义。
2. **自定义 plugin 只在 MCP/skill 都表达不了时用**——需要精确执行、二进制/流式、或必须走审批面的原生工具（B-9）。
3. **MCP server 是唯一能一次性补齐 A-3 三类缺口的路**（历史/统计、写配置、摄像头）。
4. **两条 MCP 子路线**：
   - **HA 官方 `mcp_server`**：跟 Assist 同源，实体作用域 = **仅已暴露实体**，**无**写配置/历史/摄像头（COM-01 对比表）。适合「只想用官方、且只要控制」。
   - **社区 ha-mcp**：实体作用域 = **Everything in Home Assistant**，含 automations/dashboards/helpers/backups，**Setup Wizard 支持 Hermes**（COM-23）。适合「要写配置、要历史、要摄像头」。

### 6.2 两条 MCP 子路线的接入要点

**ha-mcp → Hermes**（有官方模板，照抄即可）：

- Setup Wizard 的 Hermes 分支给出三种 transport 的 YAML（HTTP / `uvx` stdio / Docker stdio）
- `mcp_servers` 条目名建议 `home-assistant`（工具名将变成 `mcp__home_assistant__<tool>`，因连字符被 sanitize 成下划线）
- 鉴权两种写法：`headers: { Authorization: "Bearer ${env:HA_TOKEN}" }`（`${env:VAR}` / `${VAR}` 从 `~/.hermes/.env` 解析），或 `auth: oauth`
- **传输必须 Streamable HTTP**：切 SSE 会被 405 拒
- 改完配置在会话里 `/reload-mcp`，无需重启
- 只要读：给端点加 `/readonly` 后缀（连接级，非凭证级）
- **同一个 server 别在客户端里留两条条目**（README 明示是连接挂起的已知原因）

**HA 官方 `mcp_server` → Hermes**（**无官方 Hermes 示例**，需自行拼接）：

- 端点 `/api/mcp`（Assist 恒为 `/api/mcp/assist`）
- 官方页面给了 **6 个第三方 client 示例**（Claude for Desktop / ChatGPT / Claude Code / Codex / Cursor / Antigravity CLI），**没有 Hermes**
- 官方对不支持 OAuth 的客户端给了出路：「Some MCP clients may not support OAuth, but may support access tokens.」→ 走 **LLT bearer header** 是最省事的接法
- 若走 OAuth（IndieAuth）：`client_id` 必须是**客户端应用的 base URL**，且「It must never be your Home Assistant instance URL.」；Codex 示例用本地回调 `http://127.0.0.1:12345` 且强调 callback 端口必须与 `client_id` 端口一致——Hermes 侧是否支持等价回调 **未验证**
- 反代/隧道场景 hostname 必须匹配 HA 的 Internal URL 或 External URL，否则 metadata 返回相对路径被拒
- **裁剪工具集**用 `tools.include` / `tools.exclude`，写**原始**工具名

### 6.3 cron → HA 投递（官方无端到端示例，按源码事实写）

- **目标名**：`homeassistant` 合法（HMS-09 表内一行 + SRC-08 的 `_KNOWN_DELIVERY_PLATFORMS`）
- **投递走哪条**由**执行位置**决定，不由消息内容决定：
  - gateway 进程内执行（有 `adapters`/`loop`）→ `persistent_notification.create`
  - 脱离 gateway 执行（`adapters is None`）→ `notify.notify`
  - 第三种：detached worker 且 `_HERMES_CRON_EXTERNAL_WORKER` 命中 → 进 `cron.delivery_queue` 持久队列，由 gateway 用 live adapter 完成
- **必须提醒读者的坑**：`notify.notify` 是「第一个能找到的 notify action」，官方自己警告目标可能不在你预期处；两条分支在 HA 语义上并不同质
- **长报告**：HA 通道硬切 4096 不分片，日报类内容会被静默砍尾（A-9）
- **官方 cron 页没有 HA 示例，Example 列是空的**——正文如实说明，然后给「按源码事实拼出的写法」并标为**拼接**

### 6.4 什么不该交给 agent（三方对照轴的落点）

用官方原文作为判据：

- **管理类任务不该给内建 LLM 路线**：HAS-16 明说 Assist API「No administrative tasks can be performed.」
- **敏感设备（锁、车库门）默认不暴露**：HAS-09 的设计意图原文就在讲这个，但**别把它当强制**（D-8 有反例）
- **能用确定性规则表达的，不要用 LLM 表达**：阈值/时长/状态类告警用 HAS-12（Alert）/ HAS-11（trigger）；报表用 HAS-10 的 action response data + `response_variable`；对照实现 COM-03 明说不用云、不用 key、不用 LLM
- **要 LLM 学基线而非设阈值的**，参考 COM-05 的 z-score（7 天基线、3.5σ、连续两次才报、设备约 2 周才「获得被告警资格」）
- **成本要按 token 预算而非实体数估算**：工具 schema 本身就是常驻开销（COM-16 的 60.3k tokens），实体数不是单调解释变量（D-11）

### 6.5 安全最小化的操作顺序（可写成一份清单）

1. 别用 admin 账号建 LLT；建一个**受限用户/组**，用它的身份发 LLT（D-4 允许、D-5 提供粒度）
2. 该用户的实体权限按 entity/domain/area 收紧（D-5）
3. HA 官方 mcp_server 路线下，Assist 之外的 API ID 需 admin → 想避免就给非 admin 用户只开 Assist（D-7）
4. MCP 侧 `trust: untrusted` 起步；别信 `readOnlyHint`（B-7、B-8）
5. 用 `tools.include` 白名单而非 `exclude` 黑名单（B-6）
6. 事件转发从默认全关开始，逐个开 `watch_entities`，`cooldown_seconds` 按实体调（A-7、A-8）
7. 只读场景优先用 `/readonly` 端点（B-13）
8. 涉及写配置的，先 dry-run / 备份 / 可回滚（COM-05 的 atomic write → reload → verify → rollback）

---

## 七、未解决问题（按是否阻塞写作分级）

### 7.1 阻塞项 → 需你实机执行（本机无 `hermes` CLI，我无法代验）

| # | 问题 | 命令 | 影响 |
|---|---|---|---|
| Q-1 | 你的 Hermes 版本处于单下划线还是双下划线时期 | `hermes --version` | 决定正文写 `mcp__` 时是否需要附加版本说明 |
| Q-2 | 你本机实际注册名是什么 | 会话内 `/reload-mcp` 后让 agent 列出 MCP 工具全名 | 与 Q-1 互证 |
| Q-3 | `hermes mcp test` 是否真的只打印原生名（未实机跑过） | `hermes mcp test <server>` | 影响 §6.2 的排错建议措辞 |
| Q-4 | 你的 HA 版本是 2026.9 还是 2026.10 | HA「关于」页 | 决定 E-5 怎么写（跨版本行为相反） |

**Q-1/Q-2/Q-4 未回填不影响开写**——正文按「源码为准 + 标注版本差异」写即可，回填只是把注释变成确定值。

### 7.2 不阻塞，但正文必须如实标注为缺口

| # | 缺口 | 现状 |
|---|---|---|
| G-1 | `Control Home Assistant` 的文档来源 | 代码侧查无对应键；需 HA release notes / PR 讨论才能定论 |
| G-2 | `require_admin` 是否进 2026.10 正式版 | `dev` 有、`rc` 无，是否 revert 未知 |
| G-3 | SKILL.md frontmatter 的机器可读 schema | 仓库内未找到 schema/loader，只能靠 HMS-12 与 HMS-05 互证 |
| G-4 | `related_skills` 的消费方 | 仅 HMS-12 出现，作用未知 |
| G-5 | `blueprint.schedule` 的 `"every 2h"` / ISO 写法 | 无语法定论 |
| G-6 | `_deliver_standalone` 如何取 `standalone_sender_fn` | 未逐行确认（文件 94267 字节） |
| G-7 | `Prefer handling commands locally` 在哪个集成页有文档 | 四个 LLM 集成页全文无此串 |
| G-8 | HA 文档页均无「最后更新」时间戳 | 站点不暴露；只能记抓取时间 |
| G-9 | 误报率无分母 | 全部为单次事件叙述，无法算比率 |
| G-10 | 无「月账单 + 实体数 + 模型名」三者齐全的 >6 个月记录 | 最长记录缺项 |
| G-11 | 未找到 HA 侧 prompt injection / 恶意实体名触发的实测帖 | 仅媒体定性警告（二手，未采信） |
| G-12 | **Reddit 未被覆盖** | 三轮精读均未返回 reddit.com 结果 |
| G-13 | **进阶路径/学习资源轴最薄** | 见 §9.5 |

### 7.3 需在 P4 复核（我自己造的转述风险）

- probe-06/07/08 中标 **【子代理采集】** 的社区条目（COM-16~22 等）主流程**未逐条回源**；凡被当成「实测数字」引用前，需按同一标准直读核验，尤其是 **COM-16（60.3k tokens）** 与 **COM-22（token 消耗）**
- 本文件 §3 的每条主张都已挂 ID + 锚点，但**引用时仍须回原文逐字比对**，不得只凭本表措辞落笔

---

## 八、引用纪律（P4 的 write 前置约束）

1. **不得转述带 ID**：给 writer 的提示只放「来源 ID + 检索位置（锚点/行号）」，不放我改写过的句子。需要带结论时必须**原文加引号**或**明确标「未核实概述」**。
2. **每处「官方口径是 / 原文 / 官方说明」逐条回源**：验收时按 ID 打开 `sources/` 下的快照或重取原页比对，**不能只看有没有挂 ID**。
3. **版本必须带**：HA 侧任何涉及 `/api/mcp` 鉴权的句子都要写清 2026.9 / 2026.10。
4. **【子代理采集】标注要保留**：未回源的社区数字在正文里要么删，要么标来源与未复核状态。
5. **「拼接」块必须标记**：无一手示例的组合配置（如 HA 官方 mcp_server → Hermes 的 YAML）要显式标注为拼接、未经官方或实机验证。
6. **已修复的历史缺陷要标注**：COM-13 要写成「已修补」，不能当作当前行为。

---

## 九、素材质量与 P2 完成度

### 9.1 数量与档位

| 维度 | 数量 | 评价 |
|---|---|---|
| HA 官方文档 / 博客 / release notes | **28 条**（HAS-01..28，HAS-28 为排除用组） | 充足；每条路线与安全机制都有官方页，且本轮把「文档没写」也变成了有证据的结论 |
| Hermes 官方文档 | **12 条**（HMS-01..12） | 够用；发现两处文档漂移（E-1、E-10） |
| 一手源码 | **14 条**（SRC-01..14，跨 Hermes 与 HA core 两仓库、含 dev/rc/master 三分支与提交史） | **最强的一档**；前缀、分支条件、权限模型、跨版本差异全部源码级 |
| 社区 / 第三方 / issue | **23 条**（COM-01..23） | 够用；提供场景灵感与失败实例，但 **COM-16~22 主流程未逐条回源** |
| 官方 issue（一手） | 3 条（COM-13/14/15） | 关键；其中 1 条已修复、2 条 `not_planned` 无解释 |
| 待核对 / 未解决 | **14 项**（§7.2 的 G-1..G-13 + §7.1 待实机 4 项） | 集中在「文档与代码不一致」与「官方不写」，**均已如实标注，不阻塞开写** |

### 9.2 对 P2 检查项的自评

| 检查项 | 状态 | 依据 |
|---|---|---|
| 核心概念/理论素材 | ✅ | 三方对照轴（§3.3）、权限模型（§3.4）、工具天花板（§3.1） |
| 实战代码/项目案例 | ✅ | COM-23 三种 transport YAML、B-9 plugin 最小示例、COM-05 权限/预算/回滚设计、COM-03 无 LLM 对照 |
| 常见坑/最佳实践 | ✅ | §3.5 的 12 条文档/代码不一致 + §6.5 操作顺序 |
| 工具链/生态 | ✅ | ha-mcp（含 Setup Wizard）、hass-mcp、mcp-assist、myla/generative-agent、HA 官方 mcp_server、HACS 组件 |
| 进阶路径/学习资源 | ⚠️ **最薄** | 只有官方文档索引与项目清单，缺体系化学习路径；Reddit 未覆盖（G-12、G-13） |
| 素材质量已确认 | ⏸️ **待你确认** | 本表即确认材料 |

### 9.3 结论

8 个 P1 缺口**全部结案**，其中 3 个是「官方确实没写」的否定结论、1 个由源码定论。新增 12 条「文档与代码不一致」证据，构成本篇最稀缺的内容——**这是别的教程不会告诉读者的部分**。

唯一明显短板是**进阶路径/学习资源**轴（G-13），需要在 P3 决定是「补一轮检索」还是「降格为一小节」。

---

## 十、下游交接（给 outline-generator 与 chapter-writer）

### 10.1 建议章节骨架（供 P3 取舍，不是既定大纲）

基于 P1 已确认的 A+B + 三处增补，材料能支撑的骨架：

| 章 | 主题 | 主要素材 ID |
|---|---|---|
| 0 | 开篇结论：能做什么由路线决定；「装个现成 skill」不存在 | B-1、A-3、COM-23 |
| 1 | 你现在的起点：4 个内置工具的天花板 | A-1..A-9、SRC-01/02 |
| 2 | 三方对照轴：什么该交给 agent，什么本来就该用自动化 | §3.3 全部、COM-03/05/06 |
| 3 | 路线选型：skill / MCP / plugin 三者何时用 | §3.2 全部、B-14 |
| 4 | 落地：ha-mcp 接 Hermes（有官方模板） | COM-23、COM-01、B-6/B-7/B-12/B-13 |
| 5 | 落地：HA 官方 mcp_server 接 Hermes（拼接，需标注） | HAS-01/25、HAS-26、B-4/B-5 |
| 6 | 事件驱动与定时任务：白名单、限流、投递两条分支与 4096 截断 | A-7/A-8/A-9、SRC-02/08、HMS-09 |
| 7 | 安全与限界（独立成章）：LLT、权限粒度、暴露列表的真相 | §3.4 全部、SRC-14、COM-14 |
| 8 | 文档与代码不一致（成坑）：12 条实例 | §3.5 全部 |
| 9 | 成本与可靠性：token 常驻、误报机理、没有分母的误报率 | COM-16/19/22、D-11..D-15 |
| 附录 | 实机核对清单（Q-1..Q-4 命令）与未解决问题 | §7 |

### 10.2 传给下游什么

- **路径**：本文件 + `research/probe-01..08-*.md` + `sources/`
- **ID 体系**：只用 §2 的 canonical ID（`HAS-/HMS-/SRC-/COM-`）
- **不传**：本文件的转述句、`sources/` 下的整页正文
- **必须随附的约束**：§8 的 6 条引用纪律

### 10.3 写作时逐条要小心的断言

以下断言在 P4 极易被写成「官方说……」而实际是**推论或拼接**：

| 断言 | 真实性质 |
|---|---|
| 「LLT 的权限就是创建它的用户的权限」 | **源码级推论**，HA 文档从未明文写（D-2） |
| 「暴露列表就是安全边界」 | **官方设计意图**，非运行期强制（D-8、矛盾 5） |
| HA 官方 `mcp_server` 接 Hermes 的 YAML | **拼接**，官方无 Hermes 示例（§6.2、缺口 2） |
| 「HA 出站只发 persistent notification」 | **不完整**，脱 gateway 路径是 `notify.notify`（E-7） |
| 「`Control Home Assistant` 是个开关」 | **代码里查无此项**（E-3） |
| 「cron 可以把日报投到 HA」 | 目标名合法、代码支持，但**官方无端到端示例**（E-8，§6.3） |

---

**阶段状态**：P2 交付物已生成。等待用户确认素材质量后，方可将 P2 标记完成并进入 P3（大纲生成）。
