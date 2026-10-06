> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md).

# 容器自动更新

## Music Tag Web Docker 容器自动更新教程

### 📋 什么是自动更新？

Music Tag Web 提供了一键自动更新功能，当有新版本发布时，你可以通过简单的点击操作，让系统自动完成以下工作：

* ✅ 下载最新版本的程序
* ✅ 停止旧版本容器
* ✅ 启动新版本容器
* ✅ 清理旧版本镜像，释放磁盘空间
* ✅ 保留你的所有数据和配置

整个过程无需手动操作复杂的命令，确保你的应用始终运行在最新、最安全的版本。

### 🚀 使用方法

#### 通过 Web 界面更新（推荐）

**步骤 1：检查是否有新版本**

1. 登录 Music Tag Web 管理界面
2. 点击左侧菜单的「系统设置」→「系统信息」
3. 查看「系统版本」区域
4. 如果有新版本可用，会显示「检查更新」按钮

**步骤 2：执行更新**

1. 点击「检查更新」按钮
2. 在弹出的对话框中，确认容器名称（通常默认为 `music-tag-web`）
3. 点击「确认」按钮
4. 等待更新完成（通常需要 1-3 分钟）
5. 更新成功后，系统会显示成功提示

**步骤 3：验证更新**

* 刷新页面，检查版本号是否已更新
* 确认所有功能正常工作
* 检查音乐库数据是否完整

### ⚙️ 前置准备

#### 0. 🔧 重要：挂载 Docker Socket

**如果你想使用自动更新功能，在首次部署时必须挂载 Docker Socket。**

Docker Socket 是 Docker 守护进程的通信接口，挂载后，容器内的程序才能控制宿主机的 Docker，实现自动更新。\
**使用 Docker Compose 部署（推荐）**

在你的 `docker-compose.yml` 文件中添加 Docker Socket 挂载：

```yaml
version: '3'

services:
  music-tag-web:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      # 数据持久化
      - /path/to/your/music:/app/media
      - /path/to/your/config:/app/data
      - /path/to/your/download:/app/download
      # ⭐ 重要：挂载 Docker Socket，用于自动更新功能
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
```

* 将 `/path/to/your/music` 替换为你的 NAS 上音乐文件夹的绝对路径。
* 将 `/path/to/your/config` 替换为你新建的一个目录路径，用于存放应用程序的配置文件。
* `/path/to/your/download` 替换为你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录

**关键配置：**

```yaml
- /var/run/docker.sock:/var/run/docker.sock
```

启动服务：

```bash
docker-compose up -d
```

**使用 docker run 命令部署**

如果使用 `docker run` 命令启动，需要添加 `-v` 参数挂载 Docker Socket：

```bash
docker run -d \
  --name music-tag-web \
  -p 8002:8002 \
  -v /path/to/data:/app/data \
  -v /path/to/media:/app/media \
  -v /path/to/download:/app/download \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --restart unless-stopped \
  xhongc/music_tag_web:latest
```

**关键参数：**

```bash
-v /var/run/docker.sock:/var/run/docker.sock
```

#### 🔍 检查是否正确挂载

部署完成后，可以通过以下方式检查 Docker Socket 是否正确挂载：

&#x20;

**方法 1：查看容器配置**

```bash
docker inspect music-tag-web | grep docker.sock
```

应该看到类似输出：

```
"Source": "/var/run/docker.sock",
"Destination": "/var/run/docker.sock",
```

**方法 2：进入容器检查**

```bash
# 进入容器
docker exec -it music-tag-web bash

# 检查 socket 文件是否存在
ls -l /var/run/docker.sock
```

应该看到：

```
srw-rw---- 1 root docker 0 Dec  2 10:00 /var/run/docker.sock
```

#### ⚠️ 没有挂载会怎样？

如果没有挂载 Docker Socket，使用自动更新功能时会出现以下错误：

* ❌ "Docker客户端初始化失败"
* ❌ "无法连接到 Docker daemon"
* ❌ 更新按钮点击后没有反应

**解决方法：**

1. 停止并删除现有容器
2. 按照上述配置重新部署，添加 Docker Socket 挂载
3. 重新启动容器

```bash
# 停止容器
docker stop music-tag-web

# 删除容器
docker rm music-tag-web

# 使用正确的配置重新启动（添加 docker.sock 挂载）
docker-compose up -d
# 或使用 docker run 命令，确保包含 -v /var/run/docker.sock:/var/run/docker.sock
```

#### 🔐 安全说明

**为什么需要挂载 Docker Socket？**

Docker Socket 是 Docker 的控制接口，挂载后容器可以：

* 查看其他容器状态
* 启动/停止容器
* 拉取/删除镜像
* 创建新容器

#### 1. 确认容器名称

在更新前，你需要知道你的容器名称。默认情况下是 `music-tag-web`，但如果你使用了自定义名称，需要使用正确的名称。

&#x20;

**查看容器名称的方法：**

```bash
docker ps
```

在输出的 `NAMES` 列中找到 Music Tag Web 对应的容器名称。

#### 2. 确保数据持久化

**重要提醒：** 在首次安装时，请确保已经正确配置了数据卷，这样更新后你的数据不会丢失。

&#x20;

**检查数据卷配置：**

&#x20;

如果使用 Docker Compose，检查 `docker-compose.yml` 文件：

```yaml
services:
  web:
    volumes:
      - /path/to/your/music:/app/media
      - /path/to/your/config:/app/data
      - /path/to/your/download:/app/download
```

如果使用 `docker run` 命令，确保包含了 `-v` 参数：

```bash
docker run -d \
  -v /path/to/data:/app/data \
  -v /path/to/media:/app/media \
  -v /path/to/download:/app/download \
  ...
```

#### 3. 网络要求

自动更新需要从互联网下载最新版本，请确保：

* ✅ 服务器可以访问互联网
* ✅ 可以连接到 Docker Hub（或配置的镜像源）
* ✅ 网络速度稳定（新版本镜像通常在 500MB-1GB）

**如果网络受限：**

&#x20;

可以预先下载 Watchtower 镜像：

```bash
docker pull containrrr/watchtower
```

或使用国内镜像源：

```bash
# 使用阿里云镜像源
docker pull registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest
docker tag registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest containrrr/watchtower:latest
```

### 4.&#x20;

### 🔍 常见问题

#### ❓ 更新会丢失我的数据吗？

**不会。** 只要你正确配置了数据卷（volumes），所有数据都会保留，包括：

* 音乐库数据
* 用户设置
* 历史记录
* 上传的封面图片

#### ❓ 更新需要多长时间？

**通常 1-5 分钟**，具体取决于：

* 网络速度
* 新版本镜像大小
* 服务器性能

更新期间服务会短暂中断，建议在低峰时段进行。

#### ❓ 更新失败怎么办？

1. **查看错误提示**：Web 界面会显示具体的错误信息
2. **检查容器日志**：

   ```bash
   docker logs music-tag-web
   ```
3. **手动重启容器**：

   ```bash
   docker restart music-tag-web
   ```
4. **回滚到旧版本**：如果新版本有问题，可以使用旧镜像重新启动

#### ❓ 如何知道有新版本发布？

有以下几种方式：

1. **Web 界面提示**：系统会在「系统信息」页面显示「检查更新」按钮
2. **关注项目更新**：
   * GitHub Release 页面
   * 项目官方公告
   * 相关社区讨论

#### ❓ 可以自动定时更新吗？

**可以。** 如果你希望系统自动保持最新版本，可以设置定时任务：

&#x20;

**方法 1：使用系统 crontab**

```bash
# 编辑定时任务
crontab -e

# 添加以下内容（每天凌晨 3 点自动更新）
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music-tag-web
```

**方法 2：使用 Watchtower 监控模式**

&#x20;

启动一个持续运行的 Watchtower 容器，自动检测并更新：

```bash
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 86400 \
  music-tag-web
```

参数说明：

* `--interval 86400`：每 24 小时检查一次更新
* `--cleanup`：自动清理旧镜像

### 📊 更新流程

```
检查新版本
    ↓
点击「检查更新」
    ↓
确认容器名称
    ↓
系统自动执行：
  1. 下载最新镜像
  2. 停止旧容器
  3. 启动新容器
  4. 清理旧镜像
    ↓
显示更新结果
    ↓
验证功能正常
```

### 💡 最佳实践

1. **定期更新**：建议每月检查一次更新，获取最新功能和安全修复
2. **避免高峰期**：在用户较少的时间段进行更新
3. **保持备份**：重要数据定期备份，避免意外情况
4. **阅读更新说明**：更新前查看版本更新日志，了解新功能和变更
5. **测试验证**：更新后测试主要功能，确保一切正常

### 📞 获取帮助

如果在更新过程中遇到问题：

1. 查看系统日志：系统设置 → 运行日志
2. 查看任务记录：任务管理 → 审计日志
3. 检查 Docker 日志：`docker logs music-tag-web`
4. 访问项目 GitHub Issues 页面寻求帮助
5. 加入用户社区讨论

### 📝 总结

现在就去检查是否有新版本可用吧！保持系统更新，享受最新功能和最佳性能。
