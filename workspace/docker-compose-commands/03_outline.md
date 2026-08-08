# Docker 与 Docker Compose 命令的使用 - 大纲

> 笔记类型：概念速查（concept + cheat_sheet 混合）
> 预计总篇幅：约 16-20 页（正文 + 速查表，可随手翻阅）
> 章节数：6

> 说明：每条核心命令/概念均预留 `[!tip] 大白话` 通俗解释位置；高风险操作（清理、删卷）预留 `[!warning]` 易错提示。

## 第 1 章：初识 Docker：镜像与容器（大白话）
- **篇幅**: 短
- **素材引用**: §1.1 核心概念（大白话素材）
- **代码示例**: 否
- **内容要点**:
  - 镜像 = 模板 / 菜谱；容器 = 实例 / 一盘菜（`[!tip] 大白话` 位置）
  - 日常流程比喻：`pull`（拿菜谱）→ `run`（做菜上桌）→ `ps`（看摆了几盘）→ `stop/rm`（收走/倒掉）
  - 容器用完可扔，改动要写进 Dockerfile 重新 `build`，而非手工改容器
  - 本笔记怎么用：先通读第 1 章建立心智模型，后续章节当速查表随手翻

## 第 2 章：Docker 命令速查：镜像与容器管理
- **篇幅**: 中
- **素材引用**: §1.2 镜像管理、§1.3 容器管理
- **代码示例**: 是
- **内容要点**:
  - 镜像命令速查表：`pull` / `images` / `rmi` / `build -t` / `tag` / `push`（每条配一句 `[!tip] 大白话`）
  - `docker run` 核心语法与常用 Flag 表：`-d` / `-p` / `-v` / `-e` / `--rm` / `--name` / `--restart` / `-it`
  - 综合示例：`docker run -d -p 8080:80 --name web --restart=always nginx`
  - 容器生命周期命令：`ps` / `start` / `stop` / `restart` / `rm` / `exec` / `logs` / `inspect` / `cp` / `stats` / `top`
  - 易混点标注：`exec -it` 进运行中容器 vs `cp` 双向拷文件；`ps` 默认只看运行中，`-a` 含已停止

## 第 3 章：Docker 命令速查：网络、卷与系统管理
- **篇幅**: 短
- **素材引用**: §1.4 网络与卷、§1.5 系统管理
- **代码示例**: 是
- **内容要点**:
  - 网络命令组：`network ls / create / inspect / connect / disconnect / rm`
  - 数据卷命令组：`volume ls / create / inspect / rm / prune`
  - 系统命令组：`info` / `version` / `system df` / `system prune` / `login`
  - `system prune` 各 Flag 含义与风险：`-a`（连未用镜像）、`-f`、`--volumes`（高风险）
  - `[!warning]` 清理注意：卷默认不自动删除（官方理由：可能销毁数据）

## 第 4 章：Docker Compose：v1/v2 与核心命令
- **篇幅**: 中
- **素材引用**: §2.1 v1 vs v2、§2.2 compose 核心命令
- **代码示例**: 是
- **内容要点**:
  - `docker-compose`（v1，连字符）vs `docker compose`（v2，空格）区别表：实现、状态、文件兼容
  - 迁移方法：连字符改空格即 drop-in 兼容；v2 容器名用 `-`（`example-frontend-1`）、v1 用 `_`；v2 移除 `compose scale`
  - compose 核心命令表：`up` / `down` / `ps` / `logs` / `exec` / `build` / `pull` / `push` / `config` / `run` / `restart` / `stop` / `start` / `stats` / `top` / `images`
  - 关键 Flag：`up -d` 后台、`up --build`、`down -v`（破坏性删卷）、`config -q` 静默校验
  - `[!tip] 大白话`：Compose = 把一串 `docker run` 统一写进一个文件、一条命令编排成项目

## 第 5 章：compose.yaml 配置语法与常用工作流
- **篇幅**: 长
- **素材引用**: §2.3 compose.yaml 语法、§2.4 常用工作流
- **代码示例**: 是
- **内容要点**:
  - 顶层结构：`name` / `services` / `networks` / `volumes`
  - service 常用键详解：`image` / `build` / `container_name` / `command` / `entrypoint` / `ports` / `expose` / `environment` / `env_file` / `volumes` / `depends_on` / `healthcheck` / `restart` / `networks`
  - 关键语法点：命名卷必须顶层声明；`$VAR` 插值与 `$$` 转义；`${VAR:-default}` / `${VAR:?error}`；`.env` 自动加载与优先级（Shell > `--env-file` > `.env`）；默认文件名 `compose.yaml`；`-f` 可多次指定
  - 常用工作流命令序列：首次部署 → 更新镜像 → 跟随日志 → 进容器 → 优雅清理（保留卷）→ 校验配置
  - `[!tip] 大白话`：project / service / volume 比喻（项目 = 整套应用，服务 = 组件，命名卷 = 持久化仓库）

## 第 6 章：常见坑与排错
- **篇幅**: 长
- **素材引用**: §3.1 启动即退出、§3.2 权限、§3.3 清理、§3.4 Windows 路径、§3.5 其他高频坑
- **代码示例**: 是
- **内容要点**:
  - 容器启动即退出：退出码定性表（0 / 1 / 126 / 127 / 137），记忆规则「退出码 = 128 + 信号编号」，按序排查命令（`ps -a` → `inspect` → `logs` → `--entrypoint sh` 复现）
  - 权限问题：绑定挂载按数字 UID/GID 匹配；`-u $(id -u):$(id -g)` / compose `user:` / 宿主 `chown` / `PUID`·`PGID` 方案
  - 清理最佳实践：`system df` 预览 → `prune -a --filter "until=24h"` → 单类型 `prune`
  - Windows 挂载路径问题：`Invalid volume specification` 处理、`COMPOSE_CONVERT_WINDOWS_PATHS=0`、v2.35.0+ bind 源路径不存在新坑
  - 其他高频坑：端口冲突（`ps` / `ss` / `netstat` 定位）、YAML 校验（`$` 转义、`version:` 键移除）、更新不生效（`down` 后再 `up` / `--force-recreate`）
  - 末节「一页速查小结」：退出码速查 + 最常用命令一句话回顾（快速参考/总结位）

## 学习路径说明

### 前置要求
- 零基础即可，无需 Docker 经验
- 会基础命令行操作（终端 / PowerShell 中执行命令）
- 本机已安装 Docker Desktop 或 Docker Engine + Compose 插件（v2）

### 学完能做什么
- 读懂并运行常用 `docker` 命令（镜像、容器、网络、卷、系统清理）
- 看懂并编写最小 `compose.yaml`，用 `docker compose up -d` 一键部署多服务应用
- 排查最常见的三类问题：容器启动即退出、权限拒绝、端口冲突
- 安全地清理不用的镜像/容器/卷，避免误删数据
- 把本笔记当随身速查表，随时翻回对应命令表

### 建议学习顺序
- 第 1 章 → 第 2 章 → 第 3 章：先建立「镜像 vs 容器」心智模型，再上手 Docker CLI（约 1 小时）
- 第 4 章 → 第 5 章：进入 Compose，先分清 v1/v2 再学命令，最后啃配置语法（约 1-1.5 小时）
- 第 6 章：排错章节建议「用到再查」，不必一次背完；阅读完前 5 章后通读一遍建立印象（约 30 分钟）
- 总计：约 2.5-3 小时通读一遍，之后作为速查手册长期随查
