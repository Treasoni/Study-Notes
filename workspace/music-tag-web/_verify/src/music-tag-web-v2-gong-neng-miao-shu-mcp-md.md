> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/mcp.md).

# MCP

### 什么是 MCP？

MCP（Model Context Protocol，模型上下文协议）是一个开放标准，用于连接 AI 应用（如编程助手、对话机器人）与外部工具、数据源和 API。它定义了统一的 JSON-RPC 通信方式，使得大语言模型可以动态发现并调用外部功能，从而获取实时信息或执行具体操作。

简单来说，MCP 就像是 AI 应用的“USB 接口”——只要你的工具实现了这个协议，任何支持 MCP 的 AI 客户端（如 Codex、Claude Code）都可以直接与它交互，无需为每个工具编写单独的集成代码。

Music Tag Web 现已原生支持 MCP 服务端，你可以通过标准的 MCP 协议，让 AI 助手直接读取、修改和管理音乐文件的元数据标签，实现智能化的音乐库整理。

### 如何使用 Music Tag Web 的 MCP 服务

\
前置准备

1. **确保 Music Tag Web 已启动并正常运行**（默认监听 `http://127.0.0.1:8002`）。
2. **获取 Access Token**（如果启用了鉴权）：
   * 打开 Music Tag Web 前端页面。
   * 进入 **系统设置 → API 管理 → 认证管理**。
   * 找到 **Access Token**，点击生成或复制已有值。

#### MCP 地址

Music Tag Web 内置了 HTTP MCP 端点，默认地址为：

```
http://你的域名或IP:端口/mcp/
```

* `GET /mcp/` – 检查服务是否在线
* `GET /mcp/meta/status/` – 查看运行时状态
* `GET /mcp/meta/tools/` – 获取所有可用工具清单

其他可用端点（用于检查状态或工具清单）

#### 鉴权说明

MCP 请求需要在 HTTP 头中携带 Access Token，格式为：

text

```
Authorization: Bearer <你的access_token>
```

* 如果系统中 `access_token` 未设置（为空），则 `/mcp/` 不会强制鉴权，但生产环境建议务必配置。
* 配置了 `access_token` 后，所有 `GET /mcp/` 和 `POST /mcp/` 请求都必须携带正确的 Authorization 头。

#### 快速测试（curl）

**无鉴权情况（未设置 access\_token）**

bash

```
curl -X POST http://127.0.0.1:8002/mcp/ \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'
```

**有鉴权情况（已设置 access\_token）**

bash

```
curl -X POST http://127.0.0.1:8002/mcp/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-access-token' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'
```

如果只需检查端点是否可达：

bash

```
curl http://127.0.0.1:8002/mcp/ -H 'Authorization: Bearer your-access-token'
```

成功返回后，说明 MCP 服务已就绪。

***

### 在 AI 客户端中配置 MCP

#### 1. **手动编辑配置文件**（`~/.codex/config.toml` 或项目内的 `.codex/config.toml`）：

toml

```
[mcp_servers.music-tag]
url = "http://127.0.0.1:8002/mcp/"
http_headers = { "Authorization" = "Bearer 9lSCu8N69U8iF46woU6dmEqgECbs6cB2" }

```

然后在 codex cli 中输入 /mcp 出现以下内容代表 mcp 生效了。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FLjVUVMjoIp8JNpVYoj19%2Fimage.png?alt=media&amp;token=6260cb1d-b966-4672-ab26-f288ef8e81f5" alt=""><figcaption></figcaption></figure>

#### 2. 在 Claude Code 中配置（Anthropic）

**项目共享配置（`.mcp.json`）**：

在项目根目录创建 `.mcp.json` 文件，内容如下：

json

```
{
  "mcpServers": {
    "music-tag-web": {
      "type": "http",
      "url": "http://127.0.0.1:8002/mcp/",
      "headers": {
        "Authorization": "Bearer ${MUSIC_TAG_MCP_TOKEN}"
      }
    }
  }
}
```

* `local` 作用域：默认只对当前机器的当前项目生效。
* `project` 作用域：会将配置写入项目根目录的 `.mcp.json`，适合团队共享。

> 如果当前 Music Tag Web 实例没有设置 `access_token`，可以省略 `headers` 字段。但不建议在生产环境中这样做。

<br>

<br>
