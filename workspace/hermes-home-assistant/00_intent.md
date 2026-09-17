# 用 Hermes Agent 控制 Home Assistant - 意图文件

## 基本信息

- **主题**: 用 Hermes Agent 控制 Home Assistant：能力地图与实现路线
- **项目标识**: hermes-home-assistant
- **创建时间**: 2026-09-18
- **当前阶段**: 阶段 0
- **输出目标**: project-output（发布阶段再确认 vault 位置）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定（候选 `AI学习/Hermes Agent/Hermes × Home Assistant 实战`，作为第五分册）
- **MOC 路径**: 待指定（候选 `AI学习/Hermes Agent/Hermes Agent MOC.md`）

## 学习目标

### 笔记类型

实战笔记（能力地图 + 路线选型；完整可抄模板作为选做）

### 学习深度

上手实战 —— 每个能力给出可落地写法，不满足于罗列名词

### 用户基础

有基础，非零起点：

- 已完成 Hermes ↔ HA 接入（`HASS_TOKEN` / `HASS_URL` 已配，四个 `ha_*` 工具可用）
- 已有 `AI学习/Hermes Agent/` 四册（上手实战 / Tool 配置 / Docker 部署 / Rules 配置）
- 已有 `homeassistant/` 目录的部署经验（docker-ha 分册、ai-smart-home-system、客户 A 实施）

## 研究计划

### 探索方向

1. **A 能力地图：连上之后到底能做什么**
   自然语言控制、场景联动、事件驱动的主动响应、日报/巡检、异常告警、跨平台遥控、语音。
2. **B 路线选型：每个能力走哪条路实现**
   Hermes skill（Skills Hub 现成 / 自建 SKILL.md） vs MCP server vs 自定义 tool —— 各自适配场景与成本。
3. **C 可落地方案（选做）**
   3–5 个高频场景，产出能直接抄的 `SKILL.md` / `config.yaml` / `automation.yaml`。
4. **D 安全与限界**
   LLT 权限最小化、事件白名单与洪泛控制、审批门、token 成本。

### 重点收集

- **核心概念**: 双向通道（事件进来 / 控制出去）、实体-域-服务模型、Long-Lived Token 权限范围、事件白名单机制、agent 自主性与审批边界
- **实战代码**: `ha_call_service` 调用示例、`platforms.homeassistant.extra` 配置、SKILL.md 模板、MCP 接入片段、HA automation YAML
- **常见坑**: 事件洪泛与 token 成本、LLT 权限过大、平台适配器熔断、HA 侧实体暴露范围
- **工具链**: Hermes skill 体系与 Skills Hub、MCP 路线（HA 官方 MCP Server 集成 / 社区 hass-mcp）、自定义 tool 注册、HA Assist 语音管道、REST / WebSocket API

### 信源偏好

- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

### 必须复用、不得重复的既有资产

- `AI学习/Hermes Agent/Hermes Agent 上手实战/06-多平台接入与定时任务.md` —— 其中「Home Assistant：智能家居双向接入」已讲完 LLT 接入、四个 `ha_*` 工具、`watch_domains` 白名单、事件转发默认全关。本次是新笔记，不重写接入步骤，只引用。
- `workspace/hermes-agent/research/` 已有语料（含 HA 相关源）与 `update_plan_06_homeassistant.md`
- `homeassistant/` 目录：docker-ha 分册、ai-smart-home-system（FastAPI + DeepSeek 自建智能体）、客户 A 实施

### 研究阶段必须回答的三个待澄清点

1. 「skills」分线交代：Hermes 侧 skill（Skills Hub 现成 / 自建 SKILL.md） vs MCP server（HA 官方 MCP Server 集成 / 社区 hass-mcp） vs 自定义 tool
2. HA 侧三条技术路线对比：官方 MCP Server 集成 / Assist 语音管道 / REST·WebSocket 直连
3. 安全与限界：LLT 权限最小化、事件白名单与洪泛控制、审批门、token 成本

### 已核实的关键前提（P0 阶段探测所得，2026-09-18）

- **Skills Hub 没有 Home Assistant skill**（smart-home 类仅 `openhue`）→ "装个现成 skill 就能用"这条路在 HA 场景不成立
- **内置 HA 工具只有 4 个**：无历史/logbook 查询、无模板渲染、`area` 参数匹配的是 friendly_name / area 属性而非 HA area registry
- 源码含 **blocked domains 黑名单**（`shell_command` / `command_line` / `python_script` / `pyscript` / `hassio` / `rest_command`）与 SSRF 路径穿越防护 —— 现有笔记 06 未覆盖
- MCP server 与同名内置 toolset **叠加而非遮蔽**；`untrusted` server 的写操作需过审批面
- 原始记录：`research/probe-01-ha-routes.md`、`research/probe-02-hermes-tools.md`（两份均带「待核对」清单）

**写作取向（用户已确认）**：把「Skill 路线在 HA 场景其实空缺」前置为开篇结论之一。

### 其他

- 用户未指定 vault 位置；按项目规则先落 `workspace/output/`，发布阶段（P6）再确认
