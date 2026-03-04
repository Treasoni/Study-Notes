---
tags: [openclash, openwrt, 代理, clash, 路由器]
created: 2026-03-04
updated: 2026-03-04
---

# OpenClash 插件使用指南

> [!info] 概述
> **OpenClash 是 OpenWrt 路由器上的 Clash 客户端插件**，支持多种代理协议，提供强大的分流规则和 Fake-IP 功能，是功能最丰富的路由器代理解决方案之一。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解 OpenClash 特点 | [[#一、OpenClash 简介]] |
| 与其他插件对比 | [[#二、OpenClash vs Passwall2]] |
| 安装 OpenClash | [[#三、安装方法]] |
| 配置订阅 | [[#四、订阅配置]] |
| 设置分流规则 | [[#五、分流规则配置]] |
| DNS 优化 | [[#六、DNS 优化配置]] |
| 排查问题 | [[#七、常见问题]] |

---

## 一、OpenClash 简介

### 是什么

**OpenClash** 是一个运行在 OpenWrt 路由器上的 Clash 客户端插件，由 vernesong 开发维护。

### 为什么选择 OpenClash

| 优势 | 说明 |
|------|------|
| **功能丰富** | 兼容 SS、SSR、VMess、Trojan 等多种协议 |
| **规则强大** | 基于 Clash 核心，支持复杂分流规则 |
| **Fake-IP** | 优化 DNS 解析，减少延迟 |
| **界面友好** | 提供 Web 管理界面 |
| **社区活跃** | 文档丰富，教程多 |

### 通俗理解

**🎯 比喻**：OpenClash 就像路由器上的「智能交通指挥官」。它根据规则决定哪些流量走「高速公路」（代理），哪些走「普通道路」（直连），还能自动避开「堵车路段」（广告拦截）。

### 项目信息

| 项目 | 详情 |
|------|------|
| **官方 GitHub** | [vernesong/OpenClash](https://github.com/vernesong/OpenClash) |
| **配置教程网站** | [openclash.net](https://openclash.net/) |
| **最新版本** | luci-app-openclash_0.46.137_all.ipk |

> [!info] 来源
> - [OpenClash 官方仓库](https://github.com/vernesong/OpenClash) - GitHub
> - [OpenClash 配置教程](https://openclash.net/) - 官方教程站

---

## 二、OpenClash vs Passwall2

### 功能对比

| 特性 | OpenClash | Passwall2 |
|------|-----------|-----------|
| **内核** | Clash | 自研 |
| **功能丰富度** | ⭐⭐⭐ 最全面 | ⭐⭐ 精简 |
| **资源占用** | ⭐⭐ 较高 | ⭐⭐⭐ 低 |
| **配置复杂度** | ⭐⭐⭐ 复杂 | ⭐⭐ 简单 |
| **Fake-IP** | ✅ 支持 | ✅ 支持 |
| **分流规则** | ⭐⭐⭐ 强大 | ⭐⭐ 基础 |
| **适合人群** | 进阶用户 | 新手/稳定党 |

### 如何选择

```
┌─────────────────────────────────────────────────────────────┐
│                    插件选择指南                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  你的路由器配置如何？                                        │
│  │                                                          │
│  ├─ 低配置（内存 < 256MB）──→ 推荐 Passwall2               │
│  │                                                          │
│  └─ 中高配置（内存 ≥ 256MB）                                │
│     │                                                       │
│     ├─ 追求稳定简单 ────────→ 推荐 Passwall2                │
│     │                                                       │
│     └─ 需要高级功能/复杂规则 → 推荐 OpenClash               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### OpenClash 优缺点

**优点**：
- ✅ 功能最全面，兼容多种协议
- ✅ 基于 Clash 核心，规则配置灵活
- ✅ Fake-IP 模式优化 DNS 解析
- ✅ 社区活跃，文档丰富

**缺点**：
- ❌ 资源占用较高，对路由器性能有要求
- ❌ 配置选项多，新手可能感到复杂
- ❌ 需要额外下载 Clash 二进制文件

---

## 三、安装方法

### 3.1 前置要求

| 要求 | 说明 |
|------|------|
| **系统** | OpenWrt / ImmortalWrt / iStoreOS |
| **内存** | 建议 ≥ 256MB |
| **存储** | 需要约 30MB 空间 |

### 3.2 方法一：通过 iStore 安装

1. 打开路由器管理界面
2. 进入 **iStore** 软件中心
3. 搜索 **OpenClash**
4. 点击「安装」

### 3.3 方法二：命令行安装

```bash
# 更新软件包列表
opkg update

# 安装 OpenClash
opkg install luci-app-openclash

# 安装后刷新页面
```

### 3.4 方法三：手动安装 IPK

```bash
# 1. 下载最新 IPK 包
# 访问 https://github.com/vernesong/OpenClash/releases

# 2. 上传到路由器
scp luci-app-openclash_*.ipk root@192.168.1.1:/tmp/

# 3. SSH 登录路由器安装
ssh root@192.168.1.1
cd /tmp
opkg install luci-app-openclash_*.ipk --force-depends

# 4. 重启路由器或刷新页面
```

> [!warning] 注意
> 首次运行时，OpenClash 会自动下载 Clash 核心文件，请确保网络通畅。

---

## 四、订阅配置

### 4.1 添加订阅

#### 步骤 1：进入配置页面

1. 打开路由器管理界面
2. 进入 **服务** → **OpenClash**
3. 切换到 **配置订阅** 标签

#### 步骤 2：添加订阅

```yaml
# 订阅配置
配置文件名: 我的机场
订阅地址: https://your-subscription-url
User-Agent: Clash
更新间隔: 24小时
```

#### 步骤 3：更新配置

1. 点击「保存配置」
2. 点击「更新配置」获取节点
3. 等待更新完成

### 4.2 配置文件管理

| 操作 | 说明 |
|------|------|
| **导入配置** | 从本地上传 YAML 配置文件 |
| **订阅更新** | 从订阅 URL 拉取最新配置 |
| **配置切换** | 在多个配置文件间切换 |

> [!info] 来源
> - [OpenClash 配置教程](https://openclash.net/) - 官方教程站

---

## 五、分流规则配置

### 5.1 代理模式

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| **Rule（规则分流）** | 根据规则智能分流 | ✅ 日常使用推荐 |
| **Global（全局代理）** | 所有流量走节点 | 特殊需求 |
| **Direct（直连）** | 关闭代理 | 临时关闭 |

### 5.2 规则分流配置

OpenClash 基于 Clash 核心，支持灵活的分流规则：

```yaml
# 分流规则示例
rules:
  # 广告拦截
  - DOMAIN-SUFFIX,ad.com,REJECT
  - GEosite,category-ads-all,REJECT

  # 国内直连
  - GEosite,cn,DIRECT
  - GEOIP,cn,DIRECT

  # 国外代理
  - GEosite,geolocation-!cn,PROXY
  - MATCH,PROXY
```

### 5.3 规则集（Rule Providers）

```yaml
# 使用规则集
rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400
```

### 5.4 分流流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClash 分流流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  流量进入                                                   │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────────┐    匹配     ┌─────────┐                   │
│  │ 广告规则    │ ──────────→ │ REJECT  │ → 拦截            │
│  └─────────────┘             └─────────┘                   │
│     │ 不匹配                                                 │
│     ▼                                                       │
│  ┌─────────────┐    匹配     ┌─────────┐                   │
│  │ 国内规则    │ ──────────→ │ DIRECT  │ → 直连            │
│  │ (geoip:cn)  │             └─────────┘                   │
│  └─────────────┘                                           │
│     │ 不匹配                                                 │
│     ▼                                                       │
│  ┌─────────────┐           ┌─────────┐                     │
│  │ 其他流量    │ ─────────→ │ PROXY   │ → 代理节点         │
│  └─────────────┘           └─────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [2025最新 Clash 客户端详细教程](https://www.shiqidu.com/d/1268) - 七度社区

---

## 六、DNS 优化配置

### 6.1 Fake-IP 模式

**Fake-IP** 是 OpenClash 的重要功能，可以优化 DNS 解析流程：

| 优势 | 说明 |
|------|------|
| **减少解析时间** | 返回虚假 IP，实际解析由代理服务器完成 |
| **避免 DNS 污染** | 本地 DNS 请求不会暴露真实访问域名 |
| **提升连接速度** | 省去本地 DNS 解析步骤 |

### 6.2 DNS 分流配置

```yaml
# DNS 分流配置
dns:
  enable: true
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16

  # 国外域名使用代理 DNS
  nameserver:
    - https://dns.google/dns-query
    - https://dns.cloudflare.com/dns-query

  # 国内域名使用国内 DNS
  nameserver-policy:
    "geosite:cn":
      - https://doh.pub/dns-query
      - https://dns.alidns.com/dns-query
```

### 6.3 MosDNS 集成

对于更高级的 DNS 分流需求，可以配合 **MosDNS** 使用：

- 区分国内外域名解析
- 双解析通道部署
- 启用 DNS 缓存减少重复查询

> [!info] 来源
> - [OpenClash DNS解析优化方案](https://developer.baidu.com/article/detail.html?id=5872344) - 百度开发者

---

## 七、常见问题

### Q1：OpenClash 启动失败？

**排查步骤**：
```bash
# 1. 检查 Clash 核心是否下载
ls /etc/openclash/core/

# 2. 查看日志
logread | grep openclash

# 3. 手动下载核心
# 在 OpenClash 设置页面点击「下载核心」
```

### Q2：配置更新失败？

**解决方案**：
1. 检查订阅地址是否正确
2. 尝试切换 User-Agent
3. 关闭代理后更新订阅
4. 检查网络连接

### Q3：部分网站无法访问？

**排查方法**：
1. 检查分流规则是否正确
2. 尝试切换代理节点
3. 检查 DNS 配置
4. 查看 OpenClash 日志

### Q4：Fake-IP 导致的问题？

某些应用可能不兼容 Fake-IP 模式：

```yaml
# 将问题域名排除在 Fake-IP 之外
fake-ip-filter:
  - '*.lan'
  - localhost.ptlogin2.qq.com
  - '+.srv.nintendo.net'
```

### Q5：如何降低资源占用？

1. 减少规则数量
2. 禁用不需要的功能
3. 使用简洁的配置文件
4. 考虑切换到 Passwall2

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **选择建议**：
>    - 高配路由器 + 复杂需求 → OpenClash
>    - 低配路由器 + 简单需求 → Passwall2
>
> 2. **Fake-IP 很重要**：开启后能明显提升响应速度
>
> 3. **踩坑记录**：
>    - 首次安装要等待核心下载完成
>    - 规则太多会影响性能
>    - 某些游戏/应用需要排除 Fake-IP
>
> 4. **优化技巧**：
>    - 定期清理日志
>    - 使用精简规则集
>    - 配合 MosDNS 做 DNS 分流

---

## 相关文档

- [[iStore爬梯配置指南]] - iStore 代理配置
- [[../../AI学习/02-工具使用/Tailscale使用指南]] - Tailscale VPN

---

## 参考资料

### 官方资源
- [OpenClash GitHub 仓库](https://github.com/vernesong/OpenClash) - 源代码与发布
- [OpenClash 配置教程](https://openclash.net/) - 官方教程网站
- [OpenWrt 官方网站](https://openwrt.org/) - OpenWrt 官方

### 社区资源
- [2025最新 Clash 客户端详细教程](https://www.shiqidu.com/d/1268) - 七度社区
- [OpenClash DNS解析优化方案](https://developer.baidu.com/article/detail.html?id=5872344) - 百度开发者

### 第三方文档
- [Clash 官方 Wiki](https://clash.wiki/) - Clash 配置参考
- [Loyalsoldier 规则集](https://github.com/Loyalsoldier/clash-rules) - 社区规则集

---

**最后更新**：2026-03-04
