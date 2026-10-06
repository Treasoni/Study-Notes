# slskd 安装与使用 - 意图文件

## 基本信息

- **主题**: 如何使用 slskd（自托管 Soulseek 客户端）
- **项目标识**: slskd-usage
- **运行标识**: slskd-usage
- **创建时间**: 2026-09-14
- **当前阶段**: 阶段 0
- **输出目标**: obsidian（发布前先落项目 `output/`）
- **Vault 路径**: `D:\Study-Notes`（本 vault）
- **笔记目录**: `docker/`
- **MOC 路径**: `docker/Docker MOC.md`

## 已确认的源信息

- **用户提供来源**: `https://github.com/slskd/slskd#quick-start`
- **官方文档站**: https://slskd.org
- **仓库**: `slskd/slskd`（默认分支 `master`）

### GitHub API 预取事实（2026-09-14）

| 项 | 值 |
| --- | --- |
| 描述 | A modern client-server application for the Soulseek file sharing network |
| 语言 / 许可 | C# / .NET · AGPL-3.0 |
| Star | ~3904 |
| topics | soulseek, soulseek-network, soulseek-web |
| 运行形态 | 守护进程 / Docker 容器，浏览器访问 Web UI |

### Quick Start 事实（README）

- Docker 两种用户指定方式：Docker 内置 `--user 1000:1000`、Linuxserver/*arr 风格 `PUID`/`PGID`
- docker-compose 同样两种写法；镜像 `slskd/slskd`；容器内应用目录挂载到 `/app`
- 端口：`5030` = HTTP Web UI，`5031` = HTTPS（自签证书），`50300` = 入站连接监听
- 默认账号密码均为 `slskd` / `slskd`，面向公网必须修改
- `SLSKD_REMOTE_CONFIGURATION=true` 允许从 Web UI 修改配置（公网部署建议关闭）
- 同时提供二进制（binaries）运行方式

### `docs/` 目录清单（Phase 2 素材索引）

| 文件 | 大小 | 用途 |
| --- | --- | --- |
| `config.md` | 85 KB | 配置全集（认证、共享、下载、限速等） |
| `relay.md` | 10 KB | Relay 中继 |
| `reverse_proxy.md` | 4 KB | 反向代理 |
| `docker.md` | 3.7 KB | Docker 进阶 |
| `build.md` | 3.5 KB | 构建 |
| `migrations.md` | 3.1 KB | 版本迁移 |
| `vpn.md` | 2.3 KB | VPN 绑定 |
| `known_issues.md` | 1.5 KB | 已知问题 |
| `system_requirements.md` | 0.3 KB | 系统要求 |

## 学习目标

### 笔记类型

实战 · 操作指南（自托管软件上手）

### 学习深度

入门 → 上手

### 用户基础

有了解：具备 Docker 与自托管应用基础，无需从零解释容器概念

## 研究计划

### 覆盖范围（用户已确认）

- **A. 快速上手全链路**（主线）：Docker 部署 → Soulseek 账号配置 → 共享/下载目录 → Web UI 搜索、下载、队列管理
- **B. 关键配置详解**：从 `config.md` 提炼实际会改的部分 —— 认证与反向代理、共享目录与配额、下载/上传限速、黑名单
- **C. 进阶三件套**：压缩为速览小节（反向代理 / VPN 绑定 / Relay 中继）
- **D. 排错**：并入各章「常见坑」，不单独成章

### 必须覆盖的两个非官方 Quick Start 内容

1. **Soulseek 账号注册** —— slskd 只是客户端，账号需在 slsknet.org 注册
2. **共享目录要求** —— 不配置共享会被限速或踢下线，这是新手必踩步骤

### 探索方向（Phase 1 待细化）

1. 部署与首次登录全链路（Docker / compose / 二进制三条路径）
2. 账号与共享配置（Soulseek 账号、共享目录、配额、权限）
3. 日常使用（搜索、结果筛选、下载、队列、上传）
4. 配置与安全（认证、反代、VPN 绑定、限速、黑名单）
5. 排错与已知问题（端口 50300、文件权限、共享要求、常见报错）

### 重点收集

- **核心概念**: Soulseek 网络模型、client-server 架构、共享/下载目录、Relay
- **实战代码**: Docker run、docker-compose、配置文件 `slskd.yml`、环境变量
- **常见坑**: 端口 50300 未通、`1000:1000` 权限、不共享导致限流、公网裸奔默认密码
- **工具链**: Docker / Compose、gluetun（VPN）、反向代理、slskd MCP / API

### 信源偏好

- 官方文档: 是（`docs/` 与 slskd.org 优先）
- 技术博客: 是（社区部署实践、NAS 场景）
- 社区讨论: 是（GitHub Issues / Discord，用于排错与已知问题）
- 学术论文: 否

## 篇幅预期

约 3–5 万汉字；若超过 30 KB 或多于 3 章，按分册发布（与 `docker/MusicTagWeb音乐标签/` 同构）。

## 备注

- 全库检索 `slskd` / `soulseek` 零命中，属全新主题，无双链死链风险。
- 同类自托管应用既有约定：笔记落 `docker/`，MOC 落 `docker/Docker MOC.md`。
- 法务与合规提示需客观中性：Soulseek 是 P2P 网络，VPN 绑定与版权合规属用户自身责任，笔记只做技术说明。
