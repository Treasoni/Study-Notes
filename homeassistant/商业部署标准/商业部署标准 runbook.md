---
title: "商业部署标准 Runbook"
tags:
  - 智能家居/商业运营
  - 内部实施
  - 部署标准
created: 2026-08-06
updated: 2026-08-06
status: 草稿
source_project: haos-deploy-tutorial
---

# 商业部署标准 Runbook

> [!summary] 定位
> 公司内部商业交付标准。核心思路：**官方原版 HAOS + 预置国内源** 固化成「黄金模板」，每个客户从模板克隆，保证可复制、可追责、可长期维护。HAOS-CN 仅用于演示/试用，不作为交付基线。
>
> 技术细节对应教程：[[部署 HAOS 详细教程]]（安装见 [[03_官方原版HAOS安装实战|第 3 章]]、国内源配置见 [[04_手动配置国内源|第 4 章]]、稳定运行见 [[07_稳定运行保障|第 7 章]]）。

---

## 1. 商业部署原则

| 原则 | 说明 |
|------|------|
| **官方基线** | 一律用官方原版 HAOS，有 SHA256、官方 OTA、可追责 |
| **模板化** | 国内源配置只做一次，固化为黄金模板，客户从模板克隆 |
| **虚拟机优先** | 快照 = 秒级回滚，整机备份可迁移，远程运维可进管理面 |
| **可复制交付** | 每个客户 30 分钟装完，交付检查清单逐项验收 |
| **维护可预测** | 升级逐大版本 + 快照回滚；备份 3-2-1；SLA 白纸黑字 |

> [!warning] 为什么不默认 HAOS-CN
> HAOS-CN 是第三方再发行：系统镜像无校验和、构建脚本私有、OTA 依赖项目方与公益镜像站、系统内加速不可关闭。商业交付要的是「可证明、可追责、可兜底」，官方原版 + 自建模板是更稳的选择。HAOS-CN 只用于销售演示、客户试用、POC。

---

## 2. 黄金镜像/模板制作

> 目标：产出一个「装完即含国内源、基础组件齐备」的 HAOS 虚拟机模板，交付时克隆。

### 2.1 准备

- 一台模板制作机（可用 PVE / 绿联 NAS VMM / VMware Workstation）
- 官方 HAOS 镜像：x86-64 用 `haos_generic-x86-64-{ver}.img.xz`，虚拟机用 `haos_ova-{ver}.qcow2`（下载：官方 GitHub Releases）
- **校验**：对照官方 Release 的 SHA256 验证镜像完整性
```bash
sha256sum haos_ova-18.2.qcow2
# 与官方 checksum 对比；不一致则重新下载
```
- 存储：模板盘放 **SSD**（HA 数据库约 15 次写入/秒，TF/机械盘必坏）
- 固件：UEFI + 关闭 Secure Boot + 无需 TPM

### 2.2 基础安装

创建 VM 的标准参数（对应 [[03_官方原版HAOS安装实战|第 3 章]]）：

| 参数 | 值 | 说明 |
|------|-----|------|
| 机型/固件 | Q35 / UEFI | UEFI 建后不可改，一次建对 |
| CPU | ≥2 vCPU（推荐 4） | 实体机请用 host 类型 |
| 内存 | ≥2048 MB（推荐 4096） | 按负载可调 |
| 磁盘 | SATA 总线，≥32GB（推荐 64GB） | 放 SSD |
| 网卡 | e1000 / VirtIO，桥接 | 保证 HA 直接拿局域网 IP |

安装完成后访问 `http://homeassistant.local:8123` 或 `http://<IP>:8123` 确认引导成功。

### 2.3 预置国内源（关键）

> 这一步是黄金模板的核心，做一次即可。SSH 进 HAOS：`ssh root@<IP> -p 22222`。

**1) NTP 时间同步**（对应 [[04_手动配置国内源|第 4 章]]）

```ini
# /etc/systemd/timesyncd.conf
[Time]
NTP=ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com
FallbackNTP=ntp.tencent.com cn.pool.ntp.org
```

```bash
systemctl restart systemd-timesyncd.service
timedatectl   # 看到 System clock synchronized: yes 即成功
```

**2) Supervisor 镜像源（ghcr.io 加速核心）**

```bash
vi /usr/share/hassio/docker.json
```

```json
{
  "registries": {},
  "registries_mirror": {
    "ghcr.io": "ghcr.nju.edu.cn",
    "docker.io": "docker.nju.edu.cn"
  }
}
```

```bash
systemctl restart hassio-supervisor
```

> [!warning] 升级会重置
> HAOS 升级可能重置 `docker.json`，模板内应保留该文件备份，交付后维护时如发现 ghcr 拉取变慢先检查此文件。

**3) Add-on 国内仓库**

- 设置 → 加载项商店 → 右上角三个点 → 仓库 → 添加：`https://gitee.com/desmond_GT/hassio-addons`
- 镜像映射：ghcr.io → `ghcr.nju.edu.cn`；docker.io / lscr.io → `docker.1panel.live`；github.com → `gh-proxy.org`
- 免翻墙；首次安装偶发失败，重试一次即可

**4) 基础组件预装**

- Terminal & SSH（运维入口）
- Samba Backup（本地备份到 NAS 共享目录）
- Google Drive Backup（异地备份，见 [[07_稳定运行保障|第 7 章]]）
- chrony（可选，容器环境 NTP 兜底）
- 场景 packages 目录骨架（`/config/packages`）

### 2.4 导出黄金模板

1. 在 VM 内做一次完整快照（Supervisor → 系统 → 备份，命名 `GOLD-{版本}-{日期}`）
2. 关闭 VM，在宿主把该 VM **转为模板**（PVE `qm template` / 绿联 VMM「转为模板」/ VMware 快照导出）
3. 模板命名规范：`HAOS-GOLD-{核心版本}-{日期}`，例如 `HAOS-GOLD-2026.8-20260806`
4. 模板入库登记：版本号、镜像源配置版本、预装组件、SHA256、制作人、日期

> [!tip] 模板与实测
> 模板每季度或在 HA 大版本升级后重建一次；制作完成后用「交付检查清单」自测一遍再入库。

---

## 3. 交付检查清单

> 每个客户交付时逐项勾选，缺一项不验收。

### 3.1 安装
- [ ] 宿主 VT-x/AMD-V 已开启；NAS/宿主机已配固定 IP
- [ ] 从黄金模板克隆 VM，UEFI / SATA / 磁盘 ≥64GB 确认
- [ ] HA 引导成功，访问 `http://<IP>:8123` 进入向导
- [ ] 国家/时区设为 Asia/Shanghai；时区正确（不是差 8 小时）

### 3.2 国内源
- [ ] NTP 同步成功（`timedatectl` 显示 synchronized）
- [ ] ghcr 拉取验证：装一个官方 Add-on 能拉通
- [ ] Add-on 国内仓库已添加，商店可正常加载
- [ ] Docker Hub 镜像验证（如适用）：`docker info` 有 Registry Mirrors

### 3.3 稳定与备份
- [ ] 存储确认在 SSD；如历史项目有 TF/机械盘，已做 [[07_稳定运行保障|SSD 迁移]]
- [ ] 本地备份（Samba → NAS `ha-backup`）已配置并跑通一次
- [ ] 异地备份（Google Drive / 异地 NAS）已配置，3-2-1 满足
- [ ] 升级策略确认：逐大版本升级 + 升级前自动快照

### 3.4 远程与交接
- [ ] 远程访问已落地（Tailscale / FRP / 域名反代之一），并确认**勿裸映射 8123**
- [ ] 客户账号创建（owner + 受限用户），密码策略设置
- [ ] 交付文档：客户配置单（设备清单、账号、远程方式、维护联系人）
- [ ] 部署 runbook 归档到客户目录（参考 [[customers/客户A/实施/01_部署runbook|客户A runbook]]）

---

## 4. 维护 SLA 清单

### 4.1 例行维护

| 周期 | 动作 |
|------|------|
| 每周 | 检查备份是否成功（本地 + 异地）、存储剩余空间、错误日志 |
| 每月 | 检查更新提示、测试镜像源可用性（公益源会失效，多源备选）、NTP 校时 |
| 每季 | 重建黄金模板（若 HA 有重大更新）、复核远程访问通道、审核受限用户权限 |

### 4.2 升级策略

> 对应 [[07_稳定运行保障|第 7 章]] 升级与回滚。

1. 升级前：确认备份存在 + 做快照（升级前自动快照是安全网）
2. **逐大版本升级**，不跨版本跳升（如 2024.10 → 11 → 12）
3. 升级后：检查 `/config/home-assistant-rollback.log`（若出现 rollback 则回滚）
4. 失败回滚：`ha supervisor repair` → `ha core update --version <旧版本>` → 或恢复快照
5. 注意：Supervisor 自身更新不随 Core 回滚，需单独关注

### 4.3 故障响应

| 症状 | 处理 | 参考 |
|------|------|------|
| 无 IP / 断电后连不上 | `network update <iface> --ipv4-method auto`；建议静态 IP | [[08_故障排查手册与长期运维\|第 8 章]] |
| 错误码 1001/1003/1004 | 网络接口 / 启动失败 / 数据库不存在，查端口 8124/4357 | 第 8 章 |
| 数据库损坏 | 正确重启走「设置→系统→硬件」；SQLite `.recover` 重建；长期改 MariaDB | 第 8 章 |
| 时间偏移持续增大 | 优先排查 NTP；国内源 `ntp.aliyun.com` / `cn.pool.ntp.org` | 第 4/8 章 |
| 拉镜像失败 | 走 ghcr fallback 链；公益源失效则换多源清单中的其他源 | 第 4 章 |

### 4.4 SLA 指标（建议写入合同）

| 指标 | 建议值 |
|------|--------|
| 备份频率 | 每日（本地）+ 每日/周（异地） |
| RPO（可容忍数据丢失） | ≤24 小时（每日备份） |
| RTO（恢复时间） | ≤4 小时（VM 快照/模板重装） |
| 例行维护响应 | 24 小时内响应 |
| 重大故障响应 | 4 小时内响应 / 48 小时内解决（视 SLA 分级） |
| 升级窗口 | 月内非业务高峰，升级前通知客户 |

---

## 5. 与 HAOS-CN 的边界

| 场景 | 用哪个 |
|------|--------|
| 正式交付 / 长期维护 | **官方原版黄金模板** |
| 销售演示 / 客户试用 / POC | HAOS-CN（装得快、开箱即用） |
| 快速验证环境 | HAOS-CN `-full` 完整包 |
| 客户指定 / 已用 HAOS-CN 的存量 | 评估后决定：交付期可用，长期维护建议迁回官方模板（备份→重装→还原） |

> [!warning] 演示转交付
> 若客户在试用 HAOS-CN 后签单，交付时应按「备份 → 官方模板重装 → 还原」路线迁回官方基线，不要把试用环境直接当生产交付。
