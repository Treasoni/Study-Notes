# P2 素材 — 部署与启动

## 来源表
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| S1 | V2 项目介绍 | https://xiers-organization.gitbook.io/music-tag-web-v2/xiang-mu-jie-shao.md | 官方文档 | 2026-09-14 |
| S2 | V2 快速开始 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md | 官方文档 | 2026-09-14 |
| S3 | V2 Docker部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md | 官方文档 | 2026-09-14 |
| S4 | V2 Docker Compose 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md | 官方文档 | 2026-09-14 |
| S5 | V2 名词解释 | https://xiers-organization.gitbook.io/music-tag-web-v2/ming-ci-jie-shi.md | 官方文档 | 2026-09-14 |
| S6 | V1 项目介绍 | https://xiers-organization.gitbook.io/music-tag-web/xiang-mu-jie-shao.md | 官方文档 | 2026-09-14 |
| S7 | V1 快速开始 | https://xiers-organization.gitbook.io/music-tag-web/kuai-su-kai-shi.md | 官方文档 | 2026-09-14 |
| S8 | V1 站内 “V2 版本” 页 | https://xiers-organization.gitbook.io/music-tag-web/v2-ban-ben.md | 官方文档 | 2026-09-14 |

说明：8 个分配页面全部抓取成功，无 404，无 URL 替换。

## 主张 → 来源映射

### 端口与版本差异

- **主张**：V2 容器内监听端口为 8002，且不再需要 `command /start` 启动命令；V1 容器内端口为 8001 且需要该命令。
  - 来源：S2 | 锚点：快速开始 / “V2 版本部署” 与 “V1 版本部署” 小节
  - 原文：“容器内的端口是 8002，和不需要 command /start 命令”
  - 状态：已核实

- **主张**：V2 的 `docker run` 示例把 8002 映射到宿主机 8002，启动参数含 `--name=music-tag-web` 与 `--restart=unless-stopped`。
  - 来源：S3 | 锚点：Docker部署 / 第 2 步 “启动容器” 代码块
  - 原文：“docker run -d -p 8002:8002 ... --restart=unless-stopped xhongc/music_tag_web:latest”
  - 状态：已核实

- **主张**：V2 Compose 示例同样把 8002 映射到 8002，但重启策略写作 `restart: always`，与 `docker run` 示例不同。
  - 来源：S4 | 锚点：Docker Compose 部署 / yaml 代码块
  - 原文：“restart: always”
  - 状态：已核实

- **主张**：V2 支持 arm64、amd64、armv7 三种架构的 Docker 部署。
  - 来源：S2 | 锚点：快速开始 / “V2 版本部署” 列表项 “多架构支持”
  - 原文：“V2 版本支持 arm64、amd64 和 armv7 架构的 Docker 部署”
  - 状态：已核实

- **主张**：V1 示例端口为 8001，Portainer stacks 示例中额外使用了 `command: /start`。
  - 来源：S7 | 锚点：快速开始 / 第 2、3 步代码块
  - 原文：“docker run -d -p 8001:8001 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --restart=always”
  - 状态：已核实

### 卷挂载

- **主张**：V2 `docker run` 官方示例只挂载两个卷：宿主音乐目录到 `/app/media`，宿主配置目录到 `/app/data`。
  - 来源：S3 | 锚点：Docker部署 / 第 2 步 “启动容器” 代码块
  - 原文：“-v /path/to/your/music:/app/media -v /path/to/your/config:/app/data”
  - 状态：已核实

- **主张**：V2 Compose 官方示例挂载三个卷：`/app/media`、`/app/data`，外加 `/app/download`。
  - 来源：S4 | 锚点：Docker Compose 部署 / yaml 代码块 volumes 段
  - 原文：“- /path/to/your/download:/app/download”
  - 状态：已核实

- **主张**：`/app/download` 被描述为“新下载音乐的目录”，且要求不与媒体库重复和重合，用途是“后台刮削监控目录”。
  - 来源：S4 | 锚点：Docker Compose 部署 / yaml 代码块下方的说明列表
  - 原文：“不与媒体库重复和重合，用于后台刮削监控目录”
  - 状态：已核实

- **主张**：V2 文档把“绑定挂载”解释为宿主机路径映射到容器内路径，并声明容器内地址“一般是开发者定义的路径位置，不可修改了”。
  - 来源：S5 | 锚点：名词解释 / “Docker目录挂载” 小节
  - 原文：“容器内的地址一般是开发者定义的路径位置，不可修改了。”
  - 状态：已核实

- **主张**：V1 的 Portainer stacks 示例中 `/app/media` 带 `:rw` 后缀，而 Compose 版 V2 示例中三个卷均未写读写后缀。
  - 来源：S7 | 锚点：快速开始 / 第 3 步 portainer stacks 代码块
  - 原文：“- /path/to/your/music:/app/media:rw”
  - 状态：已核实

### 镜像与版本选择

- **主张**：官方镜像名为 `xhongc/music_tag_web:latest`，`latest` 表示最新版本号，也可指定版本，页面举例“2.1.7”。
  - 来源：S2 | 锚点：快速开始 / “docker 镜像说明” 小节
  - 原文：“latest 为最新版本号，你也可以指定版本，例如：2.1.7, ...”
  - 状态：已核实（注意：2.1.7 仅为举例，页面未声明其为当前版本）

- **主张**：页面指向 Docker Hub 的 tags 列表页用于查看可用版本标签。
  - 来源：S2 | 锚点：快速开始 / “docker 镜像说明” 小节内的 dockerhub 链接
  - 原文：“可以在 dockerhub 页面查看”
  - 状态：已核实

- **主张**：网络问题拉不动镜像时，官方给出阿里云镜像 `registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest`，做法是替换镜像名。
  - 来源：S2 | 锚点：快速开始 / “docker 镜像说明” 小节末段
  - 原文：“阿里云镜像名称：registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest”
  - 状态：已核实

- **主张**：V1 页面给出的镜像名与 V2 相同，均为 `xhongc/music_tag_web:latest`，页面未区分两个大版本的镜像仓库。
  - 来源：S7 | 锚点：快速开始 / 第 1 步 “从Docker Registry拉取镜像”
  - 原文：“docker pull xhongc/music_tag_web:latest”
  - 状态：已核实

### 访问地址与首次登录

- **主张**：V2 安装后访问地址为 `http://127.0.0.1:8002`，页面同时提到可用设备实际 IP 加端口 8002 访问。
  - 来源：S3 | 锚点：Docker部署 / 第 3 步 “访问应用”
  - 原文：“在网页浏览器中输入 http://127.0.0.1:8002”
  - 状态：已核实

- **主张**：V2 默认账号密码为 `admin/admin`，登录后进入管理界面可修改默认密码。
  - 来源：S3 | 锚点：Docker部署 / 第 4 步 “修改默认密码（可选）”
  - 原文：“登录后，默认账号密码为 admin/admin。”
  - 状态：已核实

- **主张**：反向代理进入报 csrf 错误时，页面建议改用局域网地址进入。
  - 来源：S3 | 锚点：Docker部署 / 第 4 步 “修改默认密码（可选）” 末条
  - 原文：“如果你反向代理页面进去报错 csrf 错误，请用局域网地址进入。”
  - 状态：已核实

- **主张**：V1 访问路径带 `/admin` 后缀，为 `127.0.0.1:8001/admin`，默认账号密码同样是 `admin/admin`。
  - 来源：S7 | 锚点：快速开始 / 第 4 步 “修改默认密码（可选）”
  - 原文：“访问在 127.0.0.1:8001/admin 默认账号密码 admin/admin”
  - 状态：已核实（与 V2 的差异：V2 未在部署页写明 `/admin` 后缀）

- **主张**：V2 支持登录后修改 Subsonic 默认账号密码，修改后可能需要重新登录，页面未加载则尝试刷新。
  - 来源：S3 | 锚点：Docker部署 / 第 5 步 “修改 Subsonic 密码（可选）”
  - 原文：“如果需要修改 Subsonic 的默认账号密码，也请在登录后进行操作。”
  - 状态：已核实

### 激活与授权

- **主张**：V2 需在登录后激活：点击 V1 标签，按提示输入 V2 激活码完成激活。
  - 来源：S3 | 锚点：Docker部署 / 第 6 步 “激活 V2 版本”
  - 原文：“登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。”
  - 状态：已核实

- **主张**：输入激活码报错时，官方建议检查服务器时间是否为正常北京时间；仍失败则联系作者。
  - 来源：S3 | 锚点：Docker部署 / 第 7 步 “遇到问题时”
  - 原文：“请检查和校正服务器时间，保证时间为正常的北京时间。”
  - 状态：已核实

- **主张**：激活码获取方式为赞助项目（爱发电），无法访问时可直接联系开发者微信号 `charlesnowed`。
  - 来源：S1 | 锚点：项目介绍 / “激活方式” 小节
  - 原文：“通过赞助我们的项目 爱发电 来获得激活码。”
  - 状态：已核实

- **主张**：V2 具有 V1 版本的全部功能，并可能增加新特性或改进。
  - 来源：S1 | 锚点：项目介绍 / 正文首段后
  - 原文：“V2 版本具有 V1 版本的所有功能”
  - 状态：已核实

- **主张**：V1 快速开始页未提及任何激活或授权步骤，流程止于修改默认密码。
  - 来源：S7 | 锚点：快速开始 / 全文
  - 原文：“此时你已经部署好了，你想知道具体怎么使用，请往下看吧。”
  - 状态：已核实

### 名词与背景（辅助理解部署语境）

- **主张**：官方定义“刮削”为自动识别音乐文件并在线获取专辑封面、歌曲名称、艺术家、专辑信息、流派和发行日期等数据。
  - 来源：S5 | 锚点：名词解释 / “刮削” 小节
  - 原文：“自动识别音乐文件，并在线获取相应的专辑封面、歌曲名称、艺术家、专辑信息、流派和发行日期等数据”
  - 状态：已核实

- **主张**：官方把“后台刮削”描述为在固定文件目录下自动完成搜索元数据、整理文件夹、重命名等一系列操作。
  - 来源：S5 | 锚点：名词解释 / “后台刮削” 小节
  - 原文：“固定的文件目录下，可自动从音乐流媒体平台搜索元数据、整理文件夹、重命名等一系列操作”
  - 状态：已核实（与 S4 的 `/app/download` 监控目录说明互为呼应）

- **主张**：官方开放 API 中，info 接口供 homepage 展示信息，lyrics 接口供音流 app 展示歌词，health 接口供 Docker 健康检查心跳检测。
  - 来源：S5 | 锚点：名词解释 / “开放API” 小节
  - 原文：“health接口可供docker健康检查心跳检测”
  - 状态：已核实

- **主张**：V1 官方声明支持的音频格式为 FLAC、APE、WAV、AIFF、WV、TTA、MP3、MP4、M4A、OGG、MPC、OPUS、WMA、DSF、DFF。
  - 来源：S6 | 锚点：项目介绍 / 首段
  - 原文：“支持FLAC, APE, WAV, AIFF, WV, TTA, MP3, MP4, M4A, OGG, MPC, OPUS, WMA, DSF, DFF等音频格式”
  - 状态：已核实

- **主张**：V1 项目源码地址为 GitHub `xhongc/music-tag-web`，作者署名 xier，官网为 musictagweb.com。
  - 来源：S6 | 锚点：项目介绍 / 正文链接与署名行
  - 原文：“https://github.com/xhongc/music-tag-web”
  - 状态：已核实

- **主张**：V1 站内 “V2 版本” 页仅有一句定位描述与一个功能预览图，并指向 V2 文档站，无部署细节。
  - 来源：S8 | 锚点：V2 版本 / 全文
  - 原文：“是集合音乐标签刮削和音乐播放一体的个人音乐库解决方案。”
  - 状态：已核实

## 本组矛盾与不一致

- **卷集合不一致（核心）**：同为 V2 官方页面，`docker run` 示例只挂 2 个卷，Compose 示例挂 3 个卷。
  - S3 原文：“-v /path/to/your/music:/app/media -v /path/to/your/config:/app/data”
  - S4 原文：“- /path/to/your/download:/app/download”
  - 影响：按 `docker run` 部署会缺少 `/app/download`，而后台刮削监控目录依赖该挂载点（S4 说明）。两组示例挂载集合不同，官方未说明二者等价或如何取舍。

- **重启策略写法不一致**：S3 用 `--restart=unless-stopped`，S4 用 `restart: always`；S7 的 V1 `docker run` 用 `--restart=always`。
  - S3 原文：“--restart=unless-stopped”
  - S4 原文：“restart: always”
  - 影响：同为官方示例，重启语义不同，官方未说明推荐哪种。

- **访问路径写法不一致**：V1 明确给出带 `/admin` 的登录地址，V2 部署页只给根地址。
  - S7 原文：“访问在 127.0.0.1:8001/admin”
  - S3 原文：“输入 http://127.0.0.1:8002”
  - 影响：V2 是否需要 `/admin` 后缀，分配页面中未取到明确说法。

- **文档内容疑似串页**：V2 Docker 部署页第 3 步提到“绿联设备”，而该页并非绿联专题页（llms.txt 中另有独立的绿联部署页）。
  - S3 原文：“或者绿联设备的实际 IP 地址加上端口 8002”
  - 状态：已核实为原文如此；[推断] 该句疑为从绿联部署页复制的残留表述。

- **激活入口表述含糊**：S3 说点“V1 标签”输入 V2 激活码，但 S1 只讲如何获取激活码，未说明界面入口；两页未给出界面截图或字段名。
  - S3 原文：“登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。”
  - 影响：首次登录后的激活路径描述不完整。

- **版本示例数字易被误读**：S2 用 “2.1.7” 作为“指定版本”的举例，未声明其为当前版本号或最低要求。
  - S2 原文：“你也可以指定版本，例如：2.1.7, ...”
  - 状态：已核实为原文如此；不得据此断言 2.1.7 是当前版本。

## 未取到的信息

- 官方页面**未使用“必填/可选”字样标注任何卷挂载**：哪些挂载点是必需、哪些可省略，分配页面中未取到明确结论（`未取到`）。
- `/app/download` 是否必需、缺失时后台刮削是否可用：`未取到`。
- 除 `/app/media`、`/app/data`、`/app/download` 之外是否还有其他可挂载路径（如歌词、插件、日志目录）：分配页面中 `未取到`。
- `latest` 与固定版本标签之间的官方选择建议（是否推荐固定版本）：`未取到`（S2 只陈述可指定，未给建议）。
- 当前最新版本号：`未取到`（S2 的 2.1.7 仅为示例，不是版本声明）。
- 是否存在 host 网络模式、自定义端口配置：llms.txt 中有“自定义服务端口”专页，但不在本次分配范围，`未取到`。
- 激活码激活失败、无响应 的详细排查步骤：llms.txt 中存在该专页，不在分配范围，`未取到`；S3 仅给出“校正服务器时间”一条。
- 各 NAS 平台（群晖、1panel、绿联、fnos、极空间）部署步骤：不在分配范围，`未取到`。
- 环境变量清单（V2 部署页未出现任何环境变量示例）：`未取到`。
- 镜像体积、资源要求、数据库默认类型在部署页的说明：`未取到`（llms.txt 提到默认 Sqlite，但该表述在“Mysql 部署”专页摘要中，非本次分配的 8 页正文）。
