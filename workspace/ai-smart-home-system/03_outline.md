---
title: 基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统（实战构建指南）- 大纲
type: outline
status: 待确认
project: ai-smart-home-system
created: 2026-08-05
---

## 学习笔记大纲：《基于 Home Assistant 的跨品牌 AI 智能家居一键部署系统》

> 笔记类型：实战构建指南（practice）
> 主线：端到端走通（一键部署 → 跨品牌接入 → AI 对话 → 场景自动化）
> 预计总篇幅：约 30,000 字
> 章节数：8
> 层级：章 → 节 → 小节（≤3 级）
> 素材来源：`02_deep_research.md` 的 §1-§8 各节

---

### 第一章：系统架构与部署选型：为什么是 Container 为主 + HAOS 为辅

- **篇幅**：约 2500 字
- **素材引用**：§1、§6（时效性修正 #1）
- **代码示例**：无（含架构示意图）
- **学习目标**：让读者先建立整体地图，理解「为什么不用 Supervised」，为后续一键部署奠定选型理由
- **章节结构**：
  - 1.1 四层架构总览
    - 用户交互层（微信 / HA App / Web / 语音）→ 智能体层 → 核心平台层 → 基础设施层
    - 数据流：一句话描述一条控制指令如何从对话走到设备执行
  - 1.2 官方部署方式现状与 Supervised 弃用修正
    - 官方弃用时间线（2025-05-22 公告 → 2025.12 弃用 Supervised 与 Core 安装）
    - 报告原方案（Supervised）为何不适用本项目的「非技术用户一键部署」约束
  - 1.3 Container vs HAOS 取舍
    - Container：官方正式路径、HA Core + Agent 同 compose 编排、一条命令部署
    - HAOS：「专机专用 / 完全非技术用户」场景的替代分发渠道
    - 硬性前置：Docker Engine 23.0+（Docker Desktop 不可用）、2025.12 起仅 x86_64/aarch64
  - 1.4 选型结论与阅读地图
    - 本笔记的端到端章节路线，读者应带着「每个章节补上系统哪一块」来读

---

### 第二章：国内镜像链与 Docker 基础设施准备

- **篇幅**：约 3000 字
- **素材引用**：§2（国内镜像链）、§6（#3）、§7（#1、#7）
- **代码示例**：有（daemon.json、pull_with_fallback 镜像回退函数、镜像前缀映射表）
- **学习目标**：解决「国内网络下镜像拉不动」这一第一个真实卡点，掌握 ghcr 整体替换而非 registry-mirrors 的认知
- **章节结构**：
  - 2.1 关键认知：registry-mirrors 只对 Docker Hub 生效，对 ghcr.io 无效
    - 为什么必须「整体替换镜像名前缀」而不是配 daemon.json
  - 2.2 ghcr 回退链实测与优先级
    - 优先级：ghcr.nju.edu.cn → docker.m.daocloud.io/ghcr.io/... → ghcr.1ms.run → 官方直连兜底 → ota.hasscn.top
    - 每个 pull 加 timeout 300，失败自动切下一跳
  - 2.3 Docker Hub 加速配置
    - daemon.json 写法（docker.1ms.run / docker.m.daocloud.io / docker.1panel.live）
  - 2.4 阿里云 ACR 与产品镜像分发
    - 个人版新实例不支持匿名拉取，必须 docker login
    - 定位：只用于「产品自有 agent 镜像」分发，不作为 ghcr 替代
  - 2.5 前置环境清单
    - OS/架构检测、Docker Engine 23.0+、TZ=Asia/Shanghai、network=host、privileged 仅 USB/Zigbee 需要

---

### 第三章：一键部署：install.sh 与 docker-compose 编排

- **篇幅**：约 5000 字
- **素材引用**：§2（install.sh 骨架、docker-compose 关键点）、§7（#4）
- **代码示例**：有（install.sh 全量骨架、docker-compose.yml、healthcheck、.env 模板）
- **学习目标**：让读者能读懂、改造并复现「一条命令部署 HA + Agent」
- **章节结构**：
  - 3.1 install.sh 逐段拆解（8 个步骤）
    - 环境检测 → 装 Docker（get.docker.com --mirror Aliyun / 回退 daocloud）→ 写 daemon.json → pull_with_fallback → 交互写 .env → compose up -d → 就绪探测（接受 200/302，超时 ≥600s）→ 打印访问地址
  - 3.2 docker-compose.yml 关键配置
    - HA 服务：image ${HA_IMAGE}、network_mode host、TZ、卷 ./config:/config + /run/dbus
    - Agent sidecar：image ${AGENT_IMAGE}、env HA_BASE_URL、depends_on + service_healthy
  - 3.3 healthcheck 的无 curl 方案
    - HA 官方镜像无 curl，用 python3 urllib 探测 8123 与 agent 8000
  - 3.4 .env 交互与敏感信息保护
    - TZ / DEEPSEEK_API_KEY / HA_IMAGE / AGENT_IMAGE，chmod 600，不入库
  - 3.5 常见坑与排错
    - 镜像名前缀替换、timeout 设置、首次启动慢、compose 版本兼容

---

### 第四章：无头 onboarding：让 HA 首次启动不再需要浏览器

- **篇幅**：约 3000 字
- **素材引用**：§2（onboarding 自动化）、§7（#4）
- **代码示例**：有（onboarding API 调用序列、.storage 预置 JSON 示例）
- **学习目标**：掌握「面向非技术用户的 5 分钟承诺」的技术实现边界，知道什么能自动化、什么必须人工
- **章节结构**：
  - 4.1 为什么需要无头 onboarding
    - 非技术用户不能面对 HA 浏览器向导；5 分钟承诺的技术边界
  - 4.2 路径 A（推荐）：onboarding API 调用序列
    - /api/onboarding/users → /auth/token → /api/onboarding/core_config → /api/onboarding/analytics → /api/onboarding/integration
    - 接口未文档化，必须做版本探测，失败回退浏览器向导
  - 4.3 路径 B（兜底）：.storage 文件预置
    - auth / core.config / onboarding / person + 预生成密码哈希
  - 4.4 config_flow 无头与人工环节分类
    - token 类集成（米家 LAN / 美的 / 海尔）可写 .storage/core.config_entries
    - OAuth 类（官方米家 / 涂鸦扫码）必须人工授权
  - 4.5 产品 UX 三阶段设计
    - A 后台安装（无可感知人工）→ B Agent 后台生成 admin 凭据 + 引导页 → C 品牌接入卡片（纯后台 / 半后台 / 必须人工三档）

---

### 第五章：跨品牌接入矩阵（核心章节）

- **篇幅**：约 5500 字
- **素材引用**：§3（整节）、§6（#4、#6）、§7（#2、#3、#5、#6）
- **代码示例**：有（configuration.yaml 集成配置、custom_components 预置目录布局、各品牌接入参数）
- **学习目标**：让读者拿到一张「可照着操作」的跨品牌接入地图，理解 MVP 优先级与各品牌时效性风险
- **章节结构**：
  - 5.1 接入矩阵总览（表格，见下）
  - 5.2 米家：xiaomi_home（官方，22k⭐，非 core）
    - OAuth 2.0 网页登录（2025 起含 CAPTCHA）、选家庭/设备
    - 风险：vacuum battery_level 弃用告警 v0.4.7 未修复；LAN 控制需中枢网关
  - 5.3 涂鸦：官方 tuya（云） vs localtuya（本地）
    - 云：App 扫码 + User Code；本地：设备 IP + ID + local_key
    - 风险：后台密钥限时；门锁/摄像头不再提供 localKey；中国区 openapi.tuyacn.com 需 IP 白名单
  - 5.4 美的：midea_ac_lan（30+ 品类，全本地）
    - V1/V2 自动发现；V3 需云端取 token(128hex)+key(64hex)
    - 风险：V1 Token API 已关、NetHome Plus 陆续关闭，老 token 必须备份
  - 5.5 格力与海尔：内置 gree 与 hon-revived
    - gree：全本地轮询、缺 hvac_action；hon-revived：hOn 云 fork、易碎作高级项
  - 5.6 华为与兜底方案
    - 华为无可靠路径，只给指引（Matter / 反向控制）
    - 兜底：Matter / MQTT / Zigbee，需 sidecar 容器与 USB 协调器，不适合纯云 MVP 默认
  - 5.7 MVP 预置清单与首次人工步骤
    - 打进镜像的 custom_components（xiaomi_home 锁 tag v0.4.7 / tuya / localtuya / midea_ac_lan / gree / hon），无 HACS
    - 产品向导要覆盖的各品牌首次人工步骤清单

**接入矩阵速览**（章节内完整表格占位，写作时按 §3 表格扩写）：

| 品牌 | 集成 | 接入方式 | 人工环节 | 时效性风险 |
|------|------|----------|----------|------------|
| 米家 | xiaomi_home（官方） | OAuth 2.0 网页登录（含 CAPTCHA） | 小米账号登录 | battery_level 弃用未修复；LAN 需中枢网关 |
| 涂鸦 | tuya（云）+ localtuya（本地） | App 扫码 + User Code / IP+ID+local_key | 扫码/取 key | 密钥限时；中国区需 IP 白名单 |
| 美的 | midea_ac_lan（全本地） | V1/V2 自动发现；V3 云端取 token+key | 美的账号取 token | V1 Token API 已关；NetHome Plus 关闭中 |
| 格力 | 内置 gree（本地轮询） | 自动发现 LAN | 需格力+ App 先配网 | 低；缺 hvac_action |
| 海尔 | hon-revived（hOn 云） | hOn 邮箱密码登录 | hOn 账号 | 云 API 易变，易碎 |
| 华为 | 无可靠路径 | — | — | 生态封闭，只给指引 |
| 兜底 | Matter / MQTT / Zigbee | sidecar 容器（Zigbee 需 USB 协调器） | 硬件 | 不适合纯云 MVP 默认 |

---

### 第六章：AI 智能体：FastAPI + DeepSeek Function Calling

- **篇幅**：约 5000 字
- **素材引用**：§4（整节）、§6（#2）、§7（#4、#7）
- **代码示例**：有（main.py、tools.py、entity_map.py / entity_map.yaml、Dockerfile、requirements.txt、.env.example）
- **学习目标**：让读者能独立实现并改造「自然语言 → 设备控制」的 Agent，避开 DeepSeek V4 的已知坑
- **章节结构**：
  - 6.1 API 事实核对
    - deepseek-v4-flash（$0.14/1M in、$0.28/1M out，缓存命中约省 50 倍）；deepseek-chat / deepseek-reasoner 旧名已停用
    - base_url 为 OpenAI 兼容端点；tool_choice 在 V4 思考模式下必须用 auto（required/指定函数返回 400）
    - thinking 默认开启，MVP 用 extra_body 关闭，避免 reasoning_content 回传问题
  - 6.2 Agent 主循环：main.py
    - FastAPI（/health、/chat）、N=1 tool-calling 循环、工具白名单 + 参数校验、asyncio.to_thread 包装阻塞调用
  - 6.3 工具层：tools.py
    - HomeAssistantClient（httpx）：get_state / call_service / ping；LLAT Bearer 后有空格
  - 6.4 实体映射：entity_map.py + entity_map.yaml
    - 口语别名 → 实体 ID，rapidfuzz WRatio 模糊匹配（score_cutoff=80）
  - 6.5 安全设计
    - 专用受限 HA 用户 + LLAT（LLAT 无 scope = 全管理员权限）
    - 工具函数名白名单、运行时参数校验、控制前查 state（unavailable/unknown）、brightness 量纲 0-255、.env chmod 600

---

### 第七章：场景模板与自动化：packages 与 Blueprint

- **篇幅**：约 3500 字
- **素材引用**：§5（custom_components 预置 / packages / Blueprint）、§6（#5）
- **代码示例**：有（packages/*.yaml 场景、blueprint YAML、envsubst/jinja2 替换模板）
- **学习目标**：让读者掌握「场景怎么模板化、怎么复制到多个客户」的 YAML 工程方法
- **章节结构**：
  - 7.1 custom_components 预置布局与版本锁定
    - config/custom_components/<domain>/（__init__.py + manifest.json + config_flow.py）
    - 无 HACS = 无自动更新；manifest version 对齐 tag，CI 校验防漂移
    - 绝不提交设备 token / 网关 key / 客户凭据
  - 7.2 packages 场景模式
    - homeassistant: packages: !include_dir_named packages；文件 key 必须是合法 domain
    - 回家 / 离家 / 睡眠：input_boolean（开关）+ script（动作序列）+ automation（触发）
  - 7.3 Blueprint 使用与限制
    - config/blueprints/automation/<author>/<file>.yaml；use_blueprint: 实例化
    - auto_climate 不存在 → 用通用 climate blueprint 或自建
  - 7.4 YAML 无变量问题的构建期替换
    - 多客户用 envsubst / jinja2 在构建期替换实体引用

---

### 第八章：产品化复制与时效性风险

- **篇幅**：约 3000 字
- **素材引用**：§5（三层分离）、§6（整节时效性修正清单）、§7（待决策事项）、§8（关键来源）
- **代码示例**：有（三层目录结构、git clone + install.sh 复制流程）
- **学习目标**：让读者理解「一个人做出来 → 复制给多个客户」的工程策略，以及哪些结论会随时间失效
- **章节结构**：
  - 8.1 三层分离复制策略
    - config.template/（模板层，无密钥）→ customers/<id>/（.env + entity_map.yaml）→ 运行时 /config（install.sh 渲染生成）
    - 实体引用由 codegen 按 entity_map 重写；hass --script check_config 校验
  - 8.2 三种分发渠道对比
    - git clone + install.sh / HA Blueprint 导入 / Docker 预打包镜像
  - 8.3 时效性修正清单回顾
    - 报告 6 处过时信息修正（Supervised、deepseek-v4-flash、ACR、xiaomi_home、auto_climate、华为）及其对本项目的意义
  - 8.4 待实测与产品决策事项（7 项）
    - 镜像链大陆实测 / xiaomi_home battery_level 修复 / 美的 V3 token / onboarding API 在 2026.7.x 有效性 / 第三方工具依赖取舍 / 首版主推品牌组合 / Agent 镜像分发通道
    - 阅读与维护建议：按 §8 关键来源追踪上游变更节奏

---

## 学习路径说明

### 前置要求
- 熟悉 Home Assistant 基础概念（entity、service、automation、configuration.yaml）
- 会使用 Docker 基础命令（run / compose），理解容器、镜像、卷
- 有 Python 基础，能读懂 FastAPI 异步代码
- 有一台可运行 Docker 的 Linux/x86_64 或 aarch64 主机（生产建议，非仅学习可放宽）
- 了解 LLM API 的基本调用方式（OpenAI 兼容格式）

### 学完能做什么
- 照着笔记从零复现「一键部署 + 跨品牌接入 + AI 对话 + 场景自动化」完整系统
- 读懂并改造 install.sh、docker-compose.yml、Agent 代码与 entity_map
- 独立接入米家 / 涂鸦 / 美的 / 格力 / 海尔等主流品牌，并预判各自时效性风险
- 用 packages 与 Blueprint 制作回家 / 离家 / 睡眠场景，按 entity_map 重写实体引用
- 用三层分离策略为多个客户复制部署，跑通 check_config 校验

### 建议学习顺序
- 按第一到第八章顺序阅读，每章完成对应的动手任务后再进下一章
- 第 1-2 章为地基（1-2 天）：看懂架构与镜像链，动手配好环境
- 第 3-4 章为部署（2-3 天）：跑通 install.sh + docker-compose + 无头 onboarding，目标「一条命令起系统」
- 第 5 章为核心攻坚（3-5 天）：至少实测 1-2 个品牌的完整接入流程
- 第 6 章为智能体（2-3 天）：跑通一个「对话 → 开灯」的最小闭环
- 第 7-8 章为收尾（2-3 天）：制作场景模板与三层复制，重读时效性风险清单
- 总计建议 10-16 天；若只学核心链路（3→5→6）可压缩到 4-6 天
