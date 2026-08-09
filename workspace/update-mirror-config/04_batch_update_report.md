# 批量更新报告：镜像加速器笔记过时信息修复

> 项目：update-mirror-config ｜ 完成：2026-08-08 ｜ 模式：patch-in-place

## 统计

| 指标 | 数量 |
|------|------|
| 处理文件数 | 4 |
| **更新文件数** | **2** |
| 跳过文件数 | 2 |
| 需复核文件数 | 0 |
| 失败数 | 0 |

## 更新摘要

| 笔记 | 输出 | 关键变更 |
|------|------|----------|
| docker/镜像加速器vs代理-概念对比.md | updates/mirror-vs-proxy/ | 修 `~/.docker/daemon.json`（Mac）误导 → GUI 说明；移除 USTC；新增 xuanyuan.me；对比表配置位置行补充 |
| docker/Windows-DockerDesktop安装指南-国内网络版.md | updates/windows-desktop-guide/ | 「方法二」改为仅 Linux dockerd + `%USERPROFILE%\.docker\daemon.json` 无效警告；USTC/NJU 标记失效；新增 1ms.run；问题2排查改 GUI + context |

## 跳过说明

| 笔记 | 原因 |
|------|------|
| docker/DockerDesktop镜像加速器配置.md | 本轮（2026-08-08）已单独完成 patch-in-place |
| docker/Linux-Docker与DockerCompose安装指南-国内网络版.md | 已准确（Linux daemon.json 正确，失效源已标注已停服） |

## 共享资料来源

- workspace/update-mirror-config/shared_research/source_bank.md
  - Docker daemon 官方文档 / docker/for-mac#2537（Docker Desktop 不读宿主机 daemon.json）
  - dongyubin/DockerHub 2026-08（镜像源可用性）
  - 2026-08-08 用户网络 curl 实测（USTC/SJTU 超时、NJU 403）

## 未处理风险与建议

1. `docker.1panel.live` 保留为「✅ 可用」但实测返回 403（GitHub 列表标注仅限中国地区）——建议用户实地验证，必要时改为「⚠️ 受限」
2. 范围外命中（homeassistant/ 的 HAOS 换源、OpenClaw 安装教程）未处理：`homeassistant/haos-deploy/04_手动配置国内源.md` 仍含 USTC 死源、`ghcr.nju.edu.cn` 受限源；如需处理可作为下一批
3. 镜像源可用性持续变化，建议保持 2-4 个源 + 定期 curl 自测

## MOC

- docker/Docker MOC.md 已索引全部相关笔记；本次仅追加更新日志条目，未复制正文
