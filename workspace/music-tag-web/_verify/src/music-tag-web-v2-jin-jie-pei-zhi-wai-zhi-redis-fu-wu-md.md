> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md).

# 外置Redis服务

容器本身就会启动一个 redis，如果你不需要**外置**的 redis，可以不进行此项的配置。

## 方法一

已有 redis 容器，将其配置 music tag web 启动命令的环境变量中

如果你的服务器上已有 Redis 服务运行，可以通过设置环境变量来指定 Redis 地址。对于不熟悉 Redis 或当前环境中未安装 Redis 的用户，此部分配置可以跳过。

<figure><img src="https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F7Xvq7A6sXOynLc1gP40l%2Fimage.png?alt=media&amp;token=8c97d304-79a6-47b5-87d8-62393fc3d020" alt=""><figcaption></figcaption></figure>

为了配置 Redis，你需要在环境变量中添加 `REDIS_HOST`，其默认端口为 6379。如果需要使用不同的端口，则应同时设置 `REDIS_PORT` 变量。`REDIS_HOST` 可以是局域网内的 IP 地址，也可以是容器网络中的连接地址，请确保所提供的地址和端口能够正常访问 Redis 服务。

如果你 redis 设置了密码，需要配置 REDIS\_PASSWORD 环境变量

## 方法二

在一个yaml 文件中一起部署 redis 和 music tag web

```yaml
version: '3'

services:
  # MySQL 数据库服务
  redis:
    image: redis:latest
    container_name: redis
    restart: always
    ports:
      - "6379:6379"  # 主机端口:容器端口
    command: redis-server --requirepass yourpassword # 设置密码

  # Music Tag Web 服务
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"  # 主机端口:容器端口
    volumes:
      - /path/to/your/music:/app/media  # 修改为你的音乐文件目录
      - /path/to/your/config:/app/data  # 修改为你的配置文件存储目录
    environment:
      - REDIS_HOST=redis  # 数据库主机名，使用服务名, 不需要修改
      - REDIS_PASSWORD=yourpassword  # 与上面的 redis 密码一致
      - REDIS_PORT=6379  # redis 端口，无需修改
    restart: always
    depends_on:
      - redis  # 依赖于 redis 服务
```

REDIS\_PASSWORD： 为 redis 容器的密码
