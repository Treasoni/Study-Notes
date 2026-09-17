# 阶段 1 探测结果：用 Hermes Agent 控制 Home Assistant

> 生成时间：2026-09-18 ｜ 运行：`hermes-home-assistant` ｜ 方向：A 能力地图 + B 路线选型
> **本文件是阶段 1 交付物**。原始证据在 `research/probe-01..05-*.md`，本文件只做汇总与指向，不复制原文。

## 一句话结论

内置 HA 工具只有 4 个且**无历史/无写配置/无摄像头**能力，所以"能做什么"的上限由"走哪条路线"决定——这正是把 A、B 合成一篇的理由。而"推荐个 skill 装上就行"这条最省事的路，在 HA 场景**不存在**。

## 二、五批探测记录

| 批次 | 主题 | 原始记录 | 主要待核对 |
|---|---|---|---|
| probe-01 | HA 侧四条技术路线（官方 MCP / 社区 MCP / Assist / REST·WS） | `research/probe-01-ha-routes.md` | 7 条 |
| probe-02 | Hermes 侧工具清单、平台适配器、MCP / skill / plugin | `research/probe-02-hermes-tools.md` | 8 条 |
| probe-03 | 真实用例场景清单（14 个场景） | `research/probe-03-scenarios.md` | 9 条 |
| probe-04 | HA 权限模型 与 审批 / 成本控制（源码级） | `research/probe-04-permissions-cost.md` | 9 条 |
| probe-05 | 三条路线的可抄配方 | `research/probe-05-recipes.md` | 8 条 |

## 三、关键发现（按对笔记骨架的影响排序）

### F1 内置能力有硬天花板，路线选择由此决定

- Hermes 内置 HA 工具**恰好 4 个**：`ha_list_entities` / `ha_get_state` / `ha_list_services` / `ha_call_service`（源码 docstring 原文，来源 HMS-01）
- 缺三块：**历史/统计**、**写配置（自动化）**、**摄像头/结构化 AI 任务**
- 落在这三类里的场景，内置工具**做不到**，必须 MCP 或自定义 plugin（probe-03 待核对第 9 条）
- 另：`ha_list_entities` 的 `area` 参数匹配的是 friendly_name 或 area 属性，**不是** HA 的 area registry（来源 HMS-01）

### F2 "装个现成 skill"这条路不存在

- Skills Hub 全部 bundled + optional skill 中，smart-home 类**只有 `openhue` 一个**；**没有 Home Assistant skill**（来源 HMS-04、HMS-05）
- 社区 MCP 项目倒是有现成的（ha-mcp 4762★ 自述 87 tools），但那是 **MCP 路线**，不是 skill
- 结论：HA 场景下 skill 路线 = **自建** SKILL.md

### F3 三条路线互补，不是替代关系

| 路线 | 什么时候用 | 代价 |
|---|---|---|
| 自建 SKILL.md | 能力已由 CLI/工具提供，只需教 agent 怎么调 | 最低；但表达不了新能力 |
| MCP server | 需要现成的大工具集（87 tools）或官方 Assist 通道 | 中；多一层进程/信任面 |
| 自定义 plugin | MCP 和 skill 都表达不了的原生工具，或要走审批面 | 最高；要写 Python |

关键细节：MCP server 若与内置 toolset **同名**（如就叫 `homeassistant`），解析结果是**内置 4 个工具 + 该 server 的工具叠加**，不是遮蔽（来源 HMS-03）。

### F4 HA 官方自己也在做，agent 不是唯一解

- 2025.9 起 HA 可主动发起对话（"you can now have Home Assistant initiate conversations."，来源 HAS-07）
- `ai_task.generate_data` 可在自动化/脚本/模板里直接调 AI，支持 `structure` 字段与 camera 附件（来源 HAS-08）
- 自动化编辑器有 Suggest 按钮
- 对照案例：`ha-household-briefing` 明确 "No cloud. No API keys. No LLM. No subscription."（来源 COM-03）
- → 建议写成第三根轴：**HA 内建 LLM / 外部 agent / 纯确定性自动化**，回答"什么该交给 agent，什么本来就该用自动化"

### F5 安全材料足够单独成章

- **LLT 没有细粒度权限**：token 不带 scope，权限 = 创建它的用户（源码级推论，HA 文档从未明说）；想做只读 agent 只能靠**受限用户/组**（HA 用户/组级实体权限支持 entity/domain/area/device 粒度）（来源 HAS-05、HAS-06）
- LLT **有效期 10 年**；吊销 = revoke refresh token
- 工具层硬防线：**blocked domains** 黑名单（`shell_command`/`command_line`/`python_script`/`pyscript`/`hassio`/`rest_command`）+ SSRF 路径穿越防护，且"先格式校验后黑名单"（来源 HMS-01）
- 审批面：MCP `trust: full/untrusted`，`untrusted` 下写操作需审批；`readOnlyHint` 只是**服务端自报**的提示
- 事件洪泛：`cooldown_seconds`（默认 30）是**逐实体**限流；事件去重（值未变不发）；默认**一条都不转发**

### F6 已验证的坑（现有笔记 06 未覆盖）

- **出站消息在 HA 通道是硬切 4096，不分片**（`content[:MAX_MESSAGE_LENGTH]`），而 Telegram/Discord/Slack/Signal 都分片 → 日报/巡检长报告会被静默砍尾（来源 HMS-02）
- **MCP 工具命名前缀同一仓库内三处冲突**（`mcp_<server>_<tool>` / `mcp__<server>__<tool>` / `mcp_chrome_devtools_win_list_pages`）→ 正文必须实机验证（probe-05 待核对第 1 条）
- **官方文档与代码冲突两处**：`mcp_server` 的 "If MCP clients are allowed to control Home Assistant" 在 2026.9.0 代码里找不到对应布尔；dev 分支 `require_admin` 默认值在新装与迁移路径不一致（probe-04 待核对第 1、2 条）
- `platforms.homeassistant.token`（YAML 键）优先于环境变量 `HASS_TOKEN`，但该键未在文档中列出（来源 HMS-02）
- 平台适配器**熔断后不自动恢复**，需 `/platform resume`（既有笔记 06 已写，本次不重复）

## 四、来源索引（项目内 ID，供正文引用）

ID 采用 `HAS-`（HA 官方）/ `HMS-`（Hermes 官方）/ `COM-`（社区项目）三前缀，避免与既有 `hermes-agent` 项目的 S1–S21 编号冲突。

### HAS（Home Assistant 官方）

| ID | 来源 |
|---|---|
| HAS-01 | https://www.home-assistant.io/integrations/mcp_server/ |
| HAS-02 | https://www.home-assistant.io/integrations/mcp/ （HA 作 MCP client，与 HAS-01 是两页） |
| HAS-03 | https://developers.home-assistant.io/docs/api/rest/ |
| HAS-04 | https://developers.home-assistant.io/docs/api/websocket/ |
| HAS-05 | https://developers.home-assistant.io/docs/auth_api/ |
| HAS-06 | https://developers.home-assistant.io/docs/auth_permissions/ |
| HAS-07 | https://www.home-assistant.io/blog/2025/09/11/ai-in-home-assistant/ |
| HAS-08 | https://www.home-assistant.io/integrations/ai_task/ |
| HAS-09 | https://www.home-assistant.io/voice_control/voice_remote_expose_devices/ |
| HAS-10 | https://www.home-assistant.io/docs/scripts/service-calls/ （`target` 批量语义） |
| HAS-11 | https://www.home-assistant.io/docs/automation/trigger/ （`zone` 触发器） |
| HAS-12 | https://www.home-assistant.io/integrations/alert/ |
| HAS-13 | https://www.home-assistant.io/integrations/recorder/ （`recorder.get_statistics`） |
| HAS-14 | https://www.home-assistant.io/integrations/telegram_bot/ |
| HAS-15 | https://www.home-assistant.io/integrations/persistent_notification/ |
| HAS-16 | https://developers.home-assistant.io/docs/core/llm/ |

### HMS（Hermes 官方）

| ID | 来源 |
|---|---|
| HMS-01 | `NousResearch/hermes-agent` → `tools/homeassistant_tool.py`（4 工具、正则校验、blocked domains、gating） |
| HMS-02 | `NousResearch/hermes-agent` → `plugins/platforms/homeassistant/adapter.py`（watch_*、cooldown、事件模板、出站截断） |
| HMS-03 | `website/docs/reference/toolsets-reference.md`（toolset 定义、MCP 命名叠加、`all` 不启用 HA） |
| HMS-04 | `website/docs/reference/mcp-config-reference.md`（mcp_servers、trust、include/exclude） |
| HMS-05 | `website/docs/user-guide/features/skills.md` + `optional-skills/smart-home/openhue/SKILL.md`（skill 目录与格式；smart-home 仅 openhue） |
| HMS-06 | `website/docs/user-guide/features/plugins.md` + `developer-guide/plugins/index.md`（plugin 最小示例、opt-in） |
| HMS-07 | `website/docs/reference/cli-commands.md`（`hermes mcp` / `hermes skills` 子命令） |
| HMS-08 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant |
| HMS-09 | https://hermes-agent.nousresearch.com/docs/user-guide/features/cron （wakeAgent / no_agent） |
| HMS-10 | https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes （`/reload-mcp`、排错） |

### COM（社区项目 / 社区帖，引用前需回一手）

| ID | 来源 | 备注 |
|---|---|---|
| COM-01 | https://github.com/homeassistant-ai/ha-mcp | 4762★，README 自述 87 tools（未比源码） |
| COM-02 | https://github.com/voska/hass-mcp | 342★，走 HA WebSocket |
| COM-03 | https://github.com/archieboy-holdings/ha-household-briefing | **无 LLM** 的确定性对照 |
| COM-04 | https://github.com/cnc-lasercraft/haclaude | 夜间巡检 + 只读工具白名单（德文 README） |
| COM-05 | https://github.com/Oasis-Enterprise/mylo | 7 天 z-score 基线告警（README 自述） |
| COM-06 | https://github.com/goruck/home-generative-agent | 自然语言生成并注册自动化 |
| COM-07 | https://github.com/tevonsb/homeassistant-mcp | 576★，最后 push 2026-01（滞后） |
| COM-08 | https://github.com/ganhammar/hass-mcp-server | 69★，HACS 组件，OAuth 2.0 |
| COM-09 | https://github.com/allenporter/mcp-server-home-assistant | **已归档**，勿选 |
| COM-10 | 社区帖 1003703（Telegram/OpenClaw skill）、1003803（SmartHub）、908474（便宜模型 + tools）、1016481（Hestia） | 均为作者自报，无第三方复现 |

## 五、素材质量

| 维度 | 数量 | 评价 |
|---|---|---|
| 官方文档（HAS + HMS） | 26 | 充足；HA 侧每条路线与每个安全机制都有官方页 |
| 一手源码核验 | 3 个文件（tool / adapter / plugin.yaml）+ mcp_server http.py | 强；安全与实现细节达源码级 |
| 社区项目（COM） | 10 | 够用；提供"别人怎么玩"的场景灵感，但**均需回一手** |
| 官方博客 | 1（HA 2025-09-11 AI in Home Assistant） | 关键；支撑 F4 三方对照 |
| 待核对项 | 41（5 批合计） | 偏高，集中在"文档与代码不一致"与"拼接未验证" |

## 六、素材缺口（需 P2 或实机验证补齐）

1. **MCP 工具命名前缀**：同仓库三处文档冲突 → **必须实机** `hermes doctor` / `/tools list` 确认
2. **HA 端点接进 Hermes 的配置块**：两边文档都无此组合示例，`optional-mcps/` 里没有 homeassistant 条目 → 需实机或补检索
3. **ha-mcp 是否支持 Hermes**：其 Setup Wizard 覆盖 15+ 客户端，未确认含 Hermes
4. **`notify.notify` 与 `persistent_notification` 的分支触发条件**：仅见源码，官方页未文档化
5. **Hermes HA 平台页无 cron→HA 端到端示例**：需自行串（HMS-09 + HMS-08 两份文档拼）
6. **HA 博客的版本门槛**：主动对话 / Suggest 的确切版本需回 release notes
7. **`creating-skills.md` 全文未取到**（429）：frontmatter 字段清单待回源逐字确认
8. **`mcp_server` "control" 开关的文档/代码冲突**：未定论，正文只能写"文档如此、代码未见对应项"

## 七、方向菜单（P1 检查点：请确认素材质量与方向）

已定：**A 能力地图 + B 路线选型**。基于探测结果，建议三处增补：

| 增补 | 理由 | 材料 |
|---|---|---|
| **① 三方对照轴**：HA 内建 LLM / 外部 agent / 纯确定性自动化 | 回答"什么该交给 agent"，比单纯列能力有用 | F4，HAS-07/08、COM-03 |
| **② 安全与限界独立成章**（原 D） | 材料达源码级，塞进边角太浪费 | F5、F6，HAS-05/06、HMS-01/02 |
| **③ "文档与代码不一致"单列成坑** | 这是本文档最稀缺的价值：官方文档会骗人 | F6 后三条 |

形态待定：单册（约 6–7 章，估 25–35k 字）或分册。**建议单册**——本主题尚未大到需要分册；若写完超 30k 字再拆。

## 八、下一步

确认后 → `complete P1` → `start P2`（深度收集）。P2 的重点是补齐第六节 8 个缺口，尤其是需实机验证的 1、2、3。
