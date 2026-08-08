---
tags: [docker, mac, 镜像加速, registry-mirrors, daemon.json]
created: 2026-03-04
updated: 2026-08-08
---

# Docker Desktop Mac 镜像加速器配置

> [!info] 概述
> **Docker 镜像加速器可以加速从 Docker Hub 拉取镜像的速度**，在国内网络环境下配置加速器是必要操作。本文档介绍 Mac 上 Docker Desktop 的配置方法：**GUI 配置（Settings → Docker Engine，唯一受支持方式）**；命令行 `daemon.json` 方式仅适用于 Linux 原生 dockerd。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解为什么需要加速器 | [[DockerDesktop镜像加速器配置#一、为什么需要镜像加速器]] |
| 通过 GUI 界面配置 | [[DockerDesktop镜像加速器配置#二、方法一：Docker Desktop GUI 配置]] |
| 通过命令行配置（仅 Linux dockerd） | [[DockerDesktop镜像加速器配置#三、命令行配置（仅适用于 Linux dockerd）]] |
| 验证配置是否生效 | [[DockerDesktop镜像加速器配置#四、验证配置]] |
| 获取可用镜像源 | [[DockerDesktop镜像加速器配置#五、可用镜像源列表]] |
| 排查问题 | [[DockerDesktop镜像加速器配置#六、常见问题]] |

---

## 一、为什么需要镜像加速器

### 是什么

**镜像加速器（Registry Mirror）** 是 Docker Hub 的镜像代理服务器。当你拉取镜像时，Docker 会优先从加速器获取，而不是直接访问 Docker Hub。

### 为什么需要

| 问题 | 说明 |
|------|------|
| **网络慢** | Docker Hub 服务器在国外，访问速度慢 |
| **连接超时** | 经常出现 timeout 错误 |
| **限速** | Docker Hub 有拉取频率限制 |

### 通俗理解

**🎯 比喻**：镜像加速器就像「CDN 加速」。就像看视频时，视频会从离你最近的 CDN 节点加载，而不是从源站加载。Docker 镜像加速器也是同样的道理，从国内的服务器获取镜像，速度更快。

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    镜像加速器工作原理                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  docker pull nginx                                          │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐    命中     ┌─────────────┐               │
│  │ 镜像加速器   │ ─────────→ │  返回镜像    │               │
│  │ (国内服务器) │             └─────────────┘               │
│  └─────────────┘                                           │
│       │ 未命中                                               │
│       ▼                                                     │
│  ┌─────────────┐           ┌─────────────┐                 │
│  │  Docker Hub │ ─────────→ │  返回镜像    │                 │
│  │ (国外服务器) │           └─────────────┘                 │
│  └─────────────┘                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [Docker Daemon 配置文档](https://docs.docker.com/engine/daemon/) - Docker 官方

---

## 二、方法一：Docker Desktop GUI 配置

### 步骤概览

```
打开 Docker Desktop → Settings → Docker Engine → 编辑 JSON → Apply & Restart
```

### 详细步骤

#### 步骤 1：打开 Docker Desktop 设置

1. 点击菜单栏的 **Docker 图标**（鲸鱼图标）
2. 选择 **Settings...**（设置）

或直接打开 Docker Desktop 应用，点击右上角 **⚙️ 设置图标**

#### 步骤 2：进入 Docker Engine 配置

在左侧导航栏中选择 **Docker Engine**

#### 步骤 3：编辑 JSON 配置

在右侧的 JSON 编辑器中，添加 `registry-mirrors` 配置：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me"
  ]
}
```

> [!warning] 注意
> - 保持 JSON 格式正确，注意逗号分隔
> - 不要与现有配置冲突
> - 镜像地址用英文引号包裹

#### 步骤 4：应用配置

点击右下角 **Apply & Restart** 按钮，等待 Docker 重启完成。

### 截图示意

```
┌─────────────────────────────────────────────────────────────┐
│  Docker Desktop Settings                                    │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────┐                                            │
│  │ General    │                                            │
│  │ Resources  │                                            │
│  │ Docker     │  ← ┌──────────────────────────────────┐   │
│  │ Engine     │    │  {                               │   │
│  │ ...        │    │    "registry-mirrors": [         │   │
│  └────────────┘    │      "https://docker.m.daocloud.io",│  │
│                    │      "https://docker.1ms.run"      │   │
│                    │    ]                               │   │
│                    │  }                                 │   │
│                    └──────────────────────────────────┘   │
│                                                            │
│                              [Apply & Restart]             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [Mac桌面Docker配置镜像地址指南](https://m.blog.csdn.net/wstever/article/details/155319540) - CSDN
> - [DockerDesktop配置镜像](https://m.blog.csdn.net/csdn1027719307/article/details/149422544) - CSDN

---

## 三、命令行配置（仅适用于 Linux dockerd）

> [!warning] ⚠️ Docker Desktop for Mac 不读取 `~/.docker/daemon.json`
>
> Docker Desktop 的 dockerd 运行在它内置的 Linux VM 里，宿主机的 `~/.docker/daemon.json` **不会被读取**。
> `~/.docker/` 只是 **Docker CLI** 的配置目录（存放 `config.json`），不是 daemon 配置。
> 所以在 Docker Desktop 上往 `~/.docker/daemon.json` 写镜像源**不会生效**。
>
> ✅ **Docker Desktop（Mac/Windows）唯一受支持入口**：`Settings → Docker Engine → Apply & Restart`（即方法一）。
> ✅ 命令行写 `daemon.json` 只适用于 **Linux 原生 dockerd**（`/etc/docker/daemon.json`）。

### 3.1 配置文件位置（Linux 原生 dockerd）

```bash
# Linux 原生 Docker 引擎的 daemon 配置路径
/etc/docker/daemon.json

# 文件通常不存在，需要手动创建
```

### 3.2 创建/编辑配置文件（Linux）

```bash
# 方法1：使用 vim 编辑
sudo vim /etc/docker/daemon.json

# 方法2：直接写入
sudo tee /etc/docker/daemon.json > /dev/null << 'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me"
  ]
}
EOF

# 重启 docker 服务使配置生效
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 3.3 完整配置示例（Linux）

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me"
  ],
  "insecure-registries": [],
  "debug": false,
  "experimental": false,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 3.4 重启 Docker 使配置生效

```bash
# 方法1：重启 Docker Desktop（Mac，命令本身可用 ✅）
osascript -e 'quit app "Docker"'
sleep 2
open -a Docker

# 方法2：Linux 原生 docker
sudo systemctl restart docker

# 方法3：手动重启 Docker Desktop
# 点击菜单栏 Docker 图标 → Restart
```

### 3.5 一键配置脚本（仅限 Linux 原生 dockerd）

```bash
#!/bin/bash
# 仅适用于 Linux 原生 dockerd；不适用于 Docker Desktop

CONFIG_FILE="/etc/docker/daemon.json"

# 备份原配置
if [ -f "$CONFIG_FILE" ]; then
    sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    echo "已备份原配置文件"
fi

# 写入新配置
sudo tee "$CONFIG_FILE" > /dev/null << 'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me"
  ]
}
EOF

# 重启使配置生效
sudo systemctl restart docker

echo "配置文件已更新: $CONFIG_FILE"
echo "请确认：docker info | grep 'Registry Mirrors'"
```

> [!info] 来源
> - [Docker daemon 配置文档](https://docs.docker.com/engine/daemon/) - Docker 官方
> - [Docker dockerd 命令参考](https://docs.docker.com/engine/reference/commandline/dockerd/) - Docker 官方

---

## 四、验证配置

### 4.1 检查配置是否生效

```bash
# 方法1：查看 docker info 输出
docker info | grep -A 5 "Registry Mirrors"

# 预期输出（示例，取决于你实际填的镜像源）：
# Registry Mirrors:
#  https://docker.1ms.run/
#  https://docker.m.daocloud.io/
#  https://docker.xuanyuan.me/
```

### 4.2 测试拉取速度

```bash
# 拉取一个小镜像测试
time docker pull alpine:latest

# 删除测试镜像
docker rmi alpine:latest
```

### 4.3 查看详细配置

```bash
# 查看完整 docker info
docker info

# 确认当前 docker context 指向 Docker Desktop
docker context show
```

> [!note] 说明
> Docker Desktop 的 daemon 配置由应用统一管理，宿主机上没有可直接 `cat` 的 `~/.docker/daemon.json`（那是 Docker CLI 的配置目录）。配置是否生效以 `docker info` 中的 `Registry Mirrors` 为准。

---

## 五、可用镜像源列表

### 国内镜像源

| 镜像源 | 地址 | 状态（2026-08 实测） |
|--------|------|------|
| **1ms.run** | `https://docker.1ms.run` | ✅ 可用 |
| **DaoCloud** | `https://docker.m.daocloud.io` | ✅ 可用 |
| **轩辕镜像** | `https://docker.xuanyuan.me` | ✅ 可用 |
| **简行镜像** | `https://docker.jiaxin.site` | ✅ 可用 |
| **DockerProxy** | `https://dockerproxy.net` | ✅ 可用 |
| **中科大** | `https://docker.mirrors.ustc.edu.cn` | ❌ 已失效 |
| **南京大学** | `https://docker.nju.edu.cn` | ❌ 已失效/受限 |
| **上海交大** | `https://docker.mirrors.sjtug.sjtu.edu.cn` | ❌ 已失效 |

> [!warning] 注意
> 镜像源可用性变化很快（部分源会被限流或屏蔽），如果某个源不可用，请尝试其他源或搜索最新的可用镜像源。

> [!tip] 配置前自测
> ```bash
> # 返回 401 或 200 说明可连通；000 或超时说明不可用
> curl -s -o /dev/null -w "%{http_code}\n" -m 10 https://<镜像地址>/v2/
> ```
>
> 持续更新的可用源列表参考：[dongyubin/DockerHub](https://github.com/dongyubin/DockerHub)

### 配置多个镜像源

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.m.daocloud.io",
    "https://docker.xuanyuan.me",
    "https://docker.jiaxin.site"
  ]
}
```

Docker 会按顺序尝试，第一个失败会自动尝试下一个。

> [!info] 来源
> - [dongyubin/DockerHub：2026-08 国内可用 Docker 镜像源汇总](https://github.com/dongyubin/DockerHub) - GitHub
> - [超全Docker镜像源配置指南](https://juejin.cn/post/7476410894355185718) - 掘金

---

## 六、常见问题

### Q1：配置后不生效？

**排查步骤**：
```bash
# 1. 确认配置填在了 Docker Desktop 的 GUI 里（Settings → Docker Engine）
#    Docker Desktop 不读取 ~/.docker/daemon.json

# 2. 确认点了 Apply & Restart，并等 Docker 完全重启
# 点击菜单栏 Docker 图标 → Restart（必要时完全退出再打开）

# 3. 检查配置是否加载
docker info | grep "Registry Mirrors"

# 4. 确认当前 context 指向 Docker Desktop
docker context ls
docker context show
#   如果指向 WSL2/远程 daemon，配置在另一边
```

> [!warning] 常见误区
> - `~/.docker/daemon.json` 是 Docker **CLI** 的配置目录，Docker Desktop 的 daemon 不会读取它。
> - 显式指定上游地址会绕过镜像源：`docker pull docker.io/nginx`、`docker pull registry.hub.docker.com/library/nginx`。镜像源只对 `docker pull nginx` 这类简写生效。
> - `registry-mirrors` 只加速 Docker Hub（`docker.io`）；`ghcr.io`、`gcr.io`、`mcr.microsoft.com` 等不经过镜像源。

### Q2：JSON 格式错误导致 Docker 无法启动？

- **Docker Desktop（Mac/Windows）**：在 Settings → Docker Engine 填入非法 JSON 后，Apply & Restart 会直接报错并拒绝应用，不会"启动后才失败"。回到该面板修正 JSON 即可。
- **Linux 原生 dockerd**：`/etc/docker/daemon.json` 语法错误会导致 dockerd 启动失败。恢复方法：

```bash
# 用备份恢复（一键脚本会自动生成 .backup.<时间戳>）
sudo cp /etc/docker/daemon.json.backup.* /etc/docker/daemon.json

# 或临时删掉，让 dockerd 以默认配置启动
sudo rm /etc/docker/daemon.json
sudo systemctl restart docker
```

### Q3：镜像源都不可用？

**解决方案**：
1. 搜索最新的可用镜像源（镜像源会经常变化）
2. 尝试使用代理
3. 使用私有镜像仓库

### Q4：GUI 配置和命令行配置冲突？

**结论**：Docker Desktop 上不存在"冲突"——它只认 GUI（Settings → Docker Engine）里的配置，命令行写的 `~/.docker/daemon.json` 根本不生效。Linux 原生 dockerd 只认 `/etc/docker/daemon.json`。两种环境的配置入口互相独立，按环境选一种即可，不要混用。

### Q5：如何查看当前使用的镜像源？

```bash
docker info | grep -A 10 "Registry Mirrors"
```

### Q6：配置后拉取速度还是很慢？

**可能原因**：
1. 镜像源本身速度慢或不稳定
2. 本地网络问题
3. 镜像源没有该镜像

**解决方案**：
1. 尝试更换其他镜像源
2. 配置多个镜像源作为备份
3. 检查网络连接

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **配置方式选择**：
>    - Docker Desktop 统一用 GUI 配置（简单直观，且是唯一生效方式）
>    - 脚本/自动化场景用命令行配置，仅适用于 Linux 原生 dockerd
>
> 2. **镜像源管理**：
>    - 配置 2~4 个镜像源作为备份，Docker 会自动按顺序回退
>    - 定期检查镜像源可用性（变化很快，可能被限流/屏蔽）
>    - 失效源及时从配置中移除
>
> 3. **踩坑记录**：
>    - 误改 `~/.docker/daemon.json`，以为配好了，实际 Docker Desktop 根本不读
>    - 显式写 `docker pull docker.io/xxx` 导致镜像源被绕过
>    - 忘记点 Apply & Restart
>    - 镜像源失效没有及时发现
>
> 4. **最佳实践**：
>    - Docker Desktop 只用 GUI；Linux 才用 daemon.json
>    - 配置前用 `curl -s -o /dev/null -w "%{http_code}" https://<镜像>/v2/` 自测
>    - 配置后 `docker info | grep "Registry Mirrors"` 验证

---

## 相关文档

- [[镜像加速器vs代理-概念对比]] - 镜像加速器与代理概念对比
- [[Windows-DockerDesktop安装指南-国内网络版]] - Windows Docker Desktop 安装指南（国内网络版）
- [[../AI学习/00-索引/MOC]] - 知识库索引

---

## 参考资料

### 官方资源
- [Docker Daemon 配置文档](https://docs.docker.com/engine/daemon/) - Docker 官方
- [Docker dockerd 命令参考](https://docs.docker.com/engine/reference/commandline/dockerd/) - Docker 官方
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) - Docker 官方

### 社区资源
- [dongyubin/DockerHub：国内可用 Docker 镜像源汇总（持续更新）](https://github.com/dongyubin/DockerHub) - GitHub
- [2026 年 5 月国内可用 Docker 镜像源列表与配置方法](https://nanhubrain.csdn.net/6a3cf7d210ee7a33f2825e57.html) - CSDN
- [超全Docker镜像源配置指南](https://juejin.cn/post/7476410894355185718) - 掘金

### 第三方文档
- [DaoCloud 镜像站](https://www.daocloud.io/mirror) - DaoCloud
- [中科大镜像站](https://mirrors.ustc.edu.cn/help/dockerhub.html) - USTC（公网 Docker 镜像已停止，仅作历史参考）

---

## 更新记录

- 2026-08-08：核实并修正命令可用性
  - ⚠️ **修正核心错误**：Docker Desktop for Mac **不读取** `~/.docker/daemon.json`（那是 Docker CLI 配置目录）；命令行写 daemon.json 仅适用于 Linux 原生 dockerd（`/etc/docker/daemon.json`）。「方法二」已改为 Linux 专用说明。
  - 镜像源实测更新：移除已失效的 USTC / 上海交大，标注南京大学受限；新增 `docker.xuanyuan.me`、`docker.jiaxin.site` 等可用源。
  - 验证命令保留 `docker info | grep "Registry Mirrors"`、`docker pull` 测速；补充 `curl .../v2/` 自测方法。
  - 新增常见误区：显式 `docker pull docker.io/xxx` 会绕过镜像源；`registry-mirrors` 只加速 Docker Hub。

---

**最后更新**：2026-08-08
