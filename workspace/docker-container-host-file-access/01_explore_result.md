# 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件 - 探测结果

- **阶段**: P1 探测式收集
- **日期**: 2026-08-29
- **探测透镜**: 3 个独立方向，3 个并行 subagent
- **候选源总数**: 14 条 → 去重后 **13 条**（1 条重复 URL：bind-mounts 官方页在两个透镜中重复出现）

---

## 候选源汇总（按透镜）

### 透镜 1：卷与挂载方案

| # | 标题 | URL | Tier | 评分 |
|---|------|-----|------|------|
| 1 | Docker Storage 存储总览（Volumes / Bind Mounts / tmpfs） | https://docs.docker.com/engine/storage/ | 1 | 5 |
| 2 | Docker 绑定挂载 Use bind mounts | https://docs.docker.com/engine/storage/bind-mounts/ | 1 | 5 |
| 3 | Docker 卷 Use volumes | https://docs.docker.com/engine/storage/volumes/ | 1 | 5 |
| 4 | Docker tmpfs mounts | https://docs.docker.com/engine/storage/tmpfs/ | 1 | 4 |
| 5 | Docker Compose volumes 参考 | https://docs.docker.com/reference/compose-file/volumes/ | 1 | 4 |

### 透镜 2：权限与用户映射

| # | 标题 | URL | Tier | 评分 |
|---|------|-----|------|------|
| 6 | Isolate containers with a user namespace (userns-remap) | https://docs.docker.com/engine/security/userns-remap/ | 1 | 5 |
| 7 | Rootless mode | https://docs.docker.com/engine/security/rootless/ | 1 | 4 |
| 8 | docker run reference (--user) | https://docs.docker.com/engine/reference/run/ | 1 | 4 |
| 9 | Docker Volume Permissions Explained | https://selfhosting.sh/foundations/docker-volume-permissions/ | 2 | 4 |
| 10 | matchhostfsowner（容器启动自动匹配宿主属主） | https://github.com/FooBarWidget/matchhostfsowner | 2 | 3 |

### 透镜 3：安全边界与替代方案

| # | 标题 | URL | Tier | 评分 |
|---|------|-----|------|------|
| 11 | Docker AppArmor 安全配置文件 | https://docs.docker.com/engine/security/apparmor/ | 1 | 4 |
| 12 | Protect the Docker daemon socket | https://docs.docker.com/engine/security/protect-access/ | 1 | 5 |
| 13 | docker-socket-proxy（HAProxy 白名单过滤 Docker API） | https://github.com/Tecnativa/docker-socket-proxy | 2 | 4 |
| 14 | Docker socket security: why docker.sock is root access | https://www.netdata.cloud/guides/docker/docker-socket-security/ | 2 | 4 |

> 注：#2 与透镜 3 的 bind-mounts 页（`docs.docker.com/storage/bind-mounts/`）为同一权威来源的不同 URL，已去重合并到 #2，其相关说明同时涵盖只读挂载与 SELinux `:z`/`:Z` 标签。

---

## 方向菜单

| 选项 | 方向 | 说明 |
|------|------|------|
| **A** | 综合实战主线（推荐） | 按「挂载 → 权限 → 安全」顺序完整覆盖三块，形成一份可直接照着做的实战笔记 |
| **B** | 聚焦挂载方案 | 深入 bind mount / named volume / tmpfs 的选型、命令与差异 |
| **C** | 聚焦权限与坑 | 深入 UID/GID、`--user`、userns-remap、rootless 与 permission denied 修复 |
| **D** | 聚焦安全边界 | 深入只读挂载、SELinux/AppArmor、Docker socket 风险与替代方案 |

---

## 覆盖缺口（P2 需补充）

- **Docker Desktop（macOS/Windows）** 的路径差异与挂载性能问题（常见实战痛点，本批未覆盖）
- **linuxserver.io 社区镜像的 PUID/PGID 环境变量模式**（大量实战部署用它规避属主问题）
- **docker compose `user:` 字段**与 named volume 初始化权限的配合
- 容器内服务**主动触发宿主命令**（如 SSH/API）的边界场景

## 预计 P2 范围

- 按所选方向从候选源中选取 **3–5 个核心源**做深度阅读
- 补充上述缺口素材（Docker Desktop、PUID/PGID、compose `user:`）
- 产出 `02_deep_research.md`：范围、来源表、声明/来源映射、矛盾点、实战指引、开放问题、下游交接
