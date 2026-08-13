# 配置和使用 opencode - 探测式收集结果

收集时间: 2026-08-13
阶段: P1 探测式收集
主线: Claude Code → opencode 迁移

## 探测维度

| # | 维度 | 核心问题 |
|---|------|---------|
| 1 | 定位与对比 | opencode 是什么？与 Claude Code 整体对比 |
| 2 | 安装配置与命令 | 如何安装、配置，常用命令与工作流 |
| 3 | 高级定制与排错 | provider/权限/MCP/Skills 与 Claude Code 差异、常见坑 |

---

## 维度 1：opencode 定位与 Claude Code 对比

### 1. opencode 官网
- **URL**: https://opencode.ai
- **摘要**: 开源 AI 编码 Agent，可运行于终端、IDE 与桌面。核心概念：多 Agent 并行会话、隐私优先（不存储代码/上下文）、自带免费模型或 BYOM 连接外部 provider、LSP 自动加载。支持 Claude/GPT/Gemini/Copilot 及本地模型。形态：CLI（TUI）+ 桌面应用 + IDE 扩展。
- **评分**: 5/5
- **关键数据**: 195K+ GitHub stars；16M 月活开发者；75+ LLM providers

### 2. GitHub 官方仓库（anomalyco/opencode）
- **URL**: https://github.com/anomalyco/opencode
- **摘要**: MIT 开源的终端 AI coding agent。内置 build（默认，全权限）/plan（只读分析）双主 Agent，Tab 切换，另有 general 子代理。客户端/服务器架构，TUI 只是客户端之一，可远程驱动；自带 LSP、web fetch、vision。五种扩展点：自定义命令、Skills、插件、自定义 Agent、MCP 服务器。
- **评分**: 5/5
- **关键数据**: MIT 协议；5 类扩展点；build/plan 双 Agent 模式

### 3. OpenCode vs Claude Code（Builder.io 同模型实测）
- **URL**: https://www.builder.io/blog/opencode-vs-claude-code
- **摘要**: 同一 Claude Sonnet 4.5 跑 4 个任务：Claude Code 用时 9m9s，OpenCode 16m20s（约慢 45%）；但 OpenCode 写出 94 个测试（CC 73 个），全量跑测试套件验证无回归。Claude Code 偏速度与开箱即用，OpenCode 偏可检查性与正确性。
- **评分**: 5/5
- **关键数据**: CC 9m9s vs OC 16m20s；94 vs 73 个测试

### 4. OpenCode：Open-Source Claude Code Alternative（DeepInfra）
- **URL**: https://deepinfra.com/blog/claude-code-alternative
- **摘要**: 定位为 Claude Code 的开源替代：模型无关（75+ provider，含 Ollama 本地/离线）、无厂商锁定、LSP 原生支持、客户端/服务器架构可远程驱动。短板：默认权限更宽（靠 opencode.json glob 配置 + Git 快照/undo 兜底，而非逐次授权）、无官方支持/SLA。
- **评分**: 4/5
- **关键数据**: 75+ providers；100% 开源（MIT）；默认权限更宽

### 5. OpenCode：终端里的 AI 编程革命（腾讯云开发者社区）
- **URL**: https://cloud.tencent.cn/developer/article/2646782
- **摘要**: 中文科普：OpenCode = 终端界面 × 任意 AI 模型 × 本地代码感知。SST 团队创建、Anomaly 维护，Go + Bubble Tea 构建 TUI。三种用法：`opencode`（TUI）、`opencode run`（无头/CI）、`opencode serve`（API/Web/远程）。
- **评分**: 4/5
- **关键数据**: Go + Bubble Tea；三种使用模式；支持本地模型离线

---

## 维度 2：安装、初始化配置与常用命令

### 1. GitHub README（安装与快速开始）
- **URL**: https://github.com/anomalyco/opencode
- **摘要**: 多平台安装：一键脚本 `curl -fsSL https://opencode.ai/install | bash`、`npm i -g opencode-ai@latest`、`brew install anomalyco/tap/opencode`、Arch/Nix/Scoop/Choco。安装路径优先级 `$OPENCODE_INSTALL_DIR` → `$XDG_BIN_DIR` → `$HOME/bin` → `$HOME/.opencode/bin`。需先移除 0.1.x 旧版本，安装后 `opencode -v` 验证。
- **评分**: 5/5

### 2. CLI 官方文档
- **URL**: https://opencode.ai/docs/cli
- **摘要**: `opencode` 无参进入 TUI；`run` 非交互工作流（`--format json`、`-m` 选模型、`-f` 附加文件、`--auto` CI 自动批准）；`auth login/list`、`agent create`、`mcp add`、`models`、`session list`、`stats`、`serve`/`web` 无头服务器。TUI 内置 `/init`、`/models`、`/connect`、`/compact` 等 slash 命令。
- **评分**: 5/5
- **关键数据**: 凭据存 `~/.local/share/opencode/auth.json`；模型列表来自 Models.dev

### 3. Configuration 官方文档（opencode.json）
- **URL**: https://opencode.ai/docs/config
- **摘要**: JSON/JSONC 格式，`$schema` 指向 opencode.ai/config.json。配置按 8 层优先级深度合并（远程组织默认 → 全局 → `OPENCODE_CONFIG` → 项目级 → `.opencode` 目录）。覆盖 `model`/`small_model`、`provider`（baseURL、自定义 npm 供应商）、`agent`、`command`、`permission`（ask/allow/deny）、`mcp`、`plugin`、`instructions`。支持 `{env:VAR}` 与 `{file:path}` 变量替换。
- **评分**: 5/5
- **关键数据**: 全局配置 `~/.config/opencode/opencode.json`；未知顶层键抛 `ConfigInvalidError`

### 4. Ollama 集成文档（本地模型配置）
- **URL**: https://github.com/ollama/ollama/blob/cecd265d/docs/integrations/opencode.mdx
- **摘要**: 通过 `provider.ollama` 用 `npm: "@ai-sdk/openai-compatible"` + `options.baseURL: http://localhost:11434/v1` 接入本地模型。
- **评分**: 3/5

### 5. opencode-primer 社区参考手册
- **URL**: https://github.com/wesammustafa/opencode-primer
- **摘要**: 社区整理 CLI 全局 flag（`--log-level`、`--debug`、`--pure`）、`run` 非交互用法、TUI slash 命令与快捷键（`ctrl+x` 前缀、Tab 切 agent）。模型以 `provider/model` 形式指定。
- **评分**: 3/5

---

## 维度 3：高级定制、迁移差异与常见坑

### 1. 自定义 Provider 配置指南
- **URL**: https://docs.venice.ai/guides/integrations/opencode
- **摘要**: `opencode.json` 的 `provider` 键下用 `@ai-sdk/openai-compatible` 包，配 `baseURL`、`options.apiKey`（支持 `{env:VAR}`）和 `models` 映射。模型引用格式 `provider/model-id`，也可用 `/connect` 把密钥存入 `auth.json`。
- **评分**: 5/5

### 2. Permissions 权限系统（官方文档）
- **URL**: https://opencode.ai/docs/permissions
- **摘要**: 权限三值 allow/ask/deny；`permission` 键支持顶层字符串、per-tool 或 glob 对象语法，最后匹配者胜出，`*`/`?` 通配。v1.1.1 起旧 `tools` 布尔配置废弃并入 `permission`。默认宽松，但 `.env` 文件默认 deny，`doom_loop`（同调用 3 次）与 `external_directory` 默认 ask。
- **评分**: 5/5
- **关键数据**: 15 个权限键；`.env` 默认拒绝；plan 代理默认 edit/bash 为 ask

### 3. MCP 集成（官方文档）
- **URL**: https://opencode.ai/docs/mcp
- **摘要**: `mcp` 键下配 `type: local`（command/cwd/environment/timeout 默认 5000ms）或 `type: remote`（url/headers/oauth）。remote 自动处理 OAuth（RFC 7591），token 存 `~/.local/share/opencode/mcp-auth.json`。CLI：`opencode mcp list/auth/logout/debug`。
- **评分**: 5/5

### 4. {env:VAR} 替换破坏认证回退（GitHub Issue）
- **URL**: https://github.com/anomalyco/opencode/issues/34388
- **摘要**: `options.apiKey` 用 `{env:VAR}` 但变量未设置时被替换为空字符串 `""`，阻断 auth.json 回退，报 401。修复方向是空值改为 falsy 判断。同类：#19946、#27853。
- **评分**: 5/5

### 5. opencode vs Claude Code Skills/AGENTS 机制对比
- **URL**: https://github.com/kenoxa/spine
- **摘要**: 一套 skills/agents/guardrails 跨 Claude Code、OpenCode、Cursor、Codex 复用。关键差异：OpenCode 上下文文件为 `AGENTS.md`（Claude Code 用 `CLAUDE.md`）；skills 用标准 SKILL.md，按 `.opencode/skills/ → .claude/skills/ → .agents/skills/` 发现；OpenCode 无原生插件市场，靠 AGENTS.md + 内置 skill 工具 + commands 达 parity；TUI 无 `/skill` 斜杠命令。
- **评分**: 4/5

---

## 综合分析

### 关键共识
1. **opencode 定位**：MIT 开源、终端优先、provider-agnostic 的 AI coding agent；客户端/服务器架构 + LSP + 双 Agent 模式（build/plan）。
2. **与 Claude Code 核心差异**：开源与模型自由（75+ provider）、可扩展性（5 类扩展点）与可检查性（偏好写测试验证）；Claude Code 胜在速度、开箱即用、安全默认值与官方支持。
3. **配置体系**：单一 `opencode.json`（8 层优先级合并），对应 Claude Code 的 settings.json + CLAUDE.md；上下文文件是 `AGENTS.md`。
4. **权限模型**：三值 allow/ask/deny + glob 规则，默认更宽；Claude Code 默认逐次询问、更安全。
5. **迁移者关键点**：Skills 发现顺序、权限收紧策略、MCP 配置方式、认证方式（auth.json / /connect）与 Claude Code 差异显著。

### 主要分歧
- **速度 vs 正确性**：Claude Code 更快（实测快约 45%），OpenCode 更重测试验证与可检查性。
- **默认安全 vs 灵活**：Claude Code 默认逐次授权更安全；OpenCode 默认权限更宽，靠 Git 快照/undo 兜底。

### 学习方向建议
按「从 Claude Code 迁移」主线，五类内容可组织为：
1. opencode 定位与架构（含与 Claude Code 对比）
2. 安装与初始化配置（opencode.json 体系 ↔ settings.json/CLAUDE.md）
3. 常用命令与日常工作流（TUI/run/slash ↔ Claude Code 命令映射）
4. 高级定制（provider、权限、MCP、Skills、AGENTS ↔ Claude Code 对应机制）
5. 常见坑与排错（认证、token、权限，迁移差异清单）
