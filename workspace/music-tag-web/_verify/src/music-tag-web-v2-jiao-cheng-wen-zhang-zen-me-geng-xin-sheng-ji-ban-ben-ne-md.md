> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/zen-me-geng-xin-sheng-ji-ban-ben-ne.md).

# 怎么更新/升级 版本呢？

发现作者更新了新版本，不知道怎么更新，好着急

提供3种方式进行更新

1. **docker pull 方式**

**步骤一：拉取新版本镜像**

首先，你需要从 Docker Hub 或其他镜像仓库中拉取应用程序的新版本镜像。假设我们想要更新到版本 2.0.1，那么命令如下：

```
docker pull xhong/music_tag_web:2.0.1
```

**步骤二：停止并删除旧容器**

接下来，你需要停止正在运行的旧版容器，并将其删除。这可以通过以下命令完成：

```
# 停止旧容器
docker stop my-music-tag-web
# 删除旧容器
docker rm my-music-tag-web
```

确保替换 `my-music-tag-web` 为你的实际容器名称或容器ID。

docker ps 命令查询容器 ID

**步骤三：使用新镜像启动新容器**

使用[快速开始](/music-tag-web-v2/kuai-su-kai-shi.md)中的命令用新镜像重新部署

2. **使用 Docker Compose 更新**

对于使用 Docker Compose 的项目，更新过程更加简化。Docker Compose 可以自动处理容器的停止、删除和重新创建。以下是基本步骤：

**拉取新镜像：**

&#x20;`docker-compose pull`&#x20;

**更新并重启服务：**

&#x20;`docker-compose up -d`&#x20;

如果需要完全清理旧资源，包括容器、网络但不包括卷（数据持久化存储）：

`docker-compose down`&#x20;

若要连同卷一起删除，请添加 -v 选项：

`docker-compose down -v`&#x20;

确保所有重要数据都已正确挂载到持久化存储上，防止数据丢失。&#x20;

3. **watchtower 自动更新**

安装第三方的软件自动更新

```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music_tag_web
```

命令末尾 music\_tag\_web 是正在启动的容器名称，改为你实际的容器名称。
