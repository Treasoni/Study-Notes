## 第 3 章：Docker 命令速查：网络、卷与系统管理

上一章我们把镜像和容器的命令玩熟了，但一个真实应用还有两个「看不见的邻居」：容器之间要互相通信（网络），数据要跨重启存活（数据卷）。这一章把这两组命令讲完，再教你安全地做系统清理——这可能是整个 Docker 里最需要「手别抖」的操作。

### 3.1 网络命令组：让容器互相找到对方

默认情况下，多个容器会加入同一个名为 `bridge` 的默认网络，可以通过容器名互相访问。需要隔离、自定义网段时，再自己建网络。

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker network ls` | 列出所有网络 | `docker network ls` |
| `docker network create [-d 驱动] NAME` | 新建网络（`-d bridge` 是默认驱动） | `docker network create mynet` |
| `docker network inspect NAME` | 查看网络详情（网段、已连接容器 IP） | `docker network inspect mynet` |
| `docker network connect 网络 容器` | 把运行中的容器接入网络 | `docker network connect mynet web` |
| `docker network disconnect 网络 容器` | 把容器移出网络 | `docker network disconnect mynet web` |
| `docker network rm NAME` | 删除网络（须先断开所有容器） | `docker network rm mynet` |

> [!tip] 大白话
> 把网络想成**楼里的内线电话**：容器一搬进这栋楼（网络），就有了一个内部号码（IP），通过容器名就能拨通彼此；`connect`/`disconnect` 就是给某个房间「接通/掐掉内线」。所以——多个容器要协作，就放进同一个网络，互相用名字访问，而不是写死 IP。

### 3.2 数据卷命令组：让数据不随容器消失

容器是「用完可扔」的，但数据库、上传文件这些数据必须活下来。数据卷（volume）就是 Docker 管理的一块独立存储，删容器不影响它。

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker volume ls` | 列出所有卷 | `docker volume ls` |
| `docker volume create NAME` | 新建命名卷 | `docker volume create mydata` |
| `docker volume inspect NAME` | 查看卷详情（挂载点、驱动） | `docker volume inspect mydata` |
| `docker volume rm NAME` | 删除指定卷 | `docker volume rm mydata` |
| `docker volume prune [-a] [-f]` | 清理未使用的卷（`-a` 也删未被引用但仍在用的，需谨慎） | `docker volume prune -f` |

挂载数据有两种常见方式，第 2 章的 `-v` 参数两者都支持：

- **命名卷**：`-v mydata:/data`，存放位置由 Docker 管理，路径可移植，适合数据库等需要长期保存的数据。
- **绑定挂载**：`-v $(pwd):/data`，直接指向宿主机某个目录，适合开发时改代码即时生效；但权限按数字 UID/GID 匹配，容易踩坑（见 [[docker里的GID和UID]]）。

> [!tip] 大白话
> 把数据卷想成**租客房间里的冰箱**：容器是租客，退了房（删除容器）冰箱和里面的东西还在；只有你主动把冰箱拖走（`volume rm` / `prune`），数据才真没了。所以——想留数据，就挂卷；删容器时别顺手把卷也删了。

### 3.3 系统命令组：看家底与安全清理

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker info` | 系统级信息（容器/镜像数量、存储驱动） | `docker info` |
| `docker version` | 分别显示 Client 与 Server/Engine 版本 | `docker version` |
| `docker system df` | 磁盘占用统计（镜像/容器/卷/构建缓存） | `docker system df` |
| `docker system prune [-a] [-f] [--volumes]` | 清理闲置资源（见下表） | `docker system prune -a` |
| `docker login [仓库]` | 登录镜像仓库（建议 `--password-stdin` 安全读密码，避免明文入历史） | `docker login` |

`system prune` 的 Flag 逐层「加码」，破坏性也随之加大：

| Flag | 含义 | 风险 |
|------|------|------|
| （无 Flag） | 删已停容器 + 未用网络 + 悬空镜像 + 未用构建缓存 | 低 |
| `-a` | 连**未被任何容器使用**的镜像一起删 | 中：之后拉镜像要重新下载 |
| `-f` | 跳过确认提示（否则会先问一句） | 低 |
| `--volumes` | 额外清理未使用的卷 | **高：可能销毁数据** |

> [!warning] 卷默认不自动删除
> `docker system prune` 默认**不会**碰数据卷。官方理由是：*"Volumes are never removed automatically, because to do so could destroy data."*（卷永不自动删除，因为那可能摧毁数据）。所以只有当你**明确**加 `--volumes` 时才会删卷——在跑这条命令前，务必确认卷里的数据不再需要，或已备份。

安全清理的推荐顺序：先 `docker system df` 预览占了多大空间 → 日常用 `docker system prune -a --filter "until=24h"` 只清 24 小时前的闲置镜像 → 需要时按类型单独清理（`docker container prune`、`docker image prune -a`、`docker network prune`、`docker buildx prune`）。

> [!warning] 别手滑
> `docker system prune -a --volumes` 会一口气删掉所有未使用镜像和未使用卷。心情不好想「大扫除」时可以这么干，但请先背出你哪几个卷里有数据库——**一旦删了，没有任何回收站**。

### 本章小结

- 网络是容器间互相发现的通道：`network create` + `connect`，容器用名字互访。
- 数据卷是独立于容器的存储：删容器不删卷，只有 `volume rm` / `prune` 才真正清数据。
- 挂载分两种：命名卷（Docker 管位置，适合持久数据）与绑定挂载（直接指宿主机目录，注意 UID/GID）。
- 清理前先 `system df` 看家底；`prune` 默认不删卷，加 `--volumes` 才是高风险的真正清空。
- `--password-stdin` 登录仓库，避免密码留在命令历史里。

### 下章预告

单个容器的「生老病死」和「周边配套」你已经全会了。但真实项目往往是十几个容器一起跑——逐个 `docker run` 会把人逼疯。下一章进入 Docker Compose，看怎么把这一整套命令写进一个文件、一条命令全部拉起。
