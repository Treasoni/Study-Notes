# SearXNG 自托管与 Hermes 接入 - 意图文件

## 基本信息

- **主题**: SearXNG 自托管与 Hermes 接入
- **项目标识**: searxng-hermes
- **运行标识**: searxng-hermes
- **工作流**: learning-note-flow
- **创建时间**: 2026-10-07
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目
- **笔记目录**: AI学习/Hermes Agent/SearXNG 自托管指南
- **MOC 路径**: AI学习/Hermes Agent/Hermes Agent MOC.md

## 学习目标

### 笔记类型
概念 + 实战混合（`concept` + `practice`）：先用概念铺垫讲清「SearXNG 是什么、为什么值得自托管」，再落到实战教程「Docker 部署 → 开启 JSON API → 接入 Hermes → 验证排错」。

### 学习深度
上手（够用即止）。目标不是研究 SearXNG 内部实现，而是**跑起来一个本地实例并成功接入 Hermes**。

### 用户基础
有了解。已熟悉 Hermes / Claude Code 配置体系（SOUL.md / AGENTS.md / config.yaml / .env），并有 Docker 自托管经验。

## 研究计划

### 探索方向
1. **SearXNG 是什么**：元搜索引擎原理、聚合 70+ 引擎、隐私模型（不追踪/不画像）、与 Google/DDG 的差别、自托管 vs 公共实例的取舍。
2. **怎么搭**：Docker 自托管完整落地（官方推荐路径）、`searxng/searxng:latest` 镜像、数据卷、`settings.yml` 覆盖、**开启 JSON 格式**（Hermes 必需，SearXNG 默认关闭）。
3. **怎么接 Hermes**：`SEARXNG_URL` 指本地实例、`web.search_backend: "searxng"`、`hermes tools` 选择路径、"无需 API key" 的关键点。
4. **验证与排错**：`curl ...?format=json` 自检、`403 Forbidden` = JSON 未开、容器未起、`web_extract` 需另配 provider 的边界。
5. **进阶（可选）**：改端口/改引擎/关不用的引擎、限流与反爬、公共实例 vs 自建对比表。

### 重点收集
- **核心概念**: 元搜索（metasearch）、聚合器、隐私代理（IP 为实例 IP）、无账号无 cookie、AGPL-3.0 与社区维护模式。
- **实战代码**: `docker-compose.yml`、`docker compose up -d`、`docker cp` 取回/写回 `settings.yml`、`docker restart`、验证用 `curl`、Hermes 侧 `SEARXNG_URL` 与 `config.yaml` 配置块。
- **常见坑**: JSON 格式默认关闭导致 `403`；`SEARXNG_BASE_URL` 与访问地址不一致；改端口后 `SEARXNG_URL` 未同步；SearXNG **只管搜索不管正文提取**（`web_extract` 需另配 provider）；公共实例会限流/随时关 JSON；`latest` 滚动更新无版本号的升级策略。
- **工具链**: Docker / Docker Compose、Hermes Agent（Web Search & Extract）、`searx.space`（公共实例列表）、官方文档 `docs.searxng.org`。

### 信源偏好
- 官方文档: 是（Hermes 官方 `web-search.md`、SearXNG 官方 `docs.searxng.org`）
- 技术博客: 是（自托管实操、避坑）
- 社区讨论: 是（GitHub Issues、公共实例限流经验）
- 学术论文: 否

## 关键已核实事实（供后续阶段避免臆造）

- GitHub `searxng/searxng`：Python 编写，AGPL-3.0，`master` 分支滚动更新，**不发版本 release**，镜像 `searxng/searxng:latest`。
- Hermes 官方文档 `website/docs/user-guide/features/web-search.md` 含 **「Option A — Self-host with Docker (recommended)」** 完整配方；原话 *"**No API key required** — just point Hermes at a running SearXNG instance."*
- SearXNG **默认关闭 JSON 格式**，Hermes 必需，需在 `settings.yml` 的 `search.formats` 加 `json`。
- SearXNG **仅 search-only**，`web_extract` 需另配 extract provider（官方明确限制）。

## 备注

- 部署机型：与 Hermes **同机本地 Docker**（`localhost:8888`），走"最省事"路径。
- 发布定位：作为 [[Hermes Agent MOC|Hermes Agent 学习分册]] 的姊妹篇（SearXNG 为该 agent 的搜索后端），完成后在 Hermes Agent MOC 追加一条索引项。
- 已有可复用笔记：[[AI学习/Hermes Agent/Hermes Rules 配置指南/README|Hermes Rules 配置指南]]、[[AI学习/Hermes Agent/Hermes Tool 配置指南/README|Hermes Tool 配置指南]]（配置体系与工具接入的对照锚点）。
