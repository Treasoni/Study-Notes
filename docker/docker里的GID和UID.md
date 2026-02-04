---
tags:
  - docker
---
# 1. Docker 里的 UID / GID

> 先纠正一个小点：  
> **Docker 里常见的是 UID / GID> 
> - **UID**：User ID（用户）
> - **GID**：Group ID（用户组）
> - **PID**：进程 ID（跟权限关系不大）

你大概率是看到过这种👇

```bash
environment:
  - PUID=1000
  - PGID=1000

```

# 2. UID / GID 是干嘛的？

一句话：

> **让容器里的程序，用“宿主机的某个用户身份”去读写文件**

Docker 容器 ≠ 虚拟机  
容器里操作文件时，**最终还是在操作宿主机的文件系统**

如果你不管 UID/GID，常见后果是：

- 容器能跑
- 但生成的文件：
    - 宿主机打不开
    - 权限全是 `root`
    - 删都删不掉 😅

---

# 3. 没设置 UID / GID 会发生什么？

举个真实案例（你一定遇到过）

`docker run -v /data/downloads:/downloads some-image`

容器里程序默认是 **root（UID=0）**

结果宿主机上：

`ls -l /data/downloads`

`-rw-r--r-- 1 root root xxx.mkv`

然后你用普通用户：

`rm xxx.mkv`

❌ **Permission denied**


# 4. 设置 UID / GID 后发生了什么？

假设你宿主机用户是：

```bash
id zhq

```
```bash
uid=1000(zhq) gid=1000(zhq)
```

Docker Compose：
```bash
services:
  app:
    image: some-image
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - /data/downloads:/downloads
```
此时：

- 容器里的程序  
    👉 **以 UID=1000 的身份运行**
- 写出来的文件  
    👉 宿主机的 `zhq` 用户能直接操作

`-rw-r--r-- 1 zhq zhq xxx.mkv`

✔ 正常人类体验

## 4.1 一个你会常用的实际场景（媒体/下载类）

像这些容器：

- qBittorrent
- Transmission
- Sonarr / Radarr
- NASTools
- Jellyfin / Emby

**90% 都要求你设置 PUID / PGID**

否则：

- 刮削失败
- 重命名失败
- 自动整理失败
- 日志一堆 Permission denied