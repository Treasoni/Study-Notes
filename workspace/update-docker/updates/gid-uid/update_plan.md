# update_plan — docker里的GID和UID

> 日期：2026-09-14
> destination_mode：`patch-in-place`（直接改写 vault 笔记 `docker/docker里的GID和UID.md`）
> 用户确认：重写为完整入门指南（2026-09-14）

## 目标结构

| # | 章节 | 来源 |
|---|------|------|
| — | frontmatter + `[!info] 相关文档` + `[!summary]` + 目录 | 新增（对齐 vault 新版体例） |
| 1 | UID / GID 是什么 | 原文第 1 节重写（修损坏行）+ 补 UID/GID/PID 对照表、`id` 查法 |
| 2 | 为什么会 Permission denied | 原文第 2、3 节合并 + 补「Docker 不做 UID 映射」根因、644 权限位逐段拆解 |
| 3 | 三种解法 | 新增（原文只有 PUID/PGID 一条路） |
| 4 | 验证与排查三步 | 新增 |
| 5 | 常见坑 | 新增（7 条） |
| 6 | 实战场景：媒体 / 下载类容器 | 原文第 4.1 节扩写 |
| — | 相关笔记 + 更新记录 | 新增 |

## 关键事实修正

| 原文表述 | 修正后 | 依据 |
|---|---|---|
| `PUID`/`PGID` 写成通用做法 | 它们是**镜像 entrypoint** 读取的自定义环境变量，不是 Docker 功能；仅 linuxserver / hotio 系有效 | linuxserver 官方文档（vault 内 `workspace/openlist-webdav-rclone-docker/sources/S12_linuxserver_puid_pgid.md`，scraped 2026-09-11） |
| 未提 `--user` / `user:` | 补为方案 B；注明并非所有镜像支持任意用户启动 | `workspace/docker-container-host-file-access/chapters/04_权限与属主.md`（S5/S6） |
| 未提 rootless / Windows 语义 | 补入第 5 章常见坑 | WebSearch（2026-09-14）+ 深挖笔记 S3 |

## 不做的事

- 不复制 [[Docker容器服务访问宿主机文件]] 第 4 章的完整内容，只保留入门所需，深挖部分用双链指向
- 不改文件名（vault 内多处双链依赖 `docker里的GID和UID`）
- 不新增 MOC 条目，只更新原有条目说明与更新日志

## 验证清单

- [x] frontmatter 可解析，字段齐全
- [x] 7 个 wiki 目标逐条断言存在且唯一
- [x] 6 个章级锚点与 H2 标题逐字匹配
- [x] 12 个代码块全部带语言标识（bash / yaml / text）
- [x] 无「列表内嵌表格」（Obsidian 无法渲染）
- [x] MOC 更新日志与索引条目同步
