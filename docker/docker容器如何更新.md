---
created: 2026-02-09
updated: 2026-02-09
tags:
  - docker
---

我给你分 **两种情况** 讲清楚（你基本就在这两种里）：

---

# 1. 你是用 `docker compose` 部署的（推荐方式）

先进入你的项目项目目录（有 `docker-compose.yml` 的地方）：

```bash
cd /你的项目目录
```


## 1.1 标准更新流程

### 第一步：拉取最新镜像

```bash
sudo docker compose pull
```

这一步只是下载最新版本镜像，**不会影响正在运行的容器**。


### 第二步：重建并启动

```bash
sudo docker compose up -d
```

它会：

- 检测镜像是否有更新
- 停止旧容器
- 用新镜像创建新容器
- 数据不会丢（前提是你有挂载 volume 或你的 docker-compose.yml 的存放路径没变）


### 第三步（可选）：清理旧镜像

```bash
sudo docker image prune -f
```

或者清理所有未使用的资源：

```bash
docker system prune -a
```

⚠️ 第二个会删所有未使用镜像，慎用！


## 1.2 快捷更新命令（一步到位）

如果你想省事，可以直接用一条命令：

```bash
docker compose up -d --pull always
```

这个命令会自动拉取最新镜像并更新容器。


## 1.3 强制重建

如果需要强制重建容器（比如修改了环境变量）：

```bash
sudo docker compose up -d --force-recreate
```

或者只更新特定服务：

```bash
sudo docker compose up -d 服务名
```


## 1.4 更新前备份（强烈推荐）

```bash
# 备份当前 docker-compose.yml
cp docker-compose.yml docker-compose.yml.bak

# 如果有重要数据，先备份 volume
# 例如：
# docker run --rm -v mydata_volume:/data -v $(pwd):/backup alpine tar czf /backup/data_backup.tar.gz /data
```


---

# 2. 你是用 `docker run` 启动的

更新前**务必确认你有挂载 volume**，否则数据会丢失！


## 2.1 第一步：拉取新镜像

```bash
docker pull 镜像名
```

比如：

```bash
docker pull ghcr.io/suwayomi/tachidesk:latest
```


## 2.2 第二步：查看并保存当前配置

**重要**：你需要记录原来的运行参数，否则重新创建会很麻烦。

查看容器的详细配置：

```bash
docker inspect 容器名 | less
```

或者只查看挂载的 volume：

```bash
docker inspect 容器名 | grep -A 10 "Mounts"
```

💡 **建议**：把你的 `docker run` 命令保存到一个 shell 脚本里，方便以后更新。


## 2.3 第三步：停止并删除旧容器

```bash
docker stop 容器名
docker rm 容器名
```

或者一步到位：

```bash
docker rm -f 容器名
```


## 2.4 第四步：用原来的 run 命令重新创建

把你当初的 `docker run` 命令再执行一遍即可。


## 2.5 使用 docker inspect 获取 run 命令

如果你忘记原来的命令，可以用这个技巧：

```bash
# 安装 runlike 工具（如果还没有）
docker pull assaflavidine/runlike
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavidine/runlike 容器名
```

这会输出重建该容器所需的完整命令。


---

# 3. 如何确认你是不是 compose 部署？

执行：

```bash
docker ps
```

如果看到：

```bash
suwayomi_suwayomi_1
```

这种带 `_1` 的，通常是 compose。

或者：

```bash
docker inspect 容器名 | grep -i compose
```

---

# 4. 如何验证更新成功？

## 4.1 检查镜像版本

```bash
docker images | grep 镜像名
```

查看 `CREATED` 时间确认是否是最新的。


## 4.2 检查容器状态

```bash
docker ps
```

确保容器状态是 `Up`。


## 4.3 进入容器查看应用版本

```bash
docker exec 容器名 应用版本命令
```

例如：

```bash
docker exec nextcloud occ status
docker exec nginx nginx -v
docker exec redis-server redis-server --version
```


## 4.4 查看容器日志

```bash
docker logs 容器名 --tail 50
```

查看最近的日志确认没有错误。


---

# 5. 如何回滚到旧版本？

如果更新后出现问题，可以回滚：

## 5.1 Compose 方式回滚

```bash
# 查看本地所有镜像版本
docker images | grep 镜像名

# 修改 docker-compose.yml，指定旧版本标签
# 然后重新部署
docker compose up -d
```


## 5.2 Docker run 方式回滚

```bash
# 停止新容器
docker stop 容器名
docker rm 容器名

# 使用旧镜像重新创建
docker run 镜像名:旧版本号 ...其他参数
```


---

# 6. 数据安全检查

更新前务必检查 volume 挂载情况：

```bash
docker inspect 容器名 | grep -A 20 "Mounts"
```

确认你的重要数据目录都在 `Mounts` 中，否则更新容器后数据会丢失！


---

# 7. 常见问题

### Q: 更新后容器启动失败怎么办？

A: 查看日志排查问题：
```bash
docker logs 容器名
```

如果无法修复，可以回滚到旧版本。


### Q: 如何批量更新所有容器？

A: 如果都是用 compose 部署的，可以写个脚本：

```bash
#!/bin/bash
for dir in */; do
  if [ -f "$dir/docker-compose.yml" ]; then
    echo "Updating $dir"
    cd "$dir"
    docker compose pull && docker compose up -d
    cd ..
  fi
done
```


### Q: 遇到权限问题怎么办？

A: 有时更新后文件权限会改变，可以修复：

```bash
docker exec 容器名 chown -R 用户:组 /path/to/data
```


---

# 8. 自动更新工具

如果你不想手动更新，可以考虑这些工具：

## 8.1 Watchtower

自动监控并更新容器：

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower
```

它会自动检测镜像更新并重建容器。


## 8.2 Portainer

可视化管理界面，支持一键更新：

```bash
docker volume create portainer_data

docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  cr.portainer.io/portainer/portainer-ce:latest
```

访问 `https://你的IP:9443` 即可管理。

---

# 9. 如何切换镜像版本

> [!info] 概述
> **一句话定义**：通过指定不同的镜像标签（tag）或摘要（digest）来使用特定版本的镜像构建容器。
> **🎯 比喻**：就像手机 App Store 里选择「历史版本」下载旧版应用，而不是只能下载最新版。

## 9.1 查看可用的镜像版本

### 方法一：Docker Hub 网页查看

1. 打开 [Docker Hub](https://hub.docker.com)
2. 搜索你想要的镜像（如 `nginx`、`redis`）
3. 点击 **Tags** 标签页
4. 浏览或搜索特定版本

### 方法二：命令行查看本地已有镜像

```bash
# 查看本地所有镜像
docker images

# 查看特定镜像的所有版本
docker images 镜像名
```

例如：
```bash
$ docker images nginx
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    605c7716cdda   2 weeks ago    141MB
nginx        1.25.0    605c7716cdda   2 weeks ago    141MB
nginx        1.24.0    a7c8739d1a3d   3 weeks ago    141MB
nginx        alpine    8e756f3fdd6a   1 week ago     23.5MB
```

## 9.2 拉取特定版本的镜像

### 使用标签（Tag）拉取

```bash
docker pull 镜像名:标签
```

例如：
```bash
# 拉取 nginx 1.25 版本
docker pull nginx:1.25.0

# 拉取 Ubuntu 22.04
docker pull ubuntu:22.04

# 拉取 Alpine 版本（更小体积）
docker pull nginx:alpine
```

> [!warning] 注意
> 如果不指定标签，Docker 默认使用 `:latest` 标签，但这**不代表**一定是最新版本！

### 使用摘要（Digest）拉取（推荐生产环境）

摘要（Digest）是镜像的**不可变标识符**，确保每次拉取的镜像完全相同。

```bash
# 先拉取镜像获取 digest
docker pull nginx:1.25.0

# 输出中会显示类似：
# Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30

# 使用 digest 拉取（确保版本完全一致）
docker pull nginx@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

## 9.3 切换容器使用的镜像版本

### Compose 方式（推荐）

**第一步**：修改 `docker-compose.yml` 中的镜像版本

```yaml
services:
  web:
    # 从 nginx:latest 改为指定版本
    image: nginx:1.25.0
```

**第二步**：重新部署

```bash
# 拉取新版本镜像
docker compose pull

# 重建并启动
docker compose up -d
```

或者一步到位：
```bash
docker compose up -d --pull always
```

### Docker run 方式

**第一步**：拉取目标版本镜像
```bash
docker pull 镜像名:目标版本
```

**第二步**：停止并删除旧容器
```bash
docker stop 容器名
docker rm 容器名
```

**第三步**：使用新镜像启动容器
```bash
# 把原来的命令中的镜像标签改为新版本
docker run -d --name 容器名 -p 80:80 镜像名:新版本
```

## 9.4 最佳实践

### ❌ 不要依赖 `latest` 标签

```yaml
# 不推荐
image: nginx:latest

# 推荐
image: nginx:1.25.0
```

**原因**：
- `latest` 只表示「最后推送的镜像」，不一定是「最新版本」
- 无法追溯具体版本，出问题难以回滚
- 团队成员可能拉到不同的镜像

### ✅ 生产环境使用 Digest

```yaml
# 最稳定的方式
image: nginx@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

**优点**：确保镜像内容永不改变

### ✅ 使用 Labels 记录版本信息

在 Dockerfile 中添加：
```dockerfile
LABEL org.opencontainers.image.version="1.0.2"
LABEL org.opencontainers.image.created="2024-01-15"
```

查看镜像的 labels：
```bash
docker inspect --format='{{json .Config.Labels}}' 镜像名
```

### 常用 OCI 标准 Labels

| Label | 说明 |
|-------|------|
| `org.opencontainers.image.version` | 软件版本 |
| `org.opencontainers.image.created` | 构建时间 |
| `org.opencontainers.image.authors` | 作者信息 |
| `org.opencontainers.image.source` | 源代码地址 |
| `org.opencontainers.image.description` | 描述信息 |

## 9.5 常见问题

### Q: 如何查看远程仓库有哪些标签？

A: 可以通过 Docker Hub 网页查看，或使用 API：
```bash
# 使用 Docker Hub API（需要认证）
curl -s "https://hub.docker.com/v2/repositories/library/nginx/tags/" | jq '.results[].name'
```

### Q: 切换版本后数据会丢失吗？

A: 只要你的 volume 挂载正确，数据不会丢失。切换版本前务必确认挂载配置：
```bash
docker inspect 容器名 | grep -A 20 "Mounts"
```

### Q: 本地有多个版本的镜像，如何删除不需要的？

A:
```bash
# 删除特定镜像
docker rmi 镜像名:标签

# 清理所有未使用的镜像
docker image prune -a
```

> [!info] 📚 来源
> - [Docker 官方文档 - docker image pull](https://docs.docker.com/reference/cli/docker/image/pull/)
> - [Docker Blog - Using Tags and Labels](https://www.docker.com/blog/docker-best-practices-using-tags-and-labels-to-manage-docker-image-sprawl/)
> - [Docker Hub - Managing Tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/tags/)
