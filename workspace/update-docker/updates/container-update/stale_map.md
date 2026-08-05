# stale_map — docker容器如何更新.md

> 运行：update-docker / container-update
> 生成：2026-08-04
> 原文件：`docker/docker容器如何更新.md`（只读，不修改）
> 更新目标：全面刷新到 2026 最新

| # | 区域 | 判定 | 说明 |
|---|------|------|------|
| — | frontmatter | **update** | 补 `status`、`source_project`；`updated` 2026-02-09 → 2026-08-04；保留 `created` 与 `tags` |
| 简介 | 开头段落之后 | **add** | 新增 `[!note]` 版本背景：Docker Engine 29.x（29.6.2）/ Compose v5.x；明确 `docker compose`（v2 插件）为标准、`docker-compose`（v1，Python）已废弃 |
| §1.1 | 标准更新流程（compose pull + up -d） | **keep** | 核心流程 timeless，正确 |
| §1.1 | 拉取最新镜像步骤 | **add** | 新增 `[!tip]`：Docker Engine 29 增强 BuildKit 并引入镜像层去重（image layer dedup），频繁更新可减少磁盘占用 |
| §1.2 | 快捷更新 `up -d --pull always` | **keep** | 正确 |
| §1.3 | 强制重建 / 指定服务更新 | **keep** | 正确 |
| §1.4 | 更新前备份（volume tar） | **keep** | 校验无误，仍正确 |
| §2.1-2.4 | docker run 重建流程 | **keep** | 正确 |
| §2.5 | runlike 获取 run 命令 | **keep** | 仍为有效社区工具 |
| §3 | 确认是否 compose 部署 | **keep** | 正确 |
| §4 | 验证更新成功 | **keep** | 正确 |
| §5 | 回滚 | **keep** | 正确 |
| §6 | 数据安全检查 | **keep** | 正确 |
| §7 | 常见问题 | **keep** | 正确 |
| §8 | 自动更新工具（Watchtower / Portainer） | **keep** | 仍有效 |
| §9 | 切换镜像版本 | **keep** | 命令与概念稳定；nginx 等示例标签仅为演示值，非 Docker 版本引用，不改 |
| 末尾 | 更新记录 | **add** | 新增 `## 更新记录`，日期 2026-08-04，记录本次变更 |

## 明确不做的改动

- **不新增 `docker compose watch`**：该功能不在共享资料库中，无法从资料库核实，按「不添加资料库外推测事实」原则省略。
- **不重写任何非过时段落**：9 节核心流程、命令、示例全部保留原样。
- **不改动原 vault 文件**：仅输出新文件到 `updates/container-update/`。
