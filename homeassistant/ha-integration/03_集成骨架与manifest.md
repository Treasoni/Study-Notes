---
title: "第 3 章：集成骨架与 manifest.json"
tags:
  - HomeAssistant
  - 集成开发
  - 学习笔记
created: 2026-08-08
updated: 2026-08-08
status: 完成
source_project: home-assistant-integration
---

> [[02_开发环境搭建|⬅️ 上一章]] | [[HA集成开发指南|📑 目录]] | [[04_ConfigFlow配置流程|下一章 ➡️]]

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

---

> [[02_开发环境搭建|⬅️ 上一章]] | [[HA集成开发指南|📑 目录]] | [[04_ConfigFlow配置流程|下一章 ➡️]]

