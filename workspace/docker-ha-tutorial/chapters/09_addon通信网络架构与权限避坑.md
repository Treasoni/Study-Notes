# 第九章：addon 与 HA 通信、网络架构与权限避坑

上一章我们把 Mosquitto、Node-RED、ESPHome、Zigbee2MQTT 这些 addon 等价容器一个个跑了起来，但它们和 Home Assistant 是彼此独立的容器。如果只让容器「跑起来」而不会「互相通信」，它们就是一座座孤岛。这一章收掉三个关键问题：addon 怎么调用 HA 的接口、网络拓扑怎么设计最稳、设备权限与互斥有哪些坑要躲。

## 一、先认钥匙：LLT + Base URL 是 Docker 版的通信方式

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

## 二、Node-RED 接入 HA：勾掉 addon 选项，填 LLT

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

## 三、hass-cli 与 ha：访客钥匙 vs 管家钥匙

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

## 四、推荐网络架构：HA 用 host 保发现，服务用 bridge 保整洁

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

## 五、权限与互斥避坑清单

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

## 总结：从零到一套完整 HA 体系的回顾与进阶

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
