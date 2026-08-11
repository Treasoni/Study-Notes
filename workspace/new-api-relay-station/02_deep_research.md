# 搭建 AI API 中转站（new-api） - 深度资料收集

收集时间: 2026-08-12
项目: new-api-relay-station
工作流: learning-note-flow（阶段 2：深度收集）
学习方向: A. 从零搭建 + 上手使用
信源构成: 官方文档（GitHub README / docs.newapi.pro / new-api-docs）为主，DeepWiki 源码解析、技术博客、社区讨论、GitHub Issues 为辅

---

## 一、资料质量概览

| 维度 | 官方文档 | 技术博客/教程 | 社区/GitHub | 说明 |
|------|---------|--------------|-------------|------|
| 部署（Docker/Compose） | 4 篇 | 2 篇 | 1 篇 | 官方 README + docs 部署文档覆盖完整 |
| 渠道配置 | 2 篇 | 1 篇 | 1 篇 | 官方渠道文档 + DeepWiki 源码解析 |
| 令牌与客户端接入 | 3 篇 | 2 篇 | 2 篇 | 官方令牌文档、倍率设置、Cherry Studio 官方接入 |
| 避坑与运维 | 2 篇 | 1 篇 | 3 篇 | 官方 FAQ、Issue #2659、PR #2663 |

共 12+ 条权威信源，官方占比高，足以支撑大纲与章节写作。

---

## 二、核心概念（术语表）

| 术语 | 含义 |
|------|------|
| 中转站 | 聚合多上游模型、统一对外提供 OpenAI 兼容 API 的网关服务 |
| 渠道（Channel） | new-api 对接一个上游服务商的最小配置单元：封装上游 Key、BaseURL、可服务模型、分组、路由属性 |
| 令牌（Token） | 分发给下游调用的认证凭证，格式 `sk-{base_key}[-{channel_id}]`，OpenAI 兼容鉴权 |
| 模型映射（ModelMapping） | 入站模型名 → 上游实际模型名的 JSON 单向改写 |
| 分组（Group） | 用户/令牌/渠道共有的路由隔离维度，默认 `default` |
| 额度（Quota） | 1 美元 = 500,000 配额点数；账户余额是扣费来源，令牌额度是子限制 |
| 预消费/后消费 | 调用前按预估 token 预扣，完成后按实际重新计算多退少补 |
| Ability 路由表 | 按 (模型, 分组) 预计算渠道索引，请求按此表选路 |
| 自动禁用（AutoBan） | 渠道连续错误达阈值后自动拉黑（状态 3），不再参与路由 |

---

## 三、部署深度素材

### 3.1 前置要求

- 操作系统：64 位 Linux（Ubuntu/CentOS/Debian），**不支持 32 位**。
- Docker + Docker Compose 必需（单容器或 compose 两种方式都基于 Docker）。
- 内存：单容器 SQLite 约 1 GB 可运行；MySQL/Redis 完整版建议 2 GB+。
- 磁盘：建议 10 GB+（镜像 + `/data` 数据 + 日志）。
- 域名：非必需；自用 `http://IP:3000` 直连即可。

### 3.2 安装 Docker（Ubuntu 示例）

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo systemctl enable --now docker
docker --version && docker compose version
```

易错点：旧版命令是 `docker-compose`（横杠），新版是 `docker compose`（空格）；报 `docker: 'compose' is not found` 需 `sudo apt install docker-compose-plugin`。

### 3.3 单容器快速部署（SQLite，个人自用）

```bash
docker run --name new-api -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v ./data:/data \
  calciumion/new-api:latest
```

- `-v ./data:/data`：**必须挂载**，否则容器重建数据全丢。
- 端口冲突：改冒号**左边**为宿主机端口，如 `-p 3480:3000`，右边容器端口 3000 不动。

### 3.4 Docker Compose 完整版（生产推荐，PostgreSQL + Redis）

```yaml
version: '3.4'

services:
  new-api:
    image: calciumion/new-api:latest
    container_name: new-api
    restart: always
    command: --log-dir /app/logs
    ports:
      - '3000:3000'
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    environment:
      - SQL_DSN=postgresql://root:123456@postgres:5432/new-api
      - REDIS_CONN_STRING=redis://redis
      - TZ=Asia/Shanghai
      - ERROR_LOG_ENABLED=true
      - BATCH_UPDATE_ENABLED=true
      - SESSION_SECRET=你的随机串
    depends_on:
      - redis
      - postgres
    healthcheck:
      test: ["CMD-SHELL", "wget -q -O - http://localhost:3000/api/status | grep -o '\"success\":\\s*true' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:latest
    container_name: redis
    restart: always

  postgres:
    image: postgres:15
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123456
      POSTGRES_DB: new-api
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

管理命令：

```bash
docker compose up -d          # 后台启动
docker compose ps             # 查看状态
docker compose logs -f        # 跟踪日志
docker compose logs --tail=100 new-api
docker compose down           # 停止（保留数据卷）
docker compose down -v        # 慎用：连数据卷一起删
```

### 3.5 首次启动初始化

1. 浏览器访问 `http://服务器IP:3000`，自动跳转初始化页。
2. 设置管理员账号 + 密码（官方**无内置默认账号**；社区流传 root/123456 因版本而异）。
3. 选择使用模式：
   - **自用模式**：个人使用，**不需给模型定价**，推荐。
   - **对外服务模式**（默认）：需为每个模型设置价格，否则模型不可用（最常见翻车点）。
   - **演示站点模式**：熟悉操作。
4. 点「初始化系统」，登录。

### 3.6 验证部署

```bash
curl -s http://localhost:3000/api/status
# 期望返回 "success": true
docker compose ps   # new-api healthy
```

---

## 四、渠道配置深度素材

### 4.1 渠道概念

每条渠道封装：上游 Key、BaseURL、可服务模型、允许路由的用户组、路由属性（Priority/Weight）、状态。
请求**只会分发到「一个」渠道**，靠 Ability 表按 (模型, 分组) 选路。

渠道状态：`1` 启用 / `2` 手动禁用 / `3` 自动禁用（AutoBan 触发）。

常见渠道类型：OpenAI(1)、Azure OpenAI(3)、Ollama(4)、自定义 OpenAI 兼容(8)、Anthropic Claude(14)、阿里云百炼(17)、OpenRouter(20)、Google Gemini(24)、Moonshot Kimi(25)、MiniMax(35)、DeepSeek(43)。

> 易错点：对接没有专属选项的服务商时，类型选 **OpenAI**（大多数服务商兼容 OpenAI 协议）。

### 4.2 添加渠道字段

| 字段 | 作用 | 易错点 |
|------|------|--------|
| Type | 上游通信协议适配器 | 选错无法通信 |
| Key | 上游认证凭据，支持多 Key 换行/JSON 数组 | 格式因服务商而异 |
| BaseURL | 覆盖默认地址 | **不要带结尾 /v1 或 /** |
| Models | 可服务模型列表 | 漏勾 = 该模型「无可用渠道」 |
| Group | 允许路由的用户组，默认 default | 与令牌/用户组对不上会无渠道 |
| Priority | 优先级，越高越先 | 高优失败会降级到低优 |
| Weight | 同优先级加权随机 | 权重 0 也可被选中 |
| ModelMapping | 入站→上游模型名改写（JSON） | 单向改写，不会让模型「存在」 |
| AutoBan | 连续错误自动禁用 | 建议开启 |

配置示例（OpenAI / DeepSeek / 自定义中转）：

```text
Type:       OpenAI（或 DeepSeek）
Name:       OpenAI-主
Key:        sk-xxxx（多 Key 换行）
BaseURL:    https://api.deepseek.com（标准服务商可留空；不带 /v1）
Models:     gpt-4o,gpt-4o-mini 或 deepseek-chat,deepseek-reasoner
Group:      default
Priority:   10
Weight:     100
AutoBan:    ✅ 开启
```

### 4.3 多 Key 池

- 一个渠道可放多个 Key：换行分隔或 JSON 数组 `["k1","k2"]`。
- 轮询模式：Round Robin 或加权随机。
- 单 Key 失败自动跳过，恢复后自动重新启用。

### 4.4 「无可用渠道」根因（三类）

1. **模型列表没对上**：渠道 Models 里没这个模型名。
2. **分组没对上**：请求令牌/用户所在组不在渠道 Group 列表。
3. **渠道被禁用**：状态 2 或 3。

特殊组 `auto`：令牌组设 auto 会遍历用户所有授权组找可用渠道。

### 4.5 测试渠道

- 单测：渠道列表「测试」按钮；批量：「测试所有渠道」。
- 报错 `invalid character '<'` = 上游返回 HTML 而非 JSON（BaseURL 指错/被 CDN 或反代拦截返回页面）。

---

## 五、令牌与客户端接入深度素材

### 5.1 令牌概念

- 格式 `sk-{base_key}[-{channel_id}]`；`-{channel_id}` 仅管理员可用，强制走指定渠道。
- 令牌额度（RemainQuota）≠ 账户余额：令牌额度是「最大消耗上限」，账户余额是扣费来源。
- 令牌额度耗尽 → 状态 `Exhausted(4)` → 报「额度不足」。
- **令牌 Key 只在创建成功弹窗完整显示一次**，必须当场复制。

令牌状态：`1 启用 / 2 禁用 / 3 过期 / 4 耗尽`。

### 5.2 创建令牌字段

| 字段 | 含义 |
|------|------|
| 名称 | 用途标注（≤50 字符） |
| 过期时间 | 留空或 -1 永不过期 |
| 剩余配额 | 最大消耗上限（可无限配额） |
| 无限配额 | 绕过令牌额度检查（仍受账户总配额约束） |
| 模型限制 ModelLimits | 白名单：只能调指定模型 |
| IP 白名单 | 限定来源 IP/CIDR，换行分隔 |
| 分组 | 该令牌走的渠道分组；设 auto 启用多分组自动切换 |

### 5.3 接入第三方客户端（通用三要素）

| 客户端 | Base URL | API Key | 模型名 |
|--------|----------|---------|--------|
| NextChat | 站点地址（或 /v1，配 BASE_URL 环境变量） | `sk-...` | 自定义模型写 `+模型名@OpenAI` |
| Cherry Studio | 站点地址（官方内置 NewAPI 类型） | `sk-...` | 手动添加模型 ID |
| ChatBox | `https://站点/v1` | `sk-...`（不要加 Bearer） | 手动填模型 ID |
| LobeChat | `https://站点/v1` | `sk-...` | 手动添加模型 ID |
| Claude Code | `ANTHROPIC_BASE_URL=https://站点` | `ANTHROPIC_API_KEY=sk-...` | `/model` 选择 |

**Claude 模型的坑**：NextChat 识别 `claude-*` 会默认走 Anthropic 原生协议（x-api-key 头）→ 报错。解决：自定义模型写 `+claude-3-5-sonnet-20241022@OpenAI`，并选下拉列表里标注 `(OpenAI)` 的项。

连接测试（推荐先做）：

```bash
curl -sS https://your-new-api.com/v1/models -H "Authorization: Bearer sk-xxxx"
```

### 5.4 额度计算

```
配额消耗 = (输入token数 + 输出token数 × 补全倍率) × 模型倍率 × 分组倍率
```

- 模型倍率示例：gpt-4o=1.25、gpt-4o-mini=0.075。
- 补全倍率：gpt-4o=4、gpt-3.5-turbo=2。
- 1 美元 = 500,000 配额点数。
- 自用场景开「自用模式」，未配置倍率走默认值。

「额度不足」排查：① 令牌剩余额度（最常见）② 账户余额 ③ 模型/分组倍率 ④ 429 频率限制。

---

## 六、避坑与运维深度素材

### 6.1 高频报错速查

| 报错 | 原因 | 处理 |
|------|------|------|
| 「无可用渠道」/ model_not_found | 模型列表、分组、渠道状态三类原因 | 核对三者一致；模型名完全一致 |
| 有余额仍 insufficient_quota | 令牌额度耗尽/倍率未配/预消费估算超限 | 查令牌额度；配倍率；自用开自用模式 |
| invalid character '<' | 上游返回 HTML（BaseURL 指错/被 CF 拦截） | 换出口 IP；核对 BaseURL |
| 分组负载饱和 | 上游 429 限流 | 加限速、降权重、加同优渠道、自动禁用 |
| 倍率或价格未配置 | 模型未配价格 | 补配或开自用模式 |

### 6.2 重试与自动禁用

- **重试只对特定 HTTP 状态码生效**（默认 429 和部分 5xx；400/408/504/524 不重试）。`exhausted`/`insufficient_quota` 非 429 会直接透传不重试（Issue #2659；PR #2663 已将「自动重试状态码」可配置化）。
- **自动禁用关键词兜底**（系统设置 → 运营设置）：匹配错误文本自动禁用渠道。官方默认词：`Your credit balance is too low`、`You exceeded your current quota`、`insufficient_quota` 等；中文可加 `剩余额度`、`用户额度不足`、`该令牌额度已用尽`。
- 配套推荐：失败自动禁用 + 成功自动启用 + 定期渠道测试 + 渠道优先级分层。

### 6.3 数据备份与升级

| 事项 | 操作 |
|------|------|
| SQLite 备份 | `cp -r ./data ./data.bak`（升级前） |
| MySQL 备份 | `mysqldump -u root -p new-api > new-api.sql` |
| Compose 升级 | `docker compose pull && docker compose down && docker compose up -d` |
| 单容器升级 | `docker pull calciumion/new-api:latest`，用相同挂载/参数重建 |
| 是否丢数据 | 挂载 volume 就不丢；**没挂 /data 容器重建即丢** |

### 6.4 安全加固（零基础版）

1. 登录后立即**改管理员密码 + 改用户名**（默认 root/admin 易被爆破）。
2. **关闭开放注册**（系统设置 → 允许注册 = 关闭）。
3. 设置固定 `SESSION_SECRET`：
   ```bash
   openssl rand -hex 16
   ```
   写进 compose environment。不设置会每次重启生成新密钥 → 全员掉登录。
4. **不要直接暴露 3000 到公网**，用 Nginx/Caddy + HTTPS 反代。

Nginx 最小反代（SSE 流式三件套 + 长超时）：

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    ssl_certificate     /etc/nginx/ssl/api.example.com.pem;
    ssl_certificate_key /etc/nginx/ssl/api.example.com.key;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;

        proxy_connect_timeout 600s;
        proxy_read_timeout    600s;
        proxy_send_timeout    600s;
        client_max_body_size  64m;
    }
}
```

Caddy 更省事（自动 HTTPS）：`api.example.com { reverse_proxy 127.0.0.1:3000 }`

---

## 七、零基础从 0 到 1 完整步骤（合成）

1. 准备 64 位 Linux 服务器（内存 1GB+），安装 Docker + Compose。
2. 选部署方式：自用 → 单容器 SQLite；生产/对外 → Compose 完整版。
3. 启动后访问 `http://IP:3000`，初始化向导创建管理员账号，选「自用模式」。
4. 立即改密、改用户名、关闭开放注册、设置 SESSION_SECRET。
5. 添加第一个渠道（选类型 → 填 Key → 选模型 → 分组 default → 提交 → 测试）。
6. 创建令牌（设额度/模型白名单/分组），当场复制 `sk-...`。
7. `curl /v1/models` 验证。
8. 接入客户端（NextChat/Cherry Studio/ChatBox 等），配 Base URL / API Key / 模型名。
9. 若对外：Nginx/Caddy + HTTPS 反代，配置自动禁用关键词兜底。
10. 日常：`docker compose logs` 看日志，`docker compose pull && up -d` 升级，先备份再升级。

---

## 八、权威信源清单

1. new-api 官方仓库 README — https://github.com/QuantumNous/new-api
2. 官方文档站 — https://docs.newapi.pro/
3. 官方部署：Docker 单容器 — https://docs.newapi.pro/en/docs/installation/deployment-methods/docker-installation
4. 官方部署：Docker Compose — https://docs.newapi.pro/en/docs/installation/deployment-methods/docker-compose-installation
5. 官方 compose 配置详解（SESSION_SECRET 等） — https://docs.newapi.pro/zh/docs/installation/config-maintenance/docker-compose-yml
6. 官方 FAQ — https://docs.newapi.pro/zh/docs/support/faq
7. 官方渠道管理 — https://docs.newapi.pro/zh/docs/guide/feature-guide/admin/channel
8. 官方令牌管理 — https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token
9. 官方倍率设置 — https://docs.newapi.pro/zh/docs/guide/console/settings/rate-settings
10. 官方 Cherry Studio 接入 — https://docs.newapi.pro/zh/docs/apps/cherry-studio
11. DeepWiki: Channel Management — https://deepwiki.com/QuantumNous/new-api/3-channel-management
12. DeepWiki: API Tokens — https://deepwiki.com/QuantumNous/new-api/6.2-api-tokens
13. GitHub Issue #2659（exhausted 不重试） — https://github.com/QuantumNous/new-api/issues/2659
14. PR #2663（自动重试状态码可配置） — https://github.com/QuantumNous/new-api/pull/2663
15. 腾讯云 Docker 搭建教程 — https://cloud.tencent.com.cn/developer/article/2632560
16. linux.do NextChat 接入排障 — https://linux.do/t/topic/176116
