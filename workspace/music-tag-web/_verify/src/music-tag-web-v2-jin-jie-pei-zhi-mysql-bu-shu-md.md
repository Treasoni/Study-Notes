> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu.md).

# Mysql 部署

本项目默认采用Sqlite数据库，sqlite 在并发写入时容易出现sqlite database is locked，因此支持提供替换成为 msyql 数据库

## &#x20; **方法一（推荐）**

在一个 yaml 文件中部署 MySQL 和 Music Tag Web 两个容器。

#### 编写 docker-compose.yml 文件

```yaml
version: '3'

services:
  # MySQL 数据库服务
  db:
    image: mysql:latest
    container_name: mysql
    restart: always
    command:  #使用 command 可以覆盖容器启动后默认执行的命令
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
    environment:
      MYSQL_ROOT_PASSWORD: your_root_password  # 修改为你的 MySQL 密码
      MYSQL_DATABASE: music_tag  # 数据库名称，无需修改
    volumes:
      - ./mysql-data:/var/lib/mysql  # 数据持久化存储目录

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
      - MYSQL_HOST=db  # 数据库主机名，使用服务名, 不需要修改
      - MYSQL_PASSWORD=your_root_password  # 与上面的 MySQL 密码一致
      - MYSQL_DB_NAME=music_tag  # 数据库名称，无需修改
      - MYSQL_USER=root  # MySQL 用户名，无需修改
      - MYSQL_PORT=3306  # MySQL 端口，无需修改
      - WORKER_NUM=8  # 后台任务工作线程数，可根据服务器性能调整
    restart: always
    depends_on:
      - db  # 依赖于 MySQL 服务
```

#### 修改配置说明

在启动容器前，你需要修改以下配置：<br>

1. **MySQL 密码**：将 `your_root_password` 替换为你自己的强密码。
2. **音乐文件目录**：将 `/path/to/your/music` 替换为你本地音乐文件所在的目录路径。
3. **配置文件目录**：将`/path/to/your/config` 替换为你配置文件存储目录，没有的话新建一个目录即可

提示：首次部署时，建议**不额外修改任何默认配置**。待系统完全启动并运行正常后，再根据实际需求针对性调整或新增配置，以便快速定位部署过程中可能出现的问题。

#### 启动容器

完成配置修改后，在项目目录下执行以下命令启动容器：

```bash
docker-compose up -d
```

这个命令会：

* 下载所需的镜像
* 创建并启动两个容器
* `-d` 参数表示在后台运行

\
验证部署

1. 检查容器是否正常运行：
2. 访问 Music Tag Web：\
   打开浏览器，访问 `http://你的服务器IP:8002`，应该能看到 Music Tag Web 的界面。

## 方法二

分开部署 mysql 和 music tag web 容器

## 安装Mysql

## &#x20;docker命令

```
docker run -p 3306:3306 --name mysql \
-v /your/mysql/data:/var/lib/mysql \
--restart=always \
-e MYSQL_ROOT_PASSWORD=your_root_password \
-e MYSQL_DATABASE=music_tag \
-d mysql:latest
```

## docker compose 命令

```yaml
version: '3'
services:
  db:
    image: mysql:latest
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: your_root_password
      MYSQL_DATABASE: music_tag
    volumes:
      - /your/mysql/data:/var/lib/mysql
```

```
修改为你的配置：
/your/mysql/data 改为你本地的目录，用于持久化 mysql 中的数据，重新部署容器数据不会丢失
your_root_password  改为你的 mysql 密码
```

## 在 Music Tag Web 中配置 mysql

如果你已经安装过 Music Tag Web 的 docker 应用，首先停止Music Tag Web 容器，重新在使用下面命令启动。/app/media 和/app/data 文件目录不需要删除。

## docker 命令

```
docker run -d \
  --name music-tag-web \
  -p 8002:8002 \
  -v /path/to/your/music:/app/media \
  -v /path/to/your/config:/app/data \
  -e MYSQL_HOST=192.168.1.24 \
  -e MYSQL_PASSWORD=123456 \
  -e MYSQL_DB_NAME=music_tag \
  -e MYSQL_USER=root \
  -e MYSQL_PORT=3306 \
  -e WORKER_NUM=8 \
  --restart always \
  xhongc/music_tag_web:latest
```

详细见 [Docker部署](/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md)

## docker compose 命令

```
version: '3'

services:
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      - /path/to/your/music:/app/media
      - /path/to/your/config:/app/data
    environment:
      - MYSQL_HOST=192.168.1.24 # mysql 局域网ip地址（没有可以不填，默认使用 sqlite）
      - MYSQL_PASSWORD=123456 # mysql密码（没有可以不填，默认使用 sqlite）
      - MYSQL_DB_NAME=music_tag # 数据表名称（没有可以不填，默认使用 sqlite）
      - MYSQL_USER=root # mysql 用户名（默认使用 root）
      - MYSQL_PORT=3306 # mysql 端口（默认使用 3306）
      - WORKER_NUM=8 #  后台并发执行任务的worker数量
    restart: always
```

详细见 [Docker Compose 部署](/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md)

```
MYSQL_HOST： mysql 局域网ip地址
MYSQL_PASSWORD： 上文配置的your_root_password
MYSQL_DB_NAME： 配置的数据库名称， 上文中为：music_tag
MYSQL_USER：默认为 root， 如果你没额外配置。
MYSQL_PORT： 默认端口为 3306
```

**配置完成后打不开 music tag web？**

请检查：

1. MySQL 端口是否暴露出来
2. music tag web 里是否能访问到 mysql
3. 如果是原先就部署有 mysql，是否创建了 music\_tag 的数据库
4. 检查数据库的配置是否有拼写错误
5. mysql 版本太新了， 可以使用 mysql:5.7

基本能解决 90% 的问题了
