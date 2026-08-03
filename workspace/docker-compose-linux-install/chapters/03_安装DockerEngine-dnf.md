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
