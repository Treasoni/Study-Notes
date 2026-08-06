---
title: "基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建指南）"
tags:
  - Home-Assistant
  - 架构
  - 部署选型
  - Docker
  - 国内镜像
  - 部署
  - Docker-Compose
  - 一键部署
  - onboarding
  - 跨品牌接入
  - xiaomi_home
  - localtuya
  - midea_ac_lan
  - Matter
  - AI智能体
  - DeepSeek
  - FastAPI
  - 自动化
  - packages
  - Blueprint
  - 产品化
  - 部署分发
  - 时效性
created: 2026-08-05
updated: 2026-08-05
status: 已完成
source_project: ai-smart-home-system
---

# 基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建指南）

> 本文档是一份端到端实战构建指南，带你从零搭建一套基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统。全文 8 章按「一键部署 → 跨品牌接入 → AI 对话 → 场景自动化」主线组织：第 1-2 章先解决架构选型与国内镜像链，第 3-4 章用 install.sh 与 docker-compose 一条命令拉起 HA + Agent 并让首次启动不再需要浏览器，第 5 章把米家 / 涂鸦 / 美的 / 格力 / 海尔接入同一套系统，第 6 章用 FastAPI + DeepSeek Function Calling 实现自然语言控制，第 7 章用 packages 与 Blueprint 把场景模板化，第 8 章把整套系统产品化复制并盘点时效性风险。建议按章节顺序阅读，每章末尾都给出了与下一章的衔接。

## 目录

- [[#第一章 系统架构与部署选型：为什么是 Container 为主 + HAOS 为辅|第一章 系统架构与部署选型]]
- [[_part02#第二章 国内镜像链与 Docker 基础设施准备|第二章 国内镜像链与 Docker 基础设施准备]]
- [[_part02#第三章 一键部署：install.sh 与 docker-compose 编排|第三章 一键部署：install.sh 与 docker-compose 编排]]
- [[_part03#第四章 无头 onboarding：让 HA 首次启动不再需要浏览器|第四章 无头 onboarding：让 HA 首次启动不再需要浏览器]]
- [[_part03#第五章 跨品牌接入矩阵|第五章 跨品牌接入矩阵]]
- [[_part03#第六章 AI 智能体：FastAPI + DeepSeek Function Calling|第六章 AI 智能体：FastAPI + DeepSeek Function Calling]]
- [[_part04#第七章 场景模板与自动化：packages 与 Blueprint|第七章 场景模板与自动化：packages 与 Blueprint]]
- [[_part04#第八章 产品化复制与时效性风险|第八章 产品化复制与时效性风险]]

---

## 第一章 系统架构与部署选型：为什么是 Container 为主 + HAOS 为辅

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §1、§6（时效性修正 #1）
> 前置关联：[[Home Assistant 三种部署方式对比与选型.md]]

> [!summary] 本章回答三个问题
> 1. 这套系统长什么样？（四层架构地图）
> 2. 为什么不能照搬报告的 Supervised 方案？（官方弃用修正）
> 3. 为什么最终是「Container 为主 + HAOS 为辅」？

要交付一套「给非技术用户也能一键部署」的跨品牌 AI 智能家居系统，第一件事不是写代码，而是选对地基：HA 以哪种形态安装、Agent 放在哪一层、设备怎么被统一管起来。选错部署方式，后面所有「一条命令」「5 分钟承诺」都会在第一步就破功。本章先给你一张四层架构地图，再解释为什么官方已经弃用的 Supervised 不可能是答案，最后落到「Container 为主 + HAOS 为辅」这条主线，并说明它如何支撑后面每一章的动手任务。

### 1.1 四层架构总览

整个系统按职责切成四层，从上到下依次是用户交互层、智能体层、核心平台层、基础设施层：

```text
┌────────────────────────────────────────────────┐
│ 用户交互层    微信 / HA App / Web / 语音         │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ 智能体层       Python FastAPI Agent             │
│               + DeepSeek Function Calling       │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ 核心平台层     Home Assistant Container          │
│               （设备管控 + 自动化引擎）            │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ 基础设施层     Docker Compose                   │
│               （HA + Agent + 可选 sidecar）      │
└────────────────────────────────────────────────┘
```

四层拆分的价值在于每一层都能独立演进：换掉 DeepSeek 换成别的模型，不影响设备层；给用户加一个语音入口，不碰智能体核心逻辑；底层从一台 Docker 主机迁移到另一台，上层无感知。对产品而言，这意味着「可替换」和「可测试」。

每一层只干一件事，层与层之间通过定义好的接口（REST API / 工具调用）通信：

- **用户交互层**：用户唯一能感知的一层。微信、HA App、Web、语音音箱都挂在这里，只负责把用户的话转成一条「意图」，不直接碰设备。
- **智能体层**：系统的「大脑」。轻量 Python（FastAPI）进程接收自然语言，用 DeepSeek Function Calling 把「把客厅灯调暗」解析成结构化工具调用，再调 Home Assistant 的 REST API。这一层是「AI 智能家居」区别于「一堆品牌 App」的关键。
- **核心平台层**：Home Assistant Container。所有品牌设备都收敛到这里统一管理，自动化引擎（automation / script / Blueprint）也在这层跑。因为有这一层，上层不需要关心米家、涂鸦、美各自对应的私有协议。
- **基础设施层**：Docker Compose 把 HA、Agent、可选 sidecar 编排到一起，一条命令拉起整套系统。「一键部署」的承诺就落在这层。

用一句话描述一条控制指令如何从对话走到设备执行：

> 用户在微信说「把客厅灯调暗」→ 智能体层把它交给 DeepSeek 解析成工具调用（`light.turn_on` + brightness）→ 通过 REST API 发给核心平台层 → HA 查实体状态、调用对应品牌设备的 service → 设备执行，结果沿原路返回对话。

### 1.2 官方部署方式现状与 Supervised 弃用修正

#### 官方弃用时间线

Home Assistant 官方安装方式在 2025 年发生了结构性变化[深度收集 §1、§6](../02_deep_research.md)：

- **2025-05-22**：官方发布弃用公告；
- **2025.12**：Supervised 与 Core 安装方式正式弃用；
- **2025.12 起**：仅支持 x86_64 / aarch64 架构（i386 / armhf / armv7 已 EOL）。

这意味着任何以 Supervised 为底座的方案，从 2025.12 起都站在一条官方不再维护的路径上。桌面报告最终决策选的是 HA Supervised，而本项目核心约束是「面向非技术用户一键部署」——把客户放到官方已弃用的路径上，后续升级、安全补丁都会变成长期负担。所以报告方案必须修正，这是本章选型逻辑的出发点。

#### 为什么「非技术用户一键部署」排除了 Supervised

[[Home Assistant 三种部署方式对比与选型.md]] 里已经对比过三种方式，这里只看结论：Supervised 的定位是把整台主机交给 HA 来管，天然不适合作为可脚本化、可复制的交付渠道。而 Container 是官方正式路径，HA 作为普通容器被 Docker 托管，天然适合自动化：HA Core 与 Agent 写进同一个 `docker-compose.yml`，由 `install.sh` 一条命令拉起整套系统，正好命中「一键部署」。

这次弃用对本项目的意义不只是「换一种安装方式」，它直接决定了 `install.sh` 的形态：因为 Container 是官方正式路径，HA 只是一个普通容器，我们才能把 HA Core、Agent（甚至未来的 sidecar）写进同一个 compose 文件里用一条命令交付；如果走 Supervised，`install.sh` 就会退化成「帮用户装一个操作系统 + 引导 HA 安装向导」，既不可复现也不可审计。另外要注意，Supervised 只是报告 6 处过时信息中的第 1 处，完整清单会在第 8 章 8.3 节统一回顾。

> [!warning] 别再用 Supervised 做交付渠道
> Supervised 已弃用（公告 2025-05-22，2025.12 生效）。任何基于它的教程、报告结论都要先做时效性修正——这是本项目与桌面报告最大的决策分歧点。

### 1.3 Container vs HAOS 取舍

弃用 Supervised 之后，官方还剩两条可用路径：Container 与 HAOS。本项目「Container 为主 + HAOS 为辅」的分工如下[深度收集 §1](../02_deep_research.md)：

- **Container（主）**：官方正式路径，HA 以容器形态运行，镜像为 `ghcr.io/home-assistant/home-assistant:stable`（Docker Hub 旧镜像自 2023.7 起已弃用，当前稳定版 2026.7.2）。HA Core 与 Agent 同 compose 编排，`install.sh` 一条命令完成部署。
- **HAOS（辅）**：「专机专用 / 完全非技术用户」场景的替代分发渠道。当客户愿意用一台专用主机跑 HA、完全不想碰命令行时，HAOS 是比 Container 更省心的交付形态。

| 维度 | Container（主） | HAOS（辅） |
|------|----------------|-----------|
| 官方定位 | 正式路径，官方镜像分发 | 专机专用 / 完全非技术用户场景的替代分发渠道 |
| 核心形态 | 容器化应用，Docker 托管 | 整机系统 |
| 部署动作 | docker compose 一条命令 | 专用主机安装 |
| 与 Agent 集成 | 同 compose 编排 sidecar | 不作为本项目主线编排 |
| 适用前提 | Docker Engine 23.0+（Docker Desktop 不可用） | x86_64 / aarch64 专用主机 |

无论走哪条路，都有两个共享的硬性前置：

- **Docker Engine 23.0+**（官方明确 Docker Desktop 不可用）；
- **2025.12 起仅 x86_64 / aarch64**——32 位设备（i386 / armhf / armv7）已 EOL，老硬件跑不了新版本。

另外，Container 路线有 3 个安装时就要记住的参数（第 3 章会用到）：

- `TZ=Asia/Shanghai` 必须显式设置；
- `--network=host` 是官方推荐，mDNS / SSDP 设备发现依赖它；
- `--privileged` 仅在需要 USB / Zigbee 设备时开启。

> [!note] 为什么不是「Container 或 HAOS」二选一
> 两者服务的人群不同：Container 服务「已有 Docker 主机、想把 HA 和 Agent 一起编排」的用户，HAOS 服务「愿意专机专用、完全不想碰命令行」的用户。本项目主线是前者，HAOS 作为后者的备用分发渠道，所以是「主 + 辅」而不是二选一。

> [!tip] 什么时候切到 HAOS
> 当交付对象没有可用的 Docker 主机、也完全不想维护命令行时，在专用主机（x86_64 / aarch64 迷你主机）上以整机系统形态安装 HAOS 再交给客户，是比教他敲 `install.sh` 更现实的路径。它仍然满足 2025.12 起的架构前提，但不适合与 Agent 做同 compose 编排。

### 1.4 选型结论与阅读地图

**最终结论：Container 为主 + HAOS 为辅。** 归纳成三条理由：

1. Supervised 已弃用，不能作为面向非技术用户的交付渠道；
2. Container 满足「一键部署 + 多组件编排」——HA Core 与 Agent 同 compose 编排，`install.sh` 一条命令；
3. HAOS 覆盖「专机专用 / 完全非技术用户」场景，作为替代分发渠道兜底。

本笔记共 8 章，是一条端到端主线。建议带着「每个章节补上系统哪一块」来读，而不是当成碎片教程：

| 章节 | 内容 | 补上系统哪一块 |
|------|------|----------------|
| 第 1 章（本章） | 系统架构与部署选型 | 整体地图与选型理由 |
| 第 2 章 | 国内镜像链与 Docker 基础设施准备 | 基础设施层：先解决「镜像拉不动」 |
| 第 3 章 | 一键部署：install.sh 与 docker-compose | 基础设施层 + 核心平台层上线 |
| 第 4 章 | 无头 onboarding | 核心平台层首次启动自动化 |
| 第 5 章 | 跨品牌接入矩阵 | 核心平台层的设备接入能力 |
| 第 6 章 | AI 智能体：FastAPI + DeepSeek | 智能体层 |
| 第 7 章 | 场景模板与自动化 | 核心平台层的自动化引擎 |
| 第 8 章 | 产品化复制与时效性风险 | 把整条链路变成产品 |

### 本章小结

- 四层架构 = 用户交互层 → 智能体层 → 核心平台层 → 基础设施层；一条控制指令从对话走到设备执行要贯穿这四层。
- Supervised 已弃用（2025-05-22 公告 → 2025.12 生效），不能作为面向非技术用户的交付渠道。
- 选型结论 = Container 为主 + HAOS 为辅：Container 负责一键编排 HA + Agent，HAOS 覆盖专机专用场景。
- 两个部署方式共享硬性前置：Docker Engine 23.0+（Docker Desktop 不可用）、2025.12 起仅 x86_64 / aarch64。
- 全笔记 8 章 = 一条端到端主线，本章是地图，后续每章补上系统的一块。

---

下一章从第一道真实卡点开始：在国内网络环境下，官方镜像 `ghcr.io` 经常拉不动。你会弄明白为什么 `daemon.json` 的 `registry-mirrors` 对 ghcr 无效，以及如何用「镜像名前缀整体替换 + 回退链」把它稳定拉下来。

![[_part02]]

![[_part03]]

![[_part04]]
