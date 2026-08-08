# 第三章：工程化部署 —— docker-compose 完整配置与三大关键决策

上一章我们用手敲的 `docker run` 把 HA「裸奔」拉了起来：一条长命令里塞满镜像、挂载、网络、时区参数，写错一处或想复现，只能翻 shell 历史。这一章把它升级为一份声明式的 `docker-compose.yml`——版本可控、参数可注释、随时可复现——同时把上线前最容易被坑的三个决策讲透：网络模式、设备直通、国内镜像。

> [!tip] 大白话
> `docker run` 像口头交代一件事，说完就忘；`docker-compose` 像把流程写成 SOP 手册，任何人照着执行都能得到一样的结果。所以「工程化」的第一步，就是把运行参数从命令行搬进 yaml 文件。

## 3.1 一份可直接抄的官方 compose.yaml

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

## 3.2 决策一：网络模式 host vs bridge

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

## 3.3 决策二：设备直通

HA 要接 Zigbee 网关、Z-Wave 棒、ESPHome 烧录器，本质上是让容器访问宿主机的 USB 串口设备。

### 用 by-id 稳定路径，别用 ttyUSB0

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

### 蓝牙（hci0）走 dbus，不走 by-id

蓝牙适配器（hci0）不是串口设备，`/dev/serial/by-id/` 里根本没有它。蓝牙集成需要容器通过宿主机的 D-Bus 系统总线去驱动蓝牙栈，所以 compose 里那行 `/run/dbus:/run/dbus:ro` 不是摆设。另外还需先在宿主机上让蓝牙上线：`bluetoothctl power on`（确保适配器已开启，再启动容器）。

## 3.4 决策三：国内镜像加速——ghcr 前缀替换

`ghcr.io` 是 GitHub 的容器仓库，HA 官方镜像就存在这里。国内拉取最常踩的坑，就是给 Docker 配了加速器却依然拉不动。

### 为什么 registry-mirrors 对 ghcr 无效

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

### 镜像源易变，配置前先实测

这类国内加速域名随时可能挂掉或换地址，正文给的地址在实操前务必实测。最靠谱的方式是用社区维护的检测项目跑一遍（[docker-registry-cn-mirror-test](https://github.com/docker-practice/docker-registry-cn-mirror-test)），或者直接 `docker pull` 一个小镜像试速度。教程的建议是**主推 + 备选**双源都配好，单个失效时不至于卡死。

## 本章小结

- 把 `docker run` 升级为 `docker-compose.yml`：镜像、挂载、网络、设备全部声明化，一条 `docker compose up -d` 即可复现。
- 网络决策：Docker 版 HA 默认用 `network_mode: host`，保住 mDNS/SSDP/UPnP 组播发现；bridge 会丢本地发现，替代方案（macvlan / Avahi / `status_use_ping`）各有代价。
- 设备决策：串口直通用 `/dev/serial/by-id/` 稳定路径 + `group_add` 加 `dialout`/`uucp` 组；`privileged` 只是兜底。蓝牙走 `/run/dbus`，不在 by-id。
- 镜像决策：`registry-mirrors` 对 `ghcr.io` 无效，要用前缀替换（`ghcr.nju.edu.cn` / `ghcr.1ms.run`）；加速域名易变，先实测再上线。

> [!tip] 大白话
> 这一章浓缩成一句话：HA 要「住进宿主网络、用身份证认设备、给 ghcr 换收件地址」。这三件事做对，容器就能长期稳定跑。

HA 本体已经在 compose 的编排下稳定运行了，但一个没有生态的智能家居中枢还只是空壳。下一章我们安装 HACS，给 HA 搬进「应用商店」，装上前端卡片、社区集成和主题。
