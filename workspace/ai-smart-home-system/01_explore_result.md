# ai-smart-home-system - 探测结果

> **阶段**: P1 探测式收集
> **日期**: 2026-08-05
> **方式**: 4 个 subagent 并行探测（Agent 实现 / HA Container 部署+国内适配 / 场景模板+组件打包 / 跨品牌主流集成矩阵）
> **用户确认方向**: 端到端走通主线（一键部署 → 跨品牌接入 → AI 对话 → 场景自动化），跨品牌接入为核心章节

---

## 一、报告时效性修正（必须更新的过时信息）

| # | 报告说法 | 2026-08 现状 | 影响 |
|---|---------|-------------|------|
| 1 | HA 部署选 Supervised | **Supervised 已于 2025.12 弃用**；官方仅 HAOS 与 Container 两条正式路径 | 部署改为 **Container 为主 + HAOS 为辅**（已确认） |
| 2 | LLM 用 `deepseek-chat` | **`deepseek-chat` 已于 2026-07-24 停用**，须改用 `deepseek-v4-flash` / `deepseek-v4-pro` | Agent 代码、install.sh 的 model 参数全部要改 |
| 3 | 镜像源用 `registry.cn-hangzhou.aliyuncs.com` ACR 个人版 | **2024-09-09 起新 ACR 个人版实例不支持匿名拉取**，不能做公开镜像站 | HA 官方镜像走 `ota.hasscn.top` 等 ghcr 代理；ACR 仅用于产品自有 agent 镜像分发 |
| 4 | 预置 `custom_components/xiaomi_gateway3` | 米家官方推荐 `xiaomi_home`（22k⭐，云默认）；gateway3 云登录 2025 年频繁故障 | 品牌矩阵需重排预置顺序 |
| 5 | 场景含 `auto_climate` blueprint | **未找到名为 auto_climate 的规范 blueprint** | 需要换用通用 climate blueprint 或自建 |
| 6 | 华为/鸿蒙可接入 | **华为生态基本无 HA 接入路径**（封闭） | 华为设备给出指引而非预置组件 |

## 二、各方向探测汇总

### 1. 智能体实现（Agent）

- **DeepSeek 现状**: 模型 `deepseek-v4-flash`（$0.14/1M 输入、$0.28/1M 输出，缓存命中便宜约 50 倍）；`deepseek-v4-pro` 更强。Base URL `https://api.deepseek.com`。Tool Calls 支持 `tools` 最多 128 个函数、`tool_choice` auto/required/指定函数。低延迟可 `thinking: disabled` 关思考。
- **HA REST API**: Long-Lived Access Token（LLAT）；`GET /api/states`、`POST /api/services/<domain>/<service>`；host 网络下 agent 用 `http://127.0.0.1:8123/api`。
- **Tool 循环**: 最小模式 = OpenAI SDK + function calling，单轮 N=1（工具调用 + 最终答复），`tool_choice="none"` 收尾；参数需运行时校验（模型可能幻觉/非法 JSON）。
- **实体映射推荐**: `entity_map.yaml` + 模糊匹配（确定性高、成本低、不幻觉 entity_id），而非把全部实体塞进 prompt。
- **安全坑**: LLAT 无 scope = 全管理员权限 → 给 agent 建专用受限 HA 用户；`POST /api/states` 不驱动设备；`brightness` 量纲 0-255。

### 2. HA Container 部署 + 国内适配

- **官方镜像**: `ghcr.io/home-assistant/home-assistant:stable`（Docker Hub 旧镜像已弃用）；当前稳定版 2026.7.2；2025.12 起仅支持 x86_64/aarch64。
- **前置**: Docker Engine 23.0+（官方明确 Docker Desktop 不可用）；`--network=host` 官方推荐；`TZ=Asia/Shanghai` 必须显式设置。
- **国内拉取**: 官方无中国镜像。社区方案：`ota.hasscn.top`（HAOS-CN ghcr 代理，匿名，最贴合 HA）→ `ghcr.nju.edu.cn`（存疑）→ 直连 ghcr 兜底。`registry-mirrors` 只对 Docker Hub 生效，ghcr 必须替换镜像名前缀。
- **install.sh 结构**: 检测 OS/架构（拒绝 32 位）→ 装 Docker（`get.docker.com --mirror Aliyun`）→ 交互写 `.env` → 写 compose → `pull` → `up -d` → 等待 `127.0.0.1:8123` 就绪 → 引导 onboarding。
- **坑**: host 网络与 `ports:` 冲突；防火墙需放行 8123；`--privileged` 给 USB 硬件；首次启动有 HA 网页向导。

### 3. 场景模板 + custom_components 打包

- **无 HACS 打包**: `/config/custom_components/<domain>/`；镜像内 COPY 或卷挂载；必须锁版本（`manifest.json` version 对齐发布 tag）；**绝不提交 token/key**。
- **packages 场景**: `homeassistant: packages: !include_dir_named packages`；每个文件 key 必须是合法 domain（`automation:`/`script:`/`input_boolean:`）；HA YAML 无变量，多客户靠 `envsubst`/jinja2 构建期替换。
- **场景模式**: `input_boolean`（场景开关）+ `script`（动作序列）+ `automation`（触发绑定）。回家/离家/睡眠各一个 package。
- **Blueprint**: 路径 `config/blueprints/automation/<author>/<file>.yaml`；`use_blueprint:` 实例化；无内置版本/自动更新；adaptive_lighting 是 custom component（可预置）。
- **三层分离**: `config.template/`（模板层）+ `customers/<id>/`（客户 .env + entity_map.yaml）+ 运行时 `/config`（install.sh 渲染生成）。

### 4. 跨品牌主流集成矩阵（用户强调的核心）

| 品牌 | 主集成 | 本地/云端 | 覆盖 | 风险 |
|------|--------|----------|------|------|
| 米家 | `xiaomi_home`（小米官方，22k⭐） | 默认云端；本地仅 Central Hub | 绝大多数品类；BLE/红外不支持 | 曾两次弃用告警（2026.1/8） |
| 涂鸦 | 内置 `tuya`（云）+ `hass-localtuya`（本地 fork） | 云 / 本地 | 所有 "Powered by Tuya" 设备（含 TCL/创维/长虹家电） | Tuya IoT 后台密钥限时（约 1 个月） |
| 美的 | `midea_ac_lan`（30+ 品类） | 全本地 | 空调/风扇/热水器/洗衣机/冰箱 + OEM | **v1 LAN token API 正在关闭**，新 V3 设备接入风险 |
| 格力 | 内置 `gree`（全本地） | 本地 | 空调 + 面板开关 | 内置版缺 `hvac_action`；需先厂商 App 配网 |
| 海尔 | `hon-revived`（hOn 云 fork） | 纯云端 | 洗衣机/空调/热水器等 | 云 API 易变，"易碎"，作高级项 |
| 华为 | 无可靠路径 | — | 基本无法直接接入 | 生态封闭 |
| 兜底 | Matter / MQTT / Zigbee | 需 sidecar 容器（Zigbee/Thread 还需 USB 协调器） | 标准设备 / DIY | 不适合纯云 MVP 默认 |

**MVP 预置顺序（无 HACS）**: ① `xiaomi_home` → ② 官方 `tuya`（云）+ `hass-localtuya` → ③ `midea_ac_lan` → ④ 内置 `gree` → ⑤ `hon-revived`（高级/易碎）。

## 三、待深入问题（P2 深度收集要解决）

1. `ota.hasscn.top` / `ghcr.nju.edu.cn` 的 2026 实时可用性与稳定性（需实测镜像链）
2. `xiaomi_home` 是否已修复弃用告警、能否用固定版本镜像长期锁定
3. 美的 v1 LAN token API 关闭进度：新 V3 设备 2026 年还能否一次性取 token
4. 涂鸦本地 key 扫码获取在中国区是否仍可用
5. 全 headless 一键部署的可行性（custom_component 的 config flow 能否零交互预配置）

## 四、来源

- DeepSeek API 文档 / 更新日志（V4 与旧名停用公告）
- home-assistant.io 官方 Linux/Container 安装、REST API、Blueprint、版本号
- XiaoMi/ha_xiaomi_home、xZetsubou/hass-localtuya、chemelli74/midea_ac_lan、mmalolepszy/hon-revived、basnijholt/adaptive-lighting 等仓库
- HAOS-CN（ota.hasscn.top）、阿里云 ACR 个人版限制官方文档
- 瀚思彼岸论坛、HA Community、Blueprints Exchange
