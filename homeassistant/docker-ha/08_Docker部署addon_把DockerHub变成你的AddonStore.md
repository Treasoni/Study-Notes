---
title: "第八章：Docker 部署 addon —— 把 Docker Hub 变成你的 Addon Store"
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
chapter: 八
---

# 第八章：Docker 部署 addon —— 把 Docker Hub 变成你的 Addon Store

[[07_更新回滚与备份_运维三件套.md|← 第七章 · 更新回滚与备份]] ｜ [[09_addon通信网络架构与权限避坑.md|第九章 · addon 通信与避坑 →]]

[[Docker 部署 Home Assistant 完全指南|← 返回索引]]

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
