---
title: VMware NAT 模式静态 IP 网关错误排错
created: 2026-08-28
updated: 2026-08-28
status: active
tags:
  - VMware
  - 排错
  - NAT
  - 网关
  - Netplan
  - DNS
  - Docker
---

# VMware NAT 模式静态 IP 网关错误排错

> [!summary] 一句话结论
> 在 VMware NAT 模式下，虚拟机网段（如 `192.168.245.0/24`）的默认网关是 **`192.168.245.2`**（VMware NAT 服务），**不是 `.1`**（VMnet8 宿主机虚拟网卡）。静态 IP 把网关写成 `.1` 后，所有发往外网的数据包和 DNS 查询都停滞在宿主机虚拟网卡上，整台虚拟机外网全面断连，表现为 Docker 拉取 DNS 超时 + `ping baidu.com` 解析失败——本质是**底层网络断连**，而非单纯的 DNS 故障。

---

## 一、故障现象与报错信息

环境：VMware Workstation 中的 Ubuntu 虚拟机（静态 IP `192.168.245.130/24`）。

**Docker 拉取报错：**

```text
failed to resolve reference "docker.io/...": dial tcp: lookup docker.m.daocloud.io on 127.0.0.53:53: read udp ...: i/o timeout
```

**系统 DNS 解析报错：**

```text
ping: baidu.com: Temporary failure in name resolution
nslookup docker.m.daocloud.io -> communications error to 127.0.0.53#53: timed out
```

**底层 IP 连通性测试：**

```text
ping 223.5.5.5 -> 100% packet loss (丢包率 100%)
```

> [!warning] 关键判读
> `ping 223.5.5.5`（公网 IP）都 100% 丢包，说明**不是 DNS 单独故障**，而是虚拟机底层出网链路已经断了。DNS 解析超时只是表象。

---

## 二、根本原因分析（Root Cause）

VMware Workstation 的 NAT 网络模式（VMnet8）下，`192.168.245.0/24` 网段里有三个关键角色：

| 地址 | 角色 |
|------|------|
| `192.168.245.1` | VMnet8 宿主机虚拟网卡（Windows/Mac 侧） |
| `192.168.245.2` | **VMware NAT 服务**：真正的出网网关，负责把虚拟机流量路由到外网 |
| `192.168.245.130` | 虚拟机自身静态 IP |

> [!note] 核心问题
> Ubuntu 静态网络配置中，默认网关被错误配置成了 `192.168.245.1`。发往外网的数据包和 DNS 请求全部停滞在宿主机虚拟网卡上，**未被 VMware NAT 服务转发**，导致整台虚拟机外网全面断连。

数据流向示意：

```text
虚拟机 ens33 (192.168.245.130)
    │  默认网关错误指向 192.168.245.1
    ▼
VMnet8 宿主机虚拟网卡 (192.168.245.1)   ← 数据包卡在这里
    │
    ▼
VMware NAT 服务 (192.168.245.2)         ← 正确的出网网关
    │
    ▼
外网 (Internet)
```

---

## 三、标准排查步骤（Checklist）

遇到类似 DNS 解析超时或 Docker 镜像无法拉取时，按以下顺序排查：

```bash
# 步骤 1：判断是单纯 DNS 故障还是底层网络断连（直接 Ping 公网 IP）
ping -c 2 223.5.5.5

# 步骤 2：查看当前默认网关配置
ip route show default

# 步骤 3：测试能否连通 NAT 网关（.2）
ping -c 2 192.168.245.2
```

> [!tip] 判定逻辑
> - 步骤 1 **丢包** → 底层网络断连，不是 DNS 问题，直接进入步骤 2 / 3。
> - 步骤 3 通、但默认网关是 `.1` → 基本锁定根因是网关配错。
> - 步骤 3 也不通 → 检查 VMware NAT 服务是否正常、宿主机代理 TUN 是否劫持流量（见第五节）。

---

## 四、解决方案与配置修复

### 4.1 临时切换网关（立即验证）

```bash
# 删除错误的 .1 网关并添加正确的 .2 网关
sudo ip route del default
sudo ip route add default via 192.168.245.2 dev ens33

# 验证外网连通性与 DNS
ping -c 2 223.5.5.5
ping -c 2 baidu.com
```

> [!note] 生效范围
> 通过 `ip route` 修改的路由**重启后失效**，仅用于快速验证根因是否正确。

### 4.2 永久修改 Netplan 配置文件

编辑系统的 Netplan 配置文件（根据实际文件名打开）：

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

```yaml
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: no
      addresses:
        - 192.168.245.130/24    # 虚拟机静态 IP
      routes:
        - to: default
          via: 192.168.245.2    # 【关键】NAT 网关必须配置为 .2
      nameservers:
        addresses:
          - 223.5.5.5
          - 114.114.114.114
          - 8.8.8.8
```

应用配置使其永久生效：

```bash
sudo netplan apply
```

> [!warning] 易错点
> Netplan 的 `routes:` 字段里，`via` 必须指向 **`.2`**。写成 `.1` 时配置文件本身不会报错，但外网就是不通——这正是「配置合法却无法上网」的典型坑。

### 4.3 重新启动 Docker 服务

```bash
cd ~/docker/hermes-stack/
sudo docker compose up -d
```

---

## 五、延伸避坑总结

> [!tip] 防坑清单
> 1. **VMware 默认网关规律**：在 VMware 的 NAT 网段（如 `192.168.X.0/24`）中，网关默认固定为 `192.168.X.2`，**绝不能填 `.1`**。
> 2. **宿主机代理软件干扰**：若宿主机开启了 VPN / 代理软件的 TUN 虚拟网卡模式，可能劫持 VMware NAT 的流量。若确认网关为 `.2` 后仍丢包，可暂时关闭宿主机 TUN 模式，或在代理软件中放行 VMnet8。
> 3. **表象与根因**：Docker 拉取 DNS 超时、`ping baidu.com` 解析失败这类报错，先 ping 公网 IP 判断是不是底层网络断连，别急着在 DNS 层和镜像源上反复折腾。

---

## 相关文档

- [[虚拟机/虚拟机 MOC.md]] - 虚拟机知识索引
- [[docker/docker镜像拉取DNS解析超时排错.md]] - 同一事故的表象层排错：systemd-resolved 超时、失效镜像源占首位
- [[linux/linux如何修改网络信息.md]] - Ubuntu Netplan 静态 IP / 网关 / DNS 配置基础
- [[虚拟机/虚拟网络模式/06_虚拟机网络模式.md]] - VMware 桥接 / NAT / 仅主机三种网络模式原理

---

**最后更新**：2026-08-28
