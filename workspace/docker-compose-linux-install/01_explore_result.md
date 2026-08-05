# Docker 与 Docker Compose 安装（国内环境）- 探测式收集结果

> 收集日期：2026-08-03 ｜ 探测方式：3 个并行 subagent ｜ 状态：待用户选择学习方向

---

## 一、Docker Engine Linux 安装（国内软件源）

### 官方方式概述
- **Ubuntu/Debian（apt）**：添加 Docker 官方 apt 仓库 `download.docker.com/linux/{ubuntu|debian}`，装 `docker-ce docker-ce-cli containerd.io`。
- **CentOS/RHEL（dnf/yum）**：`dnf config-manager --add-repo` 加官方 yum 仓库；CentOS 9/Rocky 9 用 `linux/centos/`，**Rocky/Alma 10 及 RHEL 10 改用 `linux/rhel/`**。
- 一键脚本 `curl -fsSL https://get.docker.com | sh` 国内直连易超时，需配镜像源。

### 国内软件源（装 docker-ce 包）— 2026-08 可用性
| 源 | 地址 | 状态 |
|----|------|------|
| **阿里云**（最常用） | `https://mirrors.aliyun.com/docker-ce` | ✅ 推荐；ECS 内网用 `mirrors.cloud.aliyuncs.com` |
| 清华 TUNA | `https://mirrors.tuna.tsinghua.edu.cn/docker-ce` | ✅ 可用，仅软件包，不提供 pull 加速 |
| 中科大 USTC | `https://mirrors.ustc.edu.cn/docker-ce` | ✅ 可用；其 Docker Hub 加速器已不推荐 |

> ⚠️ 关键区分：**软件源镜像**（装 docker-ce 包）≠ **镜像加速器**（docker pull 拉镜像），二者不要混写。

### 系统要求与前置
- 64 位；内核 ≥ 3.10（CentOS 7 overlay2 需高版本）；CentOS 7 已 EOL。
- systemd 管理：`systemctl enable --now docker`；cgroup 驱动建议 `native.cgroupdriver=systemd`。
- RHEL 系依赖 `container-selinux`（`Requires: container-selinux >= 2:2.74` 常见报错）、`fuse-overlayfs`、`slirp4netns`。
- CentOS 8+ firewalld 默认 nftables，需处理 `docker0` 网段放通；常见 `bridge-nf-call-iptables is disabled` 需改 sysctl。

### 安装后验证
```bash
sudo systemctl enable --now docker
docker --version
sudo docker run hello-world
sudo docker info | grep -A 3 "Registry Mirrors"
```

---

## 二、Docker Compose 安装（plugin vs standalone）

### 推荐：Compose v2 plugin（`docker compose` 空格命令）
```bash
# Debian/Ubuntu
sudo apt-get install docker-compose-plugin
# RHEL/CentOS/Fedora
sudo yum install docker-compose-plugin   # 或 dnf
```
- **国内优势**：走阿里云软件源，完全不依赖 GitHub。
- 版本匹配：Engine **必须 ≥ 20.10**，否则报 `docker: 'compose' is not a docker command`；当前 Compose v5.x。

### 备选：standalone binary（`docker-compose` 连字符命令）
```bash
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- 国内 GitHub 下载慢：ghproxy 类前缀代理（`ghproxy.net` 等）、本地下载后 scp 上传（最稳）。
- ⚠️ ghproxy 公共代理 2026 年普遍不稳定，脚本不要硬编码单域名，先 `curl -I` 探测。

### 对比结论
| 维度 | plugin（推荐） | standalone |
|------|---------------|-----------|
| 安装 | apt/dnf 走软件源 | GitHub 下载需加速 |
| 升级 | 包管理器自动 | 手动重下 |
| 官方定位 | 推荐标准 | 向后兼容保留 |

---

## 三、国内镜像加速（2026 可用清单）

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
```

### 2026-08 可用镜像源（高确认度）
| 源 | 地址 | 性质 |
|----|------|------|
| 毫秒镜像 | `https://docker.1ms.run` | 商业/社区，多仓库代理 `ghcr/k8s/quay/nvcr.1ms.run` |
| 轩辕镜像 | `https://docker.xuanyuan.me` | 社区公益，晚高峰可能限速 |
| DaoCloud | `https://docker.m.daocloud.io` | 社区公益，可拉 `gcr.io` 等 |
| 1Panel | `https://docker.1panel.live` | 官方社区，限大陆访问；旧地址 `.dev` 已失效 |
| 阿里云个人 | `https://<your-id>.mirror.aliyuncs.com` | 需注册获取，最稳定 |

### 已失效/不推荐（2026 确认）
中科大、清华、南大、上海交大、网易等老牌高校/商业 Docker Hub 加速器 **2024–2025 已大面积停服**，老博客清单大多过期，不要照抄。

### 常见坑
1. `registry-mirrors` **只对 Docker Hub 生效**；gcr.io/ghcr.io/quay.io/k8s 等需用多仓库代理域名显式拉取（如 `docker.m.daocloud.io/gcr.io/...`）。
2. 加速器是「优先尝试」非「强制」，失败会回退官方 Hub → 表现为超时。
3. 排查顺序：`docker info` 看加速器 → `curl -I <mirror>` 测连通 → 换源。
4. K8s/K3s 用 containerd，不读 daemon.json，需改 `/etc/containerd/config.toml`。
5. 加速器 ≠ 代理：加速器只影响 pull；代理让全部流量走代理，更稳但需自建。

---

## 四、推荐信源

**官方**
- Docker Engine install: https://docs.docker.com/engine/install/
- Compose plugin (Linux): https://docs.docker.com/compose/install/linux/
- Compose standalone: https://docs.docker.com/compose/install/standalone/
- 清华 TUNA docker-ce 帮助页: https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/
- 中科大 docker-ce 帮助页: https://mirrors.ustc.edu.cn/help/docker-ce.html

**国内**
- 《Docker 从入门到实践》安装篇: https://yeasy.gitbook.io/docker_practice/di-yi-bu-fen-ru-men-pian/03_install
- 阿里云 ECS 安装文档: https://www.alibabacloud.com/help/zh/ecs/user-guide/install-and-use-docker
- 2026 国内镜像源汇总（GitHub, 2026-08）: https://github.com/dongyubin/dockerhub
- 2026 Docker 国内镜像源加速指南（腾讯云, 2026-07）: https://cloud.tencent.com.cn/developer/article/2647943

---

## 五、方向菜单（待用户选择）

### A. 完整实战教程（推荐）
覆盖 **Ubuntu/Debian + CentOS/RHEL 双轨**：Engine 安装（阿里云源）→ Compose 插件 → 镜像加速 → 验证避坑，一站式的"从零到 Compose 能跑"。

### B. 精简快速上手
假设常用 **Ubuntu/Debian 单一发行版**，聚焦最短安装路径（Engine + Compose plugin + 加速器），篇幅精炼，适合已有 Docker 基础（本用户为"有了解"）快速落地。

### C. 深度避坑运维向
完整安装 + 大篇幅常见坑：内核/container-selinux/systemd、镜像加速器失效排查、K8s containerd 区别、代理 vs 加速器对比。适合运维视角。

### D. 混合：教程 + 速查
主文完整实战教程，末尾附「命令速查表 + 可用镜像源清单」附录，方便后续回查。
