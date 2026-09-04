---
title: Claude Code 使用指南
tags: [ai, 工具使用, claude-code, 入门]
updated: 2026-09-04
status: updated
source_project: claude-code-tutorial
---

# Claude Code 使用指南

> [!info] 文档定位
> **日常操作速查手册** - 装好就能用，用的时候查。更适合中国宝宝体质的配置方案。
>
> 功能速查 → [[Claude Code 常用功能]] · CLI 命令参考 → [[Claude Code CLI 完整参考]]

---

## 一、快速安装

### 0️⃣ 国内网络安装（重点）

> [!tip] 先判断你有没有代理
> - **有代理** → 直接走第 1️⃣ 节的官方原生安装器，保持自动更新，最省心。
> - **没有代理** → 用方案 B（npm + 国内镜像），全程不走外网即可装完，但需手动升级。

#### 需要放行的域名

| 域名 | 用途 | 国内直连 |
|------|------|---------|
| `claude.ai` | 官方安装脚本（install.sh / .ps1 / .cmd） | ❌ 需代理 |
| `downloads.claude.ai` | 原生二进制、apt/dnf/apk 仓库、版本清单 | ❌ 需代理 |
| `code.claude.com` | 官方文档 | ❌ 需代理 |
| `registry.npmjs.org` | npm 官方源 | ⚠️ 慢/不稳 |
| `registry.npmmirror.com` | npm 国内镜像 | ✅ 直连 |
| `github.com` | GitHub Releases（社区分发、桌面端） | ⚠️ 不稳定，可用加速 |

> [!note] 「安装」和「运行」放行的域名不同
> 上表只管**安装/更新**阶段。装完后首次登录 / 每次运行还会连 `api.anthropic.com`（API 请求）与 `platform.claude.com`（Console / 订阅授权）；不想走官方网络，直接用 [[#二、跳过登录（免认证启动）]] 配置第三方中转，只连中转服务域名即可。

#### 方案 A：终端代理 + 官方原生安装器（推荐）

先给终端设置代理（见 [[#四、代理配置]]），再运行第 1️⃣ 节的一行命令。PowerShell 示例：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
irm https://claude.ai/install.ps1 | iex
```

> [!warning] 国内直连 `downloads.claude.ai` 失败时
> 原生安装器会报 `Failed to fetch version from https://downloads.claude.ai/...`，按 [[#七、常见问题与坑]] 的「ECONNREFUSED」条目处理（设代理或开全局模式）。

#### 方案 B：npm + 国内镜像（无代理首选）

**原理**：`@anthropic-ai/claude-code` 是分发壳包，真实二进制在平台子包里（如 `@anthropic-ai/claude-code-win32-x64`）。npmmirror 已同步这些平台包，因此全程走国内镜像即可装完。

> [!tip] npm 渠道 2026-09 状态：仍在维护、同步发布
> 官方文档现在把原生安装器列为首选、npm 列为高级/备选方式，但 npm 包仍与原生**同步发布**（截至 2026-09-04 两边同为 v2.1.260），npmmirror 也已同步主包和全部平台子包。无代理用户可放心用本方案；担心以后被砍，可先用着，将来需要迁移原生时在有代理的环境跑 `claude install`。

**前置**：Node.js **22+**（官方下载：[nodejs.org](https://nodejs.org)，国内镜像：[npmmirror node](https://npmmirror.com/mirrors/node/)）

```bash
# ① 切换 npm 到国内镜像
npm config set registry https://registry.npmmirror.com

# ② 全局安装
npm install -g @anthropic-ai/claude-code
# 安装时显式放行 claude-code 的 postinstall
npm install -g @anthropic-ai/claude-code --allow-scripts=@anthropic-ai/claude-code
# ③ 验证
claude --version
```

> [!warning] 报 `claude native binary not installed` 时
> 通常是镜像未同步平台子包、或 postinstall 未执行。任选其一修复：
>
> ```bash
> # ① 显式安装平台子包（Windows x64 示例；macOS 换 -darwin-arm64/-darwin-x64）
> npm install -g @anthropic-ai/claude-code @anthropic-ai/claude-code-win32-x64
>
> # ② 从官方源重装（需代理，强制 optional 依赖 + 前台日志）
> npm install -g @anthropic-ai/claude-code --include=optional --foreground-scripts --registry=https://registry.npmjs.org/
> ```
>
> 安装过程被 `npm warn allow-scripts` 拦截、postinstall 未执行时，按 [[#npm 安装被 allow-scripts 拦截（postinstall 未执行）]] 处理。

**升级**：npm 方式**不自动更新**，手动执行：

```bash
npm install -g @anthropic-ai/claude-code@latest
```

> [!tip] 不登录官方账号
> 配置了第三方 API（见 [[#二、跳过登录（免认证启动）]]）时，可在 `~/.claude/settings.json` 的 `env` 加 `"DISABLE_INSTALLATION_CHECKS": "1"` 关闭安装检查提示。

#### 方案 C：macOS Homebrew

```bash
brew install --cask claude-code          # 稳定版（滞后约一周）
brew install --cask claude-code@latest   # 最新版
```

brew 本体可先用清华/阿里镜像加速，但 cask 下载的安装包仍可能走国外域名，慢的话直接改用方案 B。

#### 方案 D：GitHub 加速 / 社区一键脚本

- **GitHub Releases**：`downloads.claude.ai` 不通时，可从 [anthropics/claude-code releases](https://github.com/anthropics/claude-code/releases) 下载对应平台二进制——每个版本已附带 `claude-darwin-arm64.tar.gz`、`claude-win32-x64.zip` 等包与 `SHASUMS256.txt`（含 `.sig` 签名）。可配合 `gh-proxy.com` 等加速前缀；第三方镜像不稳定，下载后用仓库自带的 `SHASUMS256.txt` 核对 SHA256。
- **cc-download**（[ipfred/cc-download](https://github.com/ipfred/cc-download)）：Windows 安装/更新工具，支持代理、下载进度、SHA256 校验、离线安装包。
- **claude-code-bootstrap**（[ErgeAIA/claude-code-bootstrap](https://github.com/ErgeAIA/claude-code-bootstrap)）：Windows PowerShell 一键安装，native → winget → npm 三级兜底，自动测速选择镜像。

### 1️⃣ 一行命令安装（推荐）

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows CMD
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> [!tip] 原生安装器优势
> - 自动更新 · 无需 Node.js · 体积约 60-80MB
> - 安装后执行 `claude --version` 验证，当前 latest 为 **v2.1.260**（2026-09-04），stable 通常滞后约一周

### 2️⃣ 其他安装方式（备选）

| 平台 | 命令 | 更新方式 |
|------|------|---------|
| macOS Homebrew | `brew install --cask claude-code`（或 `claude-code@latest`） | 手动 `brew upgrade claude-code` |
| Windows WinGet | `winget install Anthropic.ClaudeCode` | 手动 |
| npm（国内无代理首选） | `npm install -g @anthropic-ai/claude-code`（先配镜像，见 [[#0️⃣ 国内网络安装（重点）\|国内网络安装]]） | 手动 `npm i -g @anthropic-ai/claude-code@latest` |
| Linux apt/dnf/apk | `apt install claude-code` 等（官方仓库） | 系统包管理器 |

### 3️⃣ 前置依赖

| 要求 | 说明 |
|------|------|
| **Git** | Claude Code 版本控制依赖，需安装并配置 `git config --global user.name/email` |
| **Node.js** | 仅 npm 方式需要 **22+**（v2.1.198 起），**原生安装器不需要** |
| **RAM** | 最低 4GB，推荐 8GB |

#### 安装 Git

Git 是 Claude Code 做版本控制（`/commit`、`/diff`、回滚）和 Subagent worktree 的底层依赖，三种主流平台装法如下。

**Windows**

| 方式 | 操作 |
|------|------|
| WinGet（推荐） | `winget install Git.Git` |
| 官方安装包 | [git-scm.com](https://git-scm.com/download/win) 下载 `.exe`，一路 Next 即可 |
| 国内加速 | 官方下载慢时用 npmmirror / 清华 TUNA 的 `git-for-windows` 镜像，或开代理直连 |

**macOS**

```bash
xcode-select --install   # 安装 Xcode Command Line Tools，自带 Git（推荐）
# 已装 Homebrew 的话也可以：
brew install git
```

**Linux**

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y git
# Fedora / RHEL
sudo dnf install -y git
```

**装完验证 + 首次配置**

```bash
git --version                                   # 验证安装
git config --global user.name "你的名字"         # Claude Code 提交署名
git config --global user.email "you@example.com"
```

> [!warning] 不配 user.name / user.email 会报错
> Claude Code 的 git 操作依赖这两个全局配置；缺失时提交会提示 `Please tell me who you are`，配置完即可恢复。

#### 安装 Node.js（仅 npm 方案需要）

> **前置判断**：走**官方原生安装器**（方案 A / C / D）不需要 Node.js；只有 **npm 渠道（方案 B，国内无代理首选）** 要求 **Node 22+**。装 Claude Code 前先跑 `node -v`，低于 `v22` 再按下面装。

**Windows**

| 方式 | 操作 |
|------|------|
| 安装包（推荐新手） | 到 [nodejs.org](https://nodejs.org) 或 [npmmirror 镜像](https://npmmirror.com/mirrors/node/) 下载 **LTS 版 `.msi`**，一路 Next |
| WinGet | `winget install OpenJS.NodeJS.LTS` |
| 多版本管理 | `nvm-windows`（[coreybutler/nvm-windows](https://github.com/coreybutler/nvm-windows)），适合要切多个 Node 版本 |

**macOS**

```bash
brew install node        # Homebrew 默认装当前稳定版（≥22）
# 需要多版本可改用 fnm / nvm
```

**Linux（注意：系统自带 nodejs 通常太旧）**

Debian / Ubuntu 仓库里的 `nodejs` 常低于 22，达不到要求。推荐官方 LTS 二进制或 nvm：

```bash
# ① 官方/镜像 LTS 二进制（以 linux-x64 为例，版本号替换为你要装的 LTS）
#    下载地址：https://nodejs.org 或 https://npmmirror.com/mirrors/node/
sudo tar -xJf node-v24.x.x-linux-x64.tar.xz -C /usr/local --strip-components=1

# ② 或 nvm（无需 sudo、方便切版本）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm install --lts
```

**装完验证**

```bash
node -v    # 输出 ≥ v22 即可
npm -v
```

> [!tip] 装完先切 npm 国内镜像
> 无代理用户装完 Node 后，先执行 `npm config set registry https://registry.npmmirror.com` 再装 Claude Code，否则 npm 仍走官方源很慢。切换细节见 [[#方案 B：npm + 国内镜像（无代理首选）|方案 B：npm + 国内镜像]]。

> [!tip] 企业代理注意
> v2.1.116+ 从 `https://downloads.claude.ai/claude-code-releases` 下载二进制文件，需将该域名加入代理白名单。

> [!info] 📚 来源
> - [GitHub 官方仓库](https://github.com/anthropics/claude-code) · [GitHub Releases](https://github.com/anthropics/claude-code/releases)
> - [Homebrew Cask](https://github.com/Homebrew/homebrew-cask) · [全平台安装指南](https://www.morphllm.com/install-claude-code)

---

## 二、跳过登录（免认证启动）

Claude Code **没有** `--no-auth` 参数，但有 6 种方式跳过 OAuth 登录。所有 API Key 类方式按**官方认证优先级**从上到下解析，同时配置多个时取最上面的一个生效。

> [!tip] 确认当前认证方式
> 在会话里运行 `/status`：`Login method` 行显示订阅账号，`API key` 行表示正在用 API Key，`Auth token` 行表示在用 `ANTHROPIC_AUTH_TOKEN` / `apiKeyHelper`。

### 官方认证优先级（高 → 低）

| 优先级 | 认证方式 | 说明 |
|--------|----------|------|
| 1 | 云厂商凭证（Bedrock / Vertex / Foundry） | 设 `CLAUDE_CODE_USE_BEDROCK` 等变量 |
| 2 | `ANTHROPIC_AUTH_TOKEN` | 环境变量，发 `Authorization: Bearer` 头 |
| 3 | `ANTHROPIC_API_KEY` | 环境变量，发 `X-Api-Key` 头 |
| 4 | `apiKeyHelper` 脚本输出 | settings.json 配置 |
| 5 | `CLAUDE_CODE_OAUTH_TOKEN` | `claude setup-token` 生成的长期 token |
| 6 | 订阅 OAuth 登录 | `/login` 登录的 Pro / Max / Team 等账号 |

> [!warning] 订阅 vs API Key
> 已登录订阅且设置了 `ANTHROPIC_API_KEY` 时，**Key 优先**（交互式会先弹一次确认）。想切回订阅：`unset ANTHROPIC_API_KEY`，再用 `/status` 复查。

### 方式一：apiKeyHelper ⭐ 官方推荐

在 `~/.claude/settings.json` 中配置 API Key 辅助脚本路径：

```json
{
  "apiKeyHelper": "/Users/你的用户名/.claude/api-key-helper.sh"
}
```

该脚本内容只需输出你的 API Key：

```bash
#!/bin/bash
echo "sk-ant-你的API密钥"
```

> [!tip] 2026 新增行为
> - 脚本通过系统 shell 运行：macOS/Linux 用 `/bin/sh`，Windows 用 `cmd`（如 `powershell -NoProfile -File C:\scripts\get-key.ps1`）
> - 输出**同时**作为 `X-Api-Key` 和 `Authorization: Bearer` 两个头发送，网关 / 代理都认
> - 默认 **5 分钟**缓存一次，或遇 HTTP 401 立即重取；可用 `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` 自定义间隔（毫秒）
> - v2.1.208 起脚本失败会报 `Your apiKeyHelper script is failing`（3 次重试后）
> - 适用于 CLI、VS Code 扩展、Agent SDK、GitHub Actions；**不适用于** Claude Desktop 和云端会话

> [!warning] 注意
> - **不要**同时设置 `ANTHROPIC_API_KEY` 环境变量（会冲突）
> - 删除 `~/.claude.json` 中的 `oauthAccount` 条目
> - 嫌写脚本麻烦，直接用下面的「方式二」env 字段，纯 JSON 一步到位

### 方式二：env 字段（走第三方 API，无需命令行）⭐ 最常用

不用每次 export，直接在 `~/.claude/settings.json` 的 `env` 字段配好就行。settings 文件里的 `env` **会覆盖** shell 里 export 的同名变量。

**使用 OpenRouter：**

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-or-v1-你的密钥",
    "ANTHROPIC_MODEL": "anthropic/claude-sonnet-4-6",
    "ANTHROPIC_API_KEY": ""
  }
}
```

**使用本地模型（LiteLLM + Ollama）：**

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8000/v1",
    "ANTHROPIC_AUTH_TOKEN": "sk-123",
    "ANTHROPIC_API_KEY": ""
  }
}
```

先启动桥接：`ollama pull qwen2.5-coder:7b && litellm --model ollama/qwen2.5-coder:7b --port 8000`

> [!warning] 协议与副作用
> - Claude Code 使用 **Anthropic `/v1/messages`** 协议：OpenRouter ✅ · LiteLLM ✅（自动转换） · **Ollama 直连 ❌**（必须通过 LiteLLM）
> - 模型**必须支持 Tool Use / Function Calling**；`ANTHROPIC_MODEL` 示例按你当前可用的模型名填写
> - `ANTHROPIC_BASE_URL` 指向非官方域名时：**Remote Control 不可用**（v2.1.196 起）；MCP 工具搜索默认关闭，需要时设 `ENABLE_TOOL_SEARCH=true`

### 方式三：hasCompletedOnboarding（跳过首启登录引导）

不想看到首次启动的「选主题 → 登录」引导，直接改 `~/.claude.json`（Windows：`C:\Users\<用户名>\.claude.json`）：

```json
{
  "hasCompletedOnboarding": true,
  "theme": "dark"
}
```

> [!tip] 说明
> 部分版本只设 `hasCompletedOnboarding` 仍会弹引导，**同时给 `theme` 一个值**更保险。适合配合上面的 API 方式免登录启动，ccgo 等启动器也是这么做的（`ccgo init`）。

### 方式四：primaryApiKey（旧方案，已不可靠）⚠️

```json
{
  "primaryApiKey": "sk-ant-你的API密钥",
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

> **permissions 可选值**：
> - `"bypassPermissions"` — 自动批准所有操作（YOLO 模式）
> - `"acceptEdits"` — 仅自动批准文件编辑
> - `"manual"` — 每次操作都询问（原 Default 权限模式已改名 Manual）

> [!warning] 2026 状态：不推荐
> `primaryApiKey` **不在官方认证优先级里**，官方文档已不列该字段。v2.0.37 起多个版本不再读取它（[GitHub issue #11631](https://github.com/anthropics/claude-code/issues/11631)），仍会弹 API Key 确认框；Docker 沙箱还会因 `.claude.json` 里存在该字段而报「凭据冲突」警告。新配置请改用**方式一**（脚本）或**方式二**（env 字段）。

### 方式五：claude setup-token（CI 长期 token）

官方提供的一次性生成长期 token，适合 CI/CD、脚本等无法弹浏览器登录的场景：

```bash
claude setup-token        # 浏览器授权后，终端打印 token（不会自动保存）
export CLAUDE_CODE_OAUTH_TOKEN=your-token
```

> [!tip] 说明
> - token 有效期 **1 年**，需要 Pro / Max / Team / Enterprise 订阅
> - 只能发模型请求，不能用于 Remote Control 或 claude.ai 连接器
> - `--bare` 模式不读该 token，请改用 `ANTHROPIC_API_KEY` 或 `apiKeyHelper`

### 方式六：CC-Switch ⭐ 可视化方案

> 跨平台桌面应用，**131K+ Star**，支持 Claude Code / Codex / Gemini CLI / OpenCode / Grok Build / OpenClaw / Hermes Agent 共 8 种工具的供应商切换，内置 50+ 平台预设。

**开发者**：[farion1231](https://github.com/farion1231/cc-switch) · **开源协议**：MIT · **最新版**：v3.20.1

#### 安装

| 平台 | 命令 / 方式 |
|------|-------------|
| macOS | `brew tap farion1231/ccswitch && brew install --cask cc-switch` |
| Windows | GitHub Releases 下载 `.msi` 安装包（或 `-Portable.zip` 免安装版） |
| Linux | DEB / RPM / AppImage 任选 |

#### 配置步骤

1. 打开 CC-Switch，选中 **Claude Code**
2. 点击右上角 **+** 号，在预设中选择你的平台（如 SiliconFlow、DeepSeek、智谱等）
3. 自动填入端点地址和模型映射，只需填写 **API Key**
4. 在首页点击「启用」即可生效

> [!tip] CC-Switch 优势
> - **热切换**：切换供应商**无需重启终端**，即时生效
> - **故障转移**：本地代理自动故障转移 + 熔断，某家宕机自动切到下一家
> - **用量统计**：Token 消耗追踪、成本监控、趋势图表
> - **MCP / Skills 统一管理**：一处编辑，双向同步到所有工具
> - **云同步**：支持 WebDAV / Dropbox / OneDrive / iCloud 多设备同步
> - **其他**：Session 管理器、Deep Link（`ccswitch://`）一键导入配置

> [!warning] 注意
> 如果同时配置了环境变量或 `settings.json`，可能会产生冲突。建议使用 CC-Switch 后，清空其他配置项，避免互相覆盖。

> [!tip] Claude Code Desktop 免登录接第三方模型
> 桌面版不走 `settings.json` 的 `env`，需单独配置：Help → **Troubleshooting** → **Enable Developer Mode**，重启后到 **Developer** → **Configure Third-Party Inference** 填 Gateway Base URL + API Key 即可免登录使用。

---

## 三、配置文件（最常用配置合集）

配置文件位置：**`~/.claude/settings.json`**

### 完整配置模板（官方 env 写法，复制粘贴即可用）

> [!warning] 先别用网上流传的 `providers` / `defaultProvider`
> `"providers"` + `"defaultProvider"` **不是官方配置**。Claude Code 原生不支持多 provider 路由（[官方 issue #74073](https://github.com/anthropics/claude-code/issues/74073)），这两个 key 写在 settings.json 里会被**静默忽略**。官方方式只有一个上游：在 `env` 里设 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN`。

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com",
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_MODEL": "deepseek-chat",
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

### 支持的第三方平台（填进 env）

| 平台 | ANTHROPIC_BASE_URL | ANTHROPIC_MODEL |
|------|---------|--------------|
| 火山引擎 | `https://ark.cn-beijing.volces.com/v1` | `ep-xxxxx` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-plus` |
| Ollama | `http://localhost:11434/v1` | `llama3.2` |

> **配置优先级**：环境变量 > settings.json > 默认值

### 多平台一键切换（官方不原生支持）

原生没有「配多个 provider、改一个开关切换」的机制。可行的替代方案：

1. **按平台存多份 settings 文件，用 `--settings` 启动**（推荐）
   ```bash
   claude --settings ~/.claude/settings.deepseek.json
   claude --settings ~/.claude/settings.volc.json
   ```
   每份文件只含对应的 `env`（`ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_MODEL`）。

2. **第三方切换工具**：CC-Switch（见 [[#方式六：CC-Switch ⭐ 可视化方案]]）等，本质也是改写 `env` 或替换配置文件。

3. **本地代理桥接**：用 LiteLLM 把多个上游合并成一个 Anthropic 兼容端点（见 [[#方式二：env 字段（走第三方 API，无需命令行）⭐ 最常用]]）。

### 取消代理

```json
{ "env": { "HTTP_PROXY": "", "HTTPS_PROXY": "" } }
```

> [!tip] 配置常见坑
> - JSON 格式错误、路径不对、环境变量覆盖 → 重启 Claude Code 生效
> - 切换第三方平台时，**同时**改 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_MODEL` 三个 env

---

## 四、代理配置

### 推荐：settings.json 配置（永久）

在 `~/.claude/settings.json` 的 `env` 字段中配置：

```json
{
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

### 取消代理

```json
{ "env": { "HTTP_PROXY": "", "HTTPS_PROXY": "" } }
```

### 常用代理端口

| 软件 | 默认端口 |
|------|---------|
| Clash | 7890 |
| V2Ray | 10808 |
| Shadowsocks | 1080 |

---

## 五、日常使用速查

### 启动命令

| 命令 | 作用 |
|------|------|
| `claude` | 启动交互会话 |
| `claude --model claude-sonnet-5` | 指定模型启动（默认 Sonnet 5） |
| `claude -m deepseek-chat` | 使用第三方模型 |
| `claude -p "query"` | 打印模式，执行后退出（自动化/CI） |
| `claude -c` | 继续最近会话 |
| `claude --resume <name>` | 恢复命名会话 |
| `claude agents` | 统一代理视图（运行/阻塞/完成的会话） |
| `claude --safe-mode` | 安全模式，禁用所有自定义项（排障用） |
| `claude --worktree` | Subagent 使用隔离 git worktree |
| `claude --permission-mode manual` | 手动权限模式启动（原 Default 已改名 Manual，每次操作询问） |
| `claude --version` | 查看版本 |
| `claude --debug` | 调试模式 |

> [!tip] 2026-08 模型现状
> - **默认模型 = Claude Sonnet 5**：原生 1M token 上下文；促销价 **$2 / $10 每 Mtok**（至 2026-08-31）。
> - **默认 Opus = Claude Opus 5**：同为原生 1M 上下文。
> - 指定模型：`claude --model claude-sonnet-5` 或 `/model claude-opus-5`。

### 会话中常用 `/` 命令

> [!tip] 2026 年新增命令
> `/cd` `/code-review` `/usage` `/effort` `/doctor` `/fast` `/plan` `/todos` `/goal` `/subtask` 等均为 2026 年新引入，旧版参考中可能未收录。其中 `/checkup` 是 `/doctor` 的别名，`/review` 是 `/code-review` 的别名。

| 命令 | 作用 |
|------|------|
| `/model` | 切换模型（列出可选） |
| `/model claude-opus-5` | 直接切换到指定模型（默认 Opus 5） |
| `/plan` | 强制规划/只读模式 |
| `/effort` | 设置努力级别（standard/high/xhigh） |
| `/fast` | 切换速度优化 API 设置 |
| `/cd <path>` | 切换工作目录（不重建缓存） |
| `/todos` | 跨会话持久化任务列表 |
| `/goal` | 保持工作直到完成条件满足 |
| `/code-review` | 代码审查（`/review` 是别名；不再自动运行，需手动调用；`--fix` 直接修复） |
| `/memory` | 编辑 CLAUDE.md（不离开会话） |
| `/doctor` | 全量环境体检（诊断/修复安装健康、未用 skills/MCP/插件、CLAUDE.md 裁剪与去重建议、慢 hooks 标记；`/checkup` 是别名） |
| `/usage` | 查看配额使用明细（按 skill/agent/插件） |
| `/compact` | 压缩会话上下文释放空间 |
| `/context` | 显示 token 消耗 |
| `/cost` | 查看 Token 消耗与费用 |
| `/rewind` | 回滚到检查点 |
| `/fork` | 复制当前对话到新后台会话 |
| `/subtask` | 会话内子代理（取代旧 in-session 子代理） |
| `/diff` | 查看会话的 git diff |
| `/init` | 创建 CLAUDE.md |
| `/clear` | 清除当前会话 |
| `/help` | 帮助 |
| `/mcp` | 查看 MCP 列表 |

### MCP 管理

```bash
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path
claude mcp list         # 查看所有
claude mcp remove fs    # 删除
claude mcp enable fs    # 启用
claude mcp disable fs   # 禁用
```

> 详细 MCP 教程 → [[Claude MCP 使用指南]]

### Skills 使用

```bash
/help              # 查看可用技能
/commit            # 提交代码
/review-pr 123     # 审查 PR
"帮我画一个流程图"   # 自然语言触发
```

> 了解 Skills → [[Skills 是什么]] · 自定义技能 → [[如何编写Skills]]

---

## 六、CLAUDE.md

> **项目级记忆文件**，Claude Code 启动时自动读取，定义项目规范、工作流、禁止事项。
> 详细的**三层记忆体系**（CLAUDE.md + Auto Memory + 自建参考文档）见 → [[#八、记忆系统]]

```bash
# 自动生成（推荐）
claude
/init
```

| 文件 | 位置 | 作用域 | 提交到 Git |
|------|------|--------|------------|
| `CLAUDE.md` | 项目根目录 | 项目级 | ✅ |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | ❌ |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | ❌ |

> 完整指南 → [[CLAUDE.md 使用指南]]

---

## 七、常见问题与坑

### 安装问题

#### Windows 原生安装后找不到命令

> [!warning] 问题现象
> 安装成功但运行 `claude --help` 报错"无法识别为 cmdlet"

> [!tip] 原因
> 原生安装器安装到了 `C:\Users\你的用户名\.local\bin`，但该路径未加入 PATH 环境变量

**解决方法**：

1. **复制路径**：`C:\Users\你的用户名\.local\bin`

2. **打开环境变量设置**：
   - 按 `Win` 键，搜索"环境变量"
   - 点击"编辑系统环境变量"

3. **添加 PATH**：
   - 点击"环境变量..."
   - 在"用户变量"中选中 `Path`，点击"编辑"
   - 点击"新建"，粘贴上述路径
   - 确认保存

4. **重启 PowerShell**：关闭当前窗口，重新打开后即可使用

---

#### Windows 安装时报 ECONNREFUSED

> [!warning] 问题现象
> 安装失败，提示 `ECONNREFUSED`
> ```
> × Installation failed
> Failed to fetch version from https://downloads.claude.ai/claude-code-releases/latest
> ```

> [!tip] 原因
> 网络连接被拒绝，通常是代理软件未接管命令行流量

**解决方法**：为 PowerShell 设置临时代理

```powershell
# 设置代理（将 7890 替换为你的代理端口）
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"

# 重新运行安装
irm https://claude.ai/install.ps1 | iex
```

> [!tip] 备选方案
> 把代理软件切换为全局模式

> [!info] 常用代理端口
> - Clash：7890
> - V2Ray：10809
> - Shadowsocks：1080

#### npm 安装后报 claude native binary not installed

> [!warning] 问题现象
> `npm install -g @anthropic-ai/claude-code` 装完，运行 `claude` 报 `Error: claude native binary not installed`

> [!tip] 原因
> 主包只是壳包，真实二进制在平台子包（如 `@anthropic-ai/claude-code-win32-x64`）里，靠 postinstall 替换。镜像未同步平台包、或脚本被 `--ignore-scripts` / `--omit=optional` 跳过时，stub 未被替换。

**解决方法**（任选其一）：

```bash
# ① 显式安装平台子包（Windows x64 示例；macOS 换 -darwin-arm64/-darwin-x64）
npm install -g @anthropic-ai/claude-code @anthropic-ai/claude-code-win32-x64

# ② 从官方源重装（需代理，强制 optional 依赖 + 前台日志）
npm install -g @anthropic-ai/claude-code --include=optional --foreground-scripts --registry=https://registry.npmjs.org/
```

> 安装成功后 `claude.exe` 约 200MB+，可据此判断 stub 是否被替换；仍不行则改用官方原生安装器。

#### npm 安装被 allow-scripts 拦截（postinstall 未执行）

> [!warning] 问题现象
> 全局安装时输出：
> ```text
> npm warn allow-scripts 1 package has install scripts not yet covered by allowScripts:
> npm warn allow-scripts   @anthropic-ai/claude-code@2.1.260 (postinstall: node install.cjs)
> npm warn allow-scripts
> npm warn allow-scripts Run `npm approve-scripts --allow-scripts-pending` to review, or `npm approve-scripts <pkg>` to allow.
> ```

> [!tip] 原因
> npm 11.16+ 引入 `allowScripts` 安装脚本策略，对**未审阅**的 postinstall 脚本输出警告（11.x 仅警告、脚本仍执行；**npm v12 起默认真正拦截**）。`@anthropic-ai/claude-code` 的 postinstall（`node install.cjs`）负责下载配置原生二进制，脚本被跳过时只装上壳包，运行报 `claude native binary not installed`。
>
> `npm approve-scripts <pkg>` 只对**本地项目**（有 `package.json`）生效；全局安装（`-g`）没有可写 `allowScripts` 字段的 `package.json`，会报错（官方错误码 `EGLOBAL`，也可能显示 `ENOMATCH`）。

**解决方法**（全局安装场景，任选其一）：

```bash
# ① 安装时显式放行 claude-code 的 postinstall
npm install -g @anthropic-ai/claude-code --allow-scripts=@anthropic-ai/claude-code

# ② 写入 npm 用户配置持久化（--location=user），之后安装不用再带参数
npm config set allow-scripts=@anthropic-ai/claude-code --location=user
npm install -g @anthropic-ai/claude-code

# ③ 想看 postinstall 实时日志（可选）
npm config set foreground-scripts true
```

> [!warning] 别用 `npm config set allow-scripts true`
> `allow-scripts` 是**包名列表**（逗号分隔字符串），不是布尔开关；写 `true` 只是加了一条名为 `true` 的包名，不会放行 claude-code。真要全放行用 `--dangerously-allow-all-scripts`，全禁止用 `--ignore-scripts`。

> [!tip] 成功判定
> 日志中出现 `> @anthropic-ai/claude-code@2.1.260 postinstall` / `> node install.cjs` 即代表脚本已执行；末尾的 `npm warn allow-scripts` 只是例行提示，不影响结果。最终以 `claude --version` 输出版本号为准；若提示 `'claude' 不是内部或外部命令`，把 `C:\Users\<用户名>\AppData\Roaming\npm` 加入系统 Path 并重启终端。

### 代理问题

| 问题 | 解决 |
|------|------|
| 设置了系统代理但终端连不上 | 终端需单独设 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量 |
| settings.json 的代理不生效 | 环境变量优先级更高，先 `echo $HTTP_PROXY` 检查 |
| 代理速度慢 | 切换节点或检查网络质量 |
| 临时取消代理 | `unset HTTP_PROXY HTTPS_PROXY` |

### MCP 问题

| 问题 | 解决 |
|------|------|
| MCP 连接失败 | 确认 `npx` 已安装、命令正确、环境变量已设置 |
| 手动测试 | `npx -y @modelcontextprotocol/server-filesystem /test/path` |

### 其他

| 问题 | 解决 |
|------|------|
| 配置不生效 | 路径？JSON 格式？环境变量覆盖？重启 Claude Code？ |
| 模型切换失败 | 模型名称不正确？平台不支持？API Key 无效？ |

### 安全建议

```bash
# 把敏感文件加入 .gitignore
.env
.mcp.json
settings.json
```

> MCP vs Skills 区别 → [[Claude MCP 使用指南]] 提供工具，[[Skills 是什么]] 提供任务模板

---

## 八、记忆系统

> Claude Code 的记忆体系由三层构成：**CLAUDE.md（明规则）→ Auto Memory（隐规则）→ 自建参考文档（专项知识）**。三者配合，cc 越用越懂你。

### 8.1 三层记忆总览

| 层 | 位置 | 优先级 | 加载方式 | 谁在维护 |
|----|------|--------|----------|----------|
| 1 | CLAUDE.md（三级） | 高 | 会话启动全量加载 | 你手动维护 |
| 2 | Auto Memory | 中 | 先读索引、按需读子文件 | cc 自己写、你校对修改 |
| 3 | 参考文档 | 按需 | cc 遇到对应任务才读 | 你手动维护 |

> **本质认知**：agent 的所有"记忆"，本质上都是在合适的时候向大模型注入压缩过的上下文。这些机制本质上还是提示词工程，只不过由 cc 帮你组织了层次。

**选层决策树：**

```
这条信息是...
├── 团队所有人都要遵守的硬性规矩？
│   └── → 第一层 CLAUDE.md（提交到 git）
├── 你个人的开发偏好？
│   └── → 第一层 ~/.claude/CLAUDE.md（用户级）
├── 项目积累的经验教训、踩坑记录？
│   └── → 第二层 Auto Memory（让 cc 自己记）
├── 太长太专门、不需要每次都读的内容？
│   └── → 第三层 参考文档（按需加载）
└── 只在某些文件/目录下才适用的规则？
    └── → .claude/rules/ + paths: 元数据（路径范围规则）
```

---

### 8.2 第一层：CLAUDE.md

> **你主动立下的规矩**，会话启动时全量加载，第一优先级。

**三级 CLAUDE.md：**

| 级别 | 文件位置 | 作用域 | 共享 | 最佳用途 |
|------|---------|--------|------|----------|
| 项目级 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 项目 | 团队（提交 git） | 编码规范、架构决策、常用命令 |
| 用户级 | `~/.claude/CLAUDE.md` | 全局 | 个人 | 开发偏好、编辑器快捷键、沟通风格 |
| 本地级 | `./CLAUDE.local.md` | 项目 | 个人（不提交 git） | 个人项目特定设置 |

> [!tip] 官方建议
> - 限制 **200 行以内**，超长降低依从性
> - 子目录 `CLAUDE.md` 仅当读取目录内文件时加载，适合 monorepo
> - `.claude/rules/` + `paths:` 元数据：路径范围规则，触及时才加载，节省上下文预算

**快速更新 Memory：**

```
# 这个项目始终使用 TypeScript 严格模式

# new rule into memory
始终使用 Zod schemas 验证用户输入

# remember this
所有版本发布使用语义化版本号
```

---

### 8.3 第二层：Auto Memory（cc 自己的笔记本）

如果说 CLAUDE.md 是**你主动立下的规矩**，那 Auto Memory 就是 **cc 在干活过程中默默记下的设计笔记**。你没显式写进 CLAUDE.md 的习惯、反馈、项目踩坑，会被一个后台 agent 静静记录。

**如何启用：**

```bash
# 在 cc 会话中输入
/memory

# 在弹出的菜单里选第一个选项"启用 Auto Memory"
# 启用后菜单里会多出"打开自动记忆文件夹"选项
```

**Auto Memory 在磁盘上的样子：**

```
~/.claude/projects/<项目标识>/memory/
├── MEMORY.md          # 索引文件，启动时加载前 200 行
├── user/              # 关于你的信息
│   └── preferences.md
├── feedback/          # 你给过的反馈
│   └── 2026-07-28_dont-override-config.md
└── project/           # 项目进度与决策
    └── architecture-decisions.md
```

**Auto Memory 会记哪几类东西：**

| 类型 | 含义 | 举例 |
|------|------|------|
| `user` | 关于你 | 你的角色、偏好（如"不喜欢深色 UI"） |
| `feedback` | 你给过的反馈 | "不要这样做"、"对，就这样" |
| `project` | 项目相关 | 进度、决策、技术选型 |
| `reference` | 外部资源索引 | "某份设计文档在 docs/design.md" |

**使用手感（重要）：**

- 它只在当前项目生效（文件存在项目目录下），换项目需重新积累
- 启用后 cc 不会每次都把所有记忆全部加载进上下文，只会读一份 `MEMORY.md` 索引——**遇到具体问题才去读对应的子文件**，占 token 很少
- 随时可以用快捷键 `Ctrl+O` 在会话中查看实际被调用过的记忆内容
- 记错了就跟它说："忘掉刚刚说的不喜欢深色主题"，它会自己删掉
- 或者在 `/memory` 菜单里选"打开自动记忆文件夹"，直接编辑对应子文件

**已知局限性：**

- 记录频率有限——不会每句话都记，只在 cc 判断"值得记住"时才写
- 准确度取决于 cc 的判断，偶尔会记偏或漏记，建议定期校对

> 提示：**一句话区分 CLAUDE.md vs Auto Memory**：CLAUDE.md 是**第一优先级、全量注入的明规则**；Auto Memory 是**第二优先级、按需注入的隐规则**。两者配合，cc 越用越懂你。

---

### 8.4 第三层：自建参考文档（渐进式披露）

除了上面两层，你还可以仿照 Skill 的"渐进式披露"机制为 cc 手动打造一套**专项参考文档**。

**应用场景**：某些东西不适合全部塞进 CLAUDE.md（太长、太专门），但 cc 需要的时候必须能查到。比如：

- **品牌视觉规范**：颜色、字体、间距 → `docs/brand-visual.md`
- **产品文本风格**：语调、术语表 → `docs/copywriting-style.md`
- **API 约定**：请求响应格式、错误码 → `docs/api-conventions.md`

**两种实现模式：**

| 方式 | 做法 | 适合场景 |
|------|------|---------|
| CLAUDE.md 指引 | 在 CLAUDE.md 里写"改视觉时必读 docs/brand-visual.md" | 文档 1-3 份，内容稳定 |
| `@` 导入 | 在 CLAUDE.md 里用 `@docs/api-conventions.md` 直接引入 | 文档 4+ 份，或内容经常变 |

**CLAUDE.md 指引模式示例：**

```markdown
## 外部参考文档

- 修改前端视觉、调颜色、调间距时 → 必读 `docs/brand-visual.md`
- 写产品文案、按钮文字、提示语时 → 必读 `docs/copywriting-style.md`
- 写 API、定义返回格式时 → 必读 `docs/api-conventions.md`
```

这样 cc 只在"需要的时候"才去读完整文档，既保证了准确性，又不占多余上下文。

---

### 8.5 .claudeignore 文件

类似于 `.gitignore`，用来告诉 Claude Code 哪些文件/目录不需要关注。

**与 .gitignore 的核心区别：**

| 特性   | .gitignore        | .claudeignore           |
| ---- | ----------------- | ----------------------- |
| 控制谁  | git add/commit    | Claude Code 文件读取        |
| 默认忽略 | 无                 | `node_modules/`、`.git/` |
| 语法   | gitignore 风格 glob | 相同语法                    |
| 互相影响 | 不                 | 不                       |

**什么时候一定要配：**

| 情况 | 不配的后果 | 推荐规则 |
|------|-----------|---------|
| 有 `node_modules/` | cc 遍历巨量依赖文件，token 暴涨 | `node_modules/` |
| 有 `dist/`、`build/`、`.next/` | 构建产物干扰 cc 理解源码 | `dist/` `.next/` `build/` |
| 有 `.env` 等敏感文件 | 可能被 cc 读取并意外展示 | `.env` `.env.*` |
| 有大文件（如 `.pkl`、`.onnx`） | 尝试读取时超时或浪费 token | `*.pkl` `*.onnx` |

**实用模板：**

```gitignore
# === 依赖 ===
node_modules/
.pnp/
.pnp.js

# === 构建产物 ===
dist/
build/
.next/
out/
.cache/
.turbo/

# === 环境与密钥 ===
.env
.env.*
*.pem
*.key

# === 大文件 ===
*.onnx
*.pkl
*.bin
*.pt

# === 自动生成 ===
generated/
coverage/
.nyc_output/

# === 日志 ===
*.log
npm-debug.log*
```

**最佳实践：**

- 把 `.claudeignore` 提交到 Git，团队共享
- 只影响 cc 的**文件探索**，不影响你通过 `Read` 工具明确要求读取的文件

---

### 8.6 settings.json 记忆相关配置

```json
{
  // 排除某些 CLAUDE.md 不被加载（monorepo 场景）
  "claudeMdExcludes": [
    "packages/legacy-app/CLAUDE.md",
    "vendors/**/CLAUDE.md"
  ],

  // 自定义 Auto Memory 目录
  "autoMemoryDirectory": "/path/to/custom/memory",

  // 显式加载指定规则文件
  "rules": [
    "~/.claude/rules/security.md",
    ".claude/rules/api-design.md"
  ]
}
```

**环境变量控制 Auto Memory：**

| 变量 | 值 | 行为 |
|------|----|------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `0` | 强制开启 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `1` | 强制关闭 |
| （未设置） | — | 默认启用 |

```bash
# 禁用 Auto Memory
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude

# 强制启用
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0 claude
```

> settings.json 完整配置详解 → [[settings.json 配置详解]]

---

## 九、关联文档

[[Agent智能体]] · [[Claude Code 常用功能]] · [[Claude Code CLI 完整参考]] · [[Claude Code 会话管理]] · [[Claude Code 模型与推理设置]] · [[Claude MCP 使用指南]] · [[CLAUDE.md 使用指南]] · [[Subagents 完整指南]] · [[如何编写Skills]] · [[Skills 是什么]] · [[人工智能重要的六大概念体系]] · [[Git 入门教程]] · [[Git 命令速查]]

---

## 参考资料

### 官方
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [What's New - 官方更新日志](https://code.claude.com/docs/en/whats-new)
- [Changelog](https://code.claude.com/docs/en/changelog)
- [GitHub 仓库](https://github.com/anthropics/claude-code)
- [Auto Mode 官方博客](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Subagents 官方博客](https://claude.com/blog/subagents-in-claude-code)
- [定制 Claude Code 官方博客](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

### 社区
- [claude-howto 学习指南](https://github.com/luongnv89/claude-howto)（41,000+ ⭐）
- [安装指南](https://www.morphllm.com/install-claude-code)
- [第三方 API 免登录配置](https://www.xugj520.cn/archives/windows-claude-code-api-setup-no-login.html)

### 跳过认证
- [CC-Switch（可视化供应商切换）](https://github.com/farion1231/cc-switch)
- [settings.json 详解](https://blog.csdn.net/tirestay/article/details/158808038)

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-07-31 | 新增「国内网络安装」专题（0️⃣）：代理+官方安装器 / npm+npmmirror 镜像 / Homebrew / GitHub 加速 + 需放行域名表；纠正 npm「已废弃」为「官方仍支持」；Node.js 要求 v18+ → v22+（v2.1.198 起）；版本号更新至 v2.1.220；新增 npm 安装「native binary not installed」FAQ |
| 2026-07-31 | 新增 FAQ「npm 安装被 allow-scripts 拦截（postinstall 未执行）」：npm 11.16+ allowScripts 策略、全局安装放行用 `--allow-scripts=<pkg>` / `allow-scripts=<pkg>`；方案 B 增加交叉引用 |
| 2026-08-03 | 更新「跳过登录（免认证启动）」章节：新增官方 6 层认证优先级表、`hasCompletedOnboarding` 免首启引导、`claude setup-token` CI 长期 token；primaryApiKey 标记为旧方案已不可靠（官方已不列，v2.0.37+ 失效）；apiKeyHelper 补充 TTL / 失败报错 / 适用面；env 字段补充 `ANTHROPIC_BASE_URL` 副作用；CC-Switch 更新至 124K+ Star / v3.16.1 / 8 工具 |
| 2026-08-07 | 修正「三、配置文件」：`providers` / `defaultProvider` 为非官方写法、会被静默忽略，改为官方 `env`（`ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_MODEL`）方案；多平台切换改为 `--settings` 多文件 / CC-Switch / LiteLLM；版本号更新至 latest v2.1.224 / stable v2.1.220 |
| 2026-08-10 | 同步 2026-08 现状：默认模型 Claude Sonnet 5（原生 1M 上下文，促销 $2/$10 每 Mtok 至 2026-08-31）、默认 Opus 5；权限模式 Default 改名 Manual（`--permission-mode manual` / `"defaultMode": "manual"`）；补充 `/doctor`（= `/checkup`）、`/fork`（复制到新后台会话）、`/subtask`；`/review` 改为 `/code-review` 别名且不再自动运行；版本号更新至 v2.1.226 |
| 2026-09-04 | 更新「国内网络安装（重点）」：核实 npm 渠道仍官方同步发布（latest v2.1.260）、npmmirror 同步主包与平台子包；GitHub Releases 已附二进制与 `SHASUMS256.txt`；补充「安装 vs 运行」放行域名说明；刷新版本号/star 数（claude-howto 41K、CC-Switch v3.20.1 / 131K） |
| 2026-09-04 | 扩充「3️⃣ 前置依赖」：新增 Git / Node.js 分步安装说明（Windows / macOS / Linux 命令、国内镜像、验证命令、git 全局配置、npm 镜像切换交叉引用） |
