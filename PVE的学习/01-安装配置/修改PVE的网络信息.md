---
tags: [pve]
---

# PVE 网络信息修改指南

> [!info] 概述
> PVE 安装后可能需要修改网络信息（IP 地址、网关等），可以通过 Web UI 或命令行两种方式完成。
> 类比：就像给电脑换一个新的 IP 地址，让它在网络中有一个新的"身份"。

## 核心概念 💡
- **vmbr0**：默认网桥名称，相当于虚拟交换机
- **物理网卡**：真实网卡名称，如 eno1、enp3s0、ens18
- **ifreload -a**：应用网络配置的命令
- **Web UI 方法**：官方推荐，最安全
- **命令行方法**：适合熟悉 Linux 的用户

## 方法一：Web UI 修改（官方推荐）

这是**最稳**、**不会被回滚**的方式。

### 操作步骤

1. **打开 PVE Web**
   ```
   https://192.168.2.10:8006
   ```

2. **进入网络配置**
   - 节点 → System → Network

3. **找到 vmbr0**
   - 点击 `vmbr0`
   - 点击 `Edit`

4. **配置网络信息**

   填写以下内容（示例）：

   | 配置项 | 值 |
   |--------|-----|
   | IPv4/CIDR | 192.168.2.10/24 |
   | Gateway | 192.168.2.1 |
   | Bridge ports | eno1（从下拉列表选） |

5. **应用配置**
   - 点击 `OK`
   - 点击 `Apply Configuration`
   - 或重启 PVE

> [!warning] 重要提示
> **不要乱填网卡名**，从下拉列表里选择真实存在的网卡

## 方法二：命令行修改

### 操作步骤

#### ① 确认真实网卡名

```bash
ip link
```

你会看到类似输出：
```
1: lo: <LOOPBACK,UP,LOWER_UP>
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP>
3: enp3s0: <BROADCAST,MULTICAST>
4: vmbr0: <BROADCAST,MULTICAST,UP,LOWER_UP>
```

👉 用**真实存在的那个**（如 eno1）

#### ② 改文件（示例）

```bash
nano /etc/network/interfaces
```

配置内容：

```bash
auto lo
iface lo inet loopback

auto eno1
iface eno1 inet manual

auto vmbr0
iface vmbr0 inet static
    address 192.168.2.10/24
    gateway 192.168.2.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
```

#### ③ ⚠️ 关键一步（很多人漏了）

```bash
ifreload -a
```

或（老版本）：

```bash
systemctl restart networking
```

📌 **只 reboot 很多时候是不生效的**

## 配置文件详解

### /etc/network/interfaces 结构

```bash
# 回环接口（本地通信）
auto lo
iface lo inet loopback

# 物理网卡（手动配置，交给网桥管理）
auto eno1
iface eno1 inet manual

# 网桥（虚拟交换机）
auto vmbr0
iface vmbr0 inet static
    address 192.168.2.10/24    # PVE 的 IP 地址
    gateway 192.168.2.1         # 网关地址
    bridge-ports eno1           # 绑定的物理网卡
    bridge-stp off              # 关闭生成树协议
    bridge-fd 0                 # 转发延迟为 0
```

## 常见网络配置

### 静态 IP（推荐）

```bash
iface vmbr0 inet static
    address 192.168.2.10/24
    gateway 192.168.2.1
```

### DHCP（自动获取 IP）

```bash
iface vmbr0 inet dhcp
```

### 多个网桥（高级）

```bash
auto vmbr0
iface vmbr0 inet static
    address 192.168.2.10/24
    gateway 192.168.2.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0

auto vmbr1
iface vmbr1 inet manual
    bridge-ports eno2
    bridge-stp off
    bridge-fd 0
```

## 注意事项 ⚠️

1. **网卡名必须真实存在**
   - 用 `ip link` 查看真实网卡名
   - 不要随意假设或复制

2. **修改后必须应用**
   - `ifreload -a` 或重启
   - 只改文件不生效

3. **Web UI 修改更安全**
   - 不会出现语法错误
   - 自动应用配置

4. **避免网络中断**
   - 建议在本地操作或用 IPMI/iKVM
   - 远程修改小心配置错误导致失联

5. **显示器显示问题**
   - 修改后重启，显示屏可能显示旧地址
   - 实际上已经改了，用新 IP 访问

## 常见问题 ❓

**Q: 修改后无法访问 Web 界面？**
A: 检查 IP 地址是否正确，用 `ip addr` 查看当前配置。

**Q: 网卡名不对怎么办？**
A: 用 `ip link` 查看真实网卡名，可能每次启动会变化。

**Q: ifreload -a 报错？**
A: 检查配置文件语法，可能是拼写错误或格式问题。

**Q: Web UI 和命令行选哪个？**
A: 推荐 Web UI，更安全可靠。命令行适合批量修改。

**Q: 如何恢复默认配置？**
A: 用 PVE 安装盘启动，选择恢复网络配置。

**Q: 可以配置多个 IP 地址吗？**
A: 可以，用 `up` 命令添加别名，如 `up ip addr add ... dev vmbr0`。

**Q: 修改后需要重启虚拟机吗？**
A: 不需要，PVE 网络配置不影响虚拟机运行（除非改了网桥配置）。

## 相关文档

[[01-安装配置/安装和使用PVE]] | [[02-虚拟机管理/PVE的网络逻辑讲解]] | [[PVE学习笔记MOC]]
