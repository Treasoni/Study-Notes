---
tags: [ai, 工具使用]
---

# Claude Code 使用指南

> [!info] 文档定位
> **本文档是完整安装配置指南** - 包含安装、配置、代理设置、MCP/Skills 配置等完整流程。功能速查请参阅 [[Claude Code 常用功能]]，CLI 命令参考请参阅 [[Claude Code CLI 完整参考]]

> [!info] 概述
> **Claude Code 是开发者的 CLI AI 助手** - 在终端中直接使用 Claude 进行软件工程任务。支持文件操作、代码编辑、Git 管理等功能，兼容多种 AI 平台。
>
> **学习路径**: [Claude How To - 完整学习指南](https://github.com/luongnv89/claude-howto) | [学习路线图](https://github.com/luongnv89/claude-howto/blob/main/LEARNING-ROADMAP.md)

## 快速导航 - Claude Code 功能全景

| 功能 | 描述 | 快速启动 | 难度 | 时间 |
|------|------|----------|------|------|
| **Slash Commands** | 用户调用的快捷命令 | `cp 01-slash-commands/*.md .claude/commands/` | 初级 | 30 min |
| **Memory** | 持久化上下文 | `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` | 初级+ | 45 min |
| **Checkpoints** | 会话快照与回滚 | 自动启用，按 `Esc+Esc` 使用 | 中级 | 45 min |
| **Skills** | 可复用的能力包 | `cp -r 03-skills/code-review ~/.claude/skills/` | 中级 | 1 hour |
| **Hooks** | 事件驱动的自动化 | `cp 06-hooks/*.sh ~/.claude/hooks/` | 中级 | 1 hour |
| **MCP** | 外部工具访问 | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` | 中级+ | 1 hour |
| **Subagents** | 专业化 AI 助手 | `cp 04-subagents/*.md .claude/agents/` | 中级+ | 1.5 hours |
| **Advanced Features** | 规划模式、后台任务等 | 配置 `settings.json` | 高级 | 2-3 hours |
| **Plugins** | 功能捆绑包 | `/plugin install pr-review` | 高级 | 2 hours |

> [!info] 📚 来源
> - [Claude How To - GitHub](https://github.com/luongnv89/claude-howto) - 21,800+ stars 的完整学习指南
> - [Feature Catalog](https://github.com/luongnv89/claude-howto/blob/main/CATALOG.md) - 功能完整目录

## 核心概念 💡

### 什么是 Claude Code

**是什么**：Anthropic 官方的 CLI 工具，让你在终端中直接使用 Claude

**为什么需要**：
- 无需离开终端即可使用 AI
- 直接操作文件和代码
- 智能 Git 集成
- 支持 MCP 和 Skills 扩展

**平台支持**：

| 平台 | baseUrl | defaultModel |
|------|---------|--------------|
| 火山引擎 | `https://ark.cn-beijing.volces.com/v1` | `ep-xxxxx` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-plus` |
| Ollama | `http://localhost:11434/v1` | `llama3.2` |

## 操作步骤

### 步骤 1：安装

> [!note] 版本信息
> **当前版本**: v2.1.131 (2026-05-06) - 从 v2.1.113 开始，Claude Code 以原生二进制文件发布（macOS/Linux/Windows）。**npm 安装方式已官方废弃**，推荐使用原生安装器。

#### 15 分钟快速开始

```bash
# 1. 克隆学习指南仓库（可选，推荐）
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# 2. 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 3. 复制第一个 Slash Command
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 4. 启动并尝试
cd /path/to/your-project
claude
# 然后输入: /optimize

# 5. 设置项目记忆（推荐）
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md
```

#### 前置要求

在安装 Claude Code 之前，请确保你的系统满足以下条件：

| 要求          | 说明                                                |
| ----------- | ------------------------------------------------- |
| **Node.js** | 仅 `npm` 安装方式需要 v18+（原生安装器无需 Node.js）                 |
| **npm**     | 仅 `npm` 安装方式需要（已废弃）                                   |
| **Git**     | 版本控制系统，Claude Code 的版本控制功能依赖于此                      |
| **RAM**     | 最低 4GB，推荐 8GB                                          |
| **终端**      | macOS Terminal / Windows PowerShell / Linux Shell |

> [!tip] 检查版本
> ```bash
> node --version  # 应显示 v18.x.x 或更高
> npm --version   # 检查 npm 是否可用
> git --version   # 检查 Git 是否可用
> ```

#### 安装 Git 并配置环境变量

> [!tip] 安装时自动配置（推荐）
> Windows 安装程序在 **"Adjusting your PATH environment"** 步骤中，选择：
> **"Git from the command line and also from 3rd-party software"**（中间选项）
>
> 这样会自动将 Git 添加到 PATH，无需手动配置！

> [!info] 手动配置环境变量（仅当安装时未选择正确选项）
> **环境变量名**：`Path`（系统变量）
>
> **需要添加的路径**：
> 
> | 路径 | 说明 |
> |------|------|
> | `C:\Program Files\Git\cmd` | Git 命令（主要，优先添加） |
> | `C:\Program Files\Git\bin` | Git 核心程序（可选） |
>
> **配置方法**：
> 1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
> 2. 在"系统变量"中找到 `Path`，点击编辑
> 3. 新建，添加上述路径
> 4. **重启终端**（关闭 PowerShell/CMD 重新打开）

**各平台安装命令**：

```bash
# macOS
brew install git

# Windows (winget)
winget install Git.Git

# Windows (Chocolatey)
choco install git

# Linux (Ubuntu/Debian)
sudo apt-get install -y git

# Linux (CentOS/RHEL)
sudo yum install -y git
```

> [!warning] 安装后必做
> 配置 Git 用户信息（用于提交记录）：
> ```bash
> git config --global user.name "你的名字"
> git config --global user.email "你的邮箱@example.com"
> ```

> [!quote] 参考资料
> - [Git 官方文档 - Installing on Windows](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
> - [Git for Windows 官网](https://gitforwindows.org/)

#### 安装 Node.js 和 npm

如果你还没有安装 Node.js，请根据你的操作系统选择以下方式：

**macOS**

```bash
# 方式一：使用 Homebrew（推荐）
brew install node

# 方式二：使用 nvm（Node Version Manager，可管理多版本）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc  # 或 source ~/.bashrc
nvm install --lts  # 安装 LTS 版本
nvm use --lts

# 验证安装
node --version
npm --version
```

**Windows**

```powershell
# 方式一：使用 winget（推荐）
winget install OpenJS.NodeJS.LTS

# 方式二：使用 Chocolatey
choco install nodejs-lts

# 方式三：使用安装程序
# 1. 访问 https://nodejs.org/
# 2. 下载 LTS 版本安装程序
# 3. 运行安装程序，按提示完成安装

# 验证安装（PowerShell）
node --version
npm --version
```

**Linux（Ubuntu/Debian）**

```bash
# 方式一：使用 NodeSource 仓库（推荐）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方式二：使用 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts

# 验证安装
node --version
npm --version
```

**Linux（CentOS/RHEL/Fedora）**

```bash
# 使用 NodeSource 仓库
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs  # CentOS/RHEL
# 或
sudo dnf install -y nodejs  # Fedora

# 验证安装
node --version
npm --version
```

> [!tip] 推荐使用 nvm
> nvm（Node Version Manager）允许你在同一台机器上安装和切换多个 Node.js 版本，非常适合开发者使用。

#### 安装方式

**方式一：原生安装器（推荐，跨平台）**

macOS/Linux：

```bash
# 推荐方式：自动安装脚本
curl -fsSL https://claude.ai/install.sh | bash

# 验证安装
claude --version
```

Windows（PowerShell，推荐）：

```powershell
# 推荐方式：自动安装脚本
irm https://claude.ai/install.ps1 | iex

# 验证安装
claude --version
```

Windows（CMD）：

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> [!tip] 原生安装器优势
> - 自动更新（可通过 `DISABLE_AUTOUPDATER=1` 在 settings.json 中禁用）
> - 无需 Node.js 环境
> - 各平台独立二进制文件，体积约 60-80MB

> [!info] 📚 来源
> - [GitHub 官方仓库 - Installation](https://github.com/anthropics/claude-code)

**方式二：Homebrew（macOS 推荐）**

```bash
# 1. 确保已安装 Homebrew
# 如未安装，运行：
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装 Claude Code
brew install --cask claude-code

# 3. 验证安装
claude --version
```

> [!tip] Homebrew 注意
> 需要手动更新：`brew upgrade claude-code`

> [!info] 📚 来源
> - [Homebrew 官方 Cask](https://github.com/Homebrew/homebrew-cask)

**方式三：WinGet（Windows 推荐）**

```powershell
# 使用 WinGet 安装
winget install Anthropic.ClaudeCode

# 验证安装
claude --version
```

> [!tip] WinGet 注意
> 需要手动更新：`winget upgrade Anthropic.ClaudeCode`

**方式四：npm（已废弃）**

```bash
# 全局安装（不推荐，官方已废弃此方式）
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

> [!warning] npm 方式已废弃
> v2.1.113+ 开始，官方已逐步废弃 npm 安装方式。新用户请使用原生安装器。npm 安装不会自动更新。

**方式五：从源码安装**

```bash
# 克隆仓库
git clone https://github.com/anthropics/claude-code.git
cd claude-code

# 安装依赖并构建
npm install
npm run build

# 全局链接
npm link
```

#### 首次启动与认证

```bash
# 启动 Claude Code
claude

# 首次启动会提示登录认证
# 选择认证方式：
#   1. 浏览器登录 - 自动打开浏览器完成授权
#   2. API Key - 直接输入 Anthropic API Key
```

> [!warning] 认证注意
> - 浏览器登录会在本地生成认证令牌
> - API Key 方式需要有效的 Anthropic 账户和订阅

#### 跳过登录与无需认证

Claude Code **没有** `--no-auth` 参数，但提供以下 4 种方式跳过 OAuth 登录：

**方式一：apiKeyHelper（官方推荐）**

创建一个脚本文件输出你的 API Key，然后在 settings.json 中引用：

```bash
# 1. 创建 API Key 辅助脚本
cat > ~/.claude/api-key-helper.sh << 'EOF'
#!/bin/bash
echo "sk-ant-你的API密钥"
EOF
chmod +x ~/.claude/api-key-helper.sh

# 2. 配置 settings.json
```

```json
{
  "apiKeyHelper": "/Users/你的用户名/.claude/api-key-helper.sh"
}
```

> [!tip] 注意
> - **不要**同时设置 `ANTHROPIC_API_KEY` 环境变量，否则会出现认证冲突警告
> - 确保 `~/.claude.json` 中没有 `oauthAccount` 条目（如有则删除）

**方式二：primaryApiKey（配置方式）**

在 `~/.claude/settings.json` 中直接配置 API Key：

```json
{
  "primaryApiKey": "sk-ant-你的API密钥",
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

> [!tip] permissions 可选值
> - `"bypassPermissions"` — YOLO 模式，自动批准所有操作
> - `"acceptEdits"` — 仅自动批准文件编辑
> - `"default"` — 每次操作都询问（默认）

**方式三：环境变量（第三方 API）**

```bash
# 使用第三方 API（如 OpenRouter、本地模型等）
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-你的密钥"
export ANTHROPIC_MODEL="anthropic/claude-3.5-sonnet"
export ANTHROPIC_API_KEY=""  # 留空

claude
```

离线使用本地模型（通过 LiteLLM 桥接 Ollama）：

```bash
# 1. 安装 Ollama 并拉取模型
ollama pull qwen2.5-coder:7b

# 2. 启动 LiteLLM 桥接
litellm --model ollama/qwen2.5-coder:7b --port 8000

# 3. 设置环境变量启动 Claude Code
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_AUTH_TOKEN="sk-123"
export ANTHROPIC_API_KEY=""
claude
```

> [!warning] 协议兼容性
> - Claude Code 使用 Anthropic `/v1/messages` 协议（与 OpenAI `/v1/chat/completions` 不同）
> - OpenRouter：原生支持 Anthropic 协议 ✅
> - LiteLLM：自动协议转换 ✅
> - Ollama 直连：不支持 ❌（必须通过 LiteLLM 桥接）
> - 模型**必须支持 Tool Use / Function Calling**

**方式四：Desktop Developer Mode（GUI 方式，2026 年 4 月新增）**

如果使用 Claude Code Desktop：
1. 菜单 → HELP → Troubleshooting → **Enable Developer Mode**
2. 重启应用
3. Developer → Configure Third-Party Inference
4. 填写 Gateway URL + API Key

> [!info] 特性
> - 完全跳过 Claude 账户登录
> - 可视化配置第三方推理端点
> - 支持 Ollama、OpenRouter 等 OpenAI 兼容后端

> [!info] 📚 来源
> - [apiKeyHelper - GitHub Issue #362](https://github.com/lbjlaq/Antigravity-Manager/issues/362)
> - [Desktop Developer Mode - 阿里云开发者](https://developer.aliyun.com/article/1731254)
> - [settings.json 绕过登录 - CSDN](https://blog.csdn.net/tirestay/article/details/158808038)
> - [第三方 API / 本地模型配置](https://www.xugj520.cn/archives/windows-claude-code-api-setup-no-login.html)

> [!warning] 企业代理注意
> v2.1.116+ 版本从 `https://downloads.claude.ai/claude-code-releases` 下载二进制文件，企业代理需要将此域名加入白名单。

#### 安装验证

```bash
# 检查版本
claude --version

# 查看帮助
claude --help

# 启动并测试
claude
> 你好，请告诉我你是什么
```

#### 常见安装问题

| 问题 | 解决方案 |
|------|---------|
| `command not found: claude` | 确认 npm 全局路径在 PATH 中 |
| `EACCES permission denied` | 使用 `sudo npm install -g` 或修复 npm 权限 |
| Node.js 版本过低 | 升级到 Node.js 18+ |
| Homebrew 安装慢 | 尝试切换镜像源或使用 npm 方式 |

> [!tip] Windows 用户注意
> 推荐使用 PowerShell 运行安装命令。如果遇到权限问题，可能需要以管理员身份运行。

### 步骤 2：配置

这里主要是配置你的大模型相关的信息

#### 方式一：环境变量（临时）

```bash
export ANTHROPIC_BASE_URL="平台API地址"
export ANTHROPIC_API_KEY="你的API Key"
claude
```

#### 方式二：配置文件（永久）

**配置文件位置**：`~/.claude/settings.json`

```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-xxx",
      "defaultModel": "deepseek-chat"
    }
  },
  "defaultProvider": "deepseek"
}
```

> [!info] 配置级别
> MCP 支持三种配置级别：项目级 `.mcp.json`、全局级 `~/.claude/claude_desktop_config.json`、插件级。详见 [[03-进阶应用/Claude MCP 使用指南]]

**配置优先级**：环境变量 > 配置文件

### 步骤 3：模型切换

> [!tip] 详细说明
> 更多模型选项、推理参数配置和第三方平台设置，请参阅 [[Claude Code 模型与推理设置]]

#### 启动时指定模型

```bash
# 使用 --model 参数（推荐）
claude --model claude-sonnet-4

# 或使用 -m 简写
claude -m claude-opus-4

# 指定第三方平台模型（需先配置 provider）
claude --model deepseek-chat
```

#### 会话中切换模型

```bash
# 交互式切换（列出可用模型供选择）
/model

# 直接切换到指定模型
/model claude-opus-4

# 切换到第三方模型
/model deepseek-chat

# 查看当前使用的模型
/status
```

### 步骤 4：配置 MCP

```bash
# 添加文件系统 MCP
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path

# 查看 MCP 列表
/mcp

# 删除 MCP
claude mcp remove filesystem
```

> [!tip] 详细说明
> 完整的 MCP 配置和使用教程请参阅 [[03-进阶应用/Claude MCP 使用指南]]

### 步骤 5：使用 Skills

```bash
# 查看可用技能
/help

# 使用斜杠命令
/commit
/review-pr 123

# 自然语言触发
"帮我画一个流程图"
```

> [!tip] 详细说明
> - 了解 Skills 概念：[[01-基础概念/Skills 是什么]]
> - 学习编写自定义 Skills：[[03-进阶应用/如何编写Skills]]

### 步骤 6：会话管理

```bash
# 创建新会话
/new                      # 创建全新会话
/new my-project           # 创建命名会话

# 管理会话
/resume                   # 列出所有历史会话
/resume my-session        # 恢复特定会话
/clear                    # 清除当前会话历史

# 查看状态
/status                   # 查看当前会话状态
/context                  # 显示 token 消耗
```

> [!tip] 详细说明
> 更多会话管理技巧请参阅 [[02-工具使用/Claude Code 会话管理]]

### 步骤 7：使用 CLAUDE.md

**什么是 CLAUDE.md**：
- 项目级配置文件
- Claude Code 启动时自动读取
- 定义项目规范、工作流程、禁止事项

**文件位置与优先级**：

| 文件 | 位置 | 作用域 | 提交到 Git |
|------|------|--------|------------|
| `CLAUDE.md` | 项目根目录 | 项目级 | ✅ 是 |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | ❌ 否 |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | ❌ 否 |

**快速开始**：
```bash
# 方式一：自动生成（推荐）
claude
/init  # 分析代码库并生成 CLAUDE.md

# 方式二：手动创建
# 在项目根目录创建 CLAUDE.md 文件
```

**最小模板**：
```markdown
# CLAUDE.md

## 项目概述
一句话描述项目功能

## 目录结构
- /src - 源代码
- /tests - 测试文件

## 常用命令
- npm install - 安装依赖
- npm run dev - 启动开发
- npm test - 运行测试

## 代码规范
- 使用 ESLint + Prettier
- 组件命名 PascalCase

## 禁止事项
- 不要修改 package-lock.json
- 不要使用 any 类型

## 完成标准
- 测试通过
- 代码检查通过
```

> [!tip] 详细说明
> 完整的 CLAUDE.md 编写指南请参阅 [[03-进阶应用/CLAUDE.md 使用指南]]

### 步骤 8：配置代理

如果需要通过代理访问 Claude API，可以使用以下几种方式配置。

#### 方式一：环境变量（临时）

**macOS/Linux:**
```bash
# 临时设置（当前终端会话有效）
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# 启动 Claude Code
claude
```

**Windows (PowerShell):**
```powershell
# 临时设置
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"

# 启动 Claude Code
claude
```

**Windows (CMD):**
```cmd
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
claude
```

#### 方式二：写入配置文件（永久）

**macOS/Linux:**
```bash
# 写入 ~/.zshrc (Zsh) 或 ~/.bashrc (Bash)
echo 'export HTTP_PROXY="http://127.0.0.1:7890"' >> ~/.zshrc
echo 'export HTTPS_PROXY="http://127.0.0.1:7890"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

**Windows:**
```powershell
# 设置用户级环境变量（永久生效）
[System.Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://127.0.0.1:7890", "User")
[System.Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://127.0.0.1:7890", "User")

# 或通过系统设置：系统属性 -> 环境变量 -> 新建
# 变量名: HTTP_PROXY / HTTPS_PROXY
# 变量值: http://127.0.0.1:7890
```

#### 方式三：集成到启动命令

**macOS/Linux (alias 方式):**
```bash
# 添加到 ~/.zshrc
alias claude-proxy='HTTP_PROXY="http://127.0.0.1:7890" HTTPS_PROXY="http://127.0.0.1:7890" claude'

# 使用
claude-proxy
```

**Windows (PowerShell 函数):**
```powershell
# 添加到 $PROFILE
function Start-ClaudeProxy {
    $env:HTTP_PROXY = "http://127.0.0.1:7890"
    $env:HTTPS_PROXY = "http://127.0.0.1:7890"
    claude
}

# 使用
Start-ClaudeProxy
```

#### 方式四：VS Code 插件配置

在 VS Code 设置 (`settings.json`) 中：
```json
{
  "claudeCode.environmentVariables": [
    {
      "name": "HTTP_PROXY",
      "value": "http://127.0.0.1:7890"
    },
    {
      "name": "HTTPS_PROXY",
      "value": "http://127.0.0.1:7890"
    }
  ]
}
```

#### 方式五：通过 settings.json 配置（推荐）

在 `~/.claude/settings.json` 中添加 `env` 字段：

```json
{
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

**完整配置示例**（包含 API 配置）：
```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-xxx",
      "defaultModel": "deepseek-chat"
    }
  },
  "defaultProvider": "deepseek",
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

**取消代理**：
```json
{
  "env": {
    "HTTP_PROXY": "",
    "HTTPS_PROXY": ""
  }
}
```

> [!tip] 配置优先级
> `env` 字段中的代理设置会被终端环境变量覆盖。如果需要临时使用不同代理，仍可通过环境变量方式。

## 注意事项 ⚠️

### 常见错误

**配置不生效**：
- ❌ 配置文件路径错误
- ❌ JSON 格式不正确
- ❌ 环境变量覆盖配置

**MCP 连接失败**：
- ❌ npx 未安装
- ❌ 服务器命令错误
- ❌ 环境变量未设置

**模型切换失败**：
- ❌ 模型名称不正确
- ❌ 平台不支持该模型
- ❌ API Key 无效

### 关键配置点

**使用 alias 快捷切换**：
```bash
# 添加到 ~/.zshrc
alias claude-volc='ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/v1" ANTHROPIC_API_KEY="xxx" claude'
alias claude-ds='ANTHROPIC_BASE_URL="https://api.deepseek.com" ANTHROPIC_API_KEY="xxx" claude'

# 使用
claude-volc  # 火山引擎
claude-ds    # DeepSeek
```

**环境变量管理**：
```bash
# 临时设置
export API_TOKEN="xxx"

# .env 文件
echo "API_TOKEN=xxx" >> .env
source .env

# 永久设置
echo 'export API_TOKEN="xxx"' >> ~/.bashrc
```

**代理配置管理**：
```bash
# 临时设置代理
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

# 取消代理
unset HTTP_PROXY HTTPS_PROXY

# 验证代理是否生效
echo $HTTP_PROXY
```

**常用代理端口**：
| 软件 | 默认端口 |
|------|---------|
| Clash | 7890 |
| V2Ray | 10808 |
| Shadowsocks | 1080 |

**安全建议**：
```bash
# .gitignore
.env
.mcp.json
settings.json
```

## 常用命令

### 启动命令

| 命令 | 功能 |
|------|------|
| `claude` | 默认启动 |
| `-m <模型>` | 指定模型 |
| `--version` | 查看版本 |
| `--help` | 查看帮助 |

### MCP 管理

| 命令 | 功能 |
|------|------|
| `claude mcp add` | 添加服务器 |
| `claude mcp list` | 列出已安装 |
| `claude mcp remove` | 删除服务器 |
| `claude mcp enable` | 启用服务器 |
| `claude mcp disable` | 禁用服务器 |

### Slash 命令

| 命令 | 功能 |
|------|------|
| `/help` | 帮助信息 |
| `/commit` | 创建提交 |
| `/plan` | 规划模式 |
| `/tasks` | 任务列表 |
| `/remember` | 记住信息 |

## 常见问题 ❓

**Q: 如何快速切换不同平台？**

A: 推荐使用 alias 方式：
```bash
alias claude-ds='ANTHROPIC_BASE_URL="https://api.deepseek.com" ANTHROPIC_API_KEY="xxx" claude'
alias claude-qwen='ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1" ANTHROPIC_API_KEY="xxx" claude'
```

**Q: 配置文件不生效怎么办？**

A: 检查：
1. 配置文件路径是否正确
2. JSON 格式是否正确
3. 是否有环境变量覆盖
4. 重启 Claude Code

**Q: 如何查看当前使用的模型？**

A: 在会话中询问："我当前使用的是什么模型？"

**Q: MCP 和 Skills 有什么区别？**

A:
- **MCP**：提供工具能力（如文件访问、数据库查询）- 详见 [[Claude MCP 使用指南]]
- **Skills**：预定义任务模板（如代码提交、PR 审查）- 详见 [[Skills 是什么]]
- Skills 可以调用 MCP 提供的工具

> [!info] 深入理解
> 想了解 Prompt、Agent、MCP 的关系，请参阅 [[01-基础概念/人工智能重要的六大概念体系]]

**Q: 如何调试 MCP 配置？**

A:
```bash
# 调试模式启动
claude --debug

# 查看状态
/mcp

# 手动测试
npx -y @modelcontextprotocol/server-filesystem /test/path
```

> [!tip] Subagent 调试
> 如果需要调试 Agent 相关问题，请参阅 [[02-工具使用/Claude Code Subagents 完整指南]]

**Q: Claude Code 无法连接网络怎么办？**

A: 检查以下几点：
1. 确认代理软件已启动，端口正确（如 7890、1080 等）
2. 确认终端代理环境变量已设置：`echo $HTTP_PROXY`
3. 测试终端网络：`curl -I https://www.google.com`
4. 检查是否需要认证代理

**Q: 只设置了系统代理，为什么终端还是连不上？**

A: 系统代理通常只对浏览器生效，命令行程序需要单独设置 `HTTP_PROXY` 和 `HTTPS_PROXY` 环境变量。

**Q: 如何临时取消代理？**

A:
```bash
# macOS/Linux
unset HTTP_PROXY HTTPS_PROXY

# Windows PowerShell
Remove-Item Env:HTTP_PROXY
Remove-Item Env:HTTPS_PROXY
```

**Q: 代理配置后速度很慢怎么办？**

A: 可能原因：
1. 代理节点不稳定 - 尝试切换节点
2. 网络质量差 - 检查网络连接
3. 代理软件设置问题 - 调整代理规则

**Q: settings.json 中的代理配置不生效？**

A: 可能原因：
1. JSON 格式错误 - 检查是否有尾随逗号或语法错误
2. 环境变量优先级更高 - 终端中的 `HTTP_PROXY` 会覆盖配置文件
3. 配置文件路径错误 - 确认是 `~/.claude/settings.json`
4. 未重启 Claude Code - 修改后需要重启才生效

**Q: settings.json 和环境变量方式哪个更好？**

A:
- **settings.json**：适合长期固定的代理配置，一次设置永久生效
- **环境变量**：适合临时切换或需要频繁更改代理的场景

## 相关文档
[[02-工具使用/Claude Code 常用功能]] | [[03-进阶应用/Claude MCP 使用指南]] | [[02-工具使用/Claude Code 会话管理]] | [[02-工具使用/Claude Code 模型与推理设置]] | [[01-基础概念/Skills 是什么]] | [[03-进阶应用/如何编写Skills]] | [[02-工具使用/Claude Code Subagents 完整指南]] | [[01-基础概念/人工智能重要的六大概念体系]] | [[03-进阶应用/CLAUDE.md 使用指南]] | [[../../Git/Git 入门教程]] | [[../../Git/Git 命令速查]]

## 参考资料

### 官方资源
- [Claude Code Official Documentation](https://code.claude.com/docs/en/overview) - 官方技术文档
- [Anthropics Claude Code GitHub](https://github.com/anthropics/claude-code) - 官方仓库
  - [GitHub Releases](https://github.com/anthropics/claude-code/releases) - 版本发布与更新日志
- [Claude Code Auto Mode - Anthropic Engineering Blog](https://www.anthropic.com/engineering/claude-code-auto-mode) - 自动权限模式官方说明

### 社区资源（强烈推荐）
- [claude-howto GitHub Repository](https://github.com/luongnv89/claude-howto) - 21,800+ stars 完整学习指南
  - [学习路线图](https://github.com/luongnv89/claude-howto/blob/main/LEARNING-ROADMAP.md) - 10 模块渐进式学习路径
  - [功能目录](https://github.com/luongnv89/claude-howto/blob/main/CATALOG.md) - 所有功能快速参考
  - [10 个教程模块](https://github.com/luongnv89/claude-howto) - 从入门到高级的完整教程
- [Boris Cherny's Workflow](https://x.com/bcherny/status/2007179832300581177) - Claude Code 创建者分享的系统化工作流

### 安装与配置
- [How to Install Claude Code (2026) - morphllm.com](https://www.morphllm.com/install-claude-code) - 全平台安装指南
- [第三方 API / 本地模型配置指南](https://www.xugj520.cn/archives/windows-claude-code-api-setup-no-login.html) - 无需登录配置方法

### 跳过认证
- [apiKeyHelper - Antigravity-Manager Issue #362](https://github.com/lbjlaq/Antigravity-Manager/issues/362) - 官方 apiKeyHelper 使用方法
- [Desktop Developer Mode 配置](https://developer.aliyun.com/article/1731254) - 绕过登录使用第三方模型
- [Windows Claude Code API 免登录配置 - CSDN](https://blog.csdn.net/tirestay/article/details/158808038) - settings.json 配置详解
