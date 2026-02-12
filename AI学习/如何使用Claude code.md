---
tags:
  - ai
---
# 1.下载Claude code
用下面网址：
```http
https://code.claude.com/docs/zh-CN/quickstart
```
根据你电脑的系统按照命令进行下载。

下载完成后就可以用下面命令进入Claudecode
```shell
claude
# 首次使用时系统会提示您登录
```
如果你有claudecode账号可以直接使用，但是如果你没有就不行。但是你可以按照我下面的操作来实现不用订阅和账号就能使用。

# 2. 使用火山引擎
这里我调用的是火山引擎的模型，其他平台的类似。
## 2.1 创建API Key
![](assets/如何使用Claude%20code/file-20260205163233511.png)
## 2.2 进行Claude code配置

我们在**文档**中直接搜索**Claude code**。按照文档中的过程来就可以了。
![](assets/如何使用Claude%20code/file-20260205163233510.png)

# 3. 使用 MCP (Model Context Protocol)

MCP 是模型上下文协议，允许 Claude Code 连接到外部工具和数据源。

## 3.1 MCP 配置文件位置

MCP 配置文件位于：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json.json`

## 3.2 添加 MCP 服务器

在配置文件的 `mcpServers` 部分添加服务器：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

## 3.3 常用 MCP 服务器

- **@modelcontextser/server-filesystem**: 访问和操作文件系统
- **@modelcontextprotocol/server-brave-search**: 使用 Brave 搜索 API
- **@modelcontextprotocol/server-git**: Git 操作
- **@modelcontextprotocol/server-postgres**: PostgreSQL 数据库访问
- **@modelcontextprotocol/server-github**: GitHub API 访问

## 3.4 CLI 里怎么用 MCP？

### 3.4.1 配置 MCP 服务器

Claude Code 使用：

```bash
claude mcp add
```

示例：添加一个本地 MCP server

```bash
claude mcp add myserver command "node server.js"
```

或者使用官方 MCP：

```bash
claude mcp add filesystem command "npx @modelcontextprotocol/server-filesystem"
```

### 3.4.2 查看已安装 MCP

```bash
claude mcp list
```

### 3.4.3 启用 MCP

在项目目录：

```bash
claude
```

Claude 会自动加载已注册的 MCP。

你可以直接说：

`读取当前目录所有 js 文件`

它会通过 MCP filesystem server 访问文件。
### 3.4.4 如何删除mcp

```
claude mcp remove <name>
```


# 4. 使用 Skills (技能)

Skills 是 Claude Code 的可扩展功能模块，可以通过斜杠命令调用。

## 4.1 查看可用技能

在 Claude Code 中输入：
```
/help
```

可以查看所有可用的技能列表。

## 4.2 技能配置位置

Skills 配置文件位置与 MCP 相同，在配置文件中通过以下方式添加：

```json
{
  "skills": {
    "directory": "/path/to/skills"
  }
}
```

## 4.3 内置技能说明

以下是常用的内置技能：

| 技能名称 | 触发关键词 | 功能描述 |
|---------|-----------|---------|
| excalidraw-diagram | Excalidraw, 画图, 流程图, 思维导图 | 生成 Excalidraw 图表 |
| obsidian-markdown | wikilinks, callouts, frontmatter | 创建 Obsidian 格式的 Markdown |
| obsidian-bases | Bases, 表格视图, 卡片视图 | 创建 Obsidian Bases 数据库 |
| json-canvas | Canvas, 画布, 思维导图 | 创建 JSON Canvas 可视化 |
| commit | /commit | 创建 git 提交 |

## 4.4 使用技能

### 方式一：斜杠命令
```
/commit "修复登录bug"
/commit -m "添加新功能"
```

### 方式二：自然语言触发
```
帮我画一个流程图
Excalidraw 用户注册流程
创建一个表格视图
```

## 4.5 创建自定义技能

1. 在 skills 目录下创建技能文件
2. 定义技能的触发条件和执行逻辑
3. 在配置文件中注册技能

示例技能结构：
```
/skills/
  ├── my-skill/
  │   ├── skill.json
  │   ├── prompt.md
  │   └── schema.json
```

skill.json 示例：
```json
{
  "name": "my-skill",
  "displayName": "我的技能",
  "description": "技能描述",
  "triggers": ["关键词1", "关键词2"],
  "type": "user-invocable"
}
```
