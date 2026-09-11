# 如何使用 OpenList 聚合网盘并挂载给 Docker - 意图文件

## 基本信息

- **主题**: 如何使用 OpenList 聚合网盘并挂载给 Docker
- **完整链路**: OpenList 聚合网盘 → 开启 WebDAV 服务 → Rclone 挂载到本地 → 映射给 Docker 容器
- **项目标识**: openlist-webdav-rclone-docker
- **运行标识**: openlist-webdav-rclone-docker
- **创建工作流状态文件**: `workspace/workflow-runs/openlist-webdav-rclone-docker.workflow.md`
- **创建时间**: 2026-09-12
- **当前阶段**: 阶段 0
- **输出目标**: project-output（先写入项目 `output/`，阶段 6 再确认是否发布到 Obsidian vault）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型

实战教程（practice）为主，配合少量概念铺垫（concept）。用户要的是一条可照做的部署链路，不是纯原理综述。

### 学习深度

上手。目标是能独立跑通全链路并自行定位常见故障，而不是只会复制命令。

### 用户基础

有了解。已会基础 Docker / Linux 命令（能读懂 `docker run`、`-v`、`compose.yaml`、`systemctl`）。

## 研究计划

### 探索方向

1. **OpenList 本体**：部署形态（Docker Compose / 二进制）、存储挂载（本地、对象存储、网盘驱动）、用户与权限、配置持久化。
2. **WebDAV 服务**：OpenList 内置 WebDAV 的开启方式、端点 URL 与路径语义、鉴权、只读/读写差异。
3. **Rclone 挂载**：`rclone config` 远端配置、`rclone mount` 参数、VFS 缓存策略、掉线与开机自启（systemd）。
4. **Docker 映射**：用 bind mount / volume 把已挂载目录传进容器、UID/GID 与 PUID/PGID、只读挂载、性能与启动顺序。

### 重点收集

- **核心概念**: WebDAV 协议和 Rclone 的概念和使用；FUSE 用户态文件系统；Docker bind mount 与 named volume 的差异。
- **实战代码**: 部署 OpenList 的 compose 片段；WebDAV 端点验证命令；`rclone.conf` 远端配置；`rclone mount` 完整命令 + systemd unit；目标容器的挂载段。
- **常见坑**: 中文文件名编码；挂载点权限（`allow_other` 与 `/etc/fuse.conf`）；容器内 UID 不匹配导致只读/无权限；启动顺序（先挂载再起容器）；WebDAV 反代前缀；`rclone mount` 空闲掉线；OpenList 数据目录未持久化导致配置丢失。
- **工具链**: OpenList、Rclone、Docker / Docker Compose、systemd、FUSE3、可选 Nginx 反向代理。
- **进阶路径**: 多网盘聚合策略、VFS 缓存调优、直链与限速、挂载健康检查与监控。

### 信源偏好

- 官方文档: 是（`doc.oplist.org`、`rclone.org`、`docs.docker.com`）
- 技术博客: 是
- 社区讨论: 是（GitHub Issues / Discussions）
- 学术论文: 否

## 备注

- 用户原始请求中的「如何使用使用」为笔误，主题按一条链路理解。
- 章节顺序建议沿链路自然推进（OpenList → WebDAV → Rclone → Docker），每段保持"能跑通"的最小闭环。
- 已核查：本仓库 `workspace/workflow-runs/` 无同名或相关运行；vault 内无 openlist / alist / rclone 既有笔记。
- 体例可参考历史运行 `lunatv-import-sites`、`docker-container-host-file-access`、`docker-compose-commands`，但不重复其内容。
- 阶段 6 发布前需再次向用户确认 `vault_path` / `note_folder` / `moc_path`。
- 本机为 Windows + Git Bash，若要给出 Linux 侧命令，需注明执行环境（宿主机 Linux / NAS / WSL）。
