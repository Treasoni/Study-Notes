---
title: Docker容器服务访问宿主机文件
tags:
  - Docker
  - 容器
  - 挂载
  - 权限
  - 安全
  - 实战笔记
created: 2026-08-29
updated: 2026-08-29
status: 已完成
source_project: docker-container-host-file-access
---

# 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件

> [!summary] 本笔记解决什么问题
> 如何让 Docker 容器内部的服务控制/处理容器外或宿主机的文件。核心思路：先选挂载方式（bind mount / named volume / tmpfs），再掌握命令行与 Compose 的挂载写法，接着解决容器内外文件的权限与属主问题，明确 docker.sock 与可写挂载的安全边界，最后结合 Docker Desktop 在 macOS/Windows 上的平台差异，走查一个 Web 服务读写宿主目录的完整实战案例。全篇共 7 章，按顺序阅读即可。

## 目录

1. [[#第 1 章：三种挂载方式怎么选（bind / volume / tmpfs）|第 1 章：三种挂载方式怎么选]]
2. [[#第 2 章：命令行挂载：docker run -v 与 --mount|第 2 章：命令行挂载]]
3. [[#第 3 章：Compose 挂载：volumes 长短语法与顶层声明|第 3 章：Compose 挂载]]
4. [[#第 4 章：权限与属主：permission denied 的根因与修复|第 4 章：权限与属主]]
5. [[#第 5 章：安全边界：只读、SELinux 与 docker.sock 风险|第 5 章：安全边界]]
6. [[#第 6 章：Docker Desktop 的差异：macOS/Windows 挂载性能|第 6 章：Docker Desktop 差异]]
7. [[#第 7 章：实战案例：Web 服务读写宿主目录的完整配置|第 7 章：实战案例]]

---

## 第 1 章：三种挂载方式怎么选（bind / volume / tmpfs）

容器里的服务要读写宿主机文件，第一步不是"怎么挂"，而是"用哪种方式挂"。Docker 提供三种挂载：bind mount、named volume、tmpfs，选错后面权限、安全、性能全都会踩坑。

### bind mount：把宿主目录直接接进容器

> [!tip] 大白话
> 把 bind mount 想成"把家里的文件柜直接搬到办公室"——容器里看到的目录和宿主是同一个柜子，改一处两边都变。所以它适合容器需要直读写宿主路径的场景。

**bind mount** 把宿主机的文件或目录直接挂进容器，两边看到的是同一份数据 [S1]。典型用途：共享宿主源码/构建产物、把容器生成的文件持久化到宿主、共享宿主配置文件（如 `/etc/resolv.conf`）[S1]。注意两个坑：默认可写，容器进程能改删宿主文件（可用只读挂载防写）；挂到容器非空目录会遮蔽原文件，容器内不便解除，最佳做法是重建容器 [S1]。

### named volume：让 Docker 帮你管数据

> [!tip] 大白话
> 把 named volume 想成"Docker 仓库里有名字的储物格"，你不直接进仓库翻，而是让 Docker 按名字取放。它适合"数据归 Docker 管"的持久化场景。

**named volume** 由 Docker 管理，位于 Docker 数据目录内，是容器持久化的首选：易备份迁移、可 CLI/API 管理、可多容器共享 [S1][S2]。生命周期上，卷独立于容器：删容器不删卷，无引用时保留，用 `docker volume prune` 清理 [S2]；空卷挂到含文件目录时，会把容器原内容预填充进卷（可用 `nocopy` 禁用）[S2]。此外还有**匿名卷**：随机唯一名、可持久，但 `--rm` 启动时随容器销毁、不自动共享 [S2]。**需要从宿主直接访问文件时，应改用 bind 而非 volume** [S2]。

### tmpfs：只活在内存里的临时盘

> [!tip] 大白话
> 把 tmpfs 想成"一次性便签纸"，写完用完就扔，不占抽屉也不留痕迹。所以它只适合临时或敏感数据。

**tmpfs** 是内存盘，数据只存在容器内存，停止即丢失，仅 Linux 支持 [S10]。适合临时文件或不想落盘的敏感数据 [S10]。

### 选型判断表

| 你的需求 | 选择 | 一句话理由 |
|---------|------|-----------|
| 容器要直读写宿主路径（源码/配置/日志） | bind mount | 宿主与容器同一份数据 [S1] |
| 仅容器间共享、数据要持久化 | named volume | Docker 托管，易备份迁移 [S2] |
| 临时/敏感数据，不想落盘 | tmpfs | 内存盘，停止即丢 [S10] |

### 本章小结

- bind mount 让容器直读宿主路径，但默认可写、挂非空目录会遮蔽原文件 [S1]
- named volume 归 Docker 管，删容器不删卷，可预填充，适合持久化 [S2]
- tmpfs 只在内存，容器停止即失，适合临时/敏感数据 [S10]
- 需要从宿主直接访问文件时，选 bind 而非 volume [S2]

下一章我们把选择落到命令上：`docker run -v` 与 `--mount` 的写法差异和易错点。

---

## 第 2 章：命令行挂载：docker run -v 与 --mount

上一章定了选型判据：容器要直接读写宿主机路径，就走 bind mount。本章落地到命令行，讲 `docker run` 的两种写法——简写 `-v` 和显式 `--mount`，以及它们的关键差异。读完你能写出带只读、自动建目录等选项的正确挂载命令，也知道官方明确警告过的坑。

### 2.1 `-v`：冒号分隔、顺序固定

`-v` 是简写，语法是冒号隔开的三段、顺序固定：`host:cont[:opts]`——宿主路径、容器路径、可选项 [S1]。顺序不能换，但可选项可以省略。

```bash
# 把当前目录下的 data 挂到容器 /app/data，默认可写
docker run -v "$(pwd)/data":/app/data alpine ls /app/data
# 输出 /app/data 下的文件列表（目录为空则无输出）
```

`opts` 常见值：`ro`（只读）、`z`/`Z`（SELinux 标签，第 5 章细讲）、bind propagation。只读示例：

```bash
# 宿主配置目录只读挂入，容器内只能读
docker run -v "$(pwd)/config":/app/config:ro nginx
```

### 2.2 `--mount`：key=value、顺序无关

`--mount` 用逗号分隔的 key=value 键值对，**顺序无关**，且必须显式声明 `type`。bind 类型用 `src`/`dst`（也可写 `source`/`target`）[S1]。

```bash
# 与上面 -v 等价：type=bind + src 宿主路径 + dst 容器路径
docker run --mount type=bind,src="$(pwd)/data",dst=/app/data alpine ls /app/data
# 输出与 -v 示例一致

# 只读 + 源目录不存在时自动创建
docker run --mount type=bind,src="$(pwd)/logs",dst=/app/logs,readonly,bind-create-src=true alpine ls /app/logs
```

> [!tip] 大白话
> 把 `-v` 想成发固定格式短信——`收件人:内容:备注`，顺序不能乱；把 `--mount` 想成填带标签的表格——`姓名=张三`，先填哪格都行。所以字段一多，`--mount` 更不容易写错，这也是官方推荐它的原因。

### 2.3 官方推荐与四个必记的坑

官方文档明确推荐 `--mount`：它更显式、支持全部选项（如 `bind-create-src`、`bind-propagation`），`-v` 只覆盖常用子集。简单场景用 `-v` 没问题，复杂场景优先 `--mount` [S1]。

1. **自动建目录的差异**：`-v` 的源路径不存在时会**自动当成目录创建**；`--mount` **默认报错**，要显式加 `bind-create-src=true` 才创建 [S1]。
2. **`dst` 必须是绝对路径**：容器侧目标路径不写绝对路径会直接报错；`src` 才允许相对路径 [S1]。
3. **bind 绑定的是 daemon 所在主机**：`docker run` 是本地命令，真正挂载动作由 daemon 执行。用远程 daemon（如 `DOCKER_HOST=ssh://...`）时，`src` 解析的是**远程主机**路径，不是你的客户端路径 [S1]。
4. **`bind-propagation` 仅 Linux**：它控制子挂载点的联动，默认 `rprivate`，仅 bind 可配、仅 Linux 生效，Docker Desktop（macOS/Windows）不支持 [S1]。

> [!tip] 大白话
> 把 `ro` 想成图书馆样本书——只能看不能改。挂载加 `ro` 后，容器进程改不了宿主文件，是对第 1 章"bind 默认可写"风险最直接的缓解。

### 本章小结

- 命令行 bind 挂载有两种写法：`-v host:cont[:opts]`（顺序固定）与 `--mount type=bind,...`（key=value 顺序无关）[S1]。
- 官方推荐 `--mount`，更显式、支持全部选项；`-v` 适合简单场景 [S1]。
- 只读挂载：`-v ...:ro` 或 `--mount ...,readonly`。
- 四个坑：`-v` 自动建目录 vs `--mount` 默认报错；`dst` 必须绝对；远程 daemon 绑远程路径；`bind-propagation` 仅 Linux、Docker Desktop 不支持 [S1]。
- 更多 docker run / docker compose 常用命令可查 [[Docker与DockerCompose命令速查]]。

下一章进入 Compose：同样的挂载用 `volumes:` 怎么写，长短语法与顶层声明又对应哪些坑。

---

## 第 3 章：Compose 挂载：volumes 长短语法与顶层声明

第 2 章的命令行挂载适合临时验证；项目一旦固定下来，配置几乎都会写进 `docker-compose.yml`。本章讲 compose 里 `volumes:` 的短语法、长语法、顶层命名卷声明，以及三个高频坑。

### 3.1 短语法：一行搞定

短语法沿用 `docker run -v` 的三段式，格式 `VOLUME:CONTAINER_PATH[:ACCESS_MODE]`：

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html:ro   # 相对宿主路径，必须 ./ 开头
      - app-data:/var/lib/data            # 不带路径 = 命名卷
```

`ACCESS_MODE` 是逗号分隔的选项列表：`rw`（默认）、`ro`（只读）、`z`、`Z`（SELinux）[S4]。适合一眼看懂的简单场景。

> [!tip] 大白话
> 把 `./html:/usr/share/nginx/html:ro` 想成一张「访客证」：左边是你宿主机上的工位，右边是访客能进的门，`ro` 就是「只能参观、不许动手」。宿主改文件，容器立刻看到；容器想写回去？门禁卡没这个权限。

### 3.2 长语法：把每个挂载展开成 map

要精确控制，用长语法。核心字段 `type/source/target/read_only`，再加类型专属子项 [S4]：

```yaml
services:
  web:
    image: nginx
    volumes:
      - type: bind
        source: ./html
        target: /usr/share/nginx/html
        read_only: true
        bind:
          create_host_path: false   # 宿主目录不存在时报错，不自动建
      - type: volume
        source: app-data
        target: /var/lib/data
        volume:
          nocopy: true              # 关闭空卷预填充
      - type: tmpfs
        target: /tmp/cache
        tmpfs:
          size: 10485760            # 10 MB 内存盘
```

- bind 子项：`propagation`、`create_host_path`、`selinux`（`z`/`Z` 标签）
- volume 子项：`nocopy`、`subpath`（只挂卷内子目录）
- tmpfs 子项：`size`、`mode` [S4]

### 3.3 顶层 `volumes:` 与 `external: true`

命名卷只给一个服务用时写在服务内即可；跨服务复用或复用已有卷，要在顶层声明 [S4]：

```yaml
services:
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
    external: true   # 引用已存在的卷，不新建
```

### 3.4 关联字段：`user` / `read_only` / `volumes_from`

- `user: "1000:1000"`：覆盖容器进程运行用户（默认取镜像 `USER`，未设则 root）[S4]
- `read_only: true`：整个容器根文件系统只读，卷可单独开写
- `volumes_from`：继承其他服务的挂载 [S4]

这三个字段第 4 章会结合权限细讲，这里先认识它们与 `volumes` 配套。

### 3.5 三个坑

1. **相对宿主路径必须以 `./` 或 `../` 开头**，否则 compose 把 `foo` 当命名卷而非目录 [S4]
2. **短语法会自动创建不存在的宿主目录**；想严格把关用长语法 `create_host_path: false` [S4]
3. **`:z/:Z` 在 compose 中会被忽略**，要打 SELinux 标签就用长语法 `selinux:` 字段 [S1][S4]

> [!tip] 大白话
> 第 3 个坑很像「装修被叫停」：短语法里的 `:z` 像口头承诺，compose 直接当没听见；长语法 `selinux:` 字段才是白纸黑字的施工许可。

### 本章小结

- 短语法三段式适合简单场景，`ACCESS_MODE` 支持 `rw/ro/z/Z`
- 长语法用 `type/source/target/read_only` 显式声明，bind/volume/tmpfs 各有子项
- 跨服务复用或引用已有卷时用顶层 `volumes:` + `external: true`
- `user`、`read_only`、`volumes_from` 与挂载配套使用
- 相对路径不加 `./` 会被当命名卷；`create_host_path: false` 阻止自动建目录

下一章进入权限篇：为什么容器一写宿主目录就 `permission denied`，UID/GID 到底怎么对得上。

---

## 第 4 章：权限与属主：permission denied 的根因与修复

上一章我们把宿主机目录挂进了容器，但"挂载成功"不等于"能读写"。最常见的现象是：容器正常启动，一读写挂载目录就报 `Permission denied`。这一章只解决一个问题——搞清楚文件属主在容器和宿主机之间到底怎么对账，然后给出三招修复手段。

### 根因：Docker 不映射 UID

Docker 有一个反直觉的设计：**它不做 UID 映射**。容器里的 UID 1000 就是宿主机的 UID 1000，文件系统只认数字 UID，不认用户名 [S5]。UID/GID 的底层原理可参考 [[docker里的GID和UID]]。所以"容器内明明是 www-data 用户，为什么打不开宿主 /data 目录"这类问题，本质是：**容器进程的用户（一个数字 UID）和挂载目录的属主（另一个数字 UID）对不上**。

> [!tip] 大白话
> 把 UID 想成数字工号。宿主机这个"文件柜管理员"只认工号不认名字。容器进程拿着工号 33，宿主机目录的锁上写的是工号 1000，自然开不了门。所以"改名字没用，得让工号对上"。

多数容器**默认以 root（UID 0）运行**，只有安全镜像才主动切到非 root 用户 [S5]。如果你以 root 写 bind 目录，宿主机上被写入的文件属主全会变成 root，之后其他程序再想读写就抓瞎了。

### 权限三步排查

遇到 `Permission denied`，按下面三步定位，别瞎试：

```bash
# ① 看容器里进程实际以什么用户跑
docker exec <容器名> id
# 输出示例：uid=999(postgres) gid=999(postgres) groups=999(postgres)

# ② 看镜像默认的 User（来自 Dockerfile USER；没设置就是 root）
docker inspect <镜像名> --format '{{.Config.User}}'

# ③ 看宿主挂载目录当前的数字属主
ls -ln /宿主机/挂载目录
```

> [!tip] 大白话
> 第一步是问"我（容器）拿的是几号工牌"，第二步是问"这面墙（镜像）出厂时默认给谁发工牌"，第三步是"看文件柜锁上是几号"。三步对到同一个数字，权限问题就消失。

### 修复三招（按场景选）

**Fix 1：改宿主目录属主**——最常用、最可靠 [S5]。

```bash
# 把宿主目录属主改成容器用户的 UID/GID（这里以 UID 1000 为例）
sudo chown -R 1000:1000 /宿主机/挂载目录
```

**Fix 2：compose 里指定 `user:`**——覆盖容器进程用户 [S4]，但**并非所有镜像都支持任意用户**，有些镜像初始化阶段必须用 root [S5]。

```yaml
services:
  app:
    image: example/app
    user: "1000:1000"        # 覆盖容器进程的 UID:GID
    volumes:
      - ./data:/app/data
```

**Fix 3：linuxserver 系镜像用 `PUID/PGID`**——特例。linuxserver 镜像与 `--user`/`user:` **不兼容**，官方只推荐通过环境变量传 PUID/PGID，entrypoint 启动时自动把文件属主改成你指定的值 [S6]。

```bash
docker run -d \
  -e PUID=1000 -e PGID=1000 \
  -v "$(pwd)"/data:/config \
  linuxserver/镜像名
```

> [!tip] 大白话
> Fix 2 是"让容器换个工牌进厂"，但有的工厂（镜像）规定进场必须用老板工牌；Fix 3 是 linuxserver 家的特殊门禁卡——你在门口报个号，保安（entrypoint）自动把对应工牌挂你脖子上。

具体选哪个，先查你的镜像文档：官方镜像（如 Postgres 容器默认 UID 999、Nextcloud 的 www-data 是 UID 33）通常配合 Fix 1 或 Fix 2；linuxserver 系直接 Fix 3。

### 进阶：userns-remap、rootless 与命名卷

**userns-remap** 把容器内的 root 映射成宿主上一个无特权的高位 UID，由 `/etc/subuid` 与 `/etc/subgid` 管理（格式如 `testuser:231072:65536`），建议新装 Docker 时启用 [S3]。但限制明确：与 `--pid=host`、`--network=host`、`--privileged` 以及不支持 userns 的卷/存储驱动**不兼容** [S3]。rootless 模式同样做重映射（容器 UID 0 → 宿主 100000、1000 → 101000），此时 **bind 宿主目录的属主必须是对应的重映射 UID** [S5]。

**命名卷**由 Docker 按镜像文件系统初始化属主，通常比 bind 省心；但**换用不同 UID 的镜像时，旧卷会保留旧属主**，需要手动清理 [S5]。

### 本章小结

- `Permission denied` 的根因是容器进程 UID 与宿主目录属主不一致——Docker 不做 UID 映射 [S5]。
- 排查三步：`docker exec id` → `docker inspect --format '{{.Config.User}}'` → 对齐宿主目录属主。
- 三招修复按场景选：`chown -R`（通用可靠）、compose `user:`（依赖镜像支持）、linuxserver `PUID/PGID`（与 `--user` 不兼容）[S5][S6]。
- userns-remap / rootless 会重映射 UID，并带来一系列兼容性限制 [S3][S5]；命名卷换镜像 UID 会残留旧属主 [S5]。

下一章我们把视角从"能不能读写"转到"该不该给读写权限"：只读挂载、SELinux 标签，以及最危险的 docker.sock 挂载，为什么被称为 root 级信任。

---

## 第 5 章：安全边界：只读、SELinux 与 docker.sock 风险

前面几章解决的是「容器能不能读写宿主文件」，这一章回答更尖锐的问题：容器一旦被攻破，会连带接管宿主的哪些能力？关键看两件事——挂载是否只读，以及 docker.sock 是否交了出去。

### 5.1 默认信任模型：root + 可写 = 提权

多数容器默认以 root 运行 [S4]，而 bind 挂载默认可写 [S1]。两者叠加意味着：容器内任意进程都能改写、删除宿主挂载目录里的文件，甚至影响非 Docker 进程。第 4 章解决「写不了」，本节解决「不该写」。

**把只读作为默认底线**：除非明确要写，一律加 `ro`。

```bash
# 推荐：--mount 显式声明只读
docker run --mount type=bind,src="$(pwd)"/config,dst=/etc/app,ro nginx

# 等价短语法
docker run -v "$(pwd)"/config:/etc/app:ro nginx
```

> [!tip] 大白话：只读挂载
> 把 `ro` 想成给宿主机目录上了一把「只读锁」——容器里能看能读，但改不了。所以就算容器被攻破，攻击者也最多偷看，删改不了你的配置和代码。

### 5.2 SELinux 标签：`:z` 与 `:Z`

在强制 SELinux 的发行版上，容器进程与宿主文件的标签不匹配会被拒绝访问。`-v` 支持两个标签选项：`:z` 表示内容在多个容器间共享，`:Z` 表示私有、不共享 [S1]。另外 `--mount` 无法设置 SELinux 标签，Compose 服务里的 `:z/:Z`（以及 `:ro`）会被忽略 [S1][S4]。

> [!warning] `:Z` 会改宿主目录标签
> `:Z` 会**重打宿主机目录的标签**，对 `/home`、`/usr` 这类系统目录使用会把宿主机搞到不可用，需手工重标恢复 [S1]。能用 `:z` 就不轻易用 `:Z`。

```bash
# :z 共享标签（多容器共用该目录）
docker run -d -v "$(pwd)"/data:/app:z nginx
```

> [!tip] 大白话：SELinux 标签
> 把标签想成文件上的「门禁卡等级」。`:z` 是发一张公用卡，几个容器都能进；`:Z` 是给目录重写一张只属于本容器的卡——所以千万别拿它刷 `/home`、`/usr` 这种系统目录，刷完宿主自己也进不去了。

### 5.3 docker.sock：把 root 交给了容器

`dockerd` 以 root 运行，监听 `/var/run/docker.sock`（默认属主 `root:docker`、权限 `0660`）。任何能写这个 socket 的进程，都能让 daemon 以 root 执行任意 API 命令，**daemon 不会重新认证客户端** [S9]。攻击路径是：写 socket → 创建 `--privileged` 容器 → 拿到宿主 root。这不是 Docker 的漏洞，而是它的信任模型设计 [S9]。

```bash
# 高危反例：把整把 root 交给容器
docker run -it -v /var/run/docker.sock:/var/run/docker.sock alpine sh
```

> [!warning] 高危：挂载 docker.sock 等于交 root
> 上面这行命令会把宿主的 Docker 管理权整个交给容器——容器内任何进程都能以 root 身份调用 Docker API 提权到宿主。**绝不**在生产使用；若某镜像确实需要访问 socket，用第 5.4 节的代理网关并只开最小权限。

只读挂载 socket 也只是「边际改善」：文件系统层面写不了，但 API 依然能查状态、inspect 其它容器、横向移动 [S9]，安全评审不要把 `ro` socket 当低风险。同理，`/`、`/etc`、`/root` 这类宿主敏感路径都不该 bind 进容器 [S9]。

> [!tip] 大白话：docker.sock
> 把 socket 想成宿主的「管理员后台入口」。你把它挂进容器，等于把 root 权限的管理员账号直接交给容器里的程序用——daemon 不验身份，谁来都当 root。所以能不挂就不挂，挂了就当「在宿主上跑 root 程序」来对待。

### 5.4 缓解：代理网关与远程认证

**方案一：docker-socket-proxy**。用 HAProxy 做白名单网关，按环境变量逐个开关 API 段，被禁的请求返回 403；默认只开 `EVENTS/PING/VERSION`，安全关键段默认关闭 [S8]。

```bash
docker run -d --name docker-socket-proxy \
  --privileged \   # 部分 SELinux/AppArmor 环境下连 socket 必需
  -p 127.0.0.1:2375:2375 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  tecnativa/docker-socket-proxy
```

**方案二：远程访问用 TLS 双向认证（2376）或 SSH**，别用裸奔的 2375——**2375 无 TLS 等于远程 root** [S9]。

```bash
# daemon 端开启 TLS 双向认证
dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem \
  --tlskey=server-key.pem -H=0.0.0.0:2376

# 私钥按 root 密码级别保管
chmod 0400 ca-key.pem key.pem server-key.pem
```

```bash
# SSH context：最省事的远程安全通道
docker context create --docker host=ssh://user@host my-remote-engine
docker context use my-remote-engine
```

### 本章小结

- 默认 root ∩ bind 默认可写 = 容器被攻破即控制宿主挂载文件；只读挂载应作为默认底线。
- SELinux `:z`/`:Z` 用 `-v` 指定；`:Z` 会重打宿主标签，勿用于系统目录。
- 挂载 docker.sock 等于把 root 交给容器，只读也不安全；`/`、`/etc`、`/root` 不要 bind。
- 需要 socket 用 docker-socket-proxy 白名单；远程访问用 TLS(2376) 或 SSH，私钥 `chmod 0400`。

下一章把视线转到 Docker Desktop：同样一份挂载配置，在 macOS/Windows 上为什么会慢得离谱？

---

## 第 6 章：Docker Desktop 的差异：macOS/Windows 挂载性能

在 macOS 或 Windows 上跑 Docker，bind mount 功能一切正常，但你会遇到一个怪现象：大量小文件读写时性能断崖式下跌。这一章讲清根因，并给出可落地的规避技巧。

### 性能根因：一切都在跨 VM 边界

Docker Desktop 的 Linux 容器跑在一台轻量 VM 内，宿主的 APFS/NTFS 文件系统必须经过虚拟文件系统桥接，每次文件操作都要跨 VM 边界往返。当项目里有成千上万个小文件（典型如 `node_modules`）时，单次操作的开销被无限放大，性能骤降；原生 Linux 没有这层桥接，所以没有此开销 [S10]。

> [!tip] 大白话
> 把跨 VM 读写想成「快递过海关」：大文件是一个集装箱，一次过检；几千个小文件是几千个小包裹，每个都要单独开箱。文件越小越碎，排队越久，整体性能就越难看。

### macOS：三种后端

| 后端 | 说明 |
|------|------|
| VirtioFS | Docker Desktop 4.22+ 默认，最快（比 gRPC-FUSE 快 2–5x） |
| gRPC-FUSE | 旧默认 |
| osxfs | legacy，最慢 |

新版本默认 VirtioFS，无需再手动切换旧后端 [S10]。

### Windows：WSL2 走 9P 协议

WSL2 后端固定走 9P 协议，没有后端可切换。关键结论：**代码放 WSL 文件系统内性能最好**；从 Windows 盘（如 `C:\`）bind 挂载会跨 9P 边界变慢 [S10]。

> [!tip] 大白话
> 把 WSL 文件系统想成「隔壁邻居」，Windows 盘想成「两条街外」。在邻居家干活随叫随到，跨街取文件就要多跑路。所以 Windows 上开发，项目先放进 WSL 里。

### Synchronized file shares（Mutagen）

官方提速方案：在 VM 内建一个 ext4 同步缓存，用 Mutagen 把宿主文件同步进去，容器读写走本地缓存，宣称 2–10x 提速。需 Pro/Team/Business 订阅（4.27+），可用 `.syncignore` 排除 `node_modules`/`.git`；不适用于 WSL、Windows 容器与 K8s hostPath [S10]。

### 社区规避技巧

- `node_modules`、`.git` 用命名卷隔离，绕开大量小文件跨 VM 的开销；
- macOS 只共享最小目录（默认 /Users、/Volumes、/private、/tmp 等），别整盘共享；
- 一致性 flag 可按需降级，例如 `-v /host:/app:delegated`（三档 `consistent`/`cached`/`delegated`，越靠后越宽松、越快）。

> [!tip] 大白话
> 「只共享最小目录」想成「只给访客会议室的钥匙，不把整栋楼的门禁都发出去」。共享范围越小，需要桥接的路径越少，越省事也越安全。

### 本章小结

- 根因是 VM 内桥接：小文件越多，跨 VM 边界的开销被放大得越厉害 [S10]。
- macOS 默认 VirtioFS 最快，gRPC-FUSE / osxfs 为旧后端 [S10]。
- WSL2 走 9P 协议，代码放 WSL 文件系统内性能最好 [S10]。
- 重度文件同步可上 Mutagen（Synchronized file shares，Pro+ 订阅）[S10]。
- 实战上：命名卷隔离依赖目录、只共享最小目录、一致性 flag 降级。

下一章将汇总选型、权限与安全规则，走查一个 Web 服务读写宿主目录的完整配置。

---

## 第 7 章：实战案例：Web 服务读写宿主目录的完整配置

前六章拆开了选型、命令、Compose、权限、安全与平台差异，本章把它们组装成一个完整场景：一个 Web 服务从宿主目录**只读**读取配置，同时把日志**可写**落到另一个宿主目录。这是「容器控制宿主文件」最典型也最常见的组合，跑通它，等于把全笔记的坑都预演了一遍。

### 7.1 场景与选型

按第 1 章的选型判断：服务要直接读写宿主路径 → 用 **bind mount**（[S1](https://docs.docker.com/engine/storage/bind-mounts/)）。配置目录是只读的，挂载时加 `ro`；日志目录需要容器持续写入，保持默认可写。两个挂载点一个防写、一个放写，正好对应第 5 章的结论——默认可写是风险，只有必要场景才放开。

> [!tip] 大白话
> 把配置目录想成「门口贴的禁令清单」——容器只能看不能改；日志目录想成「回收站」——容器可以往里扔东西，宿主随时能翻出来看。所以一个挂 `ro`，一个不挂 `ro`。

### 7.2 完整配置（两种写法二选一）

先准备宿主目录，并把属主对齐容器内 UID（本场景容器以 UID 1000 运行，[S5](https://selfhosting.sh/foundations/docker-volume-permissions/)）：

```bash
# 终端
mkdir -p /opt/myapp/config /opt/myapp/logs
sudo chown -R 1000:1000 /opt/myapp/config /opt/myapp/logs
```

#### 方式 A：`docker run` + `--mount`

```bash
# 终端
docker run -d --name web \
  --user "1000:1000" \
  --mount type=bind,src=/opt/myapp/config,dst=/app/config,ro \
  --mount type=bind,src=/opt/myapp/logs,dst=/app/logs \
  myapp/web:1.0
```

要点：`ro` 保证配置只读；`--user "1000:1000"` 让容器进程以非 root 运行；`--mount` 的 `src`/`dst` 都用绝对路径（[S1](https://docs.docker.com/engine/storage/bind-mounts/)）。

#### 方式 B：docker compose

```yaml
# compose.yml
services:
  web:
    image: myapp/web:1.0
    user: "1000:1000"
    read_only: true                    # 容器根文件系统只读，安全底线
    volumes:
      - type: bind
        source: /opt/myapp/config
        target: /app/config
        read_only: true
      - type: bind
        source: /opt/myapp/logs
        target: /app/logs
    tmpfs:
      - /tmp                            # 临时文件放内存盘
```

要点：长语法把 `type/source/target/read_only` 写清楚，比短语法更显式（[S4](https://docs.docker.com/reference/compose-file/services/)）；`read_only: true` 让整个容器只读，只有挂载的日志目录可写，临时文件交给 `tmpfs`。

### 7.3 验证与权限排查

启动后先验证挂载是否符合预期：

```bash
docker exec web id                          # 1. 看容器内 UID/GID
docker exec web ls /app/config              # 配置只读可用
docker exec web touch /app/config/x         # 应报 Read-only file system
docker exec web sh -c 'echo ok >> /app/logs/app.log'   # 日志可写
ls -l /opt/myapp/logs/app.log               # 宿主侧能看到日志
```

若报 `Permission denied`，套用第 4 章的权限三步排查（[S5](https://selfhosting.sh/foundations/docker-volume-permissions/)）：

1. `docker exec <容器> id` 看容器进程实际 UID；
2. `docker inspect <镜像> --format '{{.Config.User}}'` 看镜像默认用户；
3. 对齐宿主目录属主：`sudo chown -R <UID>:<GID> /opt/myapp/...`，或用 `--user` / PUID/PGID（linuxserver 镜像）。

> [!tip] 大白话
> 把 UID 想成「员工工号」：文件系统只认工号不认名字。容器里工号 1000 的人要写文件，宿主管文件夹的人也得是 1000，否则就是「工号对不上，拒绝放行」。chown 就是换钥匙。

### 7.4 安全底线四原则与坑位清单

收尾用安全底线四原则自查（[S9](https://www.netdata.cloud/guides/docker/docker-socket-security/)、[S7](https://docs.docker.com/engine/security/protect-access/)、[S1](https://docs.docker.com/engine/storage/bind-mounts/)）：

1. **默认只读**：能用 `ro` 就不放开写；
2. **不挂 docker.sock**：挂 socket 等于让容器内任意代码都能以 root 调用 Docker API；
3. **不挂系统目录**：别把 `/`、`/etc`、`/root` bind 进容器；
4. **非 root 运行**：`--user` / `user:` / PUID/PGID 至少用一个。

最后对照全章坑位清单：

| 坑位 | 表现 | 对策 |
|------|------|------|
| permission denied | 容器写宿主目录报错 | 三步排查对齐 UID |
| root 属主错乱 | 宿主文件全变 root | 用 `user:` 或 chown |
| bind 遮蔽非空目录 | 容器内原文件消失 | 挂到空目录，重建容器解除 |
| `-v` 自动建目录 | 源路径不存在被静默创建 | 用 `--mount` + `bind-create-src` 显式控制 |
| `:Z` 重打标签 | 宿主目录可能不可用 | SELinux 场景优先 compose 长语法 `selinux:` 字段 |
| socket=root | 容器内任意代码提权 | 不挂 socket，或走 docker-socket-proxy |
| Docker Desktop 性能 | 大量小文件读写慢 | 用命名卷隔离 node_modules，最小共享目录 |

### 本章小结

- 综合场景 = 只读配置 bind + 可写日志 bind，`docker run` 与 compose 两种写法任选；
- 权限三步排查解决九成 `permission denied`；
- 安全底线四原则是发布前的硬性检查；
- 坑位清单覆盖前六章核心陷阱，可直接当自测表。

## 相关笔记

- [[docker里的GID和UID]] - Docker 容器 UID/GID 映射原理详解
- [[Docker与DockerCompose命令速查]] - docker run / docker compose 常用命令速查
- [[Docker MOC]] - Docker 学习笔记目录

---

## 结语

至此，从选型、命令、Compose、权限、安全到平台差异的完整链路已经走通。回到最初的问题——让 Docker 容器控制/处理宿主文件——本质上是三件事：选对挂载方式（bind / volume / tmpfs）、对好文件属主（UID/GID）、守住安全边界（只读、不挂 socket、非 root）。第 7 章的坑位清单可以直接当自测表，按它逐条核对，大多数容器文件访问问题都能在几分钟内定位。
