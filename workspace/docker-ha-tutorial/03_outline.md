# 学习笔记大纲：《Docker 部署 Home Assistant 完全指南：HACS、国内稳定运行与 Addon 实战》

> 笔记类型：实战教程（practice）
> 学习深度：精通进阶
> 用户基础：有了解（知道 Docker 基本概念，可能装过 HAOS，但不熟 Docker 版 HA）
> 预计总篇幅：约 16000 - 20000 字
> 章节数：9 章
> 输出目标：Obsidian vault `homeassistant/docker-ha/`，拆分多文件（索引页 + 章节）

> 素材引用图例：`A1`-`A7`、`B1`-`B6`、`C1`-`C6`、`D1`-`D6` 分别对应 `02_deep_research.md` 中「方向 A / B / C / D」下的小节序号；`综合分析` 对应文件末尾综合分析节。

---

## 文件拆分建议（Obsidian 多文件）

目标目录 `homeassistant/docker-ha/`：

```
homeassistant/docker-ha/
├── Docker HA 索引.md                 # 索引页：导航 + 核心结论速览 + 与既有笔记互链
├── 01-部署架构与能力边界.md
├── 02-docker-run快速起跑.md
├── 03-docker-compose完整部署.md
├── 04-HACS安装与国内加速.md
├── 05-HACS配置与常用仓库.md
├── 06-版本锁定与镜像加速.md
├── 07-更新回滚与备份.md
├── 08-addon原理与compose部署.md
└── 09-addon通信网络与权限避坑.md
```

索引页聚合：三种部署方式一句话结论、全文主线 compose 文件位置、HACS 国内两段论（下载可加速 / 授权必须直连）、运维三件套口诀，并双链到 `[[Home Assistant 三种部署方式对比与选型]]` 与 `[[部署 HAOS 详细教程]]`。

---

## 第一章：为什么是 Docker 版 —— 部署架构与能力边界

- **篇幅**：短（约 800 - 1000 字）
- **章节目标**：让读者认清 Docker Container 版在 HA 三种部署方式中的定位，明确它与 HAOS / Supervised 的能力差异，建立「缺什么、补什么」的全局观，并给出全文主线（一份贯穿始终的 docker-compose.yml）。
- **覆盖要点**：
  - 三种部署方式横评（HAOS / Supervised / HA Container）与官方推荐逻辑
  - Supervised 已弃用（2025），跑 Portainer/Watchtower 会被标 Unsupported/Unhealthy
  - Container 版能力边界：无 Supervisor → 无 Add-on Store、无 ha CLI、无内置备份；更新/备份/伴生服务全部自管
  - 本教程的主线预览：部署 → HACS → 稳定运维 → addon 补足
- **大白话位**：addon = 容器；Supervisor = 自动安装/卸载/管理容器的「管家」。Docker 版没有管家，你自己当管家。
- **素材引用**：A1、综合分析
- **代码示例**：0
- **过渡思路**：搞清楚定位后，第二章立刻动手用 `docker run` 跑起第一个容器。

---

## 第二章：快速起跑 —— docker run 部署与 config 目录结构

- **篇幅**：中（约 1500 - 2000 字）
- **章节目标**：用官方 `docker run` 命令在几分钟内拉起 HA，理解 `/config` 目录与首次启动机制，为第三章升级为 compose 打底。
- **覆盖要点**：
  - 前置条件：Docker Engine ≥ 23.0.0、仅 Linux（Docker Desktop 不可用）、防火墙放行 8123
  - 官方 `docker run` 命令逐参数拆解（`--privileged`、`--restart`、`TZ`、目录挂载、`--network=host`）
  - `TZ` 必须是 tz database 名称（如 `Asia/Shanghai`），不是 UTC 偏移
  - `/config` 目录结构与「目录完全为空才自动生成 configuration.yaml」的机制与坑
  - `default_config:` 一行加载一批默认集成；`!include` 引用文件缺失会启动进 safe mode
  - UI 管理数据在隐藏 `.storage/`，与 `configuration.yaml` 都必须持久化
  - 启动验证：`docker ps`、`docker logs`、访问 `http://<host>:8123`
- **素材引用**：A2、A3、A7
- **代码示例**：2（docker run 命令、configuration.yaml 默认内容）
- **过渡思路**：跑起来了但只是「裸奔」，第三章升级为工程化 compose 编排并讲透网络、设备、国内镜像三大决策。

---

## 第三章：工程化部署 —— docker-compose 完整配置与三大关键决策

- **篇幅**：长（约 2500 - 3000 字）
- **章节目标**：交付一份可直接用于生产环境的 `docker-compose.yml`，讲透网络模式、设备直通、国内 ghcr 镜像加速三大决策，让读者「抄完就能用」。
- **覆盖要点**：
  - 官方推荐 compose.yaml 全量展示与逐段注释（volumes / privileged / network_mode / TZ）
  - 网络模式：host vs bridge —— 为何 host 是 Docker 版默认正确选择（mDNS/Zeroconf、SSDP/UPnP、DLNA 是组播，bridge/NAT 不转发组播）
  - bridge 替代方案：macvlan / Avahi reflector / ESPHome `status_use_ping: true`
  - 设备直通：`/dev/serial/by-id/` 稳定路径 vs `/dev/ttyUSB0` 漂移；宿主用户加 `dialout`/`uucp` 组；`privileged` 仅兜底
  - 蓝牙（hci0）：不在 by-id，需挂 `/run/dbus:/run/dbus:ro` 并先 `bluetoothctl power on`
  - 国内拉取 ghcr.io：`daemon.json` 的 `registry-mirrors` 对 ghcr 无效的根本原因；镜像名前缀替换 `ghcr.nju.edu.cn` / `ghcr.1ms.run`
  - 镜像源可用性易变：配置前实测 + 检测方法
- **大白话位**：
  - host 网络 = 容器直接「住进」宿主机网络；组播像「小区广播」，必须与设备在同一内网才能收到
  - registry-mirrors = 只给 Docker Hub 做「快递中转站」；ghcr 是另一家快递公司，不经过这个中转站，要改收件地址（前缀替换）
- **素材引用**：A3、A4、A5、A6、C3
- **代码示例**：3（compose.yaml、ghcr 前缀替换 pull 命令、设备映射片段）
- **过渡思路**：HA 本体稳定跑起来了，第四章开始装 HACS 扩展生态。

---

## 第四章：HACS 安装 —— Docker 三种路径与国内加速

- **篇幅**：中（约 1800 - 2200 字）
- **章节目标**：理解 HACS 官方脚本每一步在做什么，掌握 Docker 环境下三种安装路径，并能在国内网络下完成下载安装。
- **覆盖要点**：
  - HACS 是什么（社区应用商店：集成 / 前端卡片 / 主题），Docker 版必装的原因
  - 官方脚本 `get.hacs.xyz` 干了什么：探测含 `.HA_VERSION` 的目录 → 检查 wget/unzip → 下载 hacs.zip → 解压到 `custom_components/hacs/` → 校验 MINIMUM_HA_VERSION
  - Docker 三种安装路径：
    - 路径一：进容器跑官方脚本（`docker exec`）
    - 路径二：宿主机解压到挂载目录
    - 路径三：`docker cp` + 容器内解压
  - 关键约束：文件必须直接落在 `custom_components/hacs/`，不能多一层嵌套；放置后 `docker restart`
  - 国内加速：hacs-china 极速版（get.hacs.vip，注明待实测）、gh-proxy 前缀代理、GitHub API 代理（HACS 3.x「选项」UI 里填，非 configuration.yaml）
  - 镜像源时效性提示（ghproxy.com 已死，用 gh-proxy.com 等替代）
- **大白话位**：
  - HACS = 手机应用商店；官方脚本 = 自动下载并安装 App 的「安装向导」
  - 国内加速 = 给 GitHub 下载加「加速器」；但首次 GitHub 授权绕不开直连
- **素材引用**：B1、B2、B3、B6
- **代码示例**：3（三种安装路径各一段命令）
- **过渡思路**：HACS 装好了，第五章完成首次授权配置，并装一批常用仓库。

---

## 第五章：HACS 首次配置与常用仓库实战

- **篇幅**：中（约 1500 - 1800 字）
- **章节目标**：走通 HACS 3.x 首次配置全流程（含 GitHub Device flow 授权），掌握高频排障，安装常用前端卡片与集成。
- **覆盖要点**：
  - 首次配置流程：清缓存/硬刷新（Ctrl+F5）→ + Add Integration → 勾选声明 → Submit
  - Device flow 授权：复制设备代码 → 开 `github.com/login/device` → 粘贴授权 → 回 HA（代码 15 分钟有效）
  - 国内「两段论」：下载/更新可代理加速；首次授权必须直连 GitHub
  - 高频报错与定位：`Timeout of 20 reached...` = 网络/DNS；列表/token 失败 = api.github.com 被墙；授权转圈 = 需科学上网
  - 常用仓库清单：前端卡片（Mushroom、Mini Media Player、Card Mod）、集成（Xiaomi Miot Auto、browser_mod、Xiaomi Gateway3）、主题（Glassmorphism）
- **大白话位**：Device flow = 用「验证码」让 GitHub 授权 HA 读取社区仓库，类似扫码登录。
- **素材引用**：B4、B5、B6
- **代码示例**：0（以 UI 配置 + 仓库清单为主，仓库清单用表格呈现）
- **过渡思路**：生态就绪，进入「稳定运行」主题 —— 第六章先解决版本与镜像策略。

---

## 第六章：国内稳定运行 —— 版本锁定与镜像加速策略

- **篇幅**：短（约 1200 - 1500 字）
- **章节目标**：建立「锁版本、双镜像源、升级刻意为之」的生产意识，避免 `stable` 浮动标签带来的不确定性。
- **覆盖要点**：
  - `stable` 是浮动标签的风险；固定版本 tag 写法（如 `:2026.7.4`）
  - 查最新版本的方法（GitHub Releases），正文不写死版本号
  - 国内镜像源全景：`ghcr.nju.edu.cn`（主推：免费、免认证、每日同步）、`ghcr.1ms.run`、轩辕付费代理、Docker Hub 公共镜像加速（addon 等用）
  - 生产锁版 compose 写法
  - 镜像源易变：配置前实测 + 检测方法（docker-registry-cn-mirror-test）
- **大白话位**：`stable` = 永远指向「当前最新」的浮动标签，今天能用、明天升级可能带坑；锁版本 = 把车停在固定车位，想升级才手动换车位。
- **素材引用**：C2、C3
- **代码示例**：2（锁版 image 写法、镜像前缀替换 pull）
- **过渡思路**：定了版本策略，第七章进入升级、回滚、备份的运维实操闭环。

---

## 第七章：更新、回滚与备份 —— 运维三件套

- **篇幅**：长（约 2500 - 3000 字）
- **章节目标**：掌握 Docker 版 HA 完整运维闭环：升级前校验 → 升级 → 失败回滚 → 定期备份与恢复，并理解升级兼容风险。
- **覆盖要点**：
  - 更新完整流程：`docker compose pull` + `up -d`；升级前先更新 HACS/custom_components 并在旧版本验证，再动 core 版本
  - 校验命令：`docker exec ... python -m homeassistant --script check_config`
  - Docker 版不要在 HA 界面点「更新」，升级/回滚一律由 Docker 侧完成
  - 回滚完整操作：记录镜像 ID（`docker inspect`）→ 拉旧镜像 → 停删容器 → 旧 tag 重建（保留挂载/network host/TZ/privileged）；compose 改 tag 回滚
  - 数据库不兼容风险：`.storage` 与 `home-assistant_v2.db` 跨大版本可能 schema 不兼容；极端处理删库
  - 备份策略：先停容器再 `tar` 打包 `/config` 整目录（含隐藏 `.storage`、`.cloud`）；3-2-1 落地
  - 恢复：官方 backup.tar 内层解包还原到 config 挂载目录；BackupManager（挂 docker socket）一键恢复
  - 升级兼容风险案例（2026.1 / 2026.4 / 2026.6 / 2026.8 破坏性变更）与降险清单
- **大白话位**：
  - 备份 = 先把门关好再收拾房间（先停容器再打包，避免写冲突）
  - 升级 = 换发动机，先留好旧发动机（记录镜像 ID）才能随时换回来
- **素材引用**：C1、C4、C5、C6
- **代码示例**：6（更新、校验、回滚、备份、恢复、镜像记录命令）
- **过渡思路**：单机 HA 运维闭环完毕，第八章开始用 Docker 补齐「Addon Store」的缺失。

---

## 第八章：Docker 部署 addon —— 把 Docker Hub 变成你的 Addon Store

- **篇幅**：长（约 2500 - 3000 字）
- **章节目标**：理解 addon 本质就是容器镜像，掌握常用 addon（MQTT / Node-RED / ESPHome / Zigbee2MQTT）的 compose 部署与国内镜像替换。
- **覆盖要点**：
  - addon 本质 = 容器镜像（官方文档佐证）；Container 版无 Supervisor → 无 Addon Store，只能手动维护等价容器
  - 替代思路：「整个 Docker Hub 就是你的 Addon Store」；HACS 不是替代品（装集成/前端，不装容器）
  - 官方/社区 addon 镜像命名规则与拉取：`ghcr.io/hassio-addons/<addon>/<arch>:<version>`、`homeassistant/aarch64-addon-mosquitto`
  - 国内 addon 镜像替换：ghcr.io → `ghcr.nju.edu.cn`、docker.io/lscr.io → `docker.1panel.live`、github → gh-proxy
  - 完整 compose 逐段配置：mosquitto（1883 + 9001 WebSocket、目录挂载、配置要点）、Node-RED、ESPHome（host + privileged）、Zigbee2MQTT（devices by-id + depends_on）
  - mosquitto.conf 要点：`listener 1883 0.0.0.0`、匿名/密码认证切换、persistence
- **大白话位**：addon = 容器；Docker 版没有「应用商店的自动安装器」，你自己 `docker compose up` 就是「手动安装 App」；每个 addon 就是一家独立的「家电」，MQTT 是它们共同的「对讲机/局域网通讯协议」。
- **素材引用**：D1、D2、D3
- **代码示例**：4（addon 镜像拉取、完整 compose、mosquitto.conf、国内替换示例）
- **过渡思路**：容器都跑起来了，最后一章解决「它们怎么和 HA 互相通信 + 网络架构怎么设计 + 权限坑怎么避」。

---

## 第九章：addon 与 HA 通信、网络架构与权限避坑

- **篇幅**：中（约 2000 - 2400 字）
- **章节目标**：打通 addon ↔ HA 的通信链路，给出推荐的网络架构设计，并避开设备权限与互斥坑。
- **覆盖要点**：
  - 通信方式对比：Supervisor 环境（`homeassistant_api: true` + `SUPERVISOR_TOKEN`）vs Container 版（手动提供长效 token LLT + Base URL）
  - Node-RED 接入 HA：装 `node-red-contrib-home-assistant-websocket`，取消勾选「Using the Home Assistant addon」，填 Base URL + LLT
  - 地址填法：host 网络下 `http://localhost:8123`；bridge 同网填服务名 `http://homeassistant:8123`；Z2M 的 MQTT 填 `mqtt://172.17.0.1`（docker0 桥 IP）
  - CLI 区别：`hass-cli` 走 HA REST API（可用）；`hassio-cli`/`ha` 走 Supervisor API（不可用）
  - 网络架构推荐：HA 用 host（保住 mDNS/SSDP/UPnP），Mosquitto/Node-RED 用 bridge + 发布端口；全 bridge 方案与 mDNS 中继（mdns-repeater）/ macvlan
  - 权限坑：别全局 `privileged: true`，用显式 `devices:` + `group_add`；USB 用 `/dev/serial/by-id/`；ZHA 与 Z2M 互斥（二选一）；mosquitto 目录权限 chown；Frigate + USB Coral 映射
- **大白话位**：LLT = 一把「长期有效的钥匙」，让容器里的 addon 能调用 HA；`ha` 命令像「管家专属钥匙」，Docker 版没管家，只能用 REST API 这把「访客钥匙」。
- **素材引用**：D4、D5、D6
- **代码示例**：3（LLT 地址填法、网络/设备映射片段、hass-cli 用法）
- **过渡思路**：全文收束，索引页汇总「部署 → HACS → 运维 → addon」四段主线与核心口诀。

---

## 学习路径说明

### 前置要求
- Docker 基本概念：镜像、容器、卷挂载、端口映射（能读懂 `docker run` 命令即可）
- Linux 命令行基础：`wget`、`unzip`、`tar`、`docker exec`、目录权限
- Home Assistant 基础概念：集成、实体、自动化、`configuration.yaml`、前端仪表盘
- 建议先读既有笔记 `[[Home Assistant 三种部署方式对比与选型]]` 了解整体布局

### 学完能做什么
- 用 `docker-compose.yml` 从零部署一套 HA，包含国内镜像加速、设备直通、蓝牙可用
- 独立安装 HACS，并在国内网络下完成 GitHub 授权与常用卡片/集成安装
- 建立「锁版本 + 双镜像源 + 备份 + 回滚」的稳定运维闭环
- 用 Docker 部署 MQTT / Node-RED / ESPHome / Zigbee2MQTT 等 addon 等价容器，并与 HA 打通通信
- 能识别并规避 Docker 版 HA 的经典坑（host 网络、ghcr 加速、设备权限、ZHA 互斥）

### 建议学习顺序
- 必读主线（部署到运维闭环）：第 1 → 2 → 3 → 4 → 5 → 6 → 7 章，逐章实操
- 可选进阶（addon 生态）：第 8 → 9 章，按实际需求（是否要 MQTT/自动化/固件刷写）选读
- 单章阅读约 30 - 60 分钟，含实操完整走一遍约 1 - 2 天
- 国内镜像域名可用性易变，正文给出的加速地址在实操前先用检测方法实测
