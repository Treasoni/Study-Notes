---
title: "第二章：快速起跑 —— docker run 部署与 config 目录结构"
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
chapter: 二
---

# 第二章：快速起跑 —— docker run 部署与 config 目录结构

[[01_为什么是Docker版_部署架构与能力边界.md|← 第一章 · 为什么是 Docker 版]] ｜ [[03_工程化部署_docker-compose完整配置与三大关键决策.md|第三章 · 工程化部署 →]]

[[Docker 部署 Home Assistant 完全指南|← 返回索引]]

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
