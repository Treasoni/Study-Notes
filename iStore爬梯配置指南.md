---
tags: [istore, openwrt, 代理, 爬梯, passwall, homeproxy]
created: 2026-03-04
updated: 2026-03-04
---

# iStore 爬梯配置指南

> [!info] 概述
> **iStore 是 OpenWrt 路由器的软件中心，可以方便地安装代理插件实现网络代理**。本文档介绍三大主流代理插件（Passwall、Passwall2、HomeProxy）的选择与配置方法。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解有哪些插件 | [[#二、代理插件选择]] |
| 配置 Passwall2 | [[#三、Passwall2 配置教程]] |
| 配置 HomeProxy | [[#四、HomeProxy 配置教程]] |
| 安装 iStore | [[#五、iStore 安装方法]] |
| 排查问题 | [[#六、常见问题]] |

---

## 一、iStore 简介

### 是什么

**iStore** 是 OpenWrt 系统的标准软件中心/应用商店，类似于手机的应用商店，可以方便地安装、管理和卸载各种插件。

### 为什么需要

| 优势 | 说明 |
|------|------|
| **可视化操作** | 图形界面安装插件，无需命令行 |
| **一键安装** | 自动处理依赖关系 |
| **版本管理** | 方便更新和卸载 |
| **入门友好** | 适合新手用户 |

### 通俗理解

**🎯 比喻**：iStore 就像手机上的「应用商店」或「App Store」。以前安装插件需要敲命令、手动下载依赖包，现在就像在手机上点「安装」按钮一样简单。

---

## 二、代理插件选择

### 四大主流插件对比

| 特性 | OpenClash | Passwall | Passwall2 | HomeProxy |
|------|-----------|----------|-----------|-----------|
| **内核** | Clash | 多协议支持 | 精简优化 | sing-box |
| **功能** | ⭐⭐⭐ 最强大 | ⭐⭐⭐ 全面 | ⭐⭐ 精简 | ⭐⭐⭐ 现代 |
| **性能** | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐⭐ 优秀 | ⭐⭐⭐ 优秀 |
| **资源占用** | 较高 | 中等 | 低 | 低 |
| **配置复杂度** | 复杂 | 中等 | 简单 | 简单 |
| **适配系统** | 通用 OpenWrt | 通用 OpenWrt | 通用 OpenWrt | **ImmortalWrt** |
| **适合人群** | 进阶用户 | 功能党 | 稳定党/新手 | 追新党 |

> [!tip] 推荐
> - **新手入门**：Passwall2（简单稳定）
> - **进阶用户**：OpenClash（功能强大，规则灵活）
> - 详细 OpenClash 教程见 [[OpenClash插件使用指南]]

### 如何选择

```
┌─────────────────────────────────────────────────────────────┐
│                    代理插件选择指南                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  你使用的是什么系统？                                        │
│  │                                                          │
│  ├─ ImmortalWrt ────────────→ 推荐 HomeProxy               │
│  │                                                          │
│  └─ 标准 OpenWrt / iStoreOS                                 │
│     │                                                       │
│     ├─ 新手/追求稳定 ────────→ 推荐 Passwall2                │
│     │                                                       │
│     ├─ 需要复杂规则/进阶 ────→ 推荐 OpenClash                │
│     │                                                       │
│     └─ 需要全部功能 ────────→ 推荐 Passwall                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!tip] 推荐
> 大多数用户推荐使用 **Passwall2**，它在功能和性能之间取得了很好的平衡。

---

## 三、Passwall2 配置教程

### 3.1 安装方法

#### 方法一：通过 iStore 安装（推荐）

1. 打开路由器管理界面
2. 进入 **iStore** 软件中心
3. 搜索 **Passwall2**
4. 点击「安装」

#### 方法二：命令行安装

```bash
# 更新软件包列表
opkg update

# 安装 Passwall2
opkg install luci-app-passwall2

# 安装后刷新页面
```

> [!info] 来源
> - [iStore 安装和配置指南](https://m.blog.csdn.net/gitblog_07501/article/details/142235222) - CSDN

### 3.2 节点订阅配置

#### 步骤 1：进入配置页面

1. 打开路由器管理界面
2. 进入 **服务** → **PassWall2**
3. 切换到 **节点订阅** 标签

#### 步骤 2：添加订阅

```yaml
# 订阅配置
订阅名称: 我的机场
订阅地址: https://your-subscription-url
自动更新: 开启
更新间隔: 24小时
```

#### 步骤 3：更新订阅

1. 点击「保存并应用」
2. 点击「手动更新」获取节点
3. 切换到 **节点** 标签查看是否成功

> [!warning] 订阅失败排查
> - 检查订阅地址是否正确
> - 检查网络是否可访问订阅地址
> - 尝试使用代理更新订阅

> [!info] 来源
> - [Passwall 配置和网络负载均衡设置](https://www.cnblogs.com/MaelDNM/p/18330958) - 博客园

### 3.3 分流规则设置

分流规则是代理的核心，决定哪些流量走代理、哪些直连。

#### 基本分流配置

```yaml
# 规则管理（必须勾选）
☑ geoip      # IP 地理位置规则
☑ geosite    # 域名分类规则

# 分流规则（按顺序匹配）
1. Reject 规则
   - 域名: geosite:category-ads-all
   - 作用: 拦截广告

2. Direct 规则
   - 域名: geosite:cn
   - IP: geoip:cn, geoip:private
   - 作用: 国内流量直连

3. Proxy 规则
   - 域名: geosite:geolocation-!cn
   - 作用: 国外流量走代理
```

#### 配置步骤

1. 进入 **基本设置** → **规则管理**
2. 勾选 **geoip** 和 **geosite**
3. 切换到 **分流规则**
4. 按顺序添加 Reject → Direct → Proxy 规则

```
┌─────────────────────────────────────────────────────────────┐
│                    分流规则匹配流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  流量进入                                                   │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 广告域名 │ ────────→ │ Reject  │ → 拦截                  │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 国内IP/域名│ ──────→ │ Direct  │ → 直连                  │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐           ┌─────────┐                         │
│  │ 其他流量 │ ────────→ │ Proxy   │ → 代理                  │
│  └─────────┘           └─────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [OpenWRT PassWall2 配置教程](https://blog.renfei.net/posts/1626402130325676130) - Renfei Blog

### 3.4 负载均衡设置

当你有多个节点时，可以设置负载均衡来提高速度和稳定性。

#### 配置步骤

1. 进入 **基本设置** → **负载均衡**
2. 添加已订阅的节点到负载均衡组
3. 设置负载均衡策略：
   - **轮询**：依次使用各节点
   - **最小延迟**：自动选择最快的节点
   - **故障转移**：主节点不可用时切换备用

```yaml
# 负载均衡配置示例
策略: 最小延迟
检测间隔: 300秒
超时时间: 5秒
节点列表:
  - 香港-01
  - 香港-02
  - 日本-01
```

> [!info] 来源
> - [Passwall 配置和网络负载均衡设置](https://www.cnblogs.com/MaelDNM/p/18330958) - 博客园

### 3.5 完整配置流程

```bash
# === 1. 安装 Passwall2 ===
# 通过 iStore 或命令行安装

# === 2. 配置订阅 ===
# 服务 → PassWall2 → 节点订阅
# 添加订阅地址 → 保存 → 手动更新

# === 3. 设置分流规则 ===
# 基本设置 → 规则管理
# 勾选 geoip、geosite
# 配置 Reject → Direct → Proxy 规则

# === 4. 选择节点 ===
# 基本设置 → 主节点
# 选择一个节点作为默认

# === 5. 启用代理 ===
# 基本设置 → TCP 代理模式
# 选择「全局」或「分流」模式
# 点击「保存并应用」
```

---

## 四、HomeProxy 配置教程

### 4.1 简介

**HomeProxy** 是 ImmortalWrt 官方的代理解决方案：
- 基于 **sing-box** 内核
- 现代化的 Web 界面
- 支持 ARM64/AMD64 架构

> [!warning] 注意
> HomeProxy 主要针对 **ImmortalWrt** 系统，标准 OpenWrt 可能需要额外确认兼容性。

### 4.2 安装方法

#### 方法一：ImmortalWrt 系统内置

ImmortalWrt 系统通常已预装 HomeProxy。

#### 方法二：手动安装

1. 打开路由器管理界面
2. 进入 **系统** → **软件包**
3. 点击「更新列表」
4. 搜索 **HomeProxy**
5. 点击「安装」

> [!info] 来源
> - [在OpenWrt中安装HomeProxy](https://m.blog.csdn.net/x1131230123/article/details/136388371) - CSDN

### 4.3 基本配置

```yaml
# HomeProxy 配置示例

# 1. 添加节点
节点名称: 我的节点
协议: vmess
地址: example.com
端口: 443
UUID: your-uuid-here

# 2. 设置分流
模式: 规则模式
规则集:
  - geosite:cn → 直连
  - geoip:cn → 直连
  - 默认 → 代理

# 3. DNS 配置
DNS 服务器:
  - https://dns.google/dns-query
  - https://dns.cloudflare.com/dns-query
```

> [!info] 来源
> - [HomeProxy 使用教程](https://m.blog.csdn.net/gitblog_00739/article/details/146973499) - CSDN
> - [HomeProxy自动配置工具](https://m.blog.csdn.net/gitblog_00046/article/details/147387886) - CSDN

---

## 五、iStore 安装方法

如果你的路由器没有 iStore，可以手动安装。

### 方法一：一键安装脚本

```bash
# 步骤1：更新软件包列表
opkg update

# 步骤2：下载安装脚本
cd /tmp
wget https://github.com/linkease/openwrt-app-actions/raw/main/applications/luci-app-systools/root/usr/share/systools/istore-reinstall.run

# 步骤3：赋予执行权限并运行
chmod 755 istore-reinstall.run
bash istore-reinstall.run
```

### 方法二：通过软件包安装

```bash
# 更新列表
opkg update

# 安装 iStore
opkg install luci-app-istore

# 刷新页面
```

> [!info] 来源
> - [OpenWRT应用商店iStore安装指南](https://m.blog.csdn.net/gitblog_00809/article/details/156035594) - CSDN

---

## 六、常见问题

### Q1：Passwall 和 Passwall2 有什么区别？

| 特性 | Passwall | Passwall2 |
|------|----------|-----------|
| 功能 | 更全面 | 精简版 |
| 依赖 | 更多 | 更少 |
| 性能 | 中等 | 更好 |
| 推荐场景 | 需要全部功能 | 追求稳定 |

### Q2：订阅更新后没有节点？

**排查步骤**：
1. 检查订阅地址是否正确
2. 检查网络连接
3. 尝试关闭代理后更新订阅
4. 查看日志排查错误

### Q3：代理后国内网站访问慢？

**解决方案**：
1. 确保分流规则正确配置
2. 检查国内域名/IP 是否在直连规则中
3. 确保 geoip 和 geosite 规则已启用

### Q4：如何在多台设备间同步配置？

1. 导出配置文件（通常是 JSON 格式）
2. 在新设备导入配置
3. 或使用 iStoreOS 的云同步功能

### Q5：如何查看代理是否生效？

```bash
# 方法1：访问 IP 检测网站
# 浏览器打开：https://ip.sb 或 https://ifconfig.me

# 方法2：命令行检测
curl ip.sb

# 方法3：查看 Passwall2 状态页面
# 路由器管理界面 → 服务 → PassWall2 → 状态
```

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **插件选择**：大多数情况下 Passwall2 足够使用，性能好且稳定
>
> 2. **分流规则很重要**：配置好分流规则可以让国内网站直连，避免不必要的延迟
>
> 3. **踩坑记录**：
>    - 订阅地址要保密，避免泄露
>    - 更新订阅前先关闭代理
>    - 负载均衡可以提高稳定性
>
> 4. **安全建议**：
>    - 定期更新订阅
>    - 使用可靠的服务商
>    - 不要在路由器上保存敏感密码

---

## 相关文档

- [[OpenClash插件使用指南]] - OpenClash 详细配置教程
- [[../../02-工具使用/Tailscale使用指南]] - Tailscale VPN 组网
- [[../../00-索引/MOC]] - 知识库索引

---

## 参考资料

### 官方资源
- [iStore 项目地址](https://gitcode.com/gh_mirrors/is/istore) - GitCode
- [Passwall2 GitHub](https://github.com/xiaorouji/openwrt-passwall2) - xiaorouji
- [ImmortalWrt 官网](https://immortalwrt.org) - 官方网站

### 社区资源
- [OpenWRT PassWall2 配置教程](https://blog.renfei.net/posts/1626402130325676130) - Renfei Blog
- [iStore 安装和配置指南](https://m.blog.csdn.net/gitblog_07501/article/details/142235222) - CSDN
- [Passwall 配置和网络负载均衡设置](https://www.cnblogs.com/MaelDNM/p/18330958) - 博客园
- [iStore 配置NAS及https证书](https://cloud.tencent.com/developer/article/2548409) - 腾讯云
- [OpenWRT应用商店iStore安装指南](https://m.blog.csdn.net/gitblog_00809/article/details/156035594) - CSDN

### 第三方文档
- [HomeProxy 使用教程](https://m.blog.csdn.net/gitblog_00739/article/details/146973499) - CSDN
- [HomeProxy自动配置工具](https://m.blog.csdn.net/gitblog_00046/article/details/147387886) - CSDN
- [在OpenWrt中安装HomeProxy](https://m.blog.csdn.net/x1131230123/article/details/136388371) - CSDN

---

**最后更新**：2026-03-04
