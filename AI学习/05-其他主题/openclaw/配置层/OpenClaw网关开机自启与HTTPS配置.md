---
tags: [openclaw, daemon, systemd, tailscale, https, 开机自启]
created: 2026-03-04
updated: 2026-03-04
---

# OpenClaw 网关开机自启与 HTTPS 配置

> [!info] 概述
> **让 OpenClaw 网关在开机时自动启动，并通过 Tailscale 提供 HTTPS 安全访问**。适用于服务器部署、长期运行的场景。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 设置开机自启 | [[#一、开机自启配置]] |
| 用 Tailscale HTTPS | [[#二、Tailscale Serve HTTPS]] |
| 完整配置示例 | [[#三、完整配置示例]] |
| 排查问题 | [[#四、常见问题]] |

---

## 一、开机自启配置

### 是什么

OpenClaw Gateway 守护进程（daemon）是一种后台服务模式，可以让网关在系统启动时自动运行，无需手动启动。

### 为什么需要

| 场景 | 为什么需要开机自启 |
|------|---------------------|
| **服务器部署** | 服务器重启后自动恢复服务 |
| **长期运行** | 无需每次手动启动 |
| **无人值守** | 远程访问时服务始终可用 |
| **稳定性** | 服务异常退出后自动重启 |

### 通俗理解

**🎯 比喻**：就像设置闹钟的"每天重复"功能。开机自启就是让 OpenClaw 在电脑开机时"自动醒过来"开始工作，不需要你每天手动叫它起床。

### 1.1 macOS 配置

#### 方法一：使用 OpenClaw 内置命令（推荐）

```bash
# 安装 launchd 服务（开机自启）
openclaw gateway install

# 或者在配置向导时选择
openclaw onboard --install-daemon
```

#### 方法二：手动创建 plist

创建 `~/Library/LaunchAgents/com.openclaw.gateway.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/openclaw</string>
        <string>gateway</string>
        <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw.err</string>
</dict>
</plist>
```

```bash
# 加载服务
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway.plist

# 验证状态
launchctl list | grep openclaw
```

### 1.2 Linux 配置（systemd）

#### 方法一：使用 OpenClaw 内置命令

```bash
# 安装 systemd 服务
openclaw gateway install

# 启用开机自启
systemctl --user enable openclaw-gateway

# 立即启动
systemctl --user start openclaw-gateway

# 查看状态
systemctl --user status openclaw-gateway
```

#### 方法二：手动创建 systemd 服务

创建 `~/.config/systemd/user/openclaw-gateway.service`：

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/openclaw gateway
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
# 重载 systemd
systemctl --user daemon-reload

# 启用开机自启
systemctl --user enable openclaw-gateway

# 启动服务
systemctl --user start openclaw-gateway

# 查看状态
systemctl --user status openclaw-gateway
```

> [!info] 来源
> - [OpenClaw 自启动与手动启动配置说明](https://blog.csdn.net/sgr011215/article/details/158461994) - CSDN
> - [OpenClaw 保姆级安装配置教程](https://m.blog.csdn.net/liwang0113/article/details/157579187) - CSDN

### 1.3 WSL2 配置

WSL2 需要先启用 systemd 支持：

```bash
# 编辑 /etc/wsl.conf
sudo nano /etc/wsl.conf

# 添加以下内容
[boot]
systemd=true

# 重启 WSL
wsl --shutdown
```

然后按照 Linux 的 systemd 配置方法操作。

### 1.4 验证自启配置

```bash
# 查看服务状态
systemctl --user status openclaw-gateway.service

# 应该看到：
# Active: active (running)
```

---

## 二、Tailscale Serve HTTPS

### 是什么

**Tailscale Serve** 是 Tailscale 提供的内置功能，可以将本地服务通过 Tailscale 网络暴露，并自动提供 HTTPS 证书。

### 为什么需要

| 问题 | Tailscale Serve 解决方案 |
|------|--------------------------|
| HTTP 不安全 | 自动提供 HTTPS 证书 |
| CORS 配置复杂 | 同域名无跨域问题 |
| 安全上下文限制 | HTTPS 满足安全上下文要求 |
| 端口转发麻烦 | 无需配置端口转发 |

### 通俗理解

**🎯 比喻**：Tailscale Serve 就像一个"安全翻译官"，它把你本地运行的 OpenClaw（说 HTTP 方言）翻译成 HTTPS（安全方言），让外部设备能安全地听懂。

### 2.1 前置条件

1. **已安装 Tailscale**：参考 [[../../02-工具使用/Tailscale使用指南]]
2. **已启用 HTTPS**：在 Tailscale 管理后台开启 HTTPS 功能
3. **OpenClaw Gateway 正常运行**

### 2.2 一键启用（推荐）

```bash
# 启动 Gateway 并自动配置 Tailscale Serve
openclaw gateway --tailscale serve
```

**访问地址**：
```
https://<your-machine-name>.tail<tailnet-id>.ts.net/
```

例如：`https://openclaw.tail8a3e67.ts.net/`

### 2.3 手动配置 Tailscale Serve

#### 步骤 1：查看 Tailscale 域名

```bash
tailscale status

# 输出示例：
# 100.64.1.2   openclaw    your-name@  linux -
# 机器名是 "openclaw"
# tailnet ID 是 "tail8a3e67"
# 完整域名：openclaw.tail8a3e67.ts.net
```

#### 步骤 2：配置 Tailscale Serve

```bash
# 将本地 18789 端口通过 HTTPS 暴露
tailscale serve https:443 / http://127.0.0.1:18789

# 查看配置
tailscale serve status
```

#### 步骤 3：配置 CORS

```bash
# 将 Tailscale 域名添加到 CORS 白名单
openclaw config set gateway.controlUi.allowedOrigins '["https://openclaw.tail8a3e67.ts.net"]'

# 重启 Gateway
openclaw restart
```

### 2.4 完整 Tailscale 配置

**配置文件** (`~/.openclaw/openclaw.json`)：

```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "serve"
    },
    "controlUi": {
      "allowedOrigins": ["https://openclaw.tail8a3e67.ts.net"]
    },
    "auth": {
      "allowTailscale": true
    }
  }
}
```

> [!info] 来源
> - [OpenClaw Web 文档](https://docs.openclaw.ai/web) - Tailscale access
> - [OpenClaw 绑定域名HTTPS+阿里云快速部署方案](https://developer.aliyun.com/article/1712505) - 阿里云

### 2.5 Tailscale HTTPS 优势

| 优势 | 说明 |
|------|------|
| ✅ **自动证书** | Let's Encrypt 自动申请和续期 |
| ✅ **无需端口转发** | 通过 Tailscale 网络直接访问 |
| ✅ **安全上下文** | 浏览器认可的安全 HTTPS |
| ✅ **零 CORS 配置** | 同域名无跨域问题 |
| ✅ **身份认证** | 可启用 Tailscale 身份验证 |

> [!warning] 注意
> 使用 Tailscale HTTPS 域名时，建议关闭翻墙软件和代理，否则可能访问失败。

---

## 三、完整配置示例

### 场景：服务器长期运行

```bash
# === 1. 安装 OpenClaw（如果未安装）===
curl -fsSL https://openclaw.ai/install.sh | bash

# === 2. 配置 API ===
openclaw config set models.providers.deepseek '{
  "baseUrl": "https://api.deepseek.com/v1",
  "apiKey": "sk-your-key",
  "api": "openai-completions",
  "models": [{"id": "deepseek-chat", "name": "DeepSeek Chat"}]
}'

# === 3. 配置 Tailscale HTTPS ===
openclaw config set gateway.tailscale.mode "serve"
openclaw config set gateway.controlUi.allowedOrigins '["https://your-name.tailxxxx.ts.net"]'
openclaw config set gateway.auth.allowTailscale true

# === 4. 安装守护进程服务 ===
openclaw gateway install

# === 5. 启动服务 ===
openclaw gateway --tailscale serve

# === 6. 验证状态 ===
systemctl --user status openclaw-gateway
tailscale serve status
```

### 配置文件完整示例

```json
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "sk-your-api-key",
        "api": "openai-completions",
        "models": [
          {"id": "deepseek-chat", "name": "DeepSeek Chat"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek-chat"
      }
    }
  },
  "gateway": {
    "bind": "loopback",
    "port": 18789,
    "tailscale": {
      "mode": "serve"
    },
    "controlUi": {
      "allowedOrigins": ["https://openclaw.tail8a3e67.ts.net"]
    },
    "auth": {
      "mode": "token",
      "token": "your-secure-token-here",
      "allowTailscale": true
    }
  }
}
```

---

## 四、常见问题

### Q1：服务启动失败？

```bash
# 查看日志
journalctl --user -u openclaw-gateway -f

# 或
tail -f ~/.openclaw/logs/current.log

# 运行诊断
openclaw doctor --fix
```

### Q2：Tailscale HTTPS 域名无法访问？

**检查清单**：
1. Tailscale 是否正在运行：`tailscale status`
2. HTTPS 功能是否启用：登录 [Tailscale Admin](https://login.tailscale.com/admin/dns)
3. CORS 是否正确配置：`openclaw config get gateway.controlUi.allowedOrigins`
4. 关闭代理软件重试

### Q3：如何查看访问 Token？

```bash
# 获取访问链接（含 Token）
openclaw dashboard --no-open

# 输出示例：
# https://openclaw.tail8a3e67.ts.net/?token=abc123...
```

### Q4：如何停止守护进程服务？

```bash
# 停止服务
systemctl --user stop openclaw-gateway

# 禁用开机自启
systemctl --user disable openclaw-gateway

# 卸载服务
openclaw gateway uninstall
```

### Q5：设备配对失败？

```bash
# 列出待批准设备
openclaw devices list

# 批准设备
openclaw devices approve <request-id>
```

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **开机自启的价值**：对于服务器部署，开机自启是必需的，可以省去很多手动操作的麻烦
>
> 2. **Tailscale HTTPS 是最佳方案**：
>    - 相比 HTTP + allowInsecureAuth，更安全
>    - 相比自签名证书，浏览器信任
>    - 相比购买域名和证书，免费且自动
>
> 3. **踩坑记录**：
>    - 使用 Tailscale HTTPS 时必须配置 CORS
>    - 域名格式是 `机器名.tail<id>.ts.net`
>    - 翻墙软件可能干扰访问
>
> 4. **安全建议**：
>    - 设置强 Token
>    - 启用 `allowTailscale` 身份验证
>    - 定期检查已配对设备列表

---

## 相关文档

- [[OpenClaw MOC]] - OpenClaw 文档索引
- [[OpenClaw安装后配置指南]] - 基础配置
- [[OpenClaw Web控制台局域网访问配置]] - 局域网访问配置
- [[OpenClaw常用命令速查]] - 命令速查表
- [[../../02-工具使用/Tailscale使用指南]] - Tailscale 完整指南

---

## 参考资料

### 官方资源
- [OpenClaw Web 文档](https://docs.openclaw.ai/web) - Gateway Web 配置
- [OpenClaw Remote Access 文档](https://docs.openclaw.ai/gateway/remote) - 远程访问配置
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 源代码
- [Tailscale Serve 文档](https://tailscale.com/kb/1242/funnel-serve) - Tailscale 官方

### 社区资源
- [OpenClaw 自启动与手动启动配置说明](https://blog.csdn.net/sgr011215/article/details/158461994) - CSDN
- [OpenClaw 保姆级安装配置教程](https://m.blog.csdn.net/liwang0113/article/details/157579187) - CSDN
- [OpenClaw 绑定域名HTTPS+阿里云快速部署方案](https://developer.aliyun.com/article/1712505) - 阿里云开发者社区
- [Tailscale多设备连接教程](https://m.blog.csdn.net/tinygone/article/details/158315052) - CSDN

---

**最后更新**：2026-03-04
