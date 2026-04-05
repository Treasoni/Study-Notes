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
| **LSP ���成** | 语言服务器协议 | 代码补全、诊断信息 |

### LSP 服务器配置详解

插件可以包含 Language Server Protocol (LSP) 支持，提供实时代码智能。

**配置位置**：
- `.lsp.json` 文件在插件根目录
- 或 `plugin.json` 中的内联 `lsp` 字段

**字段说明**：

| 字段 | 必需 | 说明 |
|------|------|------|
| `command` | ✅ | LSP 服务器二进制文件（必须在 PATH 中） |
| `extensionToLanguage` | ✅ | 文件扩展名到语言 ID 的映射 |
| `args` | ❌ | 服务器命令行参数 |
| `transport` | ❌ | 通信方式：`stdio`（默认）或 `socket` |
| `env` | ❌ | 服务器进程的环境变量 |
| `initializationOptions` | ❌ | LSP 初始化时发送的选项 |
| `settings` | ❌ | 传递给服务器的配置 |
| `startupTimeout` | ❌ | 服务器启动最大等待时间（毫秒） |
| `shutdownTimeout` | ❌ | 优雅关闭最大时间（毫秒） |
| `restartOnCrash` | ❌ | 服务器崩溃时是否自动重启 |
| `maxRestarts` | ❌ | 放弃前最大重启次数 |

**常用语言配置示例**：

```json
// Python (pyright)
{
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}

// TypeScript
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    }
  }
}

// Go (gopls)
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**LSP 功能**：
- **即时诊断** - 编辑后立即显示错误和警告
- **代码导航** - 跳转到定义、查找引用、实现
- **悬停信息** - 悬停时显示类型签名和文档
- **符号列表** - 浏览当前文件或工作区的符号

> [!info] 📚 来源
> - [GitHub - Claude HowTo LSP 配置](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - LSP 配置参考

---

## 2. 插件结构

### 目录结构

```
my-plugin/
├── .claude-plugin/               # 插件配置目录（必需）
│   └── plugin.json              # 插件元数据（必需）
├── agents/                      # 专门化 Agent（可选）
│   ├── specialist-1.md
│   └── configs/
├── commands/                    # 自定义命令（可选）
│   ├── task-1.md
│   └── workflows/
├── skills/                      # Agent 能力定义（可选）
│   ├── skill-1.md
│   └── skill-2.md
├── hooks/                       # 事件处理器（可选）
│   └── hooks.json
├── .mcp.json                   # MCP 服务器配置（可选）
├── .lsp.json                   # LSP 服务器配置（可选）
├── settings.json               # 默认设置（可选）
├── templates/                   # 模板文件（可选）
│   └── issue-template.md
├── scripts/                     # 辅助脚本（可选）
│   ├── helper.sh
│   └── helper.py
├── docs/                        # 文档（推荐）
│   ├── README.md
│   └── USAGE.md
└── tests/                       # 测试（推荐）
    └── plugin.test.js
```

> [!info] 📚 来源
> - [GitHub - Claude HowTo 插件示例](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - 官方插件结构参考

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
  "repository": "https://github.com/user/my-plugin",
  "license": "MIT",
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

### 用户可配置选项 (userConfig) (v2.1.83+)

插件可以在 manifest 中声明用户可配置的选项，通过 `userConfig` 字段：

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "userConfig": {
    "apiKey": {
      "description": "API 密钥",
      "sensitive": true
    },
    "region": {
      "description": "部署区域",
      "default": "us-east-1"
    }
  }
}
```

**字段说明**：
| 字段 | 说明 |
|------|------|
| `description` | 选项描述 |
| `sensitive` | 设为 `true` 时，值存储在系统密钥链而非明文配置文件 |
| `default` | 默认值 |

### 持久化数据目录 (${CLAUDE_PLUGIN_DATA}) (v2.1.78+)

插件可通过 `${CLAUDE_PLUGIN_DATA}` 环境变量访问持久化数据目录：

```json
{
  "hooks": {
    "PostToolUse": [{
      "command": "node ${CLAUDE_PLUGIN_DATA}/track-usage.js"
    }]
  }
}
```

**特点**：
- 目录在插件安装时自动创建
- 每个插件有独立的数据目录
- 数据在会话间持久保存
- 插件卸载时数据会被删除

### 内联插件定义 (source: 'settings') (v2.1.80+)

可以在配置文件中直接定义插件，无需单独的仓库：

```json
{
  "pluginMarketplaces": [{
    "name": "inline-tools",
    "source": "settings",
    "plugins": [{
      "name": "quick-lint",
      "source": "./local-plugins/quick-lint"
    }]
  }]
}
```

### 插件默认设置 (settings.json)

插件可以提供 `settings.json` 文件设置默认配置：

```json
{
  "agent": "agents/specialist-1.md"
}
```

用户可在项目或用户配置中覆盖这些设置。

> [!info] 📚 来源
> - [GitHub - Claude HowTo 插件系统](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - 新功能参考

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

### 企业管理设置

管理员可以通过托管设置控制整个组织的插件行为：

| 设置 | 说明 |
|------|------|
| `enabledPlugins` | 默认启用的插件白名单 |
| `deniedPlugins` | 禁止安装的插件黑名单 |
| `extraKnownMarketplaces` | 添加额外的市场源 |
| `strictKnownMarketplaces` | 限制用户可添加的市场 |
| `allowedChannelPlugins` | 按发布渠道控制允许的插件 |

**市场限制示例**：

```json
{
  "strictKnownMarketplaces": [
    "my-org/*",
    "github.com/trusted-vendor/*"
  ]
}
```

> [!warning] 企业限制
> 在严格模式下，用户只能安装白名单市场中的插件。

### 插件安全限制

插件子 Agent 在受限沙箱中运行，以下 frontmatter 字段**不允许**在插件子 Agent 定义中使用：

| 禁止字段 | 原因 |
|----------|------|
| `hooks` | 子 Agent 不能注册事件处理器 |
| `mcpServers` | 子 Agent 不能配置 MCP 服务器 |
| `permissionMode` | 子 Agent 不能覆盖权限模型 |

这确保插件无法提升��限或修改超出其声明范围的主机环境。

> [!info] 📚 来源
> - [GitHub - Claude HowTo 插件安全](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - 安全限制参考

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

---

## 7. 故障排除

### 插件无法安装

**检查项**：
1. Claude Code 版本兼容性：`/version`
2. 验证 `plugin.json` 语法（使用 JSON 验证器）
3. 检查网络连接（远程插件）
4. 检查权限：`ls -la plugin/`

### 组件未加载

**检查项**：
1. 验证 `plugin.json` 中的路径与实际目录结构匹配
2. 检查文件权限：`chmod +x scripts/`
3. 检查组件文件语法
4. 查看日志：`/plugin debug plugin-name`

### MCP 连接失败

**检查项**：
1. 验证环境变量设置正确
2. 检查 MCP 服务器安装和运行状态
3. 独立测试 MCP 连接：`/mcp test`
4. 检查 `mcp/` 目录中的配置

### 安装后命令不可用

**检查项**：
1. 确认插件安装成功：`/plugin list --installed`
2. 检查插件是否启用：`/plugin status plugin-name`
3. 重启 Claude Code：`exit` 后重新打开
4. 检查命名冲突（与现有命令重名）

### 钩子执行问题

**检查项**：
1. 验证钩子文件有正确的执行权限
2. 检查钩子语法和事件名称
3. 查看钩子日志获取错误详情
4. 尽可能手动测试钩子

---

## 参考资料

### 官方资源
- [Claude Code 官方文档](https://docs.anthropic.com/claude-code) - 完整技术文档
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) - 官方插件仓库

### 社区资源
- [Claude HowTo - 插件系统](https://github.com/luongnv89/claude-howto/tree/main/07-plugins) - 可视化教程和示例
- [Claude HowTo 仓库](https://github.com/luongnv89/claude-howto) - 从基础到高级的完整指南
