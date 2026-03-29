---
tags: [linux, ubuntu, 网络, 旁路由, ssl, 故障排查]
created: 2026-03-29
updated: 2026-03-29
---

# Ubuntu curl SSL 连接问题排查

> [!info] 概述
> **一句话定义**：当 Ubuntu 网关指向旁路由时，可能因 ICMP 重定向导致 SSL 握手失败。
> **通俗比喻**：就像寄快递时，快递站告诉你"走另一条路更快"，但半路换了路线导致包裹丢了。

## 问题描述

### 错误现象

在 Ubuntu 上使用 curl 访问 HTTPS 网站时出现错误：

```bash
zhq@ubuntu:~$ curl https://www.bttwoo.com
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to www.bttwoo.com:443
```

### 诊断信息

尝试 ping 目标网站：

```bash
zhq@ubuntu:~$ ping www.bttwoo.com
PING www.bttwoo.com (123.140.124.34) 56(84) bytes of data.
64 bytes from 123.140.124.34: icmp_seq=1 ttl=50 time=63.5 ms
From _gateway (192.168.110.119): icmp_seq=2 Redirect Host(New nexthop: 192.168.110.1)
64 bytes from 123.140.124.34: icmp_seq=2 ttl=62.0 ms
...
```

**关键发现**：
- ✅ 可以 ping 通目标 IP
- ⚠️ 每隔一条有 **ICMP 重定向** 消息：`From _gateway: Redirect Host(New nexthop: 192.168.110.1)`

### 网络环境

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Ubuntu    │ ───▶ │   旁路由     │ ───▶ │   主路由     │ ───▶ 互联网
│192.168.110.x│      │192.168.110.119│     │192.168.110.1│
└─────────────┘      └─────────────┘      └─────────────┘
      │                    │
      └── 网关指向旁路由 ───┘
```

## 问题原因分析

### 根本原因：非对称路由

```
问题流程：

1. Ubuntu 发送数据包 ──▶ 旁路由 (192.168.110.119)
                           │
2. 旁路由发现："直连主路由更近！"
                           │
3. 旁路由发送 ICMP 重定向 ──▶ Ubuntu
   "下次直接发给 192.168.110.1"
                           │
4. 后续数据包路径改变：
   Ubuntu ──▶ 主路由 ──▶ 目标服务器
                │
           但返回包可能走：
   目标服务器 ──▶ 旁路由 ──▶ Ubuntu

   ⚠️ 去程和回程路径不一致！
```

### 错误 (35) SSL_ERROR_SYSCALL 的本质

| 误解 | 真相 |
|------|------|
| 是证书错误？ | ❌ 不是 |
| 是 OpenSSL 问题？ | ❌ 不是 |
| **是底层系统调用失败** | ✅ 正确 |

**原因链条**：
```
ICMP 重定向
    ↓
TCP/SSL 握手过程中路径变化
    ↓
数据包丢失或乱序
    ↓
SSL 握手失败
    ↓
curl 报错 (35) SSL_ERROR_SYSCALL
```

### 完整诊断流程图

```
curl HTTPS 失败
      │
      ▼
ping 测试 ────── 有 ICMP 重定向? ────┐
      │                    │          │
      │                   是          │
      │                    │          │
      │                    ▼          │
      │           检查网关设置         │
      │                    │          │
      │            网关 = 旁路由?      │
      │                    │          │
      ▼                    ▼          ▼
   网络正常           非对称路由问题   其他原因
                              │
                              ▼
                      应用下方解决方案
```

## 解决方案

### 方案一：旁路由开启 IP 动态伪装（推荐 ⭐）

> [!success] 治本方案
> 通过 SNAT 修改源 IP，强制返回包经过旁路由，消除非对称路由。

#### OpenWrt 图形界面配置

1. 登录旁路由管理界面
2. 进入 **网络** → **防火墙** → **基本设置**
3. 找到 **区域** 列表中的 **lan** 区域
4. 勾选 **IP 动态伪装 (Masquerading)**
5. 保存并应用配置

#### SSH 命令行配置

```bash
# 登录旁路由 SSH
ssh root@192.168.110.119

# 添加防火墙规则（假设 eth0 或 br-lan 是 LAN 口）
iptables -t nat -I POSTROUTING -o br-lan -j MASQUERADE

# 或者指定具体网卡
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
```

#### 原理图解

```
开启 MASQUERADE 前：
Ubuntu(192.168.110.x) ──▶ 旁路由 ──▶ 主路由 ──▶ 目标
                            │
                      源 IP 不变，仍是 192.168.110.x
                            │
目标 ──▶ 主路由 ──▶ ??? (不知道 192.168.110.x 在哪)
              │
         可能直接发给 Ubuntu（绕过旁路由）
              │
         非对称路由！返回包路径不一致


开启 MASQUERADE 后：
Ubuntu(192.168.110.x) ──▶ 旁路由 ──▶ 主路由 ──▶ 目标
                            │
                     源 IP 改为 192.168.110.119（旁路由）
                            │
目标 ──▶ 主路由 ──▶ 旁路由(192.168.110.119) ──▶ Ubuntu
                            │
                     返回包必须经过旁路由
                            │
                     路径一致！问题解决 ✅
```

> [!info] 📚 相关知识
> 详见 [[软路由教程/旁路由原理详解##MASQUERADE 是什么？为什么要加？]]

---

### 方案二：Ubuntu 禁用 ICMP 重定向（快速验证）

> [!warning] 治标不治本
> 只是忽略重定向消息，如果主路由防火墙严格，仍可能丢包。

```bash
# 临时生效（重启失效）
sudo sysctl -w net.ipv4.conf.all.accept_redirects=0
sudo sysctl -w net.ipv4.conf.default.accept_redirects=0

# 永久生效
echo "net.ipv4.conf.all.accept_redirects = 0" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.conf.default.accept_redirects = 0" | sudo tee -a /etc/sysctl.conf

# 应用配置
sudo sysctl -p
```

#### 验证是否生效

```bash
# 查看当前设置
cat /proc/sys/net/ipv4/conf/all/accept_redirects
# 输出 0 表示已禁用

# 再次 ping 测试，不应再看到 Redirect 消息
ping www.bttwoo.com
```

---

### 方案三：检查旁路由代理软件（常见坑点）

> [!tip] 排查思路
> SSL 错误不一定是路由问题，也可能是代理软件本身的问题。

#### 3.1 检查代理节点状态

```bash
# 在旁路由上检查代理日志
# OpenClash
logread | grep openclash

# Passwall
logread | grep passwall
```

**可能原因**：
- 代理节点失效
- 节点连接超时
- 代理规则匹配错误

#### 3.2 检查 DNS/Fake-IP

```bash
# 在 Ubuntu 上检查解析结果
nslookup www.bttwoo.com

# 如果返回 198.18.x.x，说明是 Fake-IP
# 确保旁路由的 Fake-IP 映射正常工作
```

#### 3.3 添加直连白名单测试

在旁路由代理规则中，将目标域名加入**直连白名单**：

```
# OpenClash 规则示例
- DOMAIN,www.bttwoo.com,DIRECT

# Passwall 规则示例
www.bttwoo.com
```

---

### 方案四：绕过旁路由（简单粗暴）

> [!note] 适用场景
> 如果该 Ubuntu 机器不需要代理/广告过滤等旁路由功能。

#### 修改网关为主路由

```bash
# 临时修改（重启失效）
sudo ip route del default
sudo ip route add default via 192.168.110.1

# 永久修改（Netplan）
sudo nano /etc/netplan/00-installer-config.yaml
```

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens18:
      dhcp4: no
      addresses:
        - 192.168.110.x/24
      routes:
        - to: default
          via: 192.168.110.1    # 改为主路由
      nameservers:
        addresses:
          - 192.168.110.1       # DNS 也改为主路由
```

```bash
# 应用配置
sudo netplan apply
```

> [!info] 📚 参考资料
> 详见 [[linux如何修改网络信息]]

---

## 方案对比

| 方案 | 效果 | 复杂度 | 推荐场景 |
|------|------|--------|----------|
| **方案一：MASQUERADE** | ✅ 治本 | ⭐⭐ 中等 | **首选方案**，一劳永逸 |
| 方案二：禁用 ICMP 重定向 | ⚠️ 治标 | ⭐ 简单 | 临时测试、快速验证 |
| 方案三：检查代理软件 | ✅ 排查 | ⭐⭐⭐ 复杂 | 怀疑代理问题时 |
| 方案四：绕过旁路由 | ✅ 有效 | ⭐ 简单 | 不需要旁路由功能的机器 |

## 诊断命令速查

```bash
# 1. 测试网络连通性
ping <目标域名>

# 2. 测试 HTTPS 连接
curl -v https://<目标域名>

# 3. 查看路由表
ip route show

# 4. 查看 ICMP 重定向设置
cat /proc/sys/net/ipv4/conf/all/accept_redirects

# 5. 抓包分析（高级）
sudo tcpdump -i any port 443 -nn

# 6. 查看当前网关
ip route | grep default
```

## 与其他概念的关系

| 概念 | 关系 | 说明 |
|------|------|------|
| [[软路由教程/旁路由原理详解]] | 根本原理 | 理解旁路由和非对称路由 |
| [[linux如何修改网络信息]] | 网络配置 | 修改 Ubuntu 网关设置 |
| [[软路由教程/iStoreOS爬梯配置指南]] | 代理配置 | 旁路由代理软件配置 |

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

## 相关文档

- [[软路由教程/旁路由原理详解]]
- [[linux如何修改网络信息]]
- [[软路由教程/iStoreOS爬梯配置指南]]

## 参考资料

### 社区资源
- [OpenWrt 防火墙配置](https://openwrt.org/docs/guide-user/firewall/firewall_configuration)
- [Linux ICMP 重定向详解](https://tldp.org/HOWTO/Adv-Routing-HOWTO/)
- [curl SSL 错误排查](https://curl.se/docs/sslcerts.html)
