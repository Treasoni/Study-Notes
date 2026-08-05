# update_report — docker容器如何更新.md

> 运行：update-docker / container-update
> 生成：2026-08-04
> 原文件：`docker/docker容器如何更新.md`（未修改）
> 输出：`updates/container-update/updated_note.md`

## 变更摘要

| 位置 | 变更 |
|------|------|
| frontmatter | 补 `status: 已更新`、`source_project: docker`；`updated` 2026-02-09 → 2026-08-04；保留 `created` 与 `tags` |
| 开头（简介后） | 新增 `[!note]` 版本背景：Docker Engine 29.x（29.6.2）/ Compose v5.x；`docker compose`（v2 插件）为标准、`docker-compose`（v1，Python）已废弃 |
| §1.1 拉取镜像 | 新增 `[!tip]`：Docker Engine 29 增强 BuildKit 并引入镜像层去重（image layer dedup），减少频繁更新时的磁盘占用 |
| 末尾 | 新增 `## 更新记录`（2026-08-04） |

**未改动**：§1-§9 全部核心流程与命令（compose pull + up -d、`--pull always`、`--force-recreate`、docker run 重建、runlike、回滚、数据安全检查、Watchtower/Portainer、镜像版本切换）按原样保留；非过时段落一律未动。

## 使用资料（`shared_research/source_bank.md`）

- **S1**（Docker Engine 29 release notes，官方）：Engine 29 为 2026 当前稳定大版本、最新补丁 29.6.2；新增 BuildKit 改进与镜像层去重。
- **S2**（Docker Desktop release notes，官方）：内置 Docker Compose v5.3.1（即 Compose v5.x）。
- **S3**（endoflife.date）：29.x 为当前维护线，28.x 已于 2026-05-13 EOL。

未使用 T2/T3/T4（镜像源、代理、WSL2）——本笔记不涉及这些主题。

## 未解决风险 / 说明

1. **`docker compose watch` 未加入**：该特性（Compose v2.21+ 的开发期自动重载）不在共享资料库中，无法从资料库核实；且本笔记主题是「更新容器」而非开发热重载。按「不添加资料库外推测事实」规则省略。如需补充，可先在共享资料库中登记后再加入。
2. **示例镜像标签未版本化**：`nginx:1.25.0`、`ubuntu:22.04` 等仅为命令演示示例，非 Docker 版本引用，资料库无对应数据，故保持原样。
3. **版本号时效**：29.6.2 / 4.83 / v5.3.1 为 2026-08 时的数据，Docker 滚动发布，后续小版本可能变化；笔记中已用「29.x / v5.x」表述以降低时效衰减。
4. **原文件零覆盖**：原 vault 文件未触碰，所有输出均在 `updates/container-update/`。
