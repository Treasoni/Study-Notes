# stale_map — docker里的GID和UID

> 更新范围：重写为完整入门指南（用户 2026-09-14 确认）
> 日期：2026-09-14
> 上一轮：2026-08-04，仅补 frontmatter，且只落到 `updates/gid-uid/updated_note.md`，**未回写 vault 笔记**，故 vault 中仍是「无 frontmatter + 损坏行」状态。

## 保留

| 区块 | 说明 |
|------|------|
| 主题与定位 | 「权限问题入门」定位不变，仍是 MOC 的「基础概念 / 解决权限问题」条目 |
| 原有双链 | [[Docker MOC]]、[[docker容器搭建错误的知识讲解]]、[[docker容器如何更新]] 全部有效 |
| 核心例子 | `-rw-r--r-- 1 root root xxx.mkv` / `rm` 被拒 / `id zhq` 输出 |
| 媒体容器场景 | qBittorrent / Transmission / Sonarr / Radarr / Jellyfin 名单与「90% 要求 PUID/PGID」结论 |

## 需要更新

| 区块 | 说明 |
|------|------|
| frontmatter | 缺 `title` / `created` / `updated` / `status` / `source_project`；`tags` 仅 `docker` |
| 第 1 节损坏行 | `> **Docker 里常见的是 UID / GID> ` 未闭合 `**` 且句子被截断，Obsidian 渲染异常 |
| 结构 | 原为 4 个 `# N.` 平铺小节，缺「验证 / 排查 / 坑位」环节，无法独立解决权限问题 |
| 代码块语言 | `-rw-r--r-- 1 root root xxx.mkv` 等**输出**被标成 ```bash，语义错误 |
| 关键事实错误 | 原文把 `PUID/PGID` 当作通用做法呈现；实际它**不是 Docker 功能**，仅支持的镜像（linuxserver / hotio 系）有效 |

## 需要删除

- 无整段删除；损坏行按原意重写（非删除）

## 需要新增

| 区块 | 说明 |
|------|------|
| `> [!summary] 本笔记解决什么问题` | 对齐 vault 新版笔记体例 |
| `## 目录` | 章级锚点导航 |
| 第 1 章补 | `id` / `id -u` / `id -g` 查法 + 输出示例；UID/GID/PID 三者区分 |
| 第 2 章补 | 「Docker 不做 UID 映射」根因；644 权限位为什么「能读不能删」的精确解释 |
| 第 3 章（新） | 三招对照表 + `chown` / `user:` / `PUID·PGID` 三种解法完整写法 |
| `> [!warning]` | PUID/PGID 不是 Docker 功能：由镜像 entrypoint 读取；linuxserver 与 `--user` 不兼容 |
| 第 4 章（新） | 验证与排查三步：`docker exec id` → `docker inspect .Config.User` → `ls -ln` |
| 第 5 章（新） | 常见坑表 7 条：`PUID=0`、存量文件不自动 chown、`--puid` 不是参数、非数字注入、rootless 重映射、命名卷残留、Docker Desktop `/mnt/c` 9P 属主 |
| `[!tip] 大白话` ×4 | 数字工号 / 文件柜管理员 / 三张工牌（用户偏好体例） |
| 更新记录 | 记本次重写 |

## 标记（未处理）

- 无
