# 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件 - 大纲

> 笔记类型：实战笔记（上手级）
> 预计总篇幅：约 4200-5800 字
> 章节数：7

## 章节概览

| 章 | 标题 | 篇幅 | 核心内容 |
|----|------|------|---------|
| 1 | 三种挂载方式怎么选（bind / volume / tmpfs） | 400-600 字 | 选型判据 |
| 2 | 命令行挂载：`docker run -v` 与 `--mount` | 600-800 字 | CLI 写法与差异 |
| 3 | Compose 挂载：`volumes` 长短语法与顶层声明 | 600-800 字 | Compose 写法 |
| 4 | 权限与属主：permission denied 的根因与修复 | 800-1000 字 | UID/GID、user、PUID/PGID、userns-remap |
| 5 | 安全边界：只读、SELinux 与 docker.sock 风险 | 600-800 字 | 信任模型与缓解 |
| 6 | Docker Desktop 的差异：macOS/Windows 挂载性能 | 400-600 字 | 性能根因与规避 |
| 7 | 实战案例：Web 服务读写宿主目录的完整配置 | 600-800 字 | 综合走查 + 检查清单 |

## 详细大纲

### 第 1 章：三种挂载方式怎么选（bind / volume / tmpfs）

- **篇幅**：400-600 字（短）
- **要点**：bind mount 定义与适用场景（共享宿主源码/构建产物、持久化到宿主、共享宿主配置文件）；named volume 的生命周期、预填充、匿名卷；tmpfs 内存盘（临时/敏感数据）；一张选型判断表收尾（需容器直读写宿主路径 → bind；仅容器间/持久化 → volume；临时敏感 → tmpfs）
- **素材**：S1「bind mount 定义与风险」、S2「volume 选型/生命周期/预填充/匿名卷」、S10「tmpfs」
- **代码示例**：无（本章为概念与判据，不放长命令）
- **覆盖坑**：bind 默认可写，容器进程可改删宿主机文件；bind 挂到容器非空目录会遮蔽原文件且不易解除；需要从宿主直接访问文件时应改用 bind，而非 volume

### 第 2 章：命令行挂载：`docker run -v` 与 `--mount`

- **篇幅**：600-800 字（中）
- **要点**：`-v` 三字段 `host:cont[:opts]` 固定顺序；`--mount` 逗号分隔 key=value、顺序无关；只读 `ro`/`readonly`；`bind-propagation` 与 `bind-create-src`；官方推荐 `--mount`（更显式、支持全部选项）
- **素材**：S1「options-for---mount」「use-the-v-flag」「bind-propagation」
- **代码示例**：有（`docker run -v` 与 `--mount` 各 2-3 条，含 `ro` 变体）
- **覆盖坑**：`-v` 源路径不存在时自动建目录，`--mount` 默认报错需 `bind-create-src`；`dst` 必须绝对路径；bind 绑定的是 daemon 所在主机，远程 daemon 无法 bind 客户端路径；bind-propagation 仅 Linux 且 Docker Desktop 不支持

### 第 3 章：Compose 挂载：`volumes` 长短语法与顶层声明

- **篇幅**：600-800 字（中）
- **要点**：短语法 `VOLUME:CONTAINER_PATH[:ACCESS_MODE]`（`rw`/`ro`/`z`/`Z`）；长语法 `type/source/target/read_only` 及 bind（`propagation`/`create_host_path`/`selinux`）、volume（`nocopy`/`subpath`）、tmpfs（`size`/`mode`）子项；顶层 `volumes:` 声明与 `external: true` 复用；关联字段 `user`、`read_only`、`volumes_from`
- **素材**：S4「volumes 长短语法」「顶层 volumes」「user/read_only 字段」
- **代码示例**：有（compose yaml 片段：短语法、长语法、顶层命名卷）
- **覆盖坑**：相对宿主路径必须以 `./` 或 `../` 开头，否则被当成命名卷；bind 短语法在源路径不存在时自动创建目录，可用长语法 `create_host_path: false` 阻止；`:z/:Z` 在服务/Compose 中会被忽略，需要 SELinux 标签时用长语法 `selinux:` 字段

### 第 4 章：权限与属主：permission denied 的根因与修复

- **篇幅**：800-1000 字（长，核心章节）
- **要点**：Docker 不映射 UID——容器内 UID 1000 即宿主 UID 1000，文件系统只认数字 UID；多数容器默认以 root 运行；修复三招：`sudo chown -R 1000:1000`、compose 设 `user: "1000:1000"`（依赖镜像支持）、linuxserver 用 `PUID/PGID` 环境变量；权限三步排查（`docker exec id` → `docker inspect <img> --format '{{.Config.User}}'` → 对齐宿主目录属主）；userns-remap 与 rootless 的映射规则
- **素材**：S5「根因与修复方案」、S6「PUID/PGID 及与 --user 的兼容性」、S3「userns-remap 原理/配置/限制」、S4「user 字段」
- **代码示例**：有（`docker exec <c> id`、`docker inspect` 查默认 User、`chown -R`、compose `user:`、linuxserver `-e PUID/PGID`）
- **覆盖坑**：permission denied 根因是容器用户与目录属主 UID 不一致；root 写 bind 目录导致宿主文件全部归 root；linuxserver 镜像与 `--user` 不兼容、官方只推荐 PUID/PGID；`user:` 并非所有镜像支持（有的初始化需 root）；userns-remap 与 `--pid=host`/`--network=host`/`--privileged`/部分存储驱动不兼容；命名卷换用不同 UID 镜像时旧属主残留

### 第 5 章：安全边界：只读、SELinux 与 docker.sock 风险

- **篇幅**：600-800 字（中）
- **要点**：默认 root + bind 默认可写 = 容器被攻破即控宿主挂载文件；只读挂载 `ro` 作为默认底线；SELinux `:z`（共享标签）与 `:Z`（私有标签）；docker.sock 挂载 = root 的信任模型（daemon 不重新认证客户端）；只读挂载 socket 仍危险；缓解方案：外部认证网关 docker-socket-proxy、TLS 双向认证（2376）、SSH context；不把 `/`、`/etc`、`/root` bind 进容器
- **素材**：S9「socket 攻击机制与审计清单」、S7「TLS/SSH 保护」、S8「docker-socket-proxy 白名单」、S1/S4「SELinux z/Z」
- **代码示例**：有（`-v /var/run/docker.sock:/var/run/docker.sock` 示例、docker-socket-proxy 启动命令、TLS 双向认证与 `docker context create ssh://` 命令、私钥 `chmod 0400`）
- **覆盖坑**：任何能写 socket 的进程都能以 root 执行任意 API 命令；只读挂载 socket 不降低 API 风险；`:Z` 重打标签可能使宿主目录不可用；2375 无 TLS 等于远程 root；socket 挂载安全评审不应按低风险对待

### 第 6 章：Docker Desktop 的差异：macOS/Windows 挂载性能

- **篇幅**：400-600 字（短）
- **要点**：性能根因（Linux 容器跑在 VM 内，宿主文件系统需虚拟文件系统桥接，大量小文件时性能骤降）；macOS 后端对比：VirtioFS（4.22+ 默认，最快）、gRPC-FUSE（旧默认）、osxfs（legacy）；Windows WSL2 走 9P 协议；Synchronized file shares（Mutagen，Pro/Team/Business 4.27+）；社区规避技巧
- **素材**：S10「Docker Desktop 文件共享后端与同步文件共享」
- **代码示例**：无（可含一行一致性 flag 示意 `:consistent`/`:cached`/`:delegated`）
- **覆盖坑**：大量小文件跨 VM 边界性能骤降；`node_modules`/`.git` 用命名卷隔离；macOS 只共享最小目录（/Users、/Volumes 等）；WSL2 下代码放 WSL 文件系统内性能最好，从 Windows 文件系统 bind 会跨 9P 变慢

### 第 7 章：实战案例：Web 服务读写宿主目录的完整配置

- **篇幅**：600-800 字（中）
- **要点**：综合场景走查（如 Nginx/Node 容器只读挂载宿主配置目录、可写挂载宿主日志目录）；完整 `docker run` 与 compose 配置二选一；套用权限三步排查；套用安全底线四原则（默认只读、不挂 socket、不挂系统目录、非 root 用户）；最终坑位检查清单
- **素材**：S1-S10 汇总（对接 02_deep_research.md「实战指引」骨架）
- **代码示例**：有（完整 `docker run --mount` 与 compose yaml 组合示例 + 验证/排查命令）
- **覆盖坑**：汇总全章坑位：permission denied、root 属主错乱、bind 遮蔽非空目录、`:Z` 改宿主标签、socket=root、`-v` 自动建目录 vs `--mount` 报错、Docker Desktop 性能

## 学习路径说明

### 前置要求

- 已安装 Docker Engine 或 Docker Desktop，能运行 `docker run` 基础命令
- 了解 docker compose 的基本结构（services、image、ports）
- 了解 Linux 文件权限基本概念（rwx、UID/GID、chown/chmod）

### 学完能做什么

- 判断自己的场景该用 bind mount、named volume 还是 tmpfs
- 写出正确的 `docker run -v` / `--mount` 与 compose `volumes:` 挂载配置
- 独立排查并修复容器内外文件的权限/属主问题（permission denied、root 属主错乱）
- 识别 docker.sock 与 bind 可写带来的安全风险，并采取只读、代理、最小权限等缓解
- 针对 Docker Desktop（macOS/Windows）选择后端与规避性能坑

### 建议学习顺序

- 第 1-3 章按顺序阅读：选型 → CLI 命令 → Compose 写法，建立命令基础
- 第 4 章（权限）为重中之重，建议多花时间动手验证
- 第 5-6 章为安全边界与平台差异，可按需跳读
- 第 7 章作为综合练习收尾，对照检查清单自测

> 待确认项：用户实际运行的镜像/服务未定，第 4 章 `user:`/PUID/PGID 的具体写法需在写作时确认；若涉及强制 SELinux/AppArmor 环境，第 5 章需补充 AppArmor profile 细节。
