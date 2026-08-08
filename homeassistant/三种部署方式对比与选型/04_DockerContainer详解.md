---
title: "第四章：Docker Container 详解"
tags:
  - 智能家居/HomeAssistant
  - 学习笔记
  - 部署方式
created: 2026-08-05
updated: 2026-08-08
status: 已完成
source_project: home-assistant-deployment-methods
---
# 第四章：Docker Container 详解

上一章的 HAOS 虚拟机是官方推荐的全托管方案，但它独占整机、无法与别的服务共存。如果你手里已经有一台 NAS 或 VPS，想把 HA 塞进去而不是再开一台机器，Docker Container 就是官方两条正式路径里更轻的那条。这一章回答三个问题：Container 版到底少了什么、官方 compose 模板每一行在做什么、以及日常升级和踩坑怎么处理。

## 4.1 是什么：仅 Core 的容器方式

Container 方式 = **你自己的 Linux 系统 + Docker 编排，只运行 Home Assistant Core 这一个容器**。官方定义是「自带系统（Linux）+ Docker 编排，只运行 Home Assistant Core」。这里「自带系统」指宿主 OS 由你管理（Debian、Ubuntu、NAS 的 DSM 等），Docker 负责把 Core 圈在容器里跑。

### 它有什么、没有什么

| 能力 | Container | HAOS |
|------|-----------|------|
| Core | ✅ | ✅ |
| Supervisor | ❌ | ✅ |
| Add-on 商店 | ❌ | ✅ |
| OTA 自动更新 | ❌（手动 pull） | ✅（约每 8h 检查） |
| 托管快照备份 | ❌ | ✅ |
| Thread / Z-Wave | ❌ 开箱不支持 | ✅（由 Add-on 提供） |
| 与其他服务共存 | ✅ | ❌ 独占 |

一句话总结：**Container 是「裸 Core」**。因为 Add-on 本质是 Supervisor 托管的 Docker 容器，没有 Supervisor 就没有 Add-on 商店；Thread、Z-Wave 这类硬件协议集成依赖 Add-on 提供运行环境，Container 开箱即不支持。这正是它与 HAOS 最核心的功能差异。

### 硬性要求

- **Docker Engine ≥ 23.0.0**（Docker CE 或 Linux 发行版仓库里的新版均可）。
- **Docker Desktop 不可用**：HA 依赖 host 网络模式和 USB 设备直通，这两者依赖 Linux 内核能力；Docker Desktop 在 macOS / Windows 上运行在虚拟机层之上，host 网络行为不兼容、设备直通不可用，官方不视为受支持环境。

> [!warning] 平台边界
> 不要在 macOS / Windows 桌面上直接跑 Container 版 HA。要么改用 WSL2 内的原生 Docker Engine（Linux 语义），要么干脆选 HAOS 虚拟机。

## 4.2 官方 compose 模板逐行拆解

官方提供了一份开箱即用的 docker-compose 模板，完整给出如下：

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /PATH_TO_YOUR_CONFIG:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro      # 蓝牙集成必需
    restart: unless-stopped
    privileged: true
    network_mode: host
    environment:
      TZ: Asia/Shanghai             # 中国标准时间（北京时间，UTC+8），必须是 tz database 名称
    devices:                        # USB 直通 Zigbee/Z-Wave
      - /dev/ttyUSB0:/dev/ttyUSB0
```

### image：镜像来源

`ghcr.io/home-assistant/home-assistant:stable` —— 官方镜像发布在 GitHub Container Registry（ghcr.io）。`stable` 是稳定版标签；想回滚到特定版本时，把它改成具体版本号（如 `2025.7.4`）即可，见 4.3。

### volumes：三个挂载各自为什么

| 挂载 | 作用 | 说明 |
|------|------|------|
| `/PATH_TO_YOUR_CONFIG:/config` | 配置持久化 | HA 的 `configuration.yaml`、数据库、custom_components 全在 /config，必须挂到宿主持久目录，否则容器重建即全部丢失 |
| `/etc/localtime:/etc/localtime:ro` | 时区文件 | 只读挂载宿主时区，让容器内日志与调度时间和宿主一致 |
| `/run/dbus:/run/dbus:ro` | 蓝牙集成必需 | 宿主 D-Bus 是蓝牙栈（BlueZ）的通信通道，只读挂载后 HA 才能发现并控制蓝牙适配器 |

其中 `:ro` 表示只读挂载，防止容器内误写宿主的系统文件。

### restart: unless-stopped

容器异常退出时自动重启，但手动 `docker stop` 后不会再被拉起。适合常驻服务，避免断电、崩溃后 HA 一直掉线。

### privileged: true

特权模式。HA 需要访问大量底层硬件（USB、部分内核接口），官方模板直接用特权模式换取最广的硬件兼容性。若想收敛权限，需要逐项用 `capabilities` + `devices` 替代，但官方模板并不保证精简后仍完整可用——能跑官方默认配置就先用默认配置。

### network_mode: host：模板里最重要的一行

直接使用宿主的网络栈，容器不拥有独立 IP。必须用 host 网络的原因是：**mDNS 设备发现和蓝牙发现依赖在宿主网络接口上广播 / 监听，bridge 网络会隔离这些广播包**。代价是端口无法用 `ports` 映射管理（见下节）。

### environment: TZ

时区必须是 tz database 标准名称（如 `Asia/Shanghai`），不是 `UTC+8` 这种偏移量写法。即使挂载了 `/etc/localtime`，仍建议显式设置，避免容器内运行时差异。

### devices：USB 设备直通

把宿主的 USB 串口设备映射进容器，典型场景是 Zigbee（Conbee、自制 CC2531 等）或 Z-Wave 适配器。可以先用 `lsusb` 查设备的 vendor:product ID，也可以直接用 `/dev/ttyUSB0` 这种设备路径。直通后还要保证容器用户有权限访问，见 4.4。

### 为什么没有 ports 段

这是新手最容易疑惑的点。既然 `network_mode: host`，容器与宿主共享网络栈，HA 的 8123 端口直接暴露在宿主所有网卡上，**不需要、也无法再用 `ports` 做端口映射**。反过来，网上有些教程既保留 host 网络又让你写 `ports:`，那是矛盾的配置。只有放弃 mDNS/蓝牙发现、改用 bridge 网络时，`ports` 才派得上用场，但会失去发现能力。

### 启动与验证

```bash
docker compose up -d
docker ps                         # 看容器状态是否为 Up
docker logs homeassistant         # 观察启动日志，直到出现 Home Assistant 启动完成
```

首次启动后浏览器访问 `http://<宿主IP>:8123`，进入初始化向导。

## 4.3 升级与维护流程

Container 没有 OTA，更新 = **拉新镜像 + 重建容器**，配置与数据留在 /config 挂载目录里不受影响。

### 方式 A：compose 项目（推荐）

```bash
docker compose pull
docker compose up -d
```

`pull` 拉取新镜像，`up -d` 用新镜像重建容器并沿用 compose 里的全部配置。升级前建议先备份 /config。

### 方式 B：纯 docker run

```bash
docker pull ghcr.io/home-assistant/home-assistant:stable
docker stop homeassistant
docker rm homeassistant
# 用与首次启动完全相同的参数重新 run
docker run -d --name homeassistant \
  --restart unless-stopped \
  --privileged \
  --network host \
  -e TZ=Asia/Shanghai \
  -v /PATH_TO_YOUR_CONFIG:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  --device /dev/ttyUSB0:/dev/ttyUSB0 \
  ghcr.io/home-assistant/home-assistant:stable
```

> [!tip] 回滚
> 新版翻车时，把镜像 tag 指回上一个可用版本，再走一遍重建流程即可。HA 配置文件向后兼容，回滚不会丢 /config 数据。

### 三件「手动」的事

| 事项 | 说明 |
|------|------|
| 备份 | 无托管快照，需自行定期备份 /config（tar、rsync、NAS 快照均可） |
| 反向代理 | 公网访问需自己配置 Nginx / Caddy 反代，官方不提供托管入口 |
| 更新 | 无自动检查通知，需关注官方 release 公告或自行接入更新提示 |

HA 官方约每月发布一个大版本，习惯了 HAOS「自动升级」的用户，用 Container 后要自己记着这个节奏。

## 4.4 常见坑

### ARM64 SoC 页大小 >4K：DISABLE_JEMALLOC

部分 ARM64 开发板（内存页大小 >4KB）启动时崩溃，日志报：

```text
<jemalloc>: Unsupported system page size
```

解决：在 environment 里加 `DISABLE_JEMALLOC=true`，让 HA 不使用 jemalloc 内存分配器。

```yaml
    environment:
      TZ: Asia/Shanghai
      DISABLE_JEMALLOC: "true"
```

### /dev/tty* 权限不足

USB 直通后容器内可能仍打不开串口。确保容器运行用户属于宿主的 `dialout` / `plugdev` 组，或通过 udev 规则放开 `/dev/ttyUSB0` 的访问权限。症状通常是日志里出现 `Permission denied`、集成反复「设备不可用」。

### 防火墙挡住 8123

容器能跑但外部访问不了时，先查宿主防火墙。Ubuntu 的 ufw 默认会拦掉入站端口，需要放行：

```bash
sudo ufw allow 8123/tcp
```

### 别把 host 网络改成 bridge

为了「安全」把 `network_mode` 改成 bridge 后，mDNS 设备发现、蓝牙发现会失效，常见症状是「设备一直搜索不到、自动发现全没了」。host 网络是官方模板的默认配置，改动前先想清楚取舍。

## 4.5 优点 / 缺点 / 适用场景

| 维度 | 结论 |
|------|------|
| 优点 | 最灵活；资源占用低（空闲约 300-400MB）；可与其他容器共存（NAS / VPS）；崩溃不影响宿主 |
| 缺点 | 无 Add-on 生态；备份 / 反代 / 更新全手动；需要 Docker 技能 |
| 适用 | 已有 Docker 主机 / NAS 用户；想与其他服务共存；能接受手动维护 |

- **最适合**：手里已有群晖 / 威联通 / 自建 NAS 或 VPS，不想为 HA 独占一台机器。Core 的空闲占用约 300-400MB，在 NAS 上几乎无感。
- **最不适合**：想要 Add-on 商店、Thread / Z-Wave 开箱支持、零维护体验的用户——这些正是 HAOS 的强项（第三章）。
- **定位提醒**：Container 是官方两条正式路径之一（另一条是 HAOS）。选它是「以功能减配换取共存与轻量」，不是「更差」，是取舍不同。

## 本章小结

- Container 只跑 Core：无 Supervisor、无 Add-on、无 OTA，Thread / Z-Wave 开箱不支持。
- 硬性要求 Docker Engine ≥ 23.0.0，Docker Desktop 不可用（host 网络 + USB 直通依赖 Linux）。
- host 网络是模板核心：mDNS / 蓝牙发现依赖它，因此模板里没有 ports 段。
- 升级 = docker pull + 重建（compose 则 `pull && up -d`）；备份 / 反代 / 更新全手动。
- 常见坑：DISABLE_JEMALLOC、/dev/tty* 权限、ufw 放行 8123、勿改 bridge。

补上第三条路径 HA Supervised：一条官方已弃用的旧路径。

---

> [[Home Assistant 三种部署方式对比与选型|⬅ 返回索引]]　·　[[03_HAOS虚拟机详解|上一篇]]　·　[[05_HASupervised详解|下一篇]]
