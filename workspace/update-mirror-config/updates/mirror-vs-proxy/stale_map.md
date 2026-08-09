# stale_map：docker/镜像加速器vs代理-概念对比.md

> 生成：2026-08-08 ｜ 模式：patch-in-place（已应用）

## 保留
- 概述、核心区别对比表（除配置位置行）
- 2.1 镜像加速器概念与工作原理图
- 代理相关章节（Daemon 代理、容器代理、验证命令）
- 个人笔记、相关文档、参考资料

## 需要更新
| 位置 | 旧内容 | 新内容 |
|------|--------|--------|
| L21 对比表 | 「配置位置 daemon.json 的 registry-mirrors」 | 「Docker Desktop 用 GUI；Linux 用 daemon.json 的 registry-mirrors」 |
| L148 注释 | `// ~/.docker/daemon.json 或 /etc/docker/daemon.json` | Docker Desktop 用 GUI；仅 Linux 读取 /etc/docker/daemon.json |
| L253-259 配置示例 | `// ~/.docker/daemon.json (Mac Docker Desktop)` + USTC 源 | GUI 说明 + 移除 USTC，加 xuanyuan.me |

## 需要删除
- `docker.mirrors.ustc.edu.cn`（已失效）

## 需要新增
- `docker.xuanyuan.me`（可用源）
- `## 更新记录` 段
- Docker Desktop 不读 `~/.docker/daemon.json` 的说明
