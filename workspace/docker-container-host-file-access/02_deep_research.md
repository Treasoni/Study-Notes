# 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件 - 深度素材

- **阶段**: P2 深度收集
- **日期**: 2026-08-29
- **方向**: A 综合实战主线（挂载 → 权限 → 安全）
- **核心源**: 9 条（官方 Tier 1 × 6，Tier 2 × 3）+ WebSearch 补充 Docker Desktop 细节 1 组

---

## 来源表

| ID | 来源 | URL | Tier | 提供内容 |
|----|------|-----|------|---------|
| S1 | Docker bind mounts 官方 | https://docs.docker.com/engine/storage/bind-mounts/ | 1 | bind 挂载定义、`-v`/`--mount` 写法、ro、bind-propagation |
| S2 | Docker volumes 官方 | https://docs.docker.com/engine/storage/volumes/ | 1 | 命名卷/匿名卷、生命周期、预填充、volume 管理命令 |
| S3 | userns-remap 官方 | https://docs.docker.com/engine/security/userns-remap/ | 1 | 用户命名空间重映射原理、配置、限制 |
| S4 | Compose services 参考 | https://docs.docker.com/reference/compose-file/services/ | 1 | compose volumes 长短语法、`user`、`read_only`、`volumes_from` |
| S5 | Docker Volume Permissions Explained | https://selfhosting.sh/foundations/docker-volume-permissions/ | 2 | 权限问题根因与修复（chown、user:、PUID/PGID、命名卷） |
| S6 | linuxserver.io PUID/PGID | https://docs.linuxserver.io/general/understanding-puid-and-pgid/ | 2 | PUID/PGID 环境变量模式及与 --user 的兼容性说明 |
| S7 | Protect the Docker daemon socket 官方 | https://docs.docker.com/engine/security/protect-access/ | 1 | docker.sock 访问=root；SSH/TLS 双向认证保护方案 |
| S8 | docker-socket-proxy | https://github.com/Tecnativa/docker-socket-proxy | 2 | HAProxy 白名单过滤 Docker API 的替代方案 |
| S9 | Docker socket security | https://www.netdata.cloud/guides/docker/docker-socket-security/ | 2 | socket 挂载攻击机制、审计与缓解清单 |
| S10 | Docker Desktop 文件共享（官方博客/文档 + WebSearch） | https://docs.docker.com/desktop/features/synchronized-file-sharing/ | 1 | macOS/Windows 文件共享后端（VirtioFS/gRPC-FUSE/osxfs）、性能与同步文件共享 |

> ⚠️ 抓取失败的源：`docs.docker.com/desktop/features/filesharing/`（404），已由 S10 替代。

---

## 声明/来源映射（按主题）

### 主题 1：挂载选型（bind / volume / tmpfs）

- **[S1] bind mount 定义**：把宿主机文件或目录直接挂进容器；与 volume 不同，volume 位于 Docker 管理目录内。适用：共享宿主源码/构建产物、把容器生成文件持久化到宿主、共享宿主配置文件（如 `/etc/resolv.conf`）。
- **[S1] bind 风险**：容器进程可写宿主机文件、可改删宿主系统文件、影响非 Docker 进程 → 默认可写，可用 `readonly`/`ro` 防写。
- **[S2] volume 选型**：容器数据持久化首选（易备份/迁移、CLI/API 管理、跨 Linux/Windows 容器、多容器共享、可预填充、高性能 I/O）；**需从宿主直接访问文件时应改用 bind**。
- **[S1] 挂到非空目录会遮蔽**：bind 挂到容器非空目录会遮蔽原文件，容器内不便解除，最佳做法是重建容器。
- **[S2] 卷生命周期**：卷独立于容器，删容器不删卷；无引用时保留，用 `docker volume prune` 清理。空卷挂到含文件目录时默认把容器原内容复制进卷（预填充），可用 `volume-nocopy` 禁用。
- **[S2] 匿名卷**：随机唯一名、可持久，但 `--rm` 启动时随容器销毁；不自动共享。
- **[S1] 远程 daemon 注意**：bind 绑定的是 daemon 所在主机；远程 daemon 无法 bind 客户端路径。Docker Desktop 的 daemon 跑在 Linux VM 内，由内建机制透明处理。
- **[S10] tmpfs**（P1 候选补充）：内存盘，`--tmpfs` 或 `--mount type=tmpfs`，仅存内存、容器停止即丢失、仅 Linux，适合临时/敏感数据。

### 主题 2：命令写法（CLI 与 Compose）

- **[S1] `--mount` vs `-v`**：官方推荐 `--mount`（更显式、支持全部选项）。`-v` 源路径不存在时**自动建目录**；`--mount` 默认报错，需 `bind-create-src`。
- **[S1] `--mount` 语法**：逗号分隔 key=value、顺序无关；`src` 可绝对/相对、`dst` 必须绝对；选项含 `readonly`/`ro`、`bind-propagation`、`bind-create-src`。
- **[S1] `-v` 语法**：冒号分隔三字段 `host:cont[:opts]`，顺序固定；bind 有效选项：`ro`、SELinux `z`/`Z`、bind propagation（默认 `rprivate`）。
- **[S4] Compose 短语法**：`VOLUME:CONTAINER_PATH[:ACCESS_MODE]`；`ACCESS_MODE` 逗号列表：`rw`（默认）、`ro`、`z`、`Z`。
- **[S4] Compose 长语法**：字段 `type/source/target/read_only`；bind 子项 `propagation/create_host_path/selinux`；volume 子项 `nocopy/subpath`；tmpfs 子项 `size/mode`。
- **[S4] Compose 注意**：bind 短语法在宿主源路径不存在时自动创建目录（兼容 legacy compose），可用长语法 `create_host_path: false` 阻止；相对宿主路径须以 `./` 或 `../` 开头（否则视为命名卷）。
- **[S4] 顶层 volumes**：单服务宿主路径可写在服务内；跨服务复用须在顶层 `volumes:` 声明命名卷，`external: true` 引用已有卷。
- **[S1] bind-propagation**：默认 `rprivate`，仅 bind 可配、仅 Linux，Docker Desktop 不支持；递归只读子挂载需内核 ≥ 5.12。

### 主题 3：权限与属主（核心坑）

- **[S5] 根因**：Docker 不映射 UID——容器内 UID 1000 即宿主 UID 1000，文件系统只认数字 UID 不认用户名；容器进程用户与挂载目录属主不同 → `Permission denied`。
- **[S5] 默认 root**：多数容器默认以 root(UID 0) 运行，安全镜像以非 root 运行；以 root 写 bind 目录 → 宿主文件全部归 root。
- **[S6] PUID/PGID**：linuxserver 镜像用 `-e PUID=1000 -e PGID=1000`（取 `id $user` 的 uid/gid），entrypoint 启动时自动改文件属主；linuxserver 镜像与 `--user` flag **不兼容**，官方推荐继续用 PUID/PGID。
- **[S5] 修复方案**：
  - Fix 1：`sudo chown -R 1000:1000` 把宿主目录属主改成容器 UID/GID（最常用可靠）。
  - Fix 2：compose 设 `user: "1000:1000"`；**并非所有镜像支持任意用户**，有的初始化需 root。
  - Fix 3：linuxserver 用 PUID/PGID。
- **[S5] 命名卷权限较少出错**：由 Docker 按镜像文件系统初始化正确属主；换用不同 UID 镜像时旧卷保留旧属主 → 需注意。
- **[S5] rootless 映射**：rootless Docker 用 userns 重映射（容器 UID 0→宿主 100000、1000→101000）；**bind 宿主目录必须属主为对应重映射 UID**。
- **[S3] userns-remap**：把容器内 root 映射为宿主无特权高位 UID；由 `/etc/subuid` 与 `/etc/subgid` 管理（格式 `testuser:231072:65536`）。配置写 `default` 自动创建 dockremap 用户。启用后旧镜像被掩蔽、数据迁至 `/var/lib/docker/{UID}.{GID}/`，**建议新装时启用**。
- **[S3] userns-remap 限制**：与 `--pid=host`、`--network=host`、不支持 userns 的卷/存储驱动、`--privileged` 不兼容；容器内 root 不能用 mknod；单容器可用 `--userns=host` 关闭。
- **[S4] compose `user`**：覆盖容器进程运行用户；默认取镜像设置（如 Dockerfile `USER`），未设置则为 root。

### 主题 4：安全边界

- **[S9] socket 挂载 = root**：`dockerd` 以 root 运行并监听 `/var/run/docker.sock`（默认 `root:docker` 0660）；任何能写入该 socket 的进程都能让 daemon 以 root 执行任意 API 命令，**daemon 不重新认证客户端**。攻击路径：写 socket → 创建 privileged 容器 → 宿主 root。**这不是 Docker 漏洞，是设计信任模型**。
- **[S9] 只读挂载 socket 仍危险**：只读减少文件系统级风险但 API 不变，仍可查询状态、inspect 其他容器、横向移动。安全评审不应把 `ro` socket 挂载当低风险。
- **[S9] 缓解建议**：不要向应用容器挂原始 socket；改用外部认证网关（如 docker-socket-proxy）；必须挂载时以最小权限用户运行、drop capabilities，并按"直接在宿主以 root 运行"对待。禁用未认证 TCP（2375 无 TLS = 远程 root）；远程访问用 TLS 双向认证（2376）或 SSH。
- **[S7] TLS 双向认证**：`--tlsverify --tlscacert --tlscert --tlskey -H=0.0.0.0:2376`；OpenSSL 生成 CA/服务器/客户端证书（服务器 CN 匹配主机名，SAN 含连接 IP）；证书/密钥须按 root 密码保管，私钥 `chmod 0400`。
- **[S7] SSH 访问**：`docker context create --docker host=ssh://user@host` 或 `DOCKER_HOST=ssh://user@host`。
- **[S8] docker-socket-proxy**：HAProxy 白名单过滤 Docker API（环境变量 0/1 控制各 API 段），危险请求返回 403；`-p 127.0.0.1:2375:2375` 绑定本机，`--privileged` 用于连接 socket；默认只开 EVENTS/PING/VERSION，安全关键段默认关闭。
- **[S1/S4] SELinux/AppArmor**：bind 支持 `:z`（共享标签）/`:Z`（私有标签）；**`:Z` 重打标签可能使宿主目录不可用**；`-v` 短语法支持 `z/Z`，但 `:z/:Z` 与 `:ro` 在**服务/Compose 中会被忽略**；AppArmor 用 `--security-opt apparmor=xxx` 收窄边界（S1 未详述，P1 候选 AppArmor 官方页补充）。
- **[S1] 未设 user + bind 可写 = 提权风险**：默认 root（S4）∩ bind 默认可写（S1）→ 容器被攻破即控宿主机挂载文件。

### 主题 5：Docker Desktop（macOS/Windows）

- **[S10] 性能根因**：Docker Desktop 的 Linux 容器跑在 VM 内，宿主文件系统（APFS/NTFS）需虚拟文件系统桥接，每次文件操作跨 VM 边界 → 大量小文件时性能骤降（原生 Linux 无此开销）。
- **[S10] macOS 后端**：VirtioFS（最快，Docker Desktop 4.22+ 默认，2–5x 优于 gRPC-FUSE）、gRPC FUSE（旧默认）、osxfs（legacy 最慢）。
- **[S10] Windows**：WSL2 后端走 9P 协议，无后端切换；代码放 WSL 文件系统内性能最好，从 Windows 文件系统 bind 会跨 9P 边界变慢。
- **[S10] 官方推荐**：Synchronized file shares（集成 Mutagen，Pro/Team/Business 订阅，4.27+），在 VM 内建 ext4 同步缓存，宣称 2–10x 提速；`.syncignore` 排除 node_modules/.git；不适用于 WSL/Windows 容器/K8s hostPath。
- **[S10] 社区规避技巧**：项目 bind 挂载 + `node_modules` 用命名卷隔离；macOS 只共享最小目录（默认 /Users、/Volumes、/private、/tmp、/var/folders）；一致性 flag `:consistent`/`:cached`/`:delegated`。

---

## 矛盾点与注意事项

| 矛盾 | 处理 |
|------|------|
| linuxserver.io：其镜像与 `--user` **不兼容**，只能用 PUID/PGID；selfhosting.sh 把 `user: "1000:1000"` 列为通用修复 | `user:` 方案**依赖镜像支持**，非普适；实战需先查镜像文档/`docker inspect` 镜像默认 User |
| Docker 官方：userns-remap 下 daemon 仍以 root 运行；rootless 才是 daemon 与容器都非 root | 两者映射起点与适用场景不同：userns-remap 保护容器→宿主；rootless 保护宿主 daemon |
| Docker 官方推荐 volume 做持久化，但用户场景是「容器控制宿主机文件」 | 该场景下 bind mount 是主线，volume 仅作为补充（性能/权限更稳），需在笔记中明确选型判据 |
| `:z/:Z` 在 Compose/服务中会被忽略 | 需要 SELinux 标签时优先在 compose 长语法用 `selinux:` 字段或明确文档说明 |

---

## 实战指引（给下游章节的骨架）

1. **选型判断**：需要容器直接读写宿主机路径 → bind mount；仅需容器间/持久化 → named volume；临时敏感 → tmpfs。
2. **最小可运行命令**：
   ```bash
   docker run --mount type=bind,src="$(pwd)"/data,dst=/app/data,ro image
   docker run -v /host/path:/container/path:ro image
   ```
3. **权限三步排查**：`docker exec <c> id` → `docker inspect <img> --format '{{.Config.User}}'` → 对齐宿主目录属主（chown 或 --user 或 PUID/PGID）。
4. **安全底线**：默认只读挂载；不挂 docker.sock 除非明确需要并加代理/最小权限；不把 `/`、`/etc`、`/root` bind 进容器；`user:` 尽量用非 root。

---

## 开放问题（P3 大纲/写作时注意）

- 用户具体跑的是哪个镜像/服务？（不同镜像的 user:/PUID/PGID 支持不同）
- 是否涉及 Docker Desktop（macOS/Windows）？→ 需要纳入 S10 性能与共享配置小节
- 是否需要「容器内服务主动触发宿主命令」的场景（SSH/API 网关）？P1 标记为边界场景，P2 未深入
- 是否用到 SELinux/AppArmor 强制环境？→ 决定是否展开 `z/Z` 与 AppArmor profile

---

## 下游交接摘要

- **给 outline-generator**：建议按「选型 → 命令 → 权限 → 安全 → 平台差异 → 实战案例」组织；每章可引用 S1-S10 的具体小节（如 S1「options-for---mount」）。
- **素材质量**：核心概念全部有官方 Tier 1 支撑；权限实战有 Tier 2 落地细节；Docker Desktop 有官方发布信息。可支撑一份「上手/实战」级完整笔记。
- **主要坑位清单**（写作时必覆盖）：permission denied、root 属主错乱、bind 遮蔽非空目录、`:Z` 改宿主标签、socket=root、`-v` 自动建目录 vs `--mount` 报错、Docker Desktop 性能。
