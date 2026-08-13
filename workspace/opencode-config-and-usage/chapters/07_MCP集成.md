# 第七章：MCP 集成——把外部工具接进来

**本章问题**：在 Claude Code 里你已经习惯了 `claude mcp add/list/get`，到了 opencode 如何把同一套 MCP server 接进来？本章讲清 opencode 的 `mcp` 配置键、local/remote 两种类型、`command` 数组与 `environment` 键、OAuth 三种模式，以及从 `mcpServers` 迁移的完整对照。

## mcp 配置键与两种类型（local / remote）

opencode 在 `opencode.json` 中用顶层 `mcp` 键声明 MCP server（Claude Code 对应 `mcpServers`）[opencode MCP 文档](https://opencode.ai/docs/mcp)。与 Claude Code 最大的不同是：**每一项必须带 `type` 字段**，用来区分两种传输方式：

- `local`：以子进程方式启动（STDIO 协议）。server 作为本地子进程运行，与 opencode 通过标准输入输出通信。适合跑在本机的工具，如文件系统、Git 辅助工具。
- `remote`：以 HTTP/SSE 协议连接远程 URL。server 部署在远端，通过 `url` 访问，适合多人共享的工具服务。

[!tip] 大白话
把 MCP server 想成「智能家电的插线板」：opencode 不内置这些技能，但通过统一插口把外部能力接进来。`local` 是把一个助手直接请进家里住（子进程，走内部的传话管道 STDIO）；`remote` 是打电话给远端的客服中心（HTTP/SSE）。

### local 配置示例

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "environment": { "NODE_ENV": "production" },
      "timeout": 30000
    }
  }
}
```

### remote 配置示例

```json
{
  "mcp": {
    "remote-tools": {
      "type": "remote",
      "url": "https://mcp.example.com/v1",
      "headers": { "X-API-Key": "sk-..." }
    }
  }
}
```

## command 数组与 environment 环境变量

两个与 Claude Code 直接冲突的写法，迁移时最容易踩坑：

1. **`command` 用数组，不用字符串**。Claude Code 里 `"command": "npx -y @modelcontextprotocol/server-filesystem /tmp"` 是整条 shell 命令；opencode 要求拆成 `["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"]`。这样做是为了避免 shell 注入——参数不经过 shell 解析，原样传给子进程。
2. **环境变量键叫 `environment`，不叫 `env`**。Claude Code 用 `env`，opencode 用 `environment`。

[!tip] 大白话
`command` 用数组就像餐厅点菜：Claude Code 是「你对着厨房喊一嗓子」——喊话内容会被完整转述（存在歧义和注入风险）；opencode 是把菜名逐个写在单子上递给厨房——每道菜都是独立的一项，不存在被「带偏」的解析空间。

`timeout` 默认 30000ms（30 秒），超过即视为子进程启动失败；遇到首次 `npx` 拉包较慢时可适当调大。语义与 Claude Code 的 `claude mcp add --timeout` 一致。

### 实战：把一条 `claude mcp add` 迁移过来

假设你在 Claude Code 里跑过这条命令：

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /tmp --env NODE_ENV=production
```

迁移到 opencode 分三步：把键名换成 `mcp`、补上 `"type": "local"`、把 command 和 env 按新格式改写。注意 `claude mcp add` 里的 `--env` 是命令参数，而 opencode 要求放在 `environment` 块里：

```json
{
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "environment": { "NODE_ENV": "production" },
      "timeout": 30000
    }
  }
}
```

相比 Claude Code 把配置写进 `.mcp.json`，opencode 的 `mcp` 块直接落在 `opencode.json`，因此能享受第 3 章讲过的 8 层配置优先级——例如项目级覆盖全局、不同项目可以各自声明不同的 server。

## OAuth 三种模式与 token 存储

远程 MCP server 往往需要认证。opencode 内建 OAuth 流程，支持三种模式 [opencode MCP 文档](https://opencode.ai/docs/mcp)：

| 模式 | 配置 | 说明 |
|------|------|------|
| 自动发现（默认） | 不配置 `oauth` | 按 RFC 7591 动态注册客户端，自动走 OAuth 授权流程 |
| 预注册客户端 | `"oauth": { "clientId": "..." }` | server 要求固定 clientId，跳过动态注册 |
| 禁用 | `"oauth": false` | 不做 OAuth，改用 API key 等静态凭据认证 |

[!tip] 大白话
OAuth token 像「临时工牌」：进门（连上远程 server）时 opencode 帮你自动申请一张，到期自动换新。`clientId` 是「你有专属工牌编号」；`oauth: false` 是「不用工牌，直接刷门禁卡（API key）」。

**token 存储位置**：`~/.local/share/opencode/mcp-auth.json`，与全局认证凭据 `auth.json` 分开存放。排查授权问题时直接看这个文件。

注意：**用 API key（如 `headers`）认证的远程 server 必须显式 `"oauth": false`**，否则 opencode 默认先尝试 OAuth 流程，可能与你预期的认证方式冲突。这也是排查远程 server「连不上」时优先检查的三件事之一：`type` 是否写对、`url` 是否可达、`oauth` 是否与认证方式匹配。

### local 还是 remote？怎么选

判断依据很简单：server 是否与你的项目运行在同一台机器上。文件系统、Git、数据库扫描这类工具用 `local`（子进程直连，延迟低、无网络暴露）；团队共享的服务、需要集中鉴权的工具用 `remote`（统一部署，客户端只存 URL 与凭据）。如果拿不准，先用 `local` 起步，后续再改为 `remote` 迁移成本很低——两者只是 `type` 与连接字段不同。

## mcp CLI 子命令族与 Claude Code 差异

`opencode mcp` 是一族子命令，比 Claude Code 的 `claude mcp add/list/get` 更完整 [OpenCode GitHub](https://github.com/anomalyco/opencode)：

```bash
opencode mcp list                  # 列出所有 server 及连接状态
opencode mcp debug <name>          # 诊断某个 server 的配置与连接
opencode mcp auth                  # 手动触发 OAuth 授权
opencode mcp logout                # 清除已存的 token
opencode mcp add ...               # 通过 CLI 添加 server（等价于写配置）
```

`mcp list` 用四种状态符号快速定位问题：

- `✓ connected`：已连接可用
- `○ disabled`：已配置但被禁用
- `⚠ needs_auth`：需要授权（未登录或 token 过期）
- `✗ failed`：连接失败，用 `mcp debug` 查原因

遇到 `⚠ needs_auth` 先跑 `opencode mcp auth` 走一遍授权；遇到 `✗ failed` 跑 `opencode mcp debug <name>`，它会打印 server 的解析结果与实际连接错误，比对着配置文件猜高效得多。整个排查闭环与 Claude Code 的 `claude mcp get` + `--verbose` 思路一致，只是命令名不同。

### mcpServers → mcp 迁移对照表

| 维度 | Claude Code | opencode |
|------|-------------|----------|
| 配置键 | `mcpServers` | `mcp`（每项必须带 `type`） |
| command 形式 | 字符串（shell 解析） | 数组（无 shell，防注入） |
| 环境变量键 | `env` | `environment` |
| OAuth | 依赖 server 端 URL 流程 | 内建自动发现（RFC 7591）/ clientId / 禁用 |
| token 存储 | `~/.claude.json` / 浏览器会话 | `~/.local/share/opencode/mcp-auth.json` |
| CLI | `claude mcp add/list/get` | `opencode mcp add/list/debug/auth/logout` |
| 配置落点 | `.mcp.json` / `claude mcp add` 写入 | `opencode.json` 的 `mcp` 键 |

## 本章小结

- opencode 的 `mcp` 键对应 Claude Code 的 `mcpServers`，但每项必须带 `type`（`local` STDIO 子进程 / `remote` HTTP/SSE）。
- `command` 用数组防 shell 注入，环境变量键是 `environment`，`timeout` 默认 30000ms。
- OAuth 三模式：自动发现（默认，RFC 7591）/ 预注册 `clientId` / `oauth: false` 禁用；token 存 `~/.local/share/opencode/mcp-auth.json`。
- `opencode mcp list/debug/auth/logout` 提供完整子命令族，`list` 用四种状态符号快速定位连接问题。

## 下一章预告

外部工具已经接进来了，下一步是把「内部能力」标准化——Skills、自定义 Agent 与 `AGENTS.md`，看它们如何像 Claude Code 的 Skills 与子代理一样被发现和复用。
