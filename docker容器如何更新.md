---
created: 2026-02-09
tags:
  - docker
---
我给你分 **两种情况** 讲清楚（你基本就在这两种里）：


# 1. 你是用 `docker compose` 部署的（推荐方式）

先进入你的项目目录（有 `docker-compose.yml` 的地方）：

```bash
cd /你的项目目录
```


## 1.1 第一步：拉取最新镜像

```bash
docker compose pull
```

这一步只是下载新版本镜像  
不会影响正在运行的容器


## 1.2 第二步：重建并更新

```bash
docker compose up -d
```

它会：

- 检测镜像有更新
- 停止旧容器
- 用新镜像创建新容器
- 数据不会丢（前提是你有挂载 volume）


## ✅ 第三步（可选）：清理旧镜像

`docker image prune -f`

或者：

`docker system prune -a`

⚠️ 第二个会删所有未使用镜像，慎用

---

# 二、你是用 `docker run` 启动的

那更新步骤是：

---

## 1️⃣ 先拉新镜像

`docker pull 镜像名`

比如：

`docker pull ghcr.io/suwayomi/tachidesk:latest`

---

## 2️⃣ 删除旧容器

⚠️ 先确认你有挂载 volume！

`docker ps`

然后：

`docker stop 容器名 docker rm 容器名`

---

## 3️⃣ 用原来的 run 命令重新创建

把你当初的 `docker run` 命令再执行一遍。

---

# 如何确认你是不是 compose 部署？

执行：

`docker ps`

如果看到：

`suwayomi_suwayomi_1`

这种带 `_1` 的，通常是 compose。

或者：

`docker inspect 容器名 | grep -i compose`

---