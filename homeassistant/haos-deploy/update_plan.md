# Update Plan — 04_手动配置国内源.md

更新日期：2026-08-07
更新方式：patch-in-place（重写替代）
更新目标：以「Docker / Supervisor / OTA 三层换源」为核心组织全章，新增三层对比，补充 2026 最新资料

## Stale Map

| 现有内容 | 处理 | 去向 |
|---------|------|------|
| 顶部 summary / 0 速查 / 时效性 / 先读 | 保留+重构 | 新 0 先看这里（三层速查表）+ 先读 |
| 4.1 Supervisor 镜像源（docker.json registries_mirror） | 保留 | 新 4.3 Supervisor 换源 |
| 4.2 Docker 12 源（daemon.json registry-mirrors） | 保留+更新 | 新 4.2 Docker 换源 |
| 4.1 补充：系统级 OTA（4 障碍 / rauc install / HAOS-CN） | 保留+升级为独立节 | 新 4.4 OTA 换源 |
| 4.3 Add-on 商店国内仓库 | 保留 | 新 4.5 其他国内化 |
| 4.4 NTP 时间同步 | 保留 | 新 4.5 其他国内化 |
| 4.5 udev bind-mount（已失效） | 保留但降级为历史说明 | 新 4.2 Docker 节的「曾经方案」 |
| 4.6 宿主 shell 替代路线（方案 A-E） | 保留 | 新 4.6 宿主 shell 前置与替代路线 |
| — 三层换源对比 | 新增 | 新 4.1 三层换源的区别（核心） |
| — 2026 最新 Docker 镜像源 | 新增 | 4.2 |
| — RAUC 补充命令 / 更新频率 | 新增 | 4.4 |

## 交叉引用影响

- 标题从「手动配置国内源（官方原版加速核心）」改为「HAOS 国内换源（Docker / Supervisor / OTA 三层全解）」
- 需同步：MOC「部署 HAOS 详细教程.md」索引、03/05 章页脚显示文本、08 章节号引用（L131/L133/L162）

## 资料收集（2026-08）

- DeepWiki HAOS-CN：三层换源机制、12 源 failover 链、腾讯 BGP OTA
- 2026 年 Docker 镜像源实测：docker.xuanyuan.me / docker.1ms.run（ghcr.1ms.run 前缀）/ docker.m.daocloud.io 等
- Supervisor registries_mirror 原理：仓库级映射，重启 hassio-supervisor 生效
- RAUC：A/B 槽位、rauc install / rauc status / ha os boot-slot、systemctl reboot
