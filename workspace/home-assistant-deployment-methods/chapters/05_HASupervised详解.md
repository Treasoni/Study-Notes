# 第五章：HA Supervised 详解（含弃用现状）

前两章讲完了官方两条正式路径——HAOS（全托管）与 Container（轻量 Core）。这一章补上第三条：HA Supervised。它曾在完整 Linux 上同时提供 Supervisor 与 Add-on，理论上兼得「全功能」与「宿主控制权」，但官方支持已于 2025.12 终止。这一章回答：它到底是什么、安装器在做什么、为什么被弃用、社区怎么看，以及它是否还有保留价值。

> [!warning] 先记住结论
> HA Supervised 已于 **2025.12 官方支持终止**，本文按「一条弃用中的旧路径」对待：不推荐新用户使用，仅在需要 Add-ons 又要宿主控制权时作过渡。读本章的目的是理解原理与迁移，而不是获得推荐。

## 5.1 历史定位与 ADR-0014（已 revert）

**定义**：Supervised = 在你自己管理的 Linux 上，用安装器部署 Supervisor + Core，从而获得「完整 HA 组件（除 HAOS 之外）」[素材 §一.3]。它保留了宿主 OS 的控制权——apt、systemd、自定义服务都可以继续用——同时拥有 HAOS 才有的 Supervisor 与 Add-on 商店。正因如此，历史上官方定位是 **「only for advanced users」**，要求精通 Linux / Docker / 网络，维护难度列为 Expert [素材 §一.3]。

**ADR-0014 与 revert**：Supervised 的官方支持曾由一份架构决策记录（ADR）正式定义，编号 ADR-0014。但该 ADR 状态已标记 **reverted（已撤销）**，官方不再承认 Supervised 是受支持的安装方式 [素材 §一.3]。网上大量 Supervised 教程写于 ADR 有效期内，内容基于这份已撤销的正式支持——阅读这类教程前，先给它打个问号。

官方定位的演进脉络：

| 阶段 | 官方态度 |
|------|---------|
| ADR-0014 有效期 | 正式支持；「only for advanced users」 |
| ADR-0014 revert 后 | 不再列为正式安装方式 |
| 2025-05-22 起 | 公告弃用，进入倒计时 |
| 2025.12 起 | 官方支持终止 |

> [!warning] 过时教程警告
> 2025 年后仍宣称 Supervised「官方支持」的教程，基本都基于已 revert 的 ADR-0014 或更早材料。先核实发布日期，再决定是否采信。

## 5.2 官方支持约束（历史定义）

Supervised 的「全功能」代价，是一长串对宿主系统的硬性要求。这些约束是官方支持的前提条件（即 ADR 有效期内，满足才算「受支持」）；如今虽然已弃用，理解它们仍是判断「自己装不装得起来」的关键。

### 宿主 OS：仅 Debian 12，无衍生版

官方唯一支持的宿主操作系统是 **Debian 12 Bookworm**，且**不接受任何衍生版**——Raspberry Pi OS、Ubuntu 等都会被安装器直接拦截 [素材 §一.3]。注意这是硬性检查，不是「强烈建议」：树莓派用户想跑 Supervised，必须先刷纯 Debian 12，而不是常见的 Raspberry Pi OS，否则安装器第一步就过不去。

### 依赖清单

| 依赖 | 最低版本 |
|------|---------|
| Docker CE | ≥ 20.10.17 |
| systemd | ≥ 239 |
| NetworkManager | ≥ 1.14.6 |
| udisks2 | ≥ 2.8 |
| AppArmor | 内核启用 |
| cgroup | v1 |
| 文件系统 | overlayfs2 |
| journald | systemd 自带 |

这张表本质上是「Supervisor 在宿主上运行的运行时环境」：Docker 提供容器、systemd 管理服务、NetworkManager 处理网络（HA 的网络管理依赖它）、udisks2 负责磁盘与 USB 存储、AppArmor 做容器安全、cgroup v1 是 Supervisor 容器资源控制的必需版本、overlayfs2 是 Docker 存储驱动。

### 宿主必须「专用于 HA」

比依赖清单更苛刻的是一条隐含约束：**宿主必须专用于 HA，不得安装额外软件**。因为几乎任何对系统状态的改动，都可能让 Supervised 的自检从 Healthy 变成 Unsupported / Unhealthy [素材 §一.3]。这带来一个反直觉的结论：Supervised 虽然跑在你的 Linux 上，但你想在它旁边装别的服务，恰恰是最容易触发 Unsupported 的行为之一。

## 5.3 安装原理与脚本步骤

官方曾维护安装脚本仓库 `supervised-installer`，负责把一套 Debian 12 系统变成 Supervised 宿主。安装分四步 [素材 §一.3]：

```bash
# 1. 安装 network-manager + systemd-resolved
#    注意：这一步会切换网络服务，宿主的 IP 可能变化
apt install network-manager systemd-resolved

# 2. 安装 curl、udisks2，并安装 Docker CE
apt install curl udisks2
curl -fsSL get.docker.com | sh

# 3. 安装 OS-Agent（Supervisor 与宿主通信的守护进程）
#    从 GitHub releases 下载 os-agent_*_linux_*.deb
dpkg -i os-agent_*_linux_*.deb

# 4. 下载并安装 homeassistant-supervised.deb（核心包）
#    装完即部署 Supervisor + Core，并注册为 systemd 服务
dpkg -i homeassistant-supervised.deb
```

四步各司其职：

| 步骤 | 装了什么 | 为什么需要 |
|------|---------|-----------|
| 1 | network-manager + systemd-resolved | Supervisor 接管网络配置，两者必须存在；切换服务时 IP 可能变化 |
| 2 | curl、udisks2、Docker CE | Docker 是 Supervisor 的容器运行时；udisks2 负责磁盘 / USB 管理 |
| 3 | OS-Agent | 宿主机与 Supervisor 之间通信的守护进程，负责上报系统状态 |
| 4 | homeassistant-supervised.deb | 主安装包，部署 Supervisor + Core 并注册为 systemd 服务 |

两个补充细节：

- **数据目录**：默认 `/var/lib/homeassistant`，可用环境变量 `DATA_SHARE` 自定义 [素材 §一.3]。
- **支持机型**：列表有限——generic-x86-64、qemux86-64、qemuarm-64、odroid-c2 / c4 / n2、khadas-vim3、raspberrypi3-64 / 4-64 / 5-64 等 [素材 §一.3]。注意树莓派条目只认 64 位，且必须跑纯 Debian。

> [!warning] 弃用后的安装器
> `supervised-installer` 仓库顶部已标注「unsupported with HA OS 2025.12.0」——即该安装器对 2025.12 之后的 HA 版本不再提供支持 [素材 §二]。照抄上面命令之前，先确认你接受「无人维护」的现实。

## 5.4 弃用时间线与现状

官方对 Supervised（连同 Core、32 位系统）的弃用，有一条清晰的时间线 [素材 §二]：

| 时间 | 事件 |
|------|------|
| 2025-05-22 | 官方公告弃用 Core、Supervised 安装方式及 32 位系统 |
| 2025.6 版本起 | 受影响系统更新后显示「支持将在六个月后结束」通知 |
| 2025.12 版本 | **官方支持终止**；supervised-installer 同步标注 unsupported |

弃用之后，Supervised 仍可继续使用和更新，但官方不再接受问题报告、并移除了端用户文档。换句话说：用下去没人拦你，但出了 bug 官方不会管，连官方排障指南都没了。

官方公告里用使用率数据解释了清理动因 [素材 §二]：

| 安装方式 | 使用率 |
|---------|--------|
| Core | 约 2.5% |
| Supervised | 约 3.3% |
| i386 / armhf | < 0.5% |
| armv7 | 约 0.95%（其中过半实际支持 64 位） |

Supervised 约 3.3% 的使用率，叠加宿主约束带来的高维护成本，让官方认为不值得持续投入维护资源。

## 5.5 社区立场与 BYPASS_OS_CHECK 风险

### 社区共识：「less supported (and liked)」

早在弃用之前，社区对 Supervised 的评价就是 **「less supported (and liked)」**——处于受支持边缘地带，选它等于自负维护责任 [素材 §二]。弃用公告之后这个立场更明确：多数老用户的实际选择是「Proxmox 上跑 HAOS VM，杂项服务用独立 LXC/VM 跑，不塞进 HA」[素材 §二]。社区并不是讨厌 Supervised 的功能，而是厌倦了它与宿主系统之间脆弱的耦合。

### BYPASS_OS_CHECK：社区流传，官方不背书

Supervised 的安装器会做宿主 OS 检查（非 Debian 12 / 衍生版直接拦截）。社区流传一种绕过方式：设置环境变量 **BYPASS_OS_CHECK**，跳过检查把包强装上去。关于它，必须把话说清楚：

> [!warning] 不要臆造细节，也不要指望官方兜底
> BYPASS_OS_CHECK 的记载主要来自社区指南，**官方文档不背书、不保证、不负责** [素材 §五]。目前能确认的事实只有两点：一是这个变量确实被社区多次提及；二是即使绕过成功，系统也几乎必然被判 Unsupported / Unhealthy，官方支持随之失效。至于它在某个具体版本怎么生效、会不会被新版本移除，**没有官方口径**——任何声称「详细教程」的帖子都应视为社区经验，需自行验证。

换句话说：BYPASS_OS_CHECK 不是「解锁官方支持的钥匙」，恰恰相反，它是「主动放弃官方支持」的按钮。

## 5.6 优点 / 缺点 / 适用场景

| 维度 | 结论 |
|------|------|
| 优点 | 兼具 Add-on 商店与宿主 OS 控制权；Thread / Z-Wave 可用（由 Add-on 提供） |
| 缺点 | 安装繁琐；维护成本高（Expert）；易被判 Unsupported / Unhealthy；仅支持纯 Debian 12；已弃用（2025.12 终止） |
| 适用 | 基本不推荐新用户；仅在需要 Add-ons 又要宿主控制权时作过渡 |

理论上，Supervised 是「功能完整性」与「灵活性」两条权衡轴上的理想折中：它有 HAOS 的 Supervisor / Add-on / Thread / Z-Wave，又有 Container 那样的宿主控制权。但它的成立前提——宿主必须专用于 HA、仅支持纯 Debian、任何改动都可能触发 Unsupported——让这个折中名存实亡：真把宿主「专用」了，与独占一台 HAOS 没有本质区别；真在共享宿主上跑，又必然触碰 Unsupported 红线 [素材 §三]。

> [!tip] 一句话判断
> 需要 Add-on 生态，选 HAOS（第三章）；需要宿主控制权且愿意手动维护，选 Container（第四章）。Supervised 夹在中间两头都想要，却两头都难做好——而且已经失去官方支持。

## 本章小结

- Supervised = 在完整 Linux 上装 Supervisor + Core；曾由 ADR-0014 定义官方支持，现已 revert。
- 官方约束极严：仅纯 Debian 12、依赖清单长、宿主必须专用，否则易被判 Unsupported / Unhealthy。
- 安装器四步：network-manager + systemd-resolved → Docker CE / curl / udisks2 → OS-Agent → dpkg -i homeassistant-supervised.deb。
- 弃用时间线：2025-05-22 公告 → 2025.6 六个月倒计时通知 → 2025.12 官方支持终止；使用率仅约 3.3%。
- BYPASS_OS_CHECK 是社区流传、官方不背书的绕过手段，强装必然 Unsupported，不构成推荐理由。

## 下一章预告

第六章把三种部署方式浓缩成一张选型决策树：按你的硬件条件与维护偏好一步步走到推荐答案，并给出官方不推荐的组合清单。
