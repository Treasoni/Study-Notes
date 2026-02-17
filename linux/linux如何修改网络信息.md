---
tags: [linux]
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

### DEB822 格式（Ubuntu 24.04+）
- **是什么**：新的软件源配置格式，也用于网络配置
- **为什么需要**：更易读、更安全的配置格式
- **与传统格式区别**：使用 `.sources` 文件而非 `.list` 文件

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
      gateway4: 192.168.1.1   # 网关
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

### 方法三：临时配置（重启失效）

```bash
# 临时设置 IP
sudo ip addr add 192.168.1.100/24 dev ens18

# 临时设置网关
sudo ip route add default via 192.168.1.1

# 临时设置 DNS
echo "nameserver 223.5.5.5" | sudo tee /etc/resolv.conf
```

## 注意事项 ⚠️

### 常见错误

**YAML 缩进错误**：
```yaml
# ❌ 错误：使用 Tab
network:
  version: 2

# ✅ 正确：使用空格
network:
    version: 2
```

**网关配置错误**：
- Ubuntu 20.04+ 使用 `routes` 而非 `gateway4`
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
ip addr show
# 或
ifconfig
```

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
- Netplan 仍为主流配置方式
- DEB822 格式用于软件源配置
- NetworkManager 作为默认后端

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

## 相关文档
[[Linux换源]] | [[linux磁盘相关的知识]]
