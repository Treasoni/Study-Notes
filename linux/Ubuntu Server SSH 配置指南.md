---
tags: [linux, ssh, ubuntu-server, 运维]
created: 2026-03-02
updated: 2026-03-02
---

# Ubuntu Server SSH 配置指南

> [!info] 概述
> **SSH（Secure Shell）** 是一种加密网络协议，用于在不安全的网络上安全地访问远程计算机。
>
> **通俗比喻**：SSH 就像是给你的服务器配了一把带密码锁的"遥控器"，让你可以在任何地方安全地控制服务器，就像坐在服务器前操作一样。

## 核心概念

### 是什么
SSH（Secure Shell）是 Linux 系统上用于远程登录和管理的标准协议，所有通信数据都经过加密，防止中间人攻击和信息泄露。

### 为什么需要
- **远程管理**：无需物理接触服务器即可进行管理
- **安全传输**：所有数据加密，防止窃听
- **自动化运维**：支持脚本自动化执行远程命令
- **文件传输**：配合 SCP/SFTP 进行安全的文件传输

### 通俗理解

**🎯 比喻**：想象你在外地想控制家里的电脑：
- **没有 SSH**：你必须飞回家，坐在电脑前操作
- **有 SSH**：你用手机就能远程控制，而且所有指令都经过加密，黑客看不懂你在干什么

**📦 基本使用示例**：
```bash
# 安装 OpenSSH Server
sudo apt update
sudo apt install -y openssh-server

# 启动并设置开机自启
sudo systemctl start ssh
sudo systemctl enable ssh

# 检查服务状态
sudo systemctl status ssh
```

## 安装与配置

### 步骤一：安装 OpenSSH Server

```bash
# 更新软件包列表
sudo apt update

# 安装 OpenSSH Server
sudo apt install -y openssh-server
```

### 步骤二：启动 SSH 服务

```bash
# 启动 SSH 服务
sudo systemctl start ssh

# 设置开机自动启动
sudo systemctl enable ssh

# 查看服务状态（确认是否正常运行）
sudo systemctl status ssh
```

正常运行的输出应显示 `active (running)` 状态。

### 步骤三：配置防火墙（如果启用 UFW）

```bash
# 允许 SSH 连接（默认端口 22）
sudo ufw allow ssh

# 或明确指定端口
sudo ufw allow 22/tcp

# 查看防火墙状态
sudo ufw status
```

### 步骤四：测试连接

```bash
# 从另一台电脑测试连接
ssh username@your_server_ip

# 例如：
ssh ubuntu@192.168.1.100
```

## 配置文件详解

SSH 主配置文件位于 `/etc/ssh/sshd_config`：

```bash
# 编辑配置文件
sudo nano /etc/ssh/sshd_config
```

### 常用配置选项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `Port 22` | 22 | SSH 监听端口 |
| `PermitRootLogin yes` | yes | 是否允许 root 登录 |
| `PasswordAuthentication yes` | yes | 是否允许密码认证 |
| `PubkeyAuthentication yes` | yes | 是否允许公钥认证 |

**修改配置后需要重启服务**：
```bash
sudo systemctl restart ssh
```

## 安全最佳实践

### 1. 禁用 root 登录（推荐）

```bash
# 在 /etc/ssh/sshd_config 中设置
PermitRootLogin no

# 重启服务
sudo systemctl restart ssh
```

### 2. 使用密钥认证（更安全）

```bash
# 在客户端生成 SSH 密钥对
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥复制到服务器
ssh-copy-id username@server_ip

# 服务器端禁用密码登录（可选，确保密钥可用后再操作）
# 在 /etc/ssh/sshd_config 中：
PasswordAuthentication no
```

### 3. 更改默认端口（可选）

```bash
# 编辑配置文件，修改端口
sudo nano /etc/ssh/sshd_config
# Port 22 → Port 2222

# 重启服务
sudo systemctl restart ssh

# 更新防火墙规则
sudo ufw allow 2222/tcp

# 连接时指定端口
ssh -p 2222 username@server_ip
```

## 常见问题

### Q1: 连接被拒绝 (Connection refused)
**原因**：SSH 服务未启动或防火墙阻止
**解决**：
```bash
# 检查服务状态
sudo systemctl status ssh

# 检查防火墙
sudo ufw status

# 确保端口开放
sudo ufw allow ssh
```

### Q2: 连接超时 (Connection timed out)
**原因**：网络问题或服务器 IP 地址错误
**解决**：检查网络连接和服务器 IP 地址是否正确

### Q3: 权限拒绝 (Permission denied)
**原因**：用户名或密码错误
**解决**：确认用户名和密码正确，或使用密钥认证

### Q4: 如何查看服务器 IP 地址？
```bash
ip addr show
# 或
hostname -I
```

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[SCP]] | 基于 SSH 的安全文件复制协议 |
| [[SFTP]] | 基于 SSH 的安全文件传输协议 |
| [[密钥认证]] | SSH 的安全认证方式之一 |

## 个人笔记
> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

## 相关文档
- [[00-索引/MOC|MOC 索引]]

## 参考资料
- [Ubuntu Server OpenSSH 官方文档](https://ubuntu.com/server/docs/openssh-server)
- [OpenSSH 官方网站](https://www.openssh.com/)
