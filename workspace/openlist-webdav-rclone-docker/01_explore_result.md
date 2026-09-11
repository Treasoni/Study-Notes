# 01 探测结果 — OpenList → WebDAV → Rclone → Docker

- **运行标识**: openlist-webdav-rclone-docker
- **阶段**: P1 探测式收集
- **探测日期**: 2026-09-12
- **探测方式**: 3 个并行 subagent，各负责 1 个独立 lens，每 lens 产出 3–5 条候选来源
- **环境基线**: 链路实际运行在 Linux 宿主机 / NAS；本机为 Windows + Git Bash（命令环境需在正文中标注）

## Lens 划分

| Lens | 覆盖范围 |
|---|---|
| A | OpenList 本体 + 内置 WebDAV 服务 |
| B | Rclone 概念与 mount 挂载（含 FUSE、开机自启） |
| C | Docker 把已挂载目录映射进容器（含权限与端到端实操） |

## 来源清单（已按 canonical URL 去重）

| ID | 来源 | URL | Tier | 日期 | Lens | 评分 |
|---|---|---|---|---|---|---|
| S01 | OpenList 官方文档 — 使用 Docker 安装 | https://doc.oplist.org/guide/installation/docker | 1 | 站点构建 2026-09-10 | A | 5 |
| S02 | OpenList 官方文档 — WebDAV | https://doc.oplist.org/guide/advanced/webdav | 1 | 站点构建 2026-09-10 | A | 5 |
| S03 | OpenList 官方文档 — 用户与权限 | https://doc.oplist.org/guide/advanced/user | 1 | 站点构建 2026-09-10 | A | 4 |
| S04 | AList Docs — WebDav（**上游口径，非 OpenList 官方**） | https://alistgo.com/guide/webdav.html | 1 | 2022-09-07 | A | 4 |
| S05 | 凡凡小站 — Docker 部署 OpenList 网盘挂载工具 | https://www.meimolihan.eu.org/posts/1d511e0a.html | 2 | 2025-09-12 | A | 3 |
| S06 | rclone mount（官方命令文档） | https://rclone.org/commands/rclone_mount/ | 1 | 随 v1.75.x | B / C | 5 |
| S07 | WebDAV（rclone 官方远端文档） | https://rclone.org/webdav/ | 1 | 随 v1.75.x | B | 5 |
| S08 | rclone Documentation（官方总览） | https://rclone.org/docs/ | 1 | 随 v1.75.x | B | 4 |
| S09 | FUSE Overview（Linux 内核官方文档） | https://docs.kernel.org/filesystems/fuse/fuse.html | 1 | 滚动更新 | B | 4 |
| S10 | rclone 论坛 Howto — 开机持久挂载（Fedora） | https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738 | 3 | 2026-05-02 | B | 3 |
| S11 | Bind mounts — Docker Docs | https://docs.docker.com/engine/storage/bind-mounts/ | 1 | 持续维护 | C | 5 |
| S12 | Understanding PUID and PGID — LinuxServer.io | https://docs.linuxserver.io/general/understanding-puid-and-pgid/ | 1 | 持续维护 | C | 5 |
| S13 | rgdevment/jellyfin-rclone — README（端到端案例） | https://github.com/rgdevment/jellyfin-rclone | 2 | 2025-06-04 | C | 4 |
| S14 | 群晖 NAS：Docker Rclone + OpenList 挂载 Plex 全攻略 | https://rmbk.cc/article/article-4962.html | 3 | 2026-03-09 | C | 3 |

**Tier 分布**：T1 × 10、T2 × 2、T3 × 2。官方文档占比高，主干无需依赖社区来源。

## 关键发现（待 P2 回源核实）

> 以下均为 P1 侦察所得的**线索**，不是结论。P2 必须回原文逐条核对后再写入 `02_deep_research.md`。

1. **WebDAV 端点语义**：OpenList 的内置 WebDAV 挂在主 HTTP 服务的 `/dav/` 路径下，账号密码与网页端相同，也可为单个存储加子路径（线索源 S02）。
2. **权限粒度**：OpenList 用户可逐项配置 WebDAV 读取 / WebDAV 管理与 mkdir、rename、move、copy、delete 等文件系统权限，官方文档附有「越权可访问内网」的安全警告（线索源 S03）。这是「只读 vs 读写」那一节的关键依据。
3. **⚠️ 版本断点**：S01 被指称含「v4.1.0 起由 PUID/PGID 改为 compose `user:`」这一重大变更。**这是 P1 转述，必须在 P2 回 S01 原文核实**，因为它同时影响第 1 章（OpenList 部署）和第 4 章（Docker 权限）两处写法。
4. **driver 能力矩阵**：AList 口径页给出各存储驱动的 WebDAV 读写能力差异（本地目录 / 阿里云盘 / OneDrive / 夸克 / 百度可读写，个别驱动不支持 copy）。引用时须标注为**上游 AList 口径**，不可当作 OpenList 官方结论（线索源 S04）。
5. **`--vfs-cache-mode` 四档**：off / minimal / writes / full 的差异与 mount 同 sync/copy 的可靠性取舍，是「Rclone 概念」一节的主干（线索源 S06）。
6. **PUID/PGID 不是 Docker 特性**：S12 明确它是镜像 entrypoint 读取的环境变量；`chown` 只覆盖 `/config` 而不覆盖媒体挂载点 —— 这解释了「为什么权限设了还是 permission denied」，是高价值排障素材。
7. **两种容器化挂载架构**（本主题最值得展开的对比点）：
   - 架构一：宿主机 `rclone mount` → bind mount 给容器（S13、S14）
   - 架构二：`rclone mount` 跑在容器内，需 `--device /dev/fuse`、`SYS_ADMIN`、`apparmor:unconfined`、`/etc/passwd` 与 `/etc/group` 只读挂载、`:shared` 传播（线索源 S06）
8. **`allow_other` 与 `/etc/fuse.conf`**：`allow_other` 依赖 `user_allow_other` 配置项，权威说明在内核文档（S09），rclone 站内仅在变更日志提及；未开启会直接导致 mount 失败（S10 有对应报错记录）。

## 覆盖缺口与风险

| 类型 | 内容 | 影响 |
|---|---|---|
| ⚠️ 可达性 | **`docs.docker.com` 在本机被网络策略拦截**（探测时 curl 返回 000），S11 的 URL 是依据官方文档结构与检索结果给出，**未实测可达** | P2 精读 S11 时若 crawl 失败，需改用镜像源或明确降级为「结构已知、原文未核」 |
| 结构缺口 | 没有任何单一来源串起 `OpenList + WebDAV + rclone + qBittorrent` 的完整 compose | 第 4 章需由通用 `:ro` / `rw` 模式推演，推演部分必须显式标注为推断 |
| 来源层级 | 官方站无 systemd 专页，开机自启只能靠 tier 3（S10） | 与该节相关的结论需标为「社区操作经验」而非官方口径 |
| 边界 | Windows / WSL 侧未覆盖（Windows 的 `rclone mount` 依赖 WinFsp） | 本机是 Windows，正文需明确「本笔记以 Linux 宿主机为准」，避免用户照抄失败 |
| 体例风险 | S05 发布于 v4.1.0 之前，其 PUID/PGID 写法可能已过期 | 引用 S05 前须先确定版本断点（见关键发现 3） |

## 方向菜单（待用户选择，不要替用户决定）

### 方向 A — 全链路主线版（推荐）

按 `OpenList → WebDAV → Rclone → Docker` 顺序，一段一个可验证闭环，聚焦 **Linux 宿主机 + Docker Compose**，终点落到「一个容器能读到网盘里的文件」。

- 适合：想从零跑通一遍并留下可复用配置
- 章节骨架：OpenList 部署 → 网盘聚合与用户权限 → 开 WebDAV 并验证 → Rclone 配置与 mount → 映射给容器 → 排障速查
- 主要来源：S01 S02 S03 S06 S07 S11 S12

### 方向 B — 全链路 + 挂载架构对比版

在方向 A 基础上，把「宿主机 mount 再 bind」与「容器内 mount 再暴露」两种架构并列对比，讲清各自的适用边界与代价。

- 适合：想理解架构取舍、将来要接多个消费容器
- 代价：篇幅与收集量增加约 30%，需精读 S06 的容器内 mount 段落与 S13 / S14
- 主要来源：方向 A 全部 + S06（容器段） + S13 + S14

### 方向 C — 排障优先版

主线压缩为速查清单，重点展开权限与故障：UID/GID 不匹配、`allow_other` 未开、启动顺序、WebDAV 反代前缀、`rclone mount` 掉线、数据目录未持久化。

- 适合：已经能跑但反复出问题，想要一份「症状 → 原因 → 处置」的表
- 代价：概念铺垫会被削薄，与新主题「上手」定位略有偏移
- 主要来源：S03 S09 S10 S12 + 各实操帖的故障段落

> 方向 A 与 B 可合并（把架构对比作为 A 的一个小节），这是推荐默认。

## P2 预估范围

- **精读 3–5 篇核心源**：S01、S02、S06、S12，另按所选方向加 1–2 篇（A 加 S11；B 加 S13/S14；C 加 S09/S10）
- **其余来源**作补充引用，不全文精读
- **预判章节数**：方向 A 约 6 章；方向 B 约 7 章；方向 C 约 4–5 章
- **P2 必做**：回源核实「关键发现 3」的版本断点；确认 `docs.docker.com` 能否抓取，不行则记录降级
