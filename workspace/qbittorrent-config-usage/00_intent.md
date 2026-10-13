# qBittorrent 下载器的配置与使用 - 意图文件

## 基本信息

- **主题**: qBittorrent 下载器的配置与使用
- **项目标识**: qbittorrent-config-usage
- **运行标识**: qbittorrent-config-usage
- **创建时间**: 2026-10-07
- **当前阶段**: 阶段 0（等待用户确认）
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目
- **笔记目录**: `流媒体与影音/qBittorrent 配置与使用/`（已确认，新建；纠正既有 `qBittorent/` 的拼写）
- **MOC 路径**: 流媒体与影音 MOC.md（归入「部署与配置」节）

## P0 用户确认（2026-10-07）

| 决策项 | 结论 |
| --- | --- |
| 与旧笔记关系 | **A**——新写一篇；既有 `qBittorent/` 的 4 篇**原位不动**，只在新篇给一句指引 |
| 成品粒度 | **单篇**（若超 ~30 KB 再建议拆分册） |
| 发布位置 | 新建 `流媒体与影音/qBittorrent 配置与使用/`，并加入 `流媒体与影音 MOC` |
| 部署环境 | **fnOS + Docker**（与 `nastool 家庭影院 fnOS 部署` 对齐） |
| 深度 / 基础 | 上手 / 有了解 |

## 学习目标

### 笔记类型

实战（配置 + 使用），配必要的概念铺垫（小白友好档：入门优先）

### 学习深度

上手——装得起来、配得对、日常用得顺，能自己排常见故障

### 用户基础

有了解——已在 Docker 里跑过 qBittorrent，且写过 4 篇旧笔记；熟悉 fnOS / Docker Compose

## 研究计划

### 探索方向

1. **装起来**：Docker 部署（面向 fnOS + MoviePilot 栈）——镜像选型（官方 / linuxserver / 增强版 fork）、`docker-compose.yml`（卷、端口、PUID/PGID）、WebUI 首次登录与初始口令
2. **配好**：连接与监听端口（BT 端口映射）、下载目录与硬链接（与 MoviePilot「同一路径」口径一致）、分类与标签、队列与限速、代理、IP 过滤、下载完成回调
3. **用起来**：加种子（磁力 / torrent 文件）、RSS 订阅、Tracker、PT 私种与分享率、做种与 H&R 避坑、常见故障速查

### 重点收集

- **核心概念**: BT/P2P、Tracker / DHT / PEX、种子与元数据、做种与分享率、私种（PT）与 H&R、硬链接
- **实战代码**: 可照抄的 `docker-compose.yml`、WebUI 关键设置项的取值与位置
- **常见坑**: BT 端口未映射导致无速度、下载目录跨文件系统导致硬链接失效、代理与 PT 站冲突、版本下限与 MoviePilot 的兼容
- **工具链**: MoviePilot V3、Jellyfin / Emby、CookieCloud

### 信源偏好

- 官方文档 / 官方仓库（qBittorrent）为主
- linuxserver 镜像文档（容器化部署口径）
- 既有 `nastool 家庭影院 fnOS 部署` 分册（本册与它的接口口径必须一致）
- 社区经验仅作为**已标注的运维经验**使用

## 与既有笔记/分册的关系

- 上级分册 `流媒体与影音/nastool 家庭影院 fnOS 部署/` 只把 qBittorrent 当作**前提条件**列出（版本 `>= 4.3.9`、下载目录映射、完成回调），**没有教怎么装和怎么配**——这正是本册要补的缺口。
- vault 根目录已有旧笔记 `qBittorent/`（4 篇，`updated: 2026-04-05`）：`qBittorrent的使用`、`qBittorrent配置代理`、`qBittorrent的Tracker`、`qBittorrent PT站点与分享率`。**需在阶段 0 确认本册与它们的关系**（替代 / 合并 / 并存）。

## 备注

### 上游核实结果（2026-10-07 探测，GitHub API）

| 项目 | 状态 | 一手依据 |
| --- | --- | --- |
| `qbittorrent/qBittorrent`（官方） | 活跃，`archived: false`，`pushed_at` 2026-10-06 | `api.github.com/repos/qbittorrent/qBittorrent` |
| 官方最新稳定版 | **v5.2.4**，发布于 2026-09-28 | `api.github.com/repos/qbittorrent/qBittorrent/releases/latest` |
| `c0re100/qBittorrent-Enhanced-Edition` | 活跃，`pushed_at` 2026-10-03 | `api.github.com/repos/c0re100/qBittorrent-Enhanced-Edition` |
| `linuxserver/docker-qbittorrent` | 活跃，`pushed_at` 2026-10-04 | `api.github.com/repos/linuxserver/docker-qbittorrent` |

### 写作纪律（本册必须显式处理的已知风险）

1. **旧笔记的版本口径已过时**：旧笔记写「官方稳定版 v5.1.x 系列 / 官方测试版 v5.2.0rc1」，与实测不符——按上面的一手探测，官方最新稳定版是 **v5.2.4**。本册不得沿用旧笔记的版本表述，须回官方 release 页面取一手值。
2. **「增强版」是社区 fork，不是官方版本**：`c0re100/qBittorrent-Enhanced-Edition` 与官方是**两个不同项目**，不是同一个项目的两个版本。笔记中必须明确区分，不得写成本项目的一个版本（同 `research-tools.md` 关于「社区封装 / 官方」不同项目的纪律）。
3. **大小写口径**：上级分册表格里写的 `Qbittorrent` 不是规范写法，官方品牌写法为 `qBittorrent`；本册统一用官方写法，并在首次出现时点明这一点。
4. **与上级分册的接口口径必须一致**：下载目录映射（`/downloads`）、版本下限（`>= 4.3.9`）、完成回调命令等说法，若与 `nastool 家庭影院 fnOS 部署` 分册冲突，以一手来源为准并显式记录差异。
