# 批量更新计划：镜像加速器笔记过时信息修复

> 项目：update-mirror-config ｜ 生成：2026-08-08

## 1. 更新目标与判断依据

| 目标 | 判断依据 |
|------|---------|
| ① 修正「Docker Desktop 读取 `~/.docker/daemon.json`（Mac）/ `%USERPROFILE%\.docker\daemon.json`（Windows）」的错误前提 | Docker Desktop 的 dockerd 运行在内置 Linux VM，宿主机 `~/.docker/` 仅为 Docker CLI 配置目录；官方支持路径为 GUI `Settings → Docker Engine`。命令行 `daemon.json` 仅适用于 Linux 原生 dockerd |
| ② 修正已失效镜像源 `docker.mirrors.ustc.edu.cn` / `docker.nju.edu.cn` / `docker.mirrors.sjtug.sjtu.edu.cn` | 2026-08-08 从用户网络 curl 实测：USTC/SJTU 超时（000），NJU 返回 403 受限；社区持续更新列表（dongyubin/DockerHub）确认已失效 |

## 2. 笔记分组

| 分组 | 笔记 | 动作 |
|------|------|------|
| Docker Desktop 镜像加速配置 | `docker/镜像加速器vs代理-概念对比.md` | **update** |
| | `docker/Windows-DockerDesktop安装指南-国内网络版.md` | **update** |
| 已准确 | `docker/DockerDesktop镜像加速器配置.md` | skip |
| | `docker/Linux-Docker与DockerCompose安装指南-国内网络版.md` | skip |

## 3. 每篇动作与更新要点

### 3.1 mirror-vs-proxy（update，patch-in-place）
- L148 / L253：把 `~/.docker/daemon.json (Mac Docker Desktop)` 的注释改为「仅 Linux dockerd」或标注 Docker Desktop 不读
- L259：从配置示例移除已失效 USTC，替换为可用源（如 `docker.xuanyuan.me`）
- L21 对比表：配置位置一栏补充 Docker Desktop 用 GUI 的说明
- 追加「更新记录」

### 3.2 windows-desktop-guide（update，patch-in-place）
- 「方法二：命令行配置」`notepad %USERPROFILE%\.docker\daemon.json` → 改为说明 Docker Desktop 不读该文件，仅 GUI 生效；Linux 才用 daemon.json
- 配置 JSON（L267-271）移除 USTC，更新为可用源
- 源状态表（L298-300）：USTC/NJU 改为「❌ 已失效」
- 追加「更新记录」

## 4. 第一批处理列表（batch_size=3，本次仅 2 篇，单批完成）

| 顺序 | 笔记 | 调用 note-updater |
|------|------|-------------------|
| 1 | `docker/镜像加速器vs代理-概念对比.md` | 是 |
| 2 | `docker/Windows-DockerDesktop安装指南-国内网络版.md` | 是 |

## 5. 输出模式与覆盖风险

- **destination_mode**：`patch-in-place`（直接修改 vault 原笔记，用户已确认）
- **覆盖风险**：低。两篇均为局部 patch，保留原结构与写作风格；每篇追加「更新记录」；不动未过时段落
- **备份**：patch 前可通过 git 回滚（vault 在 git 管理下）；必要时可在更新前对目标文件做 `.backup` 副本

## 6. 需用户确认项

- [ ] 第一批处理列表（2 篇）是否确认开始？
- [ ] 是否需要对原文件先做备份副本？（默认：git 已可回滚，不额外备份）
