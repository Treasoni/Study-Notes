# 配置和使用 opencode - 深度素材

收集时间: 2026-08-13
阶段: P2 深度收集
方向: 全面覆盖（定位对比 → 安装配置 → 命令工作流 → 高级定制 → 排错）
主线: Claude Code → opencode 迁移

---

## 1. 定位与架构

**核心定位**：MIT 开源的 AI 编码代理（"The open source AI coding agent"），来自 SST 团队。可在终端（TUI）、桌面应用、IDE 扩展三种界面使用。**将 agent 框架与模型解耦**——Claude Code 只跑 Claude，opencode 可接入任意模型。

**架构关键点**：
- **客户端/服务器分离**：单后端（server）驱动 TUI、桌面 app、VS Code/Cursor 扩展，通过 HTTP API 支持远程 Docker 会话。
- **TUI**：终端界面，多会话并行（同一项目可同时启动多个 agent）。
- **LSP 集成**：自动加载 LSP，每次编辑后把编译器诊断回喂给模型，下一轮自纠正。
- **Git 快照**：以 git 快照 + `/undo` 作为安全网（而不是权限弹窗）。
- **内置双 Agent**（Tab 切换）：`build`（默认，全权限）/ `plan`（只读分析，默认拒绝文件编辑，bash 需询问）。
- **子代理**：`general` 通用子代理，可通过 `@general` 调用。
- **隐私**：不存储用户代码或上下文数据。

**关键数据**：195K+ GitHub stars；16M+ 月活开发者；75+ LLM providers（via Models.dev）；25.3k forks；950 contributors。

## 2. 与 Claude Code 整体对比

| 维度 | opencode | Claude Code |
|------|----------|-------------|
| 开源/许可 | MIT 开源，可审计/复刻/修改 | 专有闭源 |
| 模型支持 | 75+ providers + Ollama + 任意 OpenAI 兼容端点 | 仅 Claude（官方）；本地模型靠脆弱社区代理 |
| 默认权限 | "行动，用 /undo 回滚"，透明可审计优先 | 默认只读，写文件/跑命令前询问 |
| 配置体系 | 声明式 `opencode.json`，8 层优先级合并 | CLI 命令 + `claude mcp add`，settings.json |
| 上下文文件 | `AGENTS.md`（原生加载） | `CLAUDE.md` |
| 扩展机制 | 5 类扩展点：命令、Skills、插件、自定义 Agent、MCP | 官方插件/扩展，闭环生态 |
| 速度/正确性 | 求彻底（跑全套测试验证），更慢但可检查 | 求速度，更快但可能只验证自己的改动 |
| 官方支持 | 社区/开源（SST/Anomaly），迭代快、偶发 bug | Anthropic 官方，打磨完善 |

**同模型实测**（Claude Sonnet 4.5，4 个任务）：
| 任务 | Claude Code | opencode |
|------|-------------|----------|
| 跨文件重命名 | 3m6s | 3m13s |
| Bug 修复 | 41s | 40s |
| 重构 | 2m10s | 3m16s |
| 写测试 | 73 个，3m12s | 94 个，9m11s |
| **总计** | **9m9s** | **16m20s** |

结论："Claude Code 为速度而生，opencode 为彻底而生"。opencode 会跑 `pnpm install` + 全部存量测试，Claude Code 只验证自己的改动。

**成本注意**：每 token 单价 ≠ 总成本；opencode 支持**逐步路由**控成本（规划/批量编辑/分诊用不同模型）。

## 3. 安装方式

**一键脚本**（路径优先级：`$OPENCODE_INSTALL_DIR` → `$XDG_BIN_DIR` → `$HOME/bin` → `$HOME/.opencode/bin`）：
```bash
curl -fsSL https://opencode.ai/install | bash
OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash
```

**各平台包管理器**：
| 平台 | 命令 |
|------|------|
| npm（含 bun/pnpm/yarn） | `npm i -g opencode-ai@latest` |
| macOS/Linux（推荐 tap） | `brew install anomalyco/tap/opencode` |
| macOS/Linux（官方 formula） | `brew install opencode` |
| Windows | `scoop install opencode` / `choco install opencode` |
| Arch（stable / AUR） | `sudo pacman -S opencode` / `paru -S opencode-bin` |
| Nix | `nix run nixpkgs#opencode` |

**升级/卸载**：`opencode upgrade [target]`（`--method curl|npm|pnpm|bun|brew`）；`opencode uninstall`（`--keep-config -c`、`--keep-data -d`、`--dry-run`、`--force`）。
**注意**：安装前移除 0.1.x 之前的旧版本；桌面版是 BETA。

## 4. 配置体系（opencode.json）

**格式**：JSON / JSONC（带注释）。`$schema: https://opencode.ai/config.json`（运行时）、`https://opencode.ai/tui.json`（TUI）。

**8 层优先级（从高到低）**：
1. macOS 托管偏好（MDM `ai.opencode.managed`）
2. 托管配置文件（macOS `/Library/Application Support/opencode/`、Linux `/etc/opencode/`、Windows `%ProgramData%\opencode`）
3. 内联配置 `OPENCODE_CONFIG_CONTENT` 环境变量
4. `.opencode` 目录（agents、commands、plugins…）
5. 项目配置：项目根 `opencode.json`（从当前目录向上找最近 Git 目录）
6. 自定义配置 `OPENCODE_CONFIG=/path/to/config.json`
7. 全局配置 `~/.config/opencode/opencode.json`
8. 远程配置 `.well-known/opencode`（组织默认）

配置是**合并**而非替换；项目覆盖全局，全局覆盖远程，托管设置覆盖一切。

**主要配置键**：
- `model` / `small_model`（主模型 / 轻量任务模型）、`default_agent`（无效时回退 build）、`subagent_depth`（默认 1）
- `provider`：`options` 支持 `apiKey`（env / `{file:...}` / `/connect`）、`timeout`（默认 300000ms）、`chunkTimeout`；`disabled_providers`（优先）/ `enabled_providers`
- `agent`：`description`、`model`、`prompt`、`tools`；也可用 markdown 文件定义
- `command`：`template`、`description`、`agent`、`model`
- `permission`：默认全部允许；`{ "edit": "ask", "bash": "ask" }`
- `tools`：`{ "write": false }` 禁用工具
- `mcp`：MCP server 配置
- `plugin`：npm 插件数组
- `instructions`：指令文件路径/glob 数组
- 其它：`server`、`shell`、`snapshot`、`autoupdate`、`share`、`formatter`、`lsp`、`compaction`、`experimental`

**变量替换**：
- `{env:VARIABLE_NAME}` → 环境变量（未设置则为空字符串）
- `{file:path}` → 文件内容（相对路径以配置文件目录为基准，支持 `/` 和 `~`）

**基础配置示例**：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "provider": {
    "anthropic": {
      "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" }
    }
  },
  "permission": { "edit": "ask", "bash": "ask" }
}
```

## 5. 认证方式

- `opencode auth login`（`--provider/-p`、`--method/-m`）；`auth list/ls`、`auth logout`
- 凭据存储：`~/.local/share/opencode/auth.json`
- 启动时加载：auth.json 凭据 + 环境变量 key + 项目 `.env` 文件 key
- `/connect`：TUI 内交互式配置凭据入口
- 服务端认证：`OPENCODE_SERVER_PASSWORD`（basic auth，用户名默认 `opencode`）
- 模型列表：`opencode models [provider]`（输出 `provider/model` 格式，`--refresh` 刷新缓存）
- **注意**：Anthropic 已将部分 OAuth 凭据限定 Claude Code 专用，在 opencode 里用 Claude 需 API key。

## 6. 常用命令与工作流

### TUI 交互模式
- 启动：`opencode`（当前目录）或 `opencode /path/to/project`
- 消息语法：`@` 附加文件；`!` 直接执行 shell 命令（如 `!ls -la`）

**内置 slash 命令**（`/` + 命令名；`ctrl+x` 为 leader 键）：
| 命令 | 用途 | 快捷键 |
|------|------|--------|
| `/init` | 创建/更新 `AGENTS.md` | — |
| `/new` | 新会话 | `ctrl+x n` |
| `/sessions` | 切换会话 | `ctrl+x l` |
| `/compact` | 压缩上下文 | `ctrl+x c` |
| `/undo` / `/redo` | 撤销/重做（Git 支撑） | `ctrl+x u` / `ctrl+x r` |
| `/models` | 切换模型 | `ctrl+x m` |
| `/connect` | 添加 provider | — |
| `/share` | 分享会话 | — |
| `/export` | 导出对话为 Markdown | `ctrl+x x` |
| `/exit` | 退出 | `ctrl+x q` |

### 非交互模式（run）
```bash
opencode run "Explain the use of context in Go"
opencode run --format json "list every TODO with file and line"
opencode run --agent plan --model anthropic/claude-haiku-4-5 "audit src/"
opencode run -f src/main.go "review this file"
```
- `--format default|json`（json = 原始事件流，供脚本/CI）
- `-m/--model provider/model`、`--agent`、`--variant`、`-f/--file`、`-c/--continue`、`-s/--session`
- `--auto`：自动批准未被拒绝的权限，**仅 CI**
- `--attach <url>`：挂到运行中的 server

### 服务/远程模式
- `opencode serve`：无头 API 服务器
- `opencode web`：无头服务器 + Web 界面
- `opencode attach [url]`：把 TUI 挂到远程后端
- `opencode acp`：ACP（Agent Client Protocol）服务器
- `opencode github`：`install` 生成 GitHub Actions 工作流；`run` 在 CI 中运行

### 会话/统计
- `opencode session list/delete`；`opencode stats [--days N]`（token 用量与成本）
- `opencode agent create`（引导创建自定义 agent，`--permissions/--tools` 指定权限）；`agent list`
- `opencode mcp add/list/auth/logout/debug`
- `opencode plugin/plug <module>`；`opencode pr <number>`；`opencode db`

## 7. 与 Claude Code 命令对照表

| 场景 | opencode | Claude Code |
|------|----------|-------------|
| 启动交互 TUI | `opencode` | `claude` |
| 非交互单次提示 | `opencode run "…"` | `claude -p "…"` |
| JSON 结构化输出 | `opencode run --format json` | `claude -p --output-format json` |
| 继续上次会话 | `opencode run -c` | `claude -p --continue` |
| CI 自动批准 | `opencode run --auto` | `claude -p --dangerously-skip-permissions` |
| 指定模型 | `opencode run -m provider/model` | `claude -m model` |
| 生成项目规范 | `/init` → `AGENTS.md` | `/init` → `CLAUDE.md` |
| 新会话 | `/new` | `/clear` |
| 压缩上下文 | `/compact` | `/compact` |
| 撤销 | `/undo`（Git） | `/undo`（Git） |
| 切换模型 | `/models` / `ctrl+x m` | `/model` |
| 登录/添加 provider | `/connect`、`auth login` | `/login` |
| 成本统计 | `stats` | `/cost` |
| MCP 管理 | `mcp add/list/auth` | `claude mcp add/list/get` |
| 自定义 agent | `agent create`（CLI 生成） | 手写 `.claude/agents/*.md` |
| 无头服务模式 | `serve`/`web`/`attach` | 无直接对应 |

注：映射为语义近似；`serve/attach`、`agent create`、`session list`、`stats` 在 Claude Code 中无直接等价。

## 8. 权限系统

**三值模型**：`allow`（自动放行）/ `ask`（弹窗询问）/ `deny`（阻断）。v1.1.1 起旧 `tools` 布尔配置废弃并入 `permission`。

**三层语法**：
```json
"permission": "allow",
"permission": { "bash": "allow", "edit": "deny" },
"permission": {
  "bash": { "*": "ask", "git *": "allow", "npm *": "allow", "rm *": "deny" }
}
```
- **last matching rule wins**：catch-all `"*"` 放最前、具体规则放后。
- 通配符：`*` 任意字符、`?` 单字符；`~`/`$HOME` 开头展开。
- 带参命令需带 `*` 后缀（`"grep *"` 才匹配 `grep pattern file`）。

**权限键**：`read`、`edit`、`glob`、`grep`、`bash`、`task`、`skill`、`lsp`、`question`、`webfetch`、`websearch`、`external_directory`、`doom_loop`、`todowrite`（15 个）。

**默认权限（关键）**：
- 大多数默认 `allow`（比 Claude Code 宽松得多）。
- `doom_loop`（同工具调用 3 次）与 `external_directory` 默认 `ask`。
- `.env` 系文件默认 deny（`*.env`、`*.env.*` deny，`*.env.example` 放行）。

**收紧默认权限**：
```json
"permission": { "*": "ask", "bash": { "*": "ask", "rm *": "deny", "git push *": "deny" } }
```
- `opencode --auto` 自动批准未显式 deny 的请求，显式 deny 仍生效。
- Agent 级权限（`agent.<name>.permission`）优先于全局。

**与 Claude Code 差异**：opencode 是"工具名 + 输入 glob + last matching wins"；Claude Code 是数组式规则、deny 优先、输入级匹配弱。默认基线 opencode 更宽。

## 9. 自定义 provider

**示例**（OpenAI 兼容 provider）：
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "venice/zai-org-glm-5-1",
  "provider": {
    "venice": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Venice AI",
      "options": {
        "baseURL": "https://api.venice.ai/api/v1",
        "apiKey": "{env:VENICE_API_KEY}"
      },
      "models": { "zai-org-glm-5-1": { "name": "GLM 5.1" } }
    }
  }
}
```
- provider 引用格式：`provider-id/model-id`。
- `npm` 保持 `@ai-sdk/openai-compatible`；`baseURL` 指向官方 v1 端点。
- 认证备选：`/connect` → Other → 填 provider ID → 粘贴 key，并从配置删掉 `options.apiKey`。

## 10. MCP 集成

**配置键**：`mcp`（Claude Code 是 `mcpServers`），每项必须带 `"type"`。

**local（STDIO 子进程）**：
```json
"mcp": {
  "filesystem": {
    "type": "local",
    "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    "environment": { "NODE_ENV": "production" },
    "timeout": 30000
  }
}
```
- `command` 是**数组**（避免 shell 注入）；env 键叫 `environment`；timeout 默认 30000ms。

**remote（HTTP/SSE）**：
```json
"mcp": {
  "remote-tools": {
    "type": "remote",
    "url": "https://mcp.example.com/v1",
    "headers": { "X-API-Key": "sk-..." }
  }
}
```

**OAuth 三种模式**：自动发现（默认，RFC 7591 动态注册）/ 预注册客户端（`clientId`）/ 禁用（`"oauth": false`，用 API key 时须显式关闭）。Token 存 `~/.local/share/opencode/mcp-auth.json`。

**CLI**：`opencode mcp list`（✓connected / ○disabled / ⚠needs_auth / ✗failed）、`mcp debug`、`mcp auth`、`mcp logout`。

**与 Claude Code 差异**：配置键名不同、command 用数组、env 用 `environment`、OAuth 内建自动流程、有完整 mcp 子命令族。

## 11. Skills 与 AGENTS.md

**上下文文件**：opencode 原生加载 `AGENTS.md`（Claude Code 用 `CLAUDE.md`）。

**SKILL.md 发现顺序**（6 个位置，均以 `<base>/skills/<name>/SKILL.md`）：
1. 项目 `.opencode/skills/`
2. 全局 `~/.config/opencode/skills/`
3. 项目 `.claude/skills/`
4. 全局 `~/.claude/skills/`
5. 项目 `.agents/skills/`
6. 全局 `~/.agents/skills/`

- SKILL.md frontmatter：仅识别 `name`（必填，小写+连字符）、`description`（必填，1-1024 字符）、`license`、`compatibility`、`metadata`。
- 调用：`skill({ name: "git-release" })`；权限 `permission.skill`（allow/deny/ask + 通配符）。

**扩展点**：自定义 Agent Markdown 文件（`~/.config/opencode/agents/`、`.opencode/agents/`）；hooks 仅支持 4 个共享 hook（`guard-shell`、`guard-read-large`、`inject-types-on-read`、`check-on-edit`），不支持 Claude-only hooks。

**迁移提示**：一套 skills/agents/guardrails 可通过适配器跨 Claude Code / OpenCode / Cursor / Codex 复用（如 spine 项目）。

## 12. 常见坑与排错

### 认证失败：`{env:VAR}` 空串破坏 auth.json 回退（issue #34388）
- 复现：`auth login` 存好 key → provider 配 `"apiKey": "{env:MY_API_KEY}"` → env 未设置 → 报 "Failed to initialize provider"。
- 根因：未设置 env 被替换为空串 `""`，而 provider 回退用严格相等 `=== undefined`，空串阻断 auth.json 回退 → 401。
- **教训**：自定义 provider 用 `{env:VAR}` 时，务必保证该 env 已导出，否则吞掉 auth.json 已存凭据。

### 模型不出现
- 检查 `models` map 是否注册、API key 是否在与启动 opencode 相同的 shell 导出、是否在项目目录运行以加载 `opencode.json`。

### 其他
- `baseURL` 须保持官方 v1 端点、`npm` 须为 `@ai-sdk/openai-compatible`，改错导致 endpoint 不匹配。
- 密钥含换行/空白（#25757）；`{env:}` 与 auth.json 双写冲突；版本回归破坏认证（降级可解，如 1.1.49）。
- 认证风险：Anthropic 部分 OAuth 凭据限定 Claude Code 专用，opencode 用 Claude 需 API key。

## 13. 信源清单

**官方文档/仓库**（主要信源）：
- https://opencode.ai — 官网
- https://github.com/anomalyco/opencode — GitHub 仓库（README：安装、架构、双 Agent）
- https://opencode.ai/docs/config — 配置体系
- https://opencode.ai/docs/cli — CLI 参考
- https://opencode.ai/docs/tui — TUI / slash 命令
- https://opencode.ai/docs/permissions — 权限系统
- https://opencode.ai/docs/skills — Skills 发现顺序
- https://opencode.ai/docs/agents — Agent 机制
- https://opencode.ai/docs/mcp — MCP（原始 URL 404，用 OpenCode-Book 8.4 补充）

**技术博客/社区**：
- https://www.builder.io/blog/opencode-vs-claude-code — 同模型实测对比
- https://deepinfra.com/blog/claude-code-alternative — 替代定位与优劣势
- https://docs.venice.ai/guides/integrations/opencode — 自定义 provider 配置
- https://github.com/kenoxa/spine — Skills/AGENTS 跨工具复用
- https://github.com/anomalyco/opencode/issues/34388 — 认证坑
- https://github.com/wesammustafa/opencode-primer — 社区 CLI 速查
- https://cloud.tencent.cn/developer/article/2646782 — 中文科普

**素材统计**：官方文档/仓库 9 篇、技术博客 4 篇、社区/Issue 3 篇；近 2 年内容为主。
