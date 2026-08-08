# 批处理日志：update-mirror-config

> 批量大小：3（本次仅 2 篇，单批完成）

| 时间 | 批次 | 笔记 | 动作 | 输出 | 风险 |
|------|------|------|------|------|------|
| 2026-08-08 | 1 | docker/镜像加速器vs代理-概念对比.md | patch-in-place | updates/mirror-vs-proxy/ | 低 |
| 2026-08-08 | 1 | docker/Windows-DockerDesktop安装指南-国内网络版.md | patch-in-place | updates/windows-desktop-guide/ | 低（1panel.live 需实地验证） |

## 批次 1 详情

- **镜像加速器vs代理-概念对比.md**：修正 2 处 `~/.docker/daemon.json`（Mac）错误前提 → GUI 说明；移除 USTC，新增 xuanyuan.me；对比表配置位置行补充 GUI；追加更新记录
- **Windows-DockerDesktop安装指南-国内网络版.md**：方法二改为「仅 Linux dockerd」+ Docker Desktop 不读 `%USERPROFILE%\.docker\daemon.json` 警告；USTC/NJU 标记失效；新增 1ms.run；问题2排查改 GUI + context；追加更新记录

## 需复核
- 无（needs-review 0 篇）
