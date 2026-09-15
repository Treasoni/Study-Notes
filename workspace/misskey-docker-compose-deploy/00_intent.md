# 使用 Docker Compose 部署 Misskey - 意图文件

## 基本信息

- **主题**: 使用 Docker Compose 部署 Misskey
- **项目标识**: `misskey-docker-compose-deploy`
- **运行标识**: `misskey-docker-compose-deploy`
- **工作流**: `learning-note-flow`（大纲模式）
- **创建时间**: 2026-09-15
- **当前阶段**: 阶段 0（意图澄清，等待用户确认）
- **输出目标**: project-output（暂存 `./output/final_note.md`，Obsidian 位置待后续指定）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定

## 用户原始请求

> https://misskey-hub.net/ja/ ，我想学习如何使用 docker compose 部署这个项目

线索来源：Misskey 官方文档站（Misskey Hub），用户给出的是日文入口页。

## 学习目标

### 笔记类型

**实战（practice）**——主线是「照着做能跑起来」，而不是概念科普。

### 学习深度

跑通 + 关键配置。即：

1. 用 Docker Compose 拉起 Misskey 核心服务栈，能访问、能注册、能发帖；
2. 在跑通基础上覆盖实际使用必需的配置：域名与反向代理 / TLS、文件上传与对象存储、邮件发送；
3. 不深入生产级高可用、备份恢复策略、性能压测等运维专题（除非素材里有机成本低的关键坑）。

### 用户基础

有了解。用户已经掌握 Docker / Docker Compose 基本用法（本 vault 内已有 `docker-compose-commands`、`docker-compose-linux-install`、`docker-compose部署` 等相关笔记），不需要从「什么是容器」讲起。

**关键差异点**：Misskey 不是一个「单容器 + 一个数据库」的简单应用，它有自己特有的部署约束，这些才是本篇的重点，例如：

- 数据库不是原版 PostgreSQL，而是需要 **PGroonga** 全文检索扩展；
- 配置文件不是全靠环境变量，而是 `.config/default.yml` 这份结构化 YAML，且有 `url` 这类**一旦写错就很难迁移**的字段；
- 容器启动前后有依赖顺序和初始化要求。

### 部署目标环境

用户实际要部署在 **NAS / 自建服务器**（如 fnOS、群晖）上，x86_64。笔记需要：

- 给出通用可迁移步骤，同时标注 NAS 环境的差异点（Docker 版本、路径映射、权限、内网访问、可能缺少 `docker compose` v2）；
- 不假设用户有公网域名；需说明「仅内网使用」与「对外提供服务」两种情形的配置差别。

## 研究计划

### 探索方向

1. **官方部署路径**：Misskey Hub 的 Docker 部署文档 + Misskey 仓库自带的 compose 示例（`.config/docker_example.yml`、`.config/docker_example.env`），确认官方推荐的 compose 结构、镜像标签策略、各服务职责。
2. **配置项最小集**：`.config/default.yml` 里哪些字段是**必须改**、哪些可以留默认、哪些改错会出问题（尤其是 `url`、数据库连接、Redis、`proxyBypassHosts` 之类）。
3. **NAS 落地与排错**：在 NAS / 自建服务器上跑时容易踩的坑——CPU 架构、内存下限、构建时间、卷权限、反向代理与 TLS、内网访问、端口冲突、升级方式。

### 重点收集

- **核心概念**：Misskey 的服务构成（web / PostgreSQL+PGroonga / Redis / 反向代理各自解决什么）、`default.yml` 的配置模型、`url` 字段的作用与不可变性、容器网络与卷。
- **实战配置**：官方 compose 示例逐行解释；`.env` 变量命名规则（`POSTGRES_PASSWORD` 等如何被 compose 注入）；PGroonga 镜像的选择；反向代理示例（Caddy 自动 TLS / Nginx）。
- **常见坑**：`url` 配置错误导致无法登录或媒体 URL 失效；PGroonga 未启用导致搜索报错；内存不足导致构建失败或被 OOM kill；卷权限；数据库密码与配置不一致；`docker compose` v1/v2 命令差异；升级镜像时的数据库迁移。
- **工具链**：Docker Engine / Docker Compose v2、PostgreSQL + PGroonga、Redis、Caddy / Nginx、可选对象存储（S3 兼容）。
- **对照**：与用户已有 Docker 笔记的衔接点，避免重复讲通用 compose 语法。

### 信源偏好

- 官方文档：**是，优先**（Misskey Hub 部署文档、Misskey GitHub 仓库内的示例文件与 release notes）
- 技术博客 / 社区：是（自建实例的实战记录，尤其 NAS 部署，需标注为二手）
- 社区讨论：是（Misskey GitHub Issues / Discussions，用于确认已知坑）
- 学术论文：否

## 待核实事项（交给 research-collector 回源确认，planner 不作断言）

以下都是**需要从官方文档或仓库示例核实**的点，planner 不预设结论：

1. 官方当前推荐的 compose 示例文件路径与名称，以及 compose 文件与 `.config/example.yml` 的对应关系。
2. PostgreSQL 镜像的具体选择（是否使用带 PGroonga 的官方/第三方镜像，版本号）。
3. Misskey 对内存/CPU 的官方最低与推荐要求。
4. Docker 部署文档中推荐的反向代理方案及其示例配置。
5. 镜像标签策略（`latest` vs 固定版本号）在升级时的推荐做法。
6. 文档是否有中文版；日文版与英文版内容是否有差异。
7. 用户已有的 Docker 笔记具体覆盖了哪些内容，避免重复。

## 备注

- 本 vault 内已存在若干 Docker 相关笔记，阶段 2 收集前可先扫一遍，避免内容重叠。
- 用户的 Obsidian vault 路径未提供；本篇先落在 `./output/final_note.md`，阶段 6 再确认发布位置。
