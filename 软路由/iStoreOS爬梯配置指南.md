---
tags: [istoreos, 软路由, passwall, openclash, 代理, 爬梯, 旁路由]
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
| 安装 OpenClash 插件 | [[#三、OpenClash 安装配置]] |
| 了解各插件区别 | [[#四、代理插件对比]] |
| 配置节点订阅 | [[#五、节点订阅配置]] |
| 设置分流规则 | [[#六、分流规则设置]] |
| 配置旁路由模式 | [[#七、旁路由网络配置]] |
| 排查问题 | [[#八、常见问题]] |
| 找不到任何插件 | [[#q1：istore-中找不到任何爬梯插件？]] |

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

### 2.3 iStore 不可用时的备选安装方案

> [!warning] 如果 iStore 中找不到插件
> 以下是两种常用的备选安装方法：

#### 方案 A：添加官方软件源（推荐）

> [!tip] ✅ 推荐首选
> 这是 2026 年最新的官方安装方案，使用 SourceForge 官方源，稳定可靠。

```bash
# 1. 添加 opkg key
cd /tmp
wget -O passwall.pub https://master.dl.sourceforge.net/project/openwrt-passwall-build/passwall.pub
opkg-key add /tmp/passwall.pub

# 2. 自动写入软件源（根据系统版本和架构自动配置）
read release arch << EOF
$(. /etc/openwrt_release ; echo ${DISTRIB_RELEASE%.*} $DISTRIB_ARCH)
EOF

for feed in passwall_luci passwall_packages passwall2; do
  echo "src/gz $feed https://master.dl.sourceforge.net/project/openwrt-passwall-build/releases/packages-$release/$arch/$feed" >> /etc/opkg/customfeeds.conf
done

# 3. 更新索引
opkg update

# 你可以通过 `grep` 搜索关键字，比如查找 PassWall 相关包： 

opkg list | grep passwall

# 4. 安装 PassWall 或 PassWall2
opkg install luci-app-passwall      # PassWall
opkg install luci-app-passwall2     # PassWall2（推荐）

# 5. 刷新管理界面
/etc/init.d/uhttpd restart

# 6. 安装汉化（可选）
opkg install luci-i18n-passwall-zh-cn
opkg install luci-i18n-passwall2-zh-cn

# 7. 如果你想看哪些软件已经安装（相当于系统里已经“用掉”的安装包）：
opkg list-installed 

opkg list-installed | grep passwall
# 8. 删除安装包
opkg remove 包名
- 例如删除 PassWall： 
opkg remove luci-app-passwall
```

> [!info] 📚 来源
> - [2026年最新PassWall安装教程](https://naiyous.com/10535.html) - 奶油之家

#### 方案 B：使用第三方固件

如果官方源仍无法使用，可以考虑：

1. **使用预装插件的第三方固件**
   - 从 `https://github.com/AUK9527/Are-u-ok` 下载
   - 某些社区版本预装了代理插件

2. **手动下载 IPK 包安装**
   ```bash
   # 1. 确认系统架构
   cat /etc/openwrt_release | grep ARCH

   # 2. 下载 IPK 包（示例）
   cd /tmp
   wget https://github.com/xiaorouji/openwrt-passwall2/releases/download/v1.28/luci-app-passwall2_1.28_all.ipk

   # 3. 安装（忽略依赖）
   opkg install --force-depends luci-app-passwall2_*.ipk

   # 4. 如果提示缺少依赖，逐个安装
   opkg install <缺失的依赖包名>
   ```

> [!danger] 注意
> 第三方固件可能存在安全风险，请从可信渠道获取。

---

## 三、OpenClash 安装配置

### 2.1 什么是 OpenClash

**OpenClash** 是基于 Clash 内核的 OpenWrt 代理插件，功能强大且规则灵活：

| 特性 | 说明 |
|------|------|
| **内核** | Clash Meta（支持更多协议） |
| **规则系统** | 基于 YAML 的灵活规则 |
| **游戏模式** | 专用游戏规则优化 |
| **假链接过滤** | 内置广告拦截 |

### 2.2 通过 iStore 安装

#### 步骤 1：进入 iStore

1. 浏览器打开 iStoreOS 管理界面
2. 进入 **iStore** 软件中心
3. 搜索 **OpenClash**

#### 步骤 2：安装插件

1. 点击「安装」
2. 等待安装完成
3. 安装后点击「打开」

> [!info] 📚 来源
> - [OpenClash 官方教程](https://openclash.org/) - 官方网站
> - [OpenClash 安装指南](https://clashproxy.net/openclash) - 配置教程

### 2.3 iStore 不可用时的备选安装方案

> [!warning] 如果 iStore 中找不到插件
> 以下是两种常用的备选安装方法：

#### 方案 A：添加官方软件源（推荐）

> [!tip] ✅ 推荐首选
> 这是 2026 年最新的官方安装方案，使用 SourceForge 官方源，稳定可靠。

```bash
# 1. 添加 opkg key
cd /tmp
wget -O passwall.pub https://master.dl.sourceforge.net/project/openwrt-passwall-build/passwall.pub
opkg-key add /tmp/passwall.pub

# 2. 自动写入软件源（根据系统版本和架构自动配置）
read release arch << EOF
$(. /etc/openwrt_release ; echo ${DISTRIB_RELEASE%.*} $DISTRIB_ARCH)
EOF

for feed in passwall_luci passwall_packages passwall2; do
  echo "src/gz $feed https://master.dl.sourceforge.net/project/openwrt-passwall-build/releases/packages-$release/$arch/$feed" >> /etc/opkg/customfeeds.conf
done

# 3. 更新索引
opkg update

# 4. 安装 OpenClash
opkg install luci-app-openclash

# 5. 刷新管理界面
/etc/init.d/uhttpd restart
```

> [!info] 📚 来源
> - [2026年最新PassWall安装教程](https://naiyous.com/10535.html) - 奶油之家

#### 方案 B：使用第三方固件

如果官方源仍无法使用，可以考虑：

1. **使用预装插件的第三方固件**
   - 从 `https://github.com/AUK9527/Are-u-ok` 下载
   - 某些社区版本预装了代理插件

2. **手动下载 IPK 包安装**
   ```bash
   # 1. 确认系统架构
   cat /etc/openwrt_release | grep ARCH

   # 2. 下载 OpenClash IPK 包
   cd /tmp
   wget https://github.com/vernesong/OpenClash/releases/download/v0.46.033-beta/luci-app-openclash_0.46.033-beta_all.ipk

   # 3. 安装（忽略依赖）
   opkg install --force-depends luci-app-openclash_*.ipk

   # 4. 如果提示缺少依赖，逐个安装
   opkg install <缺失的依赖包名>
   ```

> [!danger] 注意
> 第三方固件可能存在安全风险，请从可信渠道获取。

### 2.4 配置文件订阅

#### 步骤 1：进入配置订阅

1. 进入 **服务** → **OpenClash**
2. 切换到 **配置文件订阅** 标签

#### 步骤 2：添加订阅

```yaml
# 配置订阅信息
配置名称: 我的机场
订阅地址: https://your-subscription-url
自动更新: 开启
更新间隔: 24小时
```

#### 步骤 3：更新配置

1. 点击「保存并应用」
2. 点击「更新配置」
3. 等待节点加载完成

> [!info] 📚 来源
> - [OpenClash 付费节点教程](https://clash.guide/clients/router/openclash.html) - Clash Guide
> - [GitHub 详细设置方案](https://github.com/Aethersailor/Custom_OpenClash_Rules/wiki/OpenClash-%25E8%25AE%25BE%25E7%25BD%25AE%25E6%2596%25B9%25E6%25A1%2588) - GitHub Wiki

### 2.5 启动代理

#### 步骤 1：选择配置

1. 在 **覆盖设置** 中选择配置文件
2. 启用 **IPK 设置**

#### 步骤 2：启动核心

1. 切换到 **运行状态** 标签
2. 选择核心模式（推荐：Fake-IP 模式）
3. 点击「启动」

#### 步骤 3：验证

```bash
# 测试代理是否生效
curl ip.sb
```

### 2.6 规则设置

OpenClash 的规则系统非常灵活：

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClash 规则流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  流量进入                                                   │
│     │                                                       │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 广告/追踪 │ ────────→ │ REJECT  │ → 拦截                 │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐    是     ┌─────────┐                         │
│  │ 国内IP/域名│ ──────→ │ DIRECT  │ → 直连                 │
│  └─────────┘           └─────────┘                         │
│     │ 否                                                    │
│     ▼                                                       │
│  ┌─────────┐           ┌─────────┐                         │
│  │ 其他流量 │ ────────→ │ PROXY   │ → 代理                  │
│  └─────────┘           └─────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.7 核心模式选择

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| **Fake-IP** | 假 IP 模式，性能最佳 | 日常使用 |
| **Redir-Host** | 还原域名模式 | 需要真实域名的场景 |
| **TUN 模式** | 虚拟网卡模式 | 支持所有协议 |

> [!tip] 推荐选择
> 新手推荐使用 **Fake-IP 模式**，性能最佳且兼容性好。

---

## 四、代理插件对比

### 3.1 四大主流插件对比

| 特性 | OpenClash | Passwall | Passwall2 | HomeProxy |
|------|-----------|----------|-----------|-----------|
| **内核** | Clash Meta | 多协议支持 | 精简优化 | sing-box |
| **功能** | ⭐⭐⭐ 最强大 | ⭐⭐⭐ 全面 | ⭐⭐ 精简 | ⭐⭐⭐ 现代 |
| **性能** | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐⭐ 优秀 | ⭐⭐⭐ 优秀 |
| **资源占用** | 较高 | 中等 | 低 | 低 |
| **配置复杂度** | 复杂 | 中等 | 简单 | 简单 |
| **规则灵活性** | ⭐⭐⭐ 最高 | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐ 高 |
| **适配系统** | 通用 OpenWrt | 通用 OpenWrt | 通用 OpenWrt | **ImmortalWrt** |
| **适合人群** | 进阶用户 | 功能党 | 稳定党/新手 | 追新党 |

### 3.2 如何选择插件

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
│     ├─ 新手/追求稳定 ────────→ 推荐 Passwall2               │
│     │                                                       │
│     ├─ 需要复杂规则/进阶 ────→ 推荐 OpenClash               │
│     │                                                       │
│     └─ 需要全部功能 ────────→ 推荐 Passwall                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 详细对比说明

#### OpenClash

**优势**：
- 规则系统最灵活，支持自定义 YAML 规则
- 社区规则丰富，有大量现成规则可用
- 支持游戏模式优化
- 假链接过滤功能强大

**劣势**：
- 配置复杂，新手上手困难
- 资源占用较高
- 需要手动管理规则更新

**推荐场景**：
- 需要高度自定义规则
- 需要游戏加速优化
- 对网络技术有一定了解

> [!info] 📚 来源
> - [OpenClash 官方教程](https://openclash.org/) - 官方网站
> - [GitHub 详细设置方案](https://github.com/Aethersailor/Custom_OpenClash_Rules/wiki) - GitHub

#### Passwall

**优势**：
- 功能最全面，支持多种协议
- 图形界面配置相对简单
- 支持负载均衡和故障转移

**劣势**：
- 资源占用中等
- 性能不如 Passwall2

**推荐场景**：
- 需要使用多种协议
- 需要负载均衡功能
- 功能需求全面

#### Passwall2

**优势**：
- 资源占用最低
- 性能优秀，稳定性好
- 配置简单，适合新手
- 日常使用完全足够

**劣势**：
- 功能相对精简
- 规则灵活性不如 OpenClash

**推荐场景**：
- **新手首选**
- 追求稳定和性能
- 日常基本使用

> [!info] 📚 来源
> - [iStoreOS 软路由Passwall/Passwall2 进阶教程](https://www.youtube.com/watch?v=ifhmuCG8aHs) - YouTube

#### HomeProxy

**优势**：
- 基于 sing-box 内核，性能优秀
- 现代化 Web 界面
- 支持 ARM64/AMD64 架构
- 规则系统现代化

**劣势**：
- 主要针对 ImmortalWrt 系统
- 标准 OpenWrt 可能需要额外配置

**推荐场景**：
- 使用 ImmortalWrt 系统
- 追求现代化界面

> [!warning] 注意
> HomeProxy 主要针对 **ImmortalWrt** 系统，标准 OpenWrt 可能需要额外确认兼容性。

### 3.4 性能对比

根据社区测试，各插件性能表现大致如下：

| 测试项目 | OpenClash | Passwall | Passwall2 | HomeProxy |
|---------|-----------|----------|-----------|-----------|
| CPU 占用 | 较高 | 中等 | 低 | 低 |
| 内存占用 | 较高 | 中等 | 低 | 低 |
| 启动速度 | 较慢 | 中等 | 快 | 快 |
| 吞吐量 | 中等 | 中等 | 高 | 高 |

> [!tip] 性能建议
> - **性能优先**：Passwall2 或 HomeProxy
> - **功能优先**：OpenClash 或 Passwall
> - **平衡选择**：Passwall2

---

## 五、节点订阅配置

### 4.1 获取订阅地址

从你的机场服务商获取订阅链接，格式通常为：
```
https://xxx.com/api/v1/client/subscribe?token=xxxxx
```

### 4.2 添加订阅

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

### 4.3 订阅链接安全

> [!danger] 安全提醒
> - 订阅链接包含你的账号信息，不要分享给他人
> - 不要在公开场合截屏包含订阅链接的图片
> - 定期更换订阅链接保障安全

---

## 六、分流规则设置

### 5.1 什么是分流规则

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

### 5.2 基本分流配置

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

### 5.3 自定义规则

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

## 七、旁路由网络配置

### 6.1 什么是旁路由

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

### 6.2 旁路由模式配置

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

### 6.3 验证配置

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

## 八、常见问题

### Q1：iStore 中找不到任何爬梯插件？

> [!warning] 重要提示
> 如果你发现 iStore 商店中完全没有任何代理插件（Passwall、OpenClash 等），这可能是以下原因：

**原因分析**：
- **官方固件限制** - 由于法律/政策原因，官方固件可能不包含代理插件
- **软件源未更新** - 插件列表需要从服务器获取
- **海外用户网络问题** - 无法访问 `istore.istoreos.com`
- **系统版本过旧** - 需要更新到最新版本

---

#### 解决方案一：使用第三方固件

如果官方固件确实不包含代理插件，可以考虑：

1. **使用第三方定制的 iStoreOS 固件**
   - 某些社区版本预装了代理插件
   - 参考酷友社等社区的固件分享
推荐用：`https://github.com/AUK9527/Are-u-ok.git` 中下载固件。
1. **手动安装 IPK 包**
   - 从 GitHub 下载 IPK 包
   - 使用 `opkg install` 命令安装

> [!danger] 注意
> 第三方固件可能存在安全风险，请从可信渠道获取。

---

#### 解决方案二：系统修复工具

这是官方推荐的最简单修复方法：

1. 进入 **iStore** 软件中心
2. 搜索并安装 **「系统便利工具」**
3. 打开后选择 **「修复系统软件」**
4. 等待修复完成，重启 iStore

> [!info] 📚 来源
> - [iStoreOS GitHub Discussions](https://github.com/istoreos/istoreos/discussions) - 官方讨论区

#### 解决方案三：添加官方软件源（2026年最新方案，推荐）

> [!tip] ✅ 推荐首选
> 这是 2026 年最新的官方安装方案，使用 SourceForge 官方源，稳定可靠。

```bash
# 1. 添加 opkg key
cd /tmp
wget -O passwall.pub https://master.dl.sourceforge.net/project/openwrt-passwall-build/passwall.pub
opkg-key add /tmp/passwall.pub

# 2. 自动写入软件源（根据系统版本和架构自动配置）
read release arch << EOF
$(. /etc/openwrt_release ; echo ${DISTRIB_RELEASE%.*} $DISTRIB_ARCH)
EOF

for feed in passwall_luci passwall_packages passwall2; do
  echo "src/gz $feed https://master.dl.sourceforge.net/project/openwrt-passwall-build/releases/packages-$release/$arch/$feed" >> /etc/opkg/customfeeds.conf
done

# 3. 更新索引
opkg update

# 你可以通过 `grep` 搜索关键字，比如查找 PassWall 相关包： 

opkg list | grep passwall

# 4. 安装 PassWall 或 PassWall2
opkg install luci-app-passwall      # PassWall
opkg install luci-app-passwall2     # PassWall2（推荐）

# 5. 刷新管理界面
/etc/init.d/uhttpd restart

# 6. 安装汉化（可选）
opkg install luci-i18n-passwall-zh-cn
opkg install luci-i18n-passwall2-zh-cn

# 7. 如果你想看哪些软件已经安装（相当于系统里已经“用掉”的安装包）：
opkg list-installed 

opkg list-installed | grep passwall
# 8. 删除安装包
opkg remove 包名
- 例如删除 PassWall： 
opkg remove luci-app-passwall
```

> [!info] 📚 来源
> - [2026年最新PassWall安装教程](https://naiyous.com/10535.html) - 奶油之家
> - [kenzok8 软件包仓库](https://github.com/kenzok8/openwrt-packages) - GitHub（备用）

#### 解决方案四：手动下载 IPK 安装

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
