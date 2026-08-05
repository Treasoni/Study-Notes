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
