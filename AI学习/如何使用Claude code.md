---
tags:
  - ai
  - claude-code
  - 开发工具
---
# 如何使用 Claude Code

## 1. 下载和安装

### 官方下载链接
```http
https://code.claude.com/docs/zh-CN/quickstart
```

### 基本安装

根据你的操作系统选择对应的安装命令：

**macOS (Homebrew)**:
```bash
brew install claude-code
```

**npm**:
```bash
npm install -g @anthropic-ai/claude-code
```

### 首次启动

```shell
claude
# 首次使用时系统会提示您登录
```

> [!NOTE]
> 如果你有 Claude 官方账号可以直接使用。如果你没有账号，可以按照下面的配置方法使用其他兼容平台的 API。

---

## 2. 平台配置

Claude Code 支持使用兼容 OpenAI API 格式的多种平台，如火山引擎、通义千问、智谱 AI、DeepSeek 等。

配置方式有两种：
1.  **使用环境变量配置**-临时配置，适合快速测试
2. **配置文件配置** - 永久配置，适合长期使用

### 2.1 使用环境变量配置

> [!INFO] 适用场景
> - 快速测试不同平台
> - 临时切换 API
> - 不想修改配置文件

#### 配置方法

在终端中设置环境变量：

**macOS/Linux**:
```bash
export ANTHROPIC_BASE_URL="平台API地址"
export ANTHROPIC_API_KEY="你的API Key"
```

#### 各平台配置示例

**火山引擎（字节跳动）**:
```bash
export ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/v1"
export ANTHROPIC_API_KEY="你的火山引擎API Key"
```

**通义千问（阿里）** - 使用 OpenAI 兼容接口:
```bash
export ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export ANTHROPIC_API_KEY="sk-你的通义千问API Key"
```

**DeepSeek**:
```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com"
export ANTHROPIC_API_KEY="sk-你的DeepSeek API Key"
```

**智谱 AI（GLM）** - 使用兼容接口:
```bash
export ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export ANTHROPIC_API_KEY="你的智谱API Key"
```

**Ollama（本地模型）**:
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434/v1"
export ANTHROPIC_API_KEY="ollama"  # 可以是任意值
```

#### 使用 alias 方式（可选）

```bash
# 创建快捷命令，每次启动时自动设置环境变量
alias claude-volc='ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/v1" ANTHROPIC_API_KEY="你的API Key" /usr/local/bin/claude'
alias claude-ds='ANTHROPIC_BASE_URL="https://api.deepseek.com" ANTHROPIC_API_KEY="你的API Key" /usr/local/bin/claude'

# 使用
claude-volc  # 使用火山引擎
claude-ds    # 使用 DeepSeek
```

> [!WARNING] 优缺点
> - ✅ 简单快速，无需修改文件
> - ✅ 方便测试不同平台
> - ❌ 重启终端后失效
> - ❌ 难以管理多个平台

---

### 2.2 使用配置文件配置

> [!INFO] 适用场景
> - 长期使用某个平台
> - 需要管理多个平台账号
> - 团队共享配置

#### 配置文件位置

根据你的操作系统，配置文件位于：

- **macOS**: `~/.claude/settings.json`
- **Windows**: `%APPDATA%\Claude\settings.json`
- **Linux**: `~/.config/claude/settings.json`

#### 配置文件格式

```json
{
  "providers": {
    "volcengine": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "你的火山引擎API Key",
      "defaultModel": "ep-20250813142523-6k5kg"
    },
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-你的DeepSeek API Key",
      "defaultModel": "deepseek-chat"
    }
  },
  "defaultProvider": "volcengine"
}
```

#### 各平台完整配置

**火山引擎配置**:
```json
{
  "providers": {
    "volcengine": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "你的火山引擎API Key",
      "defaultModel": "ep-20250813142523-6k5kg"
    }
  },
  "defaultProvider": "volcengine"
}
```

**通义千问配置**:
```json
{
  "providers": {
    "qwen": {
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "sk-你的通义千问API Key",
      "defaultModel": "qwen-max"
    }
  },
  "defaultProvider": "qwen"
}
```

**DeepSeek 配置**:
```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-你的DeepSeek API Key",
      "defaultModel": "deepseek-chat"
    }
  },
  "defaultProvider": "deepseek"
}
```

**智谱 AI 配置**:
```json
{
  "providers": {
    "zhipu": {
      "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
      "apiKey": "你的智谱API Key",
      "defaultModel": "glm-4-plus"
    }
  },
  "defaultProvider": "zhipu"
}
```

**Ollama 配置**:
```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "apiKey": "ollama",
      "defaultModel": "llama3.2"
    }
  },
  "defaultProvider": "ollama"
}
```

#### 多平台配置示例

```json
{
  "providers": {
    "volcengine": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "火山引擎API Key",
      "defaultModel": "ep-20250813142523-6k5kg"
    },
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "DeepSeek API Key",
      "defaultModel": "deepseek-chat"
    },
    "qwen": {
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "通义千问API Key",
      "defaultModel": "qwen-max"
    }
  },
  "defaultProvider": "volcengine"
}
```

> [!TIP] 使用方法
> 配置完成后，直接运行 `claude` 即可使用默认平台。如需切换平台，使用环境变量临时覆盖。

> [!WARNING] 优缺点
> - ✅ 永久保存，重启有效
> - ✅ 支持多平台管理
> - ✅ 可设置默认平台和模型
> - ❌ 需要手动编辑文件
> - ❌ API Key 明文存储（注意安全）

---

### 2.3 两种配置方式的优先级

```
环境变量 > 配置文件 (settings.json)
```

- 环境变量的优先级高于配置文件
- 配置文件适合作为默认配置
- 环境变量适合临时覆盖或测试

**示例**:
```bash
# 默认使用配置文件中的 volcengine
claude

# 临时切换到 deepseek（环境变量覆盖）
ANTHROPIC_BASE_URL="https://api.deepseek.com" ANTHROPIC_API_KEY="sk-xxx" claude
```

---

## 3. 模型切换

### 3.1 启动时指定模型

```bash
# 使用 --model 参数
claude --model <模型名称>

# 或使用简写 -m
claude -m <模型名称>
```

**示例**:
```bash
# 使用火山引擎的推理端点
claude -m ep-20250813142523-6k5kg

# 使用 DeepSeek 聊天模型
claude -m deepseek-chat
```

### 3.2 各平台可用模型列表

| 平台 | 模型名称 | 说明 |
|------|----------|------|
| **火山引擎** | `ep-20250813142523-6k5kg` | 推理端点 ID（示例） |
| | `claude-3-5-sonnet-20241022` | Claude 3.5 Sonnet |
| **通义千问** | `qwen-max` | 最强模型 |
| | `qwen-plus` | 均衡模型 |
| | `qwen-turbo` | 快速模型 |
| **DeepSeek** | `deepseek-chat` | 通用对话 |
| | `deepseek-coder` | 代码专用 |
| **智谱 AI** | `glm-4-plus` | 最强模型 |
| | `glm-4` | 标准模型 |
| | `glm-4-flash` | 快速模型 |
| **Ollama** | `llama3.2` | Llama 3.2 |
| | `qwen2.5` | 通义千问本地版 |

### 3.3 在配置文件中设置默认模型

在 `settings.json` 的 provider 配置中添加 `defaultModel` 字段：

```json
{
  "providers": {
    "volcengine": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "你的API Key",
      "defaultModel": "ep-20250813142523-6k5kg"
    }
  },
  "defaultProvider": "volcengine"
}
```

### 3.4 运行时切换模型

在 Claude Code 会话中，你可以通过对话切换模型：

```
请切换到 deepseek-chat 模型
```

或使用更简洁的方式：
```
使用 deepseek-coder 模型
```

---

## 4. MCP 使用

MCP (Model Context Protocol) 是模型上下文协议，允许 Claude Code 连接到外部工具和数据源。

### 4.1 MCP 配置文件位置

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

### 4.2 CLI 中管理 MCP

#### 添加 MCP 服务器

```bash
claude mcp add <name> <command> [args...]
```

**示例**:
```bash
# 添加浏览器 MCP
claude mcp add browsermcp npx @browsermcp/mcp@latest

# 添加文件系统 MCP
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /Users/zhqznc/Documents
```

#### 查看 MCP 列表

```bash
claude mcp list
```

#### 删除 MCP

```bash
claude mcp remove <name>
```

**示例**:
```bash
claude mcp remove browsermcp
```

#### 启用/禁用 MCP

```bash
claude mcp enable <name>
claude mcp disable <name>
```

### 4.3 常用 MCP 服务器

| MCP 服务器 | 功能 | 安装命令 |
|-----------|------|----------|
| **filesystem** | 访问和操作文件系统 | `npx -y @modelcontextprotocol/server-filesystem <path>` |
| **brave-search** | Brave 搜索 API | `npx -y @modelcontextprotocol/server-brave-search` |
| **git** | Git 操作 | `npx -y @modelcontextprotocol/server-git --repository <path>` |
| **postgres** | PostgreSQL 数据库 | `npx -y @modelcontextprotocol/server-postgres` |
| **github** | GitHub API 访问 | `npx -y @modelcontextprotocol/server-github` |
| **browsermcp** | 浏览器自动化 | `npx @browsermcp/mcp@latest` |

### 4.4 在项目中使用 MCP

进入项目目录后启动 Claude Code：

```bash
cd /path/to/project
claude
```

Claude 会自动加载已注册的 MCP，你可以直接使用相关功能：

```
读取当前目录所有 js 文件
搜索关于 Vue 3 的最新信息
查看最近的 git 提交
```

---

## 5. Skills 使用

Skills 是 Claude Code 的可扩展功能模块，可以通过斜杠命令或自然语言调用。

### 5.1 查看可用技能

在 Claude Code 中输入：
```
/help
```

### 5.2 技能配置位置

Skills 配置文件位置与 MCP 相同：

```json
{
  "skills": {
    "directory": "/path/to/skills"
  }
}
```

### 5.3 内置技能说明

| 技能名称 | 触发关键词 | 功能描述 |
|---------|-----------|---------|
| excalidraw-diagram | Excalidraw, 画图, 流程图, 思维导图 | 生成 Excalidraw 图表 |
| obsidian-markdown | wikilinks, callouts, frontmatter | 创建 Obsidian 格式的 Markdown |
| obsidian-bases | Bases, 表格视图, 卡片视图 | 创建 Obsidian Bases 数据库 |
| json-canvas | Canvas, 画布, 思维导图 | 创建 JSON Canvas 可视化 |
| commit | /commit | 创建 git 提交 |
| review-pr | /review-pr | 审查 Pull Request |

### 5.4 使用技能的方式

#### 方式一：斜杠命令

```
/commit
/commit -m "修复登录bug"
/review-pr 123
```

#### 方式二：自然语言触发

```
帮我画一个用户注册流程图
创建一个 Excalidraw 思维导图
生成一个表格视图
```

### 5.5 创建自定义技能

1. 在 skills 目录下创建技能文件
2. 定义技能的触发条件和执行逻辑
3. 在配置文件中注册技能

**技能结构示例**:
```
/skills/
  ├── my-skill/
  │   ├── skill.json
  │   ├── prompt.md
  │   └── schema.json
```

**skill.json 示例**:
```json
{
  "name": "my-skill",
  "displayName": "我的技能",
  "description": "技能描述",
  "triggers": ["关键词1", "关键词2"],
  "type": "user-invocable"
}
```

---

## 6. CLI 常用命令

### 6.1 启动命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `claude` | 启动 Claude Code | `claude` |
| `--model <模型>` | 指定模型启动 | `claude --model deepseek-chat` |
| `-m <模型>` | 指定模型启动（简写） | `claude -m qwen-max` |
| `--version` | 查看版本 | `claude --version` |
| `--help` | 查看帮助 | `claude --help` |

### 6.2 MCP 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `claude mcp add <name> <cmd>` | 添加 MCP 服务器 | `claude mcp add browser npx @browsermcp/mcp@latest` |
| `claude mcp list` | 列出已安装的 MCP | `claude mcp list` |
| `claude mcp remove <name>` | 删除 MCP 服务器 | `claude mcp remove browser` |
| `claude mcp enable <name>` | 启用 MCP 服务器 | `claude mcp enable filesystem` |
| `claude mcp disable <name>` | 禁用 MCP 服务器 | `claude mcp disable git` |

### 6.3 Slash 命令（会话中使用）

| 命令 | 功能 | 示例 |
|------|------|------|
| `/help` | 显示所有可用命令 | `/help` |
| `/plan` | 进入规划模式 | `/plan` |
| `/commit` | 创建 git commit | `/commit` |
| `/commit -m "msg"` | 指定提交信息 | `/commit -m "修复bug"` |
| `/review-pr <编号>` | 审查 Pull Request | `/review-pr 123` |
| `/remember` | 记住项目信息 | `/remember` |
| `/tasks` | 查看任务列表 | `/tasks` |
| `/explain` | 解释代码 | `/explain src/app.js` |

### 6.4 环境变量检查

```bash
# 查看当前 API 地址
echo $ANTHROPIC_BASE_URL

# 查看当前 API Key（慎用）
echo $ANTHROPIC_API_KEY

# 查看 Claude Code 版本
claude --version
```

### 6.5 命令功能说明

- **启动命令**: 控制 Claude Code 的启动方式和模型选择
- **MCP 命令**: 管理外部工具和数据源的连接
- **Slash 命令**: 在会话中快速执行特定操作
- **环境变量**: 检查当前配置状态

---

## 7. 常见问题

### Q: 如何快速切换不同平台？

**A**: 推荐使用 alias 方式：

```bash
# 添加到 ~/.zshrc
alias claude-volc='ANTHROPIC_BASE_URL="https://ark.cn-beijing.volces.com/v1" ANTHROPIC_API_KEY="你的Key" claude'
alias claude-ds='ANTHROPIC_BASE_URL="https://api.deepseek.com" ANTHROPIC_API_KEY="你的Key" claude'
alias claude-qwen='ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1" ANTHROPIC_API_KEY="你的Key" claude'

# 使用
claude-volc  # 火山引擎
claude-ds    # DeepSeek
claude-qwen  # 通义千问
```

### Q: 配置文件不生效怎么办？

**A**: 检查以下几点：
1. 确认配置文件路径正确
2. 检查 JSON 格式是否正确（可以使用在线 JSON 验证工具）
3. 确认没有环境变量覆盖配置文件
4. 重启 Claude Code

### Q: 如何查看当前使用的模型？

**A**: 在 Claude Code 会话中询问：
```
我当前使用的是什么模型？
```

---

## 8. 相关资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Anthropic API 文档](https://docs.anthropic.com/)
