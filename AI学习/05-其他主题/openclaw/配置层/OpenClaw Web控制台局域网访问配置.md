---
tags: [openclaw, web, 局域网, control-ui, cors]
created: 2026-03-03
updated: 2026-03-03
---

# OpenClaw Web 控制台局域网访问配置

> [!info] 概述
> **OpenClaw Web 控制台默认只能本机访问，局域网设备访问需要解决三大安全障碍**。本文档提供完整的配置指南，帮助你安全地让局域网设备连接到 OpenClaw。

## 核心概念

### 什么是 Control UI

OpenClaw Control UI 是一个基于 **Vite + Lit** 的单页应用，由 Gateway 在同一端口提供：

```
默认地址：http://127.0.0.1:18789/
可选前缀：gateway.controlUi.basePath（如 /openclaw）
```

它通过 **WebSocket** 直接与 Gateway 通信。

> [!quote] 官方文档
> "The Control UI is a small Vite + Lit single-page app served by the Gateway."
> — [OpenClaw Web 文档](https://docs.openclaw.ai/web)

### 默认访问方式

| 场景 | 访问地址 | 状态 |
|------|----------|------|
| 本机访问 | `http://127.0.0.1:18789/` | ✅ 自动批准 |
| 本机访问 | `http://localhost:18789/` | ✅ 自动批准 |
| 局域网访问 | `http://192.168.x.x:18789/` | ❌ 需要配置 |

### 局域网访问的挑战

```
┌─────────────────────────────────────────────────────────────┐
│              OpenClaw 安全机制（三层防护）                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  第一层：CORS（跨域）限制                                     │
│  ├─ 默认只允许 loopback 来源                                 │
│  └─ 解决：设置 allowedOrigins                               │
│                                                             │
│  第二层：安全上下文（WebCrypto）                              │
│  ├─ HTTP 非 localhost 会被浏览器阻止                         │
│  └─ 解决：allowInsecureAuth 或 HTTPS                        │
│                                                             │
│  第三层：设备配对（Device Pairing）                          │
│  ├─ 新设备需要手动批准                                       │
│  └─ 解决：openclaw devices approve                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 一、局域网访问三大障碍

### 1.1 CORS（跨域）限制

**错误信息**：
```
origin not allowed (open the Control UI from the gateway host
or allow it in gateway.controlUi.allowedOrigins)
```

**原因**：OpenClaw 默认只允许本机访问，非 loopback 模式必须显式设置允许的来源。

> [!quote] 官方文档
> "Non-loopback Control UI deployments must set `gateway.controlUi.allowedOrigins` explicitly (full origins)."

### 1.2 HTTP 非安全上下文

**错误信息**：
```
control ui requires device identity (use HTTPS or localhost secure context)
```

**原因**：HTTP 连接（非 localhost）是"非安全上下文"，浏览器会阻止 WebCrypto API，导致无法生成设备身份。

> [!quote] 官方文档
> "If you open the dashboard over plain HTTP, the browser runs in a non-secure context and blocks WebCrypto. By default, OpenClaw blocks Control UI connections without device identity."

### 1.3 设备配对要求

**错误信息**：
```
disconnected (1008): pairing required
```

**原因**：即使是同一 Tailnet，新设备首次连接也需要一次性配对批准。

> [!quote] 官方文档
> "When you connect to the Control UI from a new browser or device, the Gateway requires a one-time pairing approval — even if you're on the same Tailnet."

---

## 二、完整解决方案

### 方案一：HTTP + 完整配置（测试环境）

适用于内网测试环境，需要配置三个参数：

```bash
# 1. 设置允许的来源（JSON 数组格式）
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.100:18789"]'

# 2. 允许不安全的 HTTP 认证
openclaw config set gateway.controlUi.allowInsecureAuth true

# 3. 设置 Gateway 绑定模式
openclaw config set gateway.bind lan

# 4. 重启服务
openclaw restart
```

**配置文件示例** (`~/.openclaw/openclaw.json`)：

```json
{
  "gateway": {
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": ["http://192.168.1.100:18789"],
      "allowInsecureAuth": true
    },
    "auth": {
      "mode": "token",
      "token": "your-token-here"
    }
  }
}
```

> [!warning] 安全提示
> `allowInsecureAuth` 不会绕过设备配对检查，只是允许 HTTP 上下文中的认证。

### 方案二：Tailscale Serve + HTTPS（推荐）

**生产环境推荐**：使用 Tailscale Serve 提供 HTTPS，无需额外配置：

```bash
# 启动 Gateway 并启用 Tailscale Serve
openclaw gateway --tailscale serve
```

**访问地址**：
```
https://<your-tailscale-name>.ts.net/
```


> [!warning]
> ⚠️  使用这个网址时，最好把翻墙软件和代理关闭，否则会访问失败


```

**优势**：
- ✅ 自动 HTTPS（安全上下文）
- ✅ 无需 CORS 配置
- ✅ 可通过 Tailscale 身份认证（`gateway.auth.allowTailscale: true`）

**配置文件**：

```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": { "mode": "serve" },
    "auth": { "allowTailscale": true }
  }
}
```

> [!info] 来源
> - [OpenClaw Web 文档](https://docs.openclaw.ai/web) - Tailscale access
> - [OpenClaw Control UI 文档](https://docs.openclaw.ai/web/control-ui) - Tailnet access

#### 方案二补充：Tailscale HTTPS 域名的 CORS 配置

如果使用 Tailscale Funnel/Serve 暴露服务，仍可能遇到 CORS 错误：

```
origin not allowed (open the Control UI from the gateway host
or allow it in gateway.controlUi.allowedOrigins)
```

**原因**：Tailscale 提供的 HTTPS 域名（如 `https://openclaw.tail8a3e67.ts.net`）也需要添加到 CORS 白名单。

**解决方法**：

```bash
# 1. 将 Tailscale 域名添加到允许列表
# 注意：必须带 https:// 前缀，用单引号包裹 JSON 数组
openclaw config set gateway.controlUi.allowedOrigins '["https://openclaw.tail8a3e67.ts.net"]'

# 2. 重启网关
openclaw gateway stop
openclaw gateway --tailscale serve
```

> [!tip] 提示
> - 这里的 `openclaw` 是你的 Tailscale 机器名（hostname）
> - `tail8a3e67` 是你的 tailnet 名称
> - 可以通过 `tailscale status` 查看完整的域名
> - 必须开启tailscale的https功能

### 方案三：危险模式（仅调试）

**仅用于紧急故障排查**，会严重降低安全性：

```bash
# 禁用设备身份检查（危险！）
openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
openclaw restart
```

> [!danger] 严重警告
> `dangerouslyDisableDeviceAuth` 禁用 Control UI 设备身份检查，是**严重安全降级**。
> 紧急用完后**立即恢复**！

---

## 三、设备配对流程

### 3.1 首次连接

从新设备访问时，会看到：
```
disconnected (1008): pairing required
```

### 3.2 批准设备

在 Gateway 主机上执行：

```bash
# 1. 列出待批准的请求
openclaw devices list

# 输出示例：
# Request ID                               Device Name    Status
# abc123-def456-ghi789                     Chrome on Mac  pending

# 2. 批准设备
openclaw devices approve <request-id>

# 例如：
openclaw devices approve abc123-def456-ghi789
```

### 3.3 设备配对说明

| 连接类型 | 是否需要配对 | 说明 |
|----------|--------------|------|
| 本机 (`127.0.0.1`) | ❌ 自动批准 | 无需操作 |
| 局域网 (LAN) | ✅ 需要配对 | 每个新设备首次需要批准 |
| Tailnet | ✅ 需要配对 | 即使同一 Tailnet 也需要批准 |

> [!note] 注意
> - 每个浏览器配置文件生成唯一的设备 ID
> - 切换浏览器或清除浏览器数据需要重新配对
> - 已批准的设备会被记住，除非手动撤销

### 3.4 管理已批准设备

```bash
# 查看所有已批准设备
openclaw devices list

# 撤销设备访问权限
openclaw devices revoke --device <device-id> --role <role>
```

---

## 四、配置清单

### 完整配置命令（HTTP 模式）

```bash
# === 必需配置 ===

# 1. 设置 Gateway 绑定模式（lan 或 0.0.0.0）
openclaw config set gateway.bind lan

# 2. 设置允许的来源（替换为你的 IP）
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.100:18789"]'

# 3. 允许 HTTP 认证
openclaw config set gateway.controlUi.allowInsecureAuth true

# 4. 设置认证 Token
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"

# === 重启生效 ===
openclaw restart

# === 获取访问 Token ===
openclaw dashboard --no-open
```

### bind 模式说明

| 模式 | 说明 | 访问地址 |
|------|------|----------|
| `loopback` (默认) | 仅本机访问 | `http://127.0.0.1:18789` |
| `lan` | 局域网访问 | `http://[局域网IP]:18789` |
| `tailnet` | Tailscale 网络 | `http://[Tailscale IP]:18789` |
| `0.0.0.0` | 所有接口 | `http://[任意IP]:18789` |

---

## 五、访问流程总结

```
┌─────────────────────────────────────────────────────────────┐
│                  局域网访问完整流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 配置 Gateway                                            │
│     ├─ gateway.bind = "lan"                                │
│     ├─ gateway.controlUi.allowedOrigins = [...]            │
│     └─ gateway.controlUi.allowInsecureAuth = true          │
│                                                             │
│  2. 重启服务                                                │
│     └─ openclaw restart                                    │
│                                                             │
│  3. 获取 Token                                              │
│     └─ openclaw dashboard --no-open                        │
│                                                             │
│  4. 局域网设备访问                                          │
│     └─ http://192.168.x.x:18789/?token=xxx                 │
│                                                             │
│  5. 设备配对（首次）                                         │
│     ├─ 看到 "pairing required"                             │
│     ├─ 在主机执行 openclaw devices list                    │
│     └─ 执行 openclaw devices approve <id>                  │
│                                                             │
│  6. 完成！可以正常使用                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 六、常见问题

### Q1：配置后仍然显示 "origin not allowed"？

检查 `allowedOrigins` 格式，必须是 **JSON 数组**：

```bash
# ❌ 错误格式
openclaw config set gateway.controlUi.allowedOrigins "http://192.168.1.100:18789"

# ✅ 正确格式（JSON 数组）
openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.100:18789"]'
```

### Q2：如何允许多个来源？

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://localhost:18789","http://127.0.0.1:18789","http://192.168.1.100:18789"]'
```

### Q3：配置后仍然显示 "requires device identity"？

确保已设置 `allowInsecureAuth`：

```bash
openclaw config set gateway.controlUi.allowInsecureAuth true
openclaw restart
```

### Q4：如何查看当前配置？

```bash
# 查看所有配置
openclaw config list

# 查看特定配置
openclaw config get gateway.controlUi
```

### Q5：如何重置配置？

```bash
# 编辑配置文件
nano ~/.openclaw/openclaw.json

# 或重置特定项
openclaw config set gateway.controlUi.allowedOrigins '[]'
```

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **三层安全机制**：OpenClaw 的安全设计很严格，CORS + 安全上下文 + 设备配对三重保护
>
> 2. **推荐方案**：
>    - 测试环境：HTTP + allowInsecureAuth
>    - 生产环境：Tailscale Serve + HTTPS
>
> 3. **踩坑记录**：
>    - `allowedOrigins` 必须是 JSON 数组格式
>    - 每次修改配置后要 `openclaw restart`
>    - 新设备首次连接需要手动批准
>
> 4. **安全建议**：
>    - 不要在生产环境使用 `dangerouslyDisableDeviceAuth`
>    - 定期更换 Token
>    - 仅允许可信 IP 访问

---

## 相关文档

- [[../OpenClaw MOC]] - OpenClaw 文档索引
- [[OpenClaw安装后配置指南]] - 配置指南
- [[../../02-工具使用/Tailscale使用指南]] - Tailscale VPN 组网

---

## 参考资料

### 官方资源

- [OpenClaw Web 文档](https://docs.openclaw.ai/web) - Gateway Web 配置
- [OpenClaw Control UI 文档](https://docs.openclaw.ai/web/control-ui) - 控制台详细说明
- [OpenClaw Remote Access 文档](https://docs.openclaw.ai/gateway/remote) - 远程访问配置
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 源代码

### 相关技术

- [Tailscale 官网](https://tailscale.com) - VPN 组网服务
- [MDN - 安全上下文](https://developer.mozilla.org/zh-CN/docs/Web/Security/Secure_Contexts) - 浏览器安全机制

---

**最后更新**：2026-03-03
