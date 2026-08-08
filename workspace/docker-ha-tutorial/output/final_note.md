---
title: "Docker 部署 Home Assistant 完全指南：HACS、国内稳定运行与 Addon 实战"
tags:
  - Home-Assistant
  - Docker
  - HACS
  - 智能家居
  - 运维
  - 实战教程
created: 2026-08-08
updated: 2026-08-08
status: 已完成
source_project: docker-ha-tutorial
---

# Docker 部署 Home Assistant 完全指南：HACS、国内稳定运行与 Addon 实战

> 本篇实战笔记把 Home Assistant 的 Docker Container 路线完整走通：从认清三种部署方式的定位，到用 `docker run` / `docker-compose` 把 HA 跑起来；从安装 HACS 补足社区生态，到锁版本、备份、回滚建立稳定运维闭环；最后用 Docker 把 addon 一个一个「装」回来。全程以国内网络为硬约束，镜像拉取、HACS 下载与更新策略都给出了可落地的加速方案。

## 目录

1. [[#第一章：为什么是 Docker 版 —— 部署架构与能力边界]]
   - [[#三种部署方式：先看清地图再上路]]
   - [[#Supervised 已弃用（2025），新装别选它]]
   - [[#Container 版能力边界：缺什么，补什么]]
   - [[#全文主线：一份 compose 贯穿始终]]
2. [[#第二章：快速起跑 —— docker run 部署与 config 目录结构]]
   - [[#一、动手前：先过三项前置条件]]
   - [[#二、官方 docker run 命令与逐参数拆解]]
   - [[#三、/config 目录：首次启动的自动生成机制]]
   - [[#四、启动验证]]
3. [[#第三章：工程化部署 —— docker-compose 完整配置与三大关键决策]]
   - [[#3.1 一份可直接抄的官方 compose.yaml]]
   - [[#3.2 决策一：网络模式 host vs bridge]]
   - [[#3.3 决策二：设备直通]]
   - [[#3.4 决策三：国内镜像加速——ghcr 前缀替换]]
4. [[#第四章：HACS 安装 —— Docker 三种路径与国内加速]]
   - [[#4.1 HACS 是什么，为什么 Docker 版要手动装]]
   - [[#4.2 官方脚本 get.hacs.xyz 在做什么]]
   - [[#4.3 Docker 三种安装路径]]
   - [[#4.4 国内加速：下载可以加速，授权必须直连]]
5. [[#第五章：HACS 首次配置与常用仓库实战]]
   - [[#5.1 先确认 HACS 真的加载了]]
   - [[#5.2 HACS 3.x 首次配置完整流程]]
   - [[#5.3 国内「两段论」：下载可加速，授权必须直连]]
   - [[#5.4 高频报错定位]]
   - [[#5.5 常用仓库清单]]
6. [[#第六章：国内稳定运行 —— 版本锁定与镜像加速策略]]
   - [[#一、`stable` 是浮动标签：今天能用，明天未必]]
   - [[#二、锁版本：固定 tag 的生产写法]]
   - [[#三、双镜像源：ghcr 前缀替换]]
7. [[#第七章：更新、回滚与备份 —— 运维三件套]]
   - [[#7.1 升级前校验：先给 HACS 和自定义组件打补丁]]
   - [[#7.2 升级：Docker 侧的两行命令]]
   - [[#7.3 回滚：留好旧发动机，随时换回来]]
   - [[#7.4 数据库 schema 风险：升级前必须备份的根本原因]]
   - [[#7.5 备份：先关门，再收拾房间]]
   - [[#7.6 恢复：把备份解包还原到 /config]]
   - [[#7.7 补：2026 年升级兼容风险案例与降险清单]]
8. [[#第八章：Docker 部署 addon —— 把 Docker Hub 变成你的 Addon Store]]
   - [[#8.1 为什么 Docker 版没有「Addon Store」]]
   - [[#8.2 替代思路：整个 Docker Hub 就是你的 Addon Store]]
   - [[#8.3 官方 / 社区 addon 镜像：命名规则与拉取]]
   - [[#8.4 国内替换映射：一条前缀对照表]]
   - [[#8.5 常见 addon 的完整 compose：五个服务逐段拆解]]
   - [[#8.6 mosquitto.conf：MQTT 的「广播室规则」]]
9. [[#第九章：addon 与 HA 通信、网络架构与权限避坑]]
   - [[#一、先认钥匙：LLT + Base URL 是 Docker 版的通信方式]]
   - [[#二、Node-RED 接入 HA：勾掉 addon 选项，填 LLT]]
   - [[#三、hass-cli 与 ha：访客钥匙 vs 管家钥匙]]
   - [[#四、推荐网络架构：HA 用 host 保发现，服务用 bridge 保整洁]]
   - [[#五、权限与互斥避坑清单]]
   - [[#总结：从零到一套完整 HA 体系的回顾与进阶]]

---

## 第一章：为什么是 Docker 版 —— 部署架构与能力边界

在动手之前，先回答一个最关键的问题：**同样是 Home Assistant，为什么选 Docker Container 版？** 很多读者是从 HAOS 入门的，习惯了界面里点一点就装好的 Add-on 商店，换到 Docker 版后会猛然发现「怎么啥都没有」。本章帮你认清 Docker 版在三种部署方式中的定位与能力边界，建立「缺什么、补什么」的全局观——这是后面 8 章所有操作的前提。

### 三种部署方式：先看清地图再上路

Home Assistant 官方截至 2026 年只正式支持两种安装方式：**HAOS**（推荐大多数用户）与 **HA Container**（已有 Docker 环境的熟练用户）；Supervised 方式已弃用[^official-install]。三者对比如下：

| 对比维度 | HAOS | Supervised | HA Container |
|---------|------|-----------|--------------|
| 本质 | 专用操作系统，含 HA 内核 | 在 Debian 系 Linux 上装 Supervisor + HA | 只跑 HA 核心的 Docker 容器 |
| Add-on Store | ✅ 自带 | ✅ 有 | ❌ 无 |
| ha CLI | ✅ | ✅ | ❌ |
| 内置备份 | ✅ | ✅ | ❌ |
| 更新/回滚 | 界面操作 | 界面操作 | Docker 侧自管 |
| 官方支持状态 | ✅ 官方推荐 | ⚠️ 2025 起弃用 | ✅ 官方支持 |
| 适合人群 | 多数用户、专用硬件 | 不建议新装 | 已有 Docker 环境的熟练用户 |

官方推荐逻辑很直白：**能装 HAOS 就装 HAOS**，它把全家桶都替你管好；只有当你已经有一个跑着 Docker 的服务器、不想为 HA 单独占一台机器时，才走 Container 路线[^official-install]。本教程就是这条「已有 Docker 环境」的路。

> [!tip] 大白话
> 把 Supervisor 想成 **容器「管家」**：它负责自动安装、卸载、管理一个个 addon 容器，还顺手提供 ha CLI 和内置备份。HAOS 和 Supervised 自带管家；Docker Container 版没有管家——**你自己当管家**。

### Supervised 已弃用（2025），新装别选它

Supervised 曾经是「既有 Linux 又想用 Add-on Store」的折中方案，但官方 2025 年起将其弃用。它的硬伤在于要求对宿主机的完全控制：你一旦在宿主机上跑 Portainer、Watchtower 这类常用运维工具，HA 就会把系统标记为 **Unsupported/Unhealthy**，官方也不再兜底[^research-a1]。所以新部署不要选这条路——要么 HAOS，要么 Docker Container。

### Container 版能力边界：缺什么，补什么

Docker Container 版的本质是**无 Supervisor 的单容器**，能力边界可以一句话概括[^research-synthesis]：

- **无 Add-on Store**：官方 addon 设计为专与 Supervisor 配合，Container 版没有「应用商店」；
- **无 ha CLI**：`hassio-cli` / `ha` 这类走 Supervisor API 的命令全部不可用；
- **无内置备份**：没有一键备份/恢复按钮，备份要自己 `tar`。

但「缺失」不等于「做不到」。addon 本质就是容器镜像，官方文档原文明确说「addon 底层就是发布到容器仓库的应用镜像」[^official-addon]，所以 **整个 Docker Hub 就是你的 Add-on Store**——只是从「商店自动安装」变成「自己 `docker compose up`」；备份也有标准命令序列。这正是本教程第 7、8、9 章要补的课。

> [!tip] 大白话
> addon = 一个**预装好软件的容器**。HAOS 的「Add-on Store」就是管家替你把容器拉下来、配置好、再启动；Docker 版没了这个商店，你手动 `docker compose up` 就是「手动安装 App」。HACS 装的是集成和前端卡片，不是容器，两者不冲突、也不能互相替代。

### 全文主线：一份 compose 贯穿始终

认清定位后，本教程的路线已经清晰，后续 8 章围绕「缺什么、补什么」展开，并始终围绕**一份可直接上线的 docker-compose.yml** 这条主线：

1. **部署**（第 2–3 章）：先用 `docker run` 快速起跑，再升级为工程化 compose；
2. **HACS**（第 4–5 章）：Docker 三种安装路径 + 国内加速 + 首次授权；
3. **稳定运维**（第 6–7 章）：锁版本、镜像加速、更新、回滚、备份三件套；
4. **addon 补足**（第 8–9 章）：把 Docker Hub 当 Add-on Store，打通通信与权限。

### 本章小结

- 官方只正式支持 HAOS 与 HA Container 两种方式；Supervised 已弃用（2025），新装不要选。
- Container 版的能力边界 = 无 Supervisor：无 Add-on Store、无 ha CLI、无内置备份，全部自管。
- 「缺失」不等于「做不到」：addon 本质是容器镜像，整个 Docker Hub 就是你的 Add-on Store。
- Docker 版没有「管家」，你得自己负责更新、备份、伴生服务——这正是本教程的实战主线。
- 记住这份地图：**部署 → HACS → 稳定运维 → addon**，接下来每一步都会回到这条主线上。

### 下一章预告

地图看完了，下一章立刻动手：用官方 `docker run` 命令在几分钟内拉起你的第一个 HA 容器，搞懂 `/config` 目录和首次启动机制，为升级成 compose 打底。

[^official-install]: [Home Assistant Installation](https://www.home-assistant.io/installation/)
[^official-addon]: [Home Assistant Developer Docs: Add-ons](https://developers.home-assistant.io/docs/add-ons/)
[^research-a1]: 深度素材方向 A1「官方推荐部署方式（截至 2026）」：Supervised 弃用、跑 Portainer/Watchtower 会被标 Unsupported/Unhealthy。
[^research-synthesis]: 深度素材综合分析「关键共识」：Docker Container 版 = 无 Supervisor 的单容器，无 Add-on Store、ha CLI、内置备份，伴生服务用独立容器自管。

---

## 第二章：快速起跑 —— docker run 部署与 config 目录结构

第一章我们确认了 Docker 版 HA 没有 Supervisor，Addon Store 和内置备份都得自己补。但「自己补」的前提是先让 HA 跑起来——本章就用官方一条 `docker run` 命令在几分钟内拉起一个能用的 HA，并借着首次启动把 `/config` 目录的自动生成机制和 `.storage` 持久化看清，为第三章升级成 compose 编排打底。

### 一、动手前：先过三项前置条件

1. **Docker Engine ≥ 23.0.0**。先跑 `docker version`，确认 Server 端版本号不小于 23 即可。
2. **仅限 Linux**。Docker Desktop（macOS / Windows 的 Docker 桌面版）不可用。HA 容器需要 host 网络与完整设备访问，Docker Desktop 跑在虚拟机层上给不了这些。
3. **防火墙放行 8123 端口**。HA 的 Web 界面默认监听 TCP 8123。Ubuntu 上用 ufw 放行：

```bash
sudo ufw allow 8123/tcp
```

> [!tip] 大白话：为什么 Docker Desktop 不行
> 把 Docker Desktop 想成「装在盒子里的 Docker」——盒子里的网络和 USB 都是模拟出来的。HA 要的局域网设备发现（组播）和设备直通，盒子都给不了；所以官方只支持 Linux 裸机，别在 Windows / macOS 上硬试。

### 二、官方 docker run 命令与逐参数拆解

官方推荐的 Docker 版安装命令就这一条，直接复制、把 `/PATH_TO_YOUR_CONFIG` 换成你的配置目录（例如 `/home/pi/ha-config`）即可（[HA 官方 Linux 安装文档](https://www.home-assistant.io/installation/linux)）：

```bash
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /PATH_TO_YOUR_CONFIG:/config \
  -v /run/dbus:/run/dbus:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

逐个参数看它做了什么：

| 参数 | 作用 | 一句话白话 |
|------|------|-----------|
| `-d` | detached，容器后台运行，不占终端 | 把 App 放后台跑，别挡着终端 |
| `--name homeassistant` | 给容器命名，后续 `docker logs/exec/restart` 都用它 | 给容器起个名字，找人好找 |
| `--privileged` | 特权模式，放开设备与内核访问权限 | 万能钥匙，第三章会教更克制的替代 |
| `--restart=unless-stopped` | 崩溃 / 宿主重启后自动拉起容器 | 不辞退的保安，除非你手动停工 |
| `-e TZ=Asia/Shanghai` | 设置时区环境变量 | 告诉 HA 现在是哪个时区 |
| `-v /PATH_TO_YOUR_CONFIG:/config` | 把宿主机目录挂载成容器内 `/config` | 给容器开一扇直通你家仓库的门 |
| `-v /run/dbus:/run/dbus:ro` | 只读挂载宿主 dbus，蓝牙集成必需（可选但常用） | 接蓝牙的「接线板」 |
| `--network=host` | host 网络模式，容器直接用宿主机网络栈 | 让容器直接「住进」宿主机网络 |
| `ghcr.io/.../home-assistant:stable` | 镜像地址（ghcr.io = GitHub 容器仓库，stable = 浮动标签） | 从哪个货仓取货 |

两个最容易踩的细节：

**TZ 是时区「姓名」，不是 UTC 偏移。** `TZ=Asia/Shanghai` 这种 tz database 名称才是对的；写成 `TZ=UTC+8` 这种偏移量是错的，HA 不会按你预期走（[HA 官方安装文档 TZ 说明](https://www.home-assistant.io/installation/linux)）。

> [!tip] 大白话：TZ 时区
> 把 `TZ` 想成「报时方式」。`Asia/Shanghai` 是告诉 HA「你在上海」，它自己处理冬夏令时；`UTC+8` 是告诉它「你现在比 UTC 快 8 小时」，一旦遇到实行夏令时的地区就会错位。所以报「地名」，别报「偏移」。

**`--network=host` 下没有端口映射。** host 模式下容器直接共享宿主网络栈，所以不需要（也不会有）`-p 8123:8123` 这种映射——访问 `http://<宿主机IP>:8123` 就是直达 HA。

### 三、/config 目录：首次启动的自动生成机制

#### 空目录才「精装修」

`-v` 挂载的宿主机目录会以 `/config` 出现在容器里，**HA 的全部配置都住在这里**。首次启动时，如果这个目录**完全为空**，HA 会自动生成一份默认 `configuration.yaml`（[HA 官方目录结构说明](https://www.home-assistant.io/installation/linux)）：

```yaml
# Loads default set of integrations. Do not remove.
default_config:
frontend:
  themes: !include_dir_merge_named themes/
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

这份文件是 HA 的「总入口」，四行各有分工：

- `default_config:`：一行加载一整批默认集成（frontend、api、discovery、history、logbook 等），日常刚起步完全够用，官方注释说「不要删」。
- `frontend:`：启用前端主题目录，`!include_dir_merge_named themes/` 表示合并加载 `themes/` 文件夹里的所有主题文件。
- `automation / script / scene:`：分别用 `!include` 引用 `automations.yaml`、`scripts.yaml`、`scenes.yaml`。这三类配置在 UI 里编辑时，HA 会写进对应的 yaml 文件。

> [!tip] 大白话：空目录才自动生成
> 把 `/config` 想成「毛坯房」，configuration.yaml 是「标配家具」。只有房子完全空着，装修队才会送家具进来；只要屋里已经有任何东西（哪怕一个 `.gitkeep`），他们就默认你自有安排，绝不送家具。所以想用默认配置，就要让挂载目录「绝对干净」。

三个相关坑：

1. **挂载了非空目录就不会生成。** 常见于宿主机 `mkdir` 后顺手 `touch .gitkeep` 或放进 README——结果首次启动没生成配置，HA 进 safe mode 或行为异常。确认目录是空的再启动。
2. **`!include` 引用的文件不存在会进 safe mode。** 默认配置引用的 yaml 文件如果缺失，HA 启动会报错并进入安全模式（界面右上角有提示）。正常首次生成后这些文件会随 UI 操作自动创建；手动删掉它们就会踩这个坑。
3. **UI 里改的设置不写 configuration.yaml。** 集成、设备、实体、自动化，这些在界面里配置的东西实际存在**隐藏的 `.storage/` 目录**里，不在 `configuration.yaml`。

#### .storage：藏起来的另一半数据

`.storage/` 是 `/config` 下的隐藏目录（名字以点开头），里面是一堆 JSON 文件，存着 UI 里配置的集成、设备、实体、云连接等。它和 `configuration.yaml` 一样**必须持久化**——因为挂载是把整个宿主机目录映射给 `/config`，所以 `.storage` 天然跟着目录一起落盘，只要别把挂载点拆散或删掉它就行。这也意味着：**备份时备份整个 `/config` 目录（含隐藏文件）**，而不是只拷 `configuration.yaml`。

> [!tip] 大白话：.storage
> 把 `/config` 想成一栋房子：`configuration.yaml` 是门口的「装修图纸」（手工改的配置），`.storage/` 是客厅后面那个**上锁的小房间**（UI 上点的设置都自动锁在里面）。你不用进去收拾，但搬家（备份）时整个房子都要搬走，漏了这个房间，你之前配好的集成全没了。

### 四、启动验证

命令敲下去之后，用三步确认它真的活了：

```bash
# 1. 看容器状态：STATUS 应为 Up，否则说明启动失败
docker ps

# 2. 看启动日志：出现一连串 "Setup of ... took" 初始化记录即正常
docker logs --tail=200 homeassistant

# 3. 浏览器打开 http://<宿主机IP>:8123，看到创建账户 / 登录页即成功
```

第一次启动要拉镜像 + 初始化集成，通常会等 1-3 分钟（视网络）。`docker logs` 是最常用的排障入口：看到红色 `ERROR` 或提示 safe mode 时，优先回头检查挂载目录是否为空、`!include` 引用的文件是否都在。

> [!tip] 大白话：docker logs
> `docker logs --tail=200` 就是看容器的「运行日志后 200 行」，相当于 HA 的「黑匣子」。起不来时先看它，别瞎猜。

### 本章小结

- Docker 版 HA 的前置就三项：Engine ≥ 23、Linux 裸机、防火墙放行 8123。
- 官方 `docker run` 一条命令即可拉起 HA；`--network=host` 下无需端口映射，访问 `http://<宿主IP>:8123`。
- `TZ` 要写 tz database 名称（`Asia/Shanghai`），不要写 UTC 偏移。
- `/config` 只在**完全为空**时才自动生成默认 `configuration.yaml`；`!include` 引用文件缺失会让 HA 进 safe mode。
- UI 配置存在隐藏的 `.storage/`，与 `configuration.yaml` 一起落盘，备份要备份整个 `/config`。

下一章，我们会把这串 `docker run` 参数搬进一份工程化的 `docker-compose.yml`，并解决「跑起来」之后真正决定体验的三个问题：网络模式怎么选、设备怎么直通、国内镜像怎么拉。跑起来只是第一步，「稳定好用」才是目标。

---

## 第三章：工程化部署 —— docker-compose 完整配置与三大关键决策

上一章我们用手敲的 `docker run` 把 HA「裸奔」拉了起来：一条长命令里塞满镜像、挂载、网络、时区参数，写错一处或想复现，只能翻 shell 历史。这一章把它升级为一份声明式的 `docker-compose.yml`——版本可控、参数可注释、随时可复现——同时把上线前最容易被坑的三个决策讲透：网络模式、设备直通、国内镜像。

> [!tip] 大白话
> `docker run` 像口头交代一件事，说完就忘；`docker-compose` 像把流程写成 SOP 手册，任何人照着执行都能得到一样的结果。所以「工程化」的第一步，就是把运行参数从命令行搬进 yaml 文件。

### 3.1 一份可直接抄的官方 compose.yaml

官方为 Container 部署提供的 compose.yaml 非常精简，我们逐段加注释展开（素材方向 A3）。

```yaml
services:
  homeassistant:                                  # 服务名
    container_name: homeassistant                 # 固定容器名，便于 docker exec / docker logs
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /PATH_TO_YOUR_CONFIG:/config              # 配置目录映射到 /config（第二章已讲过）
      - /etc/localtime:/etc/localtime:ro          # 只读挂载宿主时区，容器内时间与宿主机一致
      - /run/dbus:/run/dbus:ro                    # 蓝牙集成必需（见 3.4）
    restart: unless-stopped                       # 异常退出/开机自动拉起；手动 stop 除外
    privileged: true                              # 高权限兜底（见 3.4，能不用就不用）
    network_mode: host                            # 决策一：直接用宿主网络，见 3.2
    environment:
      TZ: Asia/Shanghai                           # 必须是 tz database 名，不能用 UTC+8
```

几个值得停下来看的点：

- **`network_mode: host`** 是全文最关键的一行，也是本章决策一的主角。
- **`privileged: true`** 官方示例默认带上，但它是一把「万能钥匙」，3.4 会讲如何用更精确的设备映射替代它。
- **`TZ: Asia/Shanghai`** 必须是时区数据库名称（tz database），第二章强调过，写成 `UTC+8` 或 `+8:00` 都无效。
- **镜像 tag 用了 `stable`**。这是浮动标签，生产上建议锁版本；第六章专门讲版本锁定，这里先保持官方默认写法。

### 3.2 决策一：网络模式 host vs bridge

Compose 默认会给容器建一个私有 bridge 网络：容器通过 NAT 访问外网，宿主通过「端口映射」把容器端口暴露出来。这套默认方案对 HA 是致命的。

> [!tip] 大白话
> 把网络想成一座小区。bridge 模式 = 容器住在独立公寓楼，楼下有门禁（NAT），外界想找你必须「转发」（端口映射）；host 模式 = 容器直接住进宿主家，共用宿主的门牌号，没有门禁。关键区别在广播：智能家居设备靠「小区广播」找人——mDNS、SSDP 这类组播协议就是小区广播。广播只在同一栋楼（同一内网）传得开，门禁（NAT）会把广播挡在门外。所以 host = 住进宿主网络，组播必须与设备同内网才能收到。

HA 的本地发现能力几乎全部依赖组播：Chromecast、HomeKit、DLNA、ESPHome、各类局域网设备自动发现。bridge/NAT 不转发组播，这些功能会全部失效（素材方向 A4）。而 host 模式下容器与宿主共享网络栈，组播、广播畅通无阻，`http://<宿主IP>:8123` 直达，无需任何端口映射。这也是官方 Docker 版推荐 host 的根本原因。

如果因为某些原因必须用 bridge（比如一台机器跑很多容器、想用 compose 网络内服务名互访），有几种补法，但都不完美：

| 方案 | 做法 | 代价 |
|------|------|------|
| macvlan | 给容器分配独立局域网 IP，绕过 NAT | 配置复杂，宿主访问容器要走特殊路由 |
| Avahi reflector | 在路由器/宿主上做 mDNS 反射 | 需额外容器或路由器支持，UDP 5353 要放行 |
| ESPHome 专用开关 | 集成里开 `status_use_ping: true` | 只救 ESPHome 一家，救不了 Chromecast/HomeKit |

结论：**除非有明确的架构理由，Docker 版 HA 就用 `network_mode: host`**。这也是第八章设计 addon 网络架构时的前提。

### 3.3 决策二：设备直通

HA 要接 Zigbee 网关、Z-Wave 棒、ESPHome 烧录器，本质上是让容器访问宿主机的 USB 串口设备。

#### 用 by-id 稳定路径，别用 ttyUSB0

USB 设备的枚举名（`/dev/ttyUSB0`、`/dev/ttyACM0`）按插入顺序分配，重启机器或换个 USB 口就可能漂移——你以为插的是同一个设备，路径却悄悄变了。Linux 为每个 USB 串口在 `/dev/serial/by-id/` 下建立了按厂商序列号命名的稳定链接，用 `ls -l /dev/serial/by-id/` 查看，输出形如 `usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB0`——左侧是稳定名，右侧是它当前对应的临时设备。

> [!tip] 大白话
> `/dev/ttyUSB0` 像「按入住顺序排」的临时门牌——隔壁搬走了，你家的号就变了；`/dev/serial/by-id/` 像身份证号——设备是谁就是谁，换楼（换 USB 口）也不变。所以 compose 里永远写身份证号，不写临时门牌。

设备映射片段（素材方向 A5）：

```yaml
services:
  homeassistant:
    devices:
      - /dev/serial/by-id/usb-XXXX:/dev/ttyACM0   # 宿主稳定路径:容器内路径
    group_add:
      - dialout
      - uucp
```

- `devices:` 把宿主设备精确映射进容器，右侧是容器内看到的路径（可自定义）。
- `group_add:` 把容器加入宿主串口设备组。宿主机上把运行 Docker 的用户加进 `dialout`/`uucp` 组，是让容器读写串口最干净的方式。
- `privileged: true` 在这时只是「兜底」——它能绕过几乎一切权限问题，但也给了容器访问宿主全部设备的能力。安全原则：能精确映射，就不上万能钥匙。

#### 蓝牙（hci0）走 dbus，不走 by-id

蓝牙适配器（hci0）不是串口设备，`/dev/serial/by-id/` 里根本没有它。蓝牙集成需要容器通过宿主机的 D-Bus 系统总线去驱动蓝牙栈，所以 compose 里那行 `/run/dbus:/run/dbus:ro` 不是摆设。另外还需先在宿主机上让蓝牙上线：`bluetoothctl power on`（确保适配器已开启，再启动容器）。

### 3.4 决策三：国内镜像加速——ghcr 前缀替换

`ghcr.io` 是 GitHub 的容器仓库，HA 官方镜像就存在这里。国内拉取最常踩的坑，就是给 Docker 配了加速器却依然拉不动。

#### 为什么 registry-mirrors 对 ghcr 无效

Docker 的 `daemon.json` 里 `registry-mirrors` 只拦截 Docker Hub（`docker.io` 和短名镜像）。`ghcr.io` 是另一个 registry 主机名，Docker 只会按字面去连 `ghcr.io`，根本不会路由到你的 Hub 镜像站（素材方向 C3）。

> [!tip] 大白话
> `registry-mirrors` 是给「Docker Hub 这家快递公司」设的中转站；`ghcr.io` 是另一家快递公司，有自己的收货地址。你给 A 公司设了中转站，B 公司的包裹当然不经过它。想让 B 公司的货到得快，得改 B 公司的「收件地址」——也就是把镜像名前缀 `ghcr.io` 换成国内代理域名。

做法是**前缀替换**：把 `ghcr.io/` 换成可用代理的域名，路径其余部分原样保留（素材方向 A6）。

```bash
# 南京大学源：免费、免认证、每日同步（2026 广泛实测可用）
docker pull ghcr.nju.edu.cn/home-assistant/home-assistant:stable
# 毫秒镜像：多来源实测可用
docker pull ghcr.1ms.run/home-assistant/home-assistant:stable
```

在 compose 里同样只是改 `image:` 一行：

```yaml
    image: "ghcr.nju.edu.cn/home-assistant/home-assistant:stable"
```

#### 镜像源易变，配置前先实测

这类国内加速域名随时可能挂掉或换地址，正文给的地址在实操前务必实测。最靠谱的方式是用社区维护的检测项目跑一遍（[docker-registry-cn-mirror-test](https://github.com/docker-practice/docker-registry-cn-mirror-test)），或者直接 `docker pull` 一个小镜像试速度。教程的建议是**主推 + 备选**双源都配好，单个失效时不至于卡死。

### 本章小结

- 把 `docker run` 升级为 `docker-compose.yml`：镜像、挂载、网络、设备全部声明化，一条 `docker compose up -d` 即可复现。
- 网络决策：Docker 版 HA 默认用 `network_mode: host`，保住 mDNS/SSDP/UPnP 组播发现；bridge 会丢本地发现，替代方案（macvlan / Avahi / `status_use_ping`）各有代价。
- 设备决策：串口直通用 `/dev/serial/by-id/` 稳定路径 + `group_add` 加 `dialout`/`uucp` 组；`privileged` 只是兜底。蓝牙走 `/run/dbus`，不在 by-id。
- 镜像决策：`registry-mirrors` 对 `ghcr.io` 无效，要用前缀替换（`ghcr.nju.edu.cn` / `ghcr.1ms.run`）；加速域名易变，先实测再上线。

> [!tip] 大白话
> 这一章浓缩成一句话：HA 要「住进宿主网络、用身份证认设备、给 ghcr 换收件地址」。这三件事做对，容器就能长期稳定跑。

HA 本体已经在 compose 的编排下稳定运行了，但一个没有生态的智能家居中枢还只是空壳。下一章我们安装 HACS，给 HA 搬进「应用商店」，装上前端卡片、社区集成和主题。

---

## 第四章：HACS 安装 —— Docker 三种路径与国内加速

第三章我们用 docker-compose 把 HA 本体稳稳跑起来了。但这时的 HA 还是个「空房子」——没有米家、没有好看的前端卡片、没有丰富的自定义集成。这一章我们装 HACS，把社区生态请进来，并重点解决国内网络下「怎么把 HACS 下载下来」这个现实问题。

### 4.1 HACS 是什么，为什么 Docker 版要手动装

> [!tip] 大白话
> HACS 可以想成「手机应用商店」。HA 官方自带的功能像系统预装 App，而米家、影音卡片、各种主题都是第三方 App——HACS 就是那个让你能发现、下载、更新这些第三方 App 的应用商店。[HACS 官方文档](https://hacs.xyz)

HACS（Home Assistant Community Store）是 HA 社区最重要的生态入口，装三类东西 [方向 B1](02_deep_research.md#1-hacs-是什么--官方脚本做了什么)：集成（integrations，如小米 Miot）、前端卡片（lovelace cards，如 Mushroom）、主题（themes）。Docker 版没有 Supervisor，也就没有「应用商店」的安装器，所以 HACS 需要我们自己动手放进去。

> [!tip] 大白话
> 为什么 Docker 版要手动放文件？想成「从安装包装 App」：HAOS 有应用商店自动下载安装，Docker 版没有商店，你得自己把 App 的安装包（hacs.zip）解压到指定目录，再重启让 HA 加载它。

### 4.2 官方脚本 get.hacs.xyz 在做什么

官方安装脚本的核心是一条命令 `wget -O - https://get.hacs.xyz | bash -`，它一共干 6 件事：

1. 探测含 `.HA_VERSION` 的配置目录（Docker 版就是 `/config`）
2. 检查 `wget` 和 `unzip`，缺一个就报错退出
3. 下载 `github.com/hacs/integration/releases/latest/download/hacs.zip`
4. 解压到 `custom_components/hacs/`（先删旧目录再解压）
5. 比对最低版本要求 `MINIMUM_HA_VERSION`
6. 提示重启 HA

理解这 6 步，就理解三种安装路径为什么可行：脚本的本质 = **找目录 → 下载 zip → 解压到 `custom_components/hacs/`**。只要最终效果一致，用什么方式装都行。

### 4.3 Docker 三种安装路径

Docker 版装 HACS 有 3 条路，区别只在「在哪一步下载、在哪一步解压」[方向 B2](02_deep_research.md#2-docker-三种安装路径)。

#### 路径一：进容器跑官方脚本

最省事，但要容器内有 wget/unzip 且能直连 GitHub：

```bash
# 1. 进容器拿到 shell
docker exec -it homeassistant bash
# 2. 切到配置目录（必须含 .HA_VERSION 才会被脚本识别）
cd /config
# 3. 跑官方脚本（自动探测目录、下载、解压）
wget -O - https://get.hacs.xyz | bash -
# 4. 退出容器并重启 HA
exit
docker restart homeassistant
```

#### 路径二：宿主机解压到挂载目录

脚本依赖容器内工具，但你可以直接在宿主机手动完成同样的事：

```bash
# 1. 进入宿主机上挂载到容器 /config 的目录
cd /path/to/your/config
# 2. 建目录、下载、解压
mkdir -p custom_components/hacs
wget https://github.com/hacs/integration/releases/latest/download/hacs.zip
unzip hacs.zip -d custom_components/hacs && rm hacs.zip
# 3. 重启让 HA 加载
docker restart homeassistant
```

#### 路径三：docker cp + 容器内解压

下载在宿主机做（方便套代理，见 4.4），解压交给容器内工具：

```bash
# 1. 宿主机下载（这里就能拼 gh-proxy 加速前缀）
wget -O /tmp/hacs.zip https://github.com/hacs/integration/releases/latest/download/hacs.zip
# 2. 拷进容器配置目录
docker cp /tmp/hacs.zip homeassistant:/config/custom_components/hacs/
# 3. 进容器解压并清理压缩包
docker exec -it homeassistant sh
cd /config/custom_components/hacs && unzip hacs.zip && rm hacs.zip
exit
# 4. 重启
docker restart homeassistant
```

> [!warning] 关键约束
> 文件必须**直接落在 `custom_components/hacs/` 根目录**，里面直接是 `__init__.py`、`const.py` 这些文件，不能多一层嵌套（比如 `custom_components/hacs/hacs/`）。多套一层 HA 就找不到。放好后一定要 `docker restart homeassistant`，HACS 才会被加载。

三条路径怎么选，看这张表：

| 路径 | 下载在哪做 | 解压在哪做 | 适用场景 |
|------|-----------|-----------|---------|
| 路径一 docker exec | 容器内 | 容器内 | 容器能直连 GitHub 且自带 unzip |
| 路径二 宿主机解压 | 宿主机 | 宿主机 | 挂载目录在宿主机、想少进容器 |
| 路径三 docker cp | 宿主机 | 容器内 | 宿主机下载要配代理，解压交给容器 |

### 4.4 国内加速：下载可以加速，授权必须直连

> [!tip] 大白话
> 国内加速 = 给 GitHub 下载装「加速器」。HACS 从 GitHub 下压缩包、拉仓库列表经常很慢或失败，加速器帮你绕过这段慢路。但它只管「下载」这一步——首次 GitHub 授权（Device flow）要打开浏览器访问 github.com，必须直连，加速器帮不上。

三个加速手段 [方向 B3](02_deep_research.md#3-国内加速方案截至-2026)：

1. **gh-proxy 前缀代理**：在原始 GitHub 地址前拼代理前缀。注意 `ghproxy.com` 已于 2025 年起失效，改用 `gh-proxy.com`、`mirror.ghproxy.com`、`ghfast.top` 等替代。写法是把原 URL 整个拼在代理域名后面，例如 `wget https://gh-proxy.com/https://github.com/hacs/integration/releases/latest/download/hacs.zip`，配合路径二/三使用。
2. **hacs-china 极速版**：把官方脚本域名换成 `get.hacs.vip`，即 `wget -O - https://get.hacs.vip | bash -`，内置 gitmirror/fastgit/ghproxy 多重加速。注意它是第三方 fork（最后发布 2025-08，可用性待实测），且同样只加速下载。
3. **GitHub API 代理**：HACS 3.x 的「选项」UI 里填自定义 API 地址（不是 configuration.yaml），如 `ghapi.hacs.vip/api`、`ghapi-cf.hacs.vip/api`，解决集成列表/版本检查加载失败。

> [!warning] 两个高频坑
> 代理域名（gh-proxy.com、get.hacs.vip 等）可用性易变，实操前先实测再配置。另外小容器常缺 `unzip`（Synology 会报 `'unzip' is not installed`），此时走路径二用宿主机 unzip 更稳；解压后如权限不对，`chown -R 1000:1000 custom_components/hacs` 修正属主 [方向 B6](02_deep_research.md#6-国内高频坑)。

### 本章小结

- HACS = HA 的社区应用商店，装集成 / 前端卡片 / 主题三类扩展
- 官方脚本 = 找 `/config` → 下载 hacs.zip → 解压到 `custom_components/hacs/`
- 三种路径殊途同归：进容器跑脚本 / 宿主机解压 / docker cp，选顺手的一条即可
- 文件必须直接落在 `custom_components/hacs/` 根目录，放完 `docker restart`
- 国内加速只解决「下载」，GitHub 首次授权必须直连

HACS 文件放好了，但还没真正「开通」——第五章我们完成首次配置和 GitHub 授权，再装一批常用的卡片与集成。

---

## 第五章：HACS 首次配置与常用仓库实战

第四章我们成功把 HACS 装进了 Docker 版 HA，重启后它就在后台静静等待。这一章我们把它「唤醒」：走通 HACS 3.x 首次配置全流程，完成 GitHub 授权，装上一批高频使用的卡片和集成，并学会快速定位最常见的报错。

### 5.1 先确认 HACS 真的加载了

重启 HA 后，打开「设置 → 设备与服务」，点右上角「+ 添加集成」，在搜索框输入 `HACS`。能搜到就直接进入 5.2；搜不到，多半是浏览器缓存了旧页面——按 `Ctrl+F5` 强制刷新（Mac 用 `Cmd+Shift+R`）再试一次。[Source: HACS 3.x 首次配置流程](https://www.hacs.xyz/)

> [!tip] 大白话：清缓存
> 把浏览器想成一位「记性太好的前台」。你换了房间号（HACS 装好了），它还按老房间指路。`Ctrl+F5` 就是拍它一下：「忘掉旧记忆，重新看」。所以新装集成后搜不到，先强刷，再排查其他问题。

### 5.2 HACS 3.x 首次配置完整流程

确认能搜到 HACS 后，按下面的顺序走（全程约 5 分钟）：

1. **添加集成**：点「+ 添加集成」→ 搜 `HACS` → 点击进入。
2. **勾选声明**：HACS 会弹出使用条款与免责声明，**全部勾选**后点 `Submit`。不勾全无法继续。
3. **Device flow 授权**：页面显示一个**设备代码**（形如 `ABCD-1234`）。复制它，另开标签页访问 `https://github.com/login/device`，粘贴代码，点 Authorize 授权 HACS 读取你的 GitHub 账号。**注意：代码 15 分钟有效**，超时需重新生成。[Source: HACS 首次配置 Device flow](https://www.hacs.xyz/)
4. **回到 HA**：授权完成后回到 HA 页面，点 `Submit`，等待几秒验证。
5. **分配区域**：选一个区域（如「家庭」）或不分配，点 `Finish`。

完成后左侧边栏会出现 HACS 入口。「搜索」就是社区仓库的入口，后面装卡片和集成都靠它。

> [!tip] 大白话：Device flow
> Device flow 就像「扫码登录」：GitHub 不给你账号密码，而是给一张一次性的「验证码」（设备代码），你去 GitHub 官网输入验证码，确认「我同意这台设备读我的仓库」。15 分钟有效，就像验证码短信会过期。好处是你全程不把密码交给 HA；只有你亲自授权，HACS 才能替你下载社区仓库。

### 5.3 国内「两段论」：下载可加速，授权必须直连

国内环境用 HACS 有一条铁律，记住它排障快一半：

- **下载/更新阶段可以加速**：第四章配置的 gh-proxy 前缀、hacs-china 极速版、HACS 3.x「选项」里填的 GitHub API 代理，都作用在这一段。
- **首次授权必须直连 GitHub**：Device flow 走的是 `github.com/login/device`，没有任何代理能替你做授权。这是账号安全边界，绕不开。所以先决条件就一条：首次授权时网络必须能直连 GitHub（开全局代理，或临时切到可直连网络）。授权完成后，日常下载、更新走代理即可，不必常开。

> [!tip] 大白话：两段论
> 把 HACS 想成「让你在 GitHub 商店自助提货」。提货（下载文件）可以找快递代理帮你拿；但「验明正身」（授权）必须你本人到场。所以下载失败可以怪网络，授权转圈只能怪自己没直连。

### 5.4 高频报错定位

授权和首次加载最容易踩的坑，集中在下表：

| 报错现象 | 原因 | 处理 |
|---|---|---|
| `Timeout of 20 reached while waiting for...` | 网络/DNS 不通 GitHub | 检查科学上网或 DNS，重试 |
| 列表加载失败 / token 失败 | `api.github.com` 被墙 | HACS「选项」里填 GitHub API 代理（如 `ghapi.hacs.vip/api`）|
| 授权一直转圈 | 未直连 github.com | 开启全局直连，再走一遍 Device flow |
| 搜不到 HACS | 浏览器缓存旧页面 | `Ctrl+F5` 强刷缓存 |
| 下载/更新失败 | 下载源被墙或代理失效 | 换 gh-proxy 前缀（ghproxy.com 已死，改用 gh-proxy.com）|

> 来源：方向 B4 报错说明与 B6 国内高频坑。[Source: HACS 国内环境高频问题](https://www.hacs.xyz/)

### 5.5 常用仓库清单

生态就绪后，下面这些是社区口碑最好、最值得先装的仓库。装法统一：HACS → 搜索仓库名 → 下载 → 重启 HA（集成类）或刷新页面（前端卡片类）。

| 类别 | 名称 | GitHub 仓库 | 用途 |
|---|---|---|---|
| 前端卡片 | Mushroom Cards | `piitaya/lovelace-mushroom` | 现代化仪表盘卡片，触控友好，替代默认卡片 |
| 前端卡片 | Mini Media Player | `piitaya/mini-media-player` | 紧凑型媒体播放器卡片 |
| 前端卡片 | Card Mod | `thomasloven/lovelace-card-mod` | 用 CSS 微调任意卡片样式 |
| 集成 | Xiaomi Miot Auto | `al-one/hass-xiaomi-miot` | 米家设备接入（走 MIoT 协议）|
| 集成 | browser_mod | `thomasloven/hass-browser_mod` | 让浏览器页面变成可控制实体 |
| 集成 | Xiaomi Gateway3 | `AlexxIT/XiaomiGateway3` | 小米多模网关接入（Zigbee/蓝牙）|
| 主题 | Glassmorphism | `reputasyon/glassmorphism-ha` | 毛玻璃质感主题 |
| 主题 | Mushroom Themes | `piitaya/lovelace-mushroom-themes` | 与 Mushroom 卡片配套的主题 |

> 来源：方向 B5 常用仓库清单。

以安装 Mushroom Cards 为例：HACS → 搜索 `Mushroom` → 结果里选 `Mushroom Cards` → 点「下载」确认版本 → 回到仪表盘编辑模式，点「添加卡片」，搜索 `Mushroom` 就能看到一整套新卡片。注意两类仓库的生效时机不同：**前端卡片无需重启**，下载完刷新页面即用；**集成类（如 Xiaomi Miot Auto）需要重启 HA**，之后才会出现在「设置 → 设备与服务 → 添加集成」的搜索结果里。

若某仓库下载后找不到实体，先回 HACS 确认它是否属于「前端卡片 / 主题 / 集成」哪一类，再按对应路径去配置——多数「装不上」其实是找错了入口。

### 本章小结

- HACS 首次配置五步走：加集成 → 勾声明 → Device flow 授权 → 回 HA 确认 → 分配区域。
- Device flow 是安全设计：验证码 15 分钟有效，全程不把 GitHub 密码交给 HA。
- 国内铁律「两段论」：下载/更新可加速，首次授权必须直连 GitHub。
- 报错先看现象定位：超时查网络、列表失败换 API 代理、转圈查直连。
- 常用仓库按需装：卡片类刷新即用，集成类需重启后配置。

生态已经就绪，接下来进入「稳定运行」主题。第六章先解决最基础也最关键的一环：版本锁定与镜像加速策略——让 HA 别再在 `stable` 浮动标签上「随波逐流」。

---

## 第六章：国内稳定运行 —— 版本锁定与镜像加速策略

HACS 配置完成、常用仓库装好之后，你的 HA 已经从「能用」进入了「要长期用」的阶段。本章解决稳定运行的核心问题：**锁版本、双镜像源、升级刻意为之**。做到这三点，HA 不会在某个清晨突然「坏掉」——真正让系统不稳定的，往往不是功能，而是你手里那个不受控的版本。

### 一、`stable` 是浮动标签：今天能用，明天未必

官方文档和大多数教程给的 image 都是 `ghcr.io/home-assistant/home-assistant:stable`。但 `stable` 不是一个具体版本，它是一个**永远指向「当前最新稳定版」的浮动标签**。

> [!tip] 大白话
> 把 `stable` 想成「最新款手机」——你买的是今天的旗舰，但厂家每个月都发新款，标签永远指向最新那台。Home Assistant 每月发布一次，任何一次升级都可能带破坏性变更（2026.1 / 2026.4 / 2026.6 / 2026.8 都有过实测案例）。所以用 `stable` 等于你的版本一直在悄悄变，哪天它自己升上去，坑就来了。[Home Assistant Releases](https://github.com/home-assistant/core/releases)

锁版本就是反过来：把车停进一个**固定车位**，想升级才手动换车位，绝不让浮动标签替你乱开。

### 二、锁版本：固定 tag 的生产写法

先查最新版本，再写进 compose。查法很简单：GitHub Releases 页 `https://github.com/home-assistant/core/releases`，取最新稳定版版本号（截至 2026 年 7 月为 `2026.7.4`，正文不写死，按你查到的为准）[方向 C2：版本锁定策略](https://github.com/home-assistant/core/releases)。

生产环境的 `image:` 应写成固定 tag：

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.7.4  # 固定 tag，不用 stable
    # volumes / privileged / network_mode: host / TZ 等，与第三章的完整配置一致
    restart: unless-stopped
```

固定 tag 的直接好处：**升级变成一次刻意动作**。改一个 tag → `docker compose pull` → `docker compose up -d`，全程你说了算；出了问题也有明确的「改回旧 tag」退路。

### 三、双镜像源：ghcr 前缀替换

先纠正一个常见误解：在 `/etc/docker/daemon.json` 里配 `registry-mirrors`，对 ghcr 是**无效**的。

> [!tip] 大白话
> `registry-mirrors` 像一家「快递中转站」，但它只接 Docker Hub 这一个发货商（`docker.io` 和短名）。ghcr.io 是另一家快递公司，有自己的发货地址，根本不经这个中转站。想加速 ghcr，只能**改收件地址**——把镜像名前缀换成国内镜像源。[方向 C3：国内镜像加速（2026）](https://github.com/docker-practice/docker-registry-cn-mirror-test)

改收件地址就是前缀替换，国内有两个主用源：

```bash
# 主推：南京大学镜像，免费、免认证、每日同步，约 8MB/s
docker pull ghcr.nju.edu.cn/home-assistant/home-assistant:2026.7.4

# 备选：毫秒镜像，2026 实测可用
docker pull ghcr.1ms.run/home-assistant/home-assistant:2026.7.4
```

国内镜像源全景：

| 镜像源 | 类型 | 说明 |
|--------|------|------|
| `ghcr.nju.edu.cn` | 公共免费 | 免认证、每日同步、约 8MB/s，主推 |
| `ghcr.1ms.run` | 公共免费 | 2026 实测可用，备选 |
| `ghcr.xuanyuan.run` | 付费代理 | 轩辕镜像，约 ¥2.9–7/年 |
| `docker.1ms.run` / `docker.m.daocloud.io` / `hub.rat.dev` | Docker Hub 加速 | 只对 addon 等 Docker Hub 镜像有效 |

把替换后的完整镜像名填进 compose 的 `image:` 即可，其余配置不动。注意：镜像源可用性易变，**配置前先实测**——用 `docker-registry-cn-mirror-test` 检测工具测一遍，再决定主源和备源。

### 本章小结

- `stable` 是浮动标签，永远指向最新版，等于「版本不可控」；生产环境用固定版本 tag（如 `:2026.7.4`）
- 查最新版本去 GitHub Releases，别在教程里写死版本号
- `registry-mirrors` 只加速 Docker Hub，对 ghcr 无效；ghcr 必须用前缀替换
- 主推 `ghcr.nju.edu.cn`、备选 `ghcr.1ms.run`，双源互备避免单一失效
- 镜像源域名易变，配置前先用 `docker-registry-cn-mirror-test` 实测

版本策略定了，下一章进入真正的运维实操闭环：**升级、回滚与备份三件套**——如何安全地把 HA 从当前版本升到下一个版本，又在失败时全身而退。

---

## 第七章：更新、回滚与备份 —— 运维三件套

第六章帮你把版本号「钉死」在了 compose 文件里，解决了「今天能用、明天升级带坑」的不确定性。但锁版本只是运维的起点：真正的挑战在于——该升级时怎么安全地升、升级坏了怎么退、日常怎么保证随时能恢复。这一章把 Docker 版 HA 的完整运维闭环一次讲透：**升级前校验 → 升级 → 失败回滚 → 定期备份与恢复**，并解释升级兼容风险从哪来、怎么降险。学完这一章，你可以放心地在任何版本上做变更。

> [!tip] 大白话：升级 = 换发动机，先留好旧发动机
> 把升级想象成给车换发动机：新发动机（新镜像）装上去可能更顺，也可能当场熄火。关键不是「会不会换」，而是换之前先拍下旧发动机的编号（镜像 ID），把旧发动机留着。
> 所以回滚的第一动作永远是「升级前先记录镜像 ID」——有了退路，才敢往前开。

---

### 7.1 升级前校验：先给 HACS 和自定义组件打补丁

很多人在升级时只盯着 HA core 版本，结果升级后一堆集成报错，还分不清是 core 的问题还是插件的锅。正确的顺序是**先更插件、再升核心**：

1. 更新 HACS 本身（HACS → 三个点 → Check for Updates）
2. 更新 HACS 里装的 custom_components（集成列表 → Update Available）
3. 在**当前旧版本**上验证这些插件正常工作
4. 然后再动 HA core 版本

> [!tip] 大白话：搬家前先修好每件家电
> 把升级核心版本想成搬家。搬家前你不会先搬过去再检查电视坏没坏——而是先把每件家电修好、确认能用，再搬进新房子。
> 所以顺序必须是「先更 HACS/插件 → 旧版本验证 → 再升 core」。这样升级后出了问题，才能确定是 core 的锅，而不是一堆插件混在一起无从排查。

**为什么必须这么做？** 因为 `custom_components` 和 core 存在隐式耦合：新版 core 可能改变内部 API，老版插件没跟上就会崩。如果先升 core 再更插件，插件崩了你无法判断「是插件太旧，还是 core 改坏了」。[Home Assistant 官方社区](https://community.home-assistant.io/t/custom-components-and-upgrading/315399) 反复强调这条顺序，2026 年的多起事故（见 7.5）也都指向「插件没更新就升 core」。

升级前还要做一次配置校验，确保 YAML 没有语法错误——否则升完直接进 safe mode：

```bash
# 进入容器，用 HA 自带的脚本校验配置（不启动服务，只检查）
docker exec homeassistant python -m homeassistant --script check_config --config /config
```

如果输出里出现 `ERROR` 或 `Invalid config`，先在旧版本上修好配置再升级。校验通过后再进行下一步。

> [!warning] 易错点
> Docker 版（Container）**不要在 HA 界面点「更新」**。界面里的更新走的是 Supervisor/OS 通道，Container 版没有 Supervisor，点了不生效甚至可能报错。升级、回滚一律由 Docker 侧完成。[Home Assistant 官方 Docker 文档](https://www.home-assistant.io/installation/linux) 明确说明 Container 版需要自己管理更新。

---

### 7.2 升级：Docker 侧的两行命令

升级的本质是「拉新镜像 + 重建容器」。用 compose 管理时只有两行：

```bash
# 先拉取新版本镜像（compose 会自动读取你指定的 image 版本）
docker compose pull homeassistant

# 用新镜像重建容器；配置/数据都在挂载卷里，不会丢
docker compose up -d
```

如果你之前锁了具体版本（比如 `2026.7.4`），升级前把 compose 里的 `image:` 那一行改成目标版本，再执行上面两行。如果直接用 `stable`，`docker compose pull` 就会自动拉到最新版——但正如第六章强调的，生产环境务必用固定版本 tag。[Home Assistant 版本发布页](https://github.com/home-assistant/core/releases) 可查到当前最新稳定版本号。

> [!tip] 大白话：pull + up = 下载发动机 + 装上去
> `pull` 只是把新发动机运到仓库（下载镜像），`up -d` 才是真正装到车上（重建容器）。
> 所以只 `pull` 不 `up` 等于买了新发动机没装，运行中的还是老版本——两个命令要连着用。

升级后验证一下版本号：

```bash
# 确认新版本号
docker logs homeassistant 2>&1 | grep -m1 "Home Assistant"

# 或者看容器信息
docker ps --filter name=homeassistant --format '{{.Image}}'
```

---

### 7.3 回滚：留好旧发动机，随时换回来

升级失败（起不来、进 safe mode、核心集成崩溃）时，第一反应不是修配置，而是**回滚**。Docker 版回滚最稳的做法是「记录镜像 ID + 旧 tag 重建」。

**第一步（升级前就要做）：记录当前镜像 ID**

```bash
# 升级前执行，把输出保存下来——这就是你的「旧发动机编号」
docker inspect homeassistant --format '{{.Image}}'
```

**第二步：回滚命令序列**

```bash
# 1. 拉取旧版本镜像（以 2026.6.5 为例）
docker pull ghcr.io/home-assistant/home-assistant:2026.6.5

# 2. 停掉并删除当前容器（数据在挂载卷里，删容器不丢配置）
docker stop homeassistant && docker rm homeassistant

# 3. 用旧 tag 重建，参数必须和原来完全一致（挂载/网络/TZ/privileged）
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /path/to/config:/config \
  -v /run/dbus:/run/dbus:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:2026.6.5
```

如果你用 compose，回滚更简单：把 `image:` 改回旧 tag，然后 `docker compose up -d` 即可，容器会自动重建。[Home Assistant 社区回滚指南](https://community.home-assistant.io/t/rollback-docker-version/365497) 给出了同样的做法，核心就一句：**换回旧 tag，重建容器，参数保持原样**。

> [!warning] 回滚不是万能的
> 回滚解决的是「新版本代码的锅」。如果升级过程中 **`.storage` 或数据库已经被新版本改写**，即使容器回滚了，数据也可能已经是新 schema——这就要看下一节的数据库风险。

---

### 7.4 数据库 schema 风险：升级前必须备份的根本原因

HA 的数据分两部分：`/config` 下的 YAML/`custom_components`，以及隐藏的 `.storage/` 目录和 `home-assistant_v2.db` 数据库。**跨大版本升级时，`.storage` 和数据库的 schema 可能不兼容**——新版升级时会把数据迁移到新格式，一旦迁移完成，旧版本就再也读不回来了。

- `.storage/`：UI 管理的集成配置、实体注册、设备注册（长期统计等）
- `home-assistant_v2.db`：历史状态、记录器数据

> [!tip] 大白话：记账本格式换了，旧账本就读不懂了
> 把 schema 升级想成换记账本格式：新格式加了新列，新版软件顺手把旧账本誊抄成了新格式。
> 一旦誊抄完，你再拿旧版软件去读这本新账本，就完全看不懂了。所以「升级前先备份」不是客套话，而是唯一能让「升级→回滚」闭环成立的前提。

如果升级后数据库损坏、HA 反复崩溃，极端处理方式是删掉数据库让它重建（**会丢历史**，配置不丢）：

```bash
# 停止容器
docker stop homeassistant

# 删除状态数据库（-wal/-shm 是 SQLite 的附属文件，一并删）
rm -f /path/to/config/home-assistant_v2.db
rm -f /path/to/config/home-assistant_v2.db-wal
rm -f /path/to/config/home-assistant_v2.db-shm

# 重启，HA 会重建一个空数据库
docker start homeassistant
```

`.storage` 一般不用动；只有配置级损坏时才考虑。这条命令救急用，但最优雅的路径永远是 7.6 的完整备份/恢复。

---

### 7.5 备份：先关门，再收拾房间

备份是整个运维三件套的地基。对 Docker 版 HA，备份对象就是 **`/config` 整个目录**（含隐藏的 `.storage`、`.cloud`）——这就是 HA 的全部状态。

**关键纪律：先停容器再打包。**

```bash
# 1. 停容器：让 HA 把正在写的文件落盘，避免打包到"写到一半"的文件
docker stop homeassistant

# 2. 打包整个 /config（含 .storage 等隐藏目录；-C 切到父目录避免路径嵌套）
tar -czf ha-config-$(date +%F).tar.gz -C /path/to/config .

# 3. 打包完立刻重启容器
docker start homeassistant
```

> [!tip] 大白话：先关门，再收拾房间
> 想象你一边开着门窗一边收拾房间，风把窗外的树叶吹进来、房间一直有人进出，你永远收拾不干净。
> 备份同理：HA 运行时会不停写 `.storage` 和数据库，直接打包就像边收拾边有人捣乱，抓到的可能是写到一半的坏文件。先 `docker stop` 等于先关门，收拾出来的才是完整干净的状态。[Home Assistant 官方备份文档](https://www.home-assistant.io/docs/configuration/backup/) 对 Docker/Core 版给出的就是「停容器 + 打包 /config」这条路。

**3-2-1 备份原则**（所有重要数据通用）：

- **3** 份副本（1 份在机器上 + 2 份备份）
- **2** 种不同介质（如本地磁盘 + NAS/移动硬盘）
- **1** 份在异地（云盘、异地服务器，防火灾/盗窃/机器报废）

Docker 版没有内置备份按钮，备份脚本建议写成 cron 任务每周自动跑一次（先停容器、打包、重启、再把 tar 同步到 NAS）。

---

### 7.6 恢复：把备份解包还原到 /config

恢复就是把备份的 `/config` 解包回挂载目录。如果你用的是 **官方 `backup.tar`**（从 HAOS/其他版本导出的备份），结构是内层再包一层 `homeassistant.tar.gz`，要双重解包：

```bash
# 官方 backup.tar 内层是 homeassistant.tar.gz，数据都在里面
tar -xOf /path/of/backup.tar "./homeassistant.tar.gz" \
  | tar --strip-components=1 -zxf - -C /path/to/config

# 解包完成后启动容器
docker start homeassistant
```

如果你按 7.5 直接打的是 `ha-config-*.tar.gz`，恢复就是普通解包：

```bash
tar -xzf ha-config-2026-08-08.tar.gz -C /path/to/config
docker start homeassistant
```

> [!note] 进阶：BackupManager 一键恢复
> 社区有 [BackupManager](https://github.com/AdarWa/BackupManager) 项目，是专门给 Docker 版 HA 的备份恢复工具（需要把 Docker socket 挂载给它的容器，注意安全边界）。它可以在 UI 里一键备份/恢复，省去手敲命令。对只想省事的人值得一试，但理解上面的手搓命令仍然是基本功——工具坏了你才知道自己在做什么。

恢复后验证：`docker ps` 看容器 Up，`docker logs` 无报错，UI 登录后确认实体、历史、配置都在。

---

### 7.7 补：2026 年升级兼容风险案例与降险清单

官方月度发布几乎每次都有破坏性变更（Breaking Changes），2026 年尤其典型：

| 版本 | 破坏性变更 |
|------|-----------|
| 2026.1 | 破坏 Homematic(IP)/ZHA/Tibber 集成 |
| 2026.4 | `custom_components` 覆盖核心集成导致 `Unable to connect` |
| 2026.6 | 移除 legacy template entities |
| 2026.8 | 基于 ContextVar 的老集成失效 |

> [!warning] 降险清单（每次升级前过一遍）
> 1. 先备份 `/config`（7.5）
> 2. 先更 HACS + custom_components，并在旧版本验证（7.1）
> 3. `check_config` 校验配置（7.1）
> 4. 记录当前镜像 ID（7.3）
> 5. 升级前先看官方 [Release Notes](https://github.com/home-assistant/core/releases) 里的 Breaking Changes，确认你用到的集成是否中招
> 6. 避免让 `custom_components` 覆盖核心集成（如 `http`、`config`），这是 2026.4 事故的根源

把这份清单当成升级的「起飞前检查」，每次升级两分钟过一遍，能避开绝大多数翻车。

---

### 本章小结

- **升级** = `docker compose pull homeassistant` + `docker compose up -d`，升完用 `docker logs` 验证版本；Docker 版不要点界面里的更新按钮。
- **升级前顺序很重要**：先更 HACS/custom_components 并在旧版本验证，再动 core；`check_config` 先校验 YAML。
- **回滚** = 升级前记录镜像 ID，失败后停删容器、用旧 tag 重建（参数保持一致）；compose 改回旧 tag 即可。
- **备份** = 先停容器再 `tar` 打包 `/config` 整目录（含 `.storage`），遵循 3-2-1；恢复就是把 tar 解包回挂载目录。
- **数据库风险**：跨大版本 `.storage`/`home-assistant_v2.db` 可能 schema 不兼容，这就是「升级前必须备份」的根本原因；极端情况删库重建（丢历史）。
- **降险**：每次升级前对照降险清单，尤其避开 custom_components 覆盖核心集成。

下一章，我们从「单机运维」切换到「生态扩展」：用 Docker 部署 addon，把整个 Docker Hub 变成你的 Addon Store，补齐 Docker 版没有 Supervisor 的短板。

---

## 第八章：Docker 部署 addon —— 把 Docker Hub 变成你的 Addon Store

第七章把「升级、回滚、备份」的运维闭环收拢了，HA 本体已经能稳定跑起来。但问题来了：很多人在 HAOS 上装 addon（Mosquitto、Node-RED、ESPHome、Zigbee2MQTT）都是点一下「安装」就完事，到了 Docker 版却发现界面里根本没有 Addon Store 这一项。这一章就解决这个缺口——搞懂 addon 本质就是容器镜像，然后用 `docker compose` 手动把常用的几个 addon「安装」回来。

### 8.1 为什么 Docker 版没有「Addon Store」

#### addon 本质就是容器镜像

Home Assistant 官方文档对 addon 的定义说得很直白：

> Under the hood, apps are container images published to a container registry like GitHub Container Registry and Docker Hub.

翻译过来：**addon 的底层就是发布到容器仓库（GHCR、Docker Hub）的容器镜像**。所谓「装 addon」，本质就是「拉一个镜像、跑一个容器」[D1]。你在 HAOS 里看到的 Addon Store，只是一个装潢好的应用商店界面，真正干活的是它背后的 Supervisor——负责从仓库拉镜像、起容器、管生命周期。

> [!tip] 大白话
> 把 addon 想成一个独立的「家电」，HAOS 的 Addon Store 就是家电城的「自动配送安装服务」：你看中哪个，店员（Supervisor）帮你搬回家、装好、通电。而每个家电本身，就是一个容器镜像。

#### Container 版没有 Supervisor，就没有自动安装器

Supervisor 是 HAOS / Supervised 部署方式才有的组件。Docker Container 版只跑一个 HA 核心容器，没有 Supervisor，自然也就没有 Addon Store、没有 `ha` CLI、没有内置备份 [A1]。addon 在设计上是「专门配合 Supervisor 使用」的，所以 Container 版装不了 addon 的原始形态——你只能手动维护**等价容器**：自己拉镜像、自己写 compose、自己管更新和权限 [D1]。

这不一定是坏事。HAOS 的 addon 有自己固定的存储、网络、权限约定，装多了反而「黑盒」；Docker 版全部摊开在 compose 文件里，每个服务什么镜像、挂什么目录、开什么端口，一目了然，可审计、可回滚。

### 8.2 替代思路：整个 Docker Hub 就是你的 Addon Store

既然没有商店，思路就换一个：**几乎所有的 addon 都能在 Docker Hub / GHCR 上找到等价独立容器**，官方 addon 仓库是 `home-assistant/addons`，社区 addon 组织是 `hassio-addons` [D1]。所以正确的替代思路是「**整个 Docker Hub 就是你的 Addon Store**」——你自己当那个管理员，用 `docker compose up` 来「手动安装 App」。

这里要特别提醒一个常见误区：

> [!tip] 大白话
> **HACS 不是 addon 商店的替代品。** HACS 是装「集成、前端卡片、主题」的，装进去的东西都住在 HA 进程内部，比如一个 `custom_components/` 插件。而 addon 是独立运行的容器，比如一个完整的 MQTT 消息服务器。把 HACS 当 addon 商店用，就像你 App 商店里只卖「浏览器插件」，你却想用它装「微信」——装不上。

记住这个分工：**HACS 管 HA 内部的插件生态，Docker 管 HA 外部的伴生服务**。两条线互不替代，各司其职。

### 8.3 官方 / 社区 addon 镜像：命名规则与拉取

知道了要去哪里找容器，还得会读镜像名。addon 镜像主要有两套命名 [D2]：

| 来源 | 命名规则 | 示例 |
|------|----------|------|
| 社区 addon（hassio-addons） | `ghcr.io/hassio-addons/<addon>/<arch>:<version>` | `ghcr.io/hassio-addons/base/amd64:21.0.1` |
| 官方 addon（Docker Hub） | `homeassistant/<arch>-addon-<addon>:<version>` | `homeassistant/aarch64-addon-mosquitto:6.4.1` |

注意那个 `<arch>` 架构标签：`amd64`（Intel/AMD 机器）、`aarch64`（ARM64，如树莓派 4/5）、`armv7`（老树莓派）[D2]。写错架构标签，镜像要么拉不到、要么拉下来跑不动。`uname -m` 看一下宿主机架构，x86_64 就选 `amd64`。

拉取命令很简单：

```bash
# 社区 addon（hassio-addons 组织，GHCR）
docker pull ghcr.io/hassio-addons/base/amd64:21.0.1

# 官方 mosquitto addon（Docker Hub）
docker pull homeassistant/aarch64-addon-mosquitto:6.4.1

# 社区 addon 里最常用的 Node-RED 社区版
docker pull ghcr.io/hassio-addons/node-red/amd64:18.5.0
```

不过**实战中通常不需要拉官方 addon 镜像**——原因见 8.5：官方 addon 内部还带着 Supervisor 的配置约定，直接 `docker compose` 跑往往不如直接用更主流的独立镜像（如 `eclipse-mosquitto`、`nodered/node-red`）干净。拉官方 addon 镜像更多是「验证网络通不通」或「确实想要 addon 的配置结构」时才用。

### 8.4 国内替换映射：一条前缀对照表

第七章已经讲过：`daemon.json` 的 `registry-mirrors` 只加速 Docker Hub，对 `ghcr.io` 无效，必须用**镜像名前缀替换** [C3]。addon 镜像分散在 ghcr.io、docker.io、lscr.io 等多个仓库，替换规则可以整理成一张对照表 [D2]：

| 原镜像源 | 国内替换前缀 | 说明 |
|----------|--------------|------|
| `ghcr.io/...` | `ghcr.nju.edu.cn/...` | 南京大学，主推：免费、免认证、每日同步 |
| `ghcr.io/...` | `ghcr.1ms.run/...` | 毫秒镜像，备选 |
| `docker.io/...`、`lscr.io/...` | `docker.1panel.live/...` | Docker Hub / LinuxServer 镜像加速 |
| GitHub 下载地址 | `gh-proxy.com/https://github.com/...` | 针对 addon 里的脚本/配置下载 |

```bash
# 国内替换示例：三行分别对应上表前三行
docker pull ghcr.nju.edu.cn/hassio-addons/base/amd64:21.0.1
docker pull ghcr.nju.edu.cn/esphome/esphome:latest
docker pull docker.1panel.live/nodered/node-red:latest
```

> [!warning] 易错点
> 替换前缀时，**只改镜像仓库主机名，路径原样保留**。把 `ghcr.io/hassio-addons/...` 换成 `ghcr.nju.edu.cn/hassio-addons/...`，后面的 `/hassio-addons/...` 一个字符都不能动。镜像源可用性易变，配置前用 `docker pull` 实测一下，或查 [docker-registry-cn-mirror-test](https://github.com/docker-practice/docker-registry-cn-mirror-test) 确认哪个源还活着 [C3]。

### 8.5 常见 addon 的完整 compose：五个服务逐段拆解

现在把「Addon Store」里最常装的四件套（Mosquitto、Node-RED、ESPHome、Zigbee2MQTT），连同 HA 本体一起，写进一份完整的 `docker-compose.yml`。这份文件可以直接放进项目的 compose 目录使用，国内环境只需把 `image` 行按 8.4 的前缀替换表改掉 [D3]。

```yaml
services:
  # ---------- HA 本体（沿用第七章的 lock 版 tag） ----------
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable   # 国内换 ghcr.nju.edu.cn 前缀
    container_name: homeassistant
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro
    network_mode: host        # mDNS/SSDP 设备发现必须 host
    restart: unless-stopped

  # ---------- addon: Mosquitto（MQTT 消息服务器） ----------
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mosquitto
    ports:
      - "1883:1883"           # MQTT 主端口
      - "9001:9001"           # MQTT over WebSocket
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    restart: unless-stopped

  # ---------- addon: Node-RED（可视化自动化） ----------
  nodered:
    image: nodered/node-red:latest
    container_name: nodered
    ports:
      - "1880:1880"           # Node-RED 编辑器
    volumes:
      - ./nodered/data:/data
    restart: unless-stopped

  # ---------- addon: ESPHome（ESP 设备固件编译） ----------
  esphome:
    image: ghcr.io/esphome/esphome                        # 国内换 ghcr.nju.edu.cn
    container_name: esphome
    ports:
      - "6052:6052"           # ESPHome Dashboard
    volumes:
      - ./esphome/config:/config
      - /etc/localtime:/etc/localtime:ro
    network_mode: host        # mDNS 发现 ESP 设备
    privileged: true          # 编译时需访问 USB 烧录口
    restart: always

  # ---------- addon: Zigbee2MQTT（Zigbee 网关） ----------
  zigbee2mqtt:
    image: ghcr.io/koenkk/zigbee2mqtt                     # 国内换 ghcr.nju.edu.cn
    container_name: zigbee2mqtt
    ports:
      - "8080:8080"           # 前端控制台
    devices:
      - "/dev/serial/by-id/<你的适配器>:/dev/ttyACM0"     # by-id 稳定路径
    volumes:
      - ./zigbee2mqtt/data:/app/data
      - /run/udev:/run/udev:ro
    environment:
      - TZ=Asia/Shanghai
    depends_on:
      - mosquitto             # 等 MQTT 先起来
    restart: unless-stopped
```

逐段解读关键点：

- **homeassistant**：就是全篇主线的那个服务，`network_mode: host` 保住 mDNS/SSDP/UPnP 设备发现，`/run/dbus` 给蓝牙用 [A3]。生产环境把 `:stable` 换成第七章的固定版本 tag。
- **mosquitto**：独立 `eclipse-mosquitto` 镜像比官方 addon 镜像更通用。三个挂载目录分别放配置、持久化数据、日志；`1883` 是 MQTT 主端口，`9001` 是 WebSocket 端口（给前端网页版 MQTT 调试工具用）[D3]。
- **nodered**：`./nodered/data` 挂到 `/data`，Node-RED 的流程和配置都存在这里，换容器不丢。
- **esphome**：必须 `network_mode: host` 才能在局域网里靠 mDNS 发现 ESP 设备；`privileged: true` 是为了让容器内的烧录工具能访问 USB 串口 [D3]。注意 ESPHome 和 HA 一样要 host，但 Node-RED、Mosquitto 用默认 bridge + 发布端口就够了——host 不是越多越好。
- **zigbee2mqtt**：设备映射**必须用 `/dev/serial/by-id/` 稳定路径**，不要写 `/dev/ttyUSB0`（USB 口换插就会漂移）[D5]。`depends_on: [mosquitto]` 保证 MQTT 先就绪，但 `depends_on` 只等容器启动不等服务可用，生产上 Z2M 有自带重连逻辑，问题不大。

### 8.6 mosquitto.conf：MQTT 的「广播室规则」

Mosquitto 镜像默认不带配置文件，得自己放一个 `./mosquitto/config/mosquitto.conf`，否则容器起不来或行为异常。最小可用版本长这样 [D3]：

```conf
# 监听所有网卡上的 1883 端口
listener 1883 0.0.0.0

# 测试阶段允许匿名连接；生产务必改成密码认证
allow_anonymous true

# 持久化：客户端会话和消息存盘，重启不丢
persistence true
persistence_location /mosquitto/data/
```

三个关键点：

1. **`listener 1883 0.0.0.0`**：`0.0.0.0` 表示监听所有网卡。如果漏掉这一行，Mosquitto 默认只监听 `localhost`，容器外的 HA、Z2M 全都连不上。
2. **`allow_anonymous`**：`true` 只在纯测试环境用——局域网里任何设备都能发消息。生产环境改成 `false`，然后用 `mosquitto_passwd` 生成密码文件，在配置里加一行 `password_file /mosquitto/config/passwd`，并把容器内的用户目录权限 chown 好（否则容器用户写不进挂载目录，这是 Mosquitto 最常见的启动报错）[D5]。
3. **`persistence true`**：把会话和 QoS 消息落盘到 `/mosquitto/data/`，容器重启不丢订阅状态。

> [!tip] 大白话
> 把 MQTT 想成各设备共用的一个「对讲机频道」。灯、传感器、Zigbee 网关各说各的语言，谁也听不懂谁；MQTT 这个频道约定了一条规矩：所有人都把消息写成「主题=内容」贴到频道公告栏（broker），想接收某类消息的人就「订阅」那个主题。Mosquitto 就是那个管公告栏的广播室，`mosquitto.conf` 就是广播室的《管理条例》。

### 本章小结

- addon 的底层就是容器镜像，由 Supervisor 负责拉取和管理；Docker Container 版没有 Supervisor，所以没有 Addon Store，只能手动维护等价容器 [D1]。
- 替代思路是把整个 Docker Hub / GHCR 当作你的 Addon Store，HACS 管 HA 内部插件生态，与 addon 不互相替代。
- 社区 addon 镜像命名 `ghcr.io/hassio-addons/<addon>/<arch>:<version>`，官方 addon 是 `homeassistant/<arch>-addon-<addon>:<version>`，架构标签要写对 [D2]。
- 国内拉取用前缀替换：`ghcr.io` → `ghcr.nju.edu.cn`，`docker.io`/`lscr.io` → `docker.1panel.live`，只改仓库主机名、路径原样保留 [D2]。
- 一份 compose 可以同时编排 HA + Mosquitto + Node-RED + ESPHome + Zigbee2MQTT，注意 ESPHome 要 host 网络、Z2M 设备用 `/dev/serial/by-id/` [D3]。
- `mosquitto.conf` 三要素：`listener 1883 0.0.0.0`、生产关匿名、开持久化 [D3]。

下一章进入收尾：这些容器是跑起来了，但「它们怎么和 HA 互相通信、网络架构怎么设计、设备权限怎么避开那些经典坑」——这是把 addon 真正用起来的关键一环。

---

## 第九章：addon 与 HA 通信、网络架构与权限避坑

上一章我们把 Mosquitto、Node-RED、ESPHome、Zigbee2MQTT 这些 addon 等价容器一个个跑了起来，但它们和 Home Assistant 是彼此独立的容器。如果只让容器「跑起来」而不会「互相通信」，它们就是一座座孤岛。这一章收掉三个关键问题：addon 怎么调用 HA 的接口、网络拓扑怎么设计最稳、设备权限与互斥有哪些坑要躲。

### 一、先认钥匙：LLT + Base URL 是 Docker 版的通信方式

在 HAOS / Supervised 环境里，Supervisor 会给每个 addon 注入一把「专用钥匙」`SUPERVISOR_TOKEN`，addon 只要在配置里写 `homeassistant_api: true`，就自动拿到 HA 的地址和令牌，全程零手动配置。

但 Docker Container 版没有 Supervisor，这个注入机制不存在。addon 容器必须自己知道两件事：**HA 在哪（Base URL）** 和 **用什么身份调用（令牌）**。这个令牌就是你在 HA 界面手动创建的「长期访问令牌」（Long-Lived Access Token，LLT）。

> [!tip] 大白话
> 把 LLT 想成你家门禁的「长期有效门禁卡」：在 HA 的「安全」页面办一张卡，交给 addon 容器，它以后每次进门（调 API）刷卡就能进。Supervisor 环境等于物业直接给每个租户发卡，你不用管；Docker 版没有物业，你得自己给每个 addon 发一张卡。

创建步骤（UI 操作，一次创建长期有效）：

1. HA 左下角点用户名 →「安全」（Security）
2. 拉到「长期访问令牌」区 → 创建令牌
3. 给个名字（如 `nodered-llt`）→ 点创建 → **令牌只显示这一次，立即复制保存**
4. 把 LLT 填进 addon 的 access token 字段，Base URL 填 HA 的地址

之后 addon 就能通过 HA 的 REST API 和 WebSocket API 读写实体、调用服务。把 LLT 和 Base URL 注入容器，常见写法是环境变量：

```yaml
# 通用注入写法：把 LLT 与 Base URL 作为环境变量传给 addon 容器
# 注：Node-RED 官方节点是在 UI 里填，多数桥接容器则支持这种 env 注入
services:
  my-bridge:
    image: <你的桥接容器镜像>
    environment:
      HA_BASE_URL: "http://localhost:8123"   # host 网络下 localhost 就是 HA
      HA_LLT: "<你的长期访问令牌>"
    restart: unless-stopped
```

### 二、Node-RED 接入 HA：勾掉 addon 选项，填 LLT

Node-RED 是最常用的自动化 addon，接入方式分三步：

1. 在 Node-RED 里安装调色板节点 `node-red-contrib-home-assistant-websocket`（Manage palette 搜索安装）
2. 双击任意 HA 节点，打开 Server 配置
3. **取消勾选「Using the Home Assistant addon」** —— 这个开关只属于 Supervised 环境，勾着会让节点去找不存在的 Supervisor API
4. 填 Base URL + LLT

地址具体怎么填，取决于上一章选的网络模式：

| 场景 | Base URL / 地址填法 | 说明 |
|------|---------------------|------|
| HA 用 host 网络 | `http://localhost:8123` 或 `http://<宿主机IP>:8123` | 容器共享宿主网络栈，localhost 就是 HA 自己 |
| HA 与 addon 同处一个 bridge 网络 | `http://homeassistant:8123` | Docker 内建 DNS 按服务名解析 |
| Z2M 等连 Mosquitto | `mqtt://172.17.0.1` | 172.17.0.1 是默认 docker0 桥的网关 IP |

> [!tip] 大白话
> 地址填法其实是在回答「这个容器怎么找到另一个容器」。host 网络下大家共用一个网络栈，说 localhost 就能找到；同一个 bridge 里像住同一栋楼，喊名字（服务名）就行；跨网络时就得说门牌号（IP 地址）。

### 三、hass-cli 与 ha：访客钥匙 vs 管家钥匙

很多教程教你进容器用 `ha` 命令管理 HA，但那只适用于 Supervised 环境。Docker 版没有 Supervisor，`ha` / `hassio-cli` 会直接报错，因为它们走的是 Supervisor API。

Docker 版可用的 CLI 是 `hass-cli` —— 它走 HA 的 REST API，本质就是拿你上面创建的 LLT 调接口：

```bash
# 安装（Python 工具）
pip install homeassistant-cli

# 查实体、调用服务：--server 填 Base URL，--token 填 LLT
hass --server http://localhost:8123 --token <你的LLT> entity list
hass --server http://localhost:8123 --token <你的LLT> service light.turn_on '{"entity_id": "light.room"}'
```

> [!tip] 大白话
> `ha` 命令像「管家专属钥匙」，只有请了管家（Supervisor）的家庭才有；Docker 版没请管家，只能用「访客钥匙」（REST API + LLT）从正门进出。同一个动作，Supervised 版喊管家办，Docker 版自己拿钥匙去办。

### 四、推荐网络架构：HA 用 host 保发现，服务用 bridge 保整洁

网络设计的总原则：**把需要组播的和只需要单播的分开**。

- **HA 必须用 host**：mDNS/Zeroconf、SSDP/UPnP、DLNA 全是组播协议，bridge/NAT 不转发组播。HA 一旦进 bridge，Chromecast、HomeKit、ESPHome 自动发现、局域网设备发现会全部失效。
- **Mosquitto、Node-RED 用 bridge + 发布端口**：它们只做单播通信，bridge 干净且能按服务名互相解析。host 模式的 HA 访问 MQTT 时填 `127.0.0.1:1883`（host 网络与宿主机共享栈，而 Mosquitto 已把 1883 发布到宿主机）。

```yaml
# 推荐架构：HA host 保发现，伴生服务 bridge 管整洁
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    network_mode: host                        # 保住 mDNS/SSDP/UPnP
    volumes: ["./config:/config", "/run/dbus:/run/dbus:ro"]
    restart: unless-stopped

  mosquitto:
    image: eclipse-mosquitto:2
    ports: ["1883:1883", "9001:9001"]         # bridge 网络，只暴露必要端口
    volumes: ["./mosquitto/config:/mosquitto/config"]
    restart: unless-stopped

  zigbee2mqtt:
    image: ghcr.io/koenkk/zigbee2mqtt
    devices:
      - "/dev/serial/by-id/<你的适配器>:/dev/ttyACM0"   # 稳定路径，见第五节
    group_add: ["dialout"]                    # 访问串口所需权限组
    environment: ["TZ=Asia/Shanghai"]
    depends_on: [mosquitto]
    restart: unless-stopped
```

如果你坚持**全 bridge 方案**（HA 也进 bridge），要补两样东西：一是容器名 DNS 解析（compose 内服务名互相可达）；二是 **mDNS 中继**，因为组播被 bridge 挡掉了。常见做法是跑一个 `jdbeeler/mdns-repeater` 中继容器，或给 HA 配 macvlan 网卡拿独立 IP。ESPhome、Z2M 这类依赖 mDNS / USB 的服务仍然建议 host 或显式映射设备。

### 五、权限与互斥避坑清单

最后是最容易踩坑的权限区，核心原则一句话：**别图省事全局 `privileged: true`，要什么设备就给什么设备**。

> [!tip] 大白话
> `privileged: true` 等于把整栋楼的钥匙全交给容器，权限过大；`devices:` 是按清单给——容器要 USB 串口，你就把那个 USB 设备「点名」递进去。前者是「给了所有门禁卡」，后者是「只给了需要的那扇门」。

- **设备映射用稳定路径**：USB 设备映射 `/dev/serial/by-id/xxx:/dev/ttyACM0`，不要用 `/dev/ttyUSB0`——换 USB 口就会漂移，重插拔后 HA / Z2M 找不到设备。
- **权限组**：容器访问串口需要宿主 `dialout` 组权限，compose 里加 `group_add: ["dialout"]`，或确保宿主用户已在 `dialout` / `uucp` 组。
- **ZHA 与 Zigbee2MQTT 互斥**：同一个 Zigbee coordinator（USB 棒）只能被一个服务占用，ZHA 和 Z2M 二选一，否则串口冲突、设备反复掉线。装了 Z2M 的话，记得在 HA「已发现」里忽略 ZHA 设备，避免它自动抢占。
- **Mosquitto 目录权限**：挂载 `./mosquitto/config` 前先 `chown` 给容器用户（通常是 1883），否则容器启动时写配置目录报 permission denied。
- **Frigate + USB Coral**：NPU 加速卡要额外映射 `/dev/bus/usb:/dev/bus/usb` 和 `/dev/apex_0:/dev/apex_0`，并设置 `shm_size`；同时关闭 HA 侧的 Protection Mode 才能让 HA 正确访问 Frigate。

| 避坑项 | 正确做法 | 错误做法 |
|--------|---------|---------|
| 容器权限 | 显式 `devices:` + `group_add` | 全局 `privileged: true` |
| USB 路径 | `/dev/serial/by-id/...` | `/dev/ttyUSB0` |
| Zigbee 设备 | ZHA / Z2M 二选一 | 两个同时占用 coordinator |
| Mosquitto 配置目录 | 先 chown 再挂载 | 直接挂载后启动 |

### 总结：从零到一套完整 HA 体系的回顾与进阶

到这里，整条主线已经走完：**部署（第 1-3 章）→ HACS 生态（第 4-5 章）→ 稳定运维（第 6-7 章）→ addon 补齐（第 8-9 章）**。最后把几个最关键的口诀收进一句：

- host 网络保住设备发现；addon 通信靠 LLT + Base URL；`ha` 命令在 Docker 版不存在，用 `hass-cli` 或 REST API
- 国内拉镜像用前缀替换（如 `ghcr.nju.edu.cn`）；`stable` 是浮动标签要锁版本；升级前先备份再动 core 版本
- 设备权限按需映射，ZHA / Z2M 互斥，USB 用 by-id 稳定路径，Mosquitto 目录先 chown

**进阶方向建议**：

- **安全加固**：MQTT 从匿名改为密码认证（`allow_anonymous false` + password_file）；LLT 按 addon 分开创建，便于单独吊销
- **高可用与远程**：给 HA 套 frp / ZeroTier 做远程访问；Frigate + Coral 做本地 NVR；配置目录做异地备份
- **DevOps 化**：用 Git 管理 `configuration.yaml`；容器镜像可加 Watchtower 自动更新提示，但升级仍需「先备份、锁版本、再验证」三步

至此，Docker 版 HA 从部署、生态、运维到 addon 的四段主线全部打通。你可以回到索引页串起全文，按需选读各章了。

---

> 本章素材引用：`02_deep_research.md` 方向 D4（addon 与 HA 通信）、D5（关键坑）、D6（网络架构设计）。
