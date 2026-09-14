# P2 素材 — 飞牛 fnOS 部署（截图恢复）

## 页面文字（可直接读取的部分）
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| S9 | 飞牛云fnos部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方文档 | 2026-09-14 |

说明：本页整页只有 11 行正文文字，其余全部是 `<figure>` 图片，且**每一个 `<figcaption></figcaption>` 都是空的**（无图注、无 alt 文本）。因此页面纯文本无法还原部署步骤，必须依赖截图。这与前置 reader 的报告一致。

- 页面标题：`# 飞牛云fnos部署`
- `fnos版本：0.8.24`
- `官网地址：` `http://www.musictagweb.com/`
- `进入docker界面搜索 xhongc/music_tag_web 点击下载`（注意：`music_tag_web` 带下划线，GitBook 源码里写作转义的 `music\_tag\_web`）
- `选择对应版本：latest`
- `等待下载完成`
- `两种方式可以部署，二选一`
- `第一种：容器部署`
- `成功部署访问8002端口，默认账号密码 都为 admin，左上角V1标签点击激活V2版本`
- `第二种：Compose部署`

页面文本已直接回答：**fnOS 版本 0.8.24**、**访问端口 8002**、**默认账号密码均为 admin**、**V2 激活入口是"左上角 V1 标签"**。以下步骤细节全部来自截图。

## 截图清单
| 图片文件 | 原图 URL | 是否可读 | 内容摘要 |
| --- | --- | --- | --- |
| fnos-01.png | https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2FVH7tTRPiis1wjlaoaXt7%2FSnipaste_2024-12-04_21-37-21.png?alt=media&token=d7a4e618-c6a0-4d15-8f8b-0b019419d42a | 可读 | 镜像仓库搜索 `xhongc/music_tag_web` 的 3 条结果 |
| fnos-02.png | .../7chjAR5Q7dBVNLXr17bE%2FSnipaste_2024-12-04_21-38-02.png?alt=media&token=3630e78a-3465-4ade-8a2c-57b87ad5309c | 可读 | "选择标签"弹窗，标签值 `latest` |
| fnos-03.png | .../2VHqtswOYeHE7Xy3CL33%2FSnipaste_2024-12-04_21-38-54.png?alt=media&token=ee7145f5-26aa-47a0-8d90-95e6438e109e | 可读 | 本地镜像列表，下载进度 10% |
| fnos-04.png | .../uBqovbYUgCKbm45JjSVy%2FSnipaste_2024-12-04_22-35-37.png?alt=media&token=e6af00ab-7727-4797-b0ff-8e8a90bfdb35 | 可读 | "创建容器"第 1 步：镜像 + 容器名称 |
| fnos-05.png | .../rdmL3Wrno5jETUc5DHSU%2FSnipaste_2025-06-03_11-00-29.png?alt=media&token=a1779cc9-782c-4c48-b0ec-cd7449dad01b | 可读 | "高级设置"：端口设置 + 存储位置（**本页信息量最大的一张**） |
| fnos-06.png | .../ddkI18yiJ1G2McCU0pNc%2Fimage.png?alt=media&token=3b905405-a765-43f1-bb43-2c976229b0e2 | 可读 | "确认信息"汇总表 |
| fnos-07.png | .../zFnKe5kFHQK8IuLvmoqP%2FSnipaste_2024-12-04_22-38-56.png?alt=media&token=c8d30f0b-d9fc-4369-8e9b-5e5ea40a6291 | 可读 | 容器管理：`music_tag_web` 运行中 |
| fnos-08.png | .../GL1cc1Vhe3oKJ51GUhap%2FSnipaste_2024-12-04_22-46-18.png?alt=media&token=184c9457-73f0-4c0c-945a-85a7b907e363 | 可读 | Compose "创建项目"：上传 docker-compose.yml 分支 |
| fnos-09.png | .../Vnmn1mFUWN6kIZ1mSyop%2FSnipaste_2024-12-04_22-49-27.png?alt=media&token=5f9b83d0-7ff6-42c7-a21b-43be88827d32 | 可读 | Compose 项目管理：项目 `music_tag_web` 正在运行 |
| fnos-10.png | .../JzARETy0sFDHal5MWAyp%2FSnipaste_2024-12-04_22-49-33.png?alt=media&token=f1a99f8f-9fa7-4433-b4b6-3f991bc8cb56 | 可读 | 容器管理：`music-tag-web`（Compose 创建的容器名） |
| fnos-11.png | .../nVHCdDgjM4NDtIqKvnzD%2FSnipaste_2024-12-04_22-48-05.png?alt=media&token=f453807e-926e-4515-aa57-3a4b4fc9b297 | 可读 | Compose "创建项目"：内嵌编辑的 YAML 全文 |

11 张全部下载成功（HTTP 200，均为有效 PNG），**无 403、无签名失效、无不可读图**。URL 前半段统一为 `https://1560078921-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FuE4PkIICNz2eL9KnNA7s%2Fuploads%2F`，上表用 `.../` 省略。

## 截图恢复出的步骤与字段

### 路线一：容器部署（截图 fnos-01 → fnos-07）

- **在 Docker 应用的"镜像仓库"页搜索框中输入**：`xhongc/music_tag_web`
  - 来源：fnos-01.png | 状态：[截图读取]（与页面正文文字一致）
- **搜索结果共 3 条**（原文照录）：
  - `xhongc/music_tag_web` — 下载量 `100K+`，收藏 `35`，描述 `Music Tag 音乐标签web版`
  - `w497273/xhongc.music_tag_web` — 下载 `35`，收藏 `0`
  - `0x152a/xhongc.music_tag_web` — 下载 `8`，收藏 `0`
  - 来源：fnos-01.png | 状态：[截图读取]
  - 说明：**官方源是第一条 `xhongc/music_tag_web`**（有描述行、下载量最高）。后两条是同名个人镜像，页面没有文字提示该选哪条，只能从截图排序判断。
- **选择标签弹窗**：标题 `选择标签`，字段名 `镜像标签`，填入值 `latest`；按钮 `取消` / `确定`
  - 来源：fnos-02.png | 状态：[截图读取]
- **下载完成后的本地镜像**：名称 `xhongc/music_tag_web`，`标签: latest`，`大小: 45.02 MB`，`创建时间: --`
  - 来源：fnos-03.png | 状态：[截图读取]
- **创建容器 - 第 1 步**（弹窗标题 `创建容器`）：
  - `选择镜像*` = `xhongc/music_tag_web:latest`
  - `容器名称*` = `music_tag_web`（**下划线**）
  - `资源限制` 复选框 = 未勾选（展开项为 `CPU权重 自动`、`内存限制 自动`）
  - `开机自动开启` 复选框 = 未勾选
  - 按钮：`取消` / `下一步`
  - 来源：fnos-04.png | 状态：[截图读取]

- **创建容器 - 第 2 步「高级设置」**（关键字段，已放大复核）：
  - 分区 `端口设置`，说明文字：`请在本地端口字段中输入可用的端口，以将端口与容器端口映射。此处列出的端口是容器的对外端口。`
    - 端口行：本地端口 `8002` → 容器端口 `8002`，协议 `TCP`；下方按钮 `+ 添加端口`
    - **容器端口 = 8002**，且本地端口也用 8002（未做端口偏移）
  - 分区 `存储位置`，说明文字：`将容器的存储空间映射到NAS上的文件夹`
    - 行 1：本地 `/vol1/1000/music` → 装载 `/app/media`，权限 `读写`
    - 行 2：本地 `/vol1/1000/mtw_config` → 装载 `/app/data`，权限 `读写`
    - 下方按钮 `+ 添加路径`
  - 底部按钮：`上一步` / `取消` / `下一步`
  - 来源：fnos-05.png | 状态：[截图读取]

- **创建容器 - 第 3 步「确认信息」**：
  - 分区 `基本信息`：`容器名称`=`music_tag_web`，`镜像名称`=`xhongc/music_tag_...`（单元格截断），`CPU限制`=`自动`，`内存限制`=`自动`，`开机自启`=`否`
  - 分区 `端口`：`本地端口`=`8002`，`容器端口`=`8002`，`协议`=`TCP`
  - 分区 `存储`：**只有 1 行** —— `本地路径`=`/vol1/1000/music`，`装载路径`=`/app/media`，`权限`=`读写`
  - 复选框 `创建后启动容器` = 已勾选
  - 按钮：`上一步` / `取消` / `创建`
  - 来源：fnos-06.png | 状态：[截图读取]

- **部署结果**：容器管理列表中 `music_tag_web`，`CPU: 0.31%`，`内存: 407.01 MB`，`↑0.00KB/s ↓0.00KB/s`，状态为运行中（绿点）；页脚 `共 1 项`
  - 来源：fnos-07.png | 状态：[截图读取]

### 路线二：Compose 部署（截图 fnos-08 → fnos-11）

- **入口**：左侧导航 `Compose` → 页面 `项目管理`，按钮 `+ 新增项目`
  - 来源：fnos-08.png、fnos-09.png | 状态：[截图读取]
- **「创建项目」弹窗字段全貌**：
  - `项目名称`（输入框，占位符 `请输入`）
  - `路径`（选择框，占位符 `请选择`）
  - `来源`（单选）：`上传docker-compose.yml` / `创建docker-compose.yml`
  - 复选框 `创建项目后立即启动`
  - 按钮：`取消` / `完成`
  - 来源：fnos-08.png（`上传docker-compose.yml` 被选中、下拉为 `请选择`、`完成` 置灰）与 fnos-11.png（`创建docker-compose.yml` 被选中、路径已填 `vol1/1000/mtw_config`、`创建项目后立即启动` 已勾选、`完成` 可点）| 状态：[截图读取]
- **路径字段实测填值**：`vol1/1000/mtw_config`（注意：此处截图里**没有**前导斜杠）
  - 来源：fnos-11.png | 状态：[截图读取]
- **内嵌 compose YAML 全文**（逐行照录，已放大复核）：
  ```yaml
  version: '3'

  services:
    music-tag:
      image: xhongc/music_tag_web:latest
      container_name: music-tag-web
      ports:
        - "8002:8002"
      volumes:
        - /vol1/1000/music:/app/media:rw
        - /vol1/1000/mtw_config:/app/data
      restart: unless-stopped
  ```
  - 来源：fnos-11.png | 状态：[截图读取]
  - 注意：此 YAML **不在页面 markdown 里**，只存在于截图中。
- **Compose 项目运行结果**：项目列表 `music_tag_web`，`正在运行`，`创建时间: 2024-12-04 10:48:17`，`容器: 1`，`路径: 存储空间1/我的文件/mtw_config/docker-compos...`（截断）；页脚 `共 1 项`
  - 来源：fnos-09.png | 状态：[截图读取]
- **Compose 创建出的容器名**：容器管理列表中为 `music-tag-web`（**连字符**），`项目: music_tag_...`（截断），`CPU: 0.53%`，`内存: 279.46 MB`
  - 来源：fnos-10.png | 状态：[截图读取]

### 对六条待确认报告的回答

1. **要在 Docker 界面搜索的镜像** = `xhongc/music_tag_web`（下划线）。页面文字与 fnos-01.png 一致；**不是**应用商店（fnOS「应用商店」在本页完全没有出现，全程走的是 Docker 应用）。— 已确认
2. **容器端口** = `8002`。在 fnos-05.png（端口设置）与 fnos-06.png（确认信息）各出现一次，本地端口同为 8002。— 已确认，与页面文字 `访问8002端口` 互相印证
3. **卷映射** = `/vol1/1000/music → /app/media`（读写）与 `/vol1/1000/mtw_config → /app/data`（读写）。两条路线都一致，Compose YAML 亦同。— 已确认
4. **环境变量 / 网络模式** = **未取到**。fnos-01 至 fnos-11 全部截图中没有出现任何环境变量输入区，也没有网络模式（bridge/host/macvlan）选择项；「高级设置」页只截了端口设置与存储位置两个分区。— 未取到
5. **V2 激活步骤是否在本页** = 仅以**页面正文文字**出现一句 `左上角V1标签点击激活V2版本`；**没有任何截图展示该 V1 标签或激活对话框**。无法从截图确认激活入口的准确位置与外观。— 文字有，截图未取到
6. **fnOS 版本** = `0.8.24`（页面正文文字 `fnos版本：0.8.24`）。截图内不含版本号。— 已确认（文字来源）

## 页面确实没有提供的信息

- **无任何图注**：11 个 `<figure>` 的 `<figcaption>` 全部为空，页面正文对每张图零解释，步骤必须靠肉眼读图。
- **无环境变量**：全页及全部截图均未出现 PUID / PGID / TZ / 时区 / 语言等任何环境变量字段。
- **无网络模式字段**：截图中未见 bridge/host 等网络模式选择。
- **无「应用商店」途径**：页面只讲 Docker 应用里的镜像仓库与 Compose，没有 fnOS 应用商店安装路径。
- **无 V2 激活的截图或文字说明**：只有一句"点击左上角V1标签激活V2版本"，没有图，也没有说明激活是否联网、是否需要邀请码或账号。
- **无 compose 文件的获取方式**：页面没有提供 `docker-compose.yml` 的下载链接或文件名，YAML 只在截图里；`上传docker-compose.yml` 分支所需的文件来源页面未给。
- **未说明 `/app/media` 与 `/app/data` 的含义**：页面没有解释这两个容器路径分别存什么（音乐库 vs 配置），也未说明能否改成别的宿主机路径。
- **未说明宿主机端口能否不等于 8002**：截图里本地端口与容器端口都填 8002，但没有任何文字说明二者必须相同。
- **未说明 fnOS 版本要求**：只写了本文写作时的 `0.8.24`，没有说最低版本要求。
- **未给出默认账号密码的修改方式**，也未说明首次登录后的后续步骤。

## 本组发现的内部不一致（供 P4/P5 注意）

- **容器部署路线的卷数量自相矛盾**：`高级设置`（fnos-05.png）配置了 **2 条**映射（music→media、mtw_config→data），但紧接着的 `确认信息`（fnos-06.png）汇总表里**只剩 1 条**（music→media）。这是截图本身的差异，不是读取误差；对比之下 Compose 路线（fnos-11.png）明确带 2 条卷。**若照容器路线走，务必确认 `/app/data` 是否真的挂上了**，因为 V2 的配置/数据库落在 `/app/data`。
- **两条路线产生不同容器名**：容器部署为 `music_tag_web`（下划线），Compose 部署为 `music-tag-web`（连字符）。后续写笔记时不要混用。
- **`路径` 字段的前导斜杠不一致**：fnos-11.png 中 Compose 的「路径」填的是 `vol1/1000/mtw_config`（无前导 `/`），而同页 YAML 卷里写的是 `/vol1/1000/mtw_config`（有前导 `/`）。
