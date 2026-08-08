# 用 Docker 配置 Home Assistant（HA）详细教程 - 探测结果

> 阶段 1 探测式收集产物。4 个方向并行探测完成，以下为汇总与方向菜单。

## 探测概览

| 方向 | 探测问题 | 核心结论 |
|------|---------|---------|
| A. Docker 部署 HA | 官方推荐、compose 形态、国内拉取、vs HAOS | 官方仅支持 HAOS 与 HA Container；Supervised 已弃用；`ghcr.io/...:stable` + host 网络是标准形态；国内需 ghcr 代理前缀 |
| B. HACS 安装与使用 | 是什么、Docker 安装、国内方案、3.x 配置 | Docker 版只能手动放 `custom_components/hacs/`；国内用 get.hacs.vip 极速版或手动 zip + ghproxy |
| C. 国内稳定使用与更新 | 更新流程、镜像加速、版本锁定、回滚、备份 | 稳定更新=手动 pull 固定版本 + 备份 /config 整目录 + 记录旧镜像 ID；ghcr 加速用 `ghcr.1ms.run` 前缀 |
| D. Docker 部署 addon | 无 Store 的替代、addon 容器化、通信、常见坑 | addon 本质是 Docker 容器；用 compose 跑等价容器替代 Store；host 网络 + 正确卷映射是关键 |

---

## 方向 A：Docker 部署 HA

- **部署方式现状**：官方 2026 仅支持 HAOS 与 HA Container；Supervised 2025 已弃用，仅适合熟练用户在 NAS/通用宿主机上用 Docker 跑。
- **官方 docker-compose 形态**：
  - 镜像：`ghcr.io/home-assistant/home-assistant:stable`（Pi5 用 `raspberrypi5-64-homeassistant:stable`）
  - `container_name: homeassistant`、`restart: unless-stopped`
  - `privileged: true` 用于 USB(Zigbee/Z-Wave)/蓝牙直通
  - `network_mode: host`（本地 mDNS/SSDP 设备发现必需；host 下不映射端口；bridge 才用 `ports: "8123:8123"`）
  - 环境变量：`TZ=<时区>`
  - 卷：`./config:/config`、`/etc/localtime:/etc/localtime:ro`、`/run/dbus:/run/dbus:ro`
- **国内拉取 ghcr.io**：`daemon.json` 的 `registry-mirrors` 只加速 Docker Hub，**不加速 ghcr.io**。方案：① ghcr 代理前缀替换（如 `ghcr.1ms.run`）；② 第三方 GHCR 专属加速代理；③ 国内定制版。
- **vs HAOS 核心差异**：单容器、无 Supervisor → 无 Add-on Store、无 ha CLI、无内置备份；`configuration.yaml` 在挂载的 `/config` 卷。
- **config 目录结构**：`configuration.yaml`（含 `default_config:`）、`secrets.yaml`（`!secret` 引用）、`automations.yaml`/`scripts.yaml`/`scenes.yaml`；目录 `custom_components/`、`www/`、`themes/`、`esphome/`。

## 方向 B：HACS 安装与使用

- **HACS 是什么**：社区插件商店，通过 GitHub API 装社区集成、Lovelace 卡片、主题、Python 脚本。Docker 版必装（米家、影音、卡片全靠它）。
- **Docker 版安装**：不能走 HAOS 的加载项商店，二选一：① `docker exec` 进容器执行 `wget -O - https://get.hacs.xyz | bash`；② 宿主机下载 release zip 解压进 `config/custom_components/hacs`。装完必须重启容器。
- **国内方案**：① `get.hacs.vip | bash`（HACS 极速版/hacs-china，走 ghproxy/gitmirror 代理）；② 手动 GitHub release zip + ghproxy 加速直链；③ 自定义 GitHub API 代理（`ghapi.hacs.vip` 等）解决列表加载。
- **HACS 3.x 配置**：Settings → Devices & Services → Add Integration → HACS → GitHub device OAuth（复制 code → github.com/login/device 授权）。注意 YAML 配置已废弃，必须 UI 授权。
- **常用仓库**：卡片 Mushroom Cards/button-card/ApexCharts；集成 Frigate/Adaptive Lighting/Browser Mod/Watchman；主题 Minimalist/Glassmorphism。
- **国内常见坑**：直连 GitHub 下载慢、失败率高；api.github.com 连不上导致列表加载失败；首次 GitHub 授权无法加速，需直连或科学上网。

## 方向 C：国内稳定使用与更新

- **Docker 稳定更新**：容器版无 UI 更新按钮。流程：`docker pull ...:stable` → stop/rm → 同参数重建；升级前先更新 HACS/custom_components 并在旧 Core 上验证。Watchtower 可用但官方标 "Caution"，大版本易破坏集成，建议手动更新或排除关键容器。
- **国内镜像加速**：公共源 2024-2025 陆续关闭；2026 可用 `ghcr.1ms.run` 前缀（免费实测可用）、轩辕专业版专属域名（付费）等。HA 官方镜像在 ghcr.io，必须用 ghcr 代理前缀。
- **版本锁定**：`stable` 是浮动标签；求稳锁具体版本号（如 `2026.7.4`），记录镜像 digest/ID 便于回滚。
- **回滚**：靠旧镜像 ID（`docker inspect --format '{{.Image}}'`），用旧 ID 重建 + 挂载备份的 config。跨大版本逐步升级。
- **兼容问题**：月度更新常引入破坏性变更，custom_components 需插件作者适配，HA 官方不处理自定义组件问题。
- **备份策略**：备份对象是 `/config` 整目录（含隐藏 `.storage`）；备份前停容器；HA 自带 backup 无法在 UI 直接恢复，需手动解压 tar 回填。推荐 3-2-1。

## 方向 D：Docker 部署 addon

- **核心前提**：Docker Container 版无 Supervisor → **没有 Addon Store**。addon 本质就是 Supervisor 拉取并管理的 Docker 容器。替代方案：自己写 `docker-compose.yml` 跑等价容器。「整个 Docker Hub 就是你的 Addon Store」。**HACS 不是替代品**（它是集成/前端商店，不装容器）。
- **addon 容器化要点**：addon 是普通镜像，可直接 docker run；运行时数据放 `/data`；Supervisor 挂载约定 `/config`(rw)、`/share`(rw)、`/ssl`(ro)；无 Supervisor 时 ingress、Supervisor API、自动端口/设备映射失效。
- **常见 addon 容器示例**：Mosquitto(`eclipse-mosquitto:2`, 1883)、Node-RED(`nodered/node-red`, 1880)、ESPHome(`esphome/esphome`, 6052/6123)。HA 用 host 网络保 mDNS/SSDP/ESPHome 发现。
- **社区镜像**：`ghcr.io/hassio-addons/base/amd64` 等基础镜像可直接 pull；官方 `home-assistant/addons` 仓库；国内 `ha-china/hassio-addons`。
- **与 HA 通信**：把 HA 当 MQTT 客户端或走 REST API；host 网络下 `localhost:8123` 可达；MQTT 在 HA 里填 broker 地址 1883。
- **常见坑**：别用 `privileged: true`（应显式 `devices:` 映射 USB，用稳定路径 `/dev/serial/by-id/`）；Zigbee 协调器互斥（ZHA 与 Zigbee2MQTT 只能其一）；Frigate+USB Coral 权限；网络模式需一致（host/bridge 混用导致 MQTT 连不上）。

---

## 方向菜单

基于探测结果，本教程可组织为以下学习方向。请选择（可多选，默认全选）：

| 选项 | 方向 | 说明 |
|------|------|------|
| **A** | Docker 部署 HA 完整实战 | docker run/compose 完整配置、目录映射、网络模式、国内镜像拉取 |
| **B** | HACS 安装与国内使用 | 官方安装 + 国内加速方案 + 3.x 配置 + 常用仓库 + 排障 |
| **C** | 国内稳定使用与更新 | 版本锁定、更新流程、回滚、备份、镜像加速策略 |
| **D** | Docker 部署 addon | 无 Store 替代方案、常见 addon 容器化 compose、与 HA 通信、权限坑 |
