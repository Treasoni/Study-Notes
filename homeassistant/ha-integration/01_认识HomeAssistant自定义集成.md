---
title: "第 1 章：认识 Home Assistant 自定义集成"
tags:
  - HomeAssistant
  - 集成开发
  - 学习笔记
created: 2026-08-08
updated: 2026-08-08
status: 完成
source_project: home-assistant-integration
---

> [[HA集成开发指南|📑 目录]] | [[02_开发环境搭建|下一章 ➡️]]

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

---

> [[HA集成开发指南|📑 目录]] | [[02_开发环境搭建|下一章 ➡️]]

