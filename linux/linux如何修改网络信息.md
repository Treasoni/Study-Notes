---
title: Linux 网络配置
tags: [linux, network]
created: 2026-07-29
updated: 2026-07-29
---

# Linux 网络配置

> [!info] 概述
> **网络配置就像给房子设置门牌号码和快递地址**。Linux 系统需要配置 IP 地址、网关和 DNS 才能正常联网和访问互联网。

## 核心概念 💡

### Netplan（Ubuntu 18.04+ 默认）
- **是什么**：Ubuntu 的网络配置工具，使用 YAML 格式配置文件
- **为什么需要**：统一管理网络接口，支持静态 IP 和 DHCP
- **与其他概念关系**：后端使用 Networkd 或 NetworkManager

### NetworkManager
- **是什么**：通用的网络管理工具，提供 GUI 和 CLI 接口
- **为什么需要**：更灵活的网络配置，支持 VPN、WiFi 等复杂场景
- **与其他概念关系**：可以通过 `nmcli` 命令行工具管理

## 操作步骤

### 方法一：Netplan 配置（推荐）

#### 1. 确认网络管理方式

```bash
ls /etc/netplan/
```

如果看到 `.yaml` 文件（如 `00-installer-config.yaml`），说明使用 Netplan。

#### 2. 编辑配置文件

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

#### 3. 静态 IP 配置示例

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:              # 网卡名称，用 ip a 查看
      dhcp4: no         # 关闭 DHCP
      addresses:
        - 192.168.1.100/24    # 静态 IP，/24 是子网掩码
      routes:
        - to: default
          via: 192.168.1.1    # 网关
      nameservers:
        addresses:
          - 223.5.5.5         # 阿里 DNS
          - 8.8.8.8           # Google DNS
```

#### 4. DHCP 配置示例

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:
      dhcp4: yes        # 启用 DHCP
```

#### 5. 应用配置

```bash
sudo netplan apply
```

> [!warning] 重要提示
> - YAML 对缩进极其敏感，只能用空格，不能用 Tab
> - `/24` 子网掩码不能省略
> - 冒号 `-` 后面必须有空格
> - `gateway4` 已弃用（Netplan 0.103+），始终使用 `routes` 格式
> - `renderer` 根据场景选择：Server 用 `networkd`，Desktop 用 `NetworkManager`
> - 配置错误会导致网络中断

### 方法二：NetworkManager 配置

#### 1. 安装 NetworkManager

```bash
sudo apt update
sudo apt install networkmanager
```

#### 2. 查看网络设备

```bash
nmcli device status
```

#### 3. 配置静态 IP

```bash
# 创建新的连接配置
sudo nmcli connection add type ethernet ifname ens18 con-name static-ip

# 设置静态 IP
sudo nmcli connection modify static-ip ipv4.addresses 192.168.1.100/24
sudo nmcli connection modify static-ip ipv4.gateway 192.168.1.1
sudo nmcli connection modify static-ip ipv4.dns "223.5.5.5 8.8.8.8"
sudo nmcli connection modify static-ip ipv4.method manual

# 启用连接
sudo nmcli connection up static-ip
```

#### 4. 配置 DHCP

```bash
sudo nmcli connection modify static-ip ipv4.method auto
sudo nmcli connection up static-ip
```

> [!tip] nmtui：NetworkManager 的文本界面
> 如果记不住 `nmcli` 命令，可以用 `nmtui`——一个交互式文本界面，通过菜单引导完成配置：
> ```bash
> sudo nmtui
> ```
> 适合不熟悉命令行的新手。

#### 5. WiFi 配置（无线网络）

```bash
# 查看可用的 WiFi 网络
nmcli dev wifi list

# 连接 WiFi
sudo nmcli dev wifi connect "WiFi名称" password "密码"

# 连接隐藏 WiFi（指定 SSID）
sudo nmcli dev wifi connect "WiFi名称" password "密码" hidden yes

# 查看已保存的连接
nmcli connection show
```

### 方法三：临时配置（重启失效）

```bash
# 临时设置 IP
sudo ip addr add 192.168.1.100/24 dev ens18

# 临时设置网关
sudo ip route add default via 192.168.1.1

# 临时设置 DNS（使用 systemd-resolved）
sudo resolvectl dns ens18 223.5.5.5 8.8.8.8

# ⚠️ 旧方法（echo ... > /etc/resolv.conf）在 systemd-resolved 管理的系统上无效
# /etc/resolv.conf 是符号链接，由 systemd-resolved 自动管理
```

### 方法四：systemd-networkd 直接配置（Arch Linux / Fedora / Debian 无桌面）

> 非 Ubuntu 发行版通常不装 Netplan，而是直接使用 systemd-networkd。配置文件放在 `/etc/systemd/network/` 下。

#### 1. 确认 systemd-networkd 是否运行

```bash
systemctl status systemd-networkd
```

如果未运行，启用并启动：

```bash
sudo systemctl enable --now systemd-networkd
```

#### 2. 创建网络配置文件

```bash
sudo nano /etc/systemd/network/20-wired.network
```

#### 3. 静态 IP 配置示例

```ini
[Match]
Name=ens18

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=223.5.5.5
DNS=8.8.8.8
```

#### 4. DHCP 配置示例

```ini
[Match]
Name=ens18

[Network]
DHCP=yes
```

#### 5. 应用配置

```bash
sudo systemctl restart systemd-networkd
```

#### 6. 查看配置状态

```bash
networkctl status
```

## 注意事项 ⚠️

### 常见错误

**YAML 缩进错误**：
```yaml
# ❌ 错误：使用 Tab
network:
  version: 2

# ✅ 正确：使用 2 空格（Netplan 标准）
network:
  version: 2
```

**网关配置错误**：
- Netplan 0.103+（Ubuntu 22.04+）已弃用 `gateway4`，必须用 `routes`
- Ubuntu 20.04 仍支持 `gateway4`，但建议新配置直接使用 `routes` 格式
- 新格式示例：
```yaml
routes:
  - to: default
    via: 192.168.1.1
```

**网卡名称错误**：
- 使用 `ip a` 或 `nmcli device status` 查看正确名称
- 常见名称：`eth0`、`ens18`、`enp3s0`

### 关键配置点

**查看网卡名称**：
```bash
ip a
# 或
nmcli device status
```

**测试网络连通性**：
```bash
# 测试本地网关
ping 192.168.1.1

# 测试互联网连接
ping 223.5.5.5

# 测试 DNS 解析
ping baidu.com
```

**查看当前 IP 配置**：
```bash
ip addr show          # 推荐，默认已安装
# 或
ip -br addr show      # 简洁输出
# 或
hostname -I           # 快速查看所有 IP
# 或
ifconfig              # 需安装 net-tools（已废弃，建议用 ip 命令替代）
```

**网络排障速查**：

| 目标 | 推荐命令 | 说明 |
|------|---------|------|
| 查看 IP 地址 | `ip -br addr` | 最简洁，一眼看清 |
| 查看路由表 | `ip route` | 检查默认网关是否正确 |
| 端口监听 | `ss -tuln` | 查看哪些端口在监听（替代 `netstat`）|
| 连通性测试 | `ping -c 4 8.8.8.8` | 测试到公网是否可达 |
| DNS 解析 | `dig baidu.com` | 查看 DNS 解析详情（需安装 dnsutils）|
| DNS 解析简洁版 | `host baidu.com` | 快速查 IP（需安装 bind9-host）|
| 跟踪路由 | `traceroute 8.8.8.8` | 排查哪一跳丢包（需安装 traceroute）|
| 抓包分析 | `sudo tcpdump -i ens18` | 查看网络流量（需安装 tcpdump）|

> `netstat`、`ifconfig` 等传统工具属于 `net-tools` 包，已多年未维护。现代 Linux 发行版默认使用 `iproute2` 套件（`ip`、`ss` 命令）。

## 常见问题 ❓

**Q: 配置后无法联网怎么办？**

A: 按以下步骤排查：
1. 检查网卡名称是否正确：`ip a`
2. 检查 YAML 语法：`sudo netplan try`（测试配置，30 秒后自动回滚）
3. 检查网关是否可达：`ping 192.168.1.1`
4. 检查 DNS 配置：`cat /etc/resolv.conf`

**Q: 如何查看当前使用的网络管理方式？**

A: 执行以下命令：
```bash
# 检查 Netplan
ls /etc/netplan/

# 检查 NetworkManager
systemctl status NetworkManager

# 检查网络服务
systemctl status networking
```

**Q: Ubuntu 24.04 的网络配置有什么变化？**

A: 主要变化：
- **Netplan 成为唯一推荐方式**，传统 `ifupdown`（`/etc/network/interfaces`）不再默认安装
- **renderer 按场景区分**：Desktop 默认 NetworkManager，Server 默认 systemd-networkd
- **`gateway4` 已完全弃用**，必须使用 `routes` 格式
- **`net-tools`（`ifconfig`）不再预装**，默认使用 `iproute2`（`ip` 命令）

**Q: 如何配置多个 IP 地址？**

A: 在 Netplan 配置中添加多个地址：
```yaml
addresses:
  - 192.168.1.100/24
  - 192.168.1.101/24
  - 10.0.0.1/24
```

**Q: 虚拟机如何配置网络？**

A: 虚拟机网络模式选择：
- **桥接模式**：虚拟机独立 IP，与宿主机同网段
- **NAT 模式**：共享宿主机网络，端口映射访问外网
- **仅主机模式**：只能与宿主机通信

## 更新记录

| 日期 | 变更内容 |
|------|---------|
| 2026-07-29 | 修复 Netplan 主示例 `gateway4` → `routes` |
| 2026-07-29 | 删除 DEB822 错误内容（DEB822 是 APT 软件源格式，非网络配置）|
| 2026-07-29 | 补充 renderer 说明（Desktop/Server 默认不同）|
| 2026-07-29 | 修正 `ifconfig` 为可选项，以 `ip` 命令为主 |
| 2026-07-29 | 修复临时 DNS 配置（改用 `resolvectl`）|
| 2026-07-29 | 扩充 Ubuntu 24.04 网络变化说明 |
| 2026-07-29 | 补充 WiFi 配置和 nmtui 文本界面说明 |
| 2026-07-29 | 新增 systemd-networkd 直接配置方法 |
| 2026-07-29 | 新增网络排障速查表 |
| 2026-07-29 | 补充 title 和 network 标签，修复 YAML 缩进示例

## 相关文档
- [[linux MOC]] - Linux 学习笔记索引
- [[Linux换源]] | [[linux磁盘相关的知识]] | [[Ubuntu curl SSL连接问题排查]]
