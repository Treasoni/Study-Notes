---
title: Docker 与 Docker Compose 安装（国内环境）
tags: [docker, linux, 安装指南, 国内网络, docker-compose, 镜像加速]
created: 2026-08-03
updated: 2026-08-04
status: 已完成
source_project: docker-compose-linux-install
---

# Docker 与 Docker Compose 安装（国内环境）

> [!info] 概述
> 一份面向**国内网络环境**的 Docker 与 Docker Compose 安装实战教程，覆盖 Ubuntu/Debian（apt）与 CentOS/RHEL（dnf/yum）双轨。从环境检查、阿里云软件源安装、Compose 插件配置，到 2026 镜像加速与常见坑排查，一站到位。

## 目录

1. 第一章：安装前准备——环境检查与方案选型
2. 第二章：安装 Docker Engine——apt（Ubuntu/Debian）
3. 第三章：安装 Docker Engine——dnf/yum（CentOS/RHEL）
4. 第四章：安装 Docker Compose（v2 plugin 与 standalone）
5. 第五章：配置国内镜像加速（registry-mirrors）
6. 第六章：安装验证与基础检查
7. 第七章：常见坑与排查（避坑手册）
8. 第八章：速查附录

---

## 第一章 安装前准备——环境检查与方案选型

> 安装 Docker 最怕的不是命令记不住，而是装到一半才发现内核版本不对、架构不匹配，或者服务器上还残留着旧版本互相打架。本章先用 5 分钟做一次"系统体检"，再统一认识我们要装的是一套怎样的"全家桶"，并确定自己该走哪条安装轨道。

### 一、先判断走哪条轨道：apt 系还是 dnf 系

服务器上的发行版分成两大家族：Ubuntu/Debian 用 `apt`，CentOS/RHEL/Rocky/Alma 用 `dnf`（CentOS 7 用 `yum`）。两条轨道的包管理命令不同，但装出来的 Docker 是一模一样的。先识别你的发行版：

```bash
cat /etc/os-release
```

看输出里的 `ID` 和 `VERSION_ID` 字段：

- `ID=ubuntu` 或 `ID=debian` → 走 **apt 系**，对应本笔记第二章
- `ID=centos`、`ID=rhel`、`ID=rocky` 或 `ID=alma` → 走 **dnf/yum 系**，对应本笔记第三章

两条轨道的差异见下表：

| 维度 | apt 系 | dnf/yum 系 |
|------|--------|------------|
| 适用发行版 | Ubuntu、Debian | CentOS、RHEL、Rocky、Alma |
| 包管理器 | `apt` / `apt-get` | `dnf`（CentOS 7 用 `yum`） |
| 对应章节 | 第二章 | 第三章 |
| 阿里云软件源路径 | `.../docker-ce/linux/ubuntu` 或 `.../linux/debian` | `.../docker-ce/linux/centos` |
| 典型内核 | 5.x（Ubuntu 20.04+） | 3.10 到 5.x 不等 |

> [!tip] 不用纠结选哪条
> 两条轨道装出来的 Docker 完全一致，区别只在包管理命令和仓库地址。你只需要选**你自己的发行版**对应的那一条，照做即可。

### 二、系统体检：内核、架构与权限

Docker 要求 64 位系统。无论哪条轨道，先跑一遍这三条：

```bash
uname -r                        # 内核版本，如 5.15.0-91-generic
dpkg --print-architecture       # Debian/Ubuntu 查架构，应输出 amd64（或 arm64）
uname -m                        # 通用查架构，应输出 x86_64（或 aarch64）
```

- **架构必须是 64 位**：x86 服务器 `uname -m` 输出 `x86_64`（Ubuntu 里 `dpkg` 对应 `amd64`），ARM 服务器输出 `aarch64`（对应 `arm64`）。若输出 `i686` / `i386`，说明是 32 位系统，无法安装现代 Docker。
- **内核版本**：官方文档给出的最低要求是 3.10，但那已是老黄历。2026 年主流发行版内核普遍 5.x，只要你的系统还能正常 `apt update` / `dnf update`，内核基本不是瓶颈 [Docker Engine install (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)。

> [!warning] 内核太老的两个典型表现
> 装好 Docker 后启动报错 `unsupported ... 3.x`，或出现网络告警 `bridge-nf-call-iptables is disabled`。遇到这些再回来翻第七章的排查。

再确认权限。安装全程需要 root 或 sudo：

```bash
whoami            # 输出 root 表示当前就是 root
sudo -v           # 有 sudo 权限时，输入密码后静默通过
```

> [!tip] 有 sudo 就够了
> 服务器上不建议一直用 root 干活，但安装阶段有 sudo 权限即可。后续章节所有命令都带 `sudo`，如果你的用户没有 sudo，安装会在第一步就失败。

### 三、清理旧版本，避免冲突

如果服务器之前装过 Docker——比如发行版自带的 `docker.io`、老版 `docker-engine`，或手动装过的 `docker-ce`——不清理直接装新版，轻则 `docker` 命令被旧版覆盖，重则 `dockerd` 启动时报错。先检查是否存在旧包：

```bash
# Debian/Ubuntu
dpkg -l | grep -E 'docker|containerd' || echo "无残留"

# CentOS/RHEL/Rocky/Alma
rpm -qa | grep -E 'docker|containerd' || echo "无残留"
```

有输出就卸载（这些包与 docker-ce 的路径冲突）：

```bash
# Debian/Ubuntu
sudo apt remove docker docker-engine docker.io containerd runc

# CentOS/RHEL/Rocky/Alma
sudo yum remove docker docker-client docker-client-latest docker-common \
  docker-latest docker-latest-logrotate docker-logrotate docker-engine
```

> [!warning] 卸载不会删除已有数据
> `remove` 只删软件包，`/var/lib/docker` 里的镜像、容器、数据卷都会保留。升级场景放心卸载；只有确认旧数据没用了，才需要手动 `rm -rf /var/lib/docker`。

### 四、统一安装路径：一次装齐全家桶

无论 apt 还是 dnf，安装命令里的包清单是**完全一致**的"全家桶"：

```bash
# 概念演示，具体安装命令见第二 / 三章
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

这个全家桶由 5 个包组成，各司其职：

| 包名 | 作用 | 类比 |
|------|------|------|
| `docker-ce` | Docker 引擎核心（dockerd 守护进程） | 厨房里的炉灶 |
| `docker-ce-cli` | `docker` 命令行客户端 | 厨师手里的菜刀 |
| `containerd.io` | 容器运行时（真正跑容器的那层） | 洗菜备菜的小工 |
| `docker-buildx-plugin` | 多架构镜像构建插件 | 多功能炒锅 |
| `docker-compose-plugin` | Compose v2 插件（`docker compose` 空格命令） | 摆好整桌菜的传菜员 |

> 🎯 比喻
> 装 Docker 别像"单点外卖"只装一个 `docker-ce`。全家桶一次装齐，等于拿到一整套完整厨房；缺了 compose 插件，第四章要用的 `docker compose` 命令就会报 `docker: 'compose' is not a docker command`（详见第七章坑 ④）。

为什么坚持"全家桶"：5 个包来自**同一个软件源**（阿里云 docker-ce 镜像源），由包管理器统一管理版本、统一升级，完全绕开 GitHub 手动下载 [Docker Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)。这是后续第二、三章安装命令的固定套路，也是本笔记推荐的唯一安装路径。

### 本章小结

- 先 `cat /etc/os-release` 认亲：Ubuntu/Debian 走 apt，CentOS/RHEL/Rocky/Alma 走 dnf/yum，双轨命令不同但装出来的 Docker 一致。
- 体检三步走：`uname -r` 看内核、`uname -m` / `dpkg --print-architecture` 确认 64 位、`sudo -v` 确认权限。
- 安装前清掉旧包（`docker.io`、`docker-engine`、旧版 `docker-ce`），卸载不会丢 `/var/lib/docker` 里的数据。
- 记住全家桶 5 件套：`docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`，apt 和 dnf 通用。
- 全家桶统一走阿里云软件源，一次装齐引擎 + 客户端 + 运行时 + buildx + compose，后续逐章展开。

下一章按轨道分头行动：Ubuntu/Debian 的读者翻到**第二章**用 apt 装引擎，CentOS/RHEL 的读者直接跳**第三章**。

---

## 第二章 安装 Docker Engine——apt（Ubuntu/Debian）

> 第一章完成了系统体检，认定自己是 apt 轨道。本章把 Ubuntu/Debian 用户的主轨道一次走完：通过阿里云软件源，用 apt 把 Docker Engine 全家桶装到服务器上。装完后 `docker` 命令即可使用；镜像加速与 hello-world 完整验证分别留到第五、六章。

### 一、安装前置依赖：ca-certificates / curl / gnupg

apt 要读取一个 HTTPS 软件源，背后需要三件工具：`curl` 负责下载 GPG 密钥，`gnupg` 负责处理密钥文件，`ca-certificates` 提供 HTTPS 证书链——否则 apt 访问阿里云时可能报证书错误。先装齐：

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
```

- `ca-certificates`：系统信任的根证书集合。最小化安装的服务器很可能没有它，装上才不至于后续全部 404/证书报错。
- `curl`：下一步下载 GPG 密钥要用。
- `gnupg`：提供 `gpg` 命令，用来校验和转换密钥。
- `-y`：跳过"是否继续"确认，脚本化安装必备。

> [!tip] 提示
> 如果输出提示某些包"已经是最新版本"，属正常现象。这一步只是保证"用的时候都有"，不是每次都有更新。

### 二、添加 Docker GPG 密钥：apt 只信任签名过的包

软件源里的每个包都带签名。apt 需要一把 GPG 公钥来验证签名，否则会拒绝安装。把密钥下载到专用目录：

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

逐步解释：

- `install -m 0755 -d /etc/apt/keyrings`：创建密钥目录，权限 0755（root 可写、所有人可读）。`/etc/apt/keyrings` 是各发行版约定俗成的密钥存放位置。
- `curl -fsSL ... | sudo gpg --dearmor -o ...`：`-fsSL` 表示静默、跟随重定向下载；`gpg --dearmor` 把 ASCII 文本公钥转成二进制 `.gpg` 文件。下载源直接用阿里云而非官方 `download.docker.com`，保证国内直连速度 [阿里云 docker-ce 镜像帮助页](https://developer.aliyun.com/mirror/docker-ce)。
- `chmod a+r`：apt 内部会以非 root 的 `_apt` 用户读取密钥，密钥必须对所有用户可读，否则 `apt update` 会报密钥权限相关错误。

> [!warning] 密钥本身不是"信任的来源"
> 这把 GPG 公钥是 Docker 官方公钥，从阿里云下载和从官网下载内容一致，区别只在下载速度。若你偏好完全官方渠道，把 URL 换成 `https://download.docker.com/linux/ubuntu/gpg` 即可 [Docker Engine install (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)。

### 三、写入 apt 源：deb822 格式 `docker.sources`（推荐）

apt 软件源文件放在 `/etc/apt/sources.list.d/` 目录下。新版 apt（Ubuntu 20.04 / Debian 11 起均支持）推荐使用 deb822 多行格式，文件后缀为 `.sources`：

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://mirrors.aliyun.com/docker-ce/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.gpg
EOF
```

这段 heredoc 里两个 `$(...)` 会在粘贴执行时被 shell 自动替换成你机器的真实值：

- `Suites`：系统代号。Ubuntu 24.04 → `noble`、22.04 → `jammy`；Debian 12 → `bookworm`。写法 `${UBUNTU_CODENAME:-$VERSION_CODENAME}` 的意思是"优先取 `UBUNTU_CODENAME`，取不到就回退到 `VERSION_CODENAME`"，一句话同时兼容 Ubuntu 和 Debian。
- `Architectures`：第一章体检得到的架构（`amd64` / `arm64`），防止 apt 去抓无关架构的包。

写入后先看一眼内容，确认两个字段已被替换成真实值：

```bash
cat /etc/apt/sources.list.d/docker.sources
```

### 四、兼容写法：传统 `docker.list`（deb 一行式）

如果你更习惯旧格式，或需要贴到老环境的脚本里，也可以写成传统 deb 一行式。效果与 deb822 完全等价，二选一即可：

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

把这一行 `deb` 拆开看，结构一目了然：

| 字段 | 含义 | 示例 |
|------|------|------|
| `[arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg]` | 架构限制 + 指定验签密钥 | `[arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg]` |
| 仓库地址 | 阿里云 docker-ce 软件源 | `https://mirrors.aliyun.com/docker-ce/linux/ubuntu` |
| 套件 | 发行版代号 + 组件 | `noble stable` |

> [!tip] 两种写法怎么选
> 新服务器用 deb822（`.sources`）是官方推荐，字段可读、后续改起来清晰；`.list` 是长期兼容写法，网上老教程大多是这个格式。**二选一写入即可**，不要两个文件同时写同一仓库，否则 `apt update` 会重复加载该源并报警告。

### 五、apt update 并安装全家桶

源写入后必须刷新包索引，apt 才能看到新仓库里的 docker-ce：

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- `apt-get update`：从刚配置的 docker 源拉取包列表。若输出里出现 `.../docker-ce/...` 相关行，说明源已生效。
- 安装的 5 个包就是第一章的"全家桶"：引擎、CLI、运行时、buildx、compose 插件一次装齐，全部来自阿里云软件源，由包管理器统一管理版本与升级，完全绕开 GitHub [Docker Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)。

> [!warning] 全家桶缺一不可
> 只装 `docker-ce` 会漏掉 compose 插件，后面用 `docker compose` 时就会报 `docker: 'compose' is not a docker command`（第七章坑 ④）。全家桶正是为了不踩这个坑。

装完可以先快速确认守护进程已在运行：

```bash
sudo systemctl status docker --no-pager | head -n 5
```

Debian 系的安装包在安装脚本里会自动把 `docker` 服务启用并启动；`hello-world` 的完整验证放在第六章，这里不展开。

### 六、阿里云 ECS 专属：走 VPC 内网源更快

如果你的服务器是阿里云 ECS 且位于 VPC 内网，可以把仓库地址换成内网域名 `mirrors.cloud.aliyuncs.com`。它走阿里云内网流量，不占用公网带宽，速度更快 [阿里云 ECS 安装文档](https://www.alibabacloud.com/help/zh/ecs/user-guide/install-and-use-docker)。注意：**该域名只在阿里云 ECS 内网可达**，本地或其他厂商的机器无法使用。

换源只需把已写入文件里的 URL 前缀替换掉（以 deb822 为例）：

```bash
sudo sed -i 's#https://mirrors.aliyun.com/docker-ce#http://mirrors.cloud.aliyuncs.com/docker-ce#' /etc/apt/sources.list.d/docker.sources
sudo apt-get update
```

> [!tip] 判断自己的 ECS 能不能用内网源
> 在 ECS 上执行 `curl -I http://mirrors.cloud.aliyuncs.com` 能通就说明可用；不通就继续用公网源 `mirrors.aliyun.com`。`sed` 里用 `#` 作分隔符，是为了避免转义 URL 中大量的 `/`。

### 七、指定版本安装：apt-cache madison

生产环境往往需要锁定版本（例如与集群环境对齐）。先列出仓库里所有可选版本：

```bash
apt-cache madison docker-ce
```

输出形如：

```
docker-ce | 5:29.7.1-1~ubuntu.24.04~noble | https://mirrors.aliyun.com/docker-ce/linux/ubuntu noble/stable amd64 Packages
docker-ce | 5:29.6.0-1~ubuntu.24.04~noble | https://mirrors.aliyun.com/docker-ce/linux/ubuntu noble/stable amd64 Packages
```

> [!note] 版本号格式解读
> 版本 `5:29.7.1-1~ubuntu.24.04~noble` 由四段组成：`5:` 是 epoch（Docker 的版本升级机制），`29.7.1` 是 Docker 引擎版本，`-1` 是打包修订号，`~ubuntu.24.04~noble` 标记目标发行版。因为带 epoch，**指定版本时必须连 `5:` 一起写**，否则 apt 找不到该版本。

安装指定版本时，`docker-ce` 与 `docker-ce-cli` 要指定**同一个版本**，避免客户端与守护进程版本错位：

```bash
sudo apt-get install -y docker-ce=5:29.7.1-1~ubuntu.24.04~noble \
  docker-ce-cli=5:29.7.1-1~ubuntu.24.04~noble \
  containerd.io docker-buildx-plugin docker-compose-plugin
```

> [!warning] 指定版本不等于永久锁版
> `install docker-ce=<版本>` 只装这一版。之后执行 `sudo apt-get upgrade` 时 docker 仍可能被升到新版本。要彻底锁版还需 `sudo apt-mark hold docker-ce`（第八章速查会收录）。

### 八、Debian 的 URL 与 Suites 差异

前面命令里凡是 Ubuntu 路径，Debian 用户都要改两处——但只改这两处就够了：

| 维度 | Ubuntu | Debian |
|------|--------|--------|
| URL 路径 | `.../linux/ubuntu` | `.../linux/debian` |
| 代号变量 | `${UBUNTU_CODENAME:-$VERSION_CODENAME}` | `$VERSION_CODENAME` |
| 典型代号 | `noble`(24.04)、`jammy`(22.04)、`focal`(20.04) | `trixie`(13)、`bookworm`(12)、`bullseye`(11) |

- URL：把 `https://mirrors.aliyun.com/docker-ce/linux/ubuntu` 里的 `ubuntu` 改成 `debian`。
- 代号：Debian 的 `/etc/os-release` 里没有 `UBUNTU_CODENAME`，只有 `VERSION_CODENAME`。前面 deb822 命令里写 `echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}"` 正是为了让**同一段命令两边通用**——Ubuntu 取前者，Debian 自动回退后者 [Docker Engine install (Debian)](https://docs.docker.com/engine/install/debian/)。

> [!tip] 装错源的最快识别
> 如果 `apt-get update` 报 404，多半是 URL 路径（`ubuntu`/`debian`）与 Suites 代号对不上。先 `cat /etc/os-release` 看真实代号，再对照上面的表格。

### 本章小结

- apt 轨道三步走：装前置依赖（`ca-certificates curl gnupg`）→ 导入 GPG 密钥到 `/etc/apt/keyrings/` → 写入软件源并 `apt-get update`。
- 软件源推荐 deb822 格式 `docker.sources`；老教程的 `docker.list` 一行式写法同样可用，两者选一，不要重复写。
- 安装命令就是第一章的全家桶：`docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`，一次装齐并自动升级。
- 阿里云 ECS 用户可把仓库换成内网源 `mirrors.cloud.aliyuncs.com`，更快且免公网；非 ECS 机器不要用。
- 要锁版本就 `apt-cache madison docker-ce` 查可用版本，再 `install docker-ce=<完整版本号>`，`docker-ce-cli` 需同步指定。
- Debian 与 Ubuntu 只在 URL 路径和 Suites 代号两处不同，命令里的变量回退写法让同一段命令两边通用。

Ubuntu/Debian 的引擎装好了，下一步翻**第四章**补上 Compose；CentOS/RHEL 的读者不用看本章，直接翻**第三章**走 dnf/yum 轨道。

---

## 第三章 安装 Docker Engine——dnf/yum（CentOS/RHEL）

> 第一章认定了自己是 CentOS/RHEL 轨道，本章把这条主线一次走完：通过阿里云软件源，用 dnf/yum 把 Docker Engine 全家桶装到服务器上。和第二章的 apt 轨道相比，命令不同但最终装出来的 Docker 完全一致——本章默认你已经读过第一章、做完了系统体检，并且用第一章第三节的命令清理过旧包。

### 一、先分清 yum 还是 dnf：安装前置插件

CentOS/RHEL 家族的包管理命令不是铁板一块：**CentOS 7 和 Stream 8 是真 yum**，RHEL 8 之后的系统（RHEL 8/9/10、Rocky、Alma、CentOS Stream 9）用的是 dnf。两者要装的前置插件也不同：

```bash
# ① CentOS 7 / Stream 8（真 yum）——装 yum-utils，提供 yum-config-manager 命令
sudo yum install -y yum-utils

# ② RHEL 8/9/10、Rocky、Alma、CentOS Stream 9（dnf 系）——装 dnf-plugins-core
sudo dnf install -y dnf-plugins-core
```

- `yum-utils` / `dnf-plugins-core`：给包管理器补上"管理软件源"的子命令。yum 系是 `yum-config-manager`，dnf 系是 `dnf config-manager`。下一步添加 Docker 仓库全靠它，所以必须先装。
- `-y`：跳过"是否继续"确认，脚本化安装必备，和第二章 apt 的 `-y` 同理。

> [!tip] yum 和 dnf 其实是一家
> RHEL 8 起 `yum` 只是 `dnf` 的兼容别名，两条命令可混用。在 CentOS 8 / Stream 8 上 `yum install yum-utils` 也能装（等价于 dnf-utils），命令照抄即可，不必纠结。

### 二、添加阿里云 docker-ce 软件源

前置装好后，用一条命令把 Docker 仓库写进系统。dnf 系用 `dnf config-manager`，CentOS 7 用 `yum-config-manager`，命令结构一样：

```bash
# CentOS 7 / Stream 8（yum 系）
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# RHEL 8/9/10、Rocky、Alma（dnf 系等价写法）
sudo dnf config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

这条 `--add-repo` 做了什么：

- 把 URL 指向的 `.repo` 文件**下载**到 `/etc/yum.repos.d/docker-ce.repo`。
- 文件里用 `$releasever` 变量自动适配系统版本：CentOS 7 解析成 `7`、Rocky 9 解析成 `9`，同一份 repo 文件全家族通用 [Docker Engine install (RHEL)](https://docs.docker.com/engine/install/rhel/)。
- 仓库地址直接用阿里云 `mirrors.aliyun.com`，不走官方 `download.docker.com`，国内直连速度快 [阿里云 docker-ce 镜像帮助页](https://developer.aliyun.com/mirror/docker-ce)。

写入后看一眼文件内容，确认 `baseurl` 和 `gpgkey` 都指向阿里云：

```bash
cat /etc/yum.repos.d/docker-ce.repo
```

输出里应能看到类似这样的段落：

```
[docker-ce-stable]
name=Docker CE Stable - $basearch
baseurl=https://mirrors.aliyun.com/docker-ce/linux/centos/$releasever/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://mirrors.aliyun.com/docker-ce/linux/centos/gpg
```

- `gpgcheck=1`：安装时校验 RPM 签名。想核对签名指纹的话，Docker 官方公钥指纹是 `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`。
- `baseurl` 里的 `$releasever` 不要手动改成数字——让它自己解析，repo 才能跨小版本自动跟随。

> [!warning] 仓库加了不一定立刻生效
> dnf/yum 在安装时会自动加载新仓库，一般不需要手动 `makecache`。但如果后续 `yum install` 报"找不到 docker-ce 包"，先执行 `sudo yum clean all && sudo yum makecache` 重建缓存再试。

### 三、sed 换源备选：官方源 + 一键替换前缀

第二种思路是：先加官方 repo，再用 `sed` 把 URL 前缀批量换成国内镜像。适合两种情况——你更信任官方文件、或者阿里云没有你要的子目录（比如第四章后文说的 RHEL 10 场景）。整体三步：

```bash
# ① 先加官方源
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# ② 一条 sed 把前缀换成阿里云
sudo sed -i 's+https://download.docker.com+https://mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo

# ③ 换源后清一下缓存
sudo dnf clean all && sudo dnf makecache
```

- `sed -i` 的 `s+旧+新+`：用 `+` 作分隔符，避免转义 URL 里大量的 `/`。把 repo 文件里所有 `https://download.docker.com` 原地替换成阿里云前缀。
- 想换清华 TUNA 就把 `+` 后面那段换成 `https://mirrors.tuna.tsinghua.edu.cn/docker-ce` [清华 TUNA docker-ce 帮助页](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)。

> [!tip] 直接 add-repo 与 官方源+sed 二选一
> 多数机器用第二节的"直接 add-repo 阿里云 URL"就够了。sed 方案是备选工具箱，尤其适合阿里云没有对应子目录时先拿官方文件、再统一换前缀。两种方式**只执行其中一种**，不要重复添加同一仓库，否则 `dnf repolist` 会看到两套 docker-ce 源。

### 四、安装全家桶并启动服务

源配好了，安装命令和 apt 轨道**一模一样**——还是第一章那 5 件套：

```bash
# dnf 系（RHEL 8/9/10、Rocky、Alma、CentOS Stream 9）
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# CentOS 7 / Stream 8（yum 系）
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

5 个包各司其职（详见第一章第四节）：引擎、CLI、运行时、buildx、compose 插件一次装齐，全部来自阿里云软件源，包管理器统一管理版本和升级，完全绕开 GitHub [Docker Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)。

装完启用并启动守护进程：

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager | head -n 5
```

- `enable --now`：设置开机自启 + 立即启动，一条命令搞定。CentOS 7 的 systemd 同样支持，不用走老的 `service docker start`。
- 状态输出出现 `Active: active (running)` 即启动成功；`hello-world` 的完整验证在第六章。

> [!warning] RHEL 系依赖坑：container-selinux
> 安装报 `Requires: container-selinux >= 2:2.74` 是 RHEL 系特有的高频问题，根因是 extras 仓库未启用或版本过低。解决办法：`sudo yum-config-manager --enable extras` 后重装 container-selinux，再回头装全家桶。完整排查见**第七章坑 ①**，这里先知道有这回事。

### 五、指定版本安装：yum list --showduplicates

生产环境常需锁定版本（比如与集群对齐）。dnf/yum 查可用版本的命令是 `--showduplicates`：

```bash
# dnf 系
dnf list docker-ce --showduplicates | head -n 20

# CentOS 7（yum 系，带上架构更精确）
yum list docker-ce.x86_64 --showduplicates | head -n 20
```

输出形如：

```
docker-ce.x86_64  3:29.7.1-1.el9  docker-ce-stable
docker-ce.x86_64  3:29.6.0-1.el9  docker-ce-stable
```

> [!note] 版本号格式解读
> `3:29.7.1-1.el9` 由四段组成：`3:` 是 epoch（Docker 的版本升级机制），`29.7.1` 是 Docker 引擎版本，`-1` 是打包修订号，`.el9` 标记目标发行版代（el9 对应 RHEL/Rocky/Alma 9 系）。

安装指定版本时，`docker-ce` 与 `docker-ce-cli` 要指定**同一个版本**，避免客户端与守护进程版本错位：

```bash
sudo dnf install -y docker-ce-3:29.7.1-1.el9 docker-ce-cli-3:29.7.1-1.el9 \
  containerd.io docker-buildx-plugin docker-compose-plugin
```

> [!warning] 指定版本不等于永久锁版
> `install docker-ce-<版本>` 只装这一版。之后 `dnf update` 时 docker 仍可能被升级。要彻底锁版还需 `dnf versionlock docker-ce`（第八章速查会收录），与第二章 apt 轨道的 `apt-mark hold` 对应。

### 六、路径分水岭：linux/centos 还是 linux/rhel

前面所有命令都写死了 `linux/centos/` 路径。但 Docker 官方从 RHEL 10 这一代开始，把 el10 的包放到了 `linux/rhel/` 子目录下。选错路径的直接后果是 `dnf makecache` 报 404 或者仓库里没有可用包 [Docker Engine install (RHEL)](https://docs.docker.com/engine/install/rhel/)。判断规则看下表：

| 系统 / 版本 | 仓库路径 | 说明 |
|------|----------|------|
| CentOS 7 / 8 / 9、CentOS Stream 8 / 9 | `linux/centos/` | `$releasever` 对应 el7/el8/el9 包 |
| Rocky / Alma 8 / 9 | `linux/centos/` | 与 CentOS 同代，el8/el9 包通用 |
| RHEL 8 / 9 | `linux/rhel/`（官方路径） | el8/el9 包与 centos 路径相同，两者皆可 |
| RHEL 10、Rocky / Alma 10、CentOS Stream 10 | `linux/rhel/` | 2025 后新代，不再走 centos 路径 |

- 规则一句话：**el8/el9 的机器用 `linux/centos/`，el10 的机器用 `linux/rhel/`**。
- 新装 RHEL 10 / Rocky 10 时，把第二节命令里的 `linux/centos` 换成 `linux/rhel`：

```bash
# el10 机器（RHEL 10 / Rocky 10 / Alma 10）
sudo dnf config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/rhel/docker-ce.repo

# 若阿里云没有 rhel 子目录（404），改用官方源 + sed 换源，兜底方案：
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo sed -i 's+https://download.docker.com+https://mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
sudo dnf clean all && sudo dnf makecache
```

> [!tip] 不确定走哪条路径时
> 先 `cat /etc/os-release` 看 `VERSION_ID` 和 `REDHAT_SUPPORT_PRODUCT_VERSION`。版本号 9 及以下走 `linux/centos/`，10 及以上走 `linux/rhel/`。装完发现 makecache 404，多半就是路径选错了。

### 七、CentOS 7 EOL 注意事项（vault 源）

CentOS 7 已于 **2024-06-30 生命周期结束（EOL）**。2026 年再装 CentOS 7，第一个障碍不是 Docker 而是系统本身：默认仓库的 `mirrorlist` 指向的镜像站点已下线，`yum` 会连不上源。装 Docker 前先把系统源切到归档仓库 vault：

```bash
# 把默认仓库从已失效的 mirror 切到 vault 归档源
sudo sed -i 's/mirrorlist=/#mirrorlist=/g; s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo
sudo yum clean all && sudo yum makecache
```

- 原理：`s/mirrorlist=/#mirrorlist=/g` 注释掉 mirrorlist 行，`s|#baseurl=...|baseurl=...|g` 取消注释并把地址改成 `vault.centos.org` 归档路径。
- vault 只保存**安全更新**，不再有新增软件包；Docker 仓库本身不受影响，但系统基础包不再更新。

两个额外的 EOL 坑：

- **container-selinux 依赖**：CentOS 7 的 extras 仓库切到 vault 后仍需手动启用，否则全家桶装到一半会卡在 `Requires: container-selinux >= 2:2.74`（第七章坑 ①）。
- **7.6 以下旧基线**：装 Docker 前先 `sudo yum update` 把系统升到 7.9，老基线上依赖反复失败的概率很高。

> [!warning] 2026 年新装机器不推荐 CentOS 7
> EOL 系统没有安全更新，装 Docker 只是勉强可用。新服务器优先选 CentOS Stream 9、Rocky 9（或直接上 Rocky 10 走 `linux/rhel/` 路径），本教程所有 dnf 命令都能照常使用。

### 本章小结

- 前置插件：CentOS 7 / Stream 8 装 `yum-utils`，RHEL 8+、Rocky、Alma 装 `dnf-plugins-core`；一个提供 `yum-config-manager`，一个提供 `dnf config-manager`。
- 添加仓库首选 `--add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo`；备选是官方源 + `sed 's+https://download.docker.com+https://mirrors.aliyun.com/docker-ce+'` 一键换前缀。
- 全家桶命令与 apt 轨道完全一致：`docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`，装完 `systemctl enable --now docker` 启动。
- 锁版本用 `yum list docker-ce.x86_64 --showduplicates`（或 `dnf list docker-ce --showduplicates`），`docker-ce` 与 `docker-ce-cli` 必须指定同一版本。
- 路径分水岭：el8/el9 走 `linux/centos/`，el10（RHEL 10 / Rocky 10 / Alma 10）走 `linux/rhel/`，选错会 makecache 404。
- CentOS 7 已 EOL：先 `sed` 切 vault 归档源再装；container-selinux 依赖问题记下"第七章坑 ①"。

dnf/yum 轨道的引擎装好了。接下来和第二、三章的读者在**第四章**汇合——补上 Docker Compose（v2 plugin 与 standalone 两种装法）。

---

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

---

## 第五章 配置国内镜像加速（registry-mirrors）

> 前两章把 Docker 装好了，可一执行 `docker pull nginx` 又开始转圈超时——这不是你装错了，而是 Docker Hub 在国内直连实在太慢。本章通过 `/etc/docker/daemon.json` 配置 `registry-mirrors` 镜像加速，给出 2026 年仍高可用的源与已失效源清单，并讲清加速器的三条边界。

### 一、先认清 registry-mirrors：它给谁加速

Docker 拉镜像的动作是 `dockerd` 守护进程去 registry 下载。`registry-mirrors` 的语义是：**优先从列表里的镜像站尝试下载，失败再回退到官方 Docker Hub**。它不是一个强制代理，而是一份"前置候选名单"。

先分清两个容易混的概念：

- **软件源（装包）**：第一章里配的阿里云 `docker-ce` 软件源，解决的是 `apt install docker-ce` 下载软件包慢的问题。
- **镜像加速器（pull）**：本章配置的 `registry-mirrors`，解决的是 `docker pull` 拉镜像慢的问题。两条路互不相干 [Docker Engine install (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)。

> [!note] 两条边界先记下
> ① `registry-mirrors` **只对 Docker Hub 生效**，拉 `ghcr.io`、`quay.io`、`k8s.gcr.io` 的镜像它帮不上忙（见第七节多仓库代理）。
> ② 加速器是「优先尝试」而非强制：加速器全部超时时，dockerd 会静默回退官方 Hub——**表现为拉取超时，而不是报错**。所以配完必须实测验证（见第五、六节）。

### 二、写入 daemon.json（JSON 语法注意）

`dockerd` 的配置集中在 `/etc/docker/daemon.json`。用 `tee` 写入一份完整配置：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io",
    "https://docker.1panel.live"
  ]
}
EOF
```

- 源列表按 2026 年实测可用性排序（清单见第三节表格），建议放 2-4 个即可，不必全塞。
- heredoc 分隔符写成 `<<'EOF'`（带引号）是为了防止 shell 把内容里的 `$` 当变量展开。这份 JSON 里没有 `$`，但养成带引号的习惯更稳。

JSON 是格式最严格、最容易翻车的部分。写错一个符号，dockerd 可能直接拒绝启动，或者启动后配置不生效。四条铁律：

- **键和字符串必须用双引号**：`"registry-mirrors"`，不能用单引号，也不能裸写 `registry-mirrors`。
- **数组元素之间用逗号，最后一个元素不能带尾逗号**：`[ "a", "b" ]` 合法，`[ "a", "b", ]` 非法。
- **JSON 不支持注释**：不要写 `// 注释` 或 `# 注释`，出现一个注释整份文件就解析失败。
- **整个文件是同一个对象**：如果已有其他键（如 `exec-opts`、`proxies`），要在**同一对大括号内并列**，而不是另开一个对象。

写完先做一次语法自检：

```bash
cat /etc/docker/daemon.json | python3 -m json.tool
```

没有报错、原样输出 JSON，说明语法 OK。报错会直接指出第几行第几个字符，照着修即可。

> [!warning] 文件已存在时不要覆盖
> 如果 `/etc/docker/daemon.json` 已经存在（例如为 K8s 配过 `"exec-opts"`），用 `sudo nano /etc/docker/daemon.json` 打开，在同一个对象里补上 `registry-mirrors` 键，而不是用 `tee` 整体覆盖，否则会把原有配置冲掉。

### 三、2026 年高确认可用源清单

> [!note] 失效是常态，别把清单当长期保证
> 免费镜像加速源受政策与成本影响，停服、限速随时可能发生；2026 年仍大面积失效的老牌高校源见下一节表格 [2026 Docker 国内镜像源指南（腾讯云 2026-07）](https://cloud.tencent.com.cn/developer/article/2647943)。

| 源 | 地址 | 性质 | 说明 |
|------|------|------|------|
| 毫秒镜像 | `https://docker.1ms.run` | 商业/社区 | 高可用；提供 `ghcr`/`k8s`/`quay`/`mcr`/`nvcr` 多仓库前缀（见第七节） |
| 轩辕镜像 | `https://docker.xuanyuan.me` | 社区公益 | 实测速度与成功率俱佳；专业版 `xuanyuan.cloud` 提供多仓库 [轩辕镜像](https://github.com/SeanChang/xuanyuan_docker_proxy) |
| DaoCloud | `https://docker.m.daocloud.io` | 社区公益 | 全协议反代，可拉 `gcr.io` 等 |
| 1Panel | `https://docker.1panel.live` | 官方社区 | 仅限大陆访问；旧地址 `docker.1panel.dev` 已失效 |
| 阿里云个人专属 | `https://<your-id>.mirror.aliyuncs.com` | 云厂商 | 需在容器镜像服务控制台开通后获得专属 ID，最稳定 [2026-08 多仓库源清单（阿里云开发者）](https://developer.aliyun.com/article/1752736) |

阿里云专属源单独说明：登录阿里云容器镜像服务控制台 →「镜像加速器」页面，会给出一个专属地址 `https://<你的专属ID>.mirror.aliyuncs.com`。它绑定你的账号，不限速不限流，比公共源稳定得多；缺点是必须有一个阿里云账号。

### 四、已失效 / 不推荐源清单（避坑）

网上大量老教程（尤其 2023 年前的）还在推这些源，2026 年它们大多已停服或失效，直接照抄只会拉取超时：

| 源 | 现状 | 备注 |
|------|------|------|
| 中科大 `docker.mirrors.ustc.edu.cn` | 已停服 | 2026 确认不可用 |
| 清华 TUNA | 不提供 pull 加速 | 仅镜像 docker-ce **软件包**，无 registry-mirrors |
| 南大 `docker.nju.edu.cn` | 已停服 | — |
| 网易 `hub-mirror.c.163.com` | 已失效 | — |
| `dockerhub.icu` | 证书错误 | — |
| `dockerproxy.cn` | 已关停 | — |
| `dockerpull.com` | DNS 解析失败 | — |
| `docker.mrxn.net` | 返回 502 | — |
| `atomhub.openatom.cn` | 已退役 | 2024-12 停止服务 |
| `docker.1panel.dev` | 已失效 | 迁移到 `docker.1panel.live` |

> [!tip] 怎么判断一个源还活着
> 一条命令测连通：`curl -I https://docker.1ms.run` 返回 `200` / `302` 且能看到响应头，基本可用；超时或 `502 / 403 / 521` 则换源。每月花 10 秒测一次，比临时抓瞎强 [dongyubin/dockerhub（2026-06 实测）](https://github.com/dongyubin/dockerhub)。

### 五、重启 docker 使配置生效

`daemon.json` 是 dockerd 启动时读取的，改完**必须重启守护进程**。正确的两步：

```bash
sudo systemctl daemon-reload   # 重新加载 systemd 单元（防止单元文件缓存）
sudo systemctl restart docker  # 重启 dockerd，读取新 daemon.json
```

`daemon-reload` 单独出现是常见遗漏：它让 systemd 重新扫描单元文件与 drop-in 配置。`restart` 前先跑一次，能避免"明明改了却没生效"的玄学。

验证是否真的读到了：

```bash
docker info | grep -A 5 "Registry Mirrors"
```

预期输出：

```
 Registry Mirrors:
  https://docker.1ms.run/
  https://docker.xuanyuan.me/
  https://docker.m.daocloud.io/
  https://docker.1panel.live/
```

能列出这几行就说明 dockerd 已加载。若这里为空，回头检查 JSON 语法——多半是 `daemon.json` 解析失败被静默忽略了。

### 六、实测速度：time docker pull

配置生效不等于拉取快。加速器是"优先尝试"，只有实测才能确认它真的在为你服务：

```bash
time docker pull nginx:alpine
```

`time` 会在命令结束后打印耗时。首次拉取会下载镜像层，正常应看到 `nginx:alpine` 在几秒到几十秒内完成；如果仍然卡到超时，按这个顺序排查：

1. `docker info | grep -A 5 "Registry Mirrors"` —— 确认加速器真的在列表里；
2. `curl -I <镜像源地址>` —— 确认源还活着；
3. 换个源（见第三节表格）再 `systemctl restart docker`。

> [!warning] pull 失败不一定是配置错了
> 免费源晚高峰（20:00-23:00）可能限速甚至临时抽风，单次失败很常见。多试一两次、或换一个源，再下结论。

### 七、边界一：只对 Docker Hub 生效 —— 多仓库代理怎么拉

`registry-mirrors` 只影响 `docker.io`（Docker Hub）的镜像。遇到 `ghcr.io`、`quay.io`、`k8s.gcr.io`、`mcr.microsoft.com` 的镜像，加速器完全帮不上忙。解决方法是**多仓库代理**：用加速器提供的前缀替换原仓库前缀，拉完再 `docker tag` 改回原名称。

以毫秒源为例，它提供 `ghcr.1ms.run` / `k8s.1ms.run` / `quay.1ms.run` / `mcr.1ms.run` / `nvcr.1ms.run` 五个前缀：

```bash
# 先把原仓库前缀替换成加速器前缀拉取
docker pull docker.1ms.run/library/nginx:alpine   # Docker Hub 的 nginx
docker pull ghcr.1ms.run/owner/myapp:v1           # GitHub Container Registry
docker pull k8s.1ms.run/pause:3.9                 # 曾经的 k8s.gcr.io

# 拉完改回原名称，后续 docker run / compose 用回原名
docker tag docker.1ms.run/library/nginx:alpine nginx:alpine
docker tag ghcr.1ms.run/owner/myapp:v1 ghcr.io/owner/myapp:v1
docker run ghcr.io/owner/myapp:v1
```

要点：

- Docker Hub 镜像经加速器前缀拉取时，官方名称前要补 `library/`（如 `library/nginx`），因为 `docker.1ms.run/nginx:alpine` 会被解析成不存在的 `docker.io/nginx`。
- 非 Hub 镜像拉完**必须 `docker tag` 回原名称**，否则 `docker-compose.yml` 里写的镜像名找不到本地镜像。tag 只是本地改名，不产生网络流量，秒级完成。
- 不同加速器提供的多仓库前缀不一样，用之前先看该源说明；轩辕的专业版 `xuanyuan.cloud` 同样提供多仓库前缀。

> [!note] containerd 不走 daemon.json
> K8s / K3s 节点用的是 containerd 而不是 dockerd，改 `/etc/docker/daemon.json` 无效。那类环境要在 `/etc/containerd/config.toml` 的 `registry.mirrors["docker.io"].endpoint` 里配置，属于另一个话题，本笔记不展开。

### 八、边界二：加速器 ≠ 代理

加速器只对 `docker pull` 一个动作生效；镜像构建（`docker build`）过程里容器内的 `apt install`、`git clone`、`curl` 下载，加速器一律管不着。要解决这些，需要的是**网络代理**——接管全部流量。

> 加速器 vs 代理的概念差异、以及"什么时候该上代理"，本笔记不展开，直接看已有 vault 笔记：[[docker/镜像加速器vs代理-概念对比]]

简版对比：

- **作用范围**：加速器只拦 `docker pull` 一个动作；代理接管全部网络流量（pull、build 里的 apt/git、curl 等）。
- **配置位置**：加速器写在 `daemon.json` 的 `registry-mirrors`；代理可配 systemd drop-in 的 `HTTP_PROXY`，或 `daemon.json` 的 `"proxies"` 键。
- **维护成本**：公共加速器开箱即用；代理一般要自建，稳定但更折腾。
- **适用场景**：只是拉镜像慢 → 加速器；构建时容器内拉依赖、频繁访问 GitHub → 代理。

本笔记只讲 **Linux 服务器**上的 daemon.json 配置；Windows / Mac 桌面版 Docker Desktop 的加速器在 GUI 里配置，原理一致但路径完全不同，见 [[docker/DockerDesktop镜像加速器配置]]。

### 本章小结

- `registry-mirrors` 是 dockerd 拉镜像时的"优先尝试名单"，**只对 Docker Hub 生效**，失败会静默回退官方源——表现为超时而非报错。
- 写 `daemon.json` 记住四条铁律：双引号、无尾逗号、无注释、同一对象并列；写错会被静默忽略或导致 dockerd 拒绝启动。
- 2026 高可用源：毫秒、轩辕、DaoCloud、1Panel、阿里云个人专属；中科大 / 南大 / 网易等老牌源已大面积失效，别照抄老教程。
- 改完必须 `systemctl daemon-reload && systemctl restart docker`，再用 `docker info | grep -A 5 "Registry Mirrors"` 和 `time docker pull` 双重验证。
- 拉 ghcr/k8s/quay 等非 Hub 镜像，用多仓库前缀 + `docker tag` 回原名；加速器不是代理，构建过程的网络问题要靠代理解决。

镜像拉得动了，下一章**第六章**做一次完整的安装验证：跑通 `hello-world`、配好非 root 用户权限、设置开机自启，让环境真正可交付。

---

## 第六章 安装验证与基础检查

> 前面的章节把 Docker 引擎、Compose 插件和镜像加速都装好了，但"装完"和"能用"之间还差最后一道体检。本章用一条条可复制的命令，把 4 件关键事项逐项确认：hello-world 冒烟测试、非 root 用户权限、开机自启、双版本确认。全部通过，你的环境才算真正可用。

### 一、先跑冒烟测试：docker run hello-world

不管你是 apt 系还是 dnf 系装出来的，验证 Docker 是否真正工作，官方标准动作都是跑一次 `hello-world`。它不会启动常驻服务，只是拉下一个极小的测试镜像，跑一个一次性容器打印欢迎信息就退出：

```bash
sudo docker run hello-world
```

预期输出（关键看中间那一段英文说明）：

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

看到 `Hello from Docker!` 这一行，说明引擎能正常拉镜像、能创建容器、容器运行时工作正常，整条链路是通的 [Docker Engine install (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)。

> [!note] 为什么用 hello-world 而不是 nginx
> hello-world 镜像只有几 KB，拉取几乎不耗时，是"最小验证面"。如果这一步在 Pull 阶段卡住超时，说明镜像拉取有问题——先回第五章确认 registry-mirrors 是否生效，而不是急着怀疑引擎。

### 二、让普通用户免 sudo：usermod + newgrp

到目前为止命令都带 `sudo`，因为 Docker 的 socket（`/var/run/docker.sock`）默认属主是 `root:docker`、权限 660——也就是说，只有 root 和 `docker` 组的成员能直接操作 Docker。把当前用户加进 `docker` 组：

```bash
sudo usermod -aG docker $USER
```

**这行命令不会立即生效**，因为你的登录会话还带着旧的用户组。两种方式让它生效：

```bash
# 方式 A：当前会话立即切换（临时，只对当前终端有效）
newgrp docker

# 方式 B：退出服务器重新登录（推荐，永久生效）
# exit 后重新 ssh 登录即可
```

验证是否生效（这次不需要 sudo）：

```bash
docker ps        # 不报 permission denied 即成功
id -nG           # 输出里应包含 docker 这个词
```

`id -nG` 会列出当前用户所属的所有组，看到 `docker` 就说明组已经加上。

> [!warning] 禁止 chmod 666 偷懒
> 有人图省事直接 `sudo chmod 666 /var/run/docker.sock`，以为一次搞定权限。这等于把 Docker 的管理权开放给系统上所有用户，而且重启后权限会被 systemd 还原，属于"既危险又无效"。正确做法就是上面的 usermod + 重新登录，详见第七章坑 ⑤。

### 三、开机自启：systemctl enable --now docker

apt 系在 Debian/Ubuntu 上安装包通常会帮你注册并启动 `docker.service`，但 **RHEL/CentOS/Rocky 系装完默认不启动、也不开机自启**，需要显式设置。`systemctl enable --now` 一条命令同时完成"开机自启"和"立即启动"两件事 [Docker Engine install (RHEL)](https://docs.docker.com/engine/install/rhel/)：

```bash
sudo systemctl enable --now docker
```

预期输出：

```
Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.
```

看到这行 symlink 提示，说明开机自启已建立。就算之前手动 `systemctl start docker` 过，这步也不会重复启动报错，是幂等的，对两条轨道都安全。

### 四、双版本确认：docker version 与 docker compose version

安装版本和运行时状态，用两个命令确认：

```bash
docker version
docker compose version
```

`docker version` 会分 **Client**（客户端）和 **Server**（守护进程）两段输出。关注 Server 段：

```
Server:
  Engine:
    Version:     29.7.1
```

Server 段有版本号，说明客户端能连上守护进程（上一步的 socket 权限也顺带验证了）。如果 Server 段报 `permission denied`，说明第二节的用户组没生效，回去重新登录再看。

`docker compose version` 预期输出 `Docker Compose version v5.x`（2026 年当前为 v5.4.0）。这一步同时验证两件事：compose 插件装上了、CLI 能找到插件路径 [Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)。如果报 `docker: 'compose' is not a docker command`，说明插件没装或路径不对，去查第七章坑 ④。

> [!tip] compose 命令兼容性要求
> 空格版 `docker compose` 需要 Engine ≥ 20.10。2026 年全新安装的 docker-ce 版本都远高于这个门槛，正常不会踩到；只有极老的存量环境才需要额外关注。

### 五、服务状态检查：systemctl status docker

最后确认守护进程本身运行正常：

```bash
systemctl status docker
```

关注第一行状态：

```
● docker.service - Docker Application Container Engine
     Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; preset: enabled)
     Active: active (running) since ...
```

`Active: active (running)` 就是健康状态。两个可快速判断的关键词：**Active 是否 running**（服务在跑）、**Loaded 里是否 enabled**（对应第三节的开机自启）。想在脚本里判断，用下面两条更省心：

```bash
systemctl is-active docker      # 输出 active 即正常
systemctl is-enabled docker     # 输出 enabled 即已设自启
```

### 体检清单速查

把本章全部命令浓缩成一段可复制粘贴的完整清单（hello-world 建议在权限配置完成后再用不带 sudo 的方式跑一遍，双保险）：

```bash
sudo systemctl enable --now docker
docker version && docker compose version
sudo usermod -aG docker $USER && newgrp docker   # 重新登录后生效
docker run hello-world                           # 免 sudo 冒烟测试
systemctl status docker                          # Active: active (running)
```

> [!example] 通过标准
> ① `docker run hello-world` 打印 `Hello from Docker!`；② `docker ps` 免 sudo 直接成功；③ `systemctl is-enabled docker` 输出 `enabled`；④ `docker compose version` 输出 v5.x；⑤ `systemctl is-active docker` 输出 `active`。五条全绿，环境就绪。

### 本章小结

- 冒烟测试用 `docker run hello-world`，看到 `Hello from Docker!` 即证明镜像拉取、容器创建、运行时整条链路正常。
- 免 sudo 靠 `sudo usermod -aG docker $USER` + 重新登录（或 `newgrp docker`），禁止 `chmod 666`（详见第七章坑 ⑤）。
- `systemctl enable --now docker` 一条命令同时搞定启动与开机自启，dnf 系尤其需要显式执行。
- `docker version` 看 Server 段、`docker compose version` 看 v5.x，双命令确认客户端、守护进程与 Compose 插件三者都正常。
- 状态检查认准 `systemctl is-active` 输出 `active`、`systemctl is-enabled` 输出 `enabled`。

环境已确认可用。不过实际运维中总有"装好了但跑不起来"的意外，下一章把 6 个高频坑整理成"现象 → 根因 → 解决"卡片，遇到问题直接对照排查。

---

## 第七章 常见坑与排查（避坑手册）

> 前六章都是"照做就能成"的顺风路，这一章换成"出问题再来看"。安装和配置过程中，90% 的报错都集中在六个高频坑上。本章把它们按「现象 → 根因 → 解决」整理成卡片，遇到问题时先对着下面这张索引表定位，再翻到对应坑照抄修复命令；没遇到就先跳过，等真踩到再回来看。

| 报错关键词 | 对应坑 | 主要影响人群 |
|------|------|------|
| `Requires: container-selinux >= 2:2.74` | 坑 ① | dnf/yum 系（CentOS/RHEL/Rocky/Alma） |
| `bridge-nf-call-iptables is disabled` | 坑 ② | 全部（尤其容器跨主机网络异常时） |
| 配了加速器仍走官方、pull 超时 | 坑 ③ | 配了 registry-mirrors 的用户 |
| `docker: 'compose' is not a docker command` | 坑 ④ | 全部 |
| `permission denied ... /var/run/docker.sock` | 坑 ⑤ | 非 root 用户执行 docker |
| cgroup driver 不一致 | 坑 ⑥ | K8s / kubeadm 用户 |

---

### 坑 ① `Requires: container-selinux >= 2:2.74`——RHEL 系装 docker-ce 报依赖失败

**现象**

第三章用 yum/dnf 安装 docker-ce 时，命令中途中止，末尾跟着一长串依赖错误：

```
错误：软件包：docker-ce-xxx.x86_64
          需要：container-selinux >= 2:2.74
```

明明软件源配置没问题，却因为一个 `container-selinux` 卡住装不上。

**根因**

`container-selinux` 是 RHEL 系提供的一个 SELinux 策略模块，给容器运行时用。Docker 的 rpm 包声明了对它的最低版本要求，而它由 `extras` 仓库提供。装不上通常有两个原因：一是服务器的 `extras` 仓库被禁用（最小化安装或自定义了仓库时常见），二是仓库里 `container-selinux` 版本低于 2:2.74。另外 CentOS 7 已于 2024-06 停止维护（EOL），基础仓库整体挪到了 vault 归档源，不处理的话 yum 直接连不上 [container-selinux 依赖解决](https://segmentfault.com/a/1190000047548761)。

**解决**

先启用 `extras` 仓库，再手动把三个依赖装齐，最后重新安装 docker-ce：

```bash
# yum（CentOS 7 / Stream 8）
sudo yum-config-manager --enable extras
sudo yum install -y container-selinux slirp4netns fuse-overlayfs
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# dnf（RHEL 8/9、Rocky/Alma）
sudo dnf config-manager --set-enabled extras
sudo dnf install -y container-selinux slirp4netns fuse-overlayfs
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

如果提示找不到 `yum-config-manager`，说明缺 `yum-utils`（第三章装过的工具），先补上再执行：

```bash
sudo yum install -y yum-utils
```

> [!warning] CentOS 7 老机器先解决 EOL 源
> 若报错里出现 `Could not resolve host: mirrorlist.centos.org` 或仓库下载失败，说明你的 CentOS 7 还指着已停服的官方源。先把基础仓库指到 vault 归档源，再执行上面的 extras 步骤：
>
> ```bash
> sudo sed -i 's/mirrorlist=/#mirrorlist=/g; s|#baseurl=http://mirror.centos.org/centos|baseurl=http://vault.centos.org/7.9.2009|g' /etc/yum.repos.d/CentOS-Base.repo
> sudo yum clean all && sudo yum makecache
> ```
>
> CentOS 7.6 以下的旧基线在装 container-selinux 时更容易反复依赖失败，这类机器建议直接升级到 Rocky/Alma 9 再装 Docker，不要在 EOL 系统上硬扛。

---

### 坑 ② `bridge-nf-call-iptables is disabled`——网络告警与容器间互通异常

**现象**

启动 docker 或查看日志时出现告警：

```
WARNING: bridge-nf-call-iptables is disabled
```

严重时表现为：同一台宿主机上跨 bridge 网络的容器之间、或容器与外部网络之间连接不通，防火墙规则对 bridge 流量不生效 [moby/moby discussion 48559](https://github.com/moby/moby/discussions/48559)。第一章体检时就提醒过：内核太老或模块未加载时会出现这个告警。

**根因**

Docker 的 bridge 网络要转发、过滤桥接流量，依赖内核模块 `br_netfilter`。这个模块没加载，内核就没有 `net.bridge.bridge-nf-call-iptables` 这个 sysctl 键（或值为 0），iptables 规则就不会作用在 bridge 网桥上。根因是模块没加载，而不是 Docker 配置错。

**解决**

临时生效（当前会话）先加载模块并打开开关：

```bash
sudo modprobe br_netfilter
sudo sysctl -w net.bridge.bridge-nf-call-iptables=1
sudo sysctl -w net.bridge.bridge-nf-call-ip6tables=1
sudo sysctl -w net.ipv4.ip_forward=1
```

只做上面这步，重启就失效了。要持久化，需要写**两个**文件——一个管 sysctl 值、一个管模块开机加载：

```bash
# 1. sysctl 配置：开机把三个开关置 1
sudo tee /etc/sysctl.d/99-bridge.conf <<EOF
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1
EOF

# 2. 模块配置：开机先加载 br_netfilter
echo "br_netfilter" | sudo tee /etc/modules-load.d/br_netfilter.conf
```

> [!warning] 两个文件缺一不可，顺序很关键
> `systemd-modules-load.service` 负责读 `/etc/modules-load.d/` 在开机早期加载模块；而 `systemd-sysctl.service` 负责应用 `/etc/sysctl.d/`。如果只写 `/etc/sysctl.d/99-bridge.conf` 不写 `/etc/modules-load.d/br_netfilter.conf`，开机时 sysctl 先执行、模块还没加载，`net.bridge.*` 这几个键根本不存在，会被静默跳过——结果就是"配置写了，重启后照样告警"。只有模块先加载、键出现，sysctl 值才能写进去。

验证是否真的持久化成功：

```bash
lsmod | grep br_netfilter                # 有输出说明模块已加载
sysctl net.bridge.bridge-nf-call-iptables   # 应输出 = 1
```

---

### 坑 ③ daemon.json 配了镜像源仍走官方——加速器失效的三种假象

**现象**

第五章在 `/etc/docker/daemon.json` 里写好了 `registry-mirrors`，`docker info` 里也能看到加速器列表，但 `docker pull nginx:alpine` 依然慢得离谱或直接超时——仿佛根本没配。

**根因**

加速器是「优先尝试」而非强制代理：Docker 会先按列表顺序尝试每个镜像源，**全部失败（超时/404/证书错误）时自动回退到 Docker Hub 直连**。所以你看到的现象往往是"配了等于没配、最后卡住超时"——其实是加速器本身不可用触发了回退 [2026 Docker 国内镜像源指南](https://cloud.tencent.com.cn/developer/article/2647943)。另外三种常见的"假配置"：daemon.json 有 JSON 语法错误（漏逗号、括号不配对、末尾多逗号）导致 dockerd 忽略配置；改完没重启 daemon；以及把镜像源写错成只对 Docker Hub 生效的范围外的仓库 [腾讯云 镜像源不生效排查](https://cloud.tencent.com.cn/developer/article/2639741)。

**解决**

按下面顺序排——先确认配置合法、再重启、再确认加载、最后测加速器本身通不通：

```bash
# 1. JSON 语法检查：有报错就说明文件写坏了
python3 -m json.tool /etc/docker/daemon.json
# 或：jq . /etc/docker/daemon.json

# 2. 改配置后必须重启（先 daemon-reload 再 restart）
sudo systemctl daemon-reload && sudo systemctl restart docker

# 3. 确认加速器被 dockerd 加载
docker info | grep -A 5 "Registry Mirrors"

# 4. 测加速器本身通不通（能返回 200/301/401 都算通，超时说明源已失效）
curl -I --max-time 5 https://docker.1ms.run/v2/
```

> [!tip] 如果 4 步都正常仍慢，直接换源
> 免费加速器晚高峰（20:00-23:00）可能限速，而且源存活变化快，建议每月实测一次。第五章清单里的高可用源按序多配几个，或换成阿里云专属地址（`https://<your-id>.mirror.aliyuncs.com`）这类最稳定的源。换源后记得回到第 2 步重启。

补充一个边界：`registry-mirrors` **只对 Docker Hub 生效**。拉 `ghcr.io`、`k8s.gcr.io`、`quay.io` 等第三方仓库的镜像走加速器是没用的，这类仓库要么直连、要么用多仓库代理前缀显式拉取（详见第五章）。

---

### 坑 ④ `docker: 'compose' is not a docker command`——compose 命令找不到

**现象**

执行 `docker compose version` 或 `docker compose up` 时报：

```
docker: 'compose' is not a docker command.
See 'docker --help'
```

第二章全家桶明明是"一次装齐"的，为什么还是没有 compose？

**根因**

Compose v2 不是 docker 内置子命令，而是一个 **CLI 插件**。docker 会到固定的插件目录里找名为 `docker-compose` 的可执行文件，找不到就报这个错。常见三种情况：① 装的时候没装 `docker-compose-plugin` 这个包（比如只装了 `docker-ce`）；② 插件装了但路径不对——尤其装在 `/usr/libexec/docker/cli-plugins/` 下时，非 root 用户常识别不到；③ Engine 版本低于 20.10，不支持插件机制 [Docker Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)。

**解决**

按你的情况对号入座：

```bash
# 情况一：没装插件包，走软件源装（推荐，第四章主推路线）
sudo apt-get install -y docker-compose-plugin      # Debian/Ubuntu
sudo yum install -y docker-compose-plugin          # CentOS/RHEL

# 情况二：手动放插件二进制到用户插件目录（任何架构按需替换后缀）
mkdir -p ~/.docker/cli-plugins/
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
  -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

# 情况三：确认 Engine 版本是否 ≥ 20.10
docker version --format '{{.Server.Version}}'
```

装完验证：

```bash
docker compose version
```

> [!note] 插件搜索路径
> docker 会按顺序找这几个目录里的 `docker-compose`：`~/.docker/cli-plugins/`、`/usr/local/lib/docker/cli-plugins/`，以及系统级的 `/usr/libexec/docker/cli-plugins/`。排在前面的用户目录优先级最高。如果你的二进制放到了非 root 系统目录却仍报错，大概率是权限或路径问题——直接放到 `~/.docker/cli-plugins/` 最省心。

另外提醒：standalone 版本命令是连字符 `docker-compose`（第四章兼容路线的产物），它和 `docker compose` 是两个东西，别用混。出现这个报错时如果 `docker-compose version` 反而能通，说明你只装了 standalone、没装 plugin。

---

### 坑 ⑤ `permission denied ... /var/run/docker.sock`——非 root 用户连不上 daemon

**现象**

用普通用户执行 `docker ps` 时报：

```
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "...": dial unix /var/run/docker.sock: connect: permission denied
```

**根因**

Docker daemon 监听在 socket `/var/run/docker.sock` 上，这个文件属主是 `root:docker`、权限 660——只有 root 和 `docker` 组的成员能读写。当前用户既不是 root 也不在 `docker` 组，就被拒之门外。另一个隐蔽情况是：第六章你已经执行过 `sudo usermod -aG docker $USER`，但**当前 SSH 会话的组信息不会自动刷新**，必须重新登录（或 `newgrp`）才生效 [docker.sock 权限问题](https://blog.csdn.net/xiaokai1999/article/details/129861664)。

**解决**

```bash
# 1. 把当前用户加进 docker 组（只需做一次）
sudo usermod -aG docker $USER

# 2. 让组立刻生效（二选一）
newgrp docker
# 或：注销当前 SSH 重新登录（最彻底）

# 3. 验证组已生效
id -nG          # 输出里应包含 docker

# 4. 免 sudo 直接跑
docker ps
```

> [!warning] 严禁 chmod 666
> 网上有教程让你 `sudo chmod 666 /var/run/docker.sock` 一劳永逸。这是错误做法：socket 每次重启 docker 都会重建并恢复权限，所以它根本不持久；更严重的是，**能操作 docker socket 就等于拿到服务器的 root 权限**（容器能挂载宿主目录），把它放开给所有用户等于把服务器交出去。正确姿势永远是把用户加进 `docker` 组，别碰权限位。

---

### 坑 ⑥ cgroup driver 不一致——K8s / kubeadm 场景专属

**现象**

在用 kubeadm 搭的集群节点上，kubelet 起不来，日志里报：

```
failed to run Kubelet: "cgroup driver" is incompatible with "systemd" (kubelet) vs "cgroupfs" (docker)
```

`docker info` 里显示的 Cgroup Driver 是 `cgroupfs`，而 kubelet 用的是 `systemd` [kubernetes/kubeadm issue 2605](https://github.com/kubernetes/kubeadm/issues/2605)。

**根因**

Docker 默认的 cgroup driver 是 `cgroupfs`；而 kubelet（尤其 kubeadm 初始化的集群）官方推荐使用 `systemd`。两者不一致时，kubelet 认为容器运行时不可用，直接启动失败。

**解决**

在 `/etc/docker/daemon.json` 里加一行 `exec-opts`，把 Docker 的 cgroup driver 对齐到 `systemd`，然后重启：

```bash
sudo tee /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
sudo systemctl daemon-reload && sudo systemctl restart docker
docker info | grep -i cgroup
# 预期输出：Cgroup Driver: systemd
```

> [!warning] daemon.json 若已有内容，要合并不要覆盖
> 如果你第五章已经配了 `registry-mirrors`，直接 `tee` 整文件会把加速器覆盖掉。要么用文本编辑器把两段拼一起，要么用 jq 合并：
>
> ```bash
> sudo apt install -y jq   # 或：sudo yum install -y jq
> sudo jq '. + { "exec-opts": ["native.cgroupdriver=systemd"] }' \
>   /etc/docker/daemon.json | sudo tee /tmp/daemon.json.tmp
> sudo mv /tmp/daemon.json.tmp /etc/docker/daemon.json
> sudo systemctl daemon-reload && sudo systemctl restart docker
> ```
>
> 合并后的文件应该同时包含 `registry-mirrors` 和 `exec-opts`，写完后务必用坑 ③ 的 `python3 -m json.tool` 检查一遍。

> [!note] 2026 年更推荐直接上 containerd
> Kubernetes 1.24+ 已彻底移除 dockershim，Docker 不再作为官方支持的容器运行时。新集群建议直接以 containerd 作为运行时，在 `/etc/containerd/config.toml` 里同样把 cgroup driver 对齐到 `systemd`，就完全绕开了"和 Docker 对齐"这一步。本笔记只讲安装不展开 K8s，这里知道方向即可。

---

### 附加：镜像加速器失效的排查顺序

踩到"拉镜像慢/超时"时，别急着怀疑系统，按固定顺序走一遍，基本能定位到是"没配好"还是"源挂了" [dongyubin/dockerhub 镜像源清单](https://github.com/dongyubin/dockerhub)：

```bash
# ① 看加速器有没有被 dockerd 加载
docker info | grep -A 5 "Registry Mirrors"

# ② 测加速器本身通不通（能返回 HTTP 状态码说明可用，超时说明源已失效）
curl -I --max-time 5 https://docker.1ms.run/v2/

# ③ 实测拉取速度，心里有个数
time docker pull nginx:alpine

# ④ 换源后记得重启再验证
sudo systemctl daemon-reload && sudo systemctl restart docker
docker info | grep -A 5 "Registry Mirrors"
```

判断逻辑：① 没输出 → 回到坑 ③ 检查 daemon.json 与重启；② 超时 → 源挂了，直接换第五章清单里的备选源；② 正常但 ③ 仍慢 → 晚高峰限速或网络问题，换更稳的源（如阿里云专属）再试。加速器 ≠ 代理，它只影响 `docker pull`；如果容器运行时（`docker run` 里的网络访问）也慢，那是另一类问题，需要走代理方案，超出本章范围。

---

### 本章小结

- 六个高频坑基本覆盖了安装到配置 90% 的报错：RHEL 依赖（①）、网络模块（②）、加速器假配置（③）、compose 插件（④）、socket 权限（⑤）、cgroup driver（⑥）。
- 坑 ① 记住 `yum-config-manager --enable extras` + 装 `container-selinux slirp4netns fuse-overlayfs`；CentOS 7 老机器先切 vault 源。
- 坑 ② 的持久化要写 `/etc/sysctl.d/` 和 `/etc/modules-load.d/` 两个文件，模块加载顺序错了重启必失效。
- 坑 ③ 加速器是"优先尝试"会回退官方，JSON 用 `python3 -m json.tool` 检查、改完必须 `daemon-reload` + `restart`。
- 坑 ④ compose 是插件不是内置命令，放 `~/.docker/cli-plugins/` 并 `chmod +x`，Engine 需 ≥ 20.10。
- 坑 ⑤ `usermod -aG docker` 后必须重新登录/`newgrp` 才生效，禁止 `chmod 666` socket。
- 坑 ⑥ K8s 场景用 `"exec-opts": ["native.cgroupdriver=systemd"]` 对齐，且记得与已有 daemon.json 配置合并。
- 加速器失效先 `docker info` → `curl -I` → 换源，三步定位，别瞎重装。

下一章是**第八章速查附录**：把前七章所有命令浓缩成可复制的速查卡片，连同镜像源清单和官方文档链接放在一起，作为日后的"手边单页"。

---

## 第八章 速查附录

> 前面七章把安装步骤讲得很细，但命令一多就容易忘。本章把全文浓缩成可复制粘贴的速查卡片：apt / dnf 两条轨道的安装命令、换源 sed、镜像加速 daemon.json，再集中列出 2026 可用的镜像加速器清单、已失效源清单和官方文档链接。日常排障先翻本章，拿不准的细节再回看对应章节。

### 一、apt 系一键速查（Ubuntu / Debian）

> 完整步骤见第二章。Debian 用户只需把下面 URL 里的 `ubuntu` 改成 `debian`；`$(...)` 会在粘贴执行时自动替换成你机器的真实值。

```bash
# ① 前置依赖
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# ② 导入 GPG 密钥（阿里云软件源）
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# ③ 写入 deb822 软件源（docker.sources）
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://mirrors.aliyun.com/docker-ce/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.gpg
EOF

# ④ 刷新并安装全家桶
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- 指定版本：`apt-cache madison docker-ce` 查版本，再 `sudo apt-get install -y docker-ce=<版本> docker-ce-cli=<同版本> containerd.io docker-buildx-plugin docker-compose-plugin`（版本号要连 `5:` 前缀一起写，详见第二章第七节）。
- 锁版本：`sudo apt-mark hold docker-ce docker-ce-cli`。
- 阿里云 ECS 换内网源：`sudo sed -i 's#https://mirrors.aliyun.com/docker-ce#http://mirrors.cloud.aliyuncs.com/docker-ce#' /etc/apt/sources.list.d/docker.sources && sudo apt-get update`。

### 二、dnf/yum 系一键速查（CentOS / RHEL / Rocky / Alma）

> 完整步骤见第三章。前置插件按发行版二选一：CentOS 7 / Stream 8 是真 yum，装 `yum-utils`；RHEL 8+、Rocky、Alma、Stream 9 装 `dnf-plugins-core`。命令区 `yum` / `dnf` 两组也是二选一。

```bash
# ① 前置插件（二选一）
sudo yum install -y yum-utils          # CentOS 7 / Stream 8
sudo dnf install -y dnf-plugins-core   # RHEL 8+ / Rocky / Alma / Stream 9

# ② 添加阿里云 docker-ce 源（二选一；el10 机器把 centos 改成 rhel）
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# ③ 安装全家桶（二选一）
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# ④ 启用并启动（两条轨道通用）
sudo systemctl enable --now docker
```

- 路径分水岭：el8/el9 走 `linux/centos/`，RHEL 10 / Rocky 10 / Alma 10 走 `linux/rhel/`，选错会 makecache 404（详见第三章第六节）。
- 指定版本：`dnf list docker-ce --showduplicates` 查版本，再 `sudo dnf install -y docker-ce-<版本> docker-ce-cli-<同版本> containerd.io docker-buildx-plugin docker-compose-plugin`。
- 锁版本：`sudo dnf versionlock docker-ce docker-ce-cli`。
- CentOS 7 是 EOL 系统，装 Docker 前先切 vault 归档源（见第三节④），并留意 `container-selinux >= 2:2.74` 依赖坑（第七章坑 ①）。

### 三、换源 sed 命令速查

> 原理：`sed -i` 原地替换文件里的 URL 前缀，用 `+` 或 `#` 作分隔符，避免转义 URL 里大量的 `/`。改完源后要清缓存/刷新索引。

```bash
# ① dnf/yum：官方源 → 阿里云
sudo sed -i 's+https://download.docker.com+https://mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
sudo dnf clean all && sudo dnf makecache

# ② dnf/yum：官方源 → 清华 TUNA
sudo sed -i 's+https://download.docker.com+https://mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
sudo dnf clean all && sudo dnf makecache

# ③ apt：阿里云公网源 → 阿里云 ECS 内网源（仅 ECS 可用）
sudo sed -i 's#https://mirrors.aliyun.com/docker-ce#http://mirrors.cloud.aliyuncs.com/docker-ce#' /etc/apt/sources.list.d/docker.sources
sudo apt-get update

# ④ CentOS 7：默认仓库切 vault 归档源（EOL 兜底，装 Docker 前先跑）
sudo sed -i 's/mirrorlist=/#mirrorlist=/g; s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo
sudo yum clean all && sudo yum makecache
```

### 四、镜像加速 daemon.json 速查

> 完整步骤见第五章。加速器只对 Docker Hub 生效，改完**必须重启 docker 才会生效**；`docker info` 里能看到才算配成功。

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io"
  ]
}
```

```bash
# 写入配置 → 重启 → 验证 → 测速
sudo tee /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://docker.m.daocloud.io"
  ]
}
EOF
sudo systemctl daemon-reload && sudo systemctl restart docker
docker info | grep -A 5 "Registry Mirrors"
time docker pull nginx:alpine
```

- 多仓库拉取：毫秒镜像同域提供 `ghcr.1ms.run` / `k8s.1ms.run` / `quay.1ms.run` / `mcr.1ms.run` 前缀，`docker pull k8s.1ms.run/pause:3.9` 后 `docker tag` 回原名称即可（详见第五章）。
- 加速器失效排查顺序：`docker info` 看加速器 → `curl -I <镜像地址>` 测连通 → 换源。加速器 ≠ 代理的概念边界见 [[docker/镜像加速器vs代理-概念对比]]。

### 五、2026 可用镜像加速器清单

> 从下表中挑 2-3 个填入 daemon.json。免费源晚高峰（20:00-23:00）可能限速，建议每月实测一次存活。验证日期：2026-08。

| 源 | 地址 | 性质 | 说明 |
|----|------|------|------|
| 毫秒镜像 | `https://docker.1ms.run` | 商业/社区 | 高可用；同域多仓库 `ghcr.1ms.run` / `k8s.1ms.run` / `quay.1ms.run` / `mcr.1ms.run` / `nvcr.1ms.run` |
| 轩辕镜像 | `https://docker.xuanyuan.me` | 社区公益 | 实测 12.3MB/s、99.2% 成功率；专业版 `xuanyuan.cloud` 提供多仓库 |
| DaoCloud | `https://docker.m.daocloud.io` | 社区公益 | 全协议反代，可拉 `gcr.io` 等 |
| 1Panel | `https://docker.1panel.live` | 官方社区 | 仅限大陆访问；旧地址 `docker.1panel.dev` 已失效 |
| 阿里云个人 | `https://<your-id>.mirror.aliyuncs.com` | 云厂商 | 需注册获取专属地址，最稳定 |

### 六、已失效 / 不推荐源清单（2026 确认）

> 老牌高校源已大面积停服，别再往 daemon.json 里填这些地址——配了也会超时回退。对照排除比挨个试快得多。

| 源 | 地址 | 失效状态 / 原因 |
|----|------|------------------|
| 中科大 | `docker.mirrors.ustc.edu.cn` | 已停服（仍提供软件源，无 pull 加速） |
| 清华 TUNA | `docker.mirrors.tuna.tsinghua.edu.cn` | 已停服（仍提供软件源，无 pull 加速） |
| 南京大学 | `docker.nju.edu.cn` | 已停服 |
| 网易 | `hub-mirror.c.163.com` | 已停服 |
| dockerhub.icu | `https://dockerhub.icu` | 证书错误 |
| dockerproxy.cn | `https://dockerproxy.cn` | 已关停 |
| dockerpull.com | `https://dockerpull.com` | DNS 解析失败 |
| docker.mrxn.net | `https://docker.mrxn.net` | HTTP 502 |
| 开放原子 | `atomhub.openatom.cn` | 2024-12 退役 |
| 1Panel 旧址 | `docker.1panel.dev` | 已失效，改用 `docker.1panel.live` |

### 七、官方文档与国内镜像站链接

- 官方文档（命令模板以官方页为准）
  - [Docker Engine install (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/)
  - [Docker Engine install (Debian)](https://docs.docker.com/engine/install/debian/)
  - [Docker Engine install (RHEL/CentOS)](https://docs.docker.com/engine/install/rhel/)
  - [Compose plugin (Linux)](https://docs.docker.com/compose/install/linux/)
  - [Compose standalone](https://docs.docker.com/compose/install/standalone/)
- 国内镜像站帮助页
  - [阿里云 docker-ce 镜像](https://developer.aliyun.com/mirror/docker-ce)
  - [清华 TUNA docker-ce](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)
  - [中科大 docker-ce](https://mirrors.ustc.edu.cn/help/docker-ce.html)

### 本章小结

- 安装命令分两轨：apt 系复制第一节、dnf/yum 系复制第二节，粘贴前先 `cat /etc/os-release` 确认发行版。
- 换源统一走 sed 原地替换，`+` / `#` 分隔符避免转义 `/`；apt 改 `docker.sources`、dnf 改 `docker-ce.repo`，目标文件别搞混。
- 镜像加速改完必须 `systemctl daemon-reload && systemctl restart docker`，再用 `docker info` 验证，否则不生效。
- 可用源从「毫秒 / 轩辕 / DaoCloud / 1Panel」里挑 2-3 个；排障时拿第六节的失效清单直接排除老地址。
- 官方文档与镜像站帮助页长期有效，是最新命令的唯一权威来源。

到这里，本笔记 8 章全部结束。装好的 Docker + Compose 环境下一步就可以实际编排了；Windows 桌面版安装见 [[docker/Windows-DockerDesktop安装指南-国内网络版]]，加速器与代理的概念边界见 [[docker/镜像加速器vs代理-概念对比]]。日后命令忘了，翻回本章即可。
