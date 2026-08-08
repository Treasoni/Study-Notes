# Docker 与 Docker Compose 命令的使用 - 探测式收集结果

收集时间: 2026-08-08
阶段: P1 探测式收集
搜索维度: Docker CLI 常用命令 / Docker Compose 命令与配置 / 常见坑与排错

---

## 一、Docker CLI 常用命令（镜像/容器/网络/卷/系统管理）

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Docker 官方 CLI 命令参考 | https://docs.docker.com/reference/ | 5/5 | 官方文档 |
| 2 | Docker 官方入门速查表 PDF | https://docs.docker.com/get-started/docker_cheatsheet.pdf | 5/5 | 官方文档 |
| 3 | Docker-Commands-Cheat-Sheet (GitHub) | https://github.com/Nikoo-Asadnejad/Docker-Commands-Cheat-Sheet | 4/5 | 社区仓库 |
| 4 | Docker Command Cheatsheet (dev.to) | https://dev.to/benriemer/the-docker-command-cheatsheet-every-developer-needs-on-their-desk-2njb | 4/5 | 技术博客 |
| 5 | The Only 30 Docker Commands You Actually Need | https://dev.to/the_aiproducer_5ec354687/... | 4/5 | 技术博客 |

**要点**：
- 基本语法 `docker [OPTIONS] COMMAND [ARG...]`，`docker --help` 总览
- 分组：镜像、容器、网络、卷、注册表、系统
- 高频 flag：`-d`（后台）、`-p`（端口）、`-v`（卷）、`-e`（环境变量）、`--rm`（用完即删）、`--restart`（重启策略）
- 清理：`docker system prune` 系列、`docker system df` 查看磁盘占用

---

## 二、Docker Compose 命令与配置

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | docker compose 命令官方参考 | https://docs.docker.com/reference/cli/docker/compose/ | 5/5 | 官方文档 |
| 2 | compose.yaml 文件语法官方参考 | https://docs.docker.com/reference/compose-file/ | 5/5 | 官方文档 |
| 3 | Compose 应用模型 | https://docs.docker.com/compose/compose-application-model/ | 4/5 | 官方文档 |
| 4 | LinuxServer.io Docker Compose 实战指南 | https://docs.linuxserver.io/general/docker-compose/ | 4/5 | 社区文档 |
| 5 | Docker Compose 常用命令速查表 (dev.to) | https://dev.to/primghostdev/docker-compose-cheat-sheet-the-10-commands-you-actually-need-2785 | 4/5 | 技术博客 |

**要点**：
- **v1 vs v2**：`docker-compose`（连字符，Python，已弃用 EOL 2022-04）vs `docker compose`（空格，Go 插件，内置，官方推荐）
- 核心命令：`up`（-d/--build/--force-recreate/--scale）、`down`（-v 删卷）、`ps`、`logs`（-f）、`exec`、`build`、`pull`、`config`（校验）、`run`、`stats`/`top`
- compose.yaml 顶层三大块：`services/networks/volumes`；service 常用键：`image`、`build`、`ports`（"host:container"）、`environment`、`env_file`、`volumes`、`depends_on`、`healthcheck`、`restart`、`networks`
- 命名卷须在顶层 `volumes` 声明；环境变量布尔值须加引号
- 更新流程：`docker compose pull && docker compose up -d`

---

## 三、常见坑与排错

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | Prune unused Docker objects（清理） | https://docs.docker.com/engine/manage-resources/pruning/ | 5/5 | 官方文档 |
| 2 | Docker container exits immediately（启动即退出） | https://www.netdata.cloud/guides/docker/docker-container-exits-immediately/ | 5/5 | 技术博客 |
| 3 | UID/GID mapping（权限） | https://docs.docker.com/engine/security/rootless/uid-gid-mapping/ | 4/5 | 官方文档 |
| 4 | Windows 目录挂载 invalid volume specification | https://stackoverflow.com/questions/79373371/... | 4/5 | 社区讨论 |
| 5 | Fixing YAML Formatting Errors in Compose | https://www.educative.io/courses/troubleshooting-docker-and-kubernetes-containers/np/formatting-errors-in-yaml-files | 4/5 | 技术博客 |

**要点**：
- **容器启动即退出**：exit code 含义（0 正常跑完 / 1 崩溃 / 126 无执行权限 / 127 二进制不存在 / 137 OOM）；排障顺序：exit code → `OOMKilled` → `docker logs` → inspect → `--entrypoint sh` 覆盖调试
- **权限**：绑定挂载按数字 UID/GID 匹配；`-u $(id -u):$(id -g)` 或 compose `user:` 对齐宿主属主
- **清理**：卷默认不删，须显式 `--volumes`；`-a` 删全部未使用镜像
- **Windows 路径**：`COMPOSE_CONVERT_WINDOWS_PATHS=0`；v2.35.0+ 不存在 bind 源路径直接报错
- **YAML**：`docker compose config --quiet` 快速校验；`$` 用 `$$` 转义；移除已弃用 `version:` 键
- **端口冲突**："port is already allocated" → `docker compose ps` / `ss -ltnp` 排查

---

## 综合分析

探测结果显示资料充分且权威度高（官方文档占比高）。三个方向正好对应一份「入门速查」笔记的自然结构：
1. **Docker CLI 命令速查**（基础，必须）
2. **Docker Compose 命令与配置**（进阶，必须）
3. **常见坑与排错**（实用补充，提升笔记价值）

由于笔记定位为「概念速查（concept + cheat_sheet 混合）」，建议三个方向全部覆盖，作为笔记的三大部分，而非择一。
