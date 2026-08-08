# 从零开发 Home Assistant 自定义集成（custom integration）

本笔记带你在已有 Home Assistant 使用基础上，从零动手开发一个可运行、可 HACS 分发的自定义集成（custom integration）。内容覆盖开发环境搭建、集成骨架与 manifest.json、Config Flow 配置流程、Sensor 实体、DataUpdateCoordinator 数据轮询、测试调试与 HACS 分发，最后附一份常见坑与最佳实践手册。适合用过 HA、会基础 Python 与 async/await、想亲手写出第一个自定义集成的读者，按章节顺序阅读即可走通「从零到可分发」的完整链路。

## 目录

1. [第 1 章：认识 Home Assistant 自定义集成](#第1章认识-home-assistant-自定义集成)
2. [第 2 章：开发环境搭建](#第2章开发环境搭建)
3. [第 3 章：集成骨架与 manifest.json](#第3章集成骨架与-manifestjson)
4. [第 4 章：Config Flow 配置流程](#第4章-config-flow-配置流程)
5. [第 5 章：Entity 平台与 Sensor 实体](#第5章-entity-平台与-sensor-实体)
6. [第 6 章：DataUpdateCoordinator 数据轮询](#第6章-dataupdatecoordinator-数据轮询)
7. [第 7 章：测试与调试](#第7章测试与调试)
8. [第 8 章：HACS 分发](#第8章-hacs-分发)
9. [第 9 章：常见坑与最佳实践](#第9章常见坑与最佳实践)

---

# 第 1 章：认识 Home Assistant 自定义集成

在写任何代码之前，先搞清楚我们要做的东西到底是什么。本章回答几个前置问题：什么是自定义集成？它和内置集成有什么区别？它住在哪？以及这本笔记会带你走到哪。看完你就有了整体地图，后面每一章只是把这张地图一步步走通。

## 什么是自定义集成

Home Assistant（HA）本身是一个**自动化中枢**，但它的能力大多由「集成」提供。集成负责把某个设备、服务或数据源接进 HA——例如把灯、传感器、天气服务或某个云端 API 变成 HA 里可操作、可自动化的对象。

**自定义集成（custom integration）** 就是由社区或个人开发者编写、不在 HA 官方发行包里的集成。它与内置集成的区别，主要在「来源」和「位置」上：

| 对比项 | 内置集成（built-in） | 自定义集成（custom） |
|--------|---------------------|---------------------|
| 代码位置 | `homeassistant/components/<domain>/` | `custom_components/<domain>/` |
| 维护方 | HA 官方核心团队 | 社区 / 个人开发者 |
| 随 HA 更新 | 是，随版本发布 | 否，需自行更新 |
| 典型示例 | mobile_app、esphome [manifest 官方文档](https://developers.home-assistant.io/docs/creating_integration_manifest/) | 各类第三方插件 |

## custom_components 的生态位置

HA 启动时会加载所有「已配置」的集成，无论它是内置还是自定义。加载路径完全由目录名决定：**目录名即 domain**，例如 `custom_components/my_weather/` 里的集成，domain 就是 `my_weather` [文件结构官方文档](https://developers.home-assistant.io/docs/creating_integration_file_structure/)。domain 是一个唯一标识符，也是后续配置、实体、状态都依赖的「身份证号」。

一个自定义集成的最小文件集只有两个：`manifest.json`（元信息）和 `__init__.py`（入口逻辑）[文件结构官方文档](https://developers.home-assistant.io/docs/creating_integration_file_structure/)。它们各自的作用，我们到第 3 章再逐个拆解。

> [!tip] 大白话：把 HA 想成一家公司
> 内置集成是「正式员工」，住在总部大楼 `homeassistant/components/`；自定义集成是「外聘员工」，住在另一栋楼 `custom_components/`。两边工牌不同、工位不同，但都在为公司干活。所以自定义集成和内置集成能力对等，只是"居住地"不同——也因此，外聘员工需要随身带一张更齐全的「入职登记表」（`manifest.json`），好让公司知道你是谁、要找谁、需要装什么依赖。

## 本笔记的学习路径

这是一份**实战笔记**，目标是照着写完一个**可运行、可 HACS 分发**的最小集成。全文按九章递进：

| 阶段 | 章节 | 内容 |
|------|------|------|
| 打基础 | 第 1-2 章 | 理解概念 + 搭好开发环境 |
| 写骨架 | 第 3 章 | 集成骨架与 manifest.json |
| 接配置 | 第 4 章 | Config Flow 配置流程 |
| 接数据 | 第 5-6 章 | Sensor 实体 + DataUpdateCoordinator（核心） |
| 提质量 | 第 7 章 | 测试与调试 |
| 上架分发 | 第 8 章 | HACS 分发 |
| 避坑 | 第 9 章 | 常见坑与最佳实践 |

> [!note] 跟着主线走
> 建议按「第 5 章 → 第 6 章」顺序阅读，先学会实体怎么写，再接入数据轮询；第 4、6 章是本笔记两处重点，值得放慢速度。

## 最终成品预览

学完这本笔记，你会交付一个这样的最小集成：

- **Config Flow**：用户在「设置 → 设备与服务」里填表单完成配置
- **Sensor 实体**：暴露 1-2 个传感器
- **DataUpdateCoordinator**：统一轮询一个外部 API，多个实体共享数据
- **HACS 分发**：别人能通过 HACS 一键安装你的集成

它的目录结构大致是这样（只是预览，细节后面各章逐一展开）：

```text
custom_components/
└── my_weather/          ← 目录名即 domain
    ├── manifest.json    ← 入职登记表（元信息）
    ├── __init__.py      ← 集成入口
    ├── config_flow.py   ← 配置流程
    ├── coordinator.py   ← 数据统一轮询
    └── sensor.py        ← 传感器实体
```

## 范围边界

本笔记聚焦「**开发集成**」本身。HA 的安装部署、日常使用、命令操作等内容，已分别收录在本库其他笔记中（HAOS 部署、部署方式对比、ha 命令使用、AI 智能家居一键部署），这里不重复展开。如果你对「怎么把 HA 跑起来」还不熟，建议先回去看那几篇，再来上手开发。

---

## 本章小结

- 自定义集成是独立于 HA 官方发行包的集成，能力与内置集成对等，区别主要在代码位置和维护方。
- 自定义集成住在 `custom_components/<domain>/`，**目录名即 domain**；最小文件集是 `manifest.json` + `__init__.py`。
- 本笔记是实战笔记，主线为：搭环境 → 骨架与 manifest → Config Flow → Sensor 实体 → Coordinator → 测试调试 → HACS 分发 → 排错。
- 最终成品是一个带 config flow + sensor + coordinator + HACS 分发的最小集成。
- 本章之后，每个核心概念都会配一个 `[!tip] 大白话` 类比，方便零基础也能看懂。

**下一章**，我们动手把开发环境搭起来：用官方推荐的 VS Code Dev Container 一键起一个带断点调试的 HA 开发环境，为第 3 章写第一个集成骨架做准备。

---

# 第 2 章：开发环境搭建

第 1 章我们认识了自定义集成住在哪（`custom_components/<domain>`）、成品长什么样（一个带 config flow + sensor + coordinator 的最小集成）。但「看懂了图纸」和「真能动手焊」之间还差一套顺手的工具链。这一章的目标很具体：**搭好一个能跑起 HA 源码、改代码立刻生效、还能下断点调试的开发环境**，并用官方脚手架生成你的第一个集成骨架。

动手前先想清楚一件事：HA 本身是个大型 Python 项目，你的集成要跑在它里面。开发环境不能只是「装个 Python 解释器」，还得把 HA 源码克隆下来、装齐依赖、能一键启动、能热调试。官方推荐的新手路径是 **VS Code Dev Container**，我们从头走一遍。[官方开发环境文档](https://developers.home-assistant.io/docs/development_environment/)

## 2.1 官方推荐：VS Code Dev Container 一键工位

> [!tip] 大白话
> 把 Dev Container 想成「装修公司给你装好所有工具的全新工位」——电钻、螺丝刀、安全帽、插座都摆好了，你刷卡进门就能开工。所以，第一次构建后你打开容器就能直接跑 HA、下断点，不用自己装 Python、pip 依赖和各种编译工具。

具体流程一共五步：

1. **Fork 仓库**：在 GitHub 上把 `home-assistant/core` fork 到自己的账号下（后续改动都推到你自己的 fork，方便以后提 PR）。
2. **Clone + 打开**：`git clone <你的 fork 地址>` 后执行 `code .`，用 VS Code 打开目录。
3. **Reopen in Container**：VS Code 检测到根目录有 `devcontainer.json`，右下角会弹出「Reopen in Container」。点它，首次构建要拉镜像、装依赖，通常需要几分钟，之后秒开。
4. **跑起 HA**：容器就绪后打开底部任务面板，选 **Run Home Assistant Core**，HA 会以开发模式启动。
5. **验证 + 调试**：浏览器访问 `http://localhost:8123` 看到 HA 界面即成功；在 Python 代码里打断点后按 **F5**，VS Code 会直接以「调试」方式重新拉起 HA——断点命中时整个 HA 暂停，可单步、看变量。

如果你在 **Windows** 上，还需要一个前置：装好 **WSL2**，并在 WSL 发行版里编辑 `/etc/wsl.conf` 写入 `systemd=true`，然后执行 `wsl --shutdown` 重启 WSL 生效（macOS 用户则直接装 Docker Desktop 即可）。Dev Container 实际跑在 Docker 里，WSL2 正是 Windows 上承载 Docker 的底层，不配好 systemd 容器起不来。

## 2.2 devcontainer 配置里到底藏了什么

官方仓库根目录的 `devcontainer.json` + `Dockerfile.dev` 已经把这些都配好了，你不需要自己写。但了解它们能帮你排查问题。下面是简化后的示意，与你 clone 到的现行版本结构一致：

```json
{
  "name": "home-assistant-core-dev",
  "dockerFile": "Dockerfile.dev",
  "appPort": ["8123:8123", "5683:5683/udp"],
  "postCreateCommand": "script/setup",
  "postStartCommand": "script/bootstrap",
  "containerEnv": {
    "PYTHONASYNCIODEBUG": "1"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "charliermarsh.ruff",
        "ms-python.pylint",
        "ms-python.vscode-pylance",
        "redhat.vscode-yaml",
        "esbenp.prettier-vscode",
        "github.vscode-pull-request-github",
        "github.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": "~/.local/ha-venv/bin/python"
      }
    }
  }
}
```

几个要点：

- **`appPort` 把容器内的 8123 映射到宿主机**，所以你浏览器访问 `localhost:8123` 就能看到 HA；`5683/udp` 是给 Shelly 设备发现预留的。
- **`postCreateCommand` / `postStartCommand`** 分别执行 `script/setup` 和 `script/bootstrap` 自动装依赖。依赖装在哪？`Dockerfile.dev` 基于 `vscode/devcontainers/base:debian`，会先用 apt 装 ffmpeg、bluez、libudev-dev、libpcap-dev、libturbojpeg0 等系统库，再用 `uv` 建一个 Python venv，把 `requirements.txt`、`requirements_test.txt`（pytest）、`requirements_test_pre_commit.txt`（Ruff/mypy）全装进去。
- **默认解释器是 `~/.local/ha-venv`**：VS Code 里的「选择解释器」直接指向它，写代码时自动补全、类型检查用的都是这套环境。
- **预装扩展**：Ruff、pylint、Pylance、yaml、prettier、GitHub PR、Copilot——覆盖了 HA 的 lint 规范、YAML 格式和 Git 协作。
- **`PYTHONASYNCIODEBUG=1`**：让 asyncio 开启调试模式，更容易暴露事件循环被阻塞的问题（第 9 章会细讲）。

> [!warning] 坑：Mosquitto 不是预装项
> 很多旧教程把「本地 Mosquitto MQTT broker」列为 devcontainer 预装项，但**现行 `devcontainer.json` / `Dockerfile.dev` 里并没有它**。如果你要开发 MQTT 相关功能，得自己 `apt install mosquitto` 或另起一个 MQTT 容器，别照抄旧教程。

## 2.3 本地 venv：不依赖 Docker 的替代方案

不想用 Docker 也没关系，官方同样支持纯手动方案：

```bash
# 1. 克隆 core 仓库
git clone https://github.com/home-assistant/core.git home-assistant-core
cd home-assistant-core
# 2. 初始化开发环境（装依赖、建 venv）
script/setup
# 3. 激活虚拟环境并启动 HA（-c 指定开发配置目录）
source .venv/bin/activate
hass -c config
```

> [!tip] 大白话
> 把本地 venv 想成「在自己家里手动搭工位」——工具得自己一件件买、自己排线，但排好之后想怎么改都自由，还能把 U 盘（USB 设备）直接插上。所以它重启快、能直通硬件，代价是首次配置要手动、环境一致性差。

`hass -c config` 里的 `-c` 指定开发配置目录：`config` 是 core 检出目录下一个供开发用的配置目录，你需要先建好它并放一份 `configuration.yaml`。两种方案怎么选，看这张表：

| 维度 | Dev Container | 本地 venv |
|------|---------------|-----------|
| 环境一致性 | 高（镜像即环境，团队一致） | 低（依赖本机 Python/系统库） |
| 首次搭建成本 | 低（一键，但要拉镜像） | 中（要手动装系统库） |
| 重启速度 | 较慢（整容器重启） | 快（本地进程重启） |
| 硬件直通 | Windows/macOS 容器难直通 | 好（USB / Zigbee / 蓝牙） |
| 断点调试 | F5 即用，零配置 | 需要自己配 debugpy |

一句话：**新手和追求「开箱即用」选 Dev Container；要频繁重启迭代、或需要直通 USB/Zigbee/蓝牙硬件的场景，本地 venv 更顺手。** 官方对新手的默认推荐是 Dev Container。

## 2.4 官方脚手架：一键生成集成骨架

环境跑通后，别从空文件开始手敲目录结构——官方提供了脚手架：

```bash
# 在 core 检出目录内运行
python3 -m script.scaffold integration
```

> [!tip] 大白话
> 把脚手架想成「装修公司给的毛坯房图纸」——你不用从一块空地开始画，图纸直接标好了哪面墙在哪、哪里留插座。所以运行一条命令，`custom_components/<domain>/` 下的标准骨架就自动生成，你只需往里填内容。

按提示输入 domain、集成名等信息后，它会按 [官方文件结构约定](https://developers.home-assistant.io/docs/creating_integration_file_structure/) 生成一组标准文件：

- `__init__.py`：含 `async_setup` 骨架和 `CONFIG_SCHEMA`
- `const.py`：`DOMAIN` 常量
- `manifest.json`：含 `quality_scale` 字段
- `quality_scale.yaml` + `tests/` 测试目录
- 如果选了 config flow，还会追加 `config_flow.py` + `strings.json` 并更新 manifest

配合 `hass -c config` 的社区实操链路是这样：先用 `hass -c config` 确认环境能跑 → 运行 scaffold 生成骨架 → `mkdir /config/custom_components` → 把生成的整个 `<domain>` 目录拷进去 → 在 `manifest.json` 里补 `"version": "0.0.1"` → 重启 HA，在「设置 → 设备与服务」里就能看到你的集成。

## 本章小结

- 官方推荐用 **VS Code Dev Container** 开发自定义集成：fork core → clone → Reopen in Container → 任务面板跑起 HA → F5 断点调试；Windows 用户需先配好 WSL2 + `systemd=true`。
- devcontainer 真实配置里值得记住的几件事：`appPort` 映射 8123、默认解释器 `~/.local/ha-venv`、预装 Ruff/pylint/Pylance/yaml/prettier 等扩展、`PYTHONASYNCIODEBUG=1`。
- 本地 venv 是可行替代：重启快、硬件直通好，但环境一致性差；按场景对照表选型。
- 官方脚手架 `python3 -m script.scaffold integration` 一键生成骨架，省去手敲目录结构。
- ⚠️ Mosquitto **不是**现行 core dev 镜像的预装项，开发 MQTT 功能要自己装，别照抄旧教程。

环境就绪、骨架到手，下一章我们拆开这个骨架的第一块核心：**集成骨架与 manifest.json**——搞清楚 `custom_components/<domain>` 里每个文件的作用，以及那张「入职登记表」里的字段到底该怎么填。

---

# 第 3 章：集成骨架与 manifest.json

上一章我们已经用 Dev Container 搭好了开发环境，能跑起 `localhost:8123` 的 HA，也学会了用官方脚手架 `python3 -m script.scaffold integration` 生成骨架。但脚手架背后到底生成了什么？为什么 HA 能认出你的集成？答案都藏在这一章：**目录结构 + manifest.json**。这一章我们会手写一个能被 HA 加载的最小集成骨架，并逐一读懂 manifest 里每个字段的含义。学完你就能亲手写出合法且能加载的集成骨架。

## 3.1 目录结构：`custom_components/<domain>`，目录名即 domain

所有自定义集成都放在配置目录的 `custom_components/` 下，每个集成独占一个子目录。HA 内置集成在 `homeassistant/components/<domain>`，自定义集成则在 `custom_components/<domain>`，两者的**目录名都等于集成标识符 domain**。HA 加载时只看目录名，不看别的东西。[官方文件结构文档](https://developers.home-assistant.io/docs/creating_integration_file_structure/)

> [!tip] 大白话
> 把 HA 比作一家公司：`custom_components/` 是外聘员工的工位区，你的集成是来入职的「外聘员工」。工位区里每个人的工位牌上写什么名字，公司就认为你是谁——所以**目录名（domain）必须和你在档案里填的名字完全一致**，写错一个字就找不到人。

最小文件集只需要两个文件：

```
custom_components/
└── hello_world/
    ├── manifest.json     # 员工档案（必备）
    └── __init__.py       # 入职后的第一个动作（必备）
```

但随着集成变大，把所有代码塞进 `__init__.py` 会难以维护。HA 支持按平台拆文件，以下是常见组织方式：

| 文件 | 职责 |
|------|------|
| `manifest.json` | 集成元信息：身份、依赖、版本、发现声明 |
| `__init__.py` | 集成入口：`async_setup` / `async_setup_entry` |
| `config_flow.py` | 配置流程（第 4 章） |
| `sensor.py` / `binary_sensor.py` / `light.py` | 每类实体一个文件（第 5 章） |
| `coordinator.py` | 数据轮询协调器（第 6 章） |
| `const.py` | 常量，如 `DOMAIN`、配置键名 |
| `services.yaml` | 声明自定义服务参数 |
| `strings.json` | 前端文案（配合 config flow） |

官方脚手架 `python3 -m script.scaffold integration`（第 2 章提过）生成的就是这套按职责拆分的骨架：`__init__.py`（含 `async_setup` + `CONFIG_SCHEMA`）、`const.py`（放 `DOMAIN` 常量）、`manifest.json`（含 `quality_scale`）、`quality_scale.yaml` 和 `tests/` 目录；若勾选 config flow，还会追加 `config_flow.py` + `strings.json`。对照上表你会发现，脚手架默认产物正好对应了「入口 + 常量 + 元信息 + 测试」的最小分工。

> 官方示例仓库 [home-assistant/example-custom-config](https://github.com/home-assistant/example-custom-config) 的 `example_sensor` 只有 `manifest.json + __init__.py + sensor.py` 三个文件；更完整的 `detailed_hello_world_push` 则拆出了 `config_flow.py`、`const.py`、`hub.py`、`sensor.py` 等。先记住「按平台拆分」这个原则即可，具体文件第 4-6 章逐个补上。

## 3.2 manifest.json：集成的「入职登记表」

`manifest.json` 是整个集成的元信息文件，HA 在加载任何代码**之前**先读它，用来决定：这个集成叫什么、由谁维护、依赖什么、适合怎么发现。字段定义见[官方 manifest 文档](https://developers.home-assistant.io/docs/creating_integration_manifest/)。先看一份完整的最小清单：

```json
{
  "domain": "hello_world",
  "name": "Hello World",
  "version": "0.1.0",
  "codeowners": ["@your_github_name"],
  "requirements": ["pyhello==0.3.1"],
  "iot_class": "local_polling",
  "integration_type": "hub",
  "documentation": "https://github.com/your_github_name/home-assistant-hello_world",
  "issue_tracker": "https://github.com/your_github_name/home-assistant-hello_world/issues"
}
```

> [!tip] 大白话
> manifest.json 就是一张**入职登记表 / 员工身份证**。HR（HA 核心）在让你干活前，先验明正身：工号是什么、叫什么、谁担保的、需要配什么工具、属于什么岗位。表上任何一项填错或缺失，都可能导致入职失败（集成无法加载）。

逐字段看核心项：

- **`domain`**：唯一标识，小写下划线，**不可改**，且必须与目录名一致。它是集成在 HA 内的「身份证号」。
- **`name`**：集成显示名，用户在前端看到的名称。
- **`version`**：自定义集成（含覆盖内置集成）**必填**，格式需符合 AwesomeVersion（CalVer 或 SemVer，如 `2026.8.1` 或 `0.1.0`）；内置 core 集成省略该字段。HACS 分发时也靠它对比版本。
- **`codeowners`**：GitHub 维护者列表，格式 `@user`，用于收到 issue/PR 通知。
- **`requirements`**：集成依赖的 PyPI 包，用 pip 兼容字符串，官方示例一律 **`==` 固定版本**。安装失败会导致集成加载失败。不固定版本会带来「环境漂移」——同一份集成在不同时间安装的依赖可能不同，问题难以复现，所以官方与 HACS 生态都要求写死版本。
- **`iot_class`**：设备联网方式，六选一：`assumed_state` / `cloud_polling` / `cloud_push` / `local_polling` / `local_push` / `calculated`。它只用于文档说明，告诉用户数据从哪里来。
- **`integration_type`**：集成类型，八选一：`device` / `entity` / `hardware` / `helper` / `hub` / `service` / `system` / `virtual`，**未设置时默认 `hub`**。
- **`config_flow`**：布尔值，声明集成用 config flow 配置（第 4 章核心，此处先知道有这字段）。

> [!tip] 大白话
> `domain` 就是**唯一工号**：小写下划线、一辈子不改。公司里可以有两个都叫「张三」的人，但工号绝不能重复。HA 用 `domain` 区分每个集成，目录名 = 工号，改一个字符就是另一个「人」了。

> [!tip] 大白话
> `version` 是**必填的版本号**。外聘员工没有「正式编制」，必须自己登记版本，HA 才能判断你有没有更新、要不要重装。格式必须规范（SemVer 如 `0.1.0` 或 CalVer 如 `2026.8.1`），否则校验直接失败。

其中 `integration_type` 的 `hub` / `service` / `device` 语义差别值得记一下，后面选型会用：

| 值 | 含义 | 典型例子 |
|------|------|---------|
| `hub` | 一个中枢网关管理多设备 | Hue、Zigbee 网关 |
| `service` | 每个配置条目连一个外部服务 | AdGuard、Plex |
| `device` | 每个配置条目对应单一物理设备 | ESPHome |
| `virtual` | 仅含 manifest 无代码，通过 `supported_by` 指向真实实现 | 虚拟集成（2022.11 引入） |

## 3.3 `dependencies` 硬依赖 vs `after_dependencies` 软依赖

两个字段都声明「本集成和别的集成有关」，但强度不同：

| 字段 | 语义 | 加载顺序 |
|------|------|---------|
| `dependencies` | **硬依赖**：所列集成必须先加载成功，本集成才会尝试加载 | 严格先于本集成 |
| `after_dependencies` | **软依赖**：优先在所列集成之后加载，但对方没加载/加载失败也不阻塞本集成 | 尽量靠后，非必需 |

> 真实例子：内置 `mobile_app` 的 `dependencies` 声明了 `http` / `webhook` / `websocket_api`——这些是它的硬前置，缺一个就起不来。

## 3.4 自动发现字段（点到即可）

HA 支持通过局域网协议自动发现设备/服务，对应的 manifest 字段只需声明「我认得这些广播特征」，不用写实现代码，发现逻辑由 HA 核心处理：

| 字段 | 发现方式 |
|------|---------|
| `zeroconf` | mDNS 服务类型（如 `_esphomelib._tcp.local.`） |
| `dhcp` | DHCP 报文特征（`registered_devices: true` 等） |
| `bluetooth` | 蓝牙广播特征 |
| `mqtt` | MQTT 主题（如 `esphome/discover/#`） |
| `ssdp` | UPnP/SSDP 设备描述 |
| `homekit` | HomeKit 配对广播 |
| `usb` | USB 设备 VID/PID |

这些字段的完整写法第 9 章排错时再展开，现在知道「HA 靠这几个键认得你的设备」即可。

## 3.5 configuration.yaml 加载与 CONFIG_SCHEMA

在没有 config flow 的最简骨架里，集成可以通过 `configuration.yaml` 加载：把 `domain` 作为顶层键写进 YAML，HA 发现后会调用 `__init__.py` 里的 `async_setup`：

```yaml
# configuration.yaml
hello_world:
  host: 192.168.1.100
```

配套的 `__init__.py` 最小骨架：

```python
"""Hello World integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

DOMAIN = "hello_world"

# 配置先经 voluptuous 校验转换，再交给集成
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required("host"): cv.string,
                vol.Optional("port", default=8080): cv.port,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """通过 YAML 加载时的入口（最简骨架验证用）。"""
    hass.data.setdefault(DOMAIN, {})
    return True
```

这里 `CONFIG_SCHEMA` 用 voluptuous 定义校验规则：`Required` 必填、`Optional` 可选带默认值，配置合法后才会传给集成。需要说明的是：**ADR-0007 / ADR-0010 已禁止新集成使用「平台键」YAML**。所谓「平台键」指老式写法把 `platform: xxx` 塞进 `sensor:` 之类顶层键下、一个集成管多个平台的模式，架构混乱且难以演进。设备和集成类新项目应一律走 config flow（第 4 章）；上面的 YAML 加载方式只用来在本章验证骨架能被 HA 识别加载，正式开发会改用 `async_setup_entry`，骨架也将大不一样。

> 验证方法：把 `hello_world/` 整个目录拷进 `/config/custom_components/`，确认 manifest 有 `"version": "0.1.0"`，重启 HA。加载成功后 `home-assistant.log` 无报错；若有报错，检查 `domain` 与目录名是否一致（这是最常见翻车点）。

## 3.6 真实 manifest 参考

看两个内置集成的高质量 manifest，验证上面讲到的字段在真实世界长什么样：

| 字段 | `mobile_app` | `esphome` |
|------|-------------|-----------|
| `integration_type` | `device` | `hub` |
| `iot_class` | `local_push` | `local_push` |
| `config_flow` | `true` | `true` |
| `dependencies` | `http` / `webhook` / `websocket_api` | 无 |
| `requirements` | `PyNaCl==1.6.2` | 三个依赖包全部 `==` 固定 |
| 发现字段 | 无 | `zeroconf: _esphomelib._tcp.local.`、`mqtt: esphome/discover/#`、`dhcp: registered_devices: true` |
| `version` | 无（内置集成省略） | 无（内置集成省略） |
| `quality_scale` | 无 | `platinum` |

两个要点：一是内置集成**不写 `version`**，但自定义集成必须写（HACS 分发依赖它）；二是 esphome 展示了发现字段与 `quality_scale` 的用法，`quality_scale` 标记集成质量等级，官方高质量集成会带 `platinum` 之类的评分。以上内容对齐 home-assistant/core 仓库中 `mobile_app` 与 `esphome` 两个集成真实的 `manifest.json`。

## 本章小结

- `custom_components/<domain>/` 是自定义集成的家，**目录名即 domain**，两者必须完全一致。
- 最小文件集是 `manifest.json + __init__.py`；功能增长后按平台拆成 `sensor.py`、`coordinator.py`、`const.py`、`services.yaml` 等。
- manifest 核心字段：`domain`（唯一、小写下划线、不可改）、`name`、`version`（自定义集成必填，AwesomeVersion 兼容）、`codeowners`、`requirements`（固定 `==` 版本）、`iot_class`（六值）、`integration_type`（八值，默认 `hub`）。
- `dependencies` 是硬依赖（必须在前），`after_dependencies` 是软依赖（尽量在前、不阻塞）。
- 自动发现字段有 `zeroconf` / `dhcp` / `bluetooth` / `mqtt` / `ssdp` / `homekit` / `usb`，只需声明特征。
- 最简骨架可经 `configuration.yaml` 顶层键 + `CONFIG_SCHEMA` 加载，但新集成应走 config flow（ADR-0007/0010）。

下一章，我们把「员工档案」真正变成「能发门禁卡」的集成：进入 Config Flow 配置流程，让用户通过表单完成配置，HA 据此生成 config entry——这是大多数现代集成真正的入口。

---

# 第 4 章：Config Flow 配置流程

第 3 章我们把 `manifest.json` 骨架和 `__init__.py` 搭好了，集成能被 HA 识别并加载。但现在的它还是一个「哑配置」集成——用户只能靠 `configuration.yaml` 写死配置。这一章我们用 Config Flow（配置流程）给它装上「设置界面」：用户在「设置 → 设备与服务 → 添加集成」里填写表单，HA 校验通过后生成一条 config entry，整个集成才真正可配置、可复用。为什么这章值得放慢速度？因为**表单 + 异常映射 + 唯一性**这三件事，是后续每一章（设备接入、数据轮询、测试）的地基。

> [!tip] 大白话
> 把 Config Flow 想成「门禁卡申请流程」。用户填一张申请表（表单），系统校验信息没问题后，发一张门禁卡（config entry）。这张卡就是 HA 记住「这个集成在这台设备上配置过」的凭证——以后每次加载都靠它。没有这张卡，集成就只是个「能加载但没法被用户配置」的空壳。

## 4.1 让 config flow 生效：两处开关

Config flow 不是魔法，它需要两处配合才能被 HA 唤起：

1. `manifest.json` 里加一行 `"config_flow": true`，告诉 HA「我这个集成支持 UI 配置」。
2. 新增 `custom_components/<domain>/config_flow.py`，在里面定义一个继承 `ConfigFlow` 的类，并把类属性 `domain` 指向我们的 `DOMAIN`。

目录结构上，它和其他文件平级：

```text
custom_components/hello_world/
├── __init__.py
├── const.py
├── config_flow.py   # 本章主角
├── manifest.json
└── strings.json
```

### 最小 config_flow.py 骨架

```python
from homeassistant import config_entries

from .const import DOMAIN


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    MINOR_VERSION = 1
```

几个关键点：

- **`config_entries.ConfigFlow` 是基类**：HA 在「设置 → 设备与服务 → 添加集成」里点到你的集成时，会实例化这个类，然后调用它的各个 `async_step_*` 方法。你写的不是「按钮点击逻辑」，而是「每一步显示什么表单、填完怎么处理」的声明。
- **`domain = DOMAIN`**：把流程绑定到你的集成 domain，与 manifest 的 `domain`、目录名三方必须一致。
- **`VERSION` / `MINOR_VERSION`**：默认都是 1。`VERSION` 是配置数据结构的主版本，当你的集成升级导致 `data` 结构不兼容时，把主版本 +1 并实现 `async_migrate_entry` 做迁移；`MINOR_VERSION` 是较新 HA 引入的次版本号，用于不破坏兼容的小改动。上手阶段记住「有这两个属性、保持默认」即可。

> [!note] 素材对齐
> 官方脚手架 `python3 -m script.scaffold integration` 选 config flow 时，会自动生成 `config_flow.py` + `strings.json` 并改写 manifest——正好就是我们这一章要写的三个文件 [官方开发环境文档](https://developers.home-assistant.io/docs/development_environment/)。

## 4.2 async_step_user：表单流程的两段式

`async_step_user` 是用户进入流程后看到的**第一个步骤**（step）。它的写法遵循一个「两段式」套路：

- **第一次进入**：`user_input` 为 `None`，此时只是**展示表单**，调用 `async_show_form`。
- **用户填完提交**：`user_input` 带着数据进来，此时**校验 + 建条目**，成功则 `async_create_entry`，失败则带着 `errors` 重新 `async_show_form`。

表单用什么描述？**voluptuous schema**（HA 内部大量使用的 Python 校验库，惯例别名 `vol`）。它声明「这个表单有哪些字段、哪些必填、什么类型」。

官方示例 `detailed_hello_world_push` 的表单就是这个模式（稍作裁剪以便聚焦）：

```python
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CannotConnect(HomeAssistantError):
    """无法连接到设备时抛出。"""


class InvalidHost(HomeAssistantError):
    """主机地址非法时抛出。"""


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass, data):
    """真正去连一次设备，连不上就抛自定义异常。"""
    if not looks_like_hostname(data[CONF_HOST]):  # 示意性检查
        raise InvalidHost
    hub = YourHubClass(hass, data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD])
    if not await hub.authenticate():
        raise CannotConnect
    # 返回给 async_create_entry 用的信息
    return {"title": hub.name, "unique_id": hub.mac}


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "invalid_host"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
```

这里还有两个「潜规则」值得记下（完整可运行版本见官方示例仓库 [example-custom-config](https://github.com/home-assistant/example-custom-config) 的 `detailed_hello_world_push`）：

- **`step_id` 必须与方法名对应**：`async_step_user` 里的表单 `step_id="user"`，因为 HA 就是按「`async_step_` + step_id」去找下一个方法。方法名改错了，流程会找不到下一步。
- **`async_show_form` 的核心参数**：`step_id`（对应哪个方法）、`data_schema`（表单长什么样）、`errors`（要不要回显错误）、`description_placeholders`（可动态填充 description 里的 `{变量}`）。上手阶段前三者够用。

流程走一遍：

1. **schema 先做类型校验**：`vol.Required(CONF_HOST): str` 表示 host 必填且必须是字符串。类型不对，voluptuous 在进入 `async_step_user` 之前就会拦下，并在对应字段下显示错误。
2. **`validate_input` 做真实校验**：类型对不代表能连上，这里真的去连一次设备。这是整个流程里唯一可能耗时的环节，所以是 `async` 的。你集成的 API 客户端 `YourHubClass` 按 HA 架构铁律应封装在独立 PyPI 库（第 6 章细讲），这里先用占位。
3. **异常映射**：连不上抛 `CannotConnect` → 记到 `errors["base"]`；主机非法抛 `InvalidHost` → 记到 `errors["host"]`。记到哪个键，决定了错误显示在哪里。
4. **兜底**：任何没预料到的异常，`except Exception` 记录完整堆栈日志，然后统一显示「未知错误」，绝不裸奔给用户看。
5. **成功**：`async_create_entry(title=..., data=user_input)` 生成 config entry，流程结束，HA 跳回「设备与服务」并显示新条目。

> [!tip] 大白话
> 把表单校验想成「门卫核验申请材料」。第一步 schema 是「查证件类型对不对」——要求填手机号，结果填了邮箱，当场打回；第二步 `validate_input` 是「查这证件能不能真的进门」——号码格式对，但系统里查无此人，也打回。字段级错误是「申请表上具体哪一行划红线」，整体错误是「整张表盖章退回，不针对某一栏」。

## 4.3 errors 回显：字段级 vs 整体 vs 兜底

`errors` 是一个字典，它有三种「落点」：

| 落点 | 写法 | 显示位置 | 典型场景 |
|------|------|----------|----------|
| 字段级 | `errors["host"]` | 表单中 host 输入框下方 | 这个字段本身有问题（如主机地址非法） |
| 整体 | `errors["base"]` | 表单顶部通用错误区 | 无法连接、认证失败这类整体性问题 |
| 兜底 | `errors["base"] = "unknown"` | 表单顶部 | 没预料到的异常，不暴露细节 |

「字段级 vs 整体」的选择标准：**错误能否归因到某一个输入框？** 能就绑字段，不能就绑 `base`。比如「密码错误」绑到 `errors["password"]`（让用户知道去改哪里），而「连不上服务器」跟哪个字段都无关，绑 `base` 最合理。

兜底 `"unknown"` 的意义是**不向用户泄露内部细节**：未知异常多半是代码 bug 或意外输入，直接展示堆栈既难看又暴露实现；正确做法是 `_LOGGER.exception` 把完整堆栈写进日志（开发时一眼定位），界面上只给一句中性的「未知错误」，用户可以去日志里排查。

错误的具体文案不写在代码里，而是写在外层 `strings.json`（下节）。代码里只放一个**错误键**（如 `"cannot_connect"`），文案由 HA 按键名去翻译文件里查。**键必须两边对齐**——代码抛了 `"invalid_host"`，`strings.json` 里没有这个键，界面上就会显示成原始键名，用户看到一串英文标识符，体验很差。

## 4.4 strings.json：把文案搬出去

`strings.json` 放在 `custom_components/<domain>/strings.json`，结构对应 config flow 的三个区块：

```json
{
  "config": {
    "step": {
      "user": {
        "title": "连接 Hello World 设备",
        "description": "请输入设备的连接信息",
        "data": {
          "host": "主机地址",
          "username": "用户名",
          "password": "密码"
        }
      }
    },
    "error": {
      "cannot_connect": "无法连接到设备",
      "invalid_host": "主机地址无效",
      "unknown": "未知错误"
    },
    "abort": {
      "already_configured": "该设备已配置"
    }
  }
}
```

- `config.step.user.data`：表单里每个字段的**显示标签**（键是字段名）。完整的文案与翻译规则见官方 [Config Flow 文档](https://developers.home-assistant.io/docs/core/integration/config_flow/)。
- `config.error`：错误键 → 用户可见文案。代码里 `errors["base"] = "cannot_connect"`，这里的 `"cannot_connect"` 就是查表的键。
- `config.abort`：流程被**中止**时的文案（如「该设备已配置」，配合唯一性使用，见下节）。

> [!note] 进阶提示
> 想要多语言，翻译由 `script.translations develop` 生成到 `translations/*.json`；公共文案可用 `[%key:common::config_flow::...%]` 引用。上手阶段先维护 `strings.json` 一份即可。

## 4.5 唯一性：async_set_unique_id + _abort_if_unique_id_configured

同一个设备被用户配置两遍，会出现重复条目、重复实体。Config Flow 提供标准防重机制：**唯一 ID + 查重中止**。在 `async_create_entry` 之前补两行：

```python
            else:
                await self.async_set_unique_id(info["unique_id"])  # 用 MAC，不是 IP
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)
```

- **`async_set_unique_id`**：给这条配置绑定一个全局唯一标识。HA 用它在 entity registry / device registry 之间关联同一台设备。
- **`_abort_if_unique_id_configured()`**：如果这个 unique_id 已经配置过，立即中止本次流程，并显示 `strings.json` 里 `config.abort.already_configured` 的文案。它还可以带 `updates=` 参数，在检测到重复时顺手把已有条目更新为新提交的数据——适合「设备信息变了、但仍是同一台」的场景。

**unique_id 选什么，是本章最容易踩的坑：**

- 禁止用 IP、设备名。IP 会变（DHCP 换地址），设备名可以重复，都不能作为稳定身份。
- 用 MAC 地址、序列号、芯片 ID 这类**出厂唯一且不变**的标识。

> [!tip] 大白话
> 把 unique_id 想成「门禁卡上的唯一编号」。编号是出厂烙上去、一辈子不变的；而 IP 就像「今天坐哪个工位」——换工位（换 IP）不影响你是谁。系统靠编号认设备：编号一样就说明「这张卡已经办过了」，直接告诉你「已配置」，不让重复办。

## 4.6 Options Flow：data 不可变，options 可变

配置条目创建后，`data` 里存的是「安装时的固定信息」（主机地址、账号等）。但用户可能之后想改一些**偏好**（如轮询频率、显示单位）。这就是 Options Flow 的舞台。

**`data` vs `options` 的分工：**

| 维度 | `data` | `options` |
|------|--------|-----------|
| 可变性 | 安装后不可变 | 用户随时可改 |
| 存放内容 | 连接凭证、设备地址 | 偏好、开关、频率等 |
| 修改方式 | 需 reconfigure/删除重配 | 设置界面里的「选项」 |
| 典型例子 | host、username、password | 更新间隔、显示单位 |

Options Flow 的骨架：在 config flow 类里声明一个静态方法返回 `OptionsFlow` 子类；OptionsFlow 的**第一个 step 恒为 `async_step_init`**。

```python
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.schema_config_entry_flow import add_suggested_values_to_schema

from .const import CONF_SCAN_INTERVAL, DOMAIN


class HelloWorldOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            # options 保存后，用户即可通过 add_update_listener 感知变更
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(CONF_SCAN_INTERVAL): cv.positive_int,
            }
        )
        return self.async_show_form(
            step_id="init",
            data_schema=add_suggested_values_to_schema(schema, self.config_entry.options),
        )


class HelloWorldConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        """让 HA 知道选项流程从哪个类实例化。"""
        return HelloWorldOptionsFlow(config_entry)
```

- `async_get_options_flow` 是 config flow 类里的**静态方法**，返回一个 OptionsFlow 实例。想让 options 变更后集成自动重新加载，可以让 OptionsFlow 继承 `OptionsFlowWithReload` 基类，省去手写 `add_update_listener` 的样板（`OptionsFlow`/`ConfigEntry` 的完整语义见官方 ConfigEntry 文档 [官方 Config Flow 文档](https://developers.home-assistant.io/docs/core/integration/config_flow/)）。
- `add_suggested_values_to_schema(schema, self.config_entry.options)`：把**当前已保存的 options** 预填进表单，用户看到的是「当前值」而不是空白。
- 保存后 `options` 变了，HA 会在条目上触发 `add_update_listener`；集成里用 `entry.async_on_unload(entry.add_update_listener(处理函数))` 监听并处理（如重新加载）。

> [!tip] 大白话
> 把 options 想成「拿到门禁卡之后，在前台登记的可调偏好」。`data` 是发卡时写死的信息（工号、所属部门），员工自己改不了；`options` 是卡上可以现场调整的偏好（比如门禁生效时段），随时找前台改，改完立刻生效。

## 4.7 异常语义：ConfigEntryNotReady vs ConfigEntryAuthFailed

config entry 创建后，HA 会调用你集成的 `async_setup_entry`（第 5、6 章会写）。这一步如果失败，抛什么异常决定了后续行为。**这两个异常是本章必须分清的一对：**

| 异常 | 语义 | 触发行为 | 类比 |
|------|------|----------|------|
| `ConfigEntryNotReady` | 设备/服务暂时不可用（刚开机、网络抖动） | 条目进入 `SETUP_RETRY`，按指数退避自动重试：等待 `min(2^次数 × 5, 上限)` 秒后再试，不是硬失败 | 门禁系统还在重启，过几秒再刷一次卡 |
| `ConfigEntryAuthFailed` | 凭证失效（token 过期、密码被改） | 触发 reauth 重新认证流程，把用户引导回「重新登录」 | 卡被吊销了，需要重新办授权 |

为什么这个区分很重要？因为**用错会让用户体验崩掉**：

- 把 `ConfigEntryAuthFailed` 误抛成 `ConfigEntryNotReady` → HA 会无限指数退避重试，但重试再多次也救不回失效的 token，白白消耗资源。
- 把临时故障误抛成 `ConfigEntryAuthFailed` → 用户被频繁拉去重新登录，其实过几秒网络就恢复了。

> [!tip] 大白话
> 把这两个异常想成两种「刷不开门」的情况。`ConfigEntryNotReady` 是「门禁系统刚开机还在自检」——系统知道过会儿就好，过几秒自动再试一次，不用你操心；`ConfigEntryAuthFailed` 是「你卡里的权限被撤了」——系统再试也没用，只能把你带到前台重新办授权。一个等自动修复，一个必须人工介入。

## 4.8 reauth / reconfigure：点到为止

两个更进阶的流程，本笔记只让你知道「存在」：

- **reauth**：凭证失效后，重新走一遍「登录/授权」来刷新凭证。
- **reconfigure**：让用户重新配置某个条目的 `data`（比如设备搬了新地址）。

官方 2024 年后的写法是用 helper 获取当前条目：`self._get_reauth_entry()` / `self._get_reconfigure_entry()`，不要再手动去 `self.context["entry_id"]` 里翻；配置 `unique_id` 后加 `_abort_if_unique_id_mismatch()` 防止改错设备。**OAuth2 的完整授权流程不在本笔记范围内**，等真正遇到再查官方文档即可。

## 4.9 本章小结

- Config Flow 由 `config_flow.py` 里继承 `config_entries.ConfigFlow` 的类承载，`manifest.json` 须设 `"config_flow": true`，二者缺一不可。
- 表单流程是「两段式」：`async_step_user(user_input=None)` 先展示表单，提交后校验，成功 `async_create_entry`，失败带 `errors` 重显表单。
- 错误映射分三种落点：字段级 `errors["字段"]`、整体 `errors["base"]`、兜底 `except Exception` + `"unknown"`；文案统一放 `strings.json`。
- 唯一性用 `async_set_unique_id` + `_abort_if_unique_id_configured()`，unique_id 选 MAC/序列号这类稳定标识，**禁用 IP/设备名**。
- `data` 安装后不可变、`options` 可变；Options Flow 首步恒为 `async_step_init`，用 `add_suggested_values_to_schema` 预填当前值。
- `ConfigEntryNotReady` 自动指数退避重试，`ConfigEntryAuthFailed` 触发 reauth——临时故障与凭证失效要分清。

下一章我们进入实体世界：把 config entry「接上电」，用 `async_forward_entry_setups` 装载 sensor 平台，写第一个真正会显示状态的 sensor 实体。到那时你会发现，这一章做好的 config entry，正是下一章实体注册的入口凭证。

---

# 第 5 章：Entity 平台与 Sensor 实体

第 4 章我们走通了 config flow：用户填完表单、校验通过，HA 签发了一张「门禁卡」——一个 config entry。但这时候打开 HA 界面，依然看不到任何数据。本章要解决的就是「从配置到展示」这一段：定义一个 sensor 平台，把 config entry 转成 HA 认识的实体，让数据真正摆上货架。读完你会明白实体是怎么被装载、注册、驱动起来的，也会看到一个「薄实体」应该长什么样。

## 5.1 平台装载机制：async_forward_entry_setups

HA 集成按「平台」拆分文件：传感器放 `sensor.py`，二进制传感器放 `binary_sensor.py`，开关放 `switch.py`……这正是第 3 章目录结构里「按平台拆分」的落地——一个文件就是一个平台，HA 通过平台文件组织不同的实体类型[官方平台索引文档](https://developers.home-assistant.io/docs/creating_component_index/)。config flow 只是「办好了门禁卡」，真正让实体出场的是 `async_forward_entry_setups`。

在 `__init__.py` 里，`async_setup_entry` 的最后一步把平台装载进来：

```python
# __init__.py —— 承接第 4 章的 async_setup_entry
async def async_setup_entry(hass, entry):
    """config flow 校验通过后，HA 调用这里正式建立条目。"""
    # 告诉 HA：请把这个 config entry 交给 sensor 平台处理。
    # HA 会去 custom_components/<domain>/sensor.py 找同名入口函数。
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
```

`async_forward_entry_setups` 做的事：为列表里的每个平台，调用对应文件里的 `async_setup_entry(hass, entry, async_add_entities)`。一次可以传多个平台，比如 `["sensor", "binary_sensor", "switch"]`。所以每个平台文件的职责非常单一——只实现这一个入口函数，把实体「注册」给 HA：

```python
# sensor.py —— sensor 平台的唯一入口
async def async_setup_entry(hass, entry, async_add_entities):
    """拿到 config entry，决定要注册哪些实体。"""
    coordinator = entry.runtime_data.coordinator  # 数据源，第 6 章接入
    async_add_entities(
        ExampleSensor(coordinator, description) for description in SENSOR_TYPES
    )
```

`async_add_entities` 是 HA 塞给你的「注册回调」：你往里丢一批实体实例，HA 就把它们纳入实体状态机，开始驱动。一个平台入口可以多次调用它，也可以一次传一个列表（比如第 6 章动态发现设备时，用差集增量添加）。

> [!tip] 大白话
> 把 config flow 想成「办了门禁卡」，`async_forward_entry_setups` 就是把这张卡送到对应柜台的过程：HA 是前台，`sensor.py` 是传感器柜台。前台拿着卡喊一声「传感器柜台有人来了」，柜台里的 `async_setup_entry` 就出来接人。所以你这头只负责写「柜台怎么接待」，装载的吆喝交给 HA。

## 5.2 Entity 状态机基础：实体怎么「活」起来

实体不是静态数据，它由一套状态机驱动[官方 Entity 文档](https://developers.home-assistant.io/docs/core/entity/)。上手阶段先记三个开关：

- **`available`**：实体当前是否可用。为 False 时 UI 置灰、自动化自动跳过。默认 True。
- **`should_poll`**：是否由 HA 周期性调用 `update()`/`async_update()` 拉取新值。默认 True（轮询模型）；设为 False 走推送模型，用 `async_write_ha_state()` / `async_schedule_update_ha_state()` 主动通知状态变化。轮询适合「不知道数据何时变」的外部 API；推送适合能主动回调的本地设备。
- **`_attr_` 前缀类属性**：给实体提供「默认实现」的声明式写法。

实体还有两个生命周期钩子值得知道：`async_added_to_hass()` 在实体加入 HA 时调用，常用于订阅外部事件；`async_will_remove_from_hass()` 在实体被移除时调用，用于退订。订阅与退订必须成对，否则会泄漏监听器——Plex 集成的 dispatcher 模式就是典型例子，第 6 章推送模型还会再碰到。

`_attr_` 是 HA 实体里最常用的套路：凡是名字以 `_attr_` 开头的类属性，HA 会自动把它当作同名属性的默认值。例如 `_attr_native_unit_of_measurement = "µg/m³"` 就等于实现了 `native_unit_of_measurement` 属性返回该值：

```python
class ExampleSensor(SensorEntity):
    _attr_has_entity_name = True            # 声明式：固定标签直接写在类上
    _attr_native_unit_of_measurement = "µg/m³"
    _attr_device_class = "pm25"
```

**关键纪律：属性 getter 禁止 I/O。** 无论用 `_attr_` 还是 `@property`，实体属性的读取都只能发生在事件循环的「内存读取」里，绝不能在这里发 HTTP 请求、查数据库、做阻塞计算。正确做法是：数据在 `update()`/`async_update()` 方法里统一拉取并缓存到 `self`，getter 只负责把缓存摆上货架。

```python
class PlainSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self):
        self._cached_value = None

    async def async_update(self):
        """should_poll=True 时，HA 周期性调用这里：唯一允许 I/O 的地方。"""
        self._cached_value = await self._fetch()  # 发请求、拿数据、缓存

    @property
    def native_value(self):
        return self._cached_value                 # getter 只读缓存
```

update 负责「取」，getter 负责「摆」，各司其职。HA 的状态驱动循环是：`async_update()` 拉新数据 → 写状态 → 界面读取属性。任何属性 getter 一旦越过这条线去做 I/O，就可能阻塞整个事件循环。

> [!warning] 易错点
> 属性 getter 里做 I/O（发请求、读文件、阻塞计算）是自定义集成最常见的问题之一：HA 的事件循环是单线程的，getter 一次阻塞，整个 HA 都会卡顿。这也是素材里反复强调的异步纪律。

> [!tip] 大白话
> `_attr_` 类属性就像「商品的固定标签」——「产地：杭州」「规格：500ml」印在包装上，顾客拿起就看，不用每次跑去仓库问。getter 只读内存就是「看标签」，代价近乎为零；如果在 getter 里发网络请求，等于每次有人看标签都要跑一趟仓库，既慢又容易把事件循环堵死。

## 5.3 身份三件套：has_entity_name / unique_id / device_info

一个新实体要「合法上岗」，有三样身份信息几乎必配：

| 配置 | 作用 | 注意 |
|------|------|------|
| `has_entity_name = True` | 实体名自动组合为「设备名 + 实体名」 | HA 官方强制新集成开启 |
| `unique_id` | 实体的唯一身份证号，关联 entity registry | 平台内唯一，禁止用 IP / 设备名 |
| `device_info` | 把实体挂到某台「设备」下，自动注册 device registry | 提供 `identifiers` 即可 |

- **`has_entity_name=True`**：官方强制项。开启后 friendly_name 由设备名与实体名拼接，避免「PM2.5 / PM2.5 / PM2.5」这种到处重名的混乱。
- **`unique_id`**：实体在 entity registry 里的主键。有了它，HA 才能在重启后记住用户对它的改名、隐藏、归属区域；没有它，每次重启实体都像「新来的」。它要求平台内唯一、一旦确定不可用户配置。
- **`device_info`**：把多个实体归到同一台「设备」下（比如一台净化器有 PM2.5 和温度两个传感器）。只要提供 `identifiers`，HA 会自动在 device registry 里建好设备记录，UI 里这些实体就出现在同一张设备卡下：

```python
self._attr_device_info = DeviceInfo(
    identifiers={(DOMAIN, coordinator.address)},
    manufacturer="Example",
    name="示例设备",
)
```

注意两个注册表的分工：**entity registry 管实体**（改名、隐藏、归属区域），**device registry 管设备**（一台设备聚合多个实体）。`unique_id` 决定实体进 entity registry，`device_info` 决定设备进 device registry。也正因为 unique_id 承担了「记住用户设置」的重任，它必须稳定且唯一：官方要求禁止用 IP、设备名这类可能变化的值，而要用 MAC、序列号或我们这里的「设备地址 + key」这类长期不变的组合。

多个平台（`sensor`、`binary_sensor`）的实体只要提供同一组 `identifiers`，就会归入同一台设备，UI 上共享一张设备卡——这是 device registry 最常见的价值。

> [!tip] 大白话
> Entity 就是「柜台展示员」，sensor 实体负责把数据摆上货架给用户看。`unique_id` 是展示员的工号，凭工号 HA 才能认出「还是上次那个人」，不然每次重启都是新面孔；`device_info` 是「所属部门」，把同属一台设备的展示员编进同一组；`has_entity_name` 决定工牌上怎么写名字。展示员自己不做数据搬运——数据由后仓（coordinator）送来，他只负责上架。

## 5.4 声明式实体写法：SensorEntityDescription + value_fn

一个集成往往有多个 sensor。与其为每个传感器复制一份类，不如把「差异」提取成描述。HA 提供 `SensorEntityDescription` 作为基类，社区常用 `@dataclass(frozen=True)` 子类化它、再追加一个 `value_fn` 字段（参考 [mops_pm25](https://github.com/haruue/mops_pm25) 的实现）：

```python
# sensor.py
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity


@dataclass(frozen=True)
class ExampleSensorDescription(SensorEntityDescription):
    """在官方描述类上「加料」：多一个 value_fn 告诉实体怎么取值。"""

    value_fn: object | None = None


SENSOR_TYPES = (
    ExampleSensorDescription(
        key="pm2_5",
        name="PM2.5",
        native_unit_of_measurement="µg/m³",
        device_class="pm25",
        value_fn=lambda c: c.data.get("pm2_5"),
    ),
    ExampleSensorDescription(
        key="temperature",
        name="温度",
        native_unit_of_measurement="°C",
        device_class="temperature",
        value_fn=lambda c: c.data.get("temperature"),
    ),
)


class ExampleSensor(CoordinatorEntity, SensorEntity):
    """实体很薄：数据从 coordinator 拿，只负责上架。"""

    _attr_has_entity_name = True

    def __init__(self, coordinator, description):
        super().__init__(coordinator)
        self.entity_description = description
        # 唯一 ID：设备地址 + 描述 key，保证平台内唯一
        self._attr_unique_id = f"{coordinator.address}-{description.key}"

    @property
    def native_value(self):
        return self.entity_description.value_fn(self.coordinator)
```

这段代码每一行的意图：

- `@dataclass(frozen=True)`：描述类不可变，安全、可哈希，符合声明式风格。
- `value_fn`：描述里声明「这个 key 怎么从 coordinator 的数据里取值」，实体类不再写 if/else 分支。它不一定是 lambda：当取值逻辑变复杂（单位换算、字段缺失时的兜底值），可以抽成命名函数，在描述里引用函数名即可。
- `entity_description` 一旦赋值，HA 会自动用描述里的 `name` / `native_unit_of_measurement` / `device_class` 填充实体属性，实体类本身不用再声明 `_attr_` 去覆盖。
- `native_value` 委托 `value_fn(self.coordinator)`：getter 只做内存读取，满足 5.2 的纪律。
- `_attr_unique_id = f"{coordinator.address}-{description.key}"`：用「设备地址 + 传感器 key」拼出稳定唯一 ID，天然满足「平台内唯一、可追溯到设备」的要求。

`SENSOR_TYPES` 是模块级常量，放在 `sensor.py` 顶部即可；描述多了也可以挪到 `const.py`。注册时用生成器表达式把每个描述实例化为实体——这正是官方维护者蓝本里的常见写法：先声明描述列表，再用一行生成器交给 `async_add_entities`，见 5.1 的入口骨架。描述列表与实体类的解耦，让「新增一个传感器」彻底变成纯配置操作。

以后想加一个传感器，只需在 `SENSOR_TYPES` 里加一行描述，实体类一行都不用改。这就是声明式写法的收益：**差异数据化，逻辑收敛在描述里。**

## 5.5 衔接：CoordinatorEntity 基类

上面的实体类继承的不是 `SensorEntity` 而是 `CoordinatorEntity`——这是一个值得提前认识的基类，它是第 6 章 DataUpdateCoordinator 的「插座」[官方数据获取文档](https://developers.home-assistant.io/docs/integration_fetching_data/)：

- 它自动接管 `should_poll`：把实体的刷新请求转成 `coordinator.async_request_refresh()`。
- 它自动实现 `async_update()`：实体该更新时，去问 coordinator 要最新数据。
- 它自动挂钩 `available`：coordinator 上次更新成功（`last_update_success`）时实体才可用，失败自动置灰。

换句话说，`CoordinatorEntity` 把 5.2 节讲的三个开关全部接管了：`should_poll`、`async_update`、`available` 都不再需要你手写，实体类只要关心「从 coordinator 的数据里取出并格式化这一个值」。一旦实体继承它，轮询、更新、可用性三件事都交给 coordinator 统一管理，实体只剩「摆数据」这一件事。这正是下一章的内容：coordinator 如何定时去 API 拉数据、多实体如何共享同一次轮询、异常如何归类成重试或 reauth。

## 本章小结

- 平台装载：`async_forward_entry_setups(entry, ["sensor"])` 把 sensor 平台接进来；平台文件只需实现 `async_setup_entry(hass, entry, async_add_entities)`，用 `async_add_entities` 注册实体。
- 实体状态机三开关：`available`、`should_poll`（默认 True）、`_attr_` 类属性；**属性 getter 只读内存，I/O 必须放 update 方法**。
- 身份三件套：`has_entity_name=True`（强制）、`unique_id`（平台内唯一、关联 entity registry）、`device_info`（自动注册 device registry）。
- 声明式写法：`@dataclass(frozen=True)` 子类化 `SensorEntityDescription` + `value_fn`，实体差异全部收敛进描述。
- 实体继承 `CoordinatorEntity` 后，轮询 / 更新 / 可用性都交给 coordinator，为第 6 章铺路。

下一章，我们要解决最后一个问题：这些实体展示的数据从哪来？DataUpdateCoordinator 将作为「仓库统一收货员」，定时去外部 API 拉数据，让所有实体共享同一份到货数据。

---

# 第 6 章：DataUpdateCoordinator 数据轮询

第 5 章我们把 sensor 实体比作「柜台展示员」，让它们把数据摆上货架。但一个关键问题悬而未决：**货架上的货从哪来？** 实体属性 getter 是禁止做网络请求的，如果让每个实体各拉各的数据，既重复又混乱。这一章解决数据来源问题：用一个 `DataUpdateCoordinator` 统一轮询外部 API，把结果缓存在内存里，所有实体共享同一份。这是 HA 集成架构中最关键的一环，也是本笔记的两大重点之一——它决定你的集成是「每家柜台各跑一趟进货」还是「一个仓库统一收货」。

## 6.1 问题：实体不能自己发请求

回顾第 5 章，实体读取数据的正确姿势是 `_attr_` 类属性或属性 getter 返回内存里的值，例如 `self.coordinator.data`。官方异步纪律明确规定：**属性 getter 只能读内存，不能做 I/O**。原因很现实——HA 的事件循环是单线程的，getter 里一旦出现网络请求，就会阻塞整个 HA 的响应，其他所有集成都会被拖住（[官方 asyncio_working_with_async 文档](https://developers.home-assistant.io/docs/dev_101_async/)）。

那数据该由谁来拉？最笨的办法是每个实体在 `update()` 里各发一次请求。假设你有 5 个实体，`update_interval` 设为 30 秒，那么每 30 秒就会对同一个 API 发出 5 次完全相同的请求——浪费带宽，也容易被对方限流。更糟的是，错误处理会散落在每个实体里，你无法统一应对「认证失效」「限流」这类全局性故障。

`DataUpdateCoordinator` 正是为解决这个问题而生的：它是 HA 内置的「数据轮询协调器」，负责按固定间隔拉取一次数据、缓存到 `coordinator.data`，再通知所有订阅的实体来读缓存（[官方 fetching_data 文档](https://developers.home-assistant.io/docs/integration_fetching_data/)）。第 5 章提到的 `CoordinatorEntity` 基类，就是实体端接入 coordinator 的标准方式。

> [!tip] 大白话
> 把 Coordinator 想成**仓库统一收货员**：外部 API 是供应商，实体是各个柜台。没有收货员时，每个柜台都得自己跑到门口接货，来一车货就重复接 N 遍；有了收货员，一车货到后他搬进仓库、分给所有柜台，每个柜台只需去仓库看一眼自己那份。所以，多个实体共享一份数据，网络请求只发一次，错误也由收货员统一处理。

理解 coordinator 的关键，是看懂一个完整轮询周期里发生的事：

1. 到达 `update_interval`（比如 30 秒），coordinator 调用 `_async_update_data`。
2. **成功**：返回值写入 `self.data`，`last_update_success` 置为 `True`，然后通知所有订阅的实体「数据更新了，来读缓存」。`CoordinatorEntity` 收到通知后自动刷新状态。
3. **失败**：`last_update_success` 置为 `False`，`CoordinatorEntity` 会把实体的 `available` 翻成 `False`——这正是第 5 章提到的「`CoordinatorEntity` 自带 Mark unavailable 逻辑」，实体端不需要写任何代码，故障时界面自动变不可用。

`last_update_success` 这个标志，就是实体「是否可用」的数据来源。所以只要 `_async_update_data` 写好，实体侧几乎不用关心轮询的成败细节。

## 6.2 coordinator.py 骨架

按第 3 章的文件组织约定，coordinator 单独放一个 `coordinator.py`。核心是继承 `DataUpdateCoordinator`，重写 `_async_update_data`——它会在每个轮询周期被调用，返回值会存进 `coordinator.data`，供所有实体读取。

```python
# coordinator.py
"""数据轮询协调器：统一拉取外部 API 数据，缓存后分发给各实体。"""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from my_cloud_api import MyApiClient          # 独立 PyPI 库（见 6.6）
from my_cloud_api.errors import (             # 库自带的自定义异常
    ApiAuthError,
    ApiRateLimitError,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator[dict]):
    """统一轮询外部 API，把数据缓存到 coordinator.data。"""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, api: MyApiClient
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),  # 每 30 秒轮询一次
        )
        self.api = api

    async def _async_setup(self) -> None:
        """一次性初始化，首次刷新期间自动调用（HA 2024.8+）。"""
        # 只做一次的事放这里：拿设备信息、建立连接、探测能力等
        await self.api.async_fetch_device_info()

    async def _async_update_data(self) -> dict:
        """每次轮询调用：拉数据并返回，存进 coordinator.data。"""
        try:
            # 网络请求必须包在超时里，防止 API 卡死整个轮询
            async with asyncio.timeout(10):
                raw = await self.api.async_fetch_sensor_data()
        except ApiAuthError as err:
            # 认证失效：触发 reauth，而不是普通重试
            raise ConfigEntryAuthFailed("API 认证失败，需要重新授权") from err
        except ApiRateLimitError as err:
            # 限流：告诉 HA 60 秒后再试
            raise UpdateFailed("请求过于频繁") from err
        # 注意：asyncio.TimeoutError 和 aiohttp.ClientError
        # 已被 coordinator 内部处理，这里无需捕获
        return raw
```

要点逐一说明：

- **`asyncio.timeout(10)`**：把网络请求包裹在 10 秒超时里，是官方文档的标准做法。API 卡住时，轮询不会无限期阻塞。
- **返回值即数据**：`_async_update_data` 的返回值会成为 `self.data`，实体只读它，绝不自己发请求。
- **不要在 `_async_update_data` 里直接做业务**：它只负责「把原始数据拿回来」，加工、建模交给独立库。

运行后你会在 `home-assistant.log` 里看到 coordinator 自己的轮询记录（Debug 级别）：

```text
Updating my_cloud data                  # 开始轮询
Finished fetching my_cloud data in 0.340 seconds   # 成功，耗时 0.34 秒
```

如果 API 一直失败，日志会显示 `Unable to fetch my_cloud data: ...`，同时实体在界面上变为不可用。这套日志是 coordinator 自动打的，不用你自己写——这也是为什么构造时要把 `_LOGGER` 传进去。

## 6.3 异常语义：把错误翻译成 HA 听得懂的语言

coordinator 的价值不只在于「少发请求」，更在于**统一错误语义**。HA 对不同的异常有不同的反应，你必须把 API 库抛出的错误翻译成 HA 认识的那几种（异常映射参考官方维护者蓝本 [ludeeus/integration_blueprint](https://github.com/ludeeus/integration_blueprint)）：

| 情况 | 抛出的异常 | HA 会怎样 |
|------|-----------|-----------|
| 认证失败（token 失效等） | `ConfigEntryAuthFailed` | 触发 reauth 重授权流程，不自动重试 |
| 一般业务错误 | `UpdateFailed` | 实体标记为不可用，下个周期再试 |
| 限流（429 等） | `UpdateFailed(retry_after=60)` | 等待 60 秒后再重试 |
| 超时 / 网络层错误 | 不捕获 | `asyncio.TimeoutError` / `aiohttp.ClientError` 由 coordinator 内部处理 |

两个易错点要特别记牢：

- **`ConfigEntryAuthFailed` 和 `ConfigEntryNotReady` 别用反**。第 4 章讲过：`NotReady` 是「暂时起不来，指数退避自动重试」，`AuthFailed` 是「登录已失效，需要用户重新授权」。认证失败时如果抛了 `NotReady`，HA 会一直空转重试，用户却得不到重新登录的提示——这是新手最常见的坑之一（素材 三.常见坑 #5）。
- **超时和网络错误不用你管**。`asyncio.TimeoutError`、`aiohttp.ClientError` 由 coordinator 内部处理并转为实体不可用，你不需要（也不应该）在 `_async_update_data` 里捕获它们。你只需要处理**业务语义**层面的错误。

为什么「限流」值得单独设一个 `retry_after=60`？因为限流通常是**可预期的**：API 明确告诉你「60 秒内别再来了」。如果你不加 `retry_after`，coordinator 会按原 `update_interval`（比如 30 秒）继续撞上去，每次都吃一个 429，白白浪费。带上 `retry_after`，coordinator 会尊重这个冷却期，到点再试。

一个完整的认证失败场景是这样流转的：集成运行中，云端把 token 吊销了 → 下一次轮询 `async_fetch_sensor_data` 抛 `ApiAuthError` → 你把它翻译成 `ConfigEntryAuthFailed` → HA 触发 reauth，用户在 UI 上重新授权 → 授权成功后配置条目重载、coordinator 重建、一切恢复正常。如果没有这一步翻译，用户只会在日志里看到「数据获取失败」，不知道是该重新登录——这就是统一异常语义的价值。

## 6.4 接线：一个 coordinator + 多个实体

coordinator 写好后，要在 `__init__.py` 的 `async_setup_entry` 里把它建起来，并接入各实体平台（官方 [fetching_data](https://developers.home-assistant.io/docs/integration_fetching_data/) 的接线方式）：

```python
# __init__.py（async_setup_entry 片段）
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from my_cloud_api import MyApiClient
from .const import DOMAIN
from .coordinator import MyCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 1. 用 entry 配置建好 API client（独立库）
    api = MyApiClient(
        host=entry.data["host"],
        token=entry.data["token"],
        session=aiohttp_client.async_get_clientsession(hass),  # 复用 HA 的会话
    )

    # 2. 只建一个 coordinator，所有实体共享
    coordinator = MyCoordinator(hass, entry, api)

    # 3. 首次刷新：失败会抛 ConfigEntryNotReady，HA 自动重试
    await coordinator.async_config_entry_first_refresh()

    # 4. 存到 entry.runtime_data（见 6.5）
    entry.runtime_data = coordinator

    # 5. 把 sensor 平台接进来
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
```

这里的顺序是刻意安排的：**先 `first_refresh`，再 `async_forward_entry_setups`**。如果首次拉取失败（比如 API 还没就绪），`async_config_entry_first_refresh()` 会抛 `ConfigEntryNotReady`，`async_setup_entry` 中止，HA 按指数退避自动重试——不会先加载一堆读不到数据的实体。

实体端用 `CoordinatorEntity` 订阅，并用 `context=idx` 区分自己是哪一路数据：

```python
# sensor.py（片段）
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MyCoordinator


class MySensor(CoordinatorEntity[MyCoordinator]):
    """订阅 coordinator 的实体：只读 coordinator.data，不自己发请求。"""

    def __init__(self, coordinator: MyCoordinator, idx: str) -> None:
        super().__init__(coordinator, context=idx)  # context 标识这一路数据
        self.idx = idx

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data
        if data is None or self.idx not in data:
            return None
        return data[self.idx]["value"]


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator: MyCoordinator = entry.runtime_data
    # 按数据里的每个条目生成一个实体
    async_add_entities(
        MySensor(coordinator, idx) for idx in coordinator.data
    )
```

两个行为细节值得留意（素材 一.5）：

- **`update_interval` 只在有订阅者时才轮询**。HA 会跟踪 coordinator 的订阅者数量，实体全部被移除、无人订阅后，轮询自动停止，不再产生无谓的网络请求。
- **`_async_setup` 做一次性初始化**（HA 2024.8+ 新增）。像「获取设备信息」这类只需做一次的事放在 `_async_setup` 里，它会在 `async_config_entry_first_refresh()` 期间被自动调用，并和 `_async_update_data` 共享同一套错误处理——初始化时认证失败同样触发 reauth，初始化失败同样走 `ConfigEntryNotReady` 重试。

`context=idx` 是这套共享机制的关键细节。多个实体订阅同一个 coordinator，HA 需要知道「这次数据更新该通知谁」。给每个实体传一个不同的 `context`（比如数据里的传感器 id），coordinator 就能按上下文区分订阅者；而不传 `context` 的实体则订阅「全部数据」。你可以在 `coordinator.async_contexts()` 里看到当前所有活跃订阅者——这也正是「只在有订阅者时才轮询」的实现基础。轮询到的数据回到 `coordinator.data` 后，每个实体读自己 `idx` 对应那一份，互不干扰。

> [!tip] 大白话
> 把 `update_interval` 想成收货员的工作节奏：收货员只在**有人来看货时才去收货**。实体订阅 coordinator，相当于登记「我每天会来取货」；如果所有实体都被移走、没有订阅者了，收货员就不再空跑，省下每次往返的运费。`_async_setup` 则像开业前的仓库盘点——只做一次，之后正常收货。

## 6.5 entry.runtime_data：coordinator 该放哪

旧式写法是把 coordinator 塞进全局字典 `hass.data[DOMAIN]`：

```python
# 旧写法：字符串键 + 全局字典，类型全靠自觉
hass.data[DOMAIN] = coordinator
# 另一处取用
coordinator = hass.data[DOMAIN]
```

新版官方蓝本推荐改用 **`entry.runtime_data`**（素材 二.ludeeus/integration_blueprint）：

```python
# 新写法：跟着 config entry 走，类型可标注
entry.runtime_data = coordinator
# 平台里取用
coordinator: MyCoordinator = entry.runtime_data
```

后者更好的原因：一是**类型安全**，可以标注 `MyCoordinator`，IDE 和静态检查都能帮你兜底；二是**不污染全局字典**，不用担心字符串键拼错、多设备实例互相覆盖；三是语义清晰，coordinator 本来就是「这个配置条目私有的运行数据」，放在 entry 上名正言顺。

多实例场景下这个优势更明显。假如一个集成支持配置两个网关，旧写法 `hass.data[DOMAIN]` 只能存一份，你得再套一层 `{entry_id: coordinator}` 字典才能区分；而 `entry.runtime_data` 天然跟着 entry 走，每个配置条目一份，平台代码里直接 `entry.runtime_data` 取到的就是「当前这个条目」的 coordinator，不会拿错。第 5 章提到的动态设备发现，也是靠 `set(coordinator.data)` 差集配合 `async_add_entities` 增量加实体，这些都建立在「coordinator 随 entry 存」的基础上。

## 6.6 架构铁律：集成要薄，协议放独立 PyPI 库

官方对自定义集成有一条**硬性架构规则**：集成代码内**禁止包含任何协议特定代码**，设备/云 API 的交互必须封装成独立 PyPI 库，集成通过 `manifest.json` 的 `requirements` 依赖它（官方 api_lib_index 文档，见[开发文档索引](https://developers.home-assistant.io/docs/creating_component_index/)）。这条规则直接决定了 6.2 里 `MyApiClient` 为什么从 `my_cloud_api` 导入，而不是写在集成里。

独立库建议拆成**两层**：

```python
# 独立 PyPI 库 my_cloud_api/api.py —— 第 1 层：认证 + HTTP 请求
"""只管「怎么把请求发出去、拿回原始数据」，不关心业务含义。"""

import aiohttp


class MyApiClient:
    def __init__(self, host: str, token: str, session: aiohttp.ClientSession) -> None:
        self._host = host
        self._token = token
        self._session = session

    async def async_fetch_sensor_data(self) -> dict:
        """拉原始 JSON 并返回，不做业务加工。"""
        url = f"{self._host}/api/sensors"
        headers = {"Authorization": f"Bearer {self._token}"}
        async with self._session.get(url, headers=headers) as resp:
            resp.raise_for_status()  # 网络/HTTP 错误从这里冒出
            return await resp.json()
```

```python
# 独立 PyPI 库 my_cloud_api/models.py —— 第 2 层：数据模型
"""把原始 JSON 变成带类型的对象，供集成直接消费。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SensorData:
    sensor_id: str
    value: float
    unit: str

    @classmethod
    def from_dict(cls, raw: dict) -> "SensorData":
        return cls(
            sensor_id=raw["id"],
            value=float(raw["value"]),
            unit=raw["unit"],
        )
```

两层各司其职：**请求层**管认证、重试、超时、翻页，**模型层**管字段校验和类型转换。集成只拿到干净的 `SensorData` 对象，完全不碰 HTTP 细节。本地联调时，在开发环境装依赖并让 HA 跳过本地包即可（素材 一.5）：`pip3 install -e ../my_cloud_api` + 启动时加 `hass --skip-pip-packages my_cloud_api`。

为什么这条规则被官方定为「铁律」，而不是「建议」？至少有三个现实理由：一是**可复用**，同一个协议库可以被多个集成、甚至非 HA 项目共用，不用每次重写一遍认证握手；二是**可版本化**，库独立发版，API 变更时只需升级 `requirements` 里的版本号，集成代码一行不改；三是**安全与审核**，HACS 和官方审查时，协议代码越少、越集中在独立库里，越容易做安全审计——把认证逻辑藏在集成里，既难审也难修。

> [!tip] 大白话
> 把集成想成餐厅前台、协议库想成后厨：前台（实体）只负责把菜端给客人，做菜（协议细节、认证、翻页）全在后厨。厨房升级换菜谱（库版本更新），前台不用改；前台也绝不自己起灶开火——否则 HACS 审核官看到你的集成里藏着一个厨房，直接打回。

## 6.7 推送模型：不轮询，等数据上门

轮询适合「API 只支持主动拉取」的场景。但有些 API 是推送式的（webhook、websocket、MQTT），这时仍用固定间隔轮询就浪费了。有两种轻量做法（素材 一.5、二.plex，点到为止）：

**做法一：保留 coordinator，手动喂数据。** 用 `coordinator.async_set_updated_data(data)` 代替轮询——实体仍然从 `coordinator.data` 读缓存，但数据不再是定时拉来的，而是外部事件到达时推给你的。

**做法二：dispatcher 纯事件驱动（Plex 模式）。** 更轻量，直接用 `async_dispatcher_send` / `async_dispatcher_connect`：

```python
# 实体订阅（async_added_to_hass 里）
self.async_on_remove(
    async_dispatcher_connect(self.hass, self._dispatcher, self._handle_update)
)
# 数据到达时通知（数据源那边）
async_dispatcher_send(hass, dispatcher)
```

推送模型有一个铁律：**订阅和退订必须成对**。在 `async_added_to_hass` 里订阅，把 unsubscribe 句柄交给 `async_on_remove`（或保存在 `async_will_remove_from_hass` 里退订），否则实体被移除后回调还挂在事件总线上，会造成内存泄漏。纯事件驱动的实体还要设 `should_poll=False`。

怎么选？一句话：**API 只能拉就轮询，API 会推就用推送**。云平台大多只提供 REST 拉取接口，轮询是默认解；MQTT、websocket、本地 UDP 这类主动上报的协议，才值得上推送模型。对「上手」阶段，先扎实掌握轮询，推送留个印象即可——大多数自定义集成用 coordinator 轮询就够用了。

## 本章小结

- Coordinator 是「仓库统一收货员」：一个实例统一轮询外部 API，`coordinator.data` 缓存一份数据，所有 `CoordinatorEntity` 共享读取，网络请求只发一次。
- `_async_update_data` 里用 `asyncio.timeout(10)` 包裹网络请求；认证失败抛 `ConfigEntryAuthFailed`（触发 reauth），一般错误和限流抛 `UpdateFailed`（限流可带 `retry_after=60`），超时和 `aiohttp.ClientError` 交给 coordinator 内部处理。
- 多实体共享一次轮询：`async_setup_entry` 只建一个 coordinator，实体用 `context=idx` 订阅；`update_interval` 只在存在订阅者时才轮询。
- `async_config_entry_first_refresh()` 失败抛 `ConfigEntryNotReady` 自动重试；一次性初始化放 `_async_setup`（HA 2024.8+）；coordinator 存进 `entry.runtime_data`，优于 `hass.data[DOMAIN]`。
- 架构铁律：集成内不放协议代码，API 交互封装成独立 PyPI 库（认证/HTTP 层 + 数据模型层）；推送场景用 `async_set_updated_data` 或 dispatcher，订阅退订必须成对。

coordinator 跑起来了，数据能稳定流进实体了。但集成越写越复杂，你怎么确认它真的没写错？第 7 章进入「测试与调试」——用 pytest 给集成写「入职考试」，用 debugpy 给 HA 装上「随身体检仪」，把隐藏在事件循环深处的 bug 揪出来。

---

# 第 7 章：测试与调试

上一章我们给集成装上了 DataUpdateCoordinator 这个「仓库统一收货员」，实体能共享一份轮询数据并对外暴露 sensor。功能看起来能跑，但你心里其实没底：这个集成真的对吗？万一某天数据读错、状态没更新，怎么及时发现？写代码时人可以靠眼睛看，但集成一旦跑起来，状态、服务、注册表之间的联动关系是肉眼盯不过来的；手动在 UI 里点一遍，也只能验证当前这一条路径，下次改动还得重来。这一章补上两块「质量保险」：用 pytest 给集成写自动化测试（入职考试），用 debugpy 和日志做运行时体检（随身体检仪）。前者帮你确认「它是对的」，后者帮你在出问题时看见「它为什么错」。

## 7.1 用 pytest 给集成上「入职考试」

> [!tip] 大白话
> 把测试想成 HA 的「入职考试」——考官不看你平时怎么偷偷努力（内部变量、私有方法），只看你的对外表现：状态机（`hass.states`）里的状态对不对、服务（`hass.services`）能不能被调用、注册表（registry）里有没有登记你这个人。所以测试断言永远走这些核心接口，不碰内部细节。

写测试依赖一个关键插件：`pytest-homeassistant-custom-component`。它从 home-assistant/core 自动抽取测试插件与 fixtures，让自定义集成能用与 HA 核心完全相同的姿势写测试，而不用自己手搭一堆假环境。它每天按 HA 最新版（含 beta）更新，所以你始终在跟 core 保持同一套测试姿势，不会因为版本漂移而测了个寂寞。

用法分两步：先在测试目录放一个 `conftest.py` 声明插件，之后所有测试文件就能直接使用 `hass` fixture。这个 `hass` fixture 会在每个测试里给你一个干净的、内存中的 Home Assistant 实例，测试之间互不污染，跑完即弃。

```python
# tests/conftest.py
import pytest

# 把 HA 核心的 pytest 插件和 fixtures 全部加载进来
pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """每个测试都自动放行 custom_components 下的自定义集成。

    从 HA 2021.6.0b0 起，加载自定义集成必须显式启用，
    否则测试里会报「找不到集成」。
    """
    yield
```

这个 `enable_custom_integrations` 是关键钥匙，有三个配套要点：

- **HA ≥ 2021.6.0b0 必需**：没有它，custom_components 里的集成在测试中根本加载不出来。
- **`recorder_mock` 要先初始化**：如果测试要 mock recorder（历史记录），`recorder_mock` 必须安排在 `enable_custom_integrations` 之前就绪，顺序反了会互相打架。
- **`asyncio_mode = auto`**：你的测试函数都是 `async` 的，需要在 `pyproject.toml` 里配置，让 pytest 自动把协程测试函数跑起来，不必给每个函数手写装饰器。

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

另外，模拟「用户在 UI 里配好的一个集成」用 `MockConfigEntry`，它要从插件包导入：`from pytest_homeassistant_custom_component.common import MockConfigEntry`。

## 7.2 写一条 sensor 平台测试用例

有了 `conftest.py`，写一条真正的测试就非常短。下面这条验证「配置条目加载后，sensor 平台注册出了可用实体」：

```python
# tests/test_sensor.py
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hello_world.const import DOMAIN


async def test_sensor_platform(
    hass: HomeAssistant,
    enable_custom_integrations,
) -> None:
    """配置条目加载后，sensor 平台应注册出可用实体。"""
    # 用 MockConfigEntry 模拟用户在 UI 里完成的一次配置
    entry = MockConfigEntry(domain=DOMAIN, data={"host": "127.0.0.1"})
    entry.add_to_hass(hass)

    # 触发 async_setup_entry，等价于用户「添加集成」
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    # 断言走核心接口 1：状态机 hass.states
    sensor_states = [
        s for s in hass.states.async_all() if s.entity_id.startswith("sensor.")
    ]
    assert sensor_states, "状态机里没有 sensor 实体"
    for state in sensor_states:
        assert state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN)

    # 断言走核心接口 2：设备注册表 device registry
    dev_reg = dr.async_get(hass)
    devices = dr.async_entries_for_config_entry(dev_reg, entry.entry_id)
    assert devices, "配置条目没有注册设备"
```

具体到上面这段：`MockConfigEntry` 造出一张「假的配置单」塞进内存版 HA，`async_setup` 触发你第 4 章写的加载逻辑；随后的 `async_block_till_done()` 会等所有挂起的异步任务跑完——包括 coordinator 的第一次刷新——然后我们才去状态机里查结果。如果断言失败，pytest 会把实际的状态值直接打出来，顺着输出就能定位是「没注册上」还是「注册上了但状态不对」。

注意测试里从头到尾**没有 import 集成内部类，也没有断言内部私有状态**——这正是官方测试指南的硬性要求（见[官方开发文档索引](https://developers.home-assistant.io/docs/creating_component_index/)）。这样做的收益很直接：以后你重构内部实现（比如换一个 API 库、改 coordinator 内部结构），只要对外行为不变，测试依然通过，不会因为「内部搬了家」而整天修测试。

## 7.3 跑测试：pytest 命令与快照

跑测试的命令与 HA 核心仓库一致：

```bash
# 全量跑
pytest tests

# 只跑某个集成，并看覆盖率
pytest ./tests/components/<组件>/ --cov=homeassistant.components.<组件> --cov-report term-missing -vv
```

两个实用参数：

- `--cov=... --cov-report term-missing`：输出覆盖率，标出哪些行没被测试覆盖，方便补齐。
- `--snapshot-update`：快照测试专用。第一次运行生成快照文件（Syrupy 的 `.ambr`），之后把实际结果与快照比对，适合断言「一大坨结构化输出没变」。上手阶段能跑通 `pytest tests` 即可，快照点到为止。

对「上手」这个深度来说，覆盖率数字不必追到 100%——重点是给最核心的两条路径各留一条测试：配置加载（config entry 能建起来）、数据更新（状态能变）。有了这两条打底，后续每次改动跑一遍，基本盘就不会坏。

## 7.4 debugpy：随身体检仪

> [!tip] 大白话
> debugpy 是「随身体检仪」——平时不带，出问题时插上，能随时看到体内每个器官的实时状态（变量值、调用栈），但做检查时会让你整个人先定住不动。HA 是单事件循环，断点一命中，**整个 HA 都会暂停**，等你看完再放行。

在 `configuration.yaml` 里加一个 `debugpy:` 键即可启用，默认监听 `0.0.0.0:5678`：

```yaml
# configuration.yaml
debugpy:
  start: true     # HA 启动时就注入调试器
  wait: false     # false：不等调试器连接直接跑；true：等 VS Code 连上才继续
                  # （wait: true 用于调试 async_setup 这类启动序列）
  # 默认 host 0.0.0.0、port 5678，可按需覆盖
```

- `start: true`：HA 启动时注入调试器；
- `wait: true`：等待调试器连接后才继续执行，用来抓住启动阶段就跑完的代码。

> [!warning] 安全提醒
> 可达调试端口的人可以执行任意代码。调试完务必关掉 `debugpy`，生产环境不要常开。

VS Code 端用 attach 方式连接，`launch.json` 大致如下：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to HA",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "127.0.0.1", "port": 5678 },
      "justMyCode": false,
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/custom_components/hello_world",
          "remoteRoot": "/config/custom_components/hello_world"
        }
      ]
    }
  ]
}
```

### 断点不命中的「三件套」

社区里最常见的问题是「我明明打了断点，为什么不命中」（core issue #110623）。原因基本逃不出下面三件，逐项核对即可：

| 排查项 | 正确姿势 | 原因 |
|--------|----------|------|
| 启动方式 | `python3 -Xfrozen_modules=off -m homeassistant`，而不是 `hass` 命令 | `hass` 可执行脚本会冻结标准库模块，调试器进不去 |
| justMyCode | `"justMyCode": false` | VS Code 默认只调试自己的代码，关掉才能进入 HA core 和依赖库 |
| pathMappings | 本地 `custom_components/<domain>` 映射到运行环境真实路径（容器里是 `/config/custom_components/<domain>`） | 路径对不上，断点位置无法匹配 |

另外记住一个「特性」：asyncio 架构下断点命中时整个 HA 会暂停——界面看起来像卡死，其实是在等你检查。这是单事件循环的必然结果，不是 bug。

配置好之后，调试节奏大致是：HA 带着 debugpy 跑起来 → VS Code 按 F5 attach → 在 `_async_update_data` 或某个实体属性处打上断点 → 触发一次轮询，断点命中时整个 HA 暂停，你在「变量」和「调用堆栈」面板里就能看到这次拿到的原始数据长什么样、是谁一路调进来的。看清后放行，HA 接着往下跑。这种「现场查看」比看日志更直观，尤其适合定位数据解析出错这类问题。

## 7.5 调试日志：从 warning 到 debug

HA 默认日志级别是 **warning**，意味着你的 `_LOGGER.debug(...)` 平时根本不输出。想打开自定义集成的调试日志，在 `configuration.yaml` 里配 `logger`：

```yaml
logger:
  default: warning
  logs:
    custom_components.hello_world: debug   # 本集成所有模块
    aiogithubapi: debug                     # requirements 依赖库要单独加一行
```

注意：requirements 里的依赖库（比如 API 客户端）要**单独加一行**——因为每个依赖库都用自己独立的 logger 名字输出，`custom_components.<domain>` 这个 logger 管不到它们；少配一行，库内部出错时你就只能看到「请求失败」这种笼统信息，定位不到真正原因。

这里有一个经典坑：UI 里的「Enable debug logging」按钮（Settings → System → Logs）对自定义组件**默认无效**（core issue #84489），因为 HA 不知道这个组件涉及哪些 logger。修法是在 `manifest.json` 里加一个 `loggers` 键，把依赖库的 logger 名列出来：

```json
{
  "domain": "hello_world",
  "name": "Hello World",
  "version": "0.0.1",
  "codeowners": ["@your-github-id"],
  "iot_class": "local_polling",
  "loggers": ["aiogithubapi"]
}
```

`loggers` 列出的是 requirements 依赖库的 logger 名（也可以把 `custom_components.hello_world` 自己加进去）。补上这个键之后，UI 按钮才能真正把对应 logger 切到 debug。

## 7.6 排障三板斧

集成跑不起来时，按这个顺序排查：

1. **校验配置**：`hass --script check_config`，会直接指出配置或 manifest 哪行有问题。这一步能在启动前就把「manifest 缺字段」「domain 与目录名不一致」这类问题暴露出来，省得反复重启半天才发现是配置写错。Docker 环境用 `docker exec home-assistant python -m homeassistant --script check_config --config /config`。
2. **看日志**：日志写在配置目录下的 `home-assistant.log`（每次启动重置）；不想翻文件，就打开 UI 的 Settings → System → Logs。
3. **确认级别**：默认是 warning，连 `_LOGGER.info` 都不显示。别在默认级别下到处找 debug 输出——先按 7.5 把 logger 打开。

## 本章小结

- 测试用 `pytest-homeassistant-custom-component`：`conftest.py` 声明 `pytest_plugins` 后直接拿 `hass` fixture；`MockConfigEntry` 从 `pytest_homeassistant_custom_component.common` 导入。
- `enable_custom_integrations` 是加载自定义集成的钥匙；`recorder_mock` 要先于它初始化；`asyncio_mode = auto` 让 async 测试自动跑。
- 断言只走核心接口（`hass.states` / `hass.services` / 设备与实体 registry），不碰内部细节——集成重构不破坏测试。
- 调试三件套：`python3 -Xfrozen_modules=off` 启动、`justMyCode: false`、`pathMappings` 对应 `custom_components`；断点命中时整个 HA 暂停。
- 调试日志：`logger` 配 `custom_components.<domain>: debug`，依赖库单独加行；UI 调试按钮需 manifest 加 `loggers` 键；排障先 `hass --script check_config` 再看 `home-assistant.log`。

集成在自己 HA 里跑通了，也经得起测试和调试了——下一步就是把它交给别人用。第 8 章「HACS 分发」会带你把集成送进应用商店，让其他用户能搜到并一键安装。

---

# 第 8 章：HACS 分发

第 7 章我们让集成通过了测试与调试，质量达标。但这只是「自己能用」；想让其他用户也能一键安装，还差最后一步——通过 HACS（Home Assistant Community Store）把集成分发出去。

> [!tip] 大白话
> HACS 就是「集成界的应用商店」。你在 GitHub 上把集成「上架」（通过 hassfest + hacs/action 校验），其他用户就能在 HACS 里搜索到它、点一下安装，就像手机上装 App 一样。本章就是走完「上架」这条路。

## 8.1 仓库根目录的 hacs.json

HACS 靠仓库根目录的 `hacs.json` 识别这个仓库装的是什么、代码放在哪。最简版本只需要一个必填字段：

```json
{
  "name": "My Awesome Integration"
}
```

`name` 是必填的显示名。其余都是可选：

| 字段 | 作用 |
|------|------|
| `content_in_root` | 代码是否直接放仓库根目录，而不是 `custom_components/` 子目录 |
| `zip_release` | 是否从 Release 的 zip 包安装（需配套 `filename` 指定包内路径） |
| `homeassistant` | 要求的最低 HA 版本 |
| `hacs` | 要求的最低 HACS 版本 |
| `persistent_directory` | 需要持久化保留的目录（更新下载时不被清掉） |

> [!note] 目录规则
> 默认 HACS 要求集成代码放在 `custom_components/<domain>/` 下，只有 `content_in_root: true` 才能直接放根目录。我们第 3 章一直遵守该结构，默认配置就够用。

## 8.2 manifest.json 至少要有 6 个必填字段

HACS 校验时，`manifest.json` 至少要包含这 6 个字段：

| 字段 | 说明 |
|------|------|
| `domain` | 唯一工号，与目录名一致（第 3 章定下，不可改） |
| `documentation` | 集成文档链接 |
| `issue_tracker` | 问题反馈入口链接 |
| `codeowners` | GitHub 维护者，格式 `@用户名` |
| `name` | 显示名 |
| `version` | 版本号 |

> [!warning] version 必须有
> 内置集成可以省略 `version`，但自定义集成在 HACS 里 `version` 是硬性必填——它既是合规校验项，也是第 8.5 节版本比对的依据。

## 8.3 双 Action 校验：上架前的质检

上架前先让两个 GitHub Action 自动检查，避免用户装到坏包。

### hassfest：HA 官方合规校验

`.github/workflows/hassfest.yaml`：

```yaml
name: Validate with hassfest

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  validate:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v4"
      - uses: "home-assistant/actions/hassfest@master"
```

它跟踪 HA 的 beta 通道，能在兼容性出问题前提前提醒你。

### hacs/action：HACS 自己的校验

`.github/workflows/hacs.yaml`：

```yaml
name: HACS Action

on:
  push:
  pull_request:
  schedule:
    - cron: "0 0 * * *"

jobs:
  hacs:
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v4"
      - uses: "hacs/action@main"
        with:
          category: "integration"
```

`category` 必填，我们是集成所以填 `integration`。两个 Action 都配好后，每次 push/PR 都会自动跑一遍，等于上架前的免费质检。

> [!tip] 大白话
> hassfest 是「平台方审核」，hacs/action 是「应用商店审核」。两个都过了，用户端才敢给你一键安装。

## 8.4 打版本：Release tag 才是版本号

HACS 以 **GitHub Release 的 tag** 作为版本来源，而不是 commit。

> [!warning] 只 push tag 不建 Release 无效
> 只打 tag 却不在 GitHub 上「Create release」是没有用的，HACS 拉不到版本。发布流程必须是：打 tag → 建 Release。
> 如果仓库还没有任何 tag，HACS 会退回用 commit 的前 7 位哈希当版本号（能看到版本，但不规范）。

> [!tip] 大白话
> Release tag 是货架上的「版本编号」。只打 tag 不建 Release，等于货架上没摆货，HACS 这个售货员拿不到东西，用户自然也无从更新。

建议的发布流程：

1. 修改 `manifest.json` 的 `version`（如 `0.1.0`）
2. `git tag v0.1.0` 并 `git push --tags`
3. 在 GitHub 仓库页为这个 tag 创建 Release

> [!note] 每仓库一个集成
> HACS 规定一个仓库只能放一个集成；有 Release 时用户端会展示最近 5 个版本。

## 8.5 HACS 怎么发现更新

用户安装后，HACS 的更新机制是这样的：

- HACS 通过 **GitHub API** 拉取你的 release 数据，约每天检查一次
- 用户已装版本存在 `manifest.json` 的 `version` 字段（HACS 记录在 `.storage/hacs.repositories`）
- 拿「当前已装版本」与「最新 release tag」比对，有新的就提示更新
- 用户下载新版本后，**必须重启 HA 才生效**

> [!warning] 未认证会被限流
> HACS 的 GitHub API 请求若未认证会被限流，导致版本陈旧。这也是「HACS 不更新」最常见的原因之一，第 9 章还会遇到。

## 最后一步：加入 brands

还有一个前置小条件：你的集成需要先加入 `home-assistant/brands` 仓库，HACS 才会收录展示。这一步通过向该仓库提交 PR 完成，具体按它的说明来即可。

## 本章小结

- `hacs.json` 是 HACS 的「上架登记表」：`name` 必填，`content_in_root`/`zip_release`/`homeassistant`/`hacs`/`persistent_directory` 按需可选。
- `manifest.json` 至少要有 6 个字段：`domain`/`documentation`/`issue_tracker`/`codeowners`/`name`/`version`。
- hassfest（`home-assistant/actions/hassfest@master`）+ hacs/action（`category: integration`）双 Action 是分发前自动质检。
- 版本取 Release tag：只 push tag 不建 Release 无效；无 tag 时退回 commit 前 7 位。
- HACS 通过 GitHub API 拉 release、约每天比对版本，未认证会限流；更新后需重启 HA 才生效。

至此，从环境搭建到测试调试再到 HACS 分发的完整链路就走通了。但上架只是开始——第 9 章我们把这些过程中最容易踩的坑集中起来，逐条给你「症状 → 原因 → 修法」。

---

# 第 9 章：常见坑与最佳实践

上一章结束时，你的集成已经在 HACS 上架，可以被别人搜索安装。但从「能跑」到「一直能跑、别人也跑得顺」，中间隔着两样东西：排掉别人踩过的坑，养成官方推荐的写法。本章不写新功能，而是把整条路上最容易翻车的 10 个坑和 7 条长期受益的实践，整理成一份可以直接对照的「排错手册」。遇到问题先翻这里，比从零看日志快得多。

> [!tip] 大白话
> 把集成开发想成装修一套房子：第 1 章到第 8 章是「按图纸施工」，本章是「竣工前的验房」。验房单上每一行都是一位前辈替你踩过的坑，你照着逐项打勾，就能在入住前把水电、防水一次查清，而不是住进去以后再砸墙。所以本章更像是「排错清单 + 体检报告」，而不是新的知识点。

## 常见坑：10 个高发事故

以下 10 条综合自官方文档、core 仓库的 issue 和社区真实排错案例。排查顺序建议：先看「症状」对号入座，再读「原因」确认，最后按「修法」动手。

| # | 症状 | 原因 | 修法 |
|---|------|------|------|
| 1 | HA 启动校验失败，集成在「设置 → 设备与服务」里不出现 | manifest 缺 `version`，而它是自定义集成必填项 | 补 `"version": "0.0.1"`，用 CalVer 或 SemVer，保证 AwesomeVersion 兼容 |
| 2 | 目录存在但集成加载失败，日志提示找不到该 domain | 目录名即 domain，大小写/下划线不一致 | `custom_components/<domain>` 的目录名与 manifest 的 `domain` 完全一致，小写下划线 |
| 3 | 自己机器上正常、别人装上报错；或依赖安装失败导致集成直接加载失败 | `requirements` 不固定版本，环境漂移 | 一律 `包名==版本号` 固定（官方示例均如此）；安装失败先看日志里的包名再排查 |
| 4 | 界面卡顿、日志出现「Blocking call」警告、传感器更新超时 | 属性 getter 里做了 I/O，或同步库阻塞了事件循环 | getter 只读内存，数据在 update 协程里拉取；同步库用 `asyncio.to_thread` 或换异步库 |
| 5 | 该自动重试的却反复弹 reauth；或该重新登录的却一直在空转 | `ConfigEntryNotReady` 与 `ConfigEntryAuthFailed` 语义用反 | 暂时连不上 → `ConfigEntryNotReady`（指数退避自动重试）；凭证失效 → `ConfigEntryAuthFailed`（触发 reauth） |
| 6 | 点了 UI 的「Enable debug logging」，自己的集成还是没日志 | 该按钮对自定义组件默认无效 | manifest 加 `"loggers": ["依赖库名"]`，并把 `custom_components.<domain>` 配到 debug |
| 7 | F5 启动后断点灰色、始终不命中 | HA 以冻结字节码启动、VS Code 默认跳过库代码、路径映射不对 | 用 `python3 -Xfrozen_modules=off -m homeassistant` 启动；`justMyCode: false`；`pathMappings` 指到 `custom_components/<domain>` |
| 8 | 配置表单里可选项留空，保存时抛 `vol.Invalid` | 可选 selector 没设 `default`，留空值过不了 voluptuous 校验 | 可选字段不设 `default`，或按条件动态组装 schema |
| 9 | 按旧教程在 devcontainer 里装 Mosquitto，发现镜像里没有 | 现行 core dev 镜像未预装 Mosquitto | 自行 `apt install mosquitto` 或另起 MQTT 容器，别照抄旧文档 |
| 10 | 明明发布了新版本，HACS 里一直显示旧版 | 只 push 了 tag 没建 Release；或未认证 GitHub API 被限流 | 必须创建 GitHub Release（版本取 release tag）；HACS 配 token 认证；下载后重启 HA 才生效 |

### 值得展开的四个坑

第 5、6、7、10 条最容易反复踩，单独说明。

**坑 5：两个异常别用反。** 这是整个笔记里语义最容易被混淆的一对。[ConfigEntry 异常语义](https://developers.home-assistant.io/docs/integration_fetching_data/) 里写得很明确：`ConfigEntryNotReady` 抛出后条目进入 `SETUP_RETRY`，HA 按 `min(2**tries*5, 最大等待)` 指数退避自动重试；`ConfigEntryAuthFailed` 则触发 reauth，让用户重新登录。用反的后果很典型：把认证失败当 `NotReady`，集成会永远重试却永远连不上；把暂时故障当 `AuthFailed`，用户会被反复叫起来输密码。

**坑 6：调试日志按钮为什么失灵。** UI 上的「Enable debug logging」只覆盖 core 组件。自定义组件默认级别是 warning，要在 [manifest](https://developers.home-assistant.io/docs/creating_integration_manifest/) 里加 `loggers` 键，把 requirements 依赖库的 logger 名列出来，这个按钮才会对你有用。

**坑 7：断点不命中是三个条件同时满足。** core issue #110623 归纳过：一是 HA 必须用 `-Xfrozen_modules=off` 启动，否则断点打在冻结的字节码上不会停；二是 VS Code 要设 `justMyCode: false`，否则 `site-packages` 里的集成代码被当成库跳过；三是 `pathMappings` 要把本地 `custom_components/<domain>` 映射到容器里对应的 `/config` 路径。

**坑 10：HACS 版本不更新的两个元凶。** 一是 [HACS 发布规则](https://hacs.xyz/docs/publish/start/)：版本号取自最新的 release tag，只 push tag 不创建 Release 是无效的；二是 HACS 靠 GitHub API 拉 release 数据，未认证会限流导致版本陈旧。另外装完新版本必须重启 HA 才生效。

> [!tip] 大白话
> 把两个异常想成电器说明书上的两类提示：`ConfigEntryNotReady` 是「正在开机，请稍候」，系统自己会重试；`ConfigEntryAuthFailed` 是「密码不对，请重新输入」，必须人来管。所以——用错异常，要么让 HA 无限空转，要么反复把用户从沙发上叫起来输密码。

## 最佳实践：7 条长期体检指标

排错解决「现在」，最佳实践保证「以后」。这 7 条大多来自官方硬性架构规则和官方维护者蓝本（`ludeeus/integration_blueprint`），照做能省掉未来大量的维护成本。

| # | 实践 | 为什么 | 适用场景 |
|---|------|--------|----------|
| 1 | 集成代码尽量薄，协议逻辑放独立 PyPI 库 | 官方硬性规则：集成内禁止包含协议特定代码，API 交互必须抽库 | 任何对接第三方 API 的集成 |
| 2 | 用 `entry.runtime_data` 存 client/coordinator | 优于 `hass.data[DOMAIN]`，随 entry 生命周期自动清理，不手动管 | HA 2024.8+，新建集成直接用 |
| 3 | 多实体共享一个 coordinator，`context=idx` 区分 | 一次轮询喂给所有实体，减少请求数；订阅/退订成对防泄漏 | 一台设备暴露多个 sensor |
| 4 | `_attr_` 类属性 + `SensorEntityDescription`（可加 `value_fn`） | 声明式定义实体，大量消除重复代码；`has_entity_name=True` 为强制项 | 字段相似的 sensor 平台 |
| 5 | reauth/reconfigure 用官方 helper | `_get_reauth_entry()` / `data_updates=` 更安全，避免 schema 演进丢数据 | 需要重新认证或改配置的集成 |
| 6 | 测试断言走核心接口 | 断言 `hass.states` / `hass.services` / registries，不碰内部细节，重构不破坏测试 | 所有集成测试 |
| 7 | 分发双 action：hassfest + hacs/action | hassfest 校验合规、hacs/action 校验 HACS 可用；manifest 6 必填字段齐备 | 上架 HACS 前必须配 |

> [!tip] 大白话
> 把最佳实践想成体检报告上的长期指标：血压、血糖、心率不会让你立刻修出一个 bug，但年年查、项项达标，集成就不会在某个深夜突然暴雷。所以——常见坑清单治「已发生的病」，最佳实践防「还没生的病」，两者合起来才是完整的保健方案。

## 小结：从零到可分发，我们走完了

本章小结：

- 10 个坑集中在五片雷区：manifest 字段、异步纪律、异常语义、调试配置、分发机制。
- 排错先对「症状」入座，再确认「原因」，最后按「修法」动手，不要跳过第二步直接改。
- 7 条最佳实践里，独立 PyPI 库、`entry.runtime_data`、核心接口断言是官方硬性规则，新建集成时就该用上。
- 调试三件套（`loggers` 键、`-Xfrozen_modules=off`、`justMyCode: false`）一次配好，之后 Debug 不再玄学。
- HACS 不更新先查两件事：有没有建 Release、GitHub API 有没有认证。

到这里，整本笔记走完了一条完整的路径：第 1 章认识集成，第 2 章搭好环境，第 3 章写出合法骨架，第 4 章做出配置流程，第 5 章暴露实体，第 6 章接入数据，第 7 章能测能调，第 8 章上架分发，第 9 章会排错。现在你拥有的不只是能跑的代码，而是一整套「从零到可分发」的方法论——下一个集成，只是换一张图纸，把这条路再走一遍。

> [!tip] 大白话
> 最后把整本笔记想成一次「从毛坯房到交付钥匙」的装修之旅：第 1 章画图纸，第 2 章进工地，第 3 到 6 章砌墙走线，第 7 章验收，第 8 章挂牌出租，第 9 章是入住后的保修卡。所以——别把这份排错清单背下来，把它贴在工位上，遇到问题对号入座，就够了。
