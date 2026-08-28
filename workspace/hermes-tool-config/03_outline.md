# Hermes Tool 配置指南 — 大纲

## 基本信息

- **定位**：实战笔记，独立成册《Hermes Tool 配置指南》（与《上手实战》分册同目录，不重复其内容）
- **深度**：上手实战
- **用户基础**：有了解（已用 Docker 跑过 Hermes，已有《Hermes Agent 上手实战》分册）
- **目标位置**：`AI学习/Hermes Agent/Hermes Tool 配置指南/`（分册文件夹 + 逐章文件，参照上手实战分册形态）；最终同步 `Hermes Agent MOC.md`
- **版本锚定**：v0.20.x（v0.20.6，2026-08-27）；所有配置键以 `hermes doctor` 输出为准
- **与《上手实战》第 5 章的边界**：第 5 章讲「skill 是什么/生命周期/SKILL.md」，本册专讲「tool 怎么配、怎么接」；仅在关系收束处交叉引用 [[Hermes Agent 上手实战/05-技能体系|第 5 章]]，不重复其正文

---

## 章节大纲

### 第 1 章：工具体系总览与配置入口

- **目标**：建立 tool 的整体心智模型（tool vs skill 边界），讲清三层配置入口（config.yaml 行为 / .env 密钥 / 运行时选择），让读者知道「工具在哪里配、配在哪一层」。
- **本章前置**：建议先读《上手实战》第 2 章（Docker 安装与 `~/.hermes` 挂载）、第 3 章（config.yaml + .env 基础）。
- **小节**：
  - ## 1.1 tool 是什么：可执行能力，与 skill 程序性知识的边界
  - ## 1.2 内置工具体系速览：约 86 个工具与 toolset 分组（web/search/terminal/file/browser/skills/mcp-<server>…）
  - ## 1.3 三层配置入口：config.yaml（行为） / `.env`（密钥） / `hermes tools` 运行时选择
  - ## 1.4 实操：启用与禁用 toolset
    - ### 交互式：`hermes tools` 逐项开关（按平台预设）
    - ### 临时：`hermes chat --toolsets "web,terminal,file"`
    - ### 持久：`hermes config set` 与全局 `agent.disabled_toolsets`
  - ## 1.5 Docker 场景：配置文件落在哪（宿主机 `~/.hermes` 挂载视角）
- **素材**：S1, S2, S5, S11, S8
- **代码示例**：有 — `hermes tools` / `hermes chat --toolsets "web,terminal"` / `hermes config set terminal.backend docker` 命令序列
- **篇幅**：3,500–5,000 字

---

### 第 2 章：内置工具与 toolsets 全解（terminal 后端与 Docker）

- **目标**：逐类过常用 toolsets，重点讲透 terminal 后端选择与「容器内的容器」概念，列出各类工具的凭据要求与输出截断行为，让读者能按需把工具开齐。
- **本章前置**：第 1 章；《上手实战》第 3 章（config.yaml）。
- **小节**：
  - ## 2.1 工具类别地图：Web / X Search / Terminal&Files / Browser / Media / Agent 编排 / Memory / Automation / Integrations
  - ## 2.2 terminal 后端选择：local / docker / ssh / singularity / modal / daytona / vercel_sandbox（`terminal.backend/cwd/timeout`）
  - ## 2.3 Docker 后端：一个持久容器复用 terminal/file/execute_code
    - ### 关键区分：宿主机跑 Hermes 容器（`-v ~/.hermes:/opt/data`）vs 容器内的容器（`terminal.backend: docker`）
    - ### `terminal.docker_image` 与容器资源键（`container_cpu`/`container_memory`/`container_disk`/`container_persistent`）
  - ## 2.4 凭据要求速查：web 搜索（EXA/PARALLEL/FIRECRAWL/TAVILY/BRAVE/SEARXNG）、图像（FAL/OpenAI/Codex/xAI/KREA）、SSH（`~/.hermes/.env`）
  - ## 2.5 输出截断与溢出：`tool_output.max_bytes/max_lines/max_line_length`、`tool_budget.mcp_result_size_chars`、spillover 落盘
  - ## 2.6 行为与安全 env：`HERMES_MAX_ITERATIONS`（默认 500）/ `HERMES_SAFE_MODE` / `HERMES_WRITE_SAFE_ROOT` / `HERMES_REDACT_SECRETS`
  - ## 2.7 实操：把 terminal 切到 docker 后端并调容器资源
- **素材**：S1, S2, S5, S11, Sec
- **代码示例**：有 — config.yaml 片段 `terminal.backend: docker` + 容器资源键；`hermes config set` 写法
- **篇幅**：6,000–8,000 字（全册最长章）

---

### 第 3 章：Tool Gateway 接入与权限审批

- **目标**：讲清 Nous Portal Tool Gateway 是什么、一次 OAuth 能聚合哪些云能力、如何接入与校验，并配好审批体系，把「云能力 + 安全审批」一次装好。
- **本章前置**：《上手实战》第 3 章（provider/凭据）；需要一个 Nous Portal 账号。
- **小节**：
  - ## 3.1 Tool Gateway 是什么：一次 OAuth 聚合四类云后端（web 搜索/Firecrawl、图像/FAL、TTS、云浏览器）+ 可选云终端（4+1）
  - ## 3.2 实操：`hermes setup --portal` 完整接入
    - ### OAuth 登录与凭据落盘（`~/.hermes/auth.json`）
    - ### `hermes model` / `hermes tools` 打开网关工具
    - ### 校验：`hermes portal tools` / `hermes portal info`（每行应 "via Nous Portal"）
  - ## 3.3 selection key 机制：`web.backend` / `image_gen.provider` / `tts.provider` / `stt.provider` / `browser.cloud_provider`
    - ### `nous` 与直连 provider 的行为差异（.env 直连 key 被忽略 / 缺 key 报错不静默回退）
    - ### 旧 `use_gateway: true` 已废弃
  - ## 3.4 凭据与令牌生命周期：JWT mint、quarantine、「re-authentication required」、`hermes auth add nous`
  - ## 3.5 自托管网关与远程 OAuth：`TOOL_GATEWAY_DOMAIN/SCHEME/USER_TOKEN`、`FIRECRAWL_GATEWAY_URL`、`ssh -L 8642` 端口转发、device-code
  - ## 3.6 审批体系 approvals：`smart`（默认）/ `manual` / `off`
    - ### CLI 审批流 `[o]nce/[s]ession/[a]lways/[d]eny` 与 `command_allowlist`
    - ### 消息平台批准/拒绝（gateway 自动设 `HERMES_EXEC_ASK=1`）
    - ### 容器后端（docker/singularity/modal/…）跳过危险命令检查
- **素材**：S3, S7, S12, S5, Sec
- **代码示例**：有 — `hermes setup --portal` + `hermes portal tools` / `hermes portal info` 命令序列
- **篇幅**：4,500–6,000 字

---

### 第 4 章：自定义工具开发与注册

- **目标**：先教会「什么时候该做工具而不是 skill」，再给出可照抄的最小注册模板，覆盖 `registry.register` 五参数与 `toolsets.py` 暴露这一关键一步。
- **本章前置**：《上手实战》第 5 章《技能体系》（skill 生命周期/SKILL.md）；有 Python 基础。
- **小节**：
  - ## 4.1 先决策：skill 还是 tool？（贡献指南优先级）
    - ### 选 skill：指令 + shell + 现有工具可表达（arXiv/git/Docker/PDF/email CLI）
    - ### 选 tool：需端到端 auth / 逻辑须精确执行 / 处理二进制与流式（Browserbase、TTS、视觉分析）
  - ## 4.2 注册五要素：`registry.register(name, toolset, schema, handler, check_fn)`
  - ## 4.3 handler 与 schema：返回 JSON 字符串、OpenAI function 格式、check_fn 依赖可用性
  - ## 4.4 自动发现机制：`discover_builtin_tools()` 与 `tools/*.py`（顶层 `register()`）
  - ## 4.5 关键一步：把 toolset 加入 `toolsets.py`，否则「注册但不暴露」
  - ## 4.6 实操：从零注册一个自定义工具
    - ### 代码：`tools/my_tool.py` 最小模板（整体照抄，源自 S6 344-386 行）
    - ### 测试：`tests/skills/test_<skill>_skill.py`（stdlib+pytest+mock，无网络）
    - ### shell 映射：grep→`search_files`、cat/head/tail→`read_file`、sed/awk→`patch`、curl→`web_extract`
  - ## 4.7 插件路径：`ctx.register_tool` / `ctx.register_cli_command`（不改核心）
- **素材**：S6
- **代码示例**：有 — `tools/my_tool.py` 最小注册模板 + `registry.register` 五参数调用
- **篇幅**：4,000–5,500 字

---

### 第 5 章：MCP 接入与排错

- **目标**：讲清 MCP 的唯一配置入口 `mcp_servers`，演示接一个真实服务器（stdio 示例），给出过滤、信任模型与命名规范，并附「工具不显示」的排查序列。
- **本章前置**：第 1 章（config 入口）；《上手实战》第 5 章（skill 概念，便于理解 MCP 与工具的关系）。
- **小节**：
  - ## 5.1 MCP 是什么：把外部能力接入普通工具注册表，贡献 ≥1 工具生成 runtime toolset `mcp-<server>`
  - ## 5.2 配置入口：`mcp_servers`（stdio 与 HTTP 共存于一 config）
    - ### 键：`enabled` / `timeout` / `connect_timeout` / `transport` / `protocol` / `tools`
    - ### `enabled: false` 完全跳过（不连接、不发现、不注册）
  - ## 5.3 实操：接入一个 MCP 服务器（github 示例）
    - ### config.yaml 完整片段（stdio: `command: npx` + `args` + `trust: untrusted`）
    - ### 目录 CLI：`hermes mcp catalog` / `install <name>` / `configure` / `login`
    - ### `/reload-mcp` 与动态刷新（`tools/list_changed`）
  - ## 5.4 工具过滤：`tools.include` / `tools.exclude`（fnmatch，include 优先）、`tools.resources` / `tools.prompts` 关闭、全过滤不建空 toolset
  - ## 5.5 工具命名与信任模型：`mcp__<server>__<tool>`（双下划线，对齐 Claude Code/Codex）与版本差异标注、`trust` / `readOnlyHint`、未识别值 fail-closed 按 untrusted
  - ## 5.6 高级：变量替换（`${VAR}` / `${env:VAR}` / `${userHome}`）、stdio env 隔离、`supports_parallel_tool_calls`、idle/lifetime 回收、OAuth（`mcp-tokens/<server>.json`）、`auxiliary.mcp` 辅助调度 slot
  - ## 5.7 实操：MCP 工具不显示的排查序列（5 步：enabled → 过滤 → `tools/list` RPC → 能力关闭 → `/reload-mcp`）
- **素材**：S4, S10, S2, S9, S11
- **代码示例**：有 — `mcp_servers` 配置片段（stdio github 示例）+ 排查命令
- **篇幅**：5,000–6,500 字

---

### 第 6 章：Skills 与工具关系 · 安全基线

- **目标**：收束 tool/skill/memory 三者关系，讲清全局禁用与安全基线（YOLO / hardline / SAFE_MODE），给出一份 Docker 场景的安全检查清单。
- **本章前置**：第 3 章（approvals 审批体系）；《上手实战》第 5 章《技能体系》。
- **小节**：
  - ## 6.1 关系收束：tool = 可执行能力 / skill = 程序性知识文档 / memory = facts（交叉引用 [[Hermes Agent 上手实战/05-技能体系|第 5 章]]，不重复正文）
  - ## 6.2 skill 门禁：`skills.write_approval`（stage 到 pending/skills）与 `skills.guard_agent_created`
  - ## 6.3 全局禁用：`agent.disabled_toolsets`（平台配置后仍生效）
  - ## 6.4 安全基线：approvals.off / YOLO 三入口（`--yolo`、`/yolo`、`HERMES_YOLO_MODE=1`）/ hardline blocklist（永不可覆盖，先于 yolo）
  - ## 6.5 防泄漏与沙箱：`HERMES_SAFE_MODE` / `HERMES_WRITE_SAFE_ROOT` / `HERMES_REDACT_SECRETS` / execute_code 沙箱剥离 API keys
  - ## 6.6 实操：Docker 场景安全检查清单（密钥只落 `~/.hermes`、容器即边界、权限最小化）
- **素材**：S6, S9, S11, Sec, S5
- **代码示例**：有 — config.yaml `agent.disabled_toolsets` 片段与安全 env 设置
- **篇幅**：3,000–4,500 字

---

## 总览

- **预计总字数**：约 26,000–35,000 字（六章合计）
- **预计章节数**：6 章
- **单章规模**：第 2 章最长（6,000–8,000 字），其余 3,000–6,500 字，分布均衡
- **拆分建议**：
  - 本册内容远超单文件 30KB 阈值（UTF-8 中文约 3 字节/字，全文预计 75–100KB），但参照《上手实战》分册形态（`AI学习/Hermes Agent/Hermes Agent 上手实战/` 文件夹 + 逐章文件），**本册保持单分册 + 6 个章节文件**即可，无需再拆成两个分册。
  - 写作时控制单章 ≤10,000 字（约 ≤30KB）；若第 2 章成稿超限，将「2.4 凭据要求速查」拆为附录速查表、或把「2.5 输出截断」并入第 1 章 1.3。
  - 所有 MCP 配置示例、注册模板代码块可整块抄自 02_deep_research.md，不需另建代码库。

---

## 学习路径说明

### 前置要求
- 已按《上手实战》第 2 章用 Docker 跑通 Hermes，理解 `-v ~/.hermes:/opt/data` 挂载
- 已读《上手实战》第 3 章（config.yaml + .env 基础）与第 5 章《技能体系》
- 第 4 章需要基础 Python 读写能力；其余章节只需会编辑 YAML 与跑 CLI

### 学完能做什么
- 能熟练启用/禁用 toolset，并按 Docker 场景配好 terminal 后端与容器资源
- 能接入 Nous Portal Tool Gateway 并配置审批模式，知道凭据生命周期与自托管网关
- 能判断「该写 skill 还是 tool」，并从零注册一个自定义工具且正确暴露
- 能接入、过滤、信任配置任意 MCP 服务器，并按序列排查「工具不显示」
- 能按安全基线收紧全局禁用项与泄漏防护，交付一份可复查的 Docker 配置

### 建议学习顺序
1. 第 1 章 → 第 2 章（建立入口与内置工具认知，2 小时）
2. 第 3 章（网关 + 权限，1.5 小时）
3. 第 5 章（MCP，1.5 小时；与第 4 章顺序可互换）
4. 第 4 章（自定义工具，需动手编码，2 小时）
5. 第 6 章（关系收束 + 安全基线复查，1 小时）
- 总计约 8 小时；每章末尾的「实操」小节务必照做，代码块可直接复制
