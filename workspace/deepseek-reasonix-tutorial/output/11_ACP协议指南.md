---
title: DeepSeek-Reasonix ACP 协议指南
topic: DeepSeek-Reasonix 配置教程
type: guide
difficulty: 高级
tags: [DeepSeek-Reasonix, ACP, Agent-Client-Protocol, JSON-RPC, 编辑器集成, stdio]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# DeepSeek-Reasonix ACP 协议指南

> [!info] 文档定位
> 本文是 DeepSeek-Reasonix 的 ACP 协议章（高级功能篇第 11 章）：面向编辑器/IDE 集成方，讲清 Agent Client Protocol v1 的传输形态、能力协商、session 生命周期与协作模式。字段与行为均取自官方 `docs/ACP.md` 与 CLI 参考；实时权威始终是应用内 `/help`。关联：[[DeepSeek-Reasonix CLI 完整参考]]、[[DeepSeek-Reasonix MCP 使用指南]]、[[DeepSeek-Reasonix 插件与扩展开发]]。

如果你用过 VS Code 扩展版的 Reasonix，其实你已经在和 ACP 打交道了——扩展只是起了一个本地 `reasonix acp` 后端，再用协议驱动它。本文回答的核心问题是：**编辑器/IDE 想接 Reasonix，双方在 wire 上到底怎么说话？** 我们从「一行行 JSON 消息」讲到「会话怎么建、怎么批、怎么关」，给集成方一张可直接照做的地图。

## 一、ACP 是什么：编辑器与 agent 之间的驾驶舱协议

ACP（Agent Client Protocol）v1 是 Reasonix 用来接编辑器/IDE 的**会话协议**。它的传输形态一句话能说清：

> **NDJSON + JSON-RPC 2.0 over stdio**——标准输入/输出上，一行一条 JSON 消息，遵守 JSON-RPC 2.0 的 request/response 约定。

三个关键词拆开看：

| 术语 | 含义 |
|------|------|
| stdio | 通过进程的 stdin/stdout 通信，`reasonix acp` 作为子进程被编辑器拉起 |
| NDJSON | Newline-Delimited JSON，一行一个完整 JSON 对象，天然适合流式事件 |
| JSON-RPC 2.0 | request/response 与通知的规范，`id` 对应、`method` 分发、`error` 上报 |

**通道纪律**：stdout 只走 ACP 协议消息（机器读的），所有诊断/日志走 stderr（人看的）。集成方解析 stdout 时不要混入提示文本——这和[[DeepSeek-Reasonix 自动化与 CI]]里 `--copy` 把提示走 stderr、保证 stdout 纯 machine-readable 是同一个原则。

> [!tip] 大白话
> 把 ACP 想成**编辑器和 agent 之间的「方向盘 + 仪表盘」接口**：MCP 是给 agent 接工具的「USB 外设口」，ACP 则是让 VS Code 这类编辑器坐进驾驶座、握着方向盘开 Reasonix 这辆车。stdout/stderr 的分工像「前台对讲机走正线、维修电话走分线」——正线只报业务，别让杂音占线。

### ACP 与 MCP：别搞混两张协议

| 协议 | 连接的双方 | 回答的问题 |
|------|-----------|-----------|
| MCP | Agent ↔ 工具服务 | 「agent 怎么调用外部工具？」 |
| ACP | 编辑器/IDE ↔ Agent | 「编辑器怎么驱动一个 agent 会话？」 |

MCP 的细节见[[DeepSeek-Reasonix MCP 使用指南]]；本章只讲 ACP。一个直观的分工：编辑器通过 ACP 说「新建会话、跑这个任务、批这个操作」，agent 在会话里通过 MCP 调工具完成它。

## 二、启动 ACP 后端

`reasonix acp` 是 ACP 后端入口，作为 stdio 子进程常驻：

```bash
reasonix acp                       # 默认配置启动
reasonix acp --model deepseek-pro  # 指定 provider/模型
reasonix acp --profile delivery    # 用 delivery 工作档
```

VS Code 扩展（Marketplace 里的 `SivanLiu.reasonix-agent`）就是这么用的：**先装 CLI，扩展启动本地 `reasonix acp` 后端**，扩展本身只是协议客户端 + 编辑器 UI（文件树、diff、审批按钮）。所以「接入编辑器」约等于「写一个 ACP 客户端」。

> [!note] 依赖关系
> VS Code 扩展要求先装 CLI，因为它复用的是本地 `reasonix` 二进制；桌面端/浏览器端是另外的入口，不在本章范围。安装路径见第 1 章。

## 三、能力协商：开局先交换「技能清单」

ACP 客户端连上后端后，第一步是能力协商——agent 告诉编辑器「我会什么、你最多能给我什么」。返回的 `agentCapabilities` 核心字段（来自官方 `ACP.md`）：

| 能力字段 | 含义 |
|----------|------|
| `loadSession` | 支持加载已有会话 |
| `sessionCapabilities` | 会话级能力上限（如上下文窗口） |
| `promptCapabilities.embeddedContext` = `true` | 支持在 prompt 里内嵌上下文 |
| `mcpCapabilities.http` = `true` | 支持 MCP over HTTP |
| `mcpCapabilities.sse` = `false` | 不支持 legacy SSE 传输 |
| `_meta["reasonix.io"]` | Reasonix 扩展能力：`sessionSteer` / `sessionInbox` / `reloadExtensions` |

```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "agentCapabilities": {
      "loadSession": true,
      "sessionCapabilities": {},
      "promptCapabilities": { "embeddedContext": true },
      "mcpCapabilities": { "http": true, "sse": false }
    },
    "_meta": {
      "reasonix.io": {
        "sessionSteer": true,
        "sessionInbox": true,
        "reloadExtensions": true
      }
    }
  }
}
```

> 上例为形状示意，字段以官方 `ACP.md` 为准。`mcpCapabilities.http: true / sse: false` 与[[DeepSeek-Reasonix MCP 使用指南]]里「HTTP 是新方向、SSE 是存量兼容」的结论一致。

> [!tip] 大白话
> 能力协商像**入职第一天交换清单**：agent 递上「我会的」（loadSession、embeddedContext、MCP over HTTP），编辑器核对「我 UI 上能配合的」（文件读写、终端、审批按钮）。两边都对上号，后面的会话才不至于互相使唤不动。

## 四、session 生命周期：8 个方法管一次会话

ACP 里「一次对话」就是一个 session。8 个生命周期方法覆盖「创建 → 用 → 停 → 收尾」：

| 方法 | 作用 | 关键参数（示意） |
|------|------|------------------|
| `session/new` | 新建会话 | `configOptions`、`mcpServers`、首条 `prompt` |
| `session/load` | 加载既有会话 | `sessionId` |
| `session/resume` | 恢复历史会话 | `sessionId` / 查询条件 |
| `session/prompt` | 向会话发提示 | `sessionId`、`prompt` |
| `session/cancel` | 取消进行中的生成 | `sessionId` |
| `session/list` | 列出会话 | — |
| `session/close` | 关闭会话（保留记录） | `sessionId` |
| `session/delete` | 删除会话 | `sessionId` |

典型的「新建并提问」两段式：

```json
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"configOptions":{"tool_approval":"ask"}}}

{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"sess_01abcd","prompt":{"type":"text","content":"帮我修掉 README 里的拼写错误"}}}
```

`session/prompt` 发出后，agent 的回复（文本、工具调用、审批请求、进度事件）会以**多行 NDJSON 事件**流式返回，而不是一次 JSON 装完——客户端要按行解析、按事件类型分派。

> [!tip] 大白话
> session 生命周期像**一通电话从拨号到挂断**：`new` 是拨号、`prompt` 是说话、`cancel` 是抢挂、`list` 是查通话记录、`close` 是挂断但留录音、`delete` 是删掉录音。编辑器要做的就是维护好这通电话的状态机。

## 五、协作模式与工具审批：编辑器里的门禁

### 5.1 协作模式三态

会话在什么「风格」下协作，由协作模式决定：

| 协作模式 | 含义 | 旧值映射 |
|---------|------|---------|
| `normal` | 常规协作 | 旧 `default` → Normal+Ask；旧 `auto` → Normal+Yolo |
| `plan` | 计划模式（只读规划） | — |
| `goal` | 目标模式 | — |

旧版 `default` / `auto` 两种取值，被映射为「常规 + 逐步审批」（Normal+Ask）与「常规 + 全自动」（Normal+Yolo）两个组合——**新三态把「协作风格」和「审批粒度」解耦了**。

### 5.2 工具审批：`configOptions.tool_approval`

审批粒度通过 `configOptions.tool_approval` 设置，三档与 Claude Code 的 Ask / Auto / Yolo 一一对应：

| `tool_approval` | 行为 | Claude Code 对应 |
|-----------------|------|------------------|
| `ask` | 每次工具调用弹审批 | Ask |
| `auto` | 自动批准常规操作 | Auto |
| `yolo` | 跳过权限（仍遵守 deny/沙箱） | Yolo |

改动经 `session/set_config_option` 下发：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "session/set_config_option",
  "params": {
    "sessionId": "sess_01abcd",
    "configId": "default",
    "option": "tool_approval",
    "value": "ask"
  }
}
```

> [!warning] 踩坑：字段是 `configId`，不是 `optionId`
> 官方文档明确指出 `session/set_config_option` 的字段是 **`configId`**（标识哪份配置），不少集成方按惯性写成 `optionId` 导致静默失败。写客户端时务必按 `ACP.md` 核对字段名。

> [!tip] 大白话
> `tool_approval` 像**办公楼门禁的三种放行策略**：`ask` 是每道门都刷卡等保安确认，`auto` 是常去楼层直接放行，`yolo` 是发了张全楼通卡（但金库和禁地仍进不去）。`session/set_config_option` 就是前台改你门禁权限的那张工单。

## 六、编辑器/IDE 接入与 MCP over ACP

### 6.1 客户端通告能力，文件操作「让路」给编辑器

ACP 客户端可以通告自己实现了 `fs.readTextFile` / `fs.writeTextFile` / `terminal` 三组能力。一旦通告：

- **文件操作**路由到编辑器的**未保存缓冲区**——agent 读写的文件先落在编辑器里还没落盘的版本上，避免「编辑器里有未保存改动、agent 却读写磁盘旧版本」的错位。
- **前台命令**路由到**客户端终端**——需要人工看的命令（长任务、交互程序）在编辑器终端里跑，而不是藏在 agent 的隐藏子进程里。

对集成方来说，这是「编辑体验」和「agent 写盘」之间最重要的一道桥。

### 6.2 MCP over ACP：会话创建时带 `mcpServers`

ACP 会话里要挂 MCP server，直接在 `session/new`（也支持 `session/load`、`session/resume`）里带 `mcpServers` 字段——这就是 Reasonix 对齐 Claude Code `mcpServers` 配置的入口（详见[[DeepSeek-Reasonix MCP 使用指南]]）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "session/new",
  "params": {
    "configOptions": { "tool_approval": "ask" },
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
}
```

stdio 的 `env` 与 HTTP 的 `headers` 采用官方 ACP 形状 `[{"name":"...","value":"..."}]`；`${VAR}` 由项目根目录 `.env` 展开（项目 `.env` 不导入 provider key）。

## 七、接入示例与常见坑

### 7.1 编辑器插件实现思路

一个最小 ACP 客户端（无论 VS Code、Vim、Emacs 还是自研 IDE）都走同一条链路：

1. **拉起后端**：以子进程启动 `reasonix acp`，持有 stdin/stdout 两个管道。
2. **能力协商**：发能力协商请求，读 `agentCapabilities`，按 `mcpCapabilities.http/sse` 决定 MCP 接入方式。
3. **建会话**：`session/new`（带 `configOptions.tool_approval` 与需要的 `mcpServers`），记住返回的 `sessionId`。
4. **事件循环**：逐行读 stdout，按 `method` 分派——文本增量进聊天面板、工具调用/权限请求进审批 UI、完成事件收尾。
5. **生命周期**：用户点「停止」发 `session/cancel`，切项目发 `session/close`，清数据发 `session/delete`。

> [!note] 与 Claude Code 的关键差异（影响 host 集成方）
> 在 Claude Code 里，「Ask/Auto/Yolo」是本地键盘循环（`Shift+Tab` 切换、`y/n` 审批）；在 Reasonix 里，工具审批**经 ACP 协议暴露**（`session/set_config_option` + `session/request_permission`）。也就是说，审批按钮是编辑器 UI 要做的事，而不是 agent 终端里的快捷键——你的插件必须自己实现审批界面。

### 7.2 常见坑

1. **stdout 混入非协议内容**。ACP 要求 stdout 只走协议消息、诊断走 stderr；解析时把 stdout 当纯 NDJSON 流，任何多余文本都视为协议违规。
2. **把 `optionId` 当 `configId`**。`session/set_config_option` 的字段是 `configId`，写错会静默失败。
3. **忘了通告 fs/terminal 能力**。不通告 `fs.readTextFile` / `fs.writeTextFile` / `terminal`，文件操作就落到磁盘真实文件，编辑器未保存缓冲区的改动可能被 agent 覆盖。
4. **SSE 的 MCP server 接不上**。`mcpCapabilities.sse = false`——Reasonix 不支持 legacy SSE 传输，MCP server 要用 stdio 或 Streamable HTTP。
5. **审批粒度与协作模式混为一谈**。`tool_approval`（ask/auto/yolo）和协作模式（normal/plan/goal）是两维，旧 `default/auto` 是两维耦合的旧值，新写法分别设置。

## 常见问题

**Q: ACP 和 MCP 到底什么关系？**
A: 两套协议分工不同：MCP 是「Agent ↔ 工具服务」（agent 怎么调外部工具，见[[DeepSeek-Reasonix MCP 使用指南]]）；ACP 是「编辑器 ↔ Agent」（编辑器怎么驱动一个 agent 会话）。编辑器经 ACP 发指令，agent 在会话里经 MCP 调工具。

**Q: VS Code 扩展是怎么接进来的？**
A: 扩展先装 CLI，然后启动本地 `reasonix acp` 子进程作为后端，扩展自身是 ACP 客户端 + 编辑器 UI（文件 diff、审批按钮、终端）。安装路径见第 1 章。

**Q: `tool_approval` 三档对应什么？**
A: `ask`（逐步审批）/ `auto`（自动批准常规操作）/ `yolo`（跳过权限），分别对应 Claude Code 的 Ask / Auto / Yolo，经 `session/set_config_option` 设置（字段是 `configId`）。

**Q: 我要在编辑器里挂一个 MCP server，怎么挂？**
A: 在 `session/new`、`session/load` 或 `session/resume` 里带 `mcpServers` 字段即可（MCP over ACP）。stdio 的 `env` 与 HTTP 的 `headers` 用 `[{"name":"...","value":"..."}]` 形状，`${VAR}` 由项目 `.env` 展开。

## 相关文档

- [[DeepSeek-Reasonix CLI 完整参考]] — `reasonix acp` 命令与启动参数
- [[DeepSeek-Reasonix MCP 使用指南]] — MCP over ACP 的 `mcpServers` 与会话消息
- [[DeepSeek-Reasonix 插件与扩展开发]] — Extension Protocol 与 Sidecar 扩展
- [[DeepSeek-Reasonix 会话与交互]] — 会话模型与权限模式语义

## 参考资料

- [esengine/DeepSeek-Reasonix 官方仓库](https://github.com/esengine/DeepSeek-Reasonix)
- `main-v2/docs/ACP.md`（+ `ACP.zh-CN.md`）：ACP v1、能力协商、session 生命周期、协作模式与工具审批
- `v1/docs/CLI-REFERENCE.md` 与 `main-v2/docs/CLI.zh-CN.md`：`reasonix acp` 命令
- 对齐 PR（Ask/Auto/Yolo ↔ `configOptions.tool_approval`）：https://github.com/esengine/DeepSeek-Reasonix/pull/6431

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-08-10 | 创建初稿（高级功能篇第 11 章，ACP 协议指南） |
