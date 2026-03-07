---
tags: [istoreos, 软路由, passwall, 代理, 爬梯, 旁路由]
created: 2026-03-07
updated: 2026-03-07
---

# iStoreOS 爬梯配置指南

> [!info] 概述
> **iStoreOS 是易有云团队基于 OpenWRT 开发的软路由系统，内置 iStore 软件中心，可以方便地安装 Passwall 等代理插件实现网络代理**。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解 iStoreOS 是什么 | [[#一、iStoreOS 简介]] |
| 安装 Passwall 插件 | [[#二、Passwall 安装配置]] |
| 配置节点订阅 | [[#三、节点订阅配置]] |
| 设置分流规则 | [[#四、分流规则设置]] |
| 配置旁路由模式 | [[#五、旁路由网络配置]] |
| 排查问题 | [[#六、常见问题]] |

---

## 一、iStoreOS 简介

### 是什么

**iStoreOS** 是基于 OpenWRT 的软路由操作系统，由易有云团队开发，主要特点：

| 特性 | 说明 |
|------|------|
| **iStore 软件中心** | 内置应用商店，图形化安装插件 |
| **中文界面** | 全中文管理界面，上手简单 |
| **x86_64/ARM64** | 支持主流软路由硬件 |
| **旁路由模式** | 可作为现有路由器的扩展 |

### 为什么选择 iStoreOS

```
┌─────────────────────────────────────────────────────────────┐
│                    iStoreOS vs 标准 OpenWrt                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  标准 OpenWrt:                                              │
│  │                                                          │
│  ├─ 需要命令行安装插件                                      │
│  ├─ 配置依赖复杂                                            │
│  └─ 适合进阶用户                                            │
│                                                             │
│  iStoreOS:                                                  │
│  │                                                          │
│  ├─ 图形化软件中心，一键安装                                │
│  ├─ 插件自带教程，新手友好                                  │
│  └─ 适合所有用户                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 📚 来源
> - [iStoreOS 官方文档](https://doc.istoreos.com/zh/guide/istore/) - 易有云产品中心
> - [iStoreOS 快速入门指南](https://mathpretty.com/19518.html) - MathPretty

---

## 二、Passwall 安装配置

### 2.1 什么是 Passwall

**Passwall** 是 OpenWrt 系统上最流行的代理插件，支持多种协议：

| 支持的协议 | 说明 |
|-----------|------|
| VMess/VLess | V2协议系列 |
| Trojan | 木马协议 |
| Shadowsocks | SS协议 |
| Hysteria2 | 新一代UDP协议 |
| Tuic | 协议 |

### 2.2 通过 iStore 安装

#### 步骤 1：进入 iStore

1. 浏览器打开 iStoreOS 管理界面（默认 `192.168.100.1`）
2. 登录后进入 **iStore** 软件中心

#### 步骤 2：搜索安装

1. 在 iStore 中搜索 **Passwall** 或 **Passwall2**
2. 点击「安装」按钮
3. 等待安装完成

#### 步骤 3：启动插件

1. 安装完成后点击「打开」
2. 进入 Passwall 配置界面

> [!tip] Passwall vs Passwall2
> - **Passwall**：功能全面，支持更多协议
> - **Passwall2**：精简版本，资源占用更低，稳定性更好
>
> 新手推荐使用 **Passwall2**

> [!info] 📚 来源
> - [iStoreOS 软路由Passwall/Passwall2 进阶教程](https://www.youtube.com/watch?v=ifhmuCG8aHs) - YouTube
> - [iStoreOS 软路由使用Passwall2](https://www.youtube.com/watch?v=vBFZtvWPqzQ) - YouTube

### 2.3 命令行安装（备选）

如果 iStore 中找不到插件，可以使用命令行安装：

```bash
# SSH 登录路由器后执行

# 更新软件包列表
opkg update

# 安装 Passwall2
opkg install luci-app-passwall2

# 安装后刷新页面
```

---

## 三、节点订阅配置

### 3.1 获取订阅地址

从你的机场服务商获取订阅链接，格式通常为：
```
https://xxx.com/api/v1/client/subscribe?token=xxxxx
```

### 3.2 添加订阅

#### 步骤 1：进入订阅管理

1. 进入 **服务** → **PassWall2**
2. 切换到 **节点订阅** 标签

#### 步骤 2：配置订阅

```yaml
# 订阅配置示例
订阅名称: 我的机场
订阅地址: https://your-subscription-url
自动更新: 开启
更新间隔: 24小时
```

#### 步骤 3：更新节点

1. 点击「保存并应用」
2. 点击「手动更新」获取节点
3. 切换到 **节点** 标签查看是否成功

> [!warning] 订阅失败排查
> - 检查订阅地址是否正确
> - 检查路由器网络是否正常
> - 尝试关闭代理后更新订阅

### 3.3 订阅链接安全

> [!danger] 安全提醒
> - 订阅链接包含你的账号信息，不要分享给他人
> - 不要在公开场合截屏包含订阅链接的图片
> - 定期更换订阅链接保障安全

---

## 四、分流规则设置

### 4.1 什么是分流规则

分流规则决定了哪些流量走代理、哪些直连：

```
┌─────────────────────────────────────────────────────────────┐
│                    分流规则匹配流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  流量进入                                                   │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 广告域名 │ ────────→ │ 拦截    │ → 广告被屏蔽             │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 国内IP/域名│ ──────→ │ 直连    │ → 直接访问（国内网站）   │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐           ┌─────────┐                         │
│  │ 其他流量 │ ────────→ │ 代理    │ → 通过代理（国外网站）   │
│  └─────────┘           └─────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 基本分流配置

#### 步骤 1：启用规则管理

1. 进入 **基本设置** → **规则管理**
2. 勾选以下选项：
   - ☑ **geoip** - IP 地理位置规则
   - ☑ **geosite** - 域名分类规则

#### 步骤 2：配置分流规则

按以下顺序添加规则：

```yaml
# 规则1：拦截广告
类型: Reject
匹配条件: geosite:category-ads-all
动作: 拦截

# 规则2：国内直连
类型: Direct
匹配条件:
  - geosite:cn (国内域名)
  - geoip:cn (国内IP)
  - geoip:private (局域网IP)
动作: 直连

# 规则3：国外代理
类型: Proxy
匹配条件: geosite:geolocation-!cn
动作: 代理
```

#### 步骤 3：应用规则

1. 点击「保存并应用」
2. 在 **状态** 页面查看规则是否生效

### 4.3 自定义规则

你可以添加自定义规则来实现特定需求：

```yaml
# 示例：特定域名走代理
类型: Proxy
匹配条件: domain:github.com
动作: 代理

# 示例：特定域名直连
类型: Direct
匹配条件: domain:baidu.com
动作: 直连
```

> [!info] 📚 来源
> - [Passwall 配置和网络负载均衡设置](https://www.cnblogs.com/MaelDNM/p/18330958) - 博客园

---

## 五、旁路由网络配置

### 5.1 什么是旁路由

**旁路由**是指在现有主路由器之外，再添加一台路由器专门处理特定流量（如代理）。

```
┌─────────────────────────────────────────────────────────────┐
│                    网络拓扑结构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  光纤调制解调器                                             │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐                                               │
│  │ 主路由器 │ (负责拨号、DHCP、WiFi)                         │
│  └─────────┘                                               │
│       │                                                     │
│       ├─────────────────────┐                               │
│       │                     │                               │
│       ▼                     ▼                               │
│  ┌─────────┐          ┌─────────┐                          │
│  │ 普通设备 │          │ iStoreOS │ (旁路由，处理代理)       │
│  └─────────┘          └─────────┘                          │
│                             │                               │
│                             ▼                               │
│                        需要代理的设备                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 旁路由模式配置

#### 方式一：网关指向（推荐）

**主路由器设置**：
1. 进入主路由器的 DHCP 设置
2. 将需要代理的设备的网关设置为 iStoreOS 的 IP

**iStoreOS 设置**：
1. 进入 **网络** → **接口**
2. 编辑 LAN 接口：
   - IPv4 地址：`192.168.100.1`（或其他）
   - 网关：主路由器 IP
   - DNS：主路由器 IP 或公共 DNS

#### 方式二：设备手动设置

在需要代理的设备上：
1. 网络设置中选择手动配置
2. IP 地址：自动获取
3. 网关：iStoreOS 的 IP 地址
4. DNS：iStoreOS 的 IP 地址或公共 DNS

### 5.3 验证配置

```bash
# 在 SSH 中测试网络连接
ping -c 3 baidu.com
ping -c 3 google.com

# 测试代理是否生效
curl ip.sb
```

> [!info] 📚 来源
> - [「旁路由」教程总纲——如何更好地配置你的旁路由？](https://www.koolcenter.com/t/topic/4426) - iStoreOS社区
> - [使用iStoreOS作为旁路由](https://wiki.wbuntu.com/linux/pve/6-istoreos-as-bypass-router/) - Atlantis Wiki
> - [【OpenWrt】可视化配置iStoreOS旁路由配置小记](https://luotianyi.vc/9170.html) - Luminous' Home

---

## 六、常见问题

### Q1：iStore 中找不到 Passwall 插件？

> [!warning] 常见问题
> 这是 iStoreOS 用户最常遇到的问题，请按以下步骤逐一排查解决。

**原因分析**：
- 系统版本过旧或软件源未更新
- 防火墙类型不兼容（nftables vs iptables）
- 软件包列表需要刷新
- 插件依赖缺失

---

#### 解决方案一：系统修复工具（推荐首选）

这是官方推荐的最简单修复方法：

1. 进入 **iStore** 软件中心
2. 搜索并安装 **「系统便利工具」**
3. 打开后选择 **「修复系统软件」**
4. 等待修复完成，重启 iStore

> [!info] 📚 来源
> - [iStoreOS GitHub Discussions](https://github.com/istoreos/istoreos/discussions) - 官方讨论区

#### 解决方案二：检查防火墙类型

防火墙类型不兼容是导致插件找不到的常见原因：

```bash
# SSH 登录后检查防火墙类型
uci get firewall.@defaults[0].input
uci get firewall.@defaults[0].forward

# 如果显示 nftables，需要切换到 iptables
```

**切换防火墙类型**：

1. 进入 **网络** → **防火墙**
2. 查看当前使用的防火墙类型
3. 如果是 nftables，切换到 iptables
4. 重启路由器后重新搜索插件

> [!info] 📚 来源
> - [iStoreOS 防火墙兼容性讨论](https://github.com/istoreos/istoreos/discussions) - GitHub

#### 解决方案三：更新软件包列表

1. 进入 **系统** → **软件包**
2. 点击 **「更新列表」**
3. 等待更新完成后，在过滤器中输入 `passwall`
4. 如果找到，点击安装

#### 解决方案四：重新安装 Passwall2

如果已安装但无法使用：

1. 进入 **系统** → **软件包**
2. 过滤器中输入 `passwall2`
3. 移除旧版本
4. 更新软件包列表
5. 重新安装 Passwall2

> [!info] 📚 来源
> - [帅强来了博客：iStoreOS下直更新Passwall2](https://shuaiqiang.cc/istoreos%25E4%25B8%258B%25E6%259B%25B4%25E6%2596%25B0passwall2/)

#### 解决方案五：添加第三方软件源

如果官方源中没有插件，可以添加第三方源：

```bash
# 1. 编辑自定义软件源配置
vi /etc/opkg/customfeeds.conf

# 2. 添加 kenzok8 第三方源（根据你的架构选择）
# x86_64 架构：
src/gz kenzo https://op.dllkids.xyz/packages/x86_64

# aarch64 架构：
# src/gz kenzo https://op.dllkids.xyz/packages/aarch64_cortex-a53

# 3. 保存后更新软件源
opkg update

# 4. 搜索并安装
opkg list | grep passwall
opkg install luci-app-passwall2
```

**可用的第三方软件源**：

| 源名称 | 地址 | 说明 |
|--------|------|------|
| kenzok8 | `op.dllkids.xyz` | 包含大量常用插件 |

> [!danger] 注意
> 第三方软件源可能存在安全风险，请谨慎使用。

> [!info] 📚 来源
> - [kenzok8 软件包仓库](https://github.com/kenzok8/openwrt-packages) - GitHub
> - [OpenWrt 第三方软件源配置](https://cxorz.com/blog/openwrt-thirdparty) - Hanasaki 博客

#### 解决方案六：手动下载 IPK 安装

如果以上方法都无效，可以手动下载 IPK 包安装：

```bash
# 1. 确认系统架构
cat /etc/openwrt_release | grep ARCH
# 常见架构：x86_64, aarch64_cortex-a53, mipsel_24kc

# 2. 下载 IPK 包（示例）
cd /tmp
wget https://github.com/xiaorouji/openwrt-passwall2/releases/download/v1.28/luci-app-passwall2_1.28_all.ipk

# 3. 安装（忽略依赖）
opkg install --force-depends luci-app-passwall2_*.ipk

# 4. 如果提示缺少依赖，逐个安装
opkg install <缺失的依赖包名>
```

**常用 IPK 下载地址**：
- [Passwall2 Releases](https://github.com/xiaorouji/openwrt-passwall2/releases)
- [kenzok8 Packages](https://github.com/kenzok8/openwrt-packages)

---

#### 完整排查流程

```bash
#!/bin/bash
# 插件安装故障排查脚本 - 复制到路由器 SSH 执行

echo "=== iStoreOS Passwall 插件安装故障排查 ==="
echo ""

echo "1. 系统信息："
cat /etc/openwrt_release
echo ""

echo "2. 系统架构："
cat /etc/openwrt_release | grep ARCH
echo ""

echo "3. 存储空间："
df -h
echo ""

echo "4. 防火墙类型："
uci get firewall.@defaults[0].input 2>/dev/null || echo "无法获取"
echo ""

echo "5. 尝试更新软件源："
opkg update
echo ""

echo "6. 搜索 Passwall 插件："
opkg list | grep -i passwall
echo ""

echo "7. 检查已安装的 Passwall："
opkg list-installed | grep -i passwall
echo ""

echo "=== 排查完成 ==="
```

> [!tip] 建议操作顺序
> 按优先级尝试以下解决方案：
> 1. **系统修复工具** → 2. **检查防火墙类型** → 3. **更新软件包列表** → 4. **重新安装** → 5. **第三方源** → 6. **手动 IPK**

### Q2：订阅更新后没有节点？

**排查步骤**：
1. 检查订阅地址是否正确
2. 检查网络连接是否正常
3. 尝试关闭代理后更新
4. 联系机场服务商确认订阅状态

### Q3：代理后国内网站访问慢？

**解决方案**：
1. 确保分流规则正确配置
2. 检查国内域名/IP 是否在直连规则中
3. 确保 geoip 和 geosite 规则已启用

### Q4：如何验证代理是否生效？

**方法一：浏览器检测**
```
访问：https://ip.sb
显示的 IP 应为代理节点的 IP
```

**方法二：命令行检测**
```bash
curl ip.sb
```

**方法三：Passwall 状态页面**
```
路由器管理界面 → 服务 → PassWall2 → 状态
```

### Q5：代理速度慢怎么办？

**优化建议**：
1. 选择延迟更低的节点
2. 启用负载均衡功能
3. 尝试不同的代理协议
4. 检查路由器硬件性能

### Q6：如何备份和恢复配置？

```bash
# 备份配置
1. 进入 系统 → 备份/升级
2. 点击「生成备份」
3. 下载备份文件

# 恢复配置
1. 进入 系统 → 备份/升级
2. 选择备份文件
3. 点击「恢复备份」
```

---

## 最佳实践

### 1. 安全建议

- 定期更新 Passwall 插件
- 使用可靠的机场服务商
- 不要分享订阅链接
- 启用访问控制，防止蹭网

### 2. 性能优化

- 使用分流规则减少不必要的代理流量
- 启用节点负载均衡
- 定期清理无用节点

### 3. 维护建议

- 定期检查订阅更新状态
- 监控路由器资源使用情况
- 备份重要配置

---

## 相关文档

- [[../AI学习/02-工具使用/Tailscale使用指南]] - Tailscale VPN 组网
- [[../AI学习/00-索引/MOC]] - 知识库索引

---

## 参考资料

### 官方资源
- [iStoreOS 官方文档](https://doc.istoreos.com/zh/guide/istore/) - 易有云产品中心
- [iStore 社区](https://www.koolcenter.com/) - 酷友社区

### 视频教程
- [iStoreOS 软路由使用Passwall2](https://www.youtube.com/watch?v=vBFZtvWPqzQ) - YouTube
- [iStoreOS 软路由Passwall/Passwall2 进阶教程](https://www.youtube.com/watch?v=ifhmuCG8aHs) - YouTube
- [旁路由istoreOS、OpenWRT配置](https://www.youtube.com/watch?v=ksVjnEZ--Ak) - YouTube

### 社区教程
- [iStoreOS 快速入门指南](https://mathpretty.com/19518.html) - MathPretty
- [「旁路由」教程总纲](https://www.koolcenter.com/t/topic/4426) - iStoreOS社区
- [使用iStoreOS作为旁路由](https://wiki.wbuntu.com/linux/pve/6-istoreos-as-bypass-router/) - Atlantis Wiki
- [可视化配置iStoreOS旁路由配置小记](https://luotianyi.vc/9170.html) - Luminous' Home
- [Passwall 配置和网络负载均衡设置](https://www.cnblogs.com/MaelDNM/p/18330958) - 博客园

### 故障排查资源
- [iStoreOS GitHub Discussions](https://github.com/istoreos/istoreos/discussions) - 官方讨论区
- [2026年最新PassWall插件更新和安装](https://naiyous.com/10535.html) - 奶油博客
- [iStoreOS下直更新Passwall2](https://shuaiqiang.cc/istoreos%25E4%25B8%258B%25E6%259B%25B4%25E6%2596%25B0passwall2/) - 帅强来了博客
- [科技老王博客：新版Passwall负载均衡](https://kejilaowang.com/openwrt-istoreos-passwall-haproxy-socks/) - 科技老王
- [OpenWrt 第三方软件源配置](https://cxorz.com/blog/openwrt-thirdparty) - Hanasaki 博客
- [kenzok8 软件包仓库](https://github.com/kenzok8/openwrt-packages) - GitHub
- [Passwall2 Releases](https://github.com/xiaorouji/openwrt-passwall2/releases) - GitHub

### 硬件相关
- [iStoreOS默认IP地址及网络配置管理指南](https://comate.baidu.com/zh/page/8zqve692bec) - 百度 Comate
- [最强软路由系统iStoreOS_X86安装体验](https://blog.zwbcc.cn/archives/istoreosx86) - zwbcc博客

---

**最后更新**：2026-03-07
