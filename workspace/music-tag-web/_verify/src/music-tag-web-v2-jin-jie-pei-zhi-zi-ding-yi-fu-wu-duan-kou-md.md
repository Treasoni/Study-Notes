> For the complete documentation index, see [llms.txt](https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/zi-ding-yi-fu-wu-duan-kou.md).

# 自定义服务端口

如果你使用网络模式host，出现端口冲突，可以进行自定义端口号

#### 一、自定义服务端口（解决端口冲突）

当使用 `host` 网络模式出现端口冲突时，可通过修改环境变量自定义端口。若使用 `bridge` 模式，通常无需修改容器内端口，仅需映射主机端口即可。

***

#### 二、核心环境变量说明（容器内端口）

以下变量用于定义容器内部服务的端口，修改后仅影响容器内部，不直接映射到主机。

| 环境变量                 | 作用说明             | 默认值  | 特殊说明                   |
| -------------------- | ---------------- | ---- | ---------------------- |
| **GUNICORN\_PORT**   | 后端服务端口           | 8001 | 选填                     |
| **NGINX\_PORT**      | Nginx代理后的后端服务端口  | 8002 | 选填                     |
| **SUPERVISOR\_PORT** | Supervisor进程管理端口 | 9001 | 选填                     |
| **REDIS\_PORT**      | Redis服务端口        | 6379 | 选填，v2.6.0 及以上版本默认 6380 |

***

#### 三、不同网络模式的配置方法

**1. Host 网络模式（推荐修改方式）**

直接在 `environment` 中添加需自定义的端口变量，无需修改 `ports` 配置。

**2. Bridge 网络模式（特殊情况修改）**

* 一般无需修改容器内端口，仅需在 `ports` 中映射主机端口即可，格式为 `“主机端口:容器内端口”`。
* 若需同时修改容器内端口，需满足两个条件：
  1. 在 `environment` 中修改对应端口变量（如 `GUNICORN_PORT`）。
  2. 在 `ports` 中同步映射新的容器内端口（如 `“8006:8006”`）。

***

#### 四、完整配置示例（含端口自定义）

```yaml
music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8006:8006"  # 主机端口:容器内端口（与NGINX_PORT保持一致）
    volumes:
      - /Users/macbookair/Music/my_music/music/music_lyc:/app/media  # 替换为你的音乐文件目录
      - ./config:/app/data  # 替换为你的配置文件存储目录
    environment:
      # 数据库相关配置（无需修改）
      - MYSQL_HOST=db
      - MYSQL_PASSWORD=your_root_password  # 需与MySQL服务密码一致
      - MYSQL_DB_NAME=music_tag
      - MYSQL_USER=root
      - MYSQL_PORT=3306
      # 性能与端口配置（可按需修改）
      - WORKER_NUM=8  # 后台任务线程数，根据服务器性能调整
      - GUNICORN_PORT=8003  # 自定义后端服务端口
      - NGINX_PORT=8006  # 自定义Nginx代理端口（与ports映射的容器内端口一致）
      - SUPERVISOR_PORT=9001  # 保持默认或按需修改
    restart: always
    depends_on:
      - db  # 依赖MySQL服务，确保先启动数据库
```
