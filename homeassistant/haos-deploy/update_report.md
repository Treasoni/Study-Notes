# Update Report — 04_手动配置国内源.md

更新日期：2026-08-07
更新方式：patch-in-place（重写替代）
更新者：Claude（note-updater 流程）

## 变更摘要

- 标题改为「第四章：HAOS 国内换源（Docker / Supervisor / OTA 三层全解）」
- 新增 4.1「三层换源的区别」：容器镜像层 / HA 组件层 / 系统固件层大对比表 + 三个误区
- 4.2 Docker 换源：更新 2026 实测镜像源（毫秒 docker.1ms.run、轩辕 docker.xuanyuan.me 等），补多仓库替换前缀（ghcr.1ms.run），udev 方案降级为「曾经方案（已失效）」
- 4.3 Supervisor 换源：保留 docker.json registries_mirror 主线，补充 docker 直改法指引
- 4.4 OTA 换源：原 4.1 补充独立成节，补 RAUC 命令（rauc install / rauc status / ha os boot-slot / systemctl reboot 注意）
- 4.5 其他国内化：合并 Add-on 商店 + NTP
- 4.6 宿主 shell 前置与替代路线：保留方案 A-E
- 追加「更新记录」小节

## 交叉引用同步

- MOC「部署 HAOS 详细教程.md」索引条目标题已更新
- 03 / 05 章页脚上一章/下一章显示文本已更新
- 08 章 L131/L133/L162 节号引用已更新（Supervisor → 4.3，Addon+NTP → 4.5）
- 01、runbook 为章节级引用，不受影响

## 资料来源（2026-08 采集）

- DeepWiki — HAOS-CN Network Service Redirection / Docker Registry Mirrors：https://deepwiki.com/ha-china/HAOS-CN
- 2026 年 Docker 国内镜像源实测（轩辕 / 毫秒 / DaoCloud / 中科大）：https://m.zpedu.com/it/ityw/38111.html
- 瀚思彼岸 — hassio 国内镜像加速：https://bbs.hassbian.com/forum.php?mod=viewthread&tid=25022
- HAOS-CN GitHub / hasscn.top 更新系统文档：https://github.com/ha-china/HAOS-CN

## 未处理风险

- 公益镜像站地址随时可能失效，笔记已加时效性说明（以 4.2/4.3 换源即可）
- OTA 手动 `rauc install` 的 .raucb 下载地址为示例版本（12.5），需以官方 Releases 为准
- 方案 D（加载项一行解锁宿主 SSH）为社区方法，存在操作风险，笔记已标注
- 工作区 `workspace/haos-deploy-tutorial/` 下的生成副本未同步（workflow 产物）
