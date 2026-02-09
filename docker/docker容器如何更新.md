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
docker compose pull
```

这一步只是下载最新版本镜像，**不会影响正在运行的容器**。


### 第二步：重建并启动

```bash
docker compose up -d
```

它会：

- 检测镜像是否有更新
- 停止旧容器
- 用新镜像创建新容器
- 数据不会丢（前提是你有挂载 volume 或你的 docker-compose.yml 的存放路径没变）


### 第三步（可选）：清理旧镜像

```bash
docker image prune -f
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
docker compose up -d --force-recreate
```

或者只更新特定服务：

```bash
docker compose up -d 服务名
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
