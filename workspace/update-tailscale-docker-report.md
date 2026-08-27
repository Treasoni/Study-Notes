# Update Report — Tailscale 使用教程（补充 Docker 部署内容）

- **日期**：2026-08-28
- **目标笔记**：`内网穿透/Tailscale使用教程.md`（patch-in-place，已完成）
- **工作文件**（本文件与 `update-tailscale-docker-plan.md` 放在 `workspace/`，未写入 Obsidian vault）

## 变更摘要

1. **5.4 节重写**：标题由「容器与 Kubernetes」改为「Docker 与 Kubernetes 集成」，新增
   - `5.4.1 单机部署：docker run` —— 官方镜像、auth key、核心命令、`TS_*` 环境变量速查表、状态目录持久化 warning、user-space 与内核态对比。
   - `5.4.2 Sidecar 模式` —— `docker compose` 示例（`network_mode: service:tailscale` 共享网络栈）、容器默认无 DNS 的易错点。
   - `5.4.3 容器作子网路由 / Exit Node` —— `TS_ROUTES` / `TS_EXTRA_ARGS` 两种部署示例、审批提醒。
   - `5.4.4 Kubernetes 部署` —— 保留原认证 / Secret / subnet router / DNS warning 内容。
2. **第 5 章引言**：改为「Docker 与 Kubernetes 容器集成」。
3. **本章小结**：最后一条扩充 Docker 部署要点（状态目录持久化、sidecar 共享网络栈、`TS_USERSPACE=false`、`TS_ROUTES`/`TS_EXTRA_ARGS`、`TS_ACCEPT_DNS`）。
4. **参考来源**：追加 `[^c5-6]`（Docker standalone 官方文档）、`[^c5-7]`（Docker 配置参数）。
5. **更新记录**：末尾追加 `## 更新记录`（2026-08-28）。

## 来源

- Tailscale Docs：Connect a Docker container (standalone) — https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-standalone
- Tailscale Docs：Docker configuration parameters — https://tailscale.com/docs/features/containers/docker/docker-params
- Tailscale Docker Hub 镜像 — https://hub.docker.com/r/tailscale/tailscale

## 未处理 / 风险

- 未新增 MOC（用户未指定 `moc_path`；该目录此前也未建 MOC）。
- 环境变量表为常用子集，非常用变量（OAuth/ID-token、`TS_SERVE_CONFIG`、metrics 等）未纳入，保持笔记「能用级」定位。
- 未在真机跑通 `docker run`，命令均以官方文档为准；如有 Tailscale 版本行为变化，以官方 docker-params 页为最新依据。
