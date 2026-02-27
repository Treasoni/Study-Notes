---
tags: [ai, 进阶应用, 插件]
---

# Claude Code 插件系统使用指南

> [!info] 为什么需要了解插件？
> 插件是 Claude Code 的核心扩展机制。理解插件系统后，你将能够：
> - 使用他人开发的插件增强 Claude Code 能力
> - 创建自己的插件，定制专属开发助手
> - 理解插件与 MCP 的关系（为什么有些 MCP 是"插件自带的"）

**相关文档**：[[03-进阶应用/Claude MCP 使用指南]] | [[04-高级应用/Claude Subagent 使用指南]] | [[02-工具使用/如何使用Claude code]]

---

## 1. 什么是插件

### 核心概念

**插件 = Claude Code 的扩展模块**

类比：
- **浏览器扩展**：给浏览器添加新功能
- **VS Code 插件**：给编辑器添加新能力
- **Claude Code 插件**：给 AI 助手添加专业技能

### 插件 vs MCP 的关系

```
Claude Code 架构：

┌─────────────────────────────────────────────┐
│           Claude Code 核心                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │   插件系统    │      │   MCP 系统    │   │
│  │  (Plugins)   │      │  (MCP)        │   │
│  └──────────────┘      └──────────────┘   │
│         │                      │           │
│         └──────────┬───────────┘           │
│                    │                       │
│            插件可以自带 MCP 服务器           │
│            (Plugin MCP)                    │
└─────────────────────────────────────────────┘
```

**关键区别**：
- **MCP**：工具通信协议（定义工具如何与 Claude 对话）
- **插件**：功能扩展容器（可以包含多个 Agent、工具、MCP 服务器等）
- **插件 MCP**：插件自带的 MCP 服务器（第4节的内容）

### 插件能做什么？

| 能力 | 说明 | 示例 |
|------|------|------|
| **自定义 Agent** | 创建专门的 AI 助手 | 代码审查 Agent、测试生成 Agent |
| **自定义命令** | 添加新的 `/` 命令 | `/review`、`/test` |
| **自带 MCP** | 捆绑 MCP 服务器 | 数据库插件自带查询 MCP |
| **事件钩子** | 响应 Claude 操作 | 写完代码自动格式化 |
| **LSP 集成** | 语言服务器协议 | 代码补全、诊断信息 |

---

## 2. 插件结构

### 目录结构

```
my-plugin/
├── .claude-plugin/               # 插件配置目录（必需）
│   └── plugin.json              # 插件元数据（必需）
├── agents/                      # 专门化 Agent（可选）
│   ├── code-reviewer.md
│   └── test-generator.md
├── commands/                    # 自定义命令（可选）
│   └── hello.md
├── skills/                      # Agent 能力定义（可选）
│   └── SKILL.md
├── hooks/                       # 事件处理器（可选）
│   └── hooks.json
├── .mcp.json                   # MCP 服务器配置（可选）
├── .lsp.json                   # LSP 服务器配置（可选）
├── assets/                      # 资源文件（可选）
│   ├── templates/
│   └── examples/
└── README.md                    # 文档（推荐）
```

### plugin.json 格式

```json
{
  "name": "my-plugin",
  "description": "我的第一个 Claude Code 插件",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["code-review", "testing"],
  "homepage": "https://github.com/user/my-plugin",
  "claude": {
    "minVersion": "1.0.0"
  },
  // 内联配置（可选）
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
      }]
    }]
  }
}
```

### Agent 文件格式

```markdown
---
name: code-reviewer
description: 代码审查专家，当用户要求"审查代码"、"review code"时触发
model: sonnet
tools: ["Read", "Grep", "Glob"]
color: blue
---

# Code Reviewer Agent

你是一位代码审查专家，专注于...
```

**Frontmatter 字段说明**：

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 唯一标识符 |
| `description` | ✅ | 触发短语，Claude 用于匹配 |
| `model` | ❌ | AI 模型：sonnet/haiku/opus |
| `color` | ❌ | UI 显示颜色 |
| `tools` | ❌ | 允许使用的工具列表 |

---

## 3. 安装和使用插件

### 安装方法

**方法1：从插件市场安装**

```bash
# 浏览市场
claude plugin marketplace

# 安装官方插件
claude plugin install code-review@anthropics/skills

# 添加市场源
claude plugin marketplace add anthropics/skills
```

**方法2：从本地路径安装**

```bash
# 从本地目录安装
claude plugin install /path/to/my-plugin

# 从 Git 仓库安装
claude plugin install https://github.com/user/plugin-repo
```

**方法3：运行时加载**

```bash
# 临时加载插件
claude --plugin-dir ./my-plugin

# 加载多个插件目录
claude --plugin-dir ~/.claude/plugins --plugin-dir ./project-plugins
```

### 插件管理命令

```bash
# 列出已安装的插件
claude plugin list

# 验证插件配置
claude plugin validate

# 启用/禁用插件
claude plugin enable my-plugin
claude plugin disable my-plugin

# 更新插件
claude plugin update my-plugin

# 卸载插件
claude plugin uninstall my-plugin
```

### 在 Claude Code 中使用

```bash
# 查看已加载的 Agent
/agents

# 使用自定义命令
/my-custom-command

# 查看插件 MCP 工具
/mcp
```

### 永久配置

在 `~/.claude/config.json` 中配置：

```json
{
  "pluginDir": "~/.claude/plugins",
  "pluginDirs": [
    "~/.claude/plugins",
    "./project-plugins"
  ]
}
```

---

## 4. 创建自己的插件

### 快速开始

**步骤1：创建目录结构**

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/agents
cd my-plugin
```

**步骤2：编写 plugin.json**

```json
{
  "name": "my-first-plugin",
  "description": "我的第一个 Claude Code 插件",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

**步骤3：创建一个 Agent**

创建 `agents/code-helper.md`：

```markdown
---
name: code-helper
description: 代码助手，帮助用户理解和编写代码
model: sonnet
---

# Code Helper

你是一位友好的代码助手，专注于：
- 解释代码逻辑
- 帮助编写清晰的代码
- 遵循最佳实践

请用简洁的方式回答用户问题。
```

**步骤4：测试插件**

```bash
# 验证配置
claude plugin validate

# 运行并加载插件
claude --plugin-dir .

# 在 Claude Code 中检查
/agents
```

### 高级功能

**1. 创建自定义命令**

创建 `commands/deploy.md`：

```markdown
---
name: deploy
description: 部署应用到生产环境
---

# 部署命令

运行以下步骤：
1. 运行测试
2. 构建项目
3. 部署到服务器
```

使用：`/deploy`

**2. 添加 MCP 服务器**

创建 `.mcp.json`：

```json
{
  "my-api": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/mcp-server.js"],
    "env": {
      "API_KEY": "${API_KEY}"
    }
  }
}
```

**3. 配置事件钩子**

创建 `hooks/hooks.json`：

```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
    }]
  }]
}
```

### 开发最佳实践

1. **命名规范**
   - 插件名使用小写字母和连字符：`my-plugin`
   - Agent 名使用小写字母和连字符：`code-reviewer`

2. **版本管理**
   - 使用语义化版本：`1.0.0`
   - 更新时修改版本号

3. **权限最小化**
   - Agent 只给需要的工具权限
   - 避免给予 `Write` 等危险权限

4. **触发词设计**
   - 提供中英文触发词
   - 明确、不模糊的描述

5. **文档完善**
   - 包含 README.md
   - 说明安装和使用方法
   - 提供示例

---

## 5. 官方插件和资源

### 官方插件仓库

- **GitHub**: [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

### 常用官方插件

| 插件 | 功能 |
|------|------|
| **code-review** | 自动 PR 审查 |
| **commit-commands** | Git 工作流简化 |
| **feature-dev** | 系统化功能开发 |
| **plugin-dev** | 插件开发工具包 |

### 相关文档

- [[03-进阶应用/Claude MCP 使用指南]] - MCP 协议详解
- [[04-高级应用/Claude Subagent 使用指南]] - Agent 系统详解

---

## 6. 常见问题

**Q: 插件和 Agent 有什么区别？**

A:
- **插件**是容器，组织多个相关功能
- **Agent**是执行单元，有特定行为和指令
- 一个插件可以包含多个 Agent

**Q: 插件会一直运行吗？**

A: 不会。插件根据需要加载：
- Agent 只在被触发时启动
- 插件 MCP 在插件启用时运行
- 禁用插件后，相关资源自动释放

**Q: 如何分享我的插件？**

A:
1. 将插件发布到 Git 仓库
2. 用户可以通过 URL 安装：`claude plugin install https://github.com/user/plugin`
3. 或提交到官方插件市场

**Q: 插件安全吗？**

A: 插件可以访问：
- 你允许的工具权限
- 环境变量（谨慎处理敏感信息）
- 文件系统（受工具权限限制）

建议：
- 只安装可信来源的插件
- 审查插件的 `plugin.json` 和 Agent 配置
- 使用最小权限原则
