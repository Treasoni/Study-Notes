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
claude mcp add myserver --command "node server.js"
```

或者使用官方 MCP：

```bash
claude mcp add filesystem --command "npx @modelcontextprotocol/server-filesystem"
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


# 三、如何使用 Skills？

Skills 在 Claude Code 里通常通过：

- Agent 模式
    
- 指定工具
    
- 自动调用
    

---

## 方法 1：直接让 Claude 用

比如：

`claude`

然后输入：

`重构这个项目的所有 API 层代码`

Claude 会自动调用：

- 文件系统
    
- 搜索
    
- 编辑工具
    

这就是 skills 在工作。

---

## 方法 2：指定模式

你可以使用：

`claude --agent`

或者：

`claude --dangerously-skip-permissions`

允许自动调用工具。

---

## 方法 3：使用任务式命令

例如：

`claude "分析这个项目结构并给出重构建议"`

Claude 会：

- 扫描项目
    
- 调用 MCP filesystem
    
- 生成分析报告
    

---

# 四、完整工作流示例

假设你想：

> 用 Claude 自动分析项目 + 修改代码 + 提交 git

---

## ① 添加 filesystem MCP

`claude mcp add filesystem --command "npx @modelcontextprotocol/server-filesystem"`

---

## ② 添加 git MCP

`claude mcp add git --command "npx @modelcontextprotocol/server-git"`

---

## ③ 进入项目目录

`cd my-project claude`

---

## ④ 给指令

`重构所有 controller 为 service + repository 分层，并提交 git commit`

Claude 会：

- 读代码
    
- 修改文件
    
- 调用 git
    
- 自动 commit
    

---

# 五、常用命令总结

### 查看 MCP

`claude mcp list`

---

### 删除 MCP

`claude mcp remove filesystem`

---

### 直接执行一次任务

`claude "为当前项目生成 README"`

---

### 进入交互模式

`claude`

---

### 启用 agent 自动模式

`claude --agent`

---

# 六、常见问题

## ❓MCP 和 Skills 有什么区别？

|MCP|Skills|
|---|---|
|插件服务器|预置能力|
|外部扩展|内部工具集合|
|你可以自己写|官方内置|

简单理解：

> MCP 是扩展接口  
> Skills 是内置能力

---

## ❓需要自己写 MCP 吗？

不一定。

官方已有：

- filesystem
    
- git
    
- browser
    
- sqlite
    
- puppeteer
    

如果你要接入：

- 企业 API
    
- 内网数据库
    
- 私有系统
    

那就要自己写 MCP。

---

# 七、进阶：自己写 MCP Server

基本结构：

`import { Server } from "@modelcontextprotocol/sdk";  const server = new Server({   name: "my-server",   version: "1.0.0", });  server.tool("sayHello", async () => {   return "Hello World"; });  server.listen();`

然后注册：

`claude mcp add myserver --command "node index.js"`

---

# 八、总结一句话

在命令行使用 MCP 和 Skills 的流程：

`1️⃣ 安装 claude 2️⃣ 添加 mcp server 3️⃣ 进入项目 4️⃣ 用自然语言指挥`

Claude 会自动调用 skills + MCP。

---

如果你告诉我：

- 你是想做自动写代码？
    
- 还是接数据库？
    
- 还是做 CI/CD？
    
- 还是接浏览器自动化？
    

我可以给你一个完整实战案例流程。

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
