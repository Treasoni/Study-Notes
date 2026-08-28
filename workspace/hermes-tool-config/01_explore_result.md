# hermes 的 tool 如何配置 — P1 探测结果

> run_id: `hermes-tool-config` ｜ 阶段：P1 探测式收集 ｜ 日期：2026-08-28
> 主题：Hermes Agent（Nous Research）工具/技能配置，上手实战，Docker 场景，版本锚定 **v0.20.x**（v0.20.0 "The Herald Release" 2026-08-03，最新补丁 v0.20.6 / 2026-08-27）

## 1. 信源汇总（已按 canonical URL 去重）

3 个透镜并行探测（入门/最佳实践/常见问题），原始候选 15 条 → 去重后 **12 条唯一源，全部为官方/一手**。信源层级：官方 11，一手 1。

| # | 标题 | URL | 层级 | 一句话相关性 | 日期 | 评分 |
|---|------|-----|------|--------------|------|------|
| S1 | Hermes Agent Tools 文档 | hermes-agent.nousresearch.com/docs/user-guide/features/tools | 官方 | 内置工具与 toolset 总览；`hermes tools` / `--toolsets` / `hermes config set` 启停；terminal 支持 local/docker/ssh/singularity 后端，Docker 单常驻容器共享 | 2026-08 | 5 |
| S2 | Tools Reference（内置工具参考） | hermes-agent.nousresearch.com/docs/reference/tools-reference | 官方 | 按 toolset 分组的全部内置工具与调用参数，作"内置工具体系"清单核对 | 2026-08 | 4 |
| S3 | Nous Tool Gateway 文档 | hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway | 官方 | 单一登录聚合 Firecrawl 搜索/FAL 图像/TTS/Browser Use 五类网关工具；`hermes setup --portal` 自动开启；per-tool `use_gateway` 开关，替代旧 `HERMES_ENABLE_NOUS_MANAGED_TOOLS` | 2026-08 | 5 |
| S4 | MCP (Model Context Protocol) 文档 | hermes-agent.nousresearch.com/docs/user-guide/features/mcp | 官方 | config.yaml `mcp_servers` 配 http/stdio 传输，启动自动发现注册外部工具；`hermes mcp add/remove/list`、`hermes tools list` 管理 | 2026-08 | 5 |
| S5 | Environment Variables 参考 | hermes-agent.nousresearch.com/docs/reference/environment-variables | 官方 | 工具凭据（Firecrawl/Tavily/Exa/FAL/Browserbase）、`TOOL_GATEWAY_*`、terminal 后端（Docker/SSH/Modal）环境变量 | 2026-08 | 4 |
| S6 | CONTRIBUTING.md（v2026.7.20） | github.com/NousResearch/hermes-agent/blob/v2026.7.20/CONTRIBUTING.md | 一手 | 自定义工具开发注册：`tools/*.py` 内 `registry.register(name, toolset, schema, handler, check_fn)` 自注册，须同步 toolsets.py 列表；明确"多数能力应做成 skill 而非 tool" | 2026-07 | 5 |
| S7 | Nous Portal 集成文档 | hermes-agent.nousresearch.com/docs/integrations/nous-portal | 官方 | 订阅制 Tool Gateway：一次 OAuth 覆盖搜索/图像/TTS/浏览器，无需各厂商 key；`hermes portal tools` 校验 | 2026-08 | 4 |
| S8 | v0.20.0 "The Herald" Release Notes | github.com/NousResearch/hermes-agent/releases/tag/v2026.8.3 | 官方 | 版本锚定：tool-call 迭代上限 **90→500**；工具自愈增强（terminal 长输出落盘、patch 诊断、write_file 校验、read_file 上限 2000 行）；MCP Lazy Server Startup | 2026-08-03 | 5 |
| S9 | 官方 FAQ | github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/faq.md | 官方 | 工具排错主入口：MCP 工具不显示（`/reload-mcp`、tools 过滤、`tools/list`）、连接失败/超时、权限拒绝（sudo/`.zshrc`/危险命令审批）、`hermes doctor` 与 errors.log 分层排查 | 2026-08 | 5 |
| S10 | MCP 配置参考（mcp-config-reference） | github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md | 官方 | 完整 YAML 键：`enabled`/timeout/`tools.include|exclude`/resources/prompts、`trust` 权限模型（untrusted 对写工具逐次审批）、SSL/mTLS 与连接错误处理 | 2026-08 | 5 |
| S11 | 配置指南 configuration.md | github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md | 官方 | 工具配置核心：`hermes tools` 写 `platform_toolsets`、`agent.disabled_toolsets` 全局禁启用、`terminal.backend` docker `docker_*` 键、`tool_output`/`tool_budget` 输出限制、`skill_manage` 审批与 Skills↔Tools 关系 | 2026-08 | 5 |
| S12 | Run Hermes Agent with Nous Portal | hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal | 官方 | 上手路径：`hermes setup --portal` 一次 OAuth 同时配模型与四类网关工具，避免手改 YAML 出错 | 2026-08 | 4 |

补充参考（不计入去重计数）：MCP 上手指南 `docs/guides/use-mcp-with-hermes`（官方，4）；Security 页（approvals.mode: manual/smart/off，官方）；Skills System 页（clarify tool=可执行能力、skill=程序性知识文档，第 5 章已覆盖）。

## 2. 方向菜单（对应意图文件 4 个探索方向）

| 方向 | 覆盖内容 | 直接支撑信源 | 候选源数 | 评分 |
|------|----------|--------------|----------|------|
| **A. 内置工具体系与启用/禁用** | 内置工具清单、toolsets、`hermes tools`/`--toolsets`/`hermes config set`、config.yaml 启用禁用、terminal 后端（local/docker/ssh） | S1, S2, S5, S11 | 4 | 高 |
| **B. Tool Gateway 与工具权限** | 网关五类后端、`hermes setup --portal`、`use_gateway` 开关、approvals 权限（manual/smart/off）、危险命令审批 | S3, S7, S12（+Security 页） | 3+1 | 高 |
| **C. 自定义工具开发与注册** | `registry.register` 契约、toolsets.py 暴露、工具 vs 技能取舍、实例 | S6 | 1 | 中（单源，需补） |
| **D. Skills 与工具关系、MCP 接入** | mcp_servers 配置、http/stdio、tools 白黑名单、trust 模型、MCP 排错、skill 引用的工具约束 | S4, S9, S10（+use-mcp 指南） | 3+1 | 高 |

## 3. 覆盖缺口

1. **方向 C 单源**：自定义工具开发只有 CONTRIBUTING.md 一个一手源，缺实际代码走查与报错排查（toolsets.py 未登记、schema 不符、handler 抛错）。
2. **权限模型分散**：approvals（manual/smart/off）在 Security 页，未与 S11 的 `skill_manage`/`disabled_toolsets` 归并成一个整体视图。
3. **"工具已启用但未被调用"**：FAQ/config.md 有依据（注册成功 + 会话权限 + 任务确实需要工具三条件），但无集中小结页，P2 需自行归纳。
4. **版本漂移风险**：发布节奏极快（v0.20.0 → v0.20.6 不到一个月），P2 须锁定笔记锚定版本并标注抓取日期。
5. **社区运维经验缺失**：toolnavs.com、segmentfault 中文排错、DEV Community Tool Gateway 参考仅列为 P2 可选的标注经验，不占高信源。

## 4. 预计 P2 深度收集范围

- **核心抓取（5-6 篇）**：S1 Tools、S3 Tool Gateway、S4 MCP、S11 configuration.md、S6 CONTRIBUTING.md、S9 FAQ（+ S12 use-mcp 指南）。
- **缺口补齐**：Security 页（approvals 权限）、自定义工具实例走查（toolsets.py / tools/ 目录示例）、MCP 排错细节（S9/S10 交叉）。
- **产出**：`02_deep_research.md`（scope + 源表 + claim/source 映射 + 矛盾点 + 实战指引 + 开放问题 + 下游 handoff）。
- **P2 结束后用户决策点**：进入大纲模式（逐章写）还是随性模式（直接出笔记）。
