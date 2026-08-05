# ai-smart-home-system - 深度收集

> **阶段**: P2 深度收集
> **日期**: 2026-08-05
> **素材来源**: 桌面报告 HTML + 4 个探测 subagent（01_explore_result）+ 4 个深度收集 subagent + 官方文档/仓库核实
> **方向**: 端到端走通主线（一键部署 → 跨品牌接入 → AI 对话 → 场景自动化）

---

## 素材质量概览

- **官方文档/仓库**（高权重）: home-assistant.io（安装/REST API/Blueprint/Tuya/Gree）、DeepSeek API 文档（Models、Tool Calls、Thinking Mode）、XiaoMi/ha_xiaomi_home、wuwentao/midea_ac_lan、xZetsubou/hass-localtuya、mmalolepszy/hon-revived、basnijholt/adaptive-lighting
- **社区实证**（中权重，已标注）: HA Community（onboarding API 逆向、.storage 预置）、瀚思彼岸论坛、镜像源汇总（2026-05/07）、docker registry 端点实测
- **代码骨架**: Agent 已生成可运行代码到 `workspace/ai-smart-home-system/agent/`（py_compile 通过）
- **时效性修正**: 报告 6 处过时信息已识别并更新（见 §6）

---

## 1. 系统架构与部署选型

### 四层架构（报告确认，无需改动）

```
用户交互层（微信 / HA App / Web / 语音）
   ↓
智能体层（Python FastAPI Agent + DeepSeek Function Calling）
   ↓
核心平台层（Home Assistant Container：设备管控 + 自动化引擎）
   ↓
基础设施层（Docker Compose：HA + Agent + 可选 sidecar）
```

### 部署决策：Container 为主 + HAOS 为辅

- **官方镜像**: `ghcr.io/home-assistant/home-assistant:stable`（Docker Hub 旧镜像 2023.7 起弃用）；当前稳定版 **2026.7.2**
- **架构**: 2025.12 起仅支持 x86_64/aarch64（i386/armhf/armv7 EOL）；**Supervised 与 Core 安装方式已弃用**
- **前置**: Docker Engine 23.0+（官方明确 Docker Desktop 不可用）；`TZ=Asia/Shanghai` 必须显式；`--network=host` 官方推荐（mDNS/SSDP 发现）；`--privileged` 仅 USB/Zigbee 需要

---

## 2. 一键部署（install.sh + onboarding 自动化）

### 国内镜像链（2026-08 核实）

| 方案 | 状态 | 匿名 | 备注 |
|------|------|------|------|
| `ghcr.nju.edu.cn` | 探测可用（/v2/ 正常） | ✅ | 高校公益，优先教育网，进回退链首位 |
| `docker.m.daocloud.io/ghcr.io/...` | 探测可用 | ✅ | DaoCloud 反代，通用前缀替换 |
| `ghcr.1ms.run` | 探测可用 | ✅ | 社区 ghcr 代理 |
| `ghcr.io` 官方直连 | 大陆慢/易超时 | ✅ | 兜底 |
| `ota.hasscn.top` | 境外探测 403（限大陆），大陆需实测 | ✅ | HAOS-CN，放回退链末位 |
| 阿里云 ACR 个人版 | 新实例**不支持匿名拉取**，须 docker login | ❌ | 仅用于产品自有 agent 镜像分发 |

> **关键**: `registry-mirrors`（daemon.json）只对 Docker Hub 生效，对 ghcr.io 无效；ghcr 必须整体替换镜像名前缀。

### install.sh 骨架（核心步骤）

1. 环境检测：OS 发行版 + 架构（拒绝 32 位）+ Docker/compose 检测
2. 装 Docker：`get.docker.com --mirror Aliyun`，失败回退 `get.daocloud.io/docker`
3. 写 daemon.json（Docker Hub 加速：docker.1ms.run / docker.m.daocloud.io / docker.1panel.live）
4. ghcr 回退链 `pull_with_fallback`（每个 pull 加 `timeout 300`）
5. 交互写 `.env`（TZ / DEEPSEEK_API_KEY / HA_IMAGE / AGENT_IMAGE，chmod 600）
6. 写 docker-compose.yml → `docker compose up -d`
7. 等待就绪：探测 `http://127.0.0.1:8123/`（接受 200/302，超时 ≥600s）
8. 打印访问地址 + 引导下一步

### docker-compose.yml 关键点

- HA 服务：`image: ${HA_IMAGE}`、`network_mode: host`、`privileged`、`TZ`、卷 `./config:/config` + `/run/dbus`
- Agent sidecar：`image: ${AGENT_IMAGE}`、`network_mode: host`、env `HA_BASE_URL=http://127.0.0.1:8123`、`depends_on: homeassistant: condition: service_healthy`
- healthcheck：HA 官方镜像**无 curl**，用 `python3 urllib` 探测 8123 与 agent 8000

### HA 首次启动 onboarding 自动化（无头）

- **路径 A（推荐，社区实证 HA 2024.11.3）**: 调 `/api/onboarding/users` → `/auth/token` → `/api/onboarding/core_config` → `/api/onboarding/analytics` → `/api/onboarding/integration`。接口未文档化，必须做版本探测，失败回退浏览器向导
- **路径 B（兜底）**: 首次启动前预置 `.storage` 文件（auth / core.config / onboarding / person 等 + 预生成密码哈希）
- **config_flow 无头**: token 类集成（米家 LAN / 美的 / 海尔）可停 HA → 写 `.storage/core.config_entries` → 启动；OAuth 类（官方米家 / 涂鸦扫码）**必须人工授权**
- **产品 UX 建议**: 阶段 A 后台安装（无可感知人工）→ 阶段 B Agent 后台生成 admin 凭据 + 引导页展示 → 阶段 C 品牌接入卡片（分三档：纯后台 / 半后台 / 必须人工）

---

## 3. 跨品牌接入矩阵（核心章节）

| 品牌 | 集成 | 接入方式 | 人工环节 | 时效性风险 |
|------|------|----------|---------|-----------|
| 米家 | `xiaomi_home`（小米官方，22k⭐，非 core） | OAuth 2.0 网页登录（2025 起含 CAPTCHA）→ 选家庭/设备 | 小米账号登录 | vacuum `battery_level` 弃用告警截至 v0.4.7 未修复（HA 2026.8 移除）；LAN 控制需中枢网关 |
| 涂鸦 | 官方 `tuya`（云）+ `localtuya`（本地 fork） | 云：App 扫码 + User Code；本地：设备 IP+ID+local_key | 扫码/取 key | 涂鸦 IoT 后台密钥限时；门锁/摄像头不再提供 localKey；中国区 `openapi.tuyacn.com` 需 IP 白名单 |
| 美的 | `midea_ac_lan`（30+ 品类，全本地） | V1/V2 自动发现；V3 需云端一次取 token(128hex)+key(64hex) | V3 首次美的账号取 token | **V1 Token API 已关，NetHome Plus 陆续关闭**；新设备可能无法取 token，老 token 必须备份 |
| 格力 | 内置 `gree`（全本地轮询） | 自动发现 LAN | 设备需先经格力+ App 配网 | 低；内置缺 `hvac_action`，增强走社区版 |
| 海尔 | `hon-revived`（hOn 云 fork） | hOn 账号登录（邮箱密码） | hOn 账号 | 云 API 易变，"易碎"，作高级项 |
| 华为 | 无可靠路径 | — | — | 生态封闭；只给指引（Matter / 反向控制） |
| 兜底 | Matter / MQTT / Zigbee | 需 sidecar 容器（Zigbee/Thread 还需 USB 协调器） | 硬件 | 不适合纯云 MVP 默认 |

### MVP 预置清单（打进镜像，无 HACS）

1. `custom_components/xiaomi_home`（锁 tag v0.4.7）
2. 内置 `tuya`（云，随 Core 提供）+ `custom_components/localtuya`（本地）
3. `custom_components/midea_ac_lan`
4. 内置 `gree`
5. `custom_components/hon`（高级/易碎）
6. 华为：文档指引，不预置组件

### 品牌接入首次人工步骤（产品向导要覆盖）

米家 OAuth 登录 / 涂鸦扫码或取 key（tinytuya 或 iot.tuya.com）/ 美的 V3 取 token（失败回退抓包教程）/ 格力 Gree+ App 配网 / 海尔 hOn 登录。

---

## 4. 智能体实现（FastAPI + DeepSeek）

### API 事实核对

- **模型**: `deepseek-v4-flash`（$0.14/1M 输入、$0.28/1M 输出，缓存命中约便宜 50 倍）；`deepseek-v4-pro` 更强。**`deepseek-chat`/`deepseek-reasoner` 旧名已于 2026-07-24 停用**
- **base_url**: `https://api.deepseek.com`（OpenAI 兼容）
- **tool_choice**: V4 思考模式下 `"required"`/指定函数返回 400 → **统一用 `"auto"`** + 系统提示 + 应用层 N=1 循环
- **thinking**: 默认开启；工具调用后需回传 `reasoning_content` 否则 400 → MVP 用 `extra_body={"thinking":{"type":"disabled"}}` 关闭
- **HA REST**: LLAT（Bearer 后有空格）；`GET /api/states/{entity_id}`；`POST /api/services/{domain}/{service}`（返回 JSON 数组）

### 已生成代码（`workspace/ai-smart-home-system/agent/`）

- `main.py` — FastAPI（/health、/chat），N=1 tool-calling 循环，工具白名单 + 参数校验，`asyncio.to_thread` 包装 OpenAI 阻塞调用
- `tools.py` — HomeAssistantClient（httpx，get_state / call_service / ping）
- `entity_map.py` + `entity_map.yaml` — 实体映射 + rapidfuzz 模糊匹配（WRatio，score_cutoff=80）
- `Dockerfile`、`requirements.txt`、`.env.example`（DEEPSEEK_MODEL=deepseek-v4-flash）

### 安全要点

- 为 agent 建**专用受限 HA 用户** + LLAT（LLAT 无 scope = 全管理员权限）
- 工具函数名白名单（只允许 TOOL_HANDLERS 里的）+ 运行时参数校验
- 控制前查 state（unavailable/unknown）；brightness 量纲 0-255
- `.env` chmod 600，不入库

---

## 5. 场景模板与三层复制

### custom_components 预置

- 目录布局 `config/custom_components/<domain>/`（`__init__.py` + `manifest.json` + `config_flow.py`）
- 版本锁定：manifest `version` 对齐发布 tag；CI 校验防漂移；无 HACS = 无自动更新
- **绝不提交**: 设备 token、网关 key、客户凭据（`.env`/真实 `entity_map.yaml` gitignore）

### packages 场景

- `homeassistant: packages: !include_dir_named packages`；每个文件 key 必须是合法 domain
- 场景模式：`input_boolean`（开关）+ `script`（动作序列）+ `automation`（触发）
- 回家/离家/睡眠各一个 package；HA YAML 无变量 → 多客户用 `envsubst`/jinja2 构建期替换

### Blueprint

- 路径 `config/blueprints/automation/<author>/<file>.yaml`；`use_blueprint:` 实例化；无内置版本/自动更新
- adaptive_lighting 是 custom component（可预置，配 scheduler blueprint）；**`auto_climate` 不存在** → 用通用 climate blueprint 或自建

### 三层分离

`config.template/`（模板层，无密钥）→ `customers/<id>/`（`.env` + `entity_map.yaml`）→ 运行时 `/config`（install.sh 渲染生成）。实体引用由 codegen 按 entity_map 重写；`hass --script check_config` 校验。

---

## 6. 时效性修正清单（报告 vs 2026-08 现状）

| # | 报告说法 | 修正 | 状态 |
|---|---------|------|------|
| 1 | Supervised | → **Container 为主 + HAOS 为辅**（Supervised 2025.12 弃用） | ✅ 已采纳 |
| 2 | `deepseek-chat` | → **`deepseek-v4-flash`**（旧名 2026-07-24 停用） | ✅ 已采纳 |
| 3 | ACR 个人版镜像站 | → **不能匿名拉取**；ghcr 走代理链（ghcr.nju.edu.cn 等） | ✅ 已采纳 |
| 4 | 预置 xiaomi_gateway3 | → 米家官方 `xiaomi_home` | ✅ 已采纳 |
| 5 | `auto_climate` blueprint | → 不存在，需自建/替换 | ✅ 已采纳 |
| 6 | 华为可接入 | → 无可靠路径，只给指引 | ✅ 已采纳 |

---

## 7. 待实测 / 产品决策事项（P2→P3 需要留意）

1. **镜像链大陆实测**: ghcr.nju.edu.cn / ota.hasscn.top 在中国大陆家庭宽带的真实可用性
2. **xiaomi_home battery_level**: 是否已有 v0.4.8+ 修复（决定 HA Core 版本锁定策略）
3. **美的 V3 新设备 2026**: NetHome Plus Token 接口对中国区新设备是否仍可用（决定美的接入承诺）
4. **onboarding API**: 在 2026 stable（2026.7.x）上是否仍有效（决定 5 分钟承诺的边界）
5. **第三方工具依赖决策**: 米家 token 提取（Xiaomi-cloud-tokens-extractor）、美的取 token（msmart-ng）是否接受
6. **首版主推品牌组合**: 决定阶段 C 品牌向导工作量与 5 分钟承诺范围
7. **Agent 镜像分发通道**: ACR 私有（需 login）vs Docker Hub 公开 vs 自建 registry

---

## 8. 关键来源

- home-assistant.io: Linux/Container 安装、REST API、Blueprint、Tuya、Gree、onboarding、2023.7/2025.5 弃用公告
- api-docs.deepseek.com: Models & Pricing、Tool Calls、Thinking Mode（V4 变更）
- GitHub: XiaoMi/ha_xiaomi_home、wuwentao/midea_ac_lan（Issue #530）、xZetsubou/hass-localtuya、mmalolepszy/hon-revived、basnijholt/adaptive-lighting、deepseek-ai/DeepSeek-V3（Issue #1376）
- 社区: HA Community（onboarding API / .storage）、瀚思彼岸论坛、2026 镜像源汇总、docker registry 端点实测
- 现有笔记: [[Home Assistant 三种部署方式对比与选型.md]]（部署选型结论交叉验证）
