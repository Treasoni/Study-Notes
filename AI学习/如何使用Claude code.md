---
tags: [ai]
---

# Claude Code 使用指南

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
- **MCP**：提供工具能力（如文件访问、数据库查询）
- **Skills**：预定义任务模板（如代码提交、PR 审查）
- Skills 可以调用 MCP 提供的工具

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

## 相关文档
[[Claude Code 常用功能]] | [[Claude MCP 使用指南]] | [[Skills 是什么]]
