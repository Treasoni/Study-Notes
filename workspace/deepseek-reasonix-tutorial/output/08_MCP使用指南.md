---
title: DeepSeek-Reasonix MCP 使用指南
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 进阶
tags: [DeepSeek-Reasonix, MCP, stdio, Streamable-HTTP, SSE, ACP]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# DeepSeek-Reasonix MCP 使用指南

> [!info] 文档定位
> 本文是 DeepSeek-Reasonix 的 MCP 接入章（03-进阶应用篇第 8 章）：讲清三类 server、命令行管理、配置声明与 MCP over ACP。面向已熟悉 Claude Code MCP 生态的用户，省略通用概念铺垫，只讲差异与接入。文中字段与行为均取自官方 `reasonix.example.toml`、CLI 参考与 ACP 文档；实时权威始终是应用内 `/help`。关联：[[reasonix.toml 配置详解]]、[[DeepSeek-Reasonix CLI 完整参考]]、[[DeepSeek-Reasonix 插件与扩展开发]]。

本文回答一个核心问题：**在 Reasonix 里接一个 MCP server，和 Claude Code 有什么不一样？** 如果你已经在 Claude Code 里配过 MCP，思路基本可以直接迁移，只差三件事：Reasonix 支持三类传输、命令行管理子命令、配置入口有两处（`[[plugins]]` 与 MCP over ACP）。

## 一、MCP 是什么：与 Claude Code 生态对齐

MCP（Model Context Protocol）是你在 Claude Code 里已经熟悉的「外接工具标准」：Agent 通过统一协议去调用外部的工具服务，比如文件系统、数据库、浏览器、内部 API。Reasonix 走的是同一套协议，接入方式也刻意与 Claude Code 对齐——`claude` 的 MCP 配置映射为 Reasonix 的 `mcpServers`（MCP over ACP），所以迁移成本很低。

需要记住的差异只有两点：

1. **Reasonix 支持三类 server**：`stdio`、`Streamable HTTP`、`legacy SSE`。
2. **配置入口有两处**：本地 stdio 插件走 `reasonix.toml` 的 `[[plugins]]`；ACP 会话里通过 `mcpServers` 附加（MCP over ACP）。

> [!tip] 大白话
> 把 MCP 想成「给 AI 接外设的 USB 接口标准」：电脑（Reasonix）不需要为每个鼠标键盘单独改造，只要它们遵守 USB 协议，插上就能用。
> 所以接入一个新的 MCP server，本质是「把外设插到统一接口上」，而不是给 Reasonix 写一套定制代码。

## 二、三种传输方式与适用场景

Reasonix 支持的三类 server 对应三种「接线方式」：

| 传输 | 形态 | 适用场景 |
|------|------|----------|
| `stdio` | 本地子进程，随 Agent 同启同停 | 本机工具（文件系统、本地数据库、命令行工具），最常用 |
| `Streamable HTTP` | 远程 HTTP 服务，跨机器调用 | 共享/远程服务、团队统一部署的 MCP 网关 |
| `legacy SSE` | 老式 HTTP 传输（Server-Sent Events） | 存量 server 尚未迁移到 Streamable HTTP 时的兼容选择 |

> [!note] 迁移提示
> 与 Claude Code 生态一致：新写的 server 优先走 `stdio`（本地）或 `Streamable HTTP`（远程），`legacy SSE` 只为兼容旧服务保留。ACP 能力协商里 `mcpCapabilities` 标记为 `http: true, sse: false`，也从侧面说明 HTTP 是新方向、SSE 是存量兼容。

> [!tip] 大白话
> 三种传输像三种连接方式：`stdio` 是「有线 USB」（线直接插在电脑上，设备随电脑开关）；`Streamable HTTP` 是「Wi-Fi 连远程服务器」（设备不在这台电脑上，通过网络访问）；`legacy SSE` 是「老式蓝牙」（老设备还在用，新设备基本不带了）。

## 三、命令行管理：`reasonix mcp`

Reasonix 提供一组 MCP 管理子命令，覆盖「查、找、装、验、逛」五个动作：

```bash
reasonix mcp list                # 列出已配置/已知的 server
reasonix mcp search <关键词>      # 搜索可用的 server
reasonix mcp install <server>    # 安装一个 server
reasonix mcp inspect <server>    # 检查一个 server 的配置或连接
reasonix mcp browse              # 浏览可用的 server
```

五个子命令按「查 → 找 → 装 → 验 → 逛」来记：先 `list` 看手头有什么，`search`/`browse` 找想接的，`install` 装上，`inspect` 验证配置与连通性。

> [!note] 版本差异
> v1 与 main-v2 的 CLI 文档命令列表不同。`reasonix mcp` 的具体子命令与参数以你安装版本的官方 CLI 参考为准；运行时报「命令不存在」，先跑应用内 `/help` 确认真实命令集（详见[[DeepSeek-Reasonix CLI 完整参考]]）。

## 四、配置文件声明：`[[plugins]]` 与 MCP over ACP

配置声明有两条路，分别对应「本地常驻插件」与「远程/会话级 server」。

### 4.1 本地 stdio 插件：`[[plugins]]`

在 `reasonix.toml` 里用 `[[plugins]]` 声明外部 stdio 插件，字段是 `name` + `command`（来自官方 `reasonix.example.toml`）：

```toml
# [[plugins]]                         # MCP/外部 stdio 插件
# name = "example"                    # 插件标识
# command = "reasonix-plugin-example" # 启动该 stdio 插件的命令
```

要点：

- 插件管理走**配置声明**，Reasonix 没有独立的插件子命令。
- `command` 是启动该 stdio 插件的可执行命令，可以是本地二进制，也可以通过 `npx` 等启动器拉起（写法与 Claude Code 的 stdio server 一致）。
- `[[plugins]]` 字段书写细节以[[reasonix.toml 配置详解]]为准；插件的扩展开发（Extension Protocol）见[[DeepSeek-Reasonix 插件与扩展开发]]。

### 4.2 远程/会话级 server：MCP over ACP

在 ACP 协议场景下（编辑器/IDE 接入时），`session/new`、`session/load`、`session/resume` 消息可以携带 `mcpServers` 字段，把 server 直接挂到会话上。这是 Reasonix 对齐 Claude Code `mcpServers` 配置的入口。

其中 `env`（stdio 的环境变量）与 `headers`（HTTP 的请求头）使用官方 ACP 形状 `[{"name":"...","value":"..."}]`：

```json
{
  "mcpServers": {
    "local-fs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": [{ "name": "MY_VAR", "value": "${MY_VAR}" }]
    },
    "remote-svc": {
      "url": "https://mcp.example.com/mcp",
      "headers": [{ "name": "Authorization", "value": "Bearer ${API_TOKEN}" }]
    }
  }
}
```

> [!note] 示意说明
> 上面的 `mcpServers` 是形状示意（与 Claude Code 的 `mcpServers` 对齐）；其中可确认的事实是：stdio 的 `env` 与 HTTP 的 `headers` 采用官方 ACP 形状 `[{"name":"...","value":"..."}]`，`${VAR}` 由项目 `.env` 展开（见下文）。

### 4.3 环境变量展开

MCP/plugin 里的 `${VAR}` 占位符，由**项目根目录的 `.env`** 展开：

- 项目 `.env` 是 `${VAR}` 展开的来源，**不是** provider key 的导入通道——Reasonix 不会从项目 `.env` 导入 provider 密钥。
- 真实密钥仍然只放在全局 `<Reasonix home>/.env`（由 `reasonix setup` 管理）。

> [!tip] 大白话
> 把 `${VAR}` 想成「填表时的『此处填写你的工号』占位符」：Reasonix 拿到项目 `.env` 里的真实值帮你填进 MCP 的环境变量或请求头，但表格本身不记录工号。
> 所以项目 `.env` 里放的是「MCP/插件要用到的变量」，而不是你的 provider API Key——后者在全局 `.env` 的保险箱里。

## 五、超时配置

MCP 的超时在 `reasonix.toml` 的 `[tools]` 节，与 `bash_timeout_seconds` 并列：

```toml
[tools]
bash_timeout_seconds = 30        # 单个 bash 命令超时
mcp_startup_timeout_seconds = 30 # MCP server 启动超时（默认 30 秒）
mcp_call_timeout_seconds = 300   # MCP 单次调用超时（默认 300 秒）
```

- `mcp_startup_timeout_seconds = 30`：server **从启动到就绪**的超时。第一次用 `npx` 拉包、本地编译、启动慢的 server，经常需要调大。
- `mcp_call_timeout_seconds = 300`：**单次工具调用**的超时。跑长任务的 tool（比如大文件处理、批量请求）可能需要调大。

> [!tip] 大白话
> 把两个超时想成「点外卖」：`mcp_startup_timeout_seconds` 是「餐厅 30 秒没开门就取消订单」（server 启动太久），`mcp_call_timeout_seconds` 是「单道菜 5 分钟没上就催单/退单」（单次调用太久）。
> 所以接上慢启动的 server 时先调大启动超时，别一上来就怀疑是 server 写错了。

## 六、接入示例

### 6.1 stdio 本地 server

在 `reasonix.toml` 声明一个本地 stdio 插件：

```toml
[[plugins]]
name = "local-fs"
command = "npx -y @modelcontextprotocol/server-filesystem /tmp"
```

保存后启动 `reasonix code .` 进入 TUI，用 `/mcp` 管理/查看 MCP server（main-v2 命令族收录了 `/mcp`）；命令行里 `reasonix mcp list` 也可以确认 server 是否就绪。

### 6.2 远程 HTTP server

远程 HTTP server 走 MCP over ACP：在 ACP 会话创建消息（`session/new`）里带 `mcpServers`：

```json
{
  "mcpServers": {
    "remote-svc": {
      "url": "https://mcp.example.com/mcp",
      "headers": [{ "name": "Authorization", "value": "Bearer ${API_TOKEN}" }]
    }
  }
}
```

`${API_TOKEN}` 由项目 `.env` 展开；ACP 会话协议细节见[[DeepSeek-Reasonix ACP 协议指南]]。

## 七、排障与常见坑

1. **项目 `.env` 不会导入 provider key**。`.env` 只作 MCP/plugin 的 `${VAR}` 展开来源；把 provider API Key 写进项目 `.env` 不会生效，provider 凭据只在全局 `<Reasonix home>/.env`。

> [!warning] 坑点：密钥放错地方
> 常见误区是把 API Key 写进项目 `.env`，指望 MCP/plugin 或 provider 自动读到。Reasonix 只把项目 `.env` 当 `${VAR}` 展开来源，不导入 provider key——provider 凭据请放全局 `.env`，MCP 要用的普通变量放项目 `.env`。

2. **慢启动 server 报超时**。先看是不是启动超时（30s）不够：`npx` 首次拉包、本地编译通常要几十秒，把 `mcp_startup_timeout_seconds` 调大到 60–120 秒；单次调用慢再调 `mcp_call_timeout_seconds`。

3. **MCP 旧字段会被静默清理**。升级后若发现配置「写了却不生效」，先怀疑废弃字段：MCP 旧字段会被忽略并在保存时移除（与 `agent.auto_plan`、`agent.max_steps` 同批废弃）。

4. **Windows 沙箱差异**。Reasonix 不在 Windows 提供 OS 级 Bash 沙箱，`[sandbox] bash = "enforce"` 在 Windows 上解析为 `off`。对依赖本地 bash 子进程的 stdio server，Windows 上的隔离能力与 macOS/Linux 不同（macOS 用 Seatbelt、Linux 用 bubblewrap），需要自行评估。

5. **配置优先级**。改配置「不生效」时按 flag > `./reasonix.toml` > 全局 `~/.reasonix/config.toml` > 内置默认的顺序排查覆盖者。

6. **版本差异导致命令找不到**。`reasonix mcp` 子命令在不同版本文档中列表不同，实时权威是应用内 `/help` 与 `/keys`。

## 常见问题

**Q: 在 Reasonix 里接 MCP，和 Claude Code 最大的不同是什么？**
A: 支持三类 server（stdio / Streamable HTTP / legacy SSE），配置入口有两处——本地 stdio 插件走 `reasonix.toml` 的 `[[plugins]]`，ACP 会话里用 `mcpServers` 附加（MCP over ACP）。`env` 与 `headers` 采用官方 ACP 形状 `[{"name":"...","value":"..."}]`。

**Q: `[[plugins]]` 和 `mcpServers` 怎么选？**
A: `[[plugins]]` 声明的是常驻的本地 stdio 插件（写在 `reasonix.toml`，跟随项目）；`mcpServers` 出现在 ACP 会话创建/加载/恢复消息里，适合编辑器/IDE 接入时按会话附加，远程 HTTP server（带 `headers`）一般走这条。

**Q: MCP server 启动一直超时怎么办？**
A: 把 `[tools]` 下的 `mcp_startup_timeout_seconds` 从默认 30 秒调大（比如 60–120 秒），慢启动多发生在 `npx` 首次拉包或本地编译。单次调用慢则调 `mcp_call_timeout_seconds`。

**Q: MCP/plugin 要用环境变量，放哪里？**
A: 把变量写进项目根目录 `.env`，配置里用 `${VAR}` 引用，Reasonix 会展开。但项目 `.env` 不会导入 provider key——provider 凭据只在全局 `<Reasonix home>/.env`。

## 相关文档

- [[reasonix.toml 配置详解]] — `[[plugins]]` 与 `[tools]` 字段书写位置
- [[DeepSeek-Reasonix CLI 完整参考]] — `reasonix mcp` 命令与参数
- [[DeepSeek-Reasonix ACP 协议指南]] — MCP over ACP 的会话消息与 `mcpServers`
- [[DeepSeek-Reasonix 插件与扩展开发]] — Extension Protocol 与插件包分发

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/reasonix.example.toml`：`[[plugins]]` 声明示例
- `main-v2/docs/GUIDE.zh-CN.md`：配置指南
- `main-v2/docs/CLI.zh-CN.md` 与 `v1/docs/CLI-REFERENCE.md`：`reasonix mcp` 命令
- `main-v2/docs/ACP.md`：MCP over ACP 与 `mcpServers`

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（进阶应用篇第 8 章，MCP 使用指南） |
