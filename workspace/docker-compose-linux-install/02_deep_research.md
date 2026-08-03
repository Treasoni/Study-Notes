# Docker 与 Docker Compose 安装（国内环境）- 深度资料收集

> 收集时间：2026-08-03 ｜ 方向：A 完整实战教程（Ubuntu/Debian + CentOS/RHEL 双轨）
> 搜索关键词：Docker Engine linux install 2026 / docker-ce 阿里云源 / docker compose plugin / 国内镜像加速器 2026 / docker 安装常见坑
> 信源：官方文档（docs.docker.com）+ 阿里云/清华镜像站 + 近期（2025-2026）技术博客 + GitHub 汇总

---

## 一、核心结论（综合分析）

1. **安装路径统一**：apt 系与 RPM 系的"全家桶"包一致 = `docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`。一次装齐 Engine + Buildx + Compose plugin。
2. **国内装 Engine 最常用阿里云软件源** `https://mirrors.aliyun.com/docker-ce`（清华 TUNA、中科大也可），关键区分：**软件源镜像（装包）≠ 镜像加速器（docker pull）**。
3. **Compose 首选 plugin 方式**（`docker compose` 空格命令），走软件源自动升级，完全绕开 GitHub；standalone（`docker-compose` 连字符）仅旧脚本兼容用。
4. **2026 镜像加速**：老牌高校源（中科大/清华/南大/网易）已大面积停服；高确认可用源 = 毫秒 `docker.1ms.run`、轩辕 `docker.xuanyuan.me`、DaoCloud `docker.m.daocloud.io`、1Panel `docker.1panel.live`（限大陆）。
5. **安装完成 ≠ 生效**：权限（usermod 后需重登）、Compose 插件路径、br_netfilter 模块、cgroup driver 对齐等隐藏前提是常见坑。

---

## 二、官方安装命令（精读 docs.docker.com）

### Ubuntu / Debian（apt，deb822 新版格式）
```bash
sudo apt update
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```
- Debian：URL 用 `https://download.docker.com/linux/debian`，Suites 用 `$VERSION_CODENAME`。
- 官方示例版本 `5:29.7.1-1~ubuntu.24.04~noble`。
- 新版不再用 `gpg --dearmor` + `docker.list`，改 deb822 `docker.sources` + `docker.asc`（兼容旧写法也可）。

### RHEL / CentOS / Rocky（dnf）
```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker run hello-world
```
- 官方页面只覆盖 RHEL 8/9/10；**Rocky/Alma 10 及 RHEL 10 用 `linux/rhel/` 路径**，CentOS 9/Rocky 9 用 `linux/centos/`。
- GPG 指纹核对：`060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`。
- CentOS 7 已 EOL，官方不再覆盖；仍需支持时用 vault 归档源 + extras 仓库。

---

## 三、国内软件源替换（阿里云 / 清华）

### 阿里云（最常用，推荐）
```bash
# Ubuntu/Debian (apt)
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# CentOS/RHEL (yum)
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo service docker start
```
- ECS VPC 内网：`http://mirrors.cloud.aliyuncs.com/docker-ce`（更快，免公网）。
- 指定版本：`apt-cache madison docker-ce` / `yum list docker-ce.x86_64 --showduplicates` 后 `install docker-ce=<VERSION>`。

### 清华 TUNA（备选）
```bash
# 一键脚本（DOWNLOAD_URL 变量 + 必须 sudo -E sh）
export DOWNLOAD_URL="https://mirrors.tuna.tsinghua.edu.cn/docker-ce"
curl -fsSL https://raw.githubusercontent.com/docker/docker-install/master/install.sh | sudo -E sh

# apt 改 deb822：URIs 换成 https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian
# dnf：先加官方 repo，再 sed -i 's+https://download.docker.com+https://mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```
- TUNA 仅提供 docker-ce **软件包**，不提供 docker pull 加速。

---

## 四、Docker Compose 安装

### 方式 A：Compose v2 plugin（推荐，`docker compose` 空格命令）
```bash
# Debian/Ubuntu
sudo apt-get update && sudo apt-get install docker-compose-plugin
# RHEL/CentOS
sudo yum update && sudo yum install docker-compose-plugin
docker compose version   # 预期：Docker Compose version v5.x
```
- 随 Docker 仓库安装，自动升级；国内走阿里云软件源，**完全绕开 GitHub**。
- Engine 必须 ≥ 20.10，否则报 `docker: 'compose' is not a docker command`。
- 当前最新 Compose v5.x（2026-08 已确认 v5.4.0）。

### 方式 B：standalone binary（兼容用，`docker-compose` 连字符）
```bash
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```
- 架构后缀：`x86_64` / `aarch64`（ARM64）/ `armv7`。
- 国内 GitHub 下载慢：ghproxy 类前缀代理（`https://ghproxy.net/...`）、本地下载 + scp 上传（最稳）。ghproxy 公共代理 2026 普遍不稳定，勿硬编码单域名。

### 对比结论
| 维度 | plugin（推荐） | standalone |
|------|---------------|-----------|
| 命令 | `docker compose`（空格） | `docker-compose`（连字符） |
| 安装 | apt/dnf 走软件源 | GitHub 下载需加速 |
| 升级 | 包管理器自动 | 手动重下覆盖 |
| 官方定位 | 推荐、标准 | 仅为向后兼容保留 |

---

## 五、2026 国内镜像加速（registry-mirrors）

### 配置（Linux `/etc/docker/daemon.json`）
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
sudo systemctl daemon-reload && sudo systemctl restart docker
docker info | grep -A 5 "Registry Mirrors"   # 确认生效
time docker pull nginx:alpine                 # 实测速度
```

### 2026 高确认可用源
| 源 | 地址 | 性质 | 说明 |
|----|------|------|------|
| 毫秒镜像 | `https://docker.1ms.run` | 商业/社区 | 高可用；多仓库 `ghcr.1ms.run`/`k8s.1ms.run`/`quay.1ms.run`/`mcr.1ms.run`/`nvcr.1ms.run` |
| 轩辕镜像 | `https://docker.xuanyuan.me` | 社区公益 | 实测 12.3MB/s、99.2% 成功率；专业版 `xuanyuan.cloud` 多仓库 |
| DaoCloud | `https://docker.m.daocloud.io` | 社区公益 | 全协议反代，可拉 `gcr.io` 等 |
| 1Panel | `https://docker.1panel.live` | 官方社区 | 仅限大陆访问；旧地址 `docker.1panel.dev` 已失效 |
| 阿里云个人 | `https://<your-id>.mirror.aliyuncs.com` | 云厂商 | 需注册获取专属地址，最稳定 |

### 已失效/不推荐（2026 确认）
中科大 `docker.mirrors.ustc.edu.cn`、清华、南大 `docker.nju.edu.cn`、网易 `hub-mirror.c.163.com`、`dockerhub.icu`（证书错）、`dockerproxy.cn`（关停）、`dockerpull.com`（DNS 失败）、`docker.mrxn.net`（502）、`atomhub.openatom.cn`（2024-12 退役）、`docker.1panel.dev`。

### 验证/使用要点
1. `registry-mirrors` **只对 Docker Hub 生效**；gcr/ghcr/quay/k8s 需多仓库代理显式拉取，如 `docker pull k8s.1ms.run/pause:3.9` 后 `docker tag` 回原名称。
2. 加速器是「优先尝试」非强制，失败回退官方 Hub → 表现为超时；改完必须重启 docker 并验证。
3. 排查顺序：`docker info` 看加速器 → `curl -I <mirror-url>` 测连通 → 换源。
4. K8s/K3s 用 containerd，不读 daemon.json，需改 `/etc/containerd/config.toml` 的 `registry.mirrors["docker.io"].endpoint`。
5. 加速器 ≠ 代理：加速器只影响 pull；代理走全部流量更稳但需自建（systemd drop-in HTTP_PROXY 或 daemon.json `"proxies"`）。
6. 晚高峰（20:00-23:00）免费源可能限速；建议每月实测一次源存活。

---

## 六、常见坑与运维细节（精读汇总）

### 1. `Requires: container-selinux >= 2:2.74`（RHEL 系）
- 根因：extras 仓库未启用或版本过低。解决：`sudo yum-config-manager --enable extras; sudo yum install -y container-selinux slirp4netns fuse-overlayfs`。
- CentOS 7 已 EOL，需启用 vault 归档源；CentOS 7.6 以下旧基线易反复依赖失败。

### 2. `bridge-nf-call-iptables is disabled`（网络告警）
- 根因：`br_netfilter` 内核模块未加载，sysctl 键不存在或为 0。
```bash
modprobe br_netfilter
sysctl -w net.bridge.bridge-nf-call-iptables=1
# 持久化：
echo -e "net.bridge.bridge-nf-call-iptables=1\nnet.bridge.bridge-nf-call-ip6tables=1\nnet.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-bridge.conf
echo "br_netfilter" | sudo tee /etc/modules-load.d/br_netfilter.conf
```
- ⚠️ 必须用 `/etc/modules-load.d/` 保证开机先加载模块，否则 systemd-sysctl 早于模块加载，重启后配置失效。

### 3. daemon.json 配了镜像源仍访问官方仓库
- registry-mirrors 是「优先尝试」非强制代理，失败自动回退 docker.io；只代理 Docker Hub。
- 改完必须 `systemctl daemon-reload && systemctl restart docker`；JSON 语法错误（漏逗号/括号）也常见。

### 4. `docker: 'compose' is not a docker command`
- Compose v2 是 CLI 插件，需装 `docker-compose-plugin` 或二进制放 `~/.docker/cli-plugins/`（或 `/usr/local/lib/docker/cli-plugins`）且 `chmod +x`。
- 插件装在 `/usr/libexec/docker/cli-plugins/` 时非 root 常不识别。

### 5. `permission denied ... /var/run/docker.sock`
- socket 属 root:docker 权限 660，非 root 需 `sudo usermod -aG docker $USER` 后**重新登录**（`newgrp docker` 或注销）生效。
- 禁止 `chmod 666`（重启失效且等于给全系统 root 权限）。

### 6. cgroup driver 不一致（K8s 场景）
- Docker 默认 cgroupfs，kubelet 推荐 systemd，不一致则 kubelet 启动失败。
- 推荐 daemon.json 加 `"exec-opts": ["native.cgroupdriver=systemd"]`。
- K8s 1.24+ 已移除 dockershim，建议用 containerd 并对齐 cgroup driver。

---

## 七、信源清单

**官方文档**
- Docker Engine install（Ubuntu）: https://docs.docker.com/engine/install/ubuntu/
- Docker Engine install（Debian）: https://docs.docker.com/engine/install/debian/
- Docker Engine install（RHEL/CentOS）: https://docs.docker.com/engine/install/rhel/
- Compose plugin (Linux): https://docs.docker.com/compose/install/linux/
- Compose standalone: https://docs.docker.com/compose/install/standalone/

**国内镜像站**
- 阿里云 docker-ce 镜像帮助页: https://developer.aliyun.com/mirror/docker-ce
- 清华 TUNA docker-ce 帮助页: https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/
- 中科大 docker-ce 帮助页: https://mirrors.ustc.edu.cn/help/docker-ce.html

**2026 镜像加速汇总**
- dongyubin/dockerhub（2026-06 实测）: https://github.com/dongyubin/dockerhub
- 2026 Docker 国内镜像源指南（腾讯云 2026-07）: https://cloud.tencent.com.cn/developer/article/2647943
- 2026-08 多仓库源清单（阿里云开发者）: https://developer.aliyun.com/article/1752736
- 轩辕镜像: https://github.com/SeanChang/xuanyuan_docker_proxy

**避坑资料**
- container-selinux: https://segmentfault.com/a/1190000047548761
- bridge-nf 告警: https://github.com/moby/moby/discussions/48559
- 镜像源不生效: https://cloud.tencent.com.cn/developer/article/2639741
- docker.sock 权限: https://blog.csdn.net/xiaokai1999/article/details/129861664
- cgroup driver: https://github.com/kubernetes/kubeadm/issues/2605

**中文书/教程**
- 《Docker 从入门到实践》安装篇: https://yeasy.gitbook.io/docker_practice/di-yi-bu-fen-ru-men-pian/03_install
- 阿里云 ECS 安装文档: https://www.alibabacloud.com/help/zh/ecs/user-guide/install-and-use-docker
