# Update Plan — Tailscale 使用教程（补充 Docker 部署内容）

- **日期**：2026-08-28
- **目标笔记**：`内网穿透/Tailscale使用教程.md`
- **更新目标**：补充 Docker 容器部署与安装 Tailscale 的内容
- **目的地模式**：patch-in-place（直接在 vault 原笔记上局部修改）

## Stale Map

| 位置 | 处理 | 说明 |
|------|------|------|
| 第 5 章引言「容器与 Kubernetes 集成」 | 更新 | 改为「Docker 与 Kubernetes 容器集成」 |
| `### 5.4 容器与 Kubernetes` | 更新 | 重写为 `### 5.4 Docker 与 Kubernetes 集成`，加入 Docker 内容 |
| 原 5.4「认证 / Subnet router / K8s YAML / DNS 易错点」 | 保留 | 并入新的 5.4.4 Kubernetes 部署 |
| 第 5 章小结最后一条 | 更新 | 补充 Docker 部署要点 |
| `参考来源` | 新增 | 追加 `[^c5-6]` Docker standalone、`[^c5-7]` Docker 配置参数 |
| 末尾 | 新增 | 追加 `## 更新记录` |
| 其余章节（1–4 章、5.1–5.3） | 保留 | 不重写未涉及段落 |

## 新增内容设计

- **5.4.1 单机部署 `docker run`**：官方镜像、auth key 生成、核心命令、`TS_*` 环境变量速查表、状态目录持久化 warning、user-space vs 内核态说明。
- **5.4.2 Sidecar 模式**：`docker compose` 示例，`network_mode: service:tailscale` 共享网络栈，容器 DNS 易错点。
- **5.4.3 容器作子网路由 / Exit Node**：`TS_ROUTES` / `TS_EXTRA_ARGS` 示例，审批提醒。
- **5.4.4 Kubernetes 部署**：保留原 K8s 认证、Secret、subnet router 与 DNS warning。

## 资料收集摘要

- Tailscale Docs：Connect a Docker container (standalone) — https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-standalone
  - 官方 `docker run` 命令：`TS_AUTHKEY` + `TS_STATE_DIR` + `./tailscale-state:/var/lib/tailscale` 挂载 + `--cap-add=net_admin,net_raw` + `--restart unless-stopped`。
- Tailscale Docs：Docker configuration parameters — https://tailscale.com/docs/features/containers/docker/docker-params
  - `TS_USERSPACE` 默认 true（user-space networking）；`TS_ROUTES` 等价 `--advertise-routes`；`TS_ACCEPT_DNS` 默认不接收；`TS_EXTRA_ARGS` / `TS_TAILSCALED_EXTRA_ARGS` 透传参数；状态目录不持久化会注册为新节点。
