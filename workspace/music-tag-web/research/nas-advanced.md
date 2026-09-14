# P2 素材 — NAS 平台部署与进阶配置

## 来源表

| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| S1 | 群晖部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/qun-hui-bu-shu.md | 官方文档 | 2026-09-14 |
| S2 | 1panel部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/1panel-bu-shu.md | 官方文档 | 2026-09-14 |
| S3 | 绿联部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/l-lian-bu-shu.md | 官方文档 | 2026-09-14 |
| S4 | 飞牛云fnos部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方文档 | 2026-09-14 |
| S5 | 极空间部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/ji-kong-jian-bu-shu.md | 官方文档（页面自述转载第三方） | 2026-09-14 |
| S6 | Mysql 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu.md | 官方文档 | 2026-09-14 |
| S7 | 外置Redis服务 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md | 官方文档 | 2026-09-14 |
| S8 | 自定义服务端口 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/zi-ding-yi-fu-wu-duan-kou.md | 官方文档 | 2026-09-14 |
| S9 | 容器自动更新 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md | 官方文档 | 2026-09-14 |

层级说明：9 页均取自官方 GitBook（xiers-organization.gitbook.io/music-tag-web-v2）。S5 页面正文自述教程转载自第三方网站，涉及 S5 的步骤主张按**社区实践**看待，不与官方自述步骤混列。

---

## 主张 → 来源映射

### A. 各 NAS 平台部署路径

- **主张**：群晖的入口是「注册表」搜索 `music_tag_web`，官方说明"第一个就是本项目的镜像"，镜像名为 `xhongc/music_tag_web`。
  - 来源：S1 | 锚点：群晖部署 / 正文第 1 步（注册表）
  - 原文："在注册表中搜索 music\_tag\_web, 第一个就是本项目的镜像，xhongc/music\_tag\_web"
  - 状态：已核实

- **主张**：群晖端口配置中容器内必须是 8002（第二个值），容器外第一个值可随意填写。
  - 来源：S1 | 锚点：群晖部署 / 正文第 2 步「填写配置」
  - 原文："端口配置容器内是 8002（第二个值），容器外可以随意填写你喜欢的（第一个值）"
  - 状态：已核实

- **主张**：群晖需把音乐文件映射到 `/app/media`、新建目录映射到 `/app/data`，官方两次强调"此路径不可更改"。
  - 来源：S1 | 锚点：群晖部署 / 正文第 2 步「存储空间设置」
  - 原文："将你的音乐文件映射到/app/media    此路径不可更改。" / "映射到 /app/data    此路径不可更改。"
  - 状态：已核实

- **主张**：1panel 有两个方式，方式一为「应用商店安装（推荐）」，方式二为「镜像安装」。
  - 来源：S2 | 锚点：1panel部署 / 小节标题「方式一、应用商店安装（推荐）」「方式二、镜像安装」
  - 原文："## 方式一、应用商店安装（推荐）" / "## 方式二、镜像安装"
  - 状态：已核实

- **主张**：1panel 应用商店安装的默认挂载路径为 `./data:/app/media:rw` 与 `./config:/app/data`。
  - 来源：S2 | 锚点：1panel部署 / 方式一 第 2 步「点击安装即可」
  - 原文："默认挂载路径为" / ".\/data:/app/media:rw" / ".\/config:/app/data"
  - 状态：已核实

- **主张**：1panel 自定义媒体库需编辑 compose 文件改挂载地址，示例为 `<你的媒体库地址>:/app/media:rw`。
  - 来源：S2 | 锚点：1panel部署 / 方式一 第 3 步 代码块
  - 原文："如需自定义媒体库地址，则编辑 compose 文件修改挂载的地址，例如："
  - 状态：已核实

- **主张**：1panel 镜像安装的镜像为 Docker Hub 的 `xhongc/music_tag_web:latest`，容器端口必须 8002 不能改变，协议选 TCP。
  - 来源：S2 | 锚点：1panel部署 / 方式二 第 1–2 步
  - 原文："容器端口必须是 8002（第二个值）不能改变，协议选 TCP 协议"
  - 状态：已核实

- **主张**：1panel 部署完成后需"登录后 点击V1 标签，输入 V2 激活 即可完成激活"。
  - 来源：S2 | 锚点：1panel部署 / 正文末段
  - 原文："在登录后 点击V1 标签，输入 V2 激活 即可完成激活。"
  - 状态：已核实

- **主张**：绿联走 SSH + `sudo -i`，随后用一条 docker run 命令启动，端口映射 `-p 8002:8002`。
  - 来源：S3 | 锚点：绿联部署 / 第 1–4 步 代码块
  - 原文："使用 `sudo -i` 命令获取管理员权限。" / "docker run -d -p 8002:8002 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --name=music-tag-web --restart=unless-stopped xhongc/music\_tag\_web:latest"
  - 状态：已核实

- **主张**：绿联页面要求把 `/path/to/your/music` 与 `/path/to/your/config` 替换为 NAS 上的绝对路径，后者需新建目录。
  - 来源：S3 | 锚点：绿联部署 / 第 4 步后说明段
  - 原文："请确保将 `/path/to/your/music` 替换为你NAS上的音乐文件夹的绝对路径，并且 `/path/to/your/config` 替换为一个你新创建的目录路径"
  - 状态：已核实

- **主张**：绿联部署完成后的访问地址为绿联设备 IP 加端口 8002，即 `http://greenlink_ip:8002`。
  - 来源：S3 | 锚点：绿联部署 / 第 5 步
  - 原文："输入绿联设备的IP地址后跟端口号8002"
  - 状态：已核实

- **主张**：飞牛 fnOS 页面首行标注"fnos版本：0.8.24"，这是全组唯一出现的 NAS 系统版本号。
  - 来源：S4 | 锚点：飞牛云fnos部署 / 标题下方首行
  - 原文："fnos版本：0.8.24"
  - 状态：已核实（该数字为页面原文；其指 fnOS 系统版本还是其它含义，页面未明写，[推断] 为作者测试所用 fnOS 系统版本）

- **主张**：飞牛 fnOS 第一步是进入 Docker 界面搜索 `xhongc/music_tag_web` 点击下载，再"选择对应版本：latest"，然后等待下载完成。
  - 来源：S4 | 锚点：飞牛云fnos部署 / 正文开头三步（附图）
  - 原文："进入docker界面搜索 xhongc/music\_tag\_web 点击下载" / "选择对应版本：latest" / "等待下载完成"
  - 状态：已核实

- **主张**：飞牛 fnOS 明确给出两条并列部署路径——"两种方式可以部署，二选一：第一种：容器部署 / 第二种：Compose部署"。
  - 来源：S4 | 锚点：飞牛云fnos部署 / 正文「两种方式可以部署，二选一」
  - 原文："两种方式可以部署，二选一" / "第一种：容器部署" / "第二种：Compose部署"
  - 状态：已核实

- **主张**：[重要缺口] 飞牛 fnOS 页的容器部署与 Compose 部署**只有截图、没有可读文字步骤**，各表单字段名与取值在 markdown 中取不到。
  - 来源：S4 | 锚点：飞牛云fnos部署 / 第一种「容器部署」下 4 张 figure、第二种下 4 张 figure
  - 原文：（图注为空）"<figcaption></figcaption>"
  - 状态：已核实（该页 markdown 正文除 5 行文字与图片链接外无表单描述）

- **主张**：飞牛 fnOS 页给出访问端口 8002、默认账号密码都是 admin，并要求"左上角V1标签点击激活V2版本"。
  - 来源：S4 | 锚点：飞牛云fnos部署 / 第一种「容器部署」末段
  - 原文："成功部署访问8002端口，默认账号密码 都为 admin，左上角V1标签点击激活V2版本"
  - 状态：已核实

- **主张**：极空间页面自述作者没有极空间 NAS，教程转载自第三方网站 `https://izspace.cn/music/musictag.html`。
  - 来源：S5 | 锚点：极空间部署 / 标题下方首行
  - 原文："由于我没有极空间nas 教程来自网站：https\://izspace.cn/music/musictag.html"
  - 状态：已核实（来源自述；因此下方极空间步骤宜按 社区实践 标注）

- **主张**：[社区实践] 极空间步骤为：拉取镜像 → 双击下载后的镜像 → 创建 Docker 文件夹目录 → 添加目录映射 → 添加端口。
  - 来源：S5 | 锚点：极空间部署 / 第一至第五步
  - 原文："1. 拉取music tag web镜像" / "第二步，双击下载后的镜像文件" / "第三步，创建 Docker 文件夹目录" / "第五步，添加端口也可以是【host】默认应该是 8002，我选择的是自定义端口【bridge】"
  - 状态：已核实

- **主张**：[社区实践] 极空间的目录映射为：本地音乐目录映射 `/app/media`、新建的 Docker 配置目录映射 `/app/data`，两者均需替换为自己的目录。
  - 来源：S5 | 锚点：极空间部署 / 第四步
  - 原文："本地存放音乐的目录 / 我的文件 /Music【替换成自己的目录】/app/media 刚新建的 Docker 配置目录 / 高速存储 /Docker/MuasiTag/config【替换成自己的目录】/app/data"
  - 状态：已核实

### B. Mysql 部署

- **主张**：该页说明其要解决的问题是 Sqlite 并发写入易报 `sqlite database is locked`，因此支持替换为 MySQL。
  - 来源：S6 | 锚点：Mysql 部署 / 正文首段
  - 原文："本项目默认采用Sqlite数据库，sqlite 在并发写入时容易出现sqlite database is locked，因此支持提供替换成为 msyql 数据库"
  - 状态：已核实

- **主张**：默认数据库是 Sqlite，MySQL 为可选替换；示例中各 MYSQL_* 变量均注明"没有可以不填，默认使用 sqlite"。
  - 来源：S6 | 锚点：Mysql 部署 / 「在 Music Tag Web 中配置 mysql」docker compose 命令代码块注释
  - 原文："MYSQL_HOST=192.168.1.24 # mysql 局域网ip地址（没有可以不填，默认使用 sqlite）"
  - 状态：已核实

- **主张**：方法一（推荐）是在一个 yaml 中同时部署 MySQL 与 Music Tag Web 两个容器，并需替换密码、音乐目录、配置目录三处。
  - 来源：S6 | 锚点：Mysql 部署 / 方法一「编写 docker-compose.yml 文件」与「修改配置说明」
  - 原文："在一个 yaml 文件中部署 MySQL 和 Music Tag Web 两个容器。" / "首次部署时，建议**不额外修改任何默认配置**"
  - 状态：已核实

- **主张**：MySQL 侧环境变量为 `MYSQL_ROOT_PASSWORD` 与 `MYSQL_DATABASE: music_tag`，后者注释写明"数据库名称，无需修改"。
  - 来源：S6 | 锚点：Mysql 部署 / 方法一 yaml 代码块 environment
  - 原文："MYSQL_DATABASE: music\_tag  # 数据库名称，无需修改"
  - 状态：已核实

- **主张**：Music Tag Web 侧需设置 MYSQL_HOST / MYSQL_PASSWORD / MYSQL_DB_NAME / MYSQL_USER / MYSQL_PORT，另有 WORKER_NUM 控制后台任务线程数。
  - 来源：S6 | 锚点：Mysql 部署 / 方法一 yaml 代码块 environment 与「docker compose 命令」注释
  - 原文："WORKER\_NUM=8 #  后台并发执行任务的worker数量"
  - 状态：已核实

- **主张**：MySQL 相关变量默认值为 MYSQL_USER=root、MYSQL_PORT=3306；MYSQL_USER"默认为 root，如果你没额外配置"。
  - 来源：S6 | 锚点：Mysql 部署 / 方法二末段变量说明
  - 原文："MYSQL\_USER：默认为 root， 如果你没额外配置。" / "MYSQL\_PORT： 默认端口为 3306"
  - 状态：已核实

- **主张**：配置后打不开时该页给出 5 条排查项，并称"基本能解决 90% 的问题了"。
  - 来源：S6 | 锚点：Mysql 部署 / 「配置完成后打不开 music tag web？」
  - 原文："1. MySQL 端口是否暴露出来 2. music tag web 里是否能访问到 mysql 3. 如果是原先就部署有 mysql，是否创建了 music\_tag 的数据库 4. 检查数据库的配置是否有拼写错误 5. mysql 版本太新了， 可以使用 mysql:5.7"
  - 状态：已核实

### C. 自定义服务端口

- **主张**：该页声明其解决的问题是：使用 host 网络模式出现端口冲突时，可通过环境变量自定义端口。
  - 来源：S8 | 锚点：自定义服务端口 / 首段与「一、自定义服务端口（解决端口冲突）」
  - 原文："如果你使用网络模式host，出现端口冲突，可以进行自定义端口号"
  - 状态：已核实

- **主张**：host 模式下直接在 `environment` 添加端口变量即可，**无需修改 `ports`**。
  - 来源：S8 | 锚点：自定义服务端口 / 「三、不同网络模式的配置方法」1. Host 网络模式
  - 原文："直接在 `environment` 中添加需自定义的端口变量，无需修改 `ports` 配置。"
  - 状态：已核实

- **主张**：bridge 模式一般无需改容器内端口，只映射主机端口；若确要改容器内端口，必须同时改 `environment` 与 `ports` 两处。
  - 来源：S8 | 锚点：自定义服务端口 / 「三、不同网络模式的配置方法」2. Bridge 网络模式
  - 原文："1. 在 `environment` 中修改对应端口变量（如 `GUNICORN_PORT`）。2. 在 `ports` 中同步映射新的容器内端口（如 `“8006:8006”`）。"
  - 状态：已核实

- **主张**：容器内端口变量与默认值为：GUNICORN_PORT=8001、NGINX_PORT=8002、SUPERVISOR_PORT=9001、REDIS_PORT=6379。
  - 来源：S8 | 锚点：自定义服务端口 / 「二、核心环境变量说明」表格
  - 原文："**GUNICORN\_PORT** | 后端服务端口 | 8001" / "**NGINX\_PORT** | Nginx代理后的后端服务端口 | 8002" / "**SUPERVISOR\_PORT** | Supervisor进程管理端口 | 9001"
  - 状态：已核实

- **主张**：完整示例中把主机与容器内端口统一改为 8006（`"8006:8006"` 且 NGINX_PORT=8006），同时设 GUNICORN_PORT=8003。
  - 来源：S8 | 锚点：自定义服务端口 / 「四、完整配置示例」yaml 代码块
  - 原文："- "8006:8006"  # 主机端口:容器内端口（与NGINX\_PORT保持一致）" / "- GUNICORN\_PORT=8003  # 自定义后端服务端口"
  - 状态：已核实

### D. 容器自动更新

- **主张**：自动更新由 Web 界面一键触发，官方声明其会下载最新程序、停旧容器、启新容器、清理旧镜像并保留数据与配置。
  - 来源：S9 | 锚点：容器自动更新 / 「📋 什么是自动更新？」
  - 原文："一键自动更新功能" / "✅ 保留你的所有数据和配置"
  - 状态：已核实

- **主张**：Web 界面路径为：登录 → 左侧菜单「系统设置」→「系统信息」→ 查看「系统版本」→ 出现「检查更新」按钮。
  - 来源：S9 | 锚点：容器自动更新 / 「步骤 1：检查是否有新版本」
  - 原文："点击左侧菜单的「系统设置」→「系统信息」" / "如果有新版本可用，会显示「检查更新」按钮"
  - 状态：已核实

- **主张**：使用自动更新前必须挂载 Docker Socket，官方原文为"在首次部署时必须挂载 Docker Socket"，镜像需 `-v /var/run/docker.sock:/var/run/docker.sock`。
  - 来源：S9 | 锚点：容器自动更新 / 「0. 🔧 重要：挂载 Docker Socket」及 yaml 代码块
  - 原文："**如果你想使用自动更新功能，在首次部署时必须挂载 Docker Socket。**"
  - 状态：已核实

- **主张**：未挂载 Socket 时官方列出的报错为"Docker客户端初始化失败""无法连接到 Docker daemon""更新按钮点击后没有反应"。
  - 来源：S9 | 锚点：容器自动更新 / 「⚠️ 没有挂载会怎样？」
  - 原文："❌ "Docker客户端初始化失败"" / "❌ "无法连接到 Docker daemon"" / "❌ 更新按钮点击后没有反应"
  - 状态：已核实

- **主张**：检查 Socket 是否挂载有两种方式：`docker inspect music-tag-web | grep docker.sock`，或进容器后 `ls -l /var/run/docker.sock`。
  - 来源：S9 | 锚点：容器自动更新 / 「🔍 检查是否正确挂载」方法 1 / 方法 2
  - 原文："docker inspect music-tag-web | grep docker.sock" / "ls -l /var/run/docker.sock"
  - 状态：已核实

- **主张**：启用自动更新时官方建议额外挂载 `/app/download` 作为后台刮削监控目录，并要求与媒体库不重复、不重合。
  - 来源：S9 | 锚点：容器自动更新 / Docker Compose 部署 yaml 与说明
  - 原文："\`/path/to/your/download\` 替换为你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录"
  - 状态：已核实

- **主张**：该页另给两种定时更新方案：crontab 每日 3 点跑一次 Watchtower，或常驻 Watchtower 以 `--interval 86400` 每 24 小时检查、`--cleanup` 清理旧镜像。
  - 来源：S9 | 锚点：容器自动更新 / 「❓ 可以自动定时更新吗？」方法 1 / 方法 2
  - 原文："0 3 \* \* \* docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music-tag-web" / "`--interval 86400`：每 24 小时检查一次更新"
  - 状态：已核实

- **主张**：网络受限时该页给出国内镜像源 `registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest`，并可 tag 回 `containrrr/watchtower:latest`。
  - 来源：S9 | 锚点：容器自动更新 / 「如果网络受限：」代码块
  - 原文："docker tag registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest containrrr/watchtower:latest"
  - 状态：已核实

- **主张**：官方称新版本镜像体积通常在 500MB-1GB，更新期间服务会短暂中断，建议低峰时段进行。
  - 来源：S9 | 锚点：容器自动更新 / 「3. 网络要求」与「❓ 更新需要多长时间？」
  - 原文："✅ 网络速度稳定（新版本镜像通常在 500MB-1GB）" / "更新期间服务会短暂中断，建议在低峰时段进行。"
  - 状态：已核实

### E. 外置 Redis

- **主张**：外置 Redis 不是必需的——容器本身会启动一个 redis，不需要外置可以完全不配置本页内容。
  - 来源：S7 | 锚点：外置Redis服务 / 正文首段
  - 原文："容器本身就会启动一个 redis，如果你不需要**外置**的 redis，可以不进行此项的配置。"
  - 状态：已核实

- **主张**：方法一是给已有 Redis 的服务器加 `REDIS_HOST` 环境变量，默认端口 6379，改端口需同时设 `REDIS_PORT`，有密码需设 `REDIS_PASSWORD`。
  - 来源：S7 | 锚点：外置Redis服务 / 方法一 说明段
  - 原文："你需要在环境变量中添加 `REDIS_HOST`，其默认端口为 6379。" / "如果你 redis 设置了密码，需要配置 REDIS\_PASSWORD 环境变量"
  - 状态：已核实

- **主张**：方法二是在同一个 yaml 里一起部署 `redis:latest` 与 Music Tag Web，Redis 侧用 `redis-server --requirepass yourpassword` 设密码。
  - 来源：S7 | 锚点：外置Redis服务 / 方法二 yaml 代码块
  - 原文："image: redis:latest" / "command: redis-server --requirepass yourpassword # 设置密码"
  - 状态：已核实

- **主张**：方法二里 Music Tag Web 侧通过 `REDIS_HOST=redis`（服务名）、`REDIS_PASSWORD=yourpassword`、`REDIS_PORT=6379` 连接。
  - 来源：S7 | 锚点：外置Redis服务 / 方法二 yaml 代码块 environment
  - 原文："- REDIS\_HOST=redis  # 数据库主机名，使用服务名, 不需要修改" / "- REDIS\_PORT=6379  # redis 端口，无需修改"
  - 状态：已核实

---

## 本组矛盾与不一致

1. **自动更新耗时两处数字不同（S9 页内自相矛盾）**
   - 「步骤 2：执行更新」写："等待更新完成（通常需要 1-3 分钟）"
   - 「❓ 更新需要多长时间？」写："**通常 1-5 分钟**"
   - 两处均出自 S9，未说明适用条件差异，需保留原样不合并。

2. **REDIS_PORT 默认值冲突（跨 S8 / S7，且 S8 页内自相矛盾）**
   - S8 表格：「**REDIS\_PORT** | Redis服务端口 | 6379 | 选填，v2.6.0 及以上版本默认 6380」——同一单元格内既写默认 6379 又写 v2.6.0+ 默认 6380。
   - S7 正文：「其默认端口为 6379」。
   - 结论：6379 与 6380 两个默认值并存，取决于是否 v2.6.0 及以上；本组无来源可确认当前实际默认值。

3. **MYSQL_DB_NAME 的语义描述不一致（S6 页内自相矛盾）**
   - 方法一 yaml 注释："MYSQL\_DATABASE: music\_tag  # 数据库名称，无需修改"
   - 方法二 compose 注释："MYSQL\_DB\_NAME=music\_tag # 数据表名称（没有可以不填，默认使用 sqlite）"
   - 同一变量一处叫"数据库名称"、一处叫"数据表名称"，二者不等价。

4. **Compose 服务名不一致（S9 页内自相矛盾，且与其他页不一致）**
   - S9 第一段 yaml 服务名为 `music-tag-web`；S9「2. 确保数据持久化」示例中服务名变成 `web`。
   - S6、S7、S8 的 yaml 服务名统一用 `music-tag`（container_name 均为 `music-tag-web`）。
   - 影响：`depends_on`、`docker-compose up` 的服务名引用会随页面不同而变化。

5. **V2 激活步骤在各 NAS 页覆盖不一致**
   - S2 写："在登录后 点击V1 标签，输入 V2 激活 即可完成激活。"
   - S4 写："左上角V1标签点击激活V2版本"
   - S1（群晖）、S3（绿联）**完全没有提到激活步骤**；S5（极空间）也未提到。
   - 不能据此推断这些平台无需激活，只能记录为页面缺失。

6. **默认账号密码仅一个来源**
   - 只有 S4 给出"默认账号密码 都为 admin"；其余 8 页均未提及默认凭据。
   - 无冲突来源，但覆盖度极低，不宜当作全平台通用结论。

7. **极空间页的来源层级与其他页不同**
   - S5 页面自述"由于我没有极空间nas 教程来自网站：https\://izspace.cn/music/musictag.html"，属转载的社区实践；其余 8 页为官方自述步骤。二者不可混引。

---

## 未取到的信息

- **飞牛 fnOS 页面最关键的部署细节取不到**：S4 的「容器部署」与「Compose部署」两节全部由截图承载（共 8 张 figure），markdown 正文无任何表单字段名、端口值、路径值或 yaml 文本。本次未对图片做 OCR，故 fnOS 容器部署/Compose 部署的具体配置项为 `未取到`。
- **fnOS 页"fnos版本：0.8.24"的含义未取到**：页面未说明该数字指 fnOS 系统版本、应用版本还是其它，仅照录原文。
- **通用 Compose 部署页（`kuai-su-kai-shi/docker-compose-bu-shu.md`）与 Docker 部署页（`kuai-su-kai-shi/docker-bu-shu.md`）不在本组分配范围**，本次未抓取。因此"各 NAS 方式与通用 Compose 方法的逐字段差异"只能以本组 9 页内出现的 compose 片段（S6 方法一/方法二、S7 方法二、S8 示例、S9 前置准备）为基准，无法与通用 Compose 页做权威对照。
- **群晖页没有给出任何 compose 或 docker run 片段**，仅描述 UI 表单填写（注册表 / 端口 / 存储空间），也未给出群晖 DSM 版本号。
- **1panel 页未给出 1Panel 面板版本号**，也未说明应用商店中该应用的版本。
- **绿联页未给出绿联系统（UGOS）版本号**，也未给出镜像 tag 之外的版本信息。
- **极空间页未在文字中给出实际端口号与完整映射路径**（只给出"【替换成自己的目录】"占位），也未给出极空间系统版本。
- **各 NAS 页均未给出 Music Tag Web 应用自身的版本号**；全组唯一版本号线索为 S4 的 "fnos版本：0.8.24"（含义未明）与 S8 提到的 "v2.6.0 及以上版本"。
- **S4 未说明 fnOS「容器部署」与「Compose部署」二选一时官方推荐哪一种**，页面仅写"二选一"。
- **S9 未给出当前最新版本号**，也未给出检查更新时"确认容器名称"对话框里除名称外的其它字段。
- **S8 未说明 `GUNICORN_PORT`、`NGINX_PORT`、`SUPERVISOR_PORT` 三者之间是否必须保持特定关系**，仅示例中让 NGINX_PORT 与 ports 容器内端口一致。
- **外置 Redis 未说明迁移影响**：切换外置 Redis 后原有缓存/数据是否重建为 `未取到`。
- **MySQL 迁移数据未说明**：从 Sqlite 切换到 MySQL 时既有 Sqlite 数据是否迁移、如何迁移，S6 全页 `未取到`。
