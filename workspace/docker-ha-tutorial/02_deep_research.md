# 用 Docker 配置 Home Assistant（HA）详细教程 - 深度资料收集

收集时间: 2026-08-08
搜索关键词: docker home assistant, ghcr 国内加速, HACS docker 安装, hacs-china, home assistant docker 更新, home assistant addon docker compose
信源: 官方文档（home-assistant.io / hacs.dev / developers.home-assistant.io / esphome.io / zigbee2mqtt.io）+ 社区讨论（home-assistant community / hassbian / 多篇实测博客）

---

## 方向 A：Docker 部署 HA

### 1. 官方推荐部署方式（截至 2026）
- **官方仅支持两种**：HAOS（推荐大多数用户）与 HA Container（已有 Docker 环境的熟练用户）。
- **Supervised 已弃用**（2025）：跑 Portainer/Watchtower 等会被标 Unsupported/Unhealthy。
- Docker Container 局限：无 Supervisor → 无 Add-on Store、无 ha CLI、无内置备份；更新/备份/伴生服务全部自管。

### 2. 官方 docker run 命令
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

### 3. 官方推荐 compose.yaml
```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /PATH_TO_YOUR_CONFIG:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
    environment:
      TZ: Asia/Shanghai
```
要点：
- Docker Engine ≥ 23.0.0；**Docker Desktop 不可用**（仅 Linux）
- `TZ` 必须是 tz database 名称（如 `Asia/Shanghai`）
- `/run/dbus` 挂载可选但蓝牙集成必需
- 防火墙放行 TCP 8123：`sudo ufw allow 8123/tcp`

### 4. 网络模式：host vs bridge
- **必须 host 的原因**：mDNS/Zeroconf、SSDP/UPnP、DLNA 是组播协议，bridge/NAT 不转发组播 → Chromecast、HomeKit、ESPHome、局域网设备发现全失效
- host 模式：容器共享宿主网络栈，`http://<host>:8123` 直达，无需端口映射；仅 Linux 生效
- bridge 模式：云集成可用，本地发现坏；替代方案 macvlan / Avahi reflector / ESPHome `status_use_ping: true`
- mDNS 默认不跨子网/VLAN，需路由器 Avahi 反射 + 放行 UDP 224.0.0.251:5353

### 5. 设备直通
- **优先稳定路径** `/dev/serial/by-id/`（按序列号命名，换 USB 口不变）；`/dev/ttyUSB0` 会漂移
- compose：`devices: - /dev/serial/by-id/...:/dev/ttyACM0`
- 权限：宿主用户加 `dialout`/`uucp` 组；`privileged` 非必需，仅兜底
- 蓝牙（hci0）：不在 `/dev/serial/by-id`；需挂 `/run/dbus:/run/dbus:ro`，先 `bluetoothctl power on`

### 6. 国内拉取 ghcr.io（关键）
- **`daemon.json` 的 `registry-mirrors` 对 ghcr.io 无效**（只加速 Docker Hub）；必须用**镜像名前缀替换**
- **ghcr.nju.edu.cn（南京大学）**：免费、免认证、每日同步、~8MB/s，广泛实测可用
  ```bash
  docker pull ghcr.nju.edu.cn/home-assistant/home-assistant:stable
  ```
- **ghcr.1ms.run（毫秒镜像）**：格式 `docker pull ghcr.1ms.run/home-assistant/home-assistant:stable`；多来源 2026 实测可用
- 其它：`docker.1panel.live`、`ghcr.dockerproxy.com`（**待实测**）
- 镜像源可用性易变，配置前查 [docker-registry-cn-mirror-test](https://github.com/docker-practice/docker-registry-cn-mirror-test)

### 7. config 目录标准结构
- Docker 版配置目录 = `/config`（挂载卷）
- **首次启动且目录为空时**自动生成默认 `configuration.yaml`：
```yaml
# Loads default set of integrations. Do not remove.
default_config:
frontend:
  themes: !include_dir_merge_named themes/
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```
- `default_config:` 一行加载一批默认集成（frontend、api、discovery、hassio 等）
- 坑：仅当目录**完全为空**才自动生成；`!include` 引用文件不存在会启动报错进 safe mode
- UI 管理数据存在隐藏 `.storage/`，与 `configuration.yaml` 都应持久化
- 校验：`hass --script check_config`

---

## 方向 B：HACS 安装与使用

### 1. HACS 是什么 + 官方脚本做了什么
- HACS = Home Assistant Community Store，社区应用商店（集成/前端卡片/主题/脚本）
- Docker 版必装：米家、影音、好看卡片全靠 HACS
- 官方脚本 `wget -O - https://get.hacs.xyz | bash -`：
  1. 探测含 `.HA_VERSION` 的配置目录（`/config` 等）
  2. 检查 `wget` + `unzip`（缺一报错退出）
  3. 下载 `github.com/hacs/integration/releases/latest/download/hacs.zip`
  4. 解压到 `custom_components/hacs/`（先删旧目录）
  5. 比对 `MINIMUM_HA_VERSION`
  6. 提示重启 HA
- Docker 为何手动放置：脚本需容器内 wget/unzip + 直连 GitHub；放置后必须 `docker restart`

### 2. Docker 三种安装路径

**路径一（进容器跑脚本）**：
```bash
docker exec -it homeassistant bash
cd /config   # 需含 .HA_VERSION
wget -O - https://get.hacs.xyz | bash -
exit
docker restart homeassistant
```

**路径二（宿主机解压到挂载目录）**：
```bash
cd <docker -v 挂载的配置目录>
mkdir -p custom_components/hacs
wget https://github.com/hacs/integration/releases/latest/download/hacs.zip
unzip hacs.zip -d custom_components/hacs && rm hacs.zip
docker restart homeassistant
```

**路径三（docker cp + 容器内解压）**：
```bash
wget -O /tmp/hacs.zip https://github.com/hacs/integration/releases/latest/download/hacs.zip
docker cp /tmp/hacs.zip homeassistant:/config/custom_components/hacs/
docker exec -it homeassistant sh
cd /config/custom_components/hacs && unzip hacs.zip && rm hacs.zip
exit
docker restart homeassistant
```
关键：文件必须直接落在 `custom_components/hacs/`，不能多一层嵌套。

### 3. 国内加速方案（截至 2026）
- **hacs-china 极速版**：`wget -O - https://get.hacs.vip | bash -`；最后发布 2025-08 v2.0.5.3；内置 gitmirror/fastgit/ghproxy 加速下载；**只加速下载，首次 GitHub 授权仍须直连**；风险=第三方 fork（可用性**待实测**）
- **ghproxy 前缀代理**：`ghproxy.com` 已失效（2025 起）；替代 `gh-proxy.com`、`mirror.ghproxy.com`、`ghproxy.net`、`ghfast.top`
  ```bash
  wget https://gh-proxy.com/https://github.com/hacs/integration/releases/latest/download/hacs.zip
  ```
- **GitHub API 代理**（解决列表加载失败）：HACS 3.x「选项」UI 填自定义 API 地址（非 configuration.yaml）：`ghapi.hacs.vip/api`、`ghapi-cf.hacs.vip/api` 等

### 4. HACS 3.x 首次配置完整流程
1. Settings → Devices & Services → **清缓存/硬刷新（Ctrl+F5）**，否则搜不到 HACS
2. + Add Integration → 搜 HACS → 勾选全部声明 → Submit
3. Device flow：复制设备代码 → 开 `https://github.com/login/device` → 粘贴代码 → Authorize HACS → 回 HA → Submit（代码 15 分钟有效）
4. 分配区域 → Finish
- 报错：`Timeout of 20 reached while waiting for...` = 网络/DNS 不通 GitHub；token/列表失败 = api.github.com 被墙；授权转圈 = 需科学上网

### 5. 常用仓库
- 前端卡片：Mushroom Cards `piitaya/lovelace-mushroom`；Mini Media Player `piitaya/mini-media-player`；Card Mod `thomasloven/lovelace-card-mod`
- 集成：Xiaomi Miot Auto `al-one/hass-xiaomi-miot`；browser_mod `thomasloven/hass-browser_mod`；Xiaomi Gateway3 `AlexxIT/XiaomiGateway3`
- 主题：Glassmorphism `reputasyon/glassmorphism-ha`；Mushroom Themes `piitaya/lovelace-mushroom-themes`

### 6. 国内高频坑
- 下载/更新失败 → gh-proxy 前缀或极速版
- 首次授权绕不开 GitHub 直连（device flow 走 github.com）
- 小容器缺 unzip（Synology 报 `'unzip' is not installed`）；属主可能需 `chown -R 1000:1000 custom_components/hacs`
- 搜不到 HACS → 强刷缓存；ghproxy.com 已死 → 改 gh-proxy.com

---

## 方向 C：国内稳定使用与更新

### 1. Docker 稳定更新完整流程
**Compose 两行**：
```bash
docker compose pull homeassistant
docker compose up -d
```
**CLI 方式**：
```bash
docker pull ghcr.io/home-assistant/home-assistant:stable
docker stop homeassistant && docker rm homeassistant
# 重跑与最初一致的 docker run 命令
```
- 升级前：改完 YAML 用 `docker exec homeassistant python -m homeassistant --script check_config --config /config` 校验
- **升级前先更新 HACS/custom_components 并在旧版本验证**，再动 core 版本
- Docker 版**不要**在 HA 界面点「更新」，升级/回滚一律由 Docker 侧完成

### 2. 版本锁定策略
- `stable` 是浮动标签；支持固定版本标签 `ghcr.io/home-assistant/home-assistant:2026.8.1`
- 查最新版本：GitHub Releases `https://github.com/home-assistant/core/releases`（截至 2026-07-24 最新稳定 **2026.7.4**）
- 生产锁版：
```yaml
image: ghcr.io/home-assistant/home-assistant:2026.7.4   # 不用 stable
```
- 升级 = 改 tag → `docker compose pull` + `up -d` 的刻意动作；记录镜像 digest/ID 便于回滚

### 3. 国内镜像加速（2026）
- **registry-mirrors 对 ghcr 无效的官方依据**：`daemon.json` 的 `registry-mirrors` 只拦截 Docker Hub（`docker.io`/短名）；`ghcr.io` 是独立 registry 主机名，不会被路由到 Hub mirror
- **ghcr.1ms.run**：已验证可用，只换域名前缀
  ```bash
  docker pull ghcr.1ms.run/home-assistant/home-assistant:2026.7.4
  ```
- **ghcr.nju.edu.cn**：免认证、每日同步、~8MB/s，稳定备选
- **轩辕镜像**（付费代理）：`你的前缀-ghcr.xuanyuan.run/<原路径>`（约 ¥2.9–7/年）
- **Docker Hub 公共镜像（addon 等）加速**：`docker.1ms.run`、`docker.m.daocloud.io`、`hub.rat.dev`

### 4. 回滚完整操作
```bash
# 1. 升级前记录当前镜像 ID
docker inspect homeassistant --format '{{.Image}}'
# 2. 拉取旧版本镜像
docker pull ghcr.io/home-assistant/home-assistant:2026.6.5
# 3. 停止并删除容器
docker stop homeassistant && docker rm homeassistant
# 4. 用旧标签重建（保留原挂载/network host/TZ/privileged 参数）
docker run -d --name homeassistant --privileged --restart=unless-stopped \
  -e TZ=Asia/Shanghai -v /PATH_TO_CONFIG:/config --network=host \
  ghcr.io/home-assistant/home-assistant:2026.6.5
```
- Compose 回滚：`image:` 改回旧 tag → `docker compose up -d`
- 验证：`docker ps`、`docker logs --tail=200 homeassistant`、UI Settings>About 确认版本
- **数据库不兼容**：`.storage` 与 `home-assistant_v2.db` 跨大版本可能 schema 不兼容；极端情况删 `home-assistant_v2.db` 及其 `-wal`
- 旧镜像拉不下来：`docker save` + tar 传输 + `docker load`

### 5. 备份策略具体命令
```bash
# 先停容器再打包，避免写冲突
docker stop homeassistant
tar -czf ha-config-$(date +%F).tar.gz -C /PATH_TO_CONFIG .
docker start homeassistant
```
- 备份对象 = `/config` 整目录（含隐藏 `.storage`、`.cloud`）
- Docker/Core 版无内置恢复按钮；官方 backup.tar 内层 `homeassistant.tar.gz` → `data/` 即完整 `/config`
- 恢复：
  ```bash
  tar -xOf /path/of/backup.tar "./homeassistant.tar.gz" | tar --strip-components=1 -zxf - -C <config挂载目录>
  ```
- **3-2-1 落地**：本地 tar + NAS/移动盘 + 异地加密副本；社区 `AdarWa/BackupManager`（仅 Docker 版，需挂 docker socket）可一键恢复

### 6. 升级兼容风险
- 官方月度发布含破坏性变更；案例：2026.1 破坏 Homematic(IP)/ZHA/Tibber；2026.4 custom_components 覆盖核心集成导致 Unable to connect；2026.6 移除 legacy template entities；2026.8 基于 ContextVar 的老集成失效
- 降险：升级前备份 + 更新 HACS/custom_components + 查 GitHub/论坛已知问题 + 避免自定义覆盖核心集成（http 等）
- 社区工具 Upgrade Advisor（HACS 安装）AI 分析 breaking changes；非官方，谨慎使用

---

## 方向 D：Docker 部署 addon

### 1. 核心原理
- **Addon 本质就是 Docker 容器**：官方文档原文「Under the hood, apps are container images published to a container registry like GitHub container registry and Docker Hub」。Supervisor 负责拉取/管理
- **Container 版无 Supervisor → 无 Addon Store**：addon 设计为专与 Supervisor 配合，Container 版只能手动维护等价容器
- **替代思路**：「整个 Docker Hub 就是你的 Addon Store」——几乎所有 addon 都能找到等价独立容器
- **HACS 不是替代品**：HACS 装集成/前端，不装容器
- 官方 addon 仓库：`home-assistant/addons`；社区 org：`hassio-addons`

### 2. 官方 addon 镜像直接跑
- 社区 addon 镜像命名：`ghcr.io/hassio-addons/<addon>/<arch>:<version>`（arch: amd64/aarch64/armv7）
  ```bash
  docker pull ghcr.io/hassio-addons/base/amd64:21.0.1
  docker pull homeassistant/aarch64-addon-mosquitto:6.4.1  # 官方 mosquitto（Docker Hub）
  ```
- 国内镜像（ha-china/hassio-addons）：ghcr.io→`ghcr.nju.edu.cn`、docker.io/lscr.io→`docker.1panel.live`、github→`gh-proxy.org`
  ```bash
  docker pull ghcr.nju.edu.cn/hassio-addons/base/amd64:21.0.1
  ```

### 3. 常见 addon 完整 compose（含国内镜像注意点）
```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable   # 国内换 ghcr.nju.edu.cn 前缀
    container_name: homeassistant
    volumes: ["./config:/config", "/etc/localtime:/etc/localtime:ro", "/run/dbus:/run/dbus:ro"]
    network_mode: host        # mDNS/SSDP 发现需要
    restart: unless-stopped

  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mosquitto
    ports: ["1883:1883", "9001:9001"]                     # 9001 = MQTT WebSocket
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    restart: unless-stopped

  nodered:
    image: nodered/node-red:latest
    container_name: nodered
    ports: ["1880:1880"]
    volumes: ["./nodered/data:/data"]
    restart: unless-stopped

  esphome:
    image: ghcr.io/esphome/esphome                        # 国内换 ghcr.nju.edu.cn
    container_name: esphome
    ports: ["6052:6052"]                                  # dashboard
    volumes: ["./esphome/config:/config", "/etc/localtime:/etc/localtime:ro"]
    network_mode: host        # mDNS 发现设备
    privileged: true
    restart: always

  zigbee2mqtt:
    image: ghcr.io/koenkk/zigbee2mqtt                     # 国内换 ghcr.nju.edu.cn
    container_name: zigbee2mqtt
    ports: ["8080:8080"]
    devices: ["/dev/serial/by-id/<你的适配器>:/dev/ttyACM0"]  # by-id 稳定路径
    volumes: ["./zigbee2mqtt/data:/app/data", "/run/udev:/run/udev:ro"]
    environment: ["TZ=Asia/Shanghai"]
    depends_on: [mosquitto]
    restart: unless-stopped
```
mosquitto.conf（`./mosquitto/config/`）：`listener 1883 0.0.0.0`、`allow_anonymous true`（测试用，生产改 `password_file` + `allow_anonymous false`）、`persistence true`、`persistence_location /mosquitto/data/`

### 4. addon 与 HA 通信
- **Supervisor 环境内**：`homeassistant_api: true` + `SUPERVISOR_TOKEN`
- **Container 版（无 Supervisor）**：手动提供**长效 token（LLT）** + 地址
- Node-RED 装 `node-red-contrib-home-assistant-websocket`，**取消勾选 "Using the Home Assistant addon"**，填 Base URL + LLT
- 地址填法：host 网络下 `http://localhost:8123`；bridge 同网可填服务名 `http://homeassistant:8123`；Z2M 的 MQTT 填 `mqtt://172.17.0.1`（docker0 桥 IP）
- **CLI 区别**：`hass-cli` 走 HA REST API（Container 版可用）；`hassio-cli`/`ha` 走 Supervisor API（Container 版**不可用**）

### 5. 关键坑
- **别全局 `privileged: true`**：用显式 `devices:` 映射 + `group_add`（rootless 加 `group_add: [dialout]`）
- **网络模式一致性**：HA 用 host 时不在任何 bridge 网，无法按容器名解析 `mosquitto`；解法是 HA 里填宿主机 IP，或 `extra_hosts` + mosquitto 固定静态 IP
- **USB 稳定路径**：Z2M 官方明确必须用 `/dev/serial/by-id/`（`/dev/ttyUSB0` 会漂移）
- **ZHA 互斥**：ZHA 与 Z2M 不能共用同一 coordinator（二选一或买第二个 dongle）；HAOS 下即使没装 ZHA 也需在「已发现」忽略该 ZHA 设备
- **mosquitto 目录权限**：挂载 config 前需 chown 或保证容器用户可写
- **Frigate + USB Coral**：`devices: [/dev/bus/usb:/dev/bus/usb, /dev/apex_0:/dev/apex_0]` + `shm_size`；关 Protection Mode

### 6. 网络模式设计（架构建议）
- **推荐默认**：HA 用 host（保住 mDNS/SSDP/UPnP）；Mosquitto、Node-RED 用 bridge + 发布端口；HA 侧通过宿主机 IP 或 `127.0.0.1:1883` 访问
- **全 bridge 方案**：HA 也进 bridge，容器名解析最干净，但丢 mDNS → 需 mDNS 中继容器（`jdbeeler/mdns-repeater`）或 macvlan
- **Node-RED 不建议 host 模式**（多余暴露端口）；仅 ESPHome/Z2M 这类依赖 mDNS/USB 的才需要 host 或显式设备映射

---

## 综合分析

### 关键共识
1. **Docker Container 版 = 无 Supervisor 的单容器**：没有 Add-on Store、ha CLI、内置备份；一切伴生服务用独立容器自管
2. **host 网络是 Docker 版 HA 的默认正确选择**：mDNS/SSDP/UPnP 设备发现依赖组播，bridge 会丢
3. **国内拉取 = 镜像名前缀替换**：`daemon.json` 的 registry-mirrors 对 ghcr.io 无效；`ghcr.nju.edu.cn` 与 `ghcr.1ms.run` 是 2026 主要可用源
4. **稳定运行三件套**：锁版本 tag（不用 stable）+ 备份 `/config` 整目录（先停容器）+ 记录旧镜像 ID 便于回滚
5. **HACS 国内使用分两段**：下载/更新可用代理加速；首次 GitHub 授权必须直连

### 时效性标注
- 镜像加速域名（ghcr.1ms.run、ghcr.nju.edu.cn、gh-proxy.com 等）可用性易变，需标注「配置前实测」并给检测方法
- HA 版本号（2026.7.4）为写作时最新稳定，正文应给出「查最新版本」的方法而非写死
- get.hacs.vip（hacs-china 极速版）最后发布 2025-08，可用性待实测；给出官方+极速版双路径

### 需要正文中强调的实战建议
- 教程给出**一份可直接用的完整 docker-compose.yml**（HA + HACS 需要的目录 + 可选 addon 容器），作为全文主线
- 国内加速给「主推 + 备选」双方案，避免单一失效源
- 更新/回滚/备份给出完整命令序列，并强调「升级前备份 + 升级前先更 HACS/custom_components」
