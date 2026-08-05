## 第四章 安装 Docker Compose（v2 plugin 与 standalone）

> 第二、三章把 Docker Engine 全家桶装好了，但如果你当初只零散装了 `docker-ce`，那么 `docker compose` 这个命令还不存在。本章补上 Compose 的两种装法：推荐路线用包管理器装 plugin（`docker compose` 空格命令），兼容路线手动下载 standalone 二进制（`docker-compose` 连字符命令），最后用一张对比表帮你选型。

### 一、先分清两种 Compose：plugin 与 standalone

Docker Compose 从 v2 开始有**两种存在形态**，命令也长得不一样：

- **Compose v2 plugin（插件）**：作为 Docker CLI 的插件安装，命令是 `docker compose`（**空格**）。它随 Docker 官方软件源一起分发，用 `apt` / `dnf` 就能装，升级交给包管理器。
- **standalone 二进制（独立程序）**：一个独立的可执行文件，命令是 `docker-compose`（**连字符**）。需要从 GitHub 手动下载，升级要自己重新下载覆盖。

一句话记住：**空格是 plugin，连字符是 standalone**。两者可以同时存在、互不干扰，但安装方式、升级方式完全不同，选错路会多踩很多坑 [Docker Compose install (Linux)](https://docs.docker.com/compose/install/linux/)。

动手之前先确认一个硬性前提：**Engine 版本必须 ≥ 20.10**，否则即使插件装好，`docker compose` 也会报 `docker: 'compose' is not a docker command`。第二、三章装的是 2026 新版引擎（29.x），远超要求，这步只是例行确认：

```bash
docker version --format '{{.Server.Version}}'
# 输出形如 29.7.1，只要 ≥ 20.10 就满足 Compose v2 的要求
```

> [!note] 别慌：你大概率已经装好 plugin 了
> 第一、二、三章的"全家桶"里已经包含 `docker-compose-plugin` 这个包。如果当时是一次装齐的，第二节可以直接跳过，从验证看起。本节给没走全家桶、或想单独补装的人准备。

### 二、方式 A：Compose v2 plugin（推荐）

plugin 方式的精髓在于：**它走的还是第二、三章配好的 docker-ce 软件源（阿里云），不是 GitHub**。所以国内服务器装 Compose 的最省心做法，就是让包管理器从已配置的源里拉 `docker-compose-plugin` 这个包 [Docker Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)：

```bash
# Ubuntu/Debian（apt 系）
sudo apt-get update && sudo apt-get install docker-compose-plugin

# CentOS/RHEL/Rocky/Alma（dnf 系；CentOS 7 用 yum）
sudo yum update && sudo yum install docker-compose-plugin
```

- 这条命令不会去碰 GitHub，全部流量走你第二、三章配好的阿里云软件源，速度有保障。
- 安装时默认装**最新版**；2026-08 实测最新是 Compose v5.4.0。
- 装好后插件会被放到 Docker CLI 的插件目录，`docker` 命令启动时自动发现它，不需要任何额外配置。

装完立刻验证：

```bash
docker compose version
# 预期输出（版本号随仓库更新）：
# Docker Compose version v5.4.0
```

> [!tip] 为什么 plugin 是官方推荐
> 它和 Docker 引擎同一套软件源、同一套升级节奏。以后 `apt update` / `dnf update` 时 Compose 跟着自动升级，不用惦记"要不要手动更新"。这正符合第一章"全家桶统一管理"的思路。

### 三、方式 B：standalone 二进制（兼容用）

什么时候才需要 standalone？典型场景：老脚本里写死了 `docker-compose` 连字符命令、不想动软件源、或者目标机器压根没配 docker-ce 源。它就是一个单文件二进制，放到 `/usr/local/bin` 即可 [Docker Compose install (standalone)](https://docs.docker.com/compose/install/standalone/)：

```bash
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

- `-SL`：`-S` 出错时显示错误信息，`-L` 跟随 GitHub 的重定向跳转，两者组合是下载二进制文件的标准姿势。
- 下载文件名里的**架构后缀**必须和第一章体检的 `uname -m` 对得上，三选一：

| 架构后缀 | 对应 `uname -m` | 适用机器 |
|---------|----------------|---------|
| `x86_64` | `x86_64` | 绝大多数 x86 服务器 |
| `aarch64` | `aarch64` | ARM64 服务器（如阿里云 ARM 实例、树莓派 4/5） |
| `armv7` | `armv7l` | 32 位 ARM（树莓派 3 及更早、部分老 ARM 板） |

拿 x86 服务器去下 `aarch64` 的文件，执行时只会得到 `Exec format error`，不会有什么友好提示。第一、三章里出现过 `docker-ce.x86_64` 这种写法，这里的架构判断逻辑一致。

> [!warning] 连字符与空格是两套命令
> standalone 装在 `/usr/local/bin/docker-compose` 只提供 `docker-compose`（连字符）。`docker compose`（空格）是 plugin 的专属命令，两者互不替代。装了 standalone 后仍想用空格命令，要么再装 plugin，要么把二进制放进 CLI 插件目录——后者属于进阶玩法，本教程不展开。

### 四、国内下载加速：ghproxy 前缀与本地下载 + scp

standalone 的唯一痛点就是 GitHub 下载慢。两种常见加速方案，按稳定性从低到高排列：

**方案一：ghproxy 类前缀代理（快，但不稳定）**

在原始 URL 前拼一个代理域名即可：

```bash
sudo curl -SL "https://ghproxy.net/https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

> [!warning] ghproxy 公共代理 2026 普遍不稳定
> `ghproxy.net` 这类公共加速域名时有变动、限速甚至关停，实测可用性波动很大。**不要在脚本或文档里硬编码单个 ghproxy 域名**，万一失效整条命令就废了。如果一定要用，优先选自己维护的镜像或时效性强的聚合列表。

**方案二：本地下载 + scp 上传（最稳，推荐）**

在一台能顺畅访问 GitHub 的机器（比如你的笔记本、或带代理的电脑）上下载好二进制，再用 `scp` 传到服务器。流程三步：

```bash
# ① 本地机器下载（Windows PowerShell / macOS / Linux 都行）
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o docker-compose

# ② 上传到服务器，把 root 和 IP 换成你自己的
scp ./docker-compose root@<服务器IP>:/tmp/

# ③ 服务器上移动到位并赋可执行权限
sudo mv /tmp/docker-compose /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- 优点：下载走你本地最快的网络，服务器只做一次 `mv`，几乎不占用带宽。
- `scp` 需要服务器开 SSH 且你有登录权限，一般买服务器后都具备。
- 文件校验可选：下载页标注了 SHA256，`sha256sum docker-compose` 比对一致更保险。

> [!tip] 两种方案怎么选
> 图省事、一次性使用选 ghproxy；长期维护、脚本自动化选本地下载 + scp（或自建反代）。2026 年公共 ghproxy 的不确定性，让"绕开 GitHub"本身成了最大的稳定性来源。

### 五、plugin vs standalone：一张表看懂选型

两种方式核心差异对比如下：

| 维度 | Compose v2 plugin（推荐） | standalone 二进制（兼容） |
|------|---------------------------|---------------------------|
| 命令形态 | `docker compose`（空格） | `docker-compose`（连字符） |
| 安装方式 | `apt` / `dnf` 装 `docker-compose-plugin`，走软件源 | 从 GitHub 下载单个二进制到 `/usr/local/bin` |
| 升级方式 | 包管理器自动升级 | 手动重新下载覆盖 |
| 网络依赖 | 国内阿里云源直连，绕开 GitHub | 依赖 GitHub，需 ghproxy 或本地 + scp 加速 |
| 官方定位 | 推荐、标准路线 | 仅为向后兼容保留 |
| 适用场景 | 新装、长期维护、脚本统一 | 老脚本兼容、不想动软件源 |

> [!tip] 选型一句话
> 新服务器一律走 plugin；只有当你手上的脚本、CI 配置、教程写死了 `docker-compose` 连字符命令，才需要额外装一个 standalone。两者不冲突，完全可以共存。

### 六、验证与版本检查

无论走哪种方式，最后用版本命令收尾：

```bash
# plugin 方式（空格）
docker compose version

# standalone 方式（连字符，若装了）
docker-compose version
```

预期输出：

```
Docker Compose version v5.4.0
```

看到版本号即安装成功。如果 `docker compose version` 报：

```
docker: 'compose' is not a docker command
```

说明 Docker CLI 没有找到 Compose 插件。最常见两类原因：

- **plugin 没装上**：`apt list --installed | grep docker-compose-plugin`（apt 系）或 `rpm -qa | grep docker-compose-plugin`（dnf 系）确认包是否存在，没有就回到第二节补装。
- **Engine 版本 < 20.10**：用第一节的 `docker version --format '{{.Server.Version}}'` 复核。

> [!note] 更完整的排查在第七章
> 插件装了却识别不了，还可能是插件二进制路径问题（比如被装到 `/usr/libexec/docker/cli-plugins/` 时非 root 用户不识别）。这类细节放**第七章坑 ④**统一讲，这里先记住：命令找不到，先查包是否在、再查版本是否达标。

### 本章小结

- 两种 Compose 形态靠命令区分：`docker compose`（空格）是 plugin，`docker-compose`（连字符）是 standalone。
- plugin 是推荐路线：`sudo apt-get install docker-compose-plugin` / `sudo yum install docker-compose-plugin`，走阿里云软件源完全绕开 GitHub，升级交给包管理器。
- standalone 是兼容路线：GitHub 下载单文件到 `/usr/local/bin/docker-compose`，架构后缀要选对（`x86_64` / `aarch64` / `armv7`）。
- 国内下载 standalone 的加速方案：ghproxy 前缀代理（快但不稳定）与本地下载 + scp（最稳），不要硬编码单个 ghproxy 域名。
- Engine 必须 ≥ 20.10；`docker compose version` 看到 `Docker Compose version v5.x` 即安装成功，报 `docker: 'compose' is not a docker command` 时先查包再查版本。

Engine 和 Compose 都就位了，下一步解决"拉镜像慢"——进入**第五章**配置国内镜像加速（registry-mirrors）。
