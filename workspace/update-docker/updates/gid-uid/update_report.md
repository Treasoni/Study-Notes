# update_report — docker里的GID和UID

> 日期：2026-09-14
> 状态：✅ 已完成（重写为完整入门指南，已回写 vault）
> 目标文件：`docker/docker里的GID和UID.md`

## 变更摘要

- **规模**：119 行 / 1,383 字符 → 318 行 / 8,235 字符。
- **结构**：由 4 个平铺 `# N.` 小节改为「概念 → 根因 → 三招解法 → 排查三步 → 常见坑 → 实战场景」六章，加 `[!summary]`、章级目录锚点、`相关笔记`、`更新记录`。
- **修 bug**：原文第 1 节 `> **Docker 里常见的是 UID / GID>` 未闭合 `**` 且句子截断，Obsidian 渲染异常；按原意改写为「跟权限有关的是 UID/GID，不是 PID」并补 UID/GID/PID 对照表。
- **补 frontmatter**：`title` / `created`(2026-07-28) / `updated`(2026-09-14) / `status` / `source_project`，`tags` 增加 `权限` `UID` `GID`（保留原 `docker`）。
- **修事实错误（本轮最重要）**：原文把 `PUID` / `PGID` 当作 Docker 的通用做法；实为**镜像 entrypoint 读取的普通环境变量**，仅 linuxserver / hotio 系及基于其 baseimage 构建的镜像有效，官方镜像写了一点用没有。补 `[!warning]` 说明，并补上被遗漏的另外两条路（`chown` / `user:`）。
- **新增**：三招解法对照表、验证与排查三步、常见坑表 7 条（含 rootless 重映射、命名卷残留、Docker Desktop `/mnt/c` 的 9P 属主问题）、4 处 `[!tip] 大白话`、6 条双链。
- **格式**：命令输出示例由 ```bash 改为 ```text（它们不是可执行命令）。
- **MOC**：`[[Docker MOC]]` 的索引条目说明更新，更新日志加一条。

## 来源

| 来源 | 用途 |
| --- | --- |
| `workspace/openlist-webdav-rclone-docker/sources/S12_linuxserver_puid_pgid.md`（linuxserver 官方文档，scraped 2026-09-11） | PUID/PGID 定义、与 `--user` 不兼容 |
| `workspace/docker-container-host-file-access/chapters/04_权限与属主.md`（S3/S4/S5/S6） | 不做 UID 映射的根因、三招修复、userns-remap / rootless |
| WebSearch @2026-09-14 | 确认 PUID/PGID 非 Docker 功能、支持者名单（LSIO / hotio）、非数字值的注入风险 |
| WebSearch @2026-09-14 | WSL2 `/mnt/c` 走 9P、不保存 UID/GID、需 `metadata` 挂载选项 |

## 未处理风险

| 风险 | 说明 |
| --- | --- |
| `created: 2026-07-28` 为近似值 | 原文无 `created`，沿用 2026-08-04 那轮的 vault 文件时间戳，非确切创作日期 |
| linuxserver 与 `--user` 的兼容性可能变化 | 依据 2026-09-11 抓取的官方文档；官方措辞是「not yet compatible」，日后可能改变，长期需回访原文 |
| `abc` 用户默认 911 | 该细节来自二手来源（WebSearch 汇总），未逐字回原始文档核实，故正文未写入具体数字 |
| 未改动 [[Docker容器服务访问宿主机文件]] | 两篇存在主题重叠（该篇第 4 章讲同一件事）。本轮用双链指向而非去重合并；若要彻底去重需单独一轮 |
