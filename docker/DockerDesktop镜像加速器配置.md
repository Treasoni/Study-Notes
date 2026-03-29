---
tags: [docker, mac, 镜像加速, registry-mirrors, daemon.json]
created: 2026-03-04
updated: 2026-03-04
---

# Docker Desktop Mac 镜像加速器配置

> [!info] 概述
> **Docker 镜像加速器可以加速从 Docker Hub 拉取镜像的速度**，在国内网络环境下配置加速器是必要操作。本文档介绍 Mac 上 Docker Desktop 的两种配置方法：GUI 界面配置和命令行配置。

## 快速导航

| 我想... | 跳转章节 |
|---------|----------|
| 了解为什么需要加速器 | [[DockerDesktop镜像加速器配置#一、为什么需要镜像加速器]] |
| 通过 GUI 界面配置 | [[DockerDesktop镜像加速器配置#二、方法一：Docker Desktop GUI 配置]] |
| 通过命令行配置 | [[DockerDesktop镜像加速器配置#三、方法二：命令行配置]] |
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
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn"
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

## 三、方法二：命令行配置

### 3.1 配置文件位置

Mac 上 Docker Desktop 的 daemon.json 配置文件位置：

```bash
# 用户级配置（推荐）
~/.docker/daemon.json

# 如果文件不存在，需要创建
```

### 3.2 创建/编辑配置文件

```bash
# 方法1：使用 vim 编辑
vim ~/.docker/daemon.json

# 方法2：使用 nano 编辑
nano ~/.docker/daemon.json

# 方法3：直接写入（如果文件不存在）
cat > ~/.docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF
```

### 3.3 完整配置示例

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn"
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
# 方法1：通过命令行重启 Docker Desktop
osascript -e 'quit app "Docker"'
sleep 2
open -a Docker

# 方法2：手动重启
# 点击菜单栏 Docker 图标 → Restart
```

### 3.5 一键配置脚本

```bash
#!/bin/bash
# Docker Desktop Mac 镜像加速器一键配置脚本

CONFIG_FILE="$HOME/.docker/daemon.json"

# 备份原配置
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d%H%M%S)"
    echo "已备份原配置文件"
fi

# 写入新配置
cat > "$CONFIG_FILE" << 'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF

echo "配置文件已更新: $CONFIG_FILE"
echo "请重启 Docker Desktop 使配置生效"
```

> [!info] 来源
> - [MAC Docker镜像源配置方法](https://m.php.cn/faq/1673553.html) - php.cn
> - [Docker dockerd 命令参考](https://docs.docker.com/engine/reference/commandline/dockerd/) - Docker 官方

---

## 四、验证配置

### 4.1 检查配置是否生效

```bash
# 方法1：查看 docker info 输出
docker info | grep -A 5 "Registry Mirrors"

# 预期输出：
# Registry Mirrors:
#  https://docker.m.daocloud.io/
#  https://docker.1ms.run/
#  https://docker.mirrors.ustc.edu.cn/
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

# 查看配置文件内容
cat ~/.docker/daemon.json
```

---

## 五、可用镜像源列表

### 国内镜像源

| 镜像源 | 地址 | 状态 |
|--------|------|------|
| **DaoCloud** | `https://docker.m.daocloud.io` | ✅ 可用 |
| **1ms.run** | `https://docker.1ms.run` | ✅ 可用 |
| **中科大** | `https://docker.mirrors.ustc.edu.cn` | ✅ 可用 |
| **南京大学** | `https://docker.nju.edu.cn` | ⚠️ 需验证 |
| **上海交大** | `https://docker.mirrors.sjtug.sjtu.edu.cn` | ⚠️ 需验证 |

> [!warning] 注意
> 镜像源可用性会变化，如果某个源不可用，请尝试其他源或搜索最新的可用镜像源。

### 配置多个镜像源

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://docker.mirrors.ustc.edu.cn",
    "https://docker.nju.edu.cn"
  ]
}
```

Docker 会按顺序尝试，第一个失败会自动尝试下一个。

> [!info] 来源
> - [超全Docker镜像源配置指南](https://juejin.cn/post/7476410894355185718) - 掘金
> - [如何配置 Docker 加速器](https://m.blog.csdn.net/weixin_51782176/article/details/146505865) - CSDN

---

## 六、常见问题

### Q1：配置后不生效？

**排查步骤**：
```bash
# 1. 检查 JSON 格式是否正确
cat ~/.docker/daemon.json | python3 -m json.tool

# 2. 检查 Docker Desktop 是否重启
# 点击菜单栏 Docker 图标 → Restart

# 3. 检查配置是否加载
docker info | grep "Registry Mirrors"
```

### Q2：JSON 格式错误导致 Docker 无法启动？

```bash
# 恢复备份配置
cp ~/.docker/daemon.json.backup.* ~/.docker/daemon.json

# 或者删除配置文件重新配置
rm ~/.docker/daemon.json
# 然后通过 Docker Desktop GUI 重新配置
```

### Q3：镜像源都不可用？

**解决方案**：
1. 搜索最新的可用镜像源（镜像源会经常变化）
2. 尝试使用代理
3. 使用私有镜像仓库

### Q4：GUI 配置和命令行配置冲突？

**优先级**：Docker Desktop GUI 配置会覆盖命令行配置。

**建议**：统一使用 GUI 配置，避免混用。

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
>    - 新手推荐 GUI 配置，简单直观
>    - 脚本/自动化场景用命令行配置
>
> 2. **镜像源管理**：
>    - 配置多个镜像源作为备份
>    - 定期检查镜像源可用性
>    - 镜像源会变化，需要及时更新
>
> 3. **踩坑记录**：
>    - JSON 格式错误导致 Docker 无法启动
>    - 忘记重启 Docker Desktop
>    - 镜像源失效没有及时发现
>
> 4. **最佳实践**：
>    - 修改前备份原配置
>    - 使用 JSON 格式化工具验证
>    - 配置后验证是否生效

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
- [Mac桌面Docker配置镜像地址指南](https://m.blog.csdn.net/wstever/article/details/155319540) - CSDN
- [DockerDesktop配置镜像](https://m.blog.csdn.net/csdn1027719307/article/details/149422544) - CSDN
- [超全Docker镜像源配置指南](https://juejin.cn/post/7476410894355185718) - 掘金
- [如何配置 Docker 加速器](https://m.blog.csdn.net/weixin_51782176/article/details/146505865) - CSDN
- [MAC Docker镜像源配置方法](https://m.php.cn/faq/1673553.html) - php.cn
- [配置镜像仓库镜像的指南](https://m.blog.csdn.net/wilsonwong/article/details/154292816) - CSDN

### 第三方文档
- [DaoCloud 镜像站](https://www.daocloud.io/mirror) - DaoCloud
- [中科大镜像站](https://mirrors.ustc.edu.cn/help/dockerhub.html) - USTC

---

**最后更新**：2026-03-04
