---
tags: [ai]
---

# Claude Code 使用指南

> [!info] 文档定位
> **本文档是完整安装配置指南** - 包含安装、配置、代理设置、MCP/Skills 配置等完整流程。功能速查请参阅 [[Claude Code 常用功能]]

> [!info] 概述
> **Claude Code 是开发者的 CLI AI 助手** - 在终端中直接使用 Claude 进行软件工程任务。支持文件操作、代码编辑、Git 管理等功能，兼容多种 AI 平台。

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

```bash
# macOS (Homebrew)
brew install claude-code

# npm
npm install -g @anthropic-ai/claude-code

# 首次启动
claude
```

### 步骤 2：配置

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
> MCP 支持三种配置级别：项目级 `.mcp.json`、全局级 `~/.claude/claude_desktop_config.json`、插件级。详见 [[Claude MCP 使用指南]]

**配置优先级**：环境变量 > 配置文件

### 步骤 3：模型切换

```bash
# 启动时指定
claude -m deepseek-chat

# 会话中切换
"使用 deepseek-chat 模型"
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
> 完整的 MCP 配置和使用教程请参阅 [[Claude MCP 使用指南]]

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
> - 了解 Skills 概念：[[Skills 是什么]]
> - 学习编写自定义 Skills：[[如何编写Skills]]

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
> 更多会话管理技巧请参阅 [[Claude Code 会话管理]]

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
> 完整的 CLAUDE.md 编写指南请参阅 [[CLAUDE.md 使用指南]]

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
> 想了解 Prompt、Agent、MCP 的关系，请参阅 [[Prompt, Agent, MCP 是什么]]

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
> 如果需要调试 Agent 相关问题，请参阅 [[Claude Subagent 使用指南]]

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
[[Claude Code 常用功能]] | [[Claude MCP 使用指南]] | [[Claude Code 会话管理]] | [[Skills 是什么]] | [[如何编写Skills]] | [[Claude Subagent 使用指南]] | [[Prompt, Agent, MCP 是什么]] | [[CLAUDE.md 使用指南]]
