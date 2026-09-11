## 第 5 章 映射给 Docker 容器

第 4 章结束时，宿主机上多了一个 `/mnt/openlist`（示例路径）：它是 rclone 用 FUSE 挂出来的目录，`ls` 能看到聚合后的网盘内容。现在的问题是：**怎么让一个 Docker 容器也能看到它？**

这一步的技术名字叫"挂载"，但真正的难点不在命令怎么写，而在两个判断：**该用哪种挂载类型**（为什么这里不能选 named volume），以及**容器以什么身份去看这些文件**（同一个链路上，两个容器的答案可能不一样）。本章把这两件事讲透，然后给出两条通用的挂载模式，最后用一个一次性测试容器把只读、读写各验证一遍。

---

### 5.1 核心概念：bind mount 还是 named volume——本章没有选择题

先把两类挂载的差别摆清楚。

| | bind mount（绑定挂载） | named volume（命名卷） |
| --- | --- | --- |
| 数据放在哪 | 宿主机上**你指定的**那个路径 | Docker 在**自己的存储目录**里创建的新目录 |
| 谁管理 | 你（宿主机文件系统的普通目录） | Docker（创建、维护、隔离都由它负责） |
| 宿主机上能直接看到吗 | 能，就是那个路径 | 能，但要先 `docker volume inspect` 查到位置 |
| 典型定位 | 需要宿主机与容器**同时**访问同一份文件 | 持久化容器自己产生的数据 |
| 传播设置 | 可配置 | 固定 `rprivate`，**不可配置** |

Docker 官方文档对 volume 的描述是：它是"用于容器的持久化数据存储，由 Docker 创建和管理"，创建后存放在宿主机的一个目录里，"与 bind mount 的相似之处在于此，区别在于 volume 由 Docker 管理，并且与宿主机的核心功能相隔离"。`docker volume inspect` 出来的 `Mountpoint` / `Source` 形如 `/var/lib/docker/volumes/my-vol/_data`，`docker inspect` 里的 `Type` 字段是 `volume`[^c5-S18]。

然后是**选型的分水岭**，这是本章全部推理的起点，官方原话是：

> Volumes are not a good choice if you need to access the files from the host, as the volume is completely managed by Docker. Use bind mounts if you need to access files or directories from both containers and the host.

翻译过来：**需要从宿主机访问这些文件时，volume 不是好选择**，因为 volume 完全由 Docker 管理；需要容器与主机**同时**访问同一文件或目录时，应该用 bind mount[^c5-S18]。

拿这把尺子量一下本章的场景：

- 第 4 章的 rclone 挂载点 `/mnt/openlist` 是一个**已经存在于宿主机上**的 FUSE 文件系统。它由 rclone 进程提供，不是 Docker 造出来的。
- volume 只能在 Docker 自己的存储目录里创建，你**没法把一个已存在的宿主机目录"变成" volume**——volume 的数据目录名是 Docker 起的。
- 因此，要把 `/mnt/openlist` 交给容器，**只能用 bind mount**。这不是偏好问题，是唯一可行项。

> [!tip] 大白话
> 把 bind mount 想成"把自家书架上指定的那一格直接敞开给客人看"——格子还在你家，客人看到的和你看到的永远是同一份。named volume 则像"Docker 自己家的一个储物柜"：柜子放在哪、里面怎么摆，全由 Docker 说了算，你从客厅看不见也够不着。
> 所以：**要宿主机和容器看同一份东西，就用 bind mount**；本章的 rclone 挂载点正是"主机上已有、Docker 造不出来"的那种东西。

顺带记住 volume 的一条硬限制，后面讲传播时会用到：官方明确 volume 使用 `rprivate`（recursive private）bind propagation，而且"bind propagation 对 volume 不可配置"[^c5-S18]。也就是说，只要选了 volume，挂载传播这一整块能力就与你无关了。

---

### 5.2 bind mount 的四条硬语义

bind mount 的行为不复杂，但有四条容易踩的规则，官方文档把它们列在同一节里[^c5-S11]。

**第一条：默认对宿主机文件有写权限。** 官方原话 `Bind mounts have write access to files on the host by default.`。副作用是容器里的进程可以改动宿主机的文件系统——创建、修改、甚至删除重要的系统文件，因此官方提醒这有安全含义。要阻止写入，就在挂载项里加 `readonly` 或 `ro`：

```bash
# 官方两种写法等价
docker run --mount type=bind,src=<宿主机路径>,dst=<容器内路径>,readonly ...
docker run -v <宿主机路径>:<容器内路径>:ro ...
```

**第二条：bind mount 创建在 Docker daemon 所在的那台宿主机上，不是客户端。** 官方原话 `Bind mounts are created to the Docker daemon host, not the client.`，并进一步说明：如果用的是远程 Docker daemon，你就**没法**用 bind mount 去访问客户端机器上的文件。对本章意味着：**rclone 挂载点必须与 Docker daemon 在同一台机器上**。如果 daemon 跑在远程主机，你得在那台主机上重新做第 4 章的挂载。

**第三条（本章最重要的一条）：挂进非空目录会遮蔽原有内容，而且这个行为与 volume 不同。** 官方对它的描述是：把文件或目录 bind mount 进容器里一个"本来就有文件或目录"的目录时，**原有内容被挂载遮蔽（obscured）**；类比是你在 Linux 宿主机上往 `/mnt` 里存了文件，然后又往 `/mnt` 挂了一个 U 盘——`/mnt` 原来的内容就被 U 盘的内容盖住了，直到 U 盘被卸载。接着是一条坏消息：

> With containers, there's no straightforward way of removing a mount to reveal the obscured files again. Your best option is to recreate the container without the mount.

容器里没有简单的办法卸下挂载、把被遮住的文件找回来，**最佳做法是去掉这个挂载、重建容器**。官方还专门点了一句：`this behavior differs from that of volumes`——**这个行为与 volume 不同**[^c5-S11]。这正是本章 bind mount / volume 对比的直接证据：

- 挂一个**空的 volume** 到装有文件的容器目录，容器里原有的文件会被**复制进** volume（官方行为，可用 `volume-nocopy` 阻止）；
- 挂一个 bind mount 到同样的位置，原有文件则是被**遮蔽**，不会被复制，也拿不回来。

所以映射时一定挑一个"容器里本来就是空的"目标路径。本章的示例统一用 `/media/openlist`——这个路径在干净镜像里不存在，不会遮住任何东西。

> [!tip] 大白话
> 遮蔽就像在书架上贴了一张大海报：海报后面的书**还在**，但你伸手只能拿到海报。想拿回后面的书，唯一省事的办法是把海报整张撕掉重贴——对应到容器，就是删掉容器重建。所以别往容器里"本来就装着东西"的目录上挂，挑个空位挂。

**第四条：带 bind mount 的容器与宿主机强绑定。** 官方说这类容器"strongly tied to the host"：bind mount 依赖宿主机上存在特定目录结构，换一台没有同样目录结构的主机运行就可能失败[^c5-S11]。这解释了为什么"先挂载再起容器"是硬顺序——挂载点是运行前提，不是运行结果。

---

### 5.3 两种写法：`--mount` 还是 `-v`

bind mount 有两种写法，官方对一般场景的结论很直接：`In general, --mount is preferred.`，因为 `--mount` 更显式、且支持全部可用选项[^c5-S11]。

两者的关键差别落在"宿主机路径不存在时会怎样"：

| | `--mount`（长写法） | `-v` / `--volume`（短写法） |
| --- | --- | --- |
| 路径不存在时 | **报错**，不自动创建 | **自动创建**该目录 |
| 创建成什么 | ——（不创建） | **始终创建为目录**（哪怕你想要的是文件） |
| 选项覆盖 | 支持全部选项 | 支持常用选项 |
| 推荐度 | 一般更推荐，更显式 | 简短，适合熟手 |

`-v` 的行为官方原文是：用 `--volume` 去 bind mount 一个宿主机上**尚不存在**的文件或目录时，"Docker 会替你在宿主机上自动创建该目录。它始终被创建为目录"[^c5-S11]。这句话的杀伤力在于后半个——**它始终创建为目录**。如果你本意是挂一个还不存在的**文件**（比如 `rclone.conf`），`-v` 会默默建出一个同名**目录**，容器里的程序读到的就是空目录，而不是你期待的配置文件。这正是第 6 章排障表里"-v 自动建目录造成的空目录假象"的来历。

`--mount` 遇到不存在的源路径则当场报错，官方给出的错误原文是[^c5-S11]：

```text
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

如果你确实想让 `--mount` 也自动创建源目录，官方提供了一个显式开关 `bind-create-src`[^c5-S11]：

```bash
docker run --mount type=bind,src=/home/user/mydir,dst=/mnt/foo,bind-create-src alpine
```

> [!tip] 大白话
> `-v` 像个不吭声的助手：你说漏了嘴、路径写错，它也默默给你把目录建出来（而且只会建成目录），等你发现"怎么是空的"时已经绕了远路。`--mount` 像个较真的助手：路径不对就当场甩你一个报错，让你立刻改对。**排错比省字更重要，所以一般优先 `--mount`。**

**本章的场景该选哪个？** 一句话：优先 `--mount`。因为 rclone 挂载点是第 4 章已经建好的**已存在**目录，`-v` 的"自动创建"在这里一点忙也帮不上，反而只能带来"创建成目录"的误伤风险；而 `--mount` 的报错恰好能在挂载点没挂上时**立刻发现**——这本就是排障里最想要的反馈。

---

### 5.4 传播（bind propagation）：默认双向都不传

这一节可以先用一句话跳过：**大多数用户永远不需要配置它**（官方原话 `many users never need to configure it`）[^c5-S11]。但本章要讲清楚它的边界，因为你挂进来的东西本身就是一个 FUSE 挂载点，属于容易和传播打交道的场景。

绑定传播（bind propagation）指的是：在一个 bind mount 内部新建的挂载，能不能传播到该挂载的副本上。官方用 `/mnt`（同时挂到 `/tmp`）举例：传播设置决定 `/tmp/a` 上的挂载会不会也出现在 `/mnt/a` 上[^c5-S11]。

官方列出的六个取值与含义[^c5-S11]：

| 取值 | 含义 |
| --- | --- |
| `shared` | 双向：原挂载的子挂载暴露给副本，副本的子挂载也传播回原挂载 |
| `slave` | 单向：原挂载的子挂载副本能看到；反方向不行 |
| `private` | 私有：子挂载不向任何一方暴露 |
| `rshared` | 同 `shared`，且传播延伸到双方**嵌套**的挂载点 |
| `rslave` | 同 `slave`，且传播延伸到双方**嵌套**的挂载点 |
| `rprivate` | **默认值**。同 `private`，原挂载与副本内任何位置的挂载点都不向任何方向传播 |

四条必须记住的边界：

1. **默认是 `rprivate`**，"对 bind mount 和 volume 都是如此"[^c5-S11]。也就是默认双向都不传播——容器里再挂东西，宿主机看不到。
2. **只有 bind mount 能配置，而且只在 Linux 宿主机上**。官方原话：`It is only configurable for bind mounts, and only on Linux host machines.`[^c5-S11]。这是本章 5.1 节"选了 volume 就没有传播能力"的呼应。
3. **挂载传播在 Docker Desktop 下不工作**（官方 Note：`Mount propagation doesn't work with Docker Desktop.`）[^c5-S11]。
4. **设置之前，宿主机文件系统本身要已经支持绑定传播**[^c5-S11]。

短写法的写法是把它当成第三个字段里的一个逗号分隔选项；官方示例（逐字）把同一个 `target/` 挂了两次，第二次同时加 `ro` 和 `rslave`[^c5-S11]：

```bash
# --mount 写法
docker run -d \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave \
  nginx:latest

# 等价的 -v 写法
docker run -d \
  --name devtest \
  -v "$(pwd)"/target:/app \
  -v "$(pwd)"/target:/app2:ro,rslave \
  nginx:latest
```

**递归与只读**：如果被 bind mount 的路径本身含有挂载（本章正是如此——`/mnt/openlist` 就是 FUSE 挂载），默认情况下这些子挂载**也会被包含进来**。这个行为由 `bind-recursive` 选项控制，而它**只被 `--mount` 支持，`-v` / `--volume` 不支持**（官方原话）[^c5-S11]。它的取值有 `enabled`（默认）/ `disabled` / `writable` / `readonly` 四个[^c5-S11]。

关于"递归只读"，官方给了一个很实际的警告：如果 bind mount 是只读的，Docker Engine 会**尽力**把子挂载也一起变成只读，这叫递归只读；但**递归只读挂载要求 Linux 内核 5.12 或更高**。内核更旧时，子挂载会被自动以读写方式挂载；在内核低于 5.12 时尝试用 `bind-recursive=readonly` 把子挂载设为只读，会**直接报错**[^c5-S11]。

> [!warning] 易错点
> "外层加了 `:ro`，里面就全都只读了"——**不成立**。内核低于 5.12 时子挂载会自动变成读写，所以一个看似只读的挂载里仍可能存在可写的子路径。依靠 `:ro` 做安全隔离时，必须知道这条边界。

---

### 5.5 SELinux：`z` 与 `Z`，以及两个"不支持"

如果宿主机开着 SELinux，bind mount 需要额外打标签，否则容器可能因为没有标签权限而读不到文件。官方提供了两个选项[^c5-S11]：

- `z`：表示 bind mount 的内容在**多个容器间共享**；
- `Z`：表示内容**私有、不共享**。

有两条后果必须提前知道：

1. **这个改动作用于宿主机文件本身**。官方原话：`This affects the file or directory on the host machine itself and can have consequences outside of the scope of Docker.`[^c5-S11]。也就是说，加 `:z` / `:Z` 改的不是容器的视图，是宿主机上那个目录的标签。官方为此专门警告：把 `/home`、`/usr` 这类系统目录以 `Z` 挂进去，会把宿主机搞到无法运行，可能得手工重打标签。
2. **`--mount` 无法修改 SELinux 标签**（官方原话 `It is not possible to modify the SELinux label using the --mount flag.`）[^c5-S11]。要用 `z`/`Z`，只能用 `-v` 的短写法把选项跟在第三个字段里，例如官方示例的 `-v "$(pwd)"/target:/app:z`[^c5-S11]。

还有一个只在与 Swarm services 同用时才出现的坑：官方 Important 块写明，用 bind mount 配 services 时，SELinux 标签（`:Z` 与 `:z`）以及 `:ro` **都会被忽略**[^c5-S11]。

> 说明：本章的抓取片段里，`--volume` 选项表那一行把选项名 `z` / `Z` 丢掉了（只剩描述文字），所以上面这两个选项名是从正文小节标题与示例行确认的，不是从表格行读到的。

---

### 5.6 本章第二个必须讲清的点：运行身份的两套机制

到这里，"挂得上"的问题解决了。接下来是"以谁的身份看"——这是本章最容易把一条链路跑崩的地方。

关键事实是：**这条链路上的两个容器，可能用两套完全不同的运行身份机制。** 取决于镜像由谁维护。

#### 机制一：OpenList 官方镜像——`user:` / `--user`

OpenList 官方文档写得非常明确[^c5-S01]：

> 在 `v4.1.0` 以后的版本中（不包含 `v4.1.0`），OpenList 镜像已经移除了 `PUID`、`PGID`，并借鉴于 MariaDB 的构建方式，使用 `useradd` 增加了用户 `openlist`（UID 1001）和组 `openlist`（GID 1001），并使用该用户运行 `openlist server`。

紧接着是官方对使用者的要求：**你需要手动处理映射目录的权限问题**，确保容器内的 `openlist(1001)` 用户有权限访问映射的目录；官方同时给出另一条路——"您也可以通过 `--user UID:GID` 的方式来运行容器指定容器内运行 OpenList 的用户和组，让容器内有权限访问映射的目录"[^c5-S01]。在环境变量表里，`PUID`/`PGID` 的说明也标注为"运行身份 UID/GID，在 v4.1.0 以后的版本中废弃"[^c5-S01]。

也就是说，OpenList 官方镜像这一侧的控制手段是：**要么把宿主机目录 chown 给 1001，要么用 `user:` / `--user` 指定运行身份**。这两条在第 1 章已经展开过，这里只需记住它的机制形态。

#### 机制二：LinuxServer.io 镜像——`-e PUID` / `-e PGID`

下面是 **LinuxServer.io 自己的立场**。必须先说清层级：S12 是 **LinuxServer.io 这个镜像维护方的说法，属于镜像维护方口径，不是 Docker 官方文档**。它描述的是其自家镜像的约定，读者不应把它当作 Docker 引擎的通用规则。

LinuxServer.io 的说明是：Docker 把容器都跑在 `root` 用户域下（因为需要网络配置、进程管理、文件系统访问），因此容器内进程也以 `root` 运行；后果是"容器生命周期内创建的所有文件和目录都归 `root` 所有，从而你无法访问它们"。他们给出的解法是 `PUID` 与 `PGID`：`Using the PUID and PGID allows our containers to map the container's internal user to a user on the host machine.`[^c5-S12]

取值怎么来？官方让他们在运行 `id $user` 后关注输出里的 `uid` 与 `gid` 两项（`The two values you will be interested in are the uid and gid.`）[^c5-S12]，一般为 1000/1000。

而最关键的一句，是他们页面顶部 Info 框里的原话[^c5-S12]：

> We are aware that recent versions of the Docker engine have introduced the `--user` flag. Our images are not yet compatible with this, so we recommend continuing usage of PUID and PGID.

翻译：他们知道新版 Docker 引擎引入了 `--user` 标志，但**他们的镜像尚不兼容 `--user`**，所以建议继续使用 PUID 和 PGID。

#### 两套机制对照

| | OpenList 官方镜像（S01，OpenList 官方口径） | LinuxServer.io 系镜像（S12，**镜像维护方口径**） |
| --- | --- | --- |
| v4.1.0 之后 | **移除** `PUID`/`PGID`，内置 `openlist`(1001)，改用 `user:` / `--user` | 仍推荐 `-e PUID` / `-e PGID` |
| 对 `--user` 的态度 | 官方推荐用法之一 | **明确说其镜像尚不兼容** |
| 与 `chown` 的关系 | 可 `chown -R 1001:1001` 后走内置用户 | 靠 PUID/PGID 映射到宿主机用户 |

**这对本章意味着什么？** 如果终点容器（消费者）选的是 LinuxServer.io 系镜像（qBittorrent、Jellyfin 等常见镜像多属此列），那么你同一条链路上会出现**两种并存的运行身份写法**：

- OpenList 容器（官方镜像）用 `user: '1000:1000'` 或 `--user 1000:1000`；
- 消费者容器（LinuxServer 镜像）用 `-e PUID=1000 -e PGID=1000`。

**两种写法都指向"让容器内进程以 uid/gid 1000 访问文件"这同一个目的，但机制不同**：`user:` / `--user` 是在运行容器时直接指定容器内 OpenList 运行的用户和组（S01 官方表述）；`PUID`/`PGID` 则是通过 `-e` 传入后，由镜像把**容器内部用户映射到宿主机上的某个用户**（S12 原话 `map the container's internal user to a user on the host machine`）。一个是"以谁的身份进门"，一个是"把内部用户对到宿主机上的那个用户"。

> [!tip] 大白话
> `--user` 像**直接指定"以谁的身份进门"**：门口保安看见 uid 1000 就放行，进去就是你身份证上的那个人。
> `PUID`/`PGID` 像**发一张临时工牌**：镜像的启动脚本先读你给的这两个数字，再把内部用户的工牌号码改成它们，之后进程才拿着这张改过号的工牌去访问文件。
> 目的都是"让容器里的进程和宿主机上那个用户对上号"，但一个是引擎层直接指定，一个是镜像内部脚本改写。**同一个链路里两套并存完全正常，别以为写错了一个。**

> [!warning] 别混用的坑
> 给 LinuxServer.io 系镜像加 `--user`，按他们自己的说法**当前不兼容**；反过来，给 v4.1.0 之后的 OpenList 官方镜像加 `-e PUID`/`-e PGID` 也不会起作用——这两个变量在镜像里已经移除了。判断依据很简单：**看镜像由谁维护。**

---

### 5.7 通用挂载模式（不绑定具体终点容器）

终点容器还没定（大纲里的 **Q5 / G2**），所以本节只给两条**通用**路径，不绑定 qBittorrent、Jellyfin 之类的具体镜像。无论终点是哪个容器，模式都一样，只是把 `<消费者镜像>` 换掉。

两条路径共同的前提：

- 宿主机挂载点沿用第 4 章产出的路径，示例值 `/mnt/openlist`；
- 容器内目标统一用 `/media/openlist`（干净镜像里不存在，不会遮蔽任何内容，见 5.2 第三条）。

#### 路径一：只读共享（把 rclone 挂载点以 `:ro` 交给消费者）

适合"消费者只负责读"的场景——比如播放器、看图、媒体扫描器。它同时占住两条安全边界：容器写不进去宿主机，容器也不能改动网盘内容。

compose 骨架：

```yaml
# compose.yaml —— 只读共享
services:
  consumer-ro:
    image: <消费者镜像>
    restart: unless-stopped
    volumes:
      # 短写法：宿主机路径:容器内路径:ro
      - "${RCLONE_MOUNT:-/mnt/openlist}:/media/openlist:ro"
```

等价的 `docker run`：

```bash
docker run -d --name consumer-ro \
  --restart=unless-stopped \
  --mount type=bind,src=/mnt/openlist,dst=/media/openlist,readonly \
  <消费者镜像>
```

如果偏好 `--mount` 的显式长写法，把上例中 `--mount` 的每一项拆成 compose 的键，就是 S11 官方示例里出现的那三个键名 `type: bind` / `source:` / `target:`[^c5-S11]。

> 字段归属说明：`type: bind` / `source` / `target` 三个键名来自 S11 官方示例；只读的 `ro` / `readonly` 也是官方选项；`${RCLONE_MOUNT:-/mnt/openlist}` 这个变量与路径值是**本笔记的编排**，不是官方字段。

#### 路径二：读写共享

适合"消费者需要写回"的场景——比如下载器把新文件写入、或需要就地重命名整理。注意两点代价：容器里的写操作会**直接落到宿主机**（进而可能落到网盘），且如 5.6 所述，能不能写成功还取决于容器运行身份与宿主机文件属主是否匹配（这是 **Q4 / G5**，见 5.9）。

compose 骨架：

```yaml
# compose.yaml —— 读写共享
services:
  consumer-rw:
    image: <消费者镜像>
    restart: unless-stopped
    volumes:
      # 不写第三段，即默认读写
      - "${RCLONE_MOUNT:-/mnt/openlist}:/media/openlist"
```

等价的 `docker run`：

```bash
docker run -d --name consumer-rw \
  --restart=unless-stopped \
  --mount type=bind,src=/mnt/openlist,dst=/media/openlist \
  <消费者镜像>
```

#### 关于"一条链路的完整 compose"（缺口 G1）

必须如实说明一个缺口：**没有任何官方来源，把 OpenList + WebDAV + rclone + 终点容器串进同一份 compose 文件**。rclone mount 在本方案的架构里是**宿主机上的一个进程**（第 4 章的 systemd unit），它不在容器里、也不属于 Docker Compose。

所以下面这份"端到端"片段是**拼装**出来的：OpenList 服务段来自 S01 的官方部署语义，消费者挂载段来自 S11 的官方 bind mount 语义，把它们连起来的编排（服务名、依赖顺序、挂载点路径）由本笔记给出。**逐段的来源都标在注释里**：

```yaml
# compose.yaml —— 本笔记拼装（G1：无官方端到端来源）
services:
  # 【来自 S01 官方部署语义】OpenList 本体；端口与数据目录见第 1 章
  openlist:
    image: openlistteam/openlist:latest
    restart: unless-stopped
    ports:
      - "5244:5244"
    volumes:
      - /etc/openlist:/opt/openlist/data
    environment:
      - UMASK=022
    # v4.1.0 之后（不含 v4.1.0）用 user: 指定运行身份（S01）
    user: "0:0"

  # 【来自 S11 官方 bind mount 语义】消费者容器
  consumer:
    image: <消费者镜像>
    restart: unless-stopped
    volumes:
      - "${RCLONE_MOUNT:-/mnt/openlist}:/media/openlist:ro"
    # 【本笔记编排】容器只是消费者，rclone mount 由宿主机 systemd 负责，
    # 不在本文件内定义。
```

重点提醒：**这份 compose 不能解决"挂载点还没挂上"的问题**。rclone mount 是宿主机侧的前置条件，必须按第 4 章先挂好、验证 `/mnt/openlist` 能 `ls` 出内容，再 `docker compose up -d`。这就是 5.2 里"容器与宿主机强绑定"的落地含义。

---

### 5.8 选型反例：什么时候确实该用 named volume

前面一路在说"本章必须用 bind mount"，但**不要把结论过度推广成"bind mount 永远更好"**。官方给 volume 列了一串它真正擅长的场景[^c5-S18]：

- 比 bind mount **更容易备份或迁移**；
- 可以用 Docker CLI 或 Docker API 管理；
- **同时支持 Linux 与 Windows 容器**；
- 可以在多个容器之间**更安全地共享**；
- 新卷可以由容器或构建过程**预填充内容**；
- 应用需要**高性能 I/O** 时。

官方还给了一条性能上的解释：比起直接写进容器的可写层，volume 更快——写可写层需要存储驱动用 Linux 内核的联合文件系统来管理，这层额外抽象会降低性能；而 volume 直接写宿主机文件系统[^c5-S18]。

对照到本章的链路，判断标准可以简化成一句话：

| 你的需求 | 该选 |
| --- | --- |
| 数据是**宿主机上已有的**（rclone 挂载点、已有媒体库、已有配置） | bind mount（**本章**） |
| 宿主机上的人/其他进程也要看同一份 | bind mount |
| 数据是**容器自己产生**的、不需要宿主机侧访问（数据库文件、应用状态） | named volume |
| 要跨多容器安全共享、要 Docker 帮着备份迁移、要高性能 I/O | named volume |

> [!tip] 大白话
> 一句话分清：**"这份数据在宿主机上本来就有、只有宿主机上的人也在用"→ bind mount；"这份数据是容器自己攒出来的、Docker 帮忙看着就行"→ named volume。**
> 本章的 rclone 挂载点属于前者里的极端例子——它不是"宿主机上有个普通目录"，而是"这个目录本身就是一个由宿主机进程提供的文件系统"。Docker 不但没法把它变成自己管理的卷，连复制它的内容都会很别扭。

---

### 5.9 待核实：bind mount 的属主与权限行为

这里是本章唯一必须标"未证实"的小节，务必读清。

一个问题：**把 rclone 挂载点 bind mount 进容器后，容器里的进程"能不能写"，由什么决定？**

本文能给出的**有来源支撑**的部分只有两块：

1. **镜像侧口径（S12，LinuxServer.io 立场，非 Docker 官方）**：容器默认在 `root` 用户域下运行，容器内创建的文件归 `root` 所有，因此需要一个映射机制（PUID/PGID 或其替代）把容器内用户对到宿主机用户上。
2. **宿主机侧的事实（S06，rclone 官方）**：第 4 章用到的 rclone 参数里，`--uid` 与 `--gid` 的默认值都是 `1000`，官方说明是"覆盖文件系统设置的 uid/gid 字段"；`--umask` 默认 `002`，官方说明是"覆盖文件系统设置的权限位"。这三个参数都标注"不支持 Windows"[^c5-S06]。也就是说，rclone 挂载出来的文件在宿主机上表现为 uid/gid 1000、受 `--umask` 控制的权限。

**本文不能给的**：Docker 官方对 bind mount 属主与权限行为的定义。**S11 与 S18 两篇官方文档都没有讨论 bind mount 的 uid/gid 属主规则**（这是缺口 **G5**）。因此：

- 不要认为"Docker 官方规定了 bind mount 里文件归谁所有"——没有这回事；
- 实际能不能写，取决于**容器内运行身份的 uid/gid** 与 **宿主机上文件的实际属主/权限**是否匹配，而宿主机那一侧由 rclone 的 `--uid/--gid/--umask`（S06）和宿主机的 umask 共同决定。

> **Q4 / G5 — 待核实**：bind mount 的属主与权限行为**没有官方一手来源**。上面这段只能用 S12 的镜像维护方口径加 S06 的 rclone 参数来推断，不能表述为"Docker 官方定义了 bind mount 属主规则"。真正动手时，请以 `ls -ln /mnt/openlist`（看宿主机上的实际数字属主）和容器内 `id`（看容器进程的实际 uid/gid）两边对照为准。

---

### 5.10 可选旁支（路标，不展开）：卷驱动插件

前面说"rclone 挂载点必须先在宿主机上挂好"，这是方向 A 主线的架构。但 Docker 官方文档的 volume 驱动章节里，还演示了另一条路：使用 **`rclone/docker-volume-rclone`** 这个卷驱动插件，先 `docker plugin install --grant-all-permissions rclone/docker-volume-rclone --aliases rclone`，再用 `docker volume create -d rclone ...` 把远端直接创建成一个 volume[^c5-S18]。

它的意义是：**不经宿主机挂载点，直接把远端当作 volume 用**。这正好绕开了本章"为什么必须用 bind mount"的前提——如果 rclone 变成了卷驱动，数据就归 Docker 管了。

本方向（方向 A）**不展开**这条路，此处只作为一个路标：等全链路跑通后再回来看。需要注意的是，官方文档里该章节的示例是 SFTP 远端（`-o type=sftp ...`），与本章的 WebDAV 远端不同，迁移到本链路上需要自行验证。

---

### 5.11 章末可跑产出：用一个一次性容器验证映射

目标：用测试容器把 rclone 挂载点映射进去，**先只读**——容器内能看到文件、但写不进去；**再改成读写**验证一次。

前置检查（第 4 章的产物必须在）：

```bash
ls -ln /mnt/openlist          # 应能看到聚合后的目录/文件，而不是空目录
mount | grep /mnt/openlist    # 应看到 FUSE 相关的挂载行
```

如果这里是空的或报错，**不要继续**——先回第 4 章把挂载跑通。原因见 5.2 第四条：bind mount 只是把宿主机已有的目录搬进容器，它不会替你把 rclone 挂上。

**第一步：只读映射**

```bash
# 起一个一次性测试容器（alpine 里带 sh，够用）
docker run -d --name mnt-ro \
  --mount type=bind,src=/mnt/openlist,dst=/media/openlist,readonly \
  alpine sleep 3600
```

在容器内查看：

```bash
docker exec mnt-ro ls -la /media/openlist
```

能看到第 2 章挂进 OpenList 的那些目录/文件（目录树示意如下），即映射成功：

```text
/media/openlist/          ← 容器内视角（= 宿主机 /mnt/openlist）
├── 阿里云盘/
│   └── 电影/
└── 本地存储/
    └── 测试.txt
```

再试着写：

```bash
docker exec mnt-ro sh -c 'echo hi > /media/openlist/_writetest'
# 预期：sh: can't create /media/openlist/_writetest: Read-only file system
```

出现 `Read-only file system` 就对了——`:ro` 生效，容器写不进去宿主机。可以用 `docker inspect` 复核，`Mounts` 段里应看到 `"Type": "bind"`、`"RW": false`、`"Propagation": "rprivate"`（S11 官方示例中这些字段的取值即为 `Type: bind`、`Mode: ro`、`RW: false`、`Propagation: rprivate`）[^c5-S11]。

**第二步：改成读写验证一次**

```bash
docker rm -f mnt-ro

docker run -d --name mnt-rw \
  --mount type=bind,src=/mnt/openlist,dst=/media/openlist \
  alpine sleep 3600

docker exec mnt-rw sh -c 'echo ok > /media/openlist/_writetest && cat /media/openlist/_writetest'
# 预期输出：ok
```

确认文件确实落到了宿主机：

```bash
ls -l /mnt/openlist/_writetest     # 宿主机上应能看到这个文件
rm /mnt/openlist/_writetest        # 清理，别污染网盘
docker rm -f mnt-rw
```

> **注意这一步验证了什么**：`alpine` 默认以 `root` 运行，所以这里验证的是"删掉 `:ro` 后挂载确实可写"，**不是**"权限匹配问题已解决"。真正换成消费者容器（尤其是 LinuxServer.io 系或非 root 运行的镜像）后，能否写入取决于运行身份与文件属主的匹配——那属于 5.9 标出的 **待核实** 区域，请以 `ls -ln` + 容器内 `id` 两边对照来判断。

---

### 本章小结

- **本章只能用 bind mount。** 官方明文：需要从宿主机访问这些文件时 volume 不是好选择，因为 volume 完全由 Docker 管理；需要容器与主机同时访问时应使用 bind mount。第 4 章的 rclone 挂载点是宿主机上已存在的 FUSE 挂载，Docker 造不出对应的 volume，所以选 bind mount 是被迫的，不是偏好。
- **bind mount 四条硬语义**：默认对宿主机文件有写权限（`:ro`/`readonly` 阻止）；创建在 daemon 宿主机而非客户端（远程 daemon 场景行不通）；挂进非空目录会**遮蔽**原有内容且没有简单办法恢复，只能重建容器——官方明说这个行为**与 volume 不同**；容器与宿主机强绑定（所以必须"先挂载再起容器"）。
- **优先 `--mount`**：更显式、支持全部选项；`-v` 会自动创建不存在的宿主机路径且**始终创建为目录**，`--mount` 则直接报错（官方错误原文已给出），官方还提供 `bind-create-src` 作为显式开关。
- **传播**：默认 `rprivate` 双向都不传；只有 bind mount 可配置、只在 Linux 宿主机；Docker Desktop 下不工作；`bind-recursive` 仅 `--mount` 支持；递归只读要求内核 5.12+。SELinux 的 `z`/`Z` 改的是**宿主机文件本身**，`--mount` 无法修改标签，services 下 `:Z`/`:z` 与 `:ro` 会被忽略。
- **运行身份有两套机制，这是本章最该记住的一点**：OpenList 官方镜像在 v4.1.0 之后（不含 v4.1.0）移除 `PUID`/`PGID`，改用 `user:` / `--user`（内置 `openlist` 1001）；LinuxServer.io 系镜像（**镜像维护方口径，非 Docker 官方**）仍推荐 `-e PUID` / `-e PGID`，并明说其镜像**尚不兼容 `--user`**。终点容器若属后者，则同一链路上两种机制并存——判断依据是"看镜像由谁维护"。
- **两个缺口如实标注**：**G1**——没有官方来源把 OpenList + WebDAV + rclone + 终点容器串成一份 compose，本章的端到端片段是拼装并逐段标明归属的；**Q4/G5**——bind mount 的属主与权限行为**无官方来源**，只能靠 S12 的镜像侧口径加 S06 的 `--uid/--gid/--umask` 支撑，不得表述为 Docker 官方规则。

---

[^c5-S01]: OpenList Docs — 使用 Docker 安装（T1，OpenList 官方口径），本地文件 `sources/S01_openlist_docker_install.md`。
[^c5-S06]: rclone — mount 命令文档（T1，rclone 官方口径），本地文件 `sources/S06_rclone_mount.md`。
[^c5-S11]: Docker Docs — Bind mounts（T1，Docker 官方），本地文件 `sources/S11_docker_bind_mounts.md`，来源 URL `https://docs.docker.com/engine/storage/bind-mounts/`。该页 Compose 示例被抓取时整段丢失换行与缩进（仅键名 `type: bind` / `source: ./static` / `target: /opt/app/static` 可用），本章所有 compose 片段均为**按官方字段重写**，非逐字引用。
[^c5-S12]: LinuxServer.io — Understanding PUID and PGID（**镜像维护方口径，非 Docker 官方文档**），本地文件 `sources/S12_linuxserver_puid_pgid.md`，来源 URL `https://docs.linuxserver.io/general/understanding-puid-and-pgid/`。该文件正文空格被去掉（如 `dockercreate--name=beets-ePUID=1000-ePGID=1000linuxserver/beets`），其命令串**不可直接复制**；本章涉及该来源的命令一律按语义重写。
[^c5-S18]: Docker Docs — Volumes（T1，Docker 官方），本地文件 `sources/S18_docker_volumes.md`，来源 URL `https://docs.docker.com/engine/storage/volumes/`。该页 Compose 示例被抓取时压成一行，本章 compose 片段为**按官方字段重写**，非逐字引用。
