---
title: "客户A · 部署 Runbook"
tags:
  - 智能家居/项目/客户A
  - 内部实施
customer: 客户A
status: 草稿
created: 2026-08-06
updated: 2026-08-06
---

# 客户A · 部署 Runbook

> 一键部署是「成品交付」不是「一条脚本」：NAS 建虚拟机 → 引导 → 配置。分步执行，每步验证。技术细节复用笔记：镜像链 [[ai-smart-home-system/02_国内镜像链与Docker基础设施]]、无头 onboarding [[ai-smart-home-system/04_无头onboarding自动化]]、Agent [[ai-smart-home-system/06_AI智能体FastAPI与DeepSeek]]、品牌矩阵 [[ai-smart-home-system/05_跨品牌接入矩阵]]。

## 0. 前置条件

- 绿联 DXP4800 Plus（16GB）到货，2×4TB HDD + M.2 SSD 装好
- 小米 BE6500 Pro Mesh 已布好，NAS 有线接入
- 宿主 BIOS 确认 **VT-x/AMD-V 开启**
- 准备：HAOS 镜像（qcow2）、Agent 仓库、场景 packages

## 1. 绿联 NAS 初始化

1. 开机进入 UGOS Pro，创建存储池（HDD 阵列，SSD 作为高速缓存/系统盘）
2. 安装并启用「虚拟机」「Docker」应用
3. 创建共享文件夹：`ha-backup`、`media`、`photos`、`camera-record`、`offsite`
4. 设置 NAS 固定 IP（如 192.168.x.10），开启 OVS 网络（虚拟网桥）

## 2. 创建 HAOS 虚拟机（关键步骤）

> ⚠️ **UEFI 建后不可改**，一次建对。

1. 下载 HAOS qcow2 镜像（国内走 HAOS-CN 分发，见下）
2. 虚拟机应用 → 新建：
   - 操作系统：Linux / Other
   - **主板类型：Q35**
   - **主板固件：UEFI**
   - CPU：硬件虚拟化，≥2 vCPU（推荐 4）
   - 内存：**4096 MB**（VM 内推荐 4GB）
   - 磁盘：**从镜像导入**（qcow2），放 **M.2 SSD**，≥32GB（建议 64GB）
   - 磁盘总线：SATA
   - 网卡：e1000，桥接模式
3. 开机，等待引导完成
4. 访问 `http://<HA-IP>:8123`（或 `homeassistant.local:8123`）

## 3. 国内镜像链（关键）

> 官方镜像/组件拉取在国内必须走镜像链，见笔记 ch2。核心结论：
> - **Docker Hub `registry-mirrors` 只对 Docker Hub 生效，对 ghcr.io 无效** → 需前缀整体替换
> - ghcr fallback 链（2026-08 实测）：`ghcr.nju.edu.cn` → `docker.m.daocloud.io/ghcr.io` → `ghcr.1ms.run` → 官方 ghcr.io（慢）→ `ota.hasscn.top`（大陆，默认注释）
> - Docker Hub mirror：`docker.1ms.run`、`docker.m.daocloud.io`、`docker.1panel.live`

| 资源 | 国内获取方式 |
|------|------------|
| HAOS 镜像 | HAOS-CN 国内分发（`ota.hasscn.top` / 社区镜像） |
| HA 升级 | 走 HAOS-CN OTA 加速 |
| Agent / 组件镜像 | ghcr fallback 链 + 阿里云 ACR 私有分发 |

> [!note] 备选：冬瓜HAOS
> 如网络折腾成本过高，可评估社区定制版**冬瓜HAOS**（预装 HACS/MIOT、国内网络优化）。但它是第三方构建，与自建镜像策略不同，仅在自建失败时降级使用。

## 4. 无头 onboarding（自动初始化）

> 用 onboarding API 自动完成首次引导，见笔记 ch4。核心 5 步：

1. `GET /api/` 探测版本（未知则退回浏览器向导）
2. `POST /api/onboarding/users` 建 owner + 拿一次性 auth_code
3. `POST /auth/token` 换长期 token（LLAT）
4. `POST /api/onboarding/core_config` 配国家/时区（Asia/Shanghai）
5. `POST /api/onboarding/analytics`（建议关）+ `POST /api/onboarding/integration`

> 兜底：pre-seed `.storage/`（auth/core.config/onboarding/person），密码 PBKDF2-SHA512，模板从干净 HA 导出。

## 5. 安装 Agent Add-on

> 复用笔记 ch6。Agent = FastAPI + DeepSeek `deepseek-v4-flash`，N=1 工具调用。

1. 在 Supervisor → Add-on Store 添加 Agent 仓库
2. 安装 Agent Add-on
3. 填配置：HA 长令牌（LLAT，用受限用户）、DeepSeek API Key
4. 健康检查：`GET /health`
5. 配 `entity_map.yaml`（客户设备语义映射，唯一客户化文件之一）

安全要点：
- **专用受限 HA 用户**（LLAT 无 scope，隔离靠用户权限，见 ch6）
- 域白名单：`light/switch/fan/cover/media_player/climate`
- 预调用状态检查：`unavailable/unknown` 设备拦截
- 亮度 0–255 换算，模型输出百分比需 clamp

## 6. 品牌接入（复用笔记 ch5 矩阵）

| 品牌 | 方式 | 要点 |
|------|------|------|
| 小米 | 官方 `xiaomi_home`（预置 v0.4.7） | OAuth 扫码登录，需人工；LAN 控制靠中枢网关 |
| Aqara（Zigbee） | 走中枢网关 → `xiaomi_home` | 无需独立集成 |
| 涂鸦 | `tuya` 云 + `localtuya` 本地 | 云 keys 有时效；国内区 `openapi.tuyacn.com` 需 IP 白名单 |
| 美的 | `midea_ac_lan` | V3 需一次性 token；V1 token API 已关，新设备走 V3 |
| 格力 | 内置 `gree` | 需先格力+ App 配对；建议换社区增强版拿完整状态 |
| 华为 | **无路径** | 仅 Matter/反向控制，按设备评估，不进 MVP |

品牌接入后按房间建立实体命名规范：`light.living_room_ceiling` 等，写入 `entity_map.yaml`。

## 7. Docker 宿主服务（NAS 侧，非 VM 内）

| 服务 | 容器 | 说明 |
|------|------|------|
| 影音 | Jellyfin | `/dev/dri` 挂载启用 QSV 转码 |
| 安防 | Frigate | `/dev/dri` OpenVINO；读摄像头 RTSP，写 `camera-record` |
| 组网 | Tailscale | NAS/HA/顾问节点入 tailnet |
| 相册 | Immich | 接系统相册或独立，补绿联相册 AI 短板 |

> 注意：Jellyfin/Frigate 用**宿主 Docker** 而不是 HAOS VM 内 Add-on，这样能用 `/dev/dri`（GPU 不直通给 VM）。

## 8. 验收清单

- [ ] HA 在线，`/api/` 正常，SSL/内网访问通
- [ ] 国内镜像链路验证：升级、拉取均走通
- [ ] 米家扫码授权完成，设备实体齐全
- [ ] Agent `/health` 通过，实体模糊匹配（rapidfuzz ≥80）验证
- [ ] 场景 packages 加载无报错（`homeassistant: packages`）
- [ ] Frigate 收到 RTSP 流并录像
- [ ] Tailscale 组网通，顾问可远程
- [ ] 快照自动备份到 `ha-backup` + 异地同步

## 9. 踩坑速查

| 症状 | 原因/处理 |
|------|---------|
| HAOS 进 UEFI Shell | 固件/磁盘/镜像配置错误；重建成 Q35+UEFI，或改用 PE 安装器 |
| VM 显示内存 90% | UGOS 显示 bug（宿主其实 <10%），以宿主监控为准 |
| HAOS 卡顿 | 宿主 VT-x 未开（跑了 TCG）；HAOS 放机械盘 |
| 拉镜像失败 | 走 ghcr fallback 链；Docker Hub 才用 registry-mirrors |
