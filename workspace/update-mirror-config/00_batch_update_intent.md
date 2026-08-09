---
source_path: "docker/"
source_scope: selected
source_glob: "*.md"
update_goal: "修复镜像加速器笔记中的过时信息：① Docker Desktop 不读取 ~/.docker/daemon.json（仅 GUI 生效）的误导；② 已失效镜像源 docker.mirrors.ustc.edu.cn / docker.nju.edu.cn / docker.mirrors.sjtug.sjtu.edu.cn"
destination_mode: patch-in-place
batch_size: 3
shared_research: yes
moc_path: "docker/Docker MOC.md"
---

# 批量更新意图：镜像加速器笔记过时信息修复

## 背景

2026-08-08 更新 `docker/DockerDesktop镜像加速器配置.md` 时发现：

1. **核心前提错误**：`~/.docker/daemon.json`（或 `%USERPROFILE%\.docker\daemon.json`）对 Docker Desktop 无效——Docker Desktop 的 dockerd 运行在内置 Linux VM，宿主机 `~/.docker/` 只是 Docker CLI 配置目录，daemon 不读取。命令行 `daemon.json` 方式仅适用于 Linux 原生 dockerd（`/etc/docker/daemon.json`）。
2. **镜像源失效**：实测 `docker.mirrors.ustc.edu.cn`、`docker.mirrors.sjtug.sjtu.edu.cn` 超时不可用，`docker.nju.edu.cn` 返回 403 受限。

## 范围

仅 `docker/` 目录下镜像加速器相关笔记：

| 文件 | 动作 |
|------|------|
| `docker/镜像加速器vs代理-概念对比.md` | update |
| `docker/Windows-DockerDesktop安装指南-国内网络版.md` | update |
| `docker/DockerDesktop镜像加速器配置.md` | skip（本轮已更新完成） |
| `docker/Linux-Docker与DockerCompose安装指南-国内网络版.md` | skip（已准确） |

## 输出

- destination_mode：patch-in-place（直接修正原笔记，每篇追加「更新记录」）
- 用户确认：范围与输出模式已由用户确认（2026-08-08）
