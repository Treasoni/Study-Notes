# update_plan — docker容器如何更新.md

> 运行：update-docker / container-update
> 生成：2026-08-04
> 依据：`workspace/update-docker/shared_research/source_bank.md`（S1 / S2 / S3）

## 目标

全面刷新到 2026 最新，同时保持「容器如何更新」的核心流程不变。核心更新路径（`docker compose pull` + `up -d`、`docker run` 重建）是 timeless 的正确做法，只补版本现状与相关新特性。

## 变更点

1. **frontmatter 补齐**
   - 补 `status: 已更新`、`source_project: docker`
   - `updated` 2026-02-09 → 2026-08-04
   - 保留 `created`（2026-02-09）与 `tags`（docker）

2. **版本背景**（开头新增 `[!note]` callout）
   - 截至 2026 年，Docker Engine 当前稳定版为 **29.x**（如 29.6.2），Docker Compose 为 **v5.x**（S1/S2）
   - 明确 `docker compose`（v2 插件）为当前标准用法，旧版 `docker-compose`（v1，基于 Python）已废弃

3. **§1.1 拉取镜像处新增 `[!tip]`**
   - Docker Engine 29 增强 BuildKit 构建并引入镜像层去重（image layer dedup），频繁更新镜像时可减少重复镜像层占用的磁盘空间（S1）

4. **末尾新增 `## 更新记录`**
   - 日期 2026-08-04 + 本次变更摘要

## 为何不做

- **不加入 `docker compose watch`**：compose watch 是开发期自动重载特性，且不在共享资料库中，无法从资料库核实，故不添加；本笔记主题是「更新容器」，非开发热重载。
- **不修改 nginx:1.25.0 / ubuntu:22.04 等示例标签**：这些只是演示命令的示例值，不是 Docker 版本引用，资料库也无相关版本数据；改动会偏离「只改过时内容」原则。

## 保持不变的核心流程

§1 compose 更新、§1.2 `--pull always`、§1.3 `--force-recreate`、§1.4 备份、§2 docker run 重建、§2.5 runlike、§3 部署方式确认、§4 验证、§5 回滚、§6 数据安全检查、§7 常见问题、§8 Watchtower/Portainer、§9 切换镜像版本 — 全部保留原文。
