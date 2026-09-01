---
tags: [istoreos, 软路由, passwall, openclash, 代理, 爬梯, 旁路由]
created: 2026-03-07
updated: 2026-09-01
---

# iStoreOS 爬梯配置指南

> [!info] 概述
> **iStoreOS 是易有云团队基于 OpenWRT 开发的软路由系统，内置 iStore 软件中心，可以方便地安装 Passwall 等代理插件实现网络代理**。

## 快速导航

| 我想...           | 跳转章节                       |
| --------------- | -------------------------- |
| 了解 iStoreOS 是什么 | [[#一、iStoreOS 简介]]         |
| 了解各插件区别         | [[#二、代理插件对比]]              |
| 配置 Passwall    | [[#三、Passwall 完整配置]]         |
| 配置 OpenClash   | [[#四、OpenClash 安装配置]]      |
| 配置旁路由模式         | [[#五、旁路由网络配置]]             |
| 排查问题            | [[#六、常见问题]]                |
| 找不到任何插件         | [[#q1：istore-中找不到任何爬梯插件？]] |

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
| **最新版本** | 24.10.8（2026-07-31 发布，稳定版）；25.12 测试版已发布（2026-08-17） |

> [!warning] ⚠️ 版本说明（2026-08 更新）
> - **当前稳定版为 24.10.8**（2026-07-31 发布）。
> - **25.12 测试版已发布**（2026-08-17，基于 OpenWrt 25.12.5）：包管理器由 `opkg` 切换为 **`apk`**，且**不支持从 24.10 保留配置升级**（ipk/apk 两套包不兼容）。升级路径：先在 24.10 中备份配置 → 重刷/不保留配置升级 → 恢复备份，自装软件需重新安装。
> - 测试版存在稳定性风险（社区有反馈丢 IP、联发科硬件加速等问题），新手建议仍使用 24.10.8 稳定版。

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

## 二、代理插件对比

> [!tip] 学习建议
> 在安装插件之前，先了解各插件的特点和区别，选择最适合你需求的插件。

### 2.1 四大主流插件对比

| 特性 | OpenClash | Passwall | Passwall2 | HomeProxy |
|------|-----------|----------|-----------|-----------|
| **内核** | Clash Meta | 多协议支持 | 精简优化 | sing-box |
| **功能** | ⭐⭐⭐ 最强大 | ⭐⭐⭐ 全面 | ⭐⭐ 精简 | ⭐⭐⭐ 现代 |
| **性能** | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐⭐ 优秀 | ⭐⭐⭐ 优秀 |
| **资源占用** | 较高 | 中等 | 低 | 低 |
| **配置复杂度** | 复杂 | 中等 | 简单 | 简单 |
| **规则灵活性** | ⭐⭐⭐ 最高 | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐ 高 |
| **当前版本** | v0.47.156 | 26.8.11-1 | 26.8.27-1 | v0.0.11 |
| **适配系统** | 通用 OpenWrt | 通用 OpenWrt | 通用 OpenWrt | **ImmortalWrt / OpenWrt 23.05+** |
| **适合人群** | 进阶用户 | 功能党 | 稳定党/新手 | 追新党 |

### 2.2 如何选择插件

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

### 2.3 详细对比说明

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

**版本说明**：自 2026 年起，Passwall2 版本号改为 **YY.M.DD-N** 格式（如 `26.8.27-1` 表示 2026 年 8 月 27 日第 1 版），不再使用旧版 `v1.xx` 格式。Passwall（v1）与 Passwall2 为独立仓库、版本各自推进。搭配的核心组件也持续更新：xray-core 更新至 26.7.28，sing-box 更新至 1.13.19。

> [!warning] 注意
> sing-box 1.13+ 已弃用旧版 DNS 配置格式，升级后需迁移 DNS 设置；新版本 xray-core 移除了 `allowInsecure` 参数，改为 `pinnedPeerCertSha256`。

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
> HomeProxy 主要面向 **ImmortalWrt / OpenWrt 23.05+** 系统；基于 sing-box 内核，依赖 `firewall4`、`kmod-nft-tproxy`、`ucode-mod-digest`。目前不支持 XHTTP 类型节点。

### 2.4 性能对比

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

## 三、Passwall 完整配置

> [!tip] 新手推荐
> Passwall2 是新手的首选，配置简单、性能优秀、稳定性好。

### 3.1 安装 Passwall

#### 3.1.1 什么是 Passwall

**Passwall** 是 OpenWrt 系统上最流行的代理插件，支持多种协议：

| 支持的协议 | 说明 |
|-----------|------|
| VMess/VLess | V2协议系列 |
| Trojan | 木马协议 |
| Shadowsocks | SS协议 |
| Hysteria2 | 新一代UDP协议 |
| Tuic | 协议 |

> [!tip] Passwall vs Passwall2
> - **Passwall**：功能全面，支持更多协议
> - **Passwall2**：精简版本，资源占用更低，稳定性更好
>
> 新手推荐使用 **Passwall2**

#### 3.1.2 安装 Passwall / Passwall2

> [!warning] 官方 iStore 商店默认不含 Passwall/Passwall2（法律/政策原因）
> 官方固件的 iStore 商店搜索不到代理插件，需从以下方案中选择一种安装插件本体；iStoreOS 用户最常用**方案 C**（iStore 手动安装 `.run` 包）。

**方案 C：通过 iStore 手动安装 `.run` 包（iStoreOS 推荐）**

> [!tip] ✅ 官方商店搜不到时的首选
> 这是 iStoreOS 用户最主流的安装方式：下载社区打包的 `.run` 安装包，在 iStore 中手动安装，图形化且操作简单。适用于 Passwall / Passwall2 / OpenClash 等。

> [!info] `.run` 包来源（24.10 专用）
> iStoreOS 24.10 的 `.run` 代理插件包位于 [bcseputetto/Are-u-ok 的 iStoreOS_24.10 Release](https://github.com/bcseputetto/Are-u-ok/releases/tag/iStoreOS_24.10)。原 AUK9527/Are-u-ok 主仓库仅维护 22.03 的 aarch64 包，24.10 已由 bcseputetto 接手维护。文件名格式 `PassWall2_<版本>_<架构>_all_sdk_24.10.run`，按架构（x86_64 / aarch64）选择。

```bash
# 1. 确认系统架构（x86_64 / aarch64 等）
source /etc/os-release; echo $OPENWRT_ARCH

# 2. 下载 .run 包（以 x86_64 为例；文件名按架构选择，以 Release 页实际为准）
cd /tmp
wget https://github.com/bcseputetto/Are-u-ok/releases/download/iStoreOS_24.10/PassWall2_26.8.27_x86_64_all_sdk_24.10.run

# 3. 方式一：iStore 后台「手动安装」上传 .run 文件
#    方式二：命令行直接执行（无 iStore 商店也可用）
sh /tmp/PassWall2_*.run
```

> [!warning] 注意
> - 安装前建议移除自行添加的第三方 opkg 软件源，避免依赖冲突。
> - 部分依赖仍需在线安装，请确保路由器自身联网正常（旁路由场景最易踩坑）；软件源可先切换到国内镜像（见 [[#3.1.3 前置准备：切换软件源到国内镜像]]）。
> - 不建议 Passwall 系列与 SSR-Plus 同时安装（存在包冲突）。
> - `.run` 包体积较大（PassWall2 约 58MB、PassWall 约 79MB），安装前确认剩余存储空间充足。

**方案 A：添加官方软件源（推荐）**

> [!tip] ✅ 推荐首选
> 这是 2026 年最新的官方安装方案，使用 SourceForge 官方源，稳定可靠。

> [!warning] 25.12（apk）用户注意
> 上述 `opkg` 源配置方式适用于 24.10 及之前版本。25.12 已切换为 `apk` 包管理器，软件源配置文件位于 `/etc/apk/repositories.d/`，需使用 `apk update` / `apk add` 等命令（opkg→apk 命令对照见 §1 版本说明）。

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

# 4. 安装依赖（透明代理依赖 nftables tproxy 内核模块）
opkg install kmod-nft-tproxy kmod-nft-socket
# 可选：替换为 dnsmasq-full（推荐，兼容性更好；若与 dnsmasq 冲突先移除）
opkg remove dnsmasq && opkg install dnsmasq-full

# 5. 安装 PassWall 或 PassWall2
opkg install luci-app-passwall      # PassWall
opkg install luci-app-passwall2     # PassWall2（推荐）

# 6. 刷新管理界面
/etc/init.d/uhttpd restart

# 7. 安装汉化（可选）
opkg install luci-i18n-passwall-zh-cn
opkg install luci-i18n-passwall2-zh-cn
```

> [!warning] 方案 A 注意
> - `opkg-key add` 命令为 24.10（opkg）专用；25.12（apk）无此命令，配置方式见 §1 版本说明。
> - 该 SourceForge 软件源仅提供 passwall_luci / passwall_packages / passwall2 三个 feed，**不包含 OpenClash**；OpenClash 安装见 §4。
> - Passwall2 安装后体积较大（含 xray-core / sing-box），请确认剩余存储空间充足。
> - 不要与 SSR-Plus 同时安装（存在包冲突）。

> [!info] 📚 来源
> - [2026年最新PassWall安装教程](https://naiyous.com/10535.html) - 奶油之家

**方案 B：手动下载 IPK 安装**

如果官方源仍无法使用：

```bash
# 1. 确认系统架构
cat /etc/openwrt_release | grep ARCH

# 2. 安装依赖（透明代理依赖 nftables tproxy 内核模块）
opkg update
opkg install kmod-nft-tproxy kmod-nft-socket
# 可选：替换为 dnsmasq-full（推荐，兼容性更好；若与 dnsmasq 冲突先移除）
opkg remove dnsmasq && opkg install dnsmasq-full

# 3. 下载 IPK 包（版本号格式为 YY.M.DD-N，以 releases 页最新为准）
cd /tmp
wget https://github.com/Openwrt-Passwall/openwrt-passwall2/releases/download/26.8.27-1/luci-app-passwall2_26.8.27-1_all.ipk

# 4. 安装（忽略依赖）
opkg install --force-depends luci-app-passwall2_*.ipk

# 5. 如果提示缺少依赖，逐个安装
opkg install <缺失的依赖包名>
```

> [!danger] 注意
> 第三方固件可能存在安全风险，请从可信渠道获取。

---

### 3.1.3 前置准备：切换软件源到国内镜像

> [!tip] 什么时候需要
> 安装 Passwall/OpenClash 时，大部分依赖包（如 `kmod-nft-tproxy`、`dnsmasq-full`）需从 opkg 软件源在线安装。iStoreOS 默认 OpenWrt 官方源在海外，国内下载慢或经常失败。**安装前先 `opkg update`，并把软件源切换到可访问的国内镜像（如阿里云）**。

#### ① 软件源配置文件

iStoreOS 用 opkg 管理软件包，软件源分两个文件：

| 文件 | 作用 |
|------|------|
| `/etc/opkg/distfeeds.conf` | 系统默认源：OpenWrt 官方包源（base / luci / packages / routing / telephony）+ iStoreOS 自身源 |
| `/etc/opkg/customfeeds.conf` | 第三方源（如 §3.1.2 方案 A 的 passwall SourceForge 源） |

换源时只换「OpenWrt 包源」部分，**不要动 iStoreOS 自身源，也不要乱混第三方源**，否则 iStore 商店可能无法安装应用。改前先备份。

#### ② 可用的国内镜像（2026-09 实测）

| 镜像 | 地址前缀 | 说明 |
|------|----------|------|
| **阿里云** | `mirrors.aliyun.com/openwrt` | CDN 快；24.10 点版本仅同步到 24.10.5，24.10.8 需走连续源 `releases/packages-24.10/`；GUI 一键选择最省事 |
| **清华 TUNA** | `mirrors.tuna.tsinghua.edu.cn/openwrt` | ✅ 24.10.8 全部 feed 可用 |
| **中科大 USTC** | `mirrors.ustc.edu.cn/openwrt` | ✅ 24.10.8 全部 feed 可用 |
| 南京大学 / 兰州大学 | `mirror.nju.edu.cn/openwrt`、`mirrors.lzu.edu.cn/openwrt` | 备选 |

#### ③ 方法一：GUI 切换（推荐）

1. 登录 iStoreOS 后台 → **首页**
2. 找到「**软件源配置**」卡片 → 点开
3. 「切换软件源」选择「**阿里云**」（或其它镜像）
4. 确认保存 → SSH 执行 `opkg update` 验证

> GUI 会自动处理版本号与架构路径，换阿里云建议走 GUI。

#### ④ 方法二：命令行 sed 替换

```bash
# 1. 备份
cp /etc/opkg/distfeeds.conf /etc/opkg/distfeeds.conf.bak

# 2. 把 OpenWrt 官方源替换为国内镜像（清华示例）
sed -i 's|downloads\.openwrt\.org|mirrors.tuna.tsinghua.edu.cn/openwrt|g' /etc/opkg/distfeeds.conf
# 中科大：将域名换成 mirrors.ustc.edu.cn/openwrt 即可

# 3. 更新索引
opkg update
```

> [!tip] 先看实际域名
> 部分 iStoreOS 固件把 OpenWrt 包源也放在自己的服务器（如 `downloads.istoreos.com` / `istoreos.com`）。换源前先 `cat /etc/opkg/distfeeds.conf` 确认域名，再把其中 **OpenWrt 官方/自带包源**的域名整体替换成镜像前缀即可，istoreos 自身源保留。

> [!warning] 阿里云不要用纯域名 sed
> 若 `distfeeds.conf` 里是 `releases/24.10.8/...` 这类点版本路径，阿里云只同步到 24.10.5 会返回 404。命令行换源首选清华/中科大；阿里云走 GUI。

#### ⑤ 验证与注意

```bash
opkg update
opkg list | grep -i passwall   # 能列出候选包即源正常
```

> [!warning] 常见坑
> - **架构必须匹配**：`opkg print-architecture` 查看（如 `x86_64`、`aarch64_cortex-a53`），URL 架构段错误必 404。
> - **旁路由先确认自身联网**：换源解决不了「路由器本身没网」。旁路由未配好代理前，路由器自身必须能直连镜像源，否则 `opkg update` 照样失败。
> - **改坏后的官方修复**：`sh -c "$(curl -sSL http://fw.koolcenter.com/iStoreOS/alpha/fix-istore.sh)"`
> - **25.12（apk）差异**：配置文件在 `/etc/apk/repositories.d/`，命令为 `apk update` / `apk add`。
> - ⚠️ **kenzok8 `op.supes.top` 源已失效**（2026-09 实测重定向到 `dl.openwrt.ai` 返回 404），不要使用；其 GitHub 仓库 releases 仍可手动下载 IPK（见参考资料）。

---

### 3.2 配置节点订阅

#### 3.2.1 获取订阅地址

从你的机场服务商获取订阅链接，格式通常为：
```
https://xxx.com/api/v1/client/subscribe?token=xxxxx
```

#### 3.2.2 添加订阅

**步骤 1：进入订阅管理**

1. 进入 **服务** → **PassWall2**
2. 切换到 **节点订阅** 标签

**步骤 2：配置订阅**

```yaml
# 订阅配置示例
订阅名称: 我的机场
订阅地址: https://your-subscription-url
自动更新: 开启
更新间隔: 24小时
```

**步骤 3：更新节点**

1. 点击「保存并应用」
2. 点击「手动更新」获取节点
3. 切换到 **节点** 标签查看是否成功

> [!warning] 订阅失败排查
> - 检查订阅地址是否正确
> - 检查路由器网络是否正常
> - 尝试关闭代理后更新订阅

#### 3.2.3 订阅链接安全

> [!danger] 安全提醒
> - 订阅链接包含你的账号信息，不要分享给他人
> - 不要在公开场合截屏包含订阅链接的图片
> - 定期更换订阅链接保障安全

---

### 3.3 配置分流规则

#### 3.3.1 什么是分流规则

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

#### 3.3.2 基本分流配置

**步骤 1：启用规则管理**

1. 进入 **基本设置** → **规则管理**
2. 勾选以下选项：
   - ☑ **geoip** - IP 地理位置规则
   - ☑ **geosite** - 域名分类规则

**步骤 2：配置分流规则**

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

**步骤 3：应用规则**

1. 点击「保存并应用」
2. 在 **状态** 页面查看规则是否生效

#### 3.3.3 自定义规则

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

### 3.4 启动代理

**步骤 1：选择节点**

1. 进入 **服务** → **PassWall2**
2. 在 **节点** 列表中选择一个可用节点

**步骤 2：启动代理**

1. 点击主开关，启用代理
2. 等待连接建立

**步骤 3：验证**

```bash
# 测试代理是否生效
curl ip.sb
```

---

## 四、OpenClash 安装配置

> [!tip] 进阶用户选择
> OpenClash 适合需要高度自定义规则和游戏加速优化的进阶用户。

### 4.1 什么是 OpenClash

**OpenClash** 是基于 Clash 内核的 OpenWrt 代理插件，功能强大且规则灵活。当前版本 v0.47.156（2026-08-10）。

| 特性 | 说明 |
|------|------|
| **内核** | Clash Meta（支持更多协议） |
| **规则系统** | 基于 YAML 的灵活规则 |
| **游戏模式** | 专用游戏规则优化 |
| **假链接过滤** | 内置广告拦截 |

**v0.47.x 新特性**：
- **LuCI 界面重构** — 更现代化的管理界面
- **订阅与配置管理分离** — 各自独立维护，不再耦合
- **覆写设置系统** — 不修改原始订阅文件即可注入自定义规则
- **多订阅合并** — 可将多个机场订阅节点合并到同一配置
- **内核管理页面** — 支持直接在线更新 Mihomo / Clash Premium 内核

### 4.2 安装 OpenClash

> [!warning] 官方 iStore 商店默认不含 OpenClash（法律/政策原因）
> 官方固件的 iStore 商店搜索不到 OpenClash，需从以下方案中选择一种安装插件本体；iStoreOS 用户最常用**方案 C**（iStore 手动安装 `.run` 包）。

**方案 C：通过 iStore 手动安装 `.run` 包（iStoreOS 推荐）**

> [!tip] ✅ 官方商店搜不到时的首选
> 从社区插件库下载 OpenClash 的 `.run` 包（已内置 Clash 核心），在 iStore「手动安装」上传即可。

> [!info] `.run` 包来源（24.10 专用）
> iStoreOS 24.10 的 `.run` 包位于 [bcseputetto/Are-u-ok 的 iStoreOS_24.10 Release](https://github.com/bcseputetto/Are-u-ok/releases/tag/iStoreOS_24.10)。文件名格式 `OpenClash_<版本>+<架构>_core_sdk_24.10.run`，其中 `+core` 表示已内置 Clash/Mihomo 内核，安装后无需再单独下载核心。

```bash
# 1. 确认系统架构
source /etc/os-release; echo $OPENWRT_ARCH

# 2. 下载 OpenClash .run 包（以 x86_64 为例；文件名以 Release 页实际为准）
cd /tmp
wget https://github.com/bcseputetto/Are-u-ok/releases/download/iStoreOS_24.10/OpenClash_0.47.156+x86_64_core_sdk_24.10.run

# 3. 方式一：iStore 后台「手动安装」上传 .run 文件
#    方式二：命令行直接执行
sh /tmp/OpenClash_*.run
```

> [!warning] 注意
> - 安装前建议移除自行添加的第三方 opkg 软件源，避免依赖冲突。
> - `.run` 包约 21MB（已含内核），安装前确认剩余存储空间充足。

**方案 A：一键安装脚本（推荐备选）**

> [!tip] 适合命令行用户
> OpenClash 没有官方 opkg 预编译包（`opkg list | grep clash` 为空），社区维护的一键脚本是更稳妥的方式，OpenWrt / iStoreOS / ImmortalWrt 通用。

```bash
# 一键安装 OpenClash（菜单式，支持安装/更新/卸载/内核管理）
wget -qO /usr/bin/openclash-menu https://raw.githubusercontent.com/slobys/openclash-auto-installer/main/menu.sh && chmod +x /usr/bin/openclash-menu && openclash-menu
```

> [!warning] 注意
> - 安装前先 `opkg update`，并把 iStoreOS 软件源切换到可访问的国内镜像（见 [[#3.1.3 前置准备：切换软件源到国内镜像]]）。
> - 确保路由器自身联网正常（旁路由场景最易失败）。
> - 若脚本方式不可用，退回方案 C（`.run`）或方案 B（手动 IPK）。

**方案 B：手动下载 IPK 安装**

```bash
# 1. 确认系统架构
cat /etc/openwrt_release | grep ARCH

# 2. 下载 OpenClash IPK 包
cd /tmp
# 获取最新版本号（以 v0.47.156 为例，以 releases 页为准）
wget https://github.com/vernesong/OpenClash/releases/download/v0.47.156/luci-app-openclash_0.47.156_all.ipk

# 3. 先安装 OpenClash 依赖（缺依赖会导致启动失败；24.10 为 nftables 栈，需 nft-tproxy / tun）
opkg update
opkg install coreutils-nohup bash curl jsonfilter ca-certificates ip-full dnsmasq-full unzip kmod-tun kmod-inet-diag kmod-nft-tproxy luci-compat

# 4. 安装主包
opkg install --force-depends luci-app-openclash_*.ipk
```

> [!warning] 注意
> - IPK 依赖从 GitHub 下载，国内网络可能失败；失败时优先检查路由器外网连通性。
> - 第三方来源 IPK 存在安全风险，请从可信渠道获取。

### 4.3 配置文件订阅

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
> - [GitHub 详细设置方案](https://github.com/Aethersailor/Custom_OpenClash_Rules/wiki) - GitHub Wiki

### 4.4 启动代理

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

### 4.5 规则设置

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

### 4.6 核心模式选择

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| **Fake-IP** | 假 IP 模式，性能最佳 | 日常使用 |
| **Redir-Host** | 还原域名模式 | 需要真实域名的场景 |
| **TUN 模式** | 虚拟网卡模式 | 支持所有协议 |

> [!tip] 推荐选择
> 新手推荐使用 **Fake-IP 模式**，性能最佳且兼容性好。

> [!warning] v0.47.x 已知问题
> - **无法随系统启动**：该问题最初出现在 v0.47.055-beta 早期版本；当前已迭代至 v0.47.156，建议先升级到最新版观察是否修复，若仍无法自启再按社区方案排查。
> - **iStoreOS 升级冲突**：从旧版 iStoreOS 升级到 24.10.8 后，OpenClash 可能与新系统发生冲突，导致部分游戏无法登录。升级前建议使用 U 盘进行全量备份。

---

## 五、旁路由网络配置

> [!tip] 📖 延伸阅读
> 想深入理解旁路由的工作原理？参见 [[旁路由原理详解]]，了解网关设置的本质原理。

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
   - 官方固件下载：[fw.koolcenter.com/iStoreOS/](https://fw.koolcenter.com/iStoreOS/)；社区预装插件固件请自行甄别风险（注意：AUK9527/Are-u-ok 仓库只提供插件 `.run` 包，**不提供固件**）
2. **手动安装 IPK 包**
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

> [!warning] 25.12（apk）用户注意
> 上述 `opkg` 源配置方式适用于 24.10 及之前版本。25.12 已切换为 `apk` 包管理器，软件源配置文件位于 `/etc/apk/repositories.d/`，需使用 `apk update` / `apk add` 等命令（opkg→apk 命令对照见 §1 版本说明）。

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

# 4. 安装依赖（透明代理依赖 nftables tproxy 内核模块）
opkg install kmod-nft-tproxy kmod-nft-socket
# 可选：替换为 dnsmasq-full（推荐，兼容性更好；若与 dnsmasq 冲突先移除）
opkg remove dnsmasq && opkg install dnsmasq-full

# 5. 安装 PassWall 或 PassWall2
opkg install luci-app-passwall      # PassWall
opkg install luci-app-passwall2     # PassWall2（推荐）

# 6. 刷新管理界面
/etc/init.d/uhttpd restart

# 7. 安装汉化（可选）
opkg install luci-i18n-passwall-zh-cn
opkg install luci-i18n-passwall2-zh-cn
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

# 2. 安装依赖（透明代理依赖 nftables tproxy 内核模块）
opkg update
opkg install kmod-nft-tproxy kmod-nft-socket
# 可选：替换为 dnsmasq-full（推荐，兼容性更好；若与 dnsmasq 冲突先移除）
opkg remove dnsmasq && opkg install dnsmasq-full

# 3. 下载 IPK 包（版本号格式为 YY.M.DD-N，以 releases 页最新为准）
cd /tmp
wget https://github.com/Openwrt-Passwall/openwrt-passwall2/releases/download/26.8.27-1/luci-app-passwall2_26.8.27-1_all.ipk

# 4. 安装（忽略依赖）
opkg install --force-depends luci-app-passwall2_*.ipk

# 5. 如果提示缺少依赖，逐个安装
opkg install <缺失的依赖包名>
```

**常用 IPK 下载地址**：
- [Passwall2 Releases](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases)
- [kenzok8 Packages](https://github.com/kenzok8/openwrt-packages)

---

#### 完整排查流程

> [!note] 25.12（apk）提示
> 以下脚本中的 `opkg` 命令适用于 24.10；25.12 已改用 `apk` 包管理器（如 `apk update` / `apk search` / `apk info`）。

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
> 1. **系统修复工具** → 2. **检查防火墙类型** → 3. **更新软件包列表** → 4. **iStore 手动安装 `.run` 包（推荐）** → 5. **第三方 opkg 源** → 6. **手动 IPK**

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

- [[软路由教程/软路由教程MOC]] - 软路由教程索引
- [[软路由教程/主流软路由系统对比与选择指南]] - 系统选择指南
- [[PVE的学习/02-虚拟机管理/PVE的网络逻辑讲解]] - PVE网络配置

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

### 插件 `.run` 包 / 安装脚本
- [bcseputetto/Are-u-ok — iStoreOS_24.10 Release](https://github.com/bcseputetto/Are-u-ok/releases/tag/iStoreOS_24.10) - iStoreOS 24.10 的 Passwall/Passwall2/OpenClash 等 `.run` 包（含 x86_64）
- [AUK9527/Are-u-ok](https://github.com/AUK9527/Are-u-ok) - 22.03 的 `.run` 包（主要 aarch64）
- [slobys/openclash-auto-installer](https://github.com/slobys/openclash-auto-installer) - OpenClash 一键安装/更新/卸载脚本

### 故障排查资源
- [iStoreOS GitHub Discussions](https://github.com/istoreos/istoreos/discussions) - 官方讨论区
- [2026年最新PassWall插件更新和安装](https://naiyous.com/10535.html) - 奶油博客
- [2026年最新PassWall插件更新和安装（新版）](https://naiyous.com/10947.html) - 奶油博客
- [iStoreOS下直更新Passwall2](https://shuaiqiang.cc/istoreos%25E4%25B8%258B%25E6%259B%25B4%25E6%2596%25B0passwall2/) - 帅强来了博客
- [科技老王博客：新版Passwall负载均衡](https://kejilaowang.com/openwrt-istoreos-passwall-haproxy-socks/) - 科技老王
- [OpenWrt 第三方软件源配置](https://cxorz.com/blog/openwrt-thirdparty) - Hanasaki 博客
- [kenzok8 软件包仓库](https://github.com/kenzok8/openwrt-packages) - GitHub
- [Passwall2 Releases](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases) - GitHub
- [Passwall Releases](https://github.com/Openwrt-Passwall/openwrt-passwall/releases) - GitHub

### 硬件相关
- [iStoreOS默认IP地址及网络配置管理指南](https://comate.baidu.com/zh/page/8zqve692bec) - 百度 Comate
- [最强软路由系统iStoreOS_X86安装体验](https://blog.zwbcc.cn/archives/istoreosx86) - zwbcc博客

---

## 更新记录

### 2026-09-01

- **新增 §3.1.3 软件源切换**：补充 iStoreOS 换源方法（GUI「软件源配置」卡片 + 命令行 sed 替换）与已验证的国内镜像（阿里云/清华 TUNA/中科大 USTC/南大兰大）；标注 kenzok8 `op.supes.top` opkg 源已失效（2026-09 实测重定向到 dl.openwrt.ai 返回 404），改为走 GitHub Releases 手动下 IPK；补充旁路由联网、架构匹配、25.12 apk 路径差异、官方修复脚本等注意点。
- **联动**：§3.1.2 方案 C 与 §4.2 方案 A 的软件源提示改为引用 §3.1.3。

### 2026-08-31

- **iStoreOS**：稳定版更新至 24.10.8（2026-07-31）；新增 25.12 测试版说明（基于 OpenWrt 25.12.5，包管理器 opkg→apk，不支持 24.10 保留配置升级）
- **Passwall**：更新至 26.8.11-1；**Passwall2**：更新至 26.8.27-1；明确两者为独立仓库、版本各自推进
- **核心组件**：xray-core 更新至 26.7.28，sing-box 更新至 1.13.19
- **OpenClash**：更新至 v0.47.156（2026-08-10）；调整 v0.47.x 已知问题描述（自启 Bug 升级观察）
- **HomeProxy**：补充版本 v0.0.11 与系统要求（ImmortalWrt / OpenWrt 23.05+，依赖 firewall4、kmod-nft-tproxy，不支持 XHTTP 节点）
- **25.12 迁移提示**：在 Passwall/OpenClash 备选安装方案中补充 apk 包管理器差异说明
- **安装方式修正**：**删除**「通过 iStore 搜索安装」的无效步骤（官方 iStore 商店默认不含 Passwall/OpenClash）；新增方案 C（iStore 手动安装 `.run` 包）作为 iStoreOS 推荐安装方式；备选安装章节重排为 §3.1.2 / §4.2
- **安装方法核实修正（2026-08-31）**：
  - `.run` 包来源修正为 **bcseputetto/Are-u-ok 的 iStoreOS_24.10 Release**（原 AUK9527 主仓库仅维护 22.03 的 aarch64 包），并给出真实文件名示例（PassWall2 26.8.27、OpenClash 0.47.156 均带 `_sdk_24.10` 后缀；OpenClash 为 `+x86_64_core` 内置内核格式）
  - **修正 OpenClash 安装错误**：删除「从 Passwall SourceForge 源 `opkg install luci-app-openclash`」的错误步骤（该源不包含 OpenClash），改为社区一键安装脚本（slobys/openclash-auto-installer，已验证仓库与默认分支）
  - **补充依赖步骤**：Passwall/Passwall2 与 OpenClash 安装前补充 `kmod-nft-tproxy` / `kmod-nft-socket`（24.10 nftables 透明代理）及可选 `dnsmasq-full`；OpenClash 方案 B 依赖更新为 24.10 适用集合（含 `kmod-tun`、`kmod-inet-diag`、`luci-compat`）
  - **方案 A 注意**：标注 `opkg-key` 为 24.10 专用、SourceForge 源不含 OpenClash、存储空间与 SSR-Plus 冲突提示
  - **修正 Q1 方案一固件来源**：AUK9527 仓库不提供固件，仅提供插件 `.run` 包；官方固件下载为 fw.koolcenter.com
- **参考资料**：补充 iStoreOS 24.10.8 更新日志、Passwall（v1）Releases 等来源

### 2026-07-11

- **iStoreOS**：版本更新至 24.10.7（Linux 6.6.141 内核），补充升级冲突提醒
- **Passwall2**：版本号变更为 YY.M.DD-N 格式，更新至 26.6.16-1，仓库迁移至 Openwrt-Passwall 组织；补充 sing-box 1.13+ DNS 配置变更提醒
- **OpenClash**：更新至 v0.47.096-dev，补充 v0.47.x 新特性（界面重构、覆写设置、多订阅合并等）；补充 v0.47.055 开机自启 Bug 提醒
- **HomeProxy**：确认保持活跃更新，补充 Docker 部署方式
- **参考资料**：更新已失效链接，补充新版本下载地址
- **插件对比表**：新增「当前版本」列

---

**最后更新**：2026-08-31
