# hermes 的 tool 如何配置 — P2 深度素材

> run_id: `hermes-tool-config` ｜ 阶段：P2 深度收集 ｜ 日期：2026-08-28
> 主题：Hermes Agent（Nous Research）工具/技能配置，上手实战，Docker 场景
> 版本锚定：**v0.20.x**（v0.20.0 "The Herald Release" 2026-08-03；最新补丁 v0.20.6 / 2026-08-27）
> 用户选择：**四个方向全收**（内置工具 / Tool Gateway+权限 / 自定义工具 / MCP+Skills）

---

## 1. Scope

- 12 个唯一信源全部为官方/一手（官方 11 + 一手 1），抓取日期 2026-08-28。
- 只提取与「工具怎么配、怎么接」相关的 claim；密钥/模型/provider 等与工具无关内容一律不进本册。
- 定位：独立成册《Hermes Tool 配置指南》，与《上手实战》第 5 章《技能体系》区分——第 5 章讲 skill 是什么/生命周期，本册讲 tool 怎么配/怎么接。

## 2. 源表（抓取记录）

| S-ID | 标题 | 缓存文件 | 层级 | 抓取 |
|------|------|----------|------|------|
| S1 | Tools 总览 | `sources/08_…tools.md` | 官方 | ✅ |
| S2 | Tools Reference | `sources/04_…tools-reference.md` | 官方 | ✅ |
| S3 | Tool Gateway | `sources/06_…tool-gateway.md` | 官方 | ✅ |
| S4 | MCP 文档 | `sources/03_…mcp.md` | 官方 | ✅ |
| S5 | 环境变量参考 | `sources/05_…environment-variables.md` | 官方 | ✅ |
| S6 | CONTRIBUTING.md | `sources/S06_CONTRIBUTING.md` | 一手 | ✅ |
| S7 | Nous Portal 集成 | `sources/02_…nous-portal.md` | 官方 | ✅ |
| S8 | v0.20.0 Release Notes | `sources/S08_release-v0.20.0-full.txt` | 官方 | ✅ |
| S9 | FAQ | `sources/S09_FAQ.md` | 官方 | ✅ |
| S10 | MCP Config Reference | `sources/S10_mcp-config-reference.md` | 官方 | ✅ |
| S11 | Configuration 指南 | `sources/S11_configuration.md` | 官方 | ✅ |
| S12 | Run with Nous Portal | `sources/01_…run-hermes-with-nous-portal.md` | 官方 | ✅ |
| Sec | Security 页 | `sources/07_…security.md` | 官方 | ✅ |

## 3. Claim / Source 映射（按 4 方向）

### 方向 A：内置工具体系与启用/禁用

| Claim | 来源 |
|-------|------|
| 内置约 86 个工具，可用性随平台、凭据、启用的 toolset 变化 | S2 |
| 工具按逻辑 toolset 分组；常用：web、search、terminal、file、browser、vision、image_gen、skills、tts、todo、memory、session_search、cronjob、code_execution、delegation、clarify、homeassistant、messaging、spotify、discord、discord_admin、debugging、safe | S1 |
| 启用/禁用：`hermes chat --toolsets "web,terminal"`；`hermes tools` 列出/交互配置；`hermes config set` 写 config.yaml | S1, S5 |
| 平台预设 toolset（hermes-cli、hermes-telegram）；MCP 服务器生成动态 toolset `mcp-<server>` | S1, S4 |
| 类别：Web、X Search、Terminal&Files（terminal/process/read_file/patch）、Browser、Media、Agent 编排（todo/clarify/execute_code/delegate_task）、Memory、Automation（cronjob）、Integrations（ha_*/MCP） | S1 |
| x_search 默认关闭，需 xAI 凭据（SuperGrok OAuth 或 XAI_API_KEY），`hermes tools`→🐦 开启 | S1 |
| terminal 后端：local(默认)/docker/ssh/singularity/modal/daytona/vercel_sandbox；config.yaml 键 `terminal.backend/cwd/timeout(秒)` | S1 |
| docker 后端 = 单个持久容器，跨 terminal/file/execute_code 复用；键 `terminal.docker_image`（例 `python:3.11-slim`）；容器资源键 `container_cpu`(默认1)/`container_memory`(5120MB)/`container_disk`(51200MB)/`container_persistent`(true) | S1, S5 |
| ssh 凭据写 `~/.hermes/.env`：`TERMINAL_SSH_HOST/USER/KEY`；ssh 端口默认 22 | S1, S5 |
| web 搜索凭据：`EXA_API_KEY` 或 `PARALLEL_API_KEY` 或 `FIRECRAWL_API_KEY` 或 `TAVILY_API_KEY`；另有 `BRAVE_SEARCH_API_KEY`、`SEARXNG_URL`（免费无需 key） | S2, S5 |
| 图像凭据：`FAL_KEY`/`OPENAI_API_KEY`/Codex OAuth/xAI OAuth/`KREA_API_KEY` | S2 |
| 行为/安全 env：`HERMES_MAX_ITERATIONS`（每次对话最大 tool-call 迭代，默认 **500**）；`HERMES_SAFE_MODE`（关插件/MCP/钩子）；`HERMES_WRITE_SAFE_ROOT`（硬拦越界 write_file/patch）；`HERMES_REDACT_SECRETS` 默认 true | S5 |
| `HERMES_MAX_ITERATIONS` 与 v0.20.0 release 的「tool-call 迭代上限 90→500」一致 | S5, S8 |
| 输出截断三键 `tool_output.max_bytes/max_lines/max_line_length`（默认 50000/2000/2000）；超长 terminal 输出保留前 40% + 后 60% 中间插 `[OUTPUT TRUNCATED]` | S11 |
| 溢出落盘 `tool_budget.mcp_result_size_chars`（MCP 工具默认 50,000 字），全量存 `$HERMES_HOME/cache/spillover/`，上下文放预览+路径 | S11 |
| 全局禁用 `agent.disabled_toolsets: [memory, web]`——在 `platform_toolsets` 之后生效，任何平台都移除 | S11 |
| 配置唯一来源：config.yaml（非机密行为）+ `.env`（密钥）；`config.yaml` 优先于 env | S5, S11 |
| 旧 `LLM_MODEL` 已移除；config.yaml 工具键以 `hermes doctor` 输出为准 | S11（沿用上手实战第 3 章） |

### 方向 B：Tool Gateway 与工具权限

| Claim | 来源 |
|-------|------|
| Tool Gateway = 付费订阅（Nous Portal），一次 OAuth 聚合四类后端：web 搜索/Firecrawl、图像/FAL、TTS、云浏览器/Browser Use（含 browser_vision）；**加云终端/Modal 为可选 add-on 共 5 类** | S3, S7 |
| 图像默认模型 FLUX 2 Klein 9B（`fal-ai/flux-2/klein/9b`），per-call 传模型 ID 给 image_generate 可覆盖 | S3 |
| 启用：`hermes setup --portal` = OAuth + 设 Nous provider + 开网关；`hermes model` 提示全开；`hermes tools` 逐工具选 | S3, S12 |
| Nous-managed 工具（Web/Image/Video/TTS/Browser）即使未登录也恒在 `hermes tools` 列出，选中即内联 Portal 登录 | S3 |
| 每类单一 selection key：`web.backend`/`image_gen.provider`/`tts.provider`/`stt.provider`/`browser.cloud_provider`，选 Nous 存为 `nous` | S3 |
| **runtime 恒用存储选择**：类别设为 `nous` 时 `.env` 直连 key 被忽略；选直连 provider（如 `image_gen.provider: fal`）缺 key 报错、不静默回退 | S3, S7 |
| 旧 `use_gateway: true` 已 **deprecated**：读时等价 `nous`、不再写入；新配置用 `hermes tools` 选 | S3, S7 |
| 凭据：OAuth refresh token 存 `~/.hermes/auth.json`（唯一磁盘凭据），每次调用 mint short-lived JWT；token 失效→quarantine→「re-authentication required」→`hermes auth add nous` 重登 | S7 |
| 自托管网关键：`TOOL_GATEWAY_DOMAIN/SCHEME/USER_TOKEN`、`FIRECRAWL_GATEWAY_URL`（写 `~/.hermes/.env`） | S3 |
| 远程 OAuth：`ssh -L 8642:127.0.0.1:8642` 端口转发，或 device-code `hermes auth add nous --type oauth` | S7 |
| 验证：`hermes portal tools` 显示 per-tool 路由（via Nous Portal 或 partner 名）；`hermes portal info` 每行应显示 "via Nous Portal" | S12 |
| **approvals.mode**：`smart`(默认，辅助 LLM 评估风险)/`manual`(恒提示)/`off`(禁用所有审批 = `--yolo`) | Sec |
| approvals 键：`timeout`=300s、`cron_mode`=deny、`single_query_mode`=deny、`mcp_reload_confirm`/`destructive_slash_confirm`=true | Sec |
| CLI 审批流：`[o]nce/[s]ession/[a]lways/[d]eny`（默认 deny）；always 存 `command_allowlist` 到 config.yaml；超时 fail-closed | Sec |
| 消息平台回复 yes/y/approve/ok 批准、no/n/deny 拒绝；gateway 运行时自动设 `HERMES_EXEC_ASK=1` | Sec |
| hardline blocklist（UNRECOVERABLE_BLOCKLIST）先于 `--yolo`/approvals.off/cron approve/"allow always" 执行，**永不可覆盖**；approvals.deny glob 高于 yolo | Sec |
| 容器后端（docker/singularity/modal/daytona/vercel_sandbox）**跳过危险命令检查**（容器即边界） | Sec |
| YOLO 三入口：`hermes --yolo`、`/yolo`（toggle）、`HERMES_YOLO_MODE=1` | Sec |
| 网关授权顺序：平台 allow-all → DM pairing → 平台 allowlist → `GATEWAY_ALLOWED_USERS` → 全局 allow-all → 默认拒绝 | Sec |

### 方向 C：自定义工具开发与注册

| Claim | 来源 |
|-------|------|
| **决策：多数能力应做成 skill**；新工具 rarely needed（贡献指南优先级第 6） | S6 |
| 选 skill：指令+shell+现有工具可表达；包装外部 CLI/API（经 terminal/web_extract）；无需自定义 Python/API key 管理 | S6 |
| 选 tool：需端到端 API key/auth/多组件配置；逻辑须每次精确执行；处理二进制/流式/实时数据 | S6 |
| 例：tool=浏览器自动化(Browserbase)、TTS、视觉分析；skill=arXiv/git/Docker/PDF/email CLI | S6 |
| 注册签名：`registry.register(name, toolset, schema, handler, check_fn)` 五参数 | S6 |
| handler 签名 `def my_tool(param1: str, param2: int = 10, **kwargs) -> str`，返回 JSON 字符串 | S6 |
| check_fn 返回 bool 表示依赖可用；schema 为 OpenAI function 格式 JSON | S6 |
| 自动发现：`discover_builtin_tools()`（tools/registry.py）导入含顶层 `register()` 的 `tools/*.py`，`model_tools.py` 无手动导入清单 | S6 |
| **工具名必须加入 `toolsets.py`**（如 `_HERMES_CORE_TOOLS`）否则「注册但不暴露」；新 toolset 须接平台 presets | S6 |
| 架构路径：`tools/registry.py` 中心注册表（schemas/handlers/dispatch）；`toolsets.py` 分组/presets；`model_tools.py` 编排 | S6 |
| 插件经 `ctx.register_tool` 注册工具、`ctx.register_cli_command` 注册 CLI，无需改核心 | S6 |
| 安全层：`tools/approval.py` 危险命令正则检测；execute_code 沙箱剥离 API keys | S6 |
| Skill 硬性约束：SKILL.md 引用工具须为原生 Hermes 工具或显式 MCP server（反引号点名）；MCP 在 `## Prerequisites` 写明 setup | S6 |
| shell 映射：grep/rg→`search_files`；cat/head/tail→`read_file`；sed/awk→`patch`；curl→`web_extract` | S6 |
| 测试：`tests/skills/test_<skill>_skill.py` 仅 stdlib+pytest+mock，无网络；`scripts/run_tests.sh` 等同 CI | S6 |
| 最小可用示例见 `S06_CONTRIBUTING.md` 第 344–386 行完整代码块（可整体抄入笔记） | S6 |

### 方向 D：Skills 与工具关系、MCP 接入

| Claim | 来源 |
|-------|------|
| `mcp_servers` 是 MCP 唯一配置入口；stdio（`command`/`args`/`env`）与 HTTP（`url`/`headers`）可共存于一 config | S4, S10 |
| 键：`enabled`、`timeout`(默认 300)、`connect_timeout`(默认 60)、`transport`(sse 默认)、`protocol`(auto/stateless/legacy)、`tools` | S4, S10 |
| `enabled: false` 完全跳过该 server：不连接、不发现、不注册 | S4 |
| 启动时自动发现 MCP server 并注册到普通工具注册表；贡献≥1 工具的 server 生成 runtime toolset `mcp-<server>` | S4 |
| 动态发现：`tools/list_changed` 通知自动刷新工具列表，免手动 `/reload-mcp`；改配置仍可手动 `/reload-mcp` | S4 |
| 过滤：`tools.include` 白名单 / `tools.exclude` 黑名单，支持 fnmatch glob，**include 优先** | S4 |
| utility 过滤：`tools.resources: false` 禁 list_resources/read_resource；`tools.prompts: false` 禁 list_prompts/get_prompt | S4 |
| 全过滤掉时不创建空 runtime MCP toolset（保持工具列表干净） | S4 |
| 目录 CLI：`hermes mcp` 选择器 / `hermes mcp catalog` 列表 / `hermes mcp install <name>` / configure / login；目录存 `optional-mcps/` 默认禁用 | S4 |
| 工具命名：**`mcp__<server>__<tool>`（双下划线）**，对齐 Claude Code/Codex；非字母数字→下划线（my-api→`mcp__my_api__list_items_v2`） | S2, S10 |
| ⚠️ 命名矛盾：S4 文档页写 `mcp_<server>_<tool>`（单下划线，如 `mcp_filesystem_read_file`）——版本差异，写笔记以双下划线为准并标注 | S4 vs S2/S10 |
| 信任模型：`trust: untrusted` 下无 `readOnlyHint: true` 注解的写工具逐次用户审批；readOnlyHint 只是 server 提示；**未识别值 fail-closed 按 untrusted** | S10 |
| 变量替换：`${VAR}` 与 `${env:VAR}` 等价，未设置保留字面量；context 变量 `${userHome}/${workspaceFolder}` 等 | S10 |
| stdio 只传显式 env + 安全基线，不传完整 shell 环境（防密钥泄漏） | S4 |
| 并行调用：默认串行；`supports_parallel_tool_calls: true` 才并发（共享状态工具勿开） | S4 |
| stdio 回收：`idle_timeout_seconds`/`max_lifetime_seconds` 透明重启重 stdio server（playwright 例 900/86400） | S4 |
| OAuth：`auth: oauth`；token 存 `~/.hermes/mcp-tokens/<server>.json` 0o600；`hermes mcp login <server>` | S4 |
| presets：`hermes mcp add codex --preset codex` 写 `command:"codex" args:["mcp-server"]` | S4 |
| MCP 排错：工具不显示先验 server 是否响应 `tools/list` RPC，再查 `tools.*`/`enabled` 并 `/reload-mcp`；server 崩溃→报超时 | S9 |
| Skills 存程序性步骤 procedures、Memory 存 facts，均可跨会话；tool=可执行能力、skill=程序性知识文档（clarify 用） | S9, S6 |
| `skills.write_approval: true` 门禁所有 agent 的 skill_manage 写（增删改），stage 到 pending/skills；`/skills approve/reject`，`/skills approval on|off` | S11 |
| `skills.guard_agent_created: true` 扫描 agent 创建内容（默认 false），命中弹审批 | S11 |
| `agent.disabled_toolsets` 全局移除（如 memory/web），platform 配置后仍移除 | S11 |
| `auxiliary.mcp` 是 MCP 工具调度的辅助模型 slot（provider/model/timeout 30）；另有 skills_hub slot | S11 |

## 4. 矛盾与版本差异

| 项 | 冲突 | 判定/处理 |
|----|------|-----------|
| MCP 工具命名 | S4 单下划线 `mcp_<server>_<tool>` vs S2/S10 双下划线 `mcp__<server>__<tool>` | main 分支文档（S10/S2）双下划线对齐 Claude Code/Codex，更可信；S4 页滞后。笔记用双下划线，标注「随版本核实」 |
| 网关后端数 | S3 说 4 类 vs S7 说 5 类 | S7 含可选 add-on 云终端/Modal（`hermes setup terminal`），实为 4+1，不算矛盾 |
| tool_output 等键归属 | A 方向源（S1/S2/S5）grep 无 `tool_output`/`tool_budget`/`platform_toolsets`/`disabled_toolsets` | 实则在 S11 configuration.md（761-816 行）——跨页取数问题，非真矛盾 |
| 旧 env var | `HERMES_ENABLE_NOUS_MANAGED_TOOLS` 全库 0 命中；ch3 旧表述提到它 | 官方现文档只认 selection key + legacy `use_gateway`；该 env var 疑已废弃，ch3 表述需后续核对修正 |
| tool-call 上限 | release 说 90→500；env 文档 `HERMES_MAX_ITERATIONS` 默认 500 | 一致，无矛盾 |
| "MCP Lazy Server Startup" | P1 期提及，P2 四源未现此术语 | 最接近行为=「启动自动发现 + idle/lifetime 透明重启」；笔记不写该术语 |

## 5. 实战指引（可直接用于写章的操作步骤）

**快速启用/禁用工具集**
```bash
hermes tools                                   # 交互式列出/开关各 toolset（按平台）
hermes chat --toolsets "web,terminal,file"     # 临时启用
hermes config set terminal.backend docker      # 写 config.yaml
```
全局关：config.yaml `agent.disabled_toolsets: [memory, web]`；输出截断调 `tool_output.max_bytes`；迭代上限 `HERMES_MAX_ITERATIONS`（默认 500）。

**接 Tool Gateway（Nous Portal）**
```bash
hermes setup --portal        # OAuth → 设 Nous provider → 开网关
hermes portal tools          # 校验 per-tool 路由
hermes portal info           # 每行应 "via Nous Portal"
```
选 Nous 时 `.env` 直连 key 被忽略；直连 provider（如 fal）缺 key 会报错不静默回退；新配置在 `hermes tools` 里选，不再写 `use_gateway`。

**接 MCP 服务器**
```yaml
# ~/.hermes/config.yaml
mcp_servers:
  github:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    enabled: true
    tools:
      include: ["*"]
    trust: untrusted      # 写工具逐次审批（无 readOnlyHint）
```
管理：`hermes mcp catalog` / `hermes mcp install <name>` / `hermes mcp login <server>`；改完 `/reload-mcp`。

**MCP 工具不显示排查（按序）**
1. `enabled: false`？→ 跳过整个 server
2. `tools.include/exclude` 过滤？→ include 优先
3. server 是否响应 `tools/list` RPC？→ 崩了会报超时
4. 能力缺失（resources/prompts 被关）？
5. `/reload-mcp` 或重启会话

**自定义工具最小模板（照抄 S06 344-386 行）**
```python
# tools/my_tool.py
from tools.registry import registry
def my_tool(param1: str, param2: int = 10, **kwargs) -> str:
    return '{"ok": true}'          # 返回 JSON 字符串
def check_fn() -> bool:
    return True                    # 依赖可用性
registry.register(
    name="my_tool",
    toolset="my_tools",            # 须同步加入 toolsets.py，否则注册不暴露
    schema={"type": "function", "name": "my_tool", "parameters": {...}},
    handler=my_tool,
    check_fn=check_fn,
)
```
先问：这事能用 skill 做吗？（多数能力应做成 skill，工具 rarely needed）

## 6. 开放问题（写章/验证时处理）

1. **MCP 工具命名**：双下划线 vs 单下划线版本差异——写笔记用双下划线，标注随版本核实。
2. **`HERMES_ENABLE_NOUS_MANAGED_TOOLS`**：官方现文档 0 命中，ch3 旧表述待修。
3. **`hermes mcp remove/list`**：源中只有 install/catalog/configure/login/add/serve，命令全集待 `hermes mcp --help` 实证。
4. **Docker 场景交叉验证**：本册面向 Docker 用户（`-v ~/.hermes:/opt/data`）；`terminal.backend: docker` 是"容器内的容器"，需与"宿主机跑 Hermes 容器"两个概念区分清楚。
5. **tool-call 迭代上限**：确认 `HERMES_MAX_ITERATIONS` 是否可配与最佳值建议。

## 7. 下游 Handoff（给 P3 大纲 / P4 写作）

- **建议分册结构**（>30KB/多章 → 拆分，参照上手实战分册）：
  1. 工具体系总览与配置入口（config.yaml + .env + `hermes tools`/`--toolsets`）
  2. 内置工具与 toolsets 全解（含 terminal 后端/凭据要求）
  3. Tool Gateway 接入与权限（Nous Portal、selection key、approvals）
  4. 自定义工具开发与注册（skill-vs-tool、registry.register、toolsets.py）
  5. MCP 接入与排错（mcp_servers、trust、过滤、常见坑）
  6. Skills 与工具关系 / 安全基线（disabled_toolsets、YOLO、hardline）
- **素材 key**：S1-S12 + Sec，统一用上表 S-ID 引用；矛盾项见 §4。
- **版本标注**：全文锚定 v0.20.x（v0.20.6），代码块加「以 `hermes doctor` 输出为准」。
- **排错章节**：素材集中在 S9（FAQ）+ S4（MCP 排查）+ Sec（权限）→ 建议独立「常见坑」章或并入对应章节。
- **补充验证**：P4 前如需，跑一次 `hermes mcp --help`/`hermes tools --help` 确认命令全集（本机无 Hermes，可依赖文档）。
