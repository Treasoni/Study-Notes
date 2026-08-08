# 更新清单：镜像加速器笔记过时信息修复

> 项目：update-mirror-config ｜ 范围：docker/ 目录 4 篇镜像加速器相关笔记
> 扫描日期：2026-08-08 ｜ 关键词：`~/.docker/daemon.json`、`registry-mirrors`、`docker.mirrors.ustc.edu.cn`、`docker.nju.edu.cn`、`docker.mirrors.sjtug.sjtu.edu.cn`

## 清单

| id | 文件 | 标题 | updated | status | 理由 | 优先级 |
|----|------|------|---------|--------|------|--------|
| mirror-vs-proxy | `docker/镜像加速器vs代理-概念对比.md` | Docker 镜像加速器 vs 代理 - 概念对比 | 2026-03-28 | **ready** | ① L148/L253 写 `~/.docker/daemon.json` 适用于 Mac Docker Desktop（错误前提）；② L259 把已失效 USTC 当可用源 | 高 |
| windows-desktop-guide | `docker/Windows-DockerDesktop安装指南-国内网络版.md` | Windows Docker Desktop 安装指南（国内网络版） | 2026-03-29 | **ready** | ① L257-274「方法二命令行配置」写 `%USERPROFILE%\.docker\daemon.json`（Docker Desktop 无效）；② L271/L299 USTC 标记为可用、L300 NJU 需验证（均已失效） | 高 |
| mac-mirror-config | `docker/DockerDesktop镜像加速器配置.md` | Docker Desktop Mac 镜像加速器配置 | 2026-08-08 | skip | 本轮（2026-08-08）已用 note-updater 完成 patch-in-place，内容已准确 | — |
| linux-install-guide | `docker/Linux-Docker与DockerCompose安装指南-国内网络版.md` | Docker 与 Docker Compose 安装（国内环境） | 2026-08-04 | skip | 已准确：Linux 用 `/etc/docker/daemon.json` 正确；USTC/NJU 已标注「已停服」；可用源为 1ms.run/daocloud | — |

## 关键词命中摘要（待更新 2 篇）

### mirror-vs-proxy（`docker/镜像加速器vs代理-概念对比.md`）
- L148：`// ~/.docker/daemon.json 或 /etc/docker/daemon.json` — 需明确 Docker Desktop 不读
- L253：`// ~/.docker/daemon.json (Mac Docker Desktop)` — **错误前提**
- L259：`"https://docker.mirrors.ustc.edu.cn"` — 已失效源，出现在配置示例
- L21：对比表「配置位置 daemon.json 的 registry-mirrors」— 可接受，建议补充 Docker Desktop 用 GUI

### windows-desktop-guide（`docker/Windows-DockerDesktop安装指南-国内网络版.md`）
- L257-274：方法二「命令行配置」`notepad %USERPROFILE%\.docker\daemon.json` — **Docker Desktop 无效**
- L267-271：JSON 含 `docker.mirrors.ustc.edu.cn`（失效）
- L298-300：源状态表 — USTC「⚠️ 时好时坏」（应改失效）、NJU「⚠️ 需验证」（应改失效）

## 结论

- **ready（待更新）**：2 篇
- **skip（无需更新）**：2 篇
- **needs-review**：0 篇
- **flag-only**：0 篇（范围外的 HAOS/OpenClaw 命中不纳入本次）
