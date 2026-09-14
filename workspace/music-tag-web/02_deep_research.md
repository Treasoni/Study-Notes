# 02 深度素材 — 如何使用 Music Tag Web

- **主题**: 如何使用 Music Tag Web（自托管音乐标签编辑器）
- **项目**: `xhongc/music-tag-web` · 默认分支 `dev_1.0`
- **阶段**: P2 深度收集
- **检索日期**: 2026-09-14
- **执行模式**: 大纲模式（outline）
- **已确认方向**: **D 折中主线** — 正文走「部署 → 首次登录 → 标签编辑与刮削 → 整理与批处理」主线；V2 播放侧、进阶配置、排错 FAQ 收进附录章节

> [!warning] 下游必读：本文档的使用规则
> 1. **来源 ID 已按组命名空间化**：`D`=部署与启动，`N`=NAS 与进阶配置，`T`=标签操作主线，`F`=FAQ 与排错，`P`=播放侧生态，`O`=飞牛 fnOS 截图读取。跨组引用请带组前缀，不要只写「S2」。
> 2. **凡标 `未取到` 的，禁止在写作时补齐。** 本项目已有先例：转述来源论断会变成伪引证。写作时只能使用标「已核实」的主张；标 `[推断]` 的必须显式写成推断。
> 3. **第四节「矛盾总表」里的每一条，正文都必须择一处理**：要么明确采用某一口径并说明，要么如实写明"官方两处说法不一致"。**不得静默取一个。**

---

## 一、Scope（本次收集的边界）

| 项 | 内容 |
| --- | --- |
| 覆盖 | 官方 GitBook 两套手册（V1 约 10 页 / V2 约 40 页）的部署、配置、操作、排错、播放侧页面；仓库 README；GitHub Issues 聚类；2 篇社区实践 |
| 主信源 | `xiers-organization.gitbook.io/music-tag-web-v2` 与 `.../music-tag-web`（GitBook 支持 `.md` 后缀直取正文） |
| 未覆盖 | Docker Hub tag 列表（本机不可达）、部分 issue 评论区（GitHub API 速率限制）、官方 changelog（**站点内不存在该页**） |
| 已知层级问题 | 极空间部署页自述转载自第三方；README 有明显 SEO 改写痕迹，仅作交叉验证 |

---

## 二、来源总表

### 部署与启动（D）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| D1 | V2 项目介绍 | …/music-tag-web-v2/xiang-mu-jie-shao.md | 官方 |
| D2 | V2 快速开始 | …/music-tag-web-v2/kuai-su-kai-shi.md | 官方 |
| D3 | V2 Docker 部署 | …/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md | 官方 |
| D4 | V2 Docker Compose 部署 | …/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md | 官方 |
| D5 | V2 名词解释 | …/music-tag-web-v2/ming-ci-jie-shi.md | 官方 |
| D6 | V1 项目介绍 | …/music-tag-web/xiang-mu-jie-shao.md | 官方 |
| D7 | V1 快速开始 | …/music-tag-web/kuai-su-kai-shi.md | 官方 |
| D8 | V1 站内「V2 版本」页 | …/music-tag-web/v2-ban-ben.md | 官方 |

### NAS 平台部署与进阶配置（N）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| N1 | 群晖部署 | …/kuai-su-kai-shi/qun-hui-bu-shu.md | 官方 |
| N2 | 1Panel 部署 | …/kuai-su-kai-shi/1panel-bu-shu.md | 官方 |
| N3 | 绿联部署 | …/kuai-su-kai-shi/l-lian-bu-shu.md | 官方 |
| N4 | 飞牛云 fnOS 部署 | …/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方（正文仅截图） |
| N5 | 极空间部署 | …/kuai-su-kai-shi/ji-kong-jian-bu-shu.md | **转载第三方** |
| N6 | Mysql 部署 | …/jin-jie-pei-zhi/mysql-bu-shu.md | 官方 |
| N7 | 外置 Redis 服务 | …/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md | 官方 |
| N8 | 自定义服务端口 | …/jin-jie-pei-zhi/zi-ding-yi-fu-wu-duan-kou.md | 官方 |
| N9 | 容器自动更新 | …/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md | 官方 |

### 标签操作主线（T）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| T1 | V1 手动修改标签 | …/music-tag-web/shou-dong-xiu-gai-biao-qian.md | 官方 |
| T2 | V1 批量修改 | …/music-tag-web/pi-liang-xiu-gai.md | 官方 |
| T3 | V1 自动批量修改 | …/music-tag-web/zi-dong-pi-liang-xiu-gai.md | 官方 |
| T4 | V1 整理文件夹 | …/music-tag-web/zheng-li-wen-jian-jia.md | 官方 |
| T5 | V1 简繁体转换 | …/music-tag-web/jian-fan-ti-zhuan-huan.md | 官方（正文仅截图） |
| T6 | V1 拆分文件名称 | …/music-tag-web/chai-fen-wen-jian-ming-cheng.md | 官方 |
| T7 | V1 切割音轨 | …/music-tag-web/qie-ge-yin-gui.md | 官方 |
| T8 | V2 手动刮削 | …/gong-neng-miao-shu/shou-dong-gua-xiao.md | 官方（**正文为空**） |
| T9 | V2 自动刮削 | …/gong-neng-miao-shu/zi-dong-gua-xiao.md | 官方（**正文为空**） |
| T10 | V2 后台刮削 | …/gong-neng-miao-shu/hou-tai-gua-xiao.md | 官方 |
| T11 | V2 基本设置 | …/gong-neng-miao-shu/ji-ben-she-zhi.md | 官方 |
| T12 | V2 变量的使用说明 | …/gong-neng-miao-shu/bian-liang-de-shi-yong-shuo-ming.md | 官方 |
| T13 | V2 名词解释 | …/music-tag-web-v2/ming-ci-jie-shi.md | 官方 |
| T14 | 教程：手动刮削能实现哪些功能 | …/jiao-cheng-wen-zhang/shou-dong-gua-xiao-neng-shi-xian-na-xie-gong-neng.md | 官方 |
| T15 | 教程：后台刮削怎么玩 | …/jiao-cheng-wen-zhang/hou-tai-gua-xiao-zen-me-wan.md | 官方 |
| T16 | 教程：批量重命名文件名称 | …/jiao-cheng-wen-zhang/pi-liang-zhong-ming-ming-wen-jian-ming-cheng.md | 官方 |
| T17 | V1 手册 llms.txt（页面树/顺序） | …/music-tag-web/llms.txt | 官方 |
| T18 | V2 手册 llms.txt（页面树/顺序） | …/music-tag-web-v2/llms.txt | 官方 |
| T19 | V2 项目介绍 | …/music-tag-web-v2/xiang-mu-jie-shao.md | 官方 |
| T20 | V2 常见问题 | …/music-tag-web-v2/chang-jian-wen-ti.md | 官方 |

### FAQ、激活、升级与排错（F）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| F1 | 常见问题 FAQ（14 组问答） | …/music-tag-web-v2/chang-jian-wen-ti.md | 官方 |
| F2 | 激活码激活失败、无响应 | …/jiao-cheng-wen-zhang/ji-huo-ma-ji-huo-shi-bai-wu-xiang-ying.md | 官方 |
| F3 | 忘记登录密码怎么办 | …/jiao-cheng-wen-zhang/wang-ji-deng-lu-mi-ma-zen-me-ban.md | 官方 |
| F4 | 怎么更新/升级版本 | …/jiao-cheng-wen-zhang/zen-me-geng-xin-sheng-ji-ban-ben-ne.md | 官方 |
| F5 | 批量重命名文件名称 | …/jiao-cheng-wen-zhang/pi-liang-zhong-ming-ming-wen-jian-ming-cheng.md | 官方 |
| F6 | 多目录独立挂载的方式 | …/jiao-cheng-wen-zhang/duo-mu-lu-du-li-gua-zai-de-fang-shi.md | 官方 |
| F7 | 手动刮削能实现哪些功能 | …/jiao-cheng-wen-zhang/shou-dong-gua-xiao-neng-shi-xian-na-xie-gong-neng.md | 官方 |
| F8 | 容器自动更新 | …/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md | 官方 |
| F9 | Mysql 部署 | …/jin-jie-pei-zhi/mysql-bu-shu.md | 官方 |
| F10 | 外置 Redis 服务 | …/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md | 官方 |
| F11 | 快速开始（V1/V2 端口与启动差异） | …/music-tag-web-v2/kuai-su-kai-shi.md | 官方 |
| F12 | Issues 列表（按评论数倒序，共 643 条） | `api.github.com/search/issues?q=repo:xhongc/music-tag-web+is:issue` | 项目仓库 |
| F13 | Issues 关键词检索（激活/登录/封面/redis） | 同上 | 项目仓库 |
| F14 | 各 issue 评论区（作者与用户回复） | `github.com/xhongc/music-tag-web/issues/{编号}` | 项目仓库 + 社区 |

### 播放侧与生态（P）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| P1 | 音乐收藏与播放 | …/gong-neng-miao-shu/yin-yue-shou-cang-yu-bo-fang.md | 官方 |
| P2 | 小爱音箱 | …/gong-neng-miao-shu/xiao-ai-yin-xiang.md | 官方 |
| P3 | 网盘音乐 | …/gong-neng-miao-shu/wang-pan-yin-yue.md | 官方 |
| P4 | 智能歌单 | …/gong-neng-miao-shu/zhi-neng-ge-dan.md | 官方 |
| P5 | 音乐去重 | …/gong-neng-miao-shu/yin-yue-qu-zhong.md | 官方 |
| P6 | Subsonic 客户端 | …/music-tag-web-v2/subsonic-ke-hu-duan.md | 官方 |
| P7 | 刮削艺术家并被 Navidrome 识别 | …/jiao-cheng-wen-zhang/gua-xiao-yi-shu-jia-bing-bei-navidrome-shi-bie.md | 官方 |
| P8 | 飞牛论坛帖 4152 | `club.fnnas.com/forum.php?mod=viewthread&tid=4152` | 社区实践 |
| P9 | 博客园：Navidrome + MusicTagWeb | `cnblogs.com/ivoink/articles/22696323` | 社区实践 |
| P10 | V2 llms.txt | …/music-tag-web-v2/llms.txt | 官方 |
| P11 | V1 llms.txt | …/music-tag-web/llms.txt | 官方 |

### 飞牛 fnOS 截图读取（O）

| ID | 标题 | URL | 层级 |
| --- | --- | --- | --- |
| O1 | 飞牛云 fnOS 部署（11 张截图逐张读图） | …/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方（内容仅存在于截图） |

---

## 三、核心主张 → 来源映射

### 3.1 部署与启动（供 Ch2 使用）

- **主张**：V2 与 V1 的部署差异只有两点——容器端口 8002（V1 为 8001），且不再需要 `command: /start`
  - 来源：D2 | 锚点：V2 快速开始·V1/V2 版本部署对比
  - 原文："与V1 版本的区别，容器内的端口是 8002，和不需要 command /start 命令"
  - 状态：已核实（父进程亲自 curl 回源确认）

- **主张**：官方 Compose 配置挂三个卷——`/app/media`（音乐库）、`/app/data`（配置与数据库）、`/app/download`（后台刮削监控目录，要求不与媒体库重合）
  - 来源：D4 | 锚点：Docker Compose 部署·yaml 代码块
  - 原文："/path/to/your/download 替换为你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录"
  - 状态：已核实

- **主张**：`docker run` 一步到位的官方示例**只挂两个卷**，不含 `/app/download`
  - 来源：D3 | 锚点：Docker 部署·第 2 步命令
  - 状态：已核实 → 与 D4 构成矛盾，见 §4.1

- **主张**：镜像为 `xhongc/music_tag_web:latest`；国内拉不动时可换阿里云镜像 `registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest`
  - 来源：D2 | 锚点：快速开始·docker 镜像说明
  - 原文："如果因为网络问题，无法拉取镜像，可以使用阿里云的 music tag web 镜像"
  - 状态：已核实

- **主张**：默认访问 `http://127.0.0.1:8002`，默认账号密码 `admin/admin`，登录后应立即改密
  - 来源：D3 | 锚点：Docker 部署·第 3、4 步
  - 状态：已核实

- **主张**：反向代理进后台报 csrf 错误时，改用局域网地址访问
  - 来源：D3 | 锚点：Docker 部署·第 4 步附注
  - 原文："如果你反向代理页面进去报错 csrf 错误，请用局域网地址进入。"
  - 状态：已核实

- **主张**：V2 首次登录后需要**激活**：点界面左上角 V1 标签输入 V2 激活码；激活码经爱发电或作者微信获取；激活失败先校正服务器时间为北京时间
  - 来源：D3 + F1 + F2 | 锚点：Docker 部署·第 6、7 步；FAQ Q3；激活码页情况 1
  - 状态：已核实（价格未取到，见 §5）

- **主张**：V2 激活有**重新激活次数上限 6 次**；在同一账号下于第二台设备激活会使前一台失效；激活信息落在 `/app/data`，该目录必须持久化，否则重装即掉激活
  - 来源：F1 | 锚点：FAQ Q10
  - 状态：已核实

- **主张**：升级示例中的镜像名写作 `xhong/music_tag_web`，与快速开始的 `xhongc/music_tag_web` 不一致（**疑似官方笔误，照抄会拉不到镜像**）
  - 来源：F4 vs F11 | 锚点：升级页·示例命令；快速开始·镜像说明
  - 状态：已核实为原文如此

### 3.2 钉住「写标签会改原文件」这一关键机制（供 Ch5 使用）

- **主张**：项目区分两种写入目标——写元数据（改文件本体）与写数据库（只能在自带 Subsonic 服务端里看到）；写元数据会影响 BT 做种
  - 来源：T11 | 锚点：基本设置
  - 原文："写入元数据会影响做种，写入数据库必须有 mtw 提供的 subsonic 服务端播放才能显示"
  - 状态：已核实
- **主张**：V1 全套操作页**没有任何一处**建议备份或警告不可逆
  - 来源：T1–T7（全组扫描） | 锚点：11 个分配页面全文
  - 状态：已核实为「确实没有」——因此**笔记不得声称"官方建议备份"**

### 3.3 标签操作主线的官方顺序（供 Ch5/Ch6 章序）

- **主张**：V1 手册的页面顺序本身就是一条操作主线，已由页面树核实而非推测
  - 来源：T17 | 锚点：V1 llms.txt 条目顺序
  - 顺序：手动修改标签 → 批量修改 → 自动批量修改 → 整理文件夹 → 简繁体转换 → 拆分文件名称 → 切割音轨
  - 状态：已核实

- **主张**：V1「批量修改」是**手动填写**共有元数据；「自动批量修改」才是从选定标签源自动匹配并保存
  - 来源：T2 / T3 | 锚点：批量修改页首句
  - 原文："勾选多个文件或文件夹进行批量修改文件中相同的元数据（注意是手动填写）"
  - 状态：已核实

- **主张**：V1「拆分文件名称」用于元数据为空、只有文件名含信息的文件，把文件名里的信息嵌入元数据
  - 来源：T6 | 锚点：拆分文件名称页导语
  - 状态：已核实

- **主张**：切割音轨依赖 CUE + 整轨文件，且 ffmpeg 需**自己放到 `/app/data/bin/ffmpeg` 并 `chmod +x`**；不支持 APE
  - 来源：T7 | 锚点：切割音轨页
  - 状态：已核实（界面侧完整步骤未取到）

- **主张**：V2 的「手动刮削」「自动刮削」两个功能页**正文为空**（只有一级标题），功能语义只能从名词解释与教程文章侧证
  - 来源：T8 / T9 vs T13 / T14 | 锚点：页面正文；名词解释
  - 状态：已核实为「页面确实无内容」，非抓取失败

- **主张**：V2 后台刮削 = 监控指定目录，对新放入的音乐自动刮削并整理归档；FAQ 明确整理步骤"必须要选择"，否则每次监控的不是增量数据、会越积越多
  - 来源：T10 + T20 | 锚点：后台刮削页；FAQ 对应问答
  - 状态：已核实

### 3.4 NAS 平台差异（供 Ch3 使用；用户设备为飞牛 fnOS）

- **主张**：飞牛 fnOS 的部署流程只存在于截图中（11 张图、图注全空），已逐张读图恢复如下
  - 来源：O1 | 锚点：fnos-01…fnos-11 截图
  - 关键值：在 **Docker 应用**（非应用商店）搜索 `xhongc/music_tag_web`（下划线）；容器端口与本机端口均为 **8002/TCP**；卷映射 `/vol1/1000/music → /app/media`、`/vol1/1000/mtw_config → /app/data`
  - 状态：[截图读取] 已核实

> [!warning] fnOS 截图本身有缺陷，写作时必须提醒
> 「高级设置」截图显示 **2 条**卷映射，但紧接着的「确认信息」汇总截图只剩 **1 条**（丢了 `/app/data`）。V2 的配置与数据库正落在 `/app/data`——照容器路线走必须自查这个卷是否真的挂上。另外容器路线与 Compose 路线生成的容器名不同（`music_tag_web` vs `music-tag-web`）。来源：O1

- **主张**：群晖部署页只用 UI 表单描述（注册表 / 端口 / 存储空间），**未给出任何 compose 或 docker run 片段**
  - 来源：N1 | 锚点：群晖部署页
  - 状态：已核实
- **主张**：极空间部署页自述转载自第三方站点，属**转载内容**而非官方自述步骤
  - 来源：N5 | 锚点：极空间部署页首句
  - 原文："由于我没有极空间nas 教程来自网站：https://izspace.cn/music/musictag.html"
  - 状态：已核实

### 3.5 进阶配置（供附录 Ap2 使用）

- **主张**：默认数据库是 Sqlite；切 MySQL 是为了解决并发写入时的 `sqlite database is locked`
  - 来源：N6 | 锚点：Mysql 部署页导语
  - 状态：已核实（Sqlite→MySQL 的数据迁移方式**未取到**）
- **主张**：外置 Redis **不是必需的**，容器自带一个 redis
  - 来源：N7 | 锚点：外置 Redis 服务页
  - 状态：已核实
- **主张**：host 网络模式下若端口冲突，可用环境变量自定义端口，官方给出的键为 `GUNICORN_PORT`(8001) / `NGINX_PORT`(8002) / `SUPERVISOR_PORT`(9001) / `REDIS_PORT`
  - 来源：N8 | 锚点：自定义服务端口页·表格
  - 状态：已核实（`REDIS_PORT` 默认值自相矛盾，见 §4.4）
- **主张**：容器内自动更新需要把 `/var/run/docker.sock` 挂进容器，更新入口在「系统设置 → 系统信息 → 检查更新」
  - 来源：N9 | 锚点：容器自动更新页
  - 状态：已核实
- **主张**：遗忘管理员密码只能在容器内执行 `python manage.py changepassword admin` 重置
  - 来源：F3 | 锚点：忘记登录密码页
  - 状态：已核实

### 3.6 播放侧与生态（供附录 Ap1 使用）

- **主张**：V2 自带一个 Open Subsonic 协议服务端，登录 host 为 `站点 ip:8002`，凭据在后台管理的 subsonic 用户中查看与修改
  - 来源：P1 / P6 | 锚点：音乐收藏与播放页
  - 原文："登录的 host 是站点 ip:8002, 账号密码在后台管理里subsonic 用户中查看并修改。"
  - 状态：已核实（默认凭据具体值未取到）
- **主张**：批量刮削艺术家封面会在 `/艺术家名/` 目录下生成 `artist.jpg`，该文件将被 Navidrome 自动识别用于艺术家页展示
  - 来源：P7 | 锚点：刮削艺术家并被 navidrome 识别页
  - 状态：已核实
- **主张**：网盘音乐通过 alist 挂载接入（容器内路径 `/app/webdav`）
  - 来源：P3 | 锚点：网盘音乐页
  - 状态：已核实（该页正文把路径误写成 `/app/weddav`，同页映射示例为正确拼写）
- **主张**：小爱音箱接入需**小米 ID（非手机号）**及设备型号、内网地址与端口；官方提示不支持的型号可能无法使用
  - 来源：P2 | 锚点：小爱音箱页
  - 状态：已核实
- **主张**（社区实践，非官方）：Navidrome 读取专辑封面用 `cover.jpg`，需在 Music Tag Web 中把「导出图片」设为开；社区给出封面 80K / 800x550 的经验值
  - 来源：P8 | 锚点：飞牛论坛帖 4152 楼层
  - 状态：社区实践，**引用时须标注层级**

---

## 四、矛盾与不一致总表（写作时必须逐条处理）

### 4.1 挂载卷集合不一致（**影响最大**）
`docker run` 示例（D3）只挂 2 卷，Compose 示例（D4）挂 3 卷，官方未说明二者等价或如何取舍。
→ **建议写法**：以 Compose 三卷为推荐配置，显式说明第三个卷 `/app/download` 是后台刮削的监控目录，并把它作为「想用后台刮削就必须挂」的条件写清；同时给出「不用后台刮削可省」的提示，并标注这是本笔记的推断。

### 4.2 重启策略三种写法
D3 `--restart=unless-stopped` / D4 `restart: always` / D7（V1）`--restart=always`。
→ 建议统一采用 `unless-stopped` 并说明差异。

### 4.3 访问路径写法不一致
V1（D7）明确给 `127.0.0.1:8001/admin`；V2（D3）只给 `http://127.0.0.1:8002`，**未说明是否仍需 `/admin` 后缀**。
→ 建议写成"访问 `http://<ip>:8002`，后台入口为 `/admin`"，并标注 V2 手册未明确这一点。

### 4.4 `REDIS_PORT` 默认值冲突
N8 同一单元格内既写默认 6379、又写 "v2.6.0 及以上版本默认 6380"；N7 正文写"其默认端口为 6379"。
→ 建议并列两值并说明取决于版本。

### 4.5 官方 host 网络建议 vs 用户实测相反
F1/F2 建议改 host 模式解决激活与网络问题；但 F14 `#360` 中用户报告"换成 bridge 网络没问题"，作者仅回"可能有端口冲突"，未撤回建议。
→ 建议写成"官方推荐 host，但社区有个案报告 host 失败、bridge 可用，可两向尝试"。

### 4.6 同一 issue 内作者给出三套登录失败口径
F14 `#360`：作者先给四条排查清单（进程重启 / redis / 内存 / 端口冲突），再改为"把 `/app/data` 中的 db 删掉再重启"，最后建议换浏览器，问题**未闭环**。
→ 排错章节如实呈现为"无确定结论"，不要把任一口径写成官方定论。

### 4.7 升级"保留数据"声明 vs 实测封面丢失
F8 官方称自动更新"保留你的所有数据和配置"；F14 `#546` 用户删旧镜像拉新镜像后封面全部 404，作者未定位根因，处置是"重新导入收藏"。
→ 建议并列两方，提示升级前自行备份 `/app/data`。

### 4.8 镜像仓库名不一致
F4 升级示例写 `xhong/music_tag_web`，D2/F11 写 `xhongc/music_tag_web`。
→ 建议以 `xhongc/music_tag_web` 为准，并提示照抄升级页示例会拉不到镜像。

### 4.9 "V2 包含 V1 所有功能" vs V2 无对应页面
T18/T19 声称 V2 具有 V1 全部功能；但 V2 页面树中查不到「切割音轨」「拆分文件名称」「简繁体转换」的独立页。
→ 建议只写"官方称 V2 包含 V1 全部功能，但 V2 手册未为这三项提供独立页面，实际入口需在界面中确认"。

### 4.10 其他需保留原样的文档缺陷（不要"顺手修正"后当成事实）
- T4 整理文件夹措辞有笔误"会更加音乐的元数据"（应为"会根据"），且**分组键字段名未取到**。
- N6 同一页把容器内路径写成 `/app/media/Pop` 与 `/music/Pop` 两版。
- N6 同一变量被注释为"数据库名称"与"数据表名称"两种语义。
- P3 正文 `/app/weddav` 与映射示例 `/app/webdav` 拼写冲突。
- 极空间页（N5）属转载，不可与官方自述步骤混引。

---

## 五、未取到的信息（**禁止在写作中补齐**）

| 类别 | 缺口 |
| --- | --- |
| 版本 | 当前最新版本号；官方**不存在** changelog/release notes 页面；D2 出现的 "2.1.7" 只是举例，不是版本声明 |
| 镜像 | Docker Hub tag 完整列表与最后推送时间（本机 `hub.docker.com` 超时不可达） |
| 商业 | 激活码价格 / 爱发电档位（三处官方页面均无金额）；重置 6 次上限的成本与耗时；激活绑定的粒度（硬件 / IP / 仅最后一次记录） |
| 刮削 | 标签源 provider 的具体名单——两版手册全文检索网易/QQ音乐/酷狗/酷我/咪咕/MusicBrainz/AcoustID/Spotify/Deezer/iTunes/Last.fm **命中数为 0**，只有"标签源""音乐流媒体平台"泛称 |
| 操作 | 整理文件夹的分组字段与同名文件处理策略；切割音轨的界面级完整步骤与整轨原文件是否保留；简繁体转换的实际操作方式（V1 该页正文仅一张截图）；V1 自动批量修改的完整界面步骤；V1 变量完整清单 |
| 安全 | 官方是否建议备份音乐文件（**全套页面均无备份建议或不可逆告警**）；操作可否撤销（仅 T19 提到 V2 元数据版本管理支持一键回退，覆盖范围未说明） |
| 排错 | `#81`（38 评论，全仓最高，默认密码进不去）、`#397`、`#24`、`#637` 等 issue 的**评论区内容**——GitHub 未认证 API 速率限制（core 剩余 0）；FAQ 14 条中**没有**默认密码相关问答 |
| 环境 | 各 NAS 页均未给出平台版本号（群晖 DSM / 1Panel / 绿联 UGOS / 极空间）；各页均未给出 Music Tag Web 自身版本号；全站未出现任何环境变量清单（PUID/TZ 等）于 fnOS 页 |
| 播放 | Navidrome 官方默认端口（社区 compose 用 4533，不作为官方事实）；Subsonic 默认用户名与密码具体值；智能歌单支持的条件字段与操作符；网盘音乐支持的网盘类型清单；封面体积/分辨率官方限制 |

---

## 六、实操指引（写进笔记的硬约束）

1. **能力边界必须前置声明**：本项目只编辑**本地已有**音乐文件的元数据，**不提供音乐下载**；许可证为 GPL-3.0 且带附加条款（禁止商业用途、版权数据须 24 小时内清除、须遵守当地法律）。这些来自仓库 README 的免责声明段，属项目自述。
2. **必须区分 V1/V2**：端口（8001/8002）与 `command: /start` 是最容易踩的第一个坑，且 README 把两版说明并排放在同一文件里，正是误导源。
3. **必须解释三个卷各自的作用**，尤其是 `/app/download`——它决定后台刮削能否工作，而 `docker run` 示例恰好漏了它。
4. **必须把「写元数据 vs 写数据库」讲清**（T11）：这直接决定用户改完标签后"为什么在别的播放器里看不到"。
5. **必须提示先备份 `/app/data` 与音乐文件本身**：官方没有任何备份建议，但升级丢封面（`#546`）与"写元数据改原文件"两件事叠加，风险是真实的。此处应标注为**本笔记的建议**，不伪装成官方口径。
6. **激活是 V2 的强制前置**：不激活则 V2 功能不可用，且有 6 次上限、二次激活会顶掉前一台。这是用户预期管理的关键，官方文档却分散在三处且无价格。
7. **NAS 差异小节以飞牛 fnOS 为主**（用户设备），并明确 fnOS 截图自身的卷映射缺陷。
8. **社区来源一律标注层级**，不与官方口径混写。

---

## 七、开放问题（需用户或后续运行决定）

1. 用户是否已有可用的音乐库与 Navidrome/Jellyfin？若有，附录 Ap1 需要展开"边车"定位；若无，可压缩为一段。
2. 用户是否会真的使用 V2 的播放侧（Subsonic / 小爱音箱）？决定 Ap1 的篇幅。
3. 用户是否愿意为 V2 激活付费/发电？这决定要不要把激活流程写成"必过门槛"。
4. 笔记是否需要覆盖切割音轨的 ffmpeg 自装步骤（较冷门且官方文档残缺）？
5. 社区 `#546` 升级丢封面这一条，是否值得单列一个"升级前检查清单"？

---

## 八、下游交接（给 outline-generator / chapter-writer）

### 交接规则（沿用项目的既有限制）
- 派发章节写作时：**只给来源 ID + 检索位置，要求先回原文核对再落笔**；不得把本文档的概述当作原文引用。
- 凡声称"官方口径是 / 官方说明 / 原文"的地方，验收时必须逐条回源比对。
- 标 `未取到` 的内容不得出现为陈述句。

### 建议大纲骨架（对应已确认的方向 D）

**正文主线**
1. 项目定位与能力边界（含 V1/V2 之分、许可证与"不下载音乐"声明）→ D1/D6/D8/T19 + 仓库 README
2. 部署：以 Docker Compose 为主（三卷详解 + 访问 + 改密）→ D2/D3/D4
3. 首次登录与激活（V2 激活码、6 次上限、`/app/data` 持久化、时间校时）→ D3/F1/F2
4. NAS 部署差异（飞牛 fnOS 为主，群晖/绿联/极空间/1Panel 简表）→ O1/N1–N5
5. 刮削与标签编辑（写元数据 vs 写数据库 → 手动改 → 批量改 → 自动刮削 → 后台刮削）→ T11/T1/T2/T3/T8–T10/T13/T14/T15
6. 整理与批处理（整理文件夹 / 拆名 / 繁简 / 切割音轨 / 批量重命名）→ T4/T5/T6/T7/T16/F5

**附录**
- Ap1 播放侧与生态（Subsonic 服务端与客户端、小爱音箱、网盘音乐、智能歌单、去重、Navidrome 联动）→ P1–P9
- Ap2 进阶配置（MySQL / Redis / 自定义端口 / 自动更新 / 多目录挂载）→ N6–N9/F6/F8
- Ap3 排错 FAQ（14 条问答精选 + issue 聚类的高频失败 + 已知文档缺陷与矛盾）→ F1–F14/T20

### 篇幅提示
主线 6 章 + 附录 3 节，预计 3 万字量级。若最终超过 30KB 或章节数超过 3，P5/P6 阶段须按项目规则**建议拆分**（分册子目录 + README + 每章独立文件 + 前后导航 + MOC 指向 README），但最终由用户决定是否单文件。

---

## 附录：分组 claim 明细（原始记录，ID 已加组前缀）

> 以下为 6 个分组的原始素材文件，已按组前缀重命名来源 ID（D/N/T/F/P/O）。这是本文档的深度层，用于写作时逐条回源核对。



---

## 部署与启动（组前缀 `D`）


## P2 素材 — 部署与启动

### 来源表
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| D1 | V2 项目介绍 | https://xiers-organization.gitbook.io/music-tag-web-v2/xiang-mu-jie-shao.md | 官方文档 | 2026-09-14 |
| D2 | V2 快速开始 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md | 官方文档 | 2026-09-14 |
| D3 | V2 Docker部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md | 官方文档 | 2026-09-14 |
| D4 | V2 Docker Compose 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md | 官方文档 | 2026-09-14 |
| D5 | V2 名词解释 | https://xiers-organization.gitbook.io/music-tag-web-v2/ming-ci-jie-shi.md | 官方文档 | 2026-09-14 |
| D6 | V1 项目介绍 | https://xiers-organization.gitbook.io/music-tag-web/xiang-mu-jie-shao.md | 官方文档 | 2026-09-14 |
| D7 | V1 快速开始 | https://xiers-organization.gitbook.io/music-tag-web/kuai-su-kai-shi.md | 官方文档 | 2026-09-14 |
| D8 | V1 站内 “V2 版本” 页 | https://xiers-organization.gitbook.io/music-tag-web/v2-ban-ben.md | 官方文档 | 2026-09-14 |

说明：8 个分配页面全部抓取成功，无 404，无 URL 替换。

### 主张 → 来源映射

#### 端口与版本差异

- **主张**：V2 容器内监听端口为 8002，且不再需要 `command /start` 启动命令；V1 容器内端口为 8001 且需要该命令。
  - 来源：D2 | 锚点：快速开始 / “V2 版本部署” 与 “V1 版本部署” 小节
  - 原文：“容器内的端口是 8002，和不需要 command /start 命令”
  - 状态：已核实

- **主张**：V2 的 `docker run` 示例把 8002 映射到宿主机 8002，启动参数含 `--name=music-tag-web` 与 `--restart=unless-stopped`。
  - 来源：D3 | 锚点：Docker部署 / 第 2 步 “启动容器” 代码块
  - 原文：“docker run -d -p 8002:8002 ... --restart=unless-stopped xhongc/music_tag_web:latest”
  - 状态：已核实

- **主张**：V2 Compose 示例同样把 8002 映射到 8002，但重启策略写作 `restart: always`，与 `docker run` 示例不同。
  - 来源：D4 | 锚点：Docker Compose 部署 / yaml 代码块
  - 原文：“restart: always”
  - 状态：已核实

- **主张**：V2 支持 arm64、amd64、armv7 三种架构的 Docker 部署。
  - 来源：D2 | 锚点：快速开始 / “V2 版本部署” 列表项 “多架构支持”
  - 原文：“V2 版本支持 arm64、amd64 和 armv7 架构的 Docker 部署”
  - 状态：已核实

- **主张**：V1 示例端口为 8001，Portainer stacks 示例中额外使用了 `command: /start`。
  - 来源：D7 | 锚点：快速开始 / 第 2、3 步代码块
  - 原文：“docker run -d -p 8001:8001 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --restart=always”
  - 状态：已核实

#### 卷挂载

- **主张**：V2 `docker run` 官方示例只挂载两个卷：宿主音乐目录到 `/app/media`，宿主配置目录到 `/app/data`。
  - 来源：D3 | 锚点：Docker部署 / 第 2 步 “启动容器” 代码块
  - 原文：“-v /path/to/your/music:/app/media -v /path/to/your/config:/app/data”
  - 状态：已核实

- **主张**：V2 Compose 官方示例挂载三个卷：`/app/media`、`/app/data`，外加 `/app/download`。
  - 来源：D4 | 锚点：Docker Compose 部署 / yaml 代码块 volumes 段
  - 原文：“- /path/to/your/download:/app/download”
  - 状态：已核实

- **主张**：`/app/download` 被描述为“新下载音乐的目录”，且要求不与媒体库重复和重合，用途是“后台刮削监控目录”。
  - 来源：D4 | 锚点：Docker Compose 部署 / yaml 代码块下方的说明列表
  - 原文：“不与媒体库重复和重合，用于后台刮削监控目录”
  - 状态：已核实

- **主张**：V2 文档把“绑定挂载”解释为宿主机路径映射到容器内路径，并声明容器内地址“一般是开发者定义的路径位置，不可修改了”。
  - 来源：D5 | 锚点：名词解释 / “Docker目录挂载” 小节
  - 原文：“容器内的地址一般是开发者定义的路径位置，不可修改了。”
  - 状态：已核实

- **主张**：V1 的 Portainer stacks 示例中 `/app/media` 带 `:rw` 后缀，而 Compose 版 V2 示例中三个卷均未写读写后缀。
  - 来源：D7 | 锚点：快速开始 / 第 3 步 portainer stacks 代码块
  - 原文：“- /path/to/your/music:/app/media:rw”
  - 状态：已核实

#### 镜像与版本选择

- **主张**：官方镜像名为 `xhongc/music_tag_web:latest`，`latest` 表示最新版本号，也可指定版本，页面举例“2.1.7”。
  - 来源：D2 | 锚点：快速开始 / “docker 镜像说明” 小节
  - 原文：“latest 为最新版本号，你也可以指定版本，例如：2.1.7, ...”
  - 状态：已核实（注意：2.1.7 仅为举例，页面未声明其为当前版本）

- **主张**：页面指向 Docker Hub 的 tags 列表页用于查看可用版本标签。
  - 来源：D2 | 锚点：快速开始 / “docker 镜像说明” 小节内的 dockerhub 链接
  - 原文：“可以在 dockerhub 页面查看”
  - 状态：已核实

- **主张**：网络问题拉不动镜像时，官方给出阿里云镜像 `registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest`，做法是替换镜像名。
  - 来源：D2 | 锚点：快速开始 / “docker 镜像说明” 小节末段
  - 原文：“阿里云镜像名称：registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest”
  - 状态：已核实

- **主张**：V1 页面给出的镜像名与 V2 相同，均为 `xhongc/music_tag_web:latest`，页面未区分两个大版本的镜像仓库。
  - 来源：D7 | 锚点：快速开始 / 第 1 步 “从Docker Registry拉取镜像”
  - 原文：“docker pull xhongc/music_tag_web:latest”
  - 状态：已核实

#### 访问地址与首次登录

- **主张**：V2 安装后访问地址为 `http://127.0.0.1:8002`，页面同时提到可用设备实际 IP 加端口 8002 访问。
  - 来源：D3 | 锚点：Docker部署 / 第 3 步 “访问应用”
  - 原文：“在网页浏览器中输入 http://127.0.0.1:8002”
  - 状态：已核实

- **主张**：V2 默认账号密码为 `admin/admin`，登录后进入管理界面可修改默认密码。
  - 来源：D3 | 锚点：Docker部署 / 第 4 步 “修改默认密码（可选）”
  - 原文：“登录后，默认账号密码为 admin/admin。”
  - 状态：已核实

- **主张**：反向代理进入报 csrf 错误时，页面建议改用局域网地址进入。
  - 来源：D3 | 锚点：Docker部署 / 第 4 步 “修改默认密码（可选）” 末条
  - 原文：“如果你反向代理页面进去报错 csrf 错误，请用局域网地址进入。”
  - 状态：已核实

- **主张**：V1 访问路径带 `/admin` 后缀，为 `127.0.0.1:8001/admin`，默认账号密码同样是 `admin/admin`。
  - 来源：D7 | 锚点：快速开始 / 第 4 步 “修改默认密码（可选）”
  - 原文：“访问在 127.0.0.1:8001/admin 默认账号密码 admin/admin”
  - 状态：已核实（与 V2 的差异：V2 未在部署页写明 `/admin` 后缀）

- **主张**：V2 支持登录后修改 Subsonic 默认账号密码，修改后可能需要重新登录，页面未加载则尝试刷新。
  - 来源：D3 | 锚点：Docker部署 / 第 5 步 “修改 Subsonic 密码（可选）”
  - 原文：“如果需要修改 Subsonic 的默认账号密码，也请在登录后进行操作。”
  - 状态：已核实

#### 激活与授权

- **主张**：V2 需在登录后激活：点击 V1 标签，按提示输入 V2 激活码完成激活。
  - 来源：D3 | 锚点：Docker部署 / 第 6 步 “激活 V2 版本”
  - 原文：“登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。”
  - 状态：已核实

- **主张**：输入激活码报错时，官方建议检查服务器时间是否为正常北京时间；仍失败则联系作者。
  - 来源：D3 | 锚点：Docker部署 / 第 7 步 “遇到问题时”
  - 原文：“请检查和校正服务器时间，保证时间为正常的北京时间。”
  - 状态：已核实

- **主张**：激活码获取方式为赞助项目（爱发电），无法访问时可直接联系开发者微信号 `charlesnowed`。
  - 来源：D1 | 锚点：项目介绍 / “激活方式” 小节
  - 原文：“通过赞助我们的项目 爱发电 来获得激活码。”
  - 状态：已核实

- **主张**：V2 具有 V1 版本的全部功能，并可能增加新特性或改进。
  - 来源：D1 | 锚点：项目介绍 / 正文首段后
  - 原文：“V2 版本具有 V1 版本的所有功能”
  - 状态：已核实

- **主张**：V1 快速开始页未提及任何激活或授权步骤，流程止于修改默认密码。
  - 来源：D7 | 锚点：快速开始 / 全文
  - 原文：“此时你已经部署好了，你想知道具体怎么使用，请往下看吧。”
  - 状态：已核实

#### 名词与背景（辅助理解部署语境）

- **主张**：官方定义“刮削”为自动识别音乐文件并在线获取专辑封面、歌曲名称、艺术家、专辑信息、流派和发行日期等数据。
  - 来源：D5 | 锚点：名词解释 / “刮削” 小节
  - 原文：“自动识别音乐文件，并在线获取相应的专辑封面、歌曲名称、艺术家、专辑信息、流派和发行日期等数据”
  - 状态：已核实

- **主张**：官方把“后台刮削”描述为在固定文件目录下自动完成搜索元数据、整理文件夹、重命名等一系列操作。
  - 来源：D5 | 锚点：名词解释 / “后台刮削” 小节
  - 原文：“固定的文件目录下，可自动从音乐流媒体平台搜索元数据、整理文件夹、重命名等一系列操作”
  - 状态：已核实（与 D4 的 `/app/download` 监控目录说明互为呼应）

- **主张**：官方开放 API 中，info 接口供 homepage 展示信息，lyrics 接口供音流 app 展示歌词，health 接口供 Docker 健康检查心跳检测。
  - 来源：D5 | 锚点：名词解释 / “开放API” 小节
  - 原文：“health接口可供docker健康检查心跳检测”
  - 状态：已核实

- **主张**：V1 官方声明支持的音频格式为 FLAC、APE、WAV、AIFF、WV、TTA、MP3、MP4、M4A、OGG、MPC、OPUS、WMA、DSF、DFF。
  - 来源：D6 | 锚点：项目介绍 / 首段
  - 原文：“支持FLAC, APE, WAV, AIFF, WV, TTA, MP3, MP4, M4A, OGG, MPC, OPUS, WMA, DSF, DFF等音频格式”
  - 状态：已核实

- **主张**：V1 项目源码地址为 GitHub `xhongc/music-tag-web`，作者署名 xier，官网为 musictagweb.com。
  - 来源：D6 | 锚点：项目介绍 / 正文链接与署名行
  - 原文：“https://github.com/xhongc/music-tag-web”
  - 状态：已核实

- **主张**：V1 站内 “V2 版本” 页仅有一句定位描述与一个功能预览图，并指向 V2 文档站，无部署细节。
  - 来源：D8 | 锚点：V2 版本 / 全文
  - 原文：“是集合音乐标签刮削和音乐播放一体的个人音乐库解决方案。”
  - 状态：已核实

### 本组矛盾与不一致

- **卷集合不一致（核心）**：同为 V2 官方页面，`docker run` 示例只挂 2 个卷，Compose 示例挂 3 个卷。
  - D3 原文：“-v /path/to/your/music:/app/media -v /path/to/your/config:/app/data”
  - D4 原文：“- /path/to/your/download:/app/download”
  - 影响：按 `docker run` 部署会缺少 `/app/download`，而后台刮削监控目录依赖该挂载点（D4 说明）。两组示例挂载集合不同，官方未说明二者等价或如何取舍。

- **重启策略写法不一致**：D3 用 `--restart=unless-stopped`，D4 用 `restart: always`；D7 的 V1 `docker run` 用 `--restart=always`。
  - D3 原文：“--restart=unless-stopped”
  - D4 原文：“restart: always”
  - 影响：同为官方示例，重启语义不同，官方未说明推荐哪种。

- **访问路径写法不一致**：V1 明确给出带 `/admin` 的登录地址，V2 部署页只给根地址。
  - D7 原文：“访问在 127.0.0.1:8001/admin”
  - D3 原文：“输入 http://127.0.0.1:8002”
  - 影响：V2 是否需要 `/admin` 后缀，分配页面中未取到明确说法。

- **文档内容疑似串页**：V2 Docker 部署页第 3 步提到“绿联设备”，而该页并非绿联专题页（llms.txt 中另有独立的绿联部署页）。
  - D3 原文：“或者绿联设备的实际 IP 地址加上端口 8002”
  - 状态：已核实为原文如此；[推断] 该句疑为从绿联部署页复制的残留表述。

- **激活入口表述含糊**：D3 说点“V1 标签”输入 V2 激活码，但 D1 只讲如何获取激活码，未说明界面入口；两页未给出界面截图或字段名。
  - D3 原文：“登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。”
  - 影响：首次登录后的激活路径描述不完整。

- **版本示例数字易被误读**：D2 用 “2.1.7” 作为“指定版本”的举例，未声明其为当前版本号或最低要求。
  - D2 原文：“你也可以指定版本，例如：2.1.7, ...”
  - 状态：已核实为原文如此；不得据此断言 2.1.7 是当前版本。

### 未取到的信息

- 官方页面**未使用“必填/可选”字样标注任何卷挂载**：哪些挂载点是必需、哪些可省略，分配页面中未取到明确结论（`未取到`）。
- `/app/download` 是否必需、缺失时后台刮削是否可用：`未取到`。
- 除 `/app/media`、`/app/data`、`/app/download` 之外是否还有其他可挂载路径（如歌词、插件、日志目录）：分配页面中 `未取到`。
- `latest` 与固定版本标签之间的官方选择建议（是否推荐固定版本）：`未取到`（D2 只陈述可指定，未给建议）。
- 当前最新版本号：`未取到`（D2 的 2.1.7 仅为示例，不是版本声明）。
- 是否存在 host 网络模式、自定义端口配置：llms.txt 中有“自定义服务端口”专页，但不在本次分配范围，`未取到`。
- 激活码激活失败、无响应 的详细排查步骤：llms.txt 中存在该专页，不在分配范围，`未取到`；D3 仅给出“校正服务器时间”一条。
- 各 NAS 平台（群晖、1panel、绿联、fnos、极空间）部署步骤：不在分配范围，`未取到`。
- 环境变量清单（V2 部署页未出现任何环境变量示例）：`未取到`。
- 镜像体积、资源要求、数据库默认类型在部署页的说明：`未取到`（llms.txt 提到默认 Sqlite，但该表述在“Mysql 部署”专页摘要中，非本次分配的 8 页正文）。


---

## NAS 平台部署与进阶配置（组前缀 `N`）


## P2 素材 — NAS 平台部署与进阶配置

### 来源表

| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| N1 | 群晖部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/qun-hui-bu-shu.md | 官方文档 | 2026-09-14 |
| N2 | 1panel部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/1panel-bu-shu.md | 官方文档 | 2026-09-14 |
| N3 | 绿联部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/l-lian-bu-shu.md | 官方文档 | 2026-09-14 |
| N4 | 飞牛云fnos部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方文档 | 2026-09-14 |
| N5 | 极空间部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/ji-kong-jian-bu-shu.md | 官方文档（页面自述转载第三方） | 2026-09-14 |
| N6 | Mysql 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu.md | 官方文档 | 2026-09-14 |
| N7 | 外置Redis服务 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md | 官方文档 | 2026-09-14 |
| N8 | 自定义服务端口 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/zi-ding-yi-fu-wu-duan-kou.md | 官方文档 | 2026-09-14 |
| N9 | 容器自动更新 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md | 官方文档 | 2026-09-14 |

层级说明：9 页均取自官方 GitBook（xiers-organization.gitbook.io/music-tag-web-v2）。N5 页面正文自述教程转载自第三方网站，涉及 N5 的步骤主张按**社区实践**看待，不与官方自述步骤混列。

---

### 主张 → 来源映射

#### A. 各 NAS 平台部署路径

- **主张**：群晖的入口是「注册表」搜索 `music_tag_web`，官方说明"第一个就是本项目的镜像"，镜像名为 `xhongc/music_tag_web`。
  - 来源：N1 | 锚点：群晖部署 / 正文第 1 步（注册表）
  - 原文："在注册表中搜索 music\_tag\_web, 第一个就是本项目的镜像，xhongc/music\_tag\_web"
  - 状态：已核实

- **主张**：群晖端口配置中容器内必须是 8002（第二个值），容器外第一个值可随意填写。
  - 来源：N1 | 锚点：群晖部署 / 正文第 2 步「填写配置」
  - 原文："端口配置容器内是 8002（第二个值），容器外可以随意填写你喜欢的（第一个值）"
  - 状态：已核实

- **主张**：群晖需把音乐文件映射到 `/app/media`、新建目录映射到 `/app/data`，官方两次强调"此路径不可更改"。
  - 来源：N1 | 锚点：群晖部署 / 正文第 2 步「存储空间设置」
  - 原文："将你的音乐文件映射到/app/media    此路径不可更改。" / "映射到 /app/data    此路径不可更改。"
  - 状态：已核实

- **主张**：1panel 有两个方式，方式一为「应用商店安装（推荐）」，方式二为「镜像安装」。
  - 来源：N2 | 锚点：1panel部署 / 小节标题「方式一、应用商店安装（推荐）」「方式二、镜像安装」
  - 原文："## 方式一、应用商店安装（推荐）" / "## 方式二、镜像安装"
  - 状态：已核实

- **主张**：1panel 应用商店安装的默认挂载路径为 `./data:/app/media:rw` 与 `./config:/app/data`。
  - 来源：N2 | 锚点：1panel部署 / 方式一 第 2 步「点击安装即可」
  - 原文："默认挂载路径为" / ".\/data:/app/media:rw" / ".\/config:/app/data"
  - 状态：已核实

- **主张**：1panel 自定义媒体库需编辑 compose 文件改挂载地址，示例为 `<你的媒体库地址>:/app/media:rw`。
  - 来源：N2 | 锚点：1panel部署 / 方式一 第 3 步 代码块
  - 原文："如需自定义媒体库地址，则编辑 compose 文件修改挂载的地址，例如："
  - 状态：已核实

- **主张**：1panel 镜像安装的镜像为 Docker Hub 的 `xhongc/music_tag_web:latest`，容器端口必须 8002 不能改变，协议选 TCP。
  - 来源：N2 | 锚点：1panel部署 / 方式二 第 1–2 步
  - 原文："容器端口必须是 8002（第二个值）不能改变，协议选 TCP 协议"
  - 状态：已核实

- **主张**：1panel 部署完成后需"登录后 点击V1 标签，输入 V2 激活 即可完成激活"。
  - 来源：N2 | 锚点：1panel部署 / 正文末段
  - 原文："在登录后 点击V1 标签，输入 V2 激活 即可完成激活。"
  - 状态：已核实

- **主张**：绿联走 SSH + `sudo -i`，随后用一条 docker run 命令启动，端口映射 `-p 8002:8002`。
  - 来源：N3 | 锚点：绿联部署 / 第 1–4 步 代码块
  - 原文："使用 `sudo -i` 命令获取管理员权限。" / "docker run -d -p 8002:8002 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --name=music-tag-web --restart=unless-stopped xhongc/music\_tag\_web:latest"
  - 状态：已核实

- **主张**：绿联页面要求把 `/path/to/your/music` 与 `/path/to/your/config` 替换为 NAS 上的绝对路径，后者需新建目录。
  - 来源：N3 | 锚点：绿联部署 / 第 4 步后说明段
  - 原文："请确保将 `/path/to/your/music` 替换为你NAS上的音乐文件夹的绝对路径，并且 `/path/to/your/config` 替换为一个你新创建的目录路径"
  - 状态：已核实

- **主张**：绿联部署完成后的访问地址为绿联设备 IP 加端口 8002，即 `http://greenlink_ip:8002`。
  - 来源：N3 | 锚点：绿联部署 / 第 5 步
  - 原文："输入绿联设备的IP地址后跟端口号8002"
  - 状态：已核实

- **主张**：飞牛 fnOS 页面首行标注"fnos版本：0.8.24"，这是全组唯一出现的 NAS 系统版本号。
  - 来源：N4 | 锚点：飞牛云fnos部署 / 标题下方首行
  - 原文："fnos版本：0.8.24"
  - 状态：已核实（该数字为页面原文；其指 fnOS 系统版本还是其它含义，页面未明写，[推断] 为作者测试所用 fnOS 系统版本）

- **主张**：飞牛 fnOS 第一步是进入 Docker 界面搜索 `xhongc/music_tag_web` 点击下载，再"选择对应版本：latest"，然后等待下载完成。
  - 来源：N4 | 锚点：飞牛云fnos部署 / 正文开头三步（附图）
  - 原文："进入docker界面搜索 xhongc/music\_tag\_web 点击下载" / "选择对应版本：latest" / "等待下载完成"
  - 状态：已核实

- **主张**：飞牛 fnOS 明确给出两条并列部署路径——"两种方式可以部署，二选一：第一种：容器部署 / 第二种：Compose部署"。
  - 来源：N4 | 锚点：飞牛云fnos部署 / 正文「两种方式可以部署，二选一」
  - 原文："两种方式可以部署，二选一" / "第一种：容器部署" / "第二种：Compose部署"
  - 状态：已核实

- **主张**：[重要缺口] 飞牛 fnOS 页的容器部署与 Compose 部署**只有截图、没有可读文字步骤**，各表单字段名与取值在 markdown 中取不到。
  - 来源：N4 | 锚点：飞牛云fnos部署 / 第一种「容器部署」下 4 张 figure、第二种下 4 张 figure
  - 原文：（图注为空）"<figcaption></figcaption>"
  - 状态：已核实（该页 markdown 正文除 5 行文字与图片链接外无表单描述）

- **主张**：飞牛 fnOS 页给出访问端口 8002、默认账号密码都是 admin，并要求"左上角V1标签点击激活V2版本"。
  - 来源：N4 | 锚点：飞牛云fnos部署 / 第一种「容器部署」末段
  - 原文："成功部署访问8002端口，默认账号密码 都为 admin，左上角V1标签点击激活V2版本"
  - 状态：已核实

- **主张**：极空间页面自述作者没有极空间 NAS，教程转载自第三方网站 `https://izspace.cn/music/musictag.html`。
  - 来源：N5 | 锚点：极空间部署 / 标题下方首行
  - 原文："由于我没有极空间nas 教程来自网站：https\://izspace.cn/music/musictag.html"
  - 状态：已核实（来源自述；因此下方极空间步骤宜按 社区实践 标注）

- **主张**：[社区实践] 极空间步骤为：拉取镜像 → 双击下载后的镜像 → 创建 Docker 文件夹目录 → 添加目录映射 → 添加端口。
  - 来源：N5 | 锚点：极空间部署 / 第一至第五步
  - 原文："1. 拉取music tag web镜像" / "第二步，双击下载后的镜像文件" / "第三步，创建 Docker 文件夹目录" / "第五步，添加端口也可以是【host】默认应该是 8002，我选择的是自定义端口【bridge】"
  - 状态：已核实

- **主张**：[社区实践] 极空间的目录映射为：本地音乐目录映射 `/app/media`、新建的 Docker 配置目录映射 `/app/data`，两者均需替换为自己的目录。
  - 来源：N5 | 锚点：极空间部署 / 第四步
  - 原文："本地存放音乐的目录 / 我的文件 /Music【替换成自己的目录】/app/media 刚新建的 Docker 配置目录 / 高速存储 /Docker/MuasiTag/config【替换成自己的目录】/app/data"
  - 状态：已核实

#### B. Mysql 部署

- **主张**：该页说明其要解决的问题是 Sqlite 并发写入易报 `sqlite database is locked`，因此支持替换为 MySQL。
  - 来源：N6 | 锚点：Mysql 部署 / 正文首段
  - 原文："本项目默认采用Sqlite数据库，sqlite 在并发写入时容易出现sqlite database is locked，因此支持提供替换成为 msyql 数据库"
  - 状态：已核实

- **主张**：默认数据库是 Sqlite，MySQL 为可选替换；示例中各 MYSQL_* 变量均注明"没有可以不填，默认使用 sqlite"。
  - 来源：N6 | 锚点：Mysql 部署 / 「在 Music Tag Web 中配置 mysql」docker compose 命令代码块注释
  - 原文："MYSQL_HOST=192.168.1.24 # mysql 局域网ip地址（没有可以不填，默认使用 sqlite）"
  - 状态：已核实

- **主张**：方法一（推荐）是在一个 yaml 中同时部署 MySQL 与 Music Tag Web 两个容器，并需替换密码、音乐目录、配置目录三处。
  - 来源：N6 | 锚点：Mysql 部署 / 方法一「编写 docker-compose.yml 文件」与「修改配置说明」
  - 原文："在一个 yaml 文件中部署 MySQL 和 Music Tag Web 两个容器。" / "首次部署时，建议**不额外修改任何默认配置**"
  - 状态：已核实

- **主张**：MySQL 侧环境变量为 `MYSQL_ROOT_PASSWORD` 与 `MYSQL_DATABASE: music_tag`，后者注释写明"数据库名称，无需修改"。
  - 来源：N6 | 锚点：Mysql 部署 / 方法一 yaml 代码块 environment
  - 原文："MYSQL_DATABASE: music\_tag  # 数据库名称，无需修改"
  - 状态：已核实

- **主张**：Music Tag Web 侧需设置 MYSQL_HOST / MYSQL_PASSWORD / MYSQL_DB_NAME / MYSQL_USER / MYSQL_PORT，另有 WORKER_NUM 控制后台任务线程数。
  - 来源：N6 | 锚点：Mysql 部署 / 方法一 yaml 代码块 environment 与「docker compose 命令」注释
  - 原文："WORKER\_NUM=8 #  后台并发执行任务的worker数量"
  - 状态：已核实

- **主张**：MySQL 相关变量默认值为 MYSQL_USER=root、MYSQL_PORT=3306；MYSQL_USER"默认为 root，如果你没额外配置"。
  - 来源：N6 | 锚点：Mysql 部署 / 方法二末段变量说明
  - 原文："MYSQL\_USER：默认为 root， 如果你没额外配置。" / "MYSQL\_PORT： 默认端口为 3306"
  - 状态：已核实

- **主张**：配置后打不开时该页给出 5 条排查项，并称"基本能解决 90% 的问题了"。
  - 来源：N6 | 锚点：Mysql 部署 / 「配置完成后打不开 music tag web？」
  - 原文："1. MySQL 端口是否暴露出来 2. music tag web 里是否能访问到 mysql 3. 如果是原先就部署有 mysql，是否创建了 music\_tag 的数据库 4. 检查数据库的配置是否有拼写错误 5. mysql 版本太新了， 可以使用 mysql:5.7"
  - 状态：已核实

#### C. 自定义服务端口

- **主张**：该页声明其解决的问题是：使用 host 网络模式出现端口冲突时，可通过环境变量自定义端口。
  - 来源：N8 | 锚点：自定义服务端口 / 首段与「一、自定义服务端口（解决端口冲突）」
  - 原文："如果你使用网络模式host，出现端口冲突，可以进行自定义端口号"
  - 状态：已核实

- **主张**：host 模式下直接在 `environment` 添加端口变量即可，**无需修改 `ports`**。
  - 来源：N8 | 锚点：自定义服务端口 / 「三、不同网络模式的配置方法」1. Host 网络模式
  - 原文："直接在 `environment` 中添加需自定义的端口变量，无需修改 `ports` 配置。"
  - 状态：已核实

- **主张**：bridge 模式一般无需改容器内端口，只映射主机端口；若确要改容器内端口，必须同时改 `environment` 与 `ports` 两处。
  - 来源：N8 | 锚点：自定义服务端口 / 「三、不同网络模式的配置方法」2. Bridge 网络模式
  - 原文："1. 在 `environment` 中修改对应端口变量（如 `GUNICORN_PORT`）。2. 在 `ports` 中同步映射新的容器内端口（如 `“8006:8006”`）。"
  - 状态：已核实

- **主张**：容器内端口变量与默认值为：GUNICORN_PORT=8001、NGINX_PORT=8002、SUPERVISOR_PORT=9001、REDIS_PORT=6379。
  - 来源：N8 | 锚点：自定义服务端口 / 「二、核心环境变量说明」表格
  - 原文："**GUNICORN\_PORT** | 后端服务端口 | 8001" / "**NGINX\_PORT** | Nginx代理后的后端服务端口 | 8002" / "**SUPERVISOR\_PORT** | Supervisor进程管理端口 | 9001"
  - 状态：已核实

- **主张**：完整示例中把主机与容器内端口统一改为 8006（`"8006:8006"` 且 NGINX_PORT=8006），同时设 GUNICORN_PORT=8003。
  - 来源：N8 | 锚点：自定义服务端口 / 「四、完整配置示例」yaml 代码块
  - 原文："- "8006:8006"  # 主机端口:容器内端口（与NGINX\_PORT保持一致）" / "- GUNICORN\_PORT=8003  # 自定义后端服务端口"
  - 状态：已核实

#### D. 容器自动更新

- **主张**：自动更新由 Web 界面一键触发，官方声明其会下载最新程序、停旧容器、启新容器、清理旧镜像并保留数据与配置。
  - 来源：N9 | 锚点：容器自动更新 / 「📋 什么是自动更新？」
  - 原文："一键自动更新功能" / "✅ 保留你的所有数据和配置"
  - 状态：已核实

- **主张**：Web 界面路径为：登录 → 左侧菜单「系统设置」→「系统信息」→ 查看「系统版本」→ 出现「检查更新」按钮。
  - 来源：N9 | 锚点：容器自动更新 / 「步骤 1：检查是否有新版本」
  - 原文："点击左侧菜单的「系统设置」→「系统信息」" / "如果有新版本可用，会显示「检查更新」按钮"
  - 状态：已核实

- **主张**：使用自动更新前必须挂载 Docker Socket，官方原文为"在首次部署时必须挂载 Docker Socket"，镜像需 `-v /var/run/docker.sock:/var/run/docker.sock`。
  - 来源：N9 | 锚点：容器自动更新 / 「0. 🔧 重要：挂载 Docker Socket」及 yaml 代码块
  - 原文："**如果你想使用自动更新功能，在首次部署时必须挂载 Docker Socket。**"
  - 状态：已核实

- **主张**：未挂载 Socket 时官方列出的报错为"Docker客户端初始化失败""无法连接到 Docker daemon""更新按钮点击后没有反应"。
  - 来源：N9 | 锚点：容器自动更新 / 「⚠️ 没有挂载会怎样？」
  - 原文："❌ "Docker客户端初始化失败"" / "❌ "无法连接到 Docker daemon"" / "❌ 更新按钮点击后没有反应"
  - 状态：已核实

- **主张**：检查 Socket 是否挂载有两种方式：`docker inspect music-tag-web | grep docker.sock`，或进容器后 `ls -l /var/run/docker.sock`。
  - 来源：N9 | 锚点：容器自动更新 / 「🔍 检查是否正确挂载」方法 1 / 方法 2
  - 原文："docker inspect music-tag-web | grep docker.sock" / "ls -l /var/run/docker.sock"
  - 状态：已核实

- **主张**：启用自动更新时官方建议额外挂载 `/app/download` 作为后台刮削监控目录，并要求与媒体库不重复、不重合。
  - 来源：N9 | 锚点：容器自动更新 / Docker Compose 部署 yaml 与说明
  - 原文："\`/path/to/your/download\` 替换为你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录"
  - 状态：已核实

- **主张**：该页另给两种定时更新方案：crontab 每日 3 点跑一次 Watchtower，或常驻 Watchtower 以 `--interval 86400` 每 24 小时检查、`--cleanup` 清理旧镜像。
  - 来源：N9 | 锚点：容器自动更新 / 「❓ 可以自动定时更新吗？」方法 1 / 方法 2
  - 原文："0 3 \* \* \* docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music-tag-web" / "`--interval 86400`：每 24 小时检查一次更新"
  - 状态：已核实

- **主张**：网络受限时该页给出国内镜像源 `registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest`，并可 tag 回 `containrrr/watchtower:latest`。
  - 来源：N9 | 锚点：容器自动更新 / 「如果网络受限：」代码块
  - 原文："docker tag registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest containrrr/watchtower:latest"
  - 状态：已核实

- **主张**：官方称新版本镜像体积通常在 500MB-1GB，更新期间服务会短暂中断，建议低峰时段进行。
  - 来源：N9 | 锚点：容器自动更新 / 「3. 网络要求」与「❓ 更新需要多长时间？」
  - 原文："✅ 网络速度稳定（新版本镜像通常在 500MB-1GB）" / "更新期间服务会短暂中断，建议在低峰时段进行。"
  - 状态：已核实

#### E. 外置 Redis

- **主张**：外置 Redis 不是必需的——容器本身会启动一个 redis，不需要外置可以完全不配置本页内容。
  - 来源：N7 | 锚点：外置Redis服务 / 正文首段
  - 原文："容器本身就会启动一个 redis，如果你不需要**外置**的 redis，可以不进行此项的配置。"
  - 状态：已核实

- **主张**：方法一是给已有 Redis 的服务器加 `REDIS_HOST` 环境变量，默认端口 6379，改端口需同时设 `REDIS_PORT`，有密码需设 `REDIS_PASSWORD`。
  - 来源：N7 | 锚点：外置Redis服务 / 方法一 说明段
  - 原文："你需要在环境变量中添加 `REDIS_HOST`，其默认端口为 6379。" / "如果你 redis 设置了密码，需要配置 REDIS\_PASSWORD 环境变量"
  - 状态：已核实

- **主张**：方法二是在同一个 yaml 里一起部署 `redis:latest` 与 Music Tag Web，Redis 侧用 `redis-server --requirepass yourpassword` 设密码。
  - 来源：N7 | 锚点：外置Redis服务 / 方法二 yaml 代码块
  - 原文："image: redis:latest" / "command: redis-server --requirepass yourpassword # 设置密码"
  - 状态：已核实

- **主张**：方法二里 Music Tag Web 侧通过 `REDIS_HOST=redis`（服务名）、`REDIS_PASSWORD=yourpassword`、`REDIS_PORT=6379` 连接。
  - 来源：N7 | 锚点：外置Redis服务 / 方法二 yaml 代码块 environment
  - 原文："- REDIS\_HOST=redis  # 数据库主机名，使用服务名, 不需要修改" / "- REDIS\_PORT=6379  # redis 端口，无需修改"
  - 状态：已核实

---

### 本组矛盾与不一致

1. **自动更新耗时两处数字不同（N9 页内自相矛盾）**
   - 「步骤 2：执行更新」写："等待更新完成（通常需要 1-3 分钟）"
   - 「❓ 更新需要多长时间？」写："**通常 1-5 分钟**"
   - 两处均出自 N9，未说明适用条件差异，需保留原样不合并。

2. **REDIS_PORT 默认值冲突（跨 N8 / N7，且 N8 页内自相矛盾）**
   - N8 表格：「**REDIS\_PORT** | Redis服务端口 | 6379 | 选填，v2.6.0 及以上版本默认 6380」——同一单元格内既写默认 6379 又写 v2.6.0+ 默认 6380。
   - N7 正文：「其默认端口为 6379」。
   - 结论：6379 与 6380 两个默认值并存，取决于是否 v2.6.0 及以上；本组无来源可确认当前实际默认值。

3. **MYSQL_DB_NAME 的语义描述不一致（N6 页内自相矛盾）**
   - 方法一 yaml 注释："MYSQL\_DATABASE: music\_tag  # 数据库名称，无需修改"
   - 方法二 compose 注释："MYSQL\_DB\_NAME=music\_tag # 数据表名称（没有可以不填，默认使用 sqlite）"
   - 同一变量一处叫"数据库名称"、一处叫"数据表名称"，二者不等价。

4. **Compose 服务名不一致（N9 页内自相矛盾，且与其他页不一致）**
   - N9 第一段 yaml 服务名为 `music-tag-web`；N9「2. 确保数据持久化」示例中服务名变成 `web`。
   - N6、N7、N8 的 yaml 服务名统一用 `music-tag`（container_name 均为 `music-tag-web`）。
   - 影响：`depends_on`、`docker-compose up` 的服务名引用会随页面不同而变化。

5. **V2 激活步骤在各 NAS 页覆盖不一致**
   - N2 写："在登录后 点击V1 标签，输入 V2 激活 即可完成激活。"
   - N4 写："左上角V1标签点击激活V2版本"
   - N1（群晖）、N3（绿联）**完全没有提到激活步骤**；N5（极空间）也未提到。
   - 不能据此推断这些平台无需激活，只能记录为页面缺失。

6. **默认账号密码仅一个来源**
   - 只有 N4 给出"默认账号密码 都为 admin"；其余 8 页均未提及默认凭据。
   - 无冲突来源，但覆盖度极低，不宜当作全平台通用结论。

7. **极空间页的来源层级与其他页不同**
   - N5 页面自述"由于我没有极空间nas 教程来自网站：https\://izspace.cn/music/musictag.html"，属转载的社区实践；其余 8 页为官方自述步骤。二者不可混引。

---

### 未取到的信息

- **飞牛 fnOS 页面最关键的部署细节取不到**：N4 的「容器部署」与「Compose部署」两节全部由截图承载（共 8 张 figure），markdown 正文无任何表单字段名、端口值、路径值或 yaml 文本。本次未对图片做 OCR，故 fnOS 容器部署/Compose 部署的具体配置项为 `未取到`。
- **fnOS 页"fnos版本：0.8.24"的含义未取到**：页面未说明该数字指 fnOS 系统版本、应用版本还是其它，仅照录原文。
- **通用 Compose 部署页（`kuai-su-kai-shi/docker-compose-bu-shu.md`）与 Docker 部署页（`kuai-su-kai-shi/docker-bu-shu.md`）不在本组分配范围**，本次未抓取。因此"各 NAS 方式与通用 Compose 方法的逐字段差异"只能以本组 9 页内出现的 compose 片段（N6 方法一/方法二、N7 方法二、N8 示例、N9 前置准备）为基准，无法与通用 Compose 页做权威对照。
- **群晖页没有给出任何 compose 或 docker run 片段**，仅描述 UI 表单填写（注册表 / 端口 / 存储空间），也未给出群晖 DSM 版本号。
- **1panel 页未给出 1Panel 面板版本号**，也未说明应用商店中该应用的版本。
- **绿联页未给出绿联系统（UGOS）版本号**，也未给出镜像 tag 之外的版本信息。
- **极空间页未在文字中给出实际端口号与完整映射路径**（只给出"【替换成自己的目录】"占位），也未给出极空间系统版本。
- **各 NAS 页均未给出 Music Tag Web 应用自身的版本号**；全组唯一版本号线索为 N4 的 "fnos版本：0.8.24"（含义未明）与 N8 提到的 "v2.6.0 及以上版本"。
- **N4 未说明 fnOS「容器部署」与「Compose部署」二选一时官方推荐哪一种**，页面仅写"二选一"。
- **N9 未给出当前最新版本号**，也未给出检查更新时"确认容器名称"对话框里除名称外的其它字段。
- **N8 未说明 `GUNICORN_PORT`、`NGINX_PORT`、`SUPERVISOR_PORT` 三者之间是否必须保持特定关系**，仅示例中让 NGINX_PORT 与 ports 容器内端口一致。
- **外置 Redis 未说明迁移影响**：切换外置 Redis 后原有缓存/数据是否重建为 `未取到`。
- **MySQL 迁移数据未说明**：从 Sqlite 切换到 MySQL 时既有 Sqlite 数据是否迁移、如何迁移，N6 全页 `未取到`。


---

## 标签编辑与刮削操作主线（组前缀 `T`）


## P2 素材 — 标签编辑与刮削操作主线

### 来源表
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| T1 | V1 手动修改标签 | https://xiers-organization.gitbook.io/music-tag-web/shou-dong-xiu-gai-biao-qian.md | 官方文档 | 2026-09-14 |
| T2 | V1 批量修改 | https://xiers-organization.gitbook.io/music-tag-web/pi-liang-xiu-gai.md | 官方文档 | 2026-09-14 |
| T3 | V1 自动批量修改 | https://xiers-organization.gitbook.io/music-tag-web/zi-dong-pi-liang-xiu-gai.md | 官方文档 | 2026-09-14 |
| T4 | V1 整理文件夹 | https://xiers-organization.gitbook.io/music-tag-web/zheng-li-wen-jian-jia.md | 官方文档 | 2026-09-14 |
| T5 | V1 简繁体转换 | https://xiers-organization.gitbook.io/music-tag-web/jian-fan-ti-zhuan-huan.md | 官方文档 | 2026-09-14 |
| T6 | V1 拆分文件名称 | https://xiers-organization.gitbook.io/music-tag-web/chai-fen-wen-jian-ming-cheng.md | 官方文档 | 2026-09-14 |
| T7 | V1 切割音轨 | https://xiers-organization.gitbook.io/music-tag-web/qie-ge-yin-gui.md | 官方文档 | 2026-09-14 |
| T8 | V2 手动刮削 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/shou-dong-gua-xiao.md | 官方文档 | 2026-09-14 |
| T9 | V2 自动刮削 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/zi-dong-gua-xiao.md | 官方文档 | 2026-09-14 |
| T10 | V2 后台刮削 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/hou-tai-gua-xiao.md | 官方文档 | 2026-09-14 |
| T11 | V2 基本设置 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/ji-ben-she-zhi.md | 官方文档 | 2026-09-14 |
| T12 | V2 变量的使用说明 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/bian-liang-de-shi-yong-shuo-ming.md | 官方文档 | 2026-09-14 |
| T13 | V2 名词解释 | https://xiers-organization.gitbook.io/music-tag-web-v2/ming-ci-jie-shi.md | 官方文档 | 2026-09-14 |
| T14 | V2 教程文章：手动刮削能实现哪些功能？ | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/shou-dong-gua-xiao-neng-shi-xian-na-xie-gong-neng.md | 官方文档（教程文章） | 2026-09-14 |
| T15 | V2 教程文章：后台刮削怎么玩 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/hou-tai-gua-xiao-zen-me-wan.md | 官方文档（教程文章） | 2026-09-14 |
| T16 | V2 教程文章：批量重命名文件名称 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/pi-liang-zhong-ming-ming-wen-jian-ming-cheng.md | 官方文档（教程文章） | 2026-09-14 |
| T17 | V1 llms.txt（页面树/顺序） | https://xiers-organization.gitbook.io/music-tag-web/llms.txt | 官方文档 | 2026-09-14 |
| T18 | V2 llms.txt（页面树/顺序） | https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt | 官方文档 | 2026-09-14 |
| T19 | V2 项目介绍 | https://xiers-organization.gitbook.io/music-tag-web-v2/xiang-mu-jie-shao.md | 官方文档 | 2026-09-14 |
| T20 | V2 常见问题 | https://xiers-organization.gitbook.io/music-tag-web-v2/chang-jian-wen-ti.md | 官方文档 | 2026-09-14 |

说明：11 个分配页面均按给定 URL 抓取，无 404、无需替换 URL。其中 T8、T9 抓取成功但**正文为空**（详见“未取到的信息”）。

### 主张 → 来源映射

#### A. 页面顺序是否等同工作流顺序（本组前提假设的核验）

- **主张**：V1 手册 llms.txt 的页面顺序依次为：项目介绍 → 快速开始 → 手动修改标签 → 批量修改 → 自动批量修改 → 整理文件夹 → 简繁体转换 → 拆分文件名称 → 切割音轨 → V2 版本。
  - 来源：T17 | 锚点：llms.txt “Music Tag Web” 列表项顺序
  - 原文：“- [手动修改标签](...)：手动刮削，针对个别的音乐文件进行修改”
  - 状态：已核实

- **主张**：V1 llms.txt 为“手动修改标签”页写的摘要直接使用“手动刮削”一词，说明 V1 页名“修改标签”与 V2 术语“刮削”指同一操作。
  - 来源：T17 | 锚点：llms.txt “手动修改标签”条目描述
  - 原文：“手动刮削，针对个别的音乐文件进行修改”
  - 状态：已核实

- **主张**：V1 llms.txt 各页摘要自身标注了三种批量级操作的差别：批量修改“注意是手动填写”，自动批量修改“自动从你选定的标签源中匹配”。
  - 来源：T17 | 锚点：llms.txt “批量修改”“自动批量修改”条目描述
  - 原文：“勾选多个文件或文件夹进行批量修改文件中相同的元数据（注意是手动填写）”
  - 状态：已核实

#### B. 各操作的前置状态与点击动作

- **主张**：手动修改标签流程为 6 步：配置说明 → 查询音乐标签信息 → 选中应用的标签元数据 → 歌词翻译 → 歌词操作 → 保存信息；第 1 步要求先选一个标签源并选展示字段。
  - 来源：T1 | 锚点：手动修改标签 / 编号 1–6 列表
  - 原文：“选中一个标签源，用于后续的刮削”
  - 状态：已核实

- **主张**：手动修改标签的“应用”有三种粒度：应用栏箭头按钮应用全部元数据；点击各标签下的数据独自应用；歌词栏“加载歌词”异步加载歌词数据。
  - 来源：T1 | 锚点：手动修改标签 / 第 3 步“选中应用的标签元数据”
  - 原文：“应用栏-箭头按钮 应用全部元数据”
  - 状态：已核实

- **主张**：字段选中顺序会影响页面显示顺序；这是 T1 第 1 步配置说明中明确写出的一条界面行为。
  - 来源：T1 | 锚点：手动修改标签 / 第 1 步“配置说明”
  - 原文：“选中展示字段，字段选中的顺序会影响页面的显示。”
  - 状态：已核实

- **主张**：手动修改标签支持 lrc 双向操作：开启“导出 lrc”开关把元数据中歌词导出为 `${filename}.lrc`；开启“导入 lrc”开关把同名 lrc 文件嵌入音乐元数据。
  - 来源：T1 | 锚点：手动修改标签 / 第 5 步“歌词操作”
  - 原文：“打开导出 lrc 开关，会将音乐元数据中歌词导出为 ${filename}.lrc 的歌词文件”
  - 状态：已核实

- **主张**：批量修改的前置状态是“勾选多个文件或文件夹”，且文档明确该操作修改的是各文件共有的、由用户手动填写的元数据，不是联网匹配结果。
  - 来源：T2 | 锚点：批量修改 / 标题下正文首段
  - 原文：“勾选多个文件或文件夹进行批量修改文件中相同的元数据（注意是手动填写）”
  - 状态：已核实

- **主张**：批量修改给出的两个官方示例是：批量把音乐风格改为“流行乐”；批量把文件名改为“艺术家+专辑”格式（后者需配合变量）。
  - 来源：T2 | 锚点：批量修改 / 两个“例如”段落
  - 原文：“例如： 你想要批量把音乐的风格修改为 流行乐”
  - 状态：已核实

- **主张**：自动批量修改的前置状态是已选定标签源，行为是“自动从你选定的标签源中匹配并保存到音乐文件中”，不需要手动填写元数据。
  - 来源：T3 | 锚点：自动批量修改 / 标题下正文首段
  - 原文：“自动从你选定的标签源中匹配并保存到音乐文件中”
  - 状态：已核实

- **主张**：自动批量修改提供宽松/严格两种匹配模式：宽松只按标题匹配；严格按“标题+歌手”或“标题+专辑”匹配。
  - 来源：T3 | 锚点：自动批量修改 / 编号 1“宽松模式”、2“严格模式”
  - 原文：“只根据标题匹配元数据, 可能存在同名或翻唱歌曲。”
  - 状态：已核实

- **主张**：官方对严格模式也承认会误判，并建议少量批量修改加手动辅助修正；这是文档中唯一的准确性免责表述。
  - 来源：T3 | 锚点：自动批量修改 / 第 2 项“严格模式”
  - 原文：“（也会出现错误判断的情况，建议少量批量修改，手动辅助修正。）”
  - 状态：已核实

- **主张**：拆分文件名称的前置状态是“只有文件名称存在歌曲基本信息，元数据中没有”；操作为定义标题规则，命中后把文件名中的信息嵌入元数据。
  - 来源：T6 | 锚点：拆分文件名称 / 标题下正文首段
  - 原文：“只有文件名称存在歌曲基本信息，元数据中没有的情况，可以快速的将文件名称中的基本信息嵌入到音乐元数据中。”
  - 状态：已核实

- **主张**：拆分文件名称最多支持定义两条标题规则，命中规则的文件才被修改；文档示例规则为 `${tracknumber}.${title}`。
  - 来源：T6 | 锚点：拆分文件名称 / 编号 1 及其示例
  - 原文：“支持定义两个标题规则，成功命中规则的文件会被修改。”
  - 状态：已核实

#### C. 标签源 / 提供方名单（问题 3）

- **主张**：三个抓取的 V1/V2 核心页面只使用“标签源”“音乐流媒体平台”这类泛称，未点名任何具体提供方。
  - 来源：T1 / T3 / T13 | 锚点：T1 第 1 步；T3 首段；T13 “自动刮削”词条
  - 原文：“自动从音乐流媒体平台搜索**元数据**实行**刮削**操作”
  - 状态：已核实

- **主张**：V2 项目介绍提到内置多种标签源插件并支持用户上传自定义插件，但同样未列出插件或标签源名称。
  - 来源：T19 | 锚点：项目介绍 / V2 新增功能“插件模块”
  - 原文：“**插件模块**：内置多种标签源插件，并支持用户上传自定义插件”
  - 状态：已核实

- **主张**：对 V1+V2 手册做关键词全文扫描（网易/QQ音乐/酷狗/酷我/MusicBrainz/AcoustID/Spotify/Last.fm 等），命中数为 0；本组可确认“具体提供方名单”在文档中不存在。
  - 来源：T17 / T18 | 锚点：按 llms.txt 枚举页面后逐页 grep
  - 原文：不适用（未命中）
  - 状态：[推断]（推断为文档确实未公开名单，而非抓取遗漏）

#### D. 原音频文件发生什么（问题 4）

- **主张**：V2 基本设置区分两种写入位置：写入元数据会改文件本体，写入数据库则只把信息存进 mtw 数据库，需用其 Subsonic 服务端才能显示。
  - 来源：T11 | 锚点：基本设置 / 编号 1“本地音乐写入位置”
  - 原文：“写入元数据会影响做种，写入数据库必须有 mtw 提供的 subsonic 服务端播放才能显示。”
  - 状态：已核实

- **主张**：对 webdav/网盘音乐，选“写入元数据”时行为是下载音乐→本地修改→再上传回网盘，官方称“有较为频繁的操作”。
  - 来源：T11 | 锚点：基本设置 / 编号 2“webdav 音乐写入位置”
  - 原文：“写入元数据会下载音乐后修改再上传回网盘，有较为频繁的操作”
  - 状态：已核实

- **主张**：对 webdav 音乐选“写入数据库”时，只读取音乐文件的一部分内容即可读到元数据，然后存入 mtw 数据库。
  - 来源：T11 | 锚点：基本设置 / 编号 2“webdav 音乐写入位置”
  - 原文：“写入数据库，只会读取音乐文件的一部分内容就能读到元数据，然后存入 mtw 的数据库”
  - 状态：已核实

- **主张**：V1 切割音轨的输出是“无损切割”产生的新音轨文件（页面标题即如此表述），原始整轨文件如何处理未作说明。
  - 来源：T7 | 锚点：切割音轨 / 标题下副标题
  - 原文：“使用CUE专辑标记文件无损切割整轨CD音轨”
  - 状态：已核实

- **主张**：关于“是否制作副本”“操作可否撤销”“是否备份原文件”，抓取的 11 个分配页面均无任何明文说明。
  - 来源：T1–T11 | 锚点：逐页全文检索 备份/副本/撤销/回退/不可逆 等词
  - 原文：不适用（未命中）
  - 状态：已核实（作为“文档未说明”这一事实）

- **主张**：V2 项目介绍是唯一给出“可回退”保障的地方：元数据版本管理自动记录每次修改历史，支持版本查看、差异对比与一键回退。
  - 来源：T19 | 锚点：项目介绍 / V2 新增功能“元数据版本管理”
  - 原文：“自动记录每次元数据修改历史，支持版本查看、差异对比与一键回退”
  - 状态：已核实

#### E. 整理文件夹的分组键与冲突（问题 5）

- **主张**：整理文件夹的分组依据只说“以元数据中的值”，页面未指明具体取哪个字段（标题/专辑/艺术家等），也未给出默认分组规则。
  - 来源：T4 | 锚点：整理文件夹 / 标题下正文首段
  - 原文：“将音乐文件，以元数据中的值进行分组到文件夹中”
  - 状态：已核实

- **主张**：多级目录是可选项；“整理后的根目录”用于指定整理结果的存放位置。
  - 来源：T4 | 锚点：整理文件夹 / “支持多级目录（可选）”“整理后的根目录”
  - 原文：“整理后的根目录：意味着整理后文件会存放在这个目录下。”
  - 状态：已核实

- **主张**：关于同名文件的覆盖/重命名策略，整理文件夹页无任何文字说明；未取到冲突处理规则。
  - 来源：T4 | 锚点：整理文件夹 / 全文
  - 原文：不适用（未命中）
  - 状态：已核实（作为“文档未说明”这一事实）

- **主张**：整理文件夹附带“删除空文件夹”，只删当前层级的空目录，不级联；A/B/C 全空时先删 C，要级联需再执行两次。
  - 来源：T4 | 锚点：整理文件夹 / “删除空文件夹”小节
  - 原文：“例如 A/B/C 都为空， 会优先将 C 目录删除，不会将 A/B/C 级联删除，（如果想级联删除，再执行两次）”
  - 状态：已核实

#### F. 切割音轨的输入要求（问题 6）

- **主张**：切割音轨的输入是“CUE 专辑标记文件”加整轨 CD 音轨，页面副标题明确二者配套使用。
  - 来源：T7 | 锚点：切割音轨 / 标题下副标题
  - 原文：“使用CUE专辑标记文件无损切割整轨CD音轨”
  - 状态：已核实

- **主张**：使用前必须自行下载 ffmpeg，按电脑系统架构选版本，把可执行文件放到挂载的 `/app/data/bin/` 目录，最终路径为 `/app/data/bin/ffmpeg`。
  - 来源：T7 | 锚点：切割音轨 / 编号 1–3
  - 原文：“最终路径是 /app/data/bin/ffmpeg”
  - 状态：已核实

- **主张**：ffmpeg 需要执行权限，官方给出的命令是 `chmod +x /app/data/bin/ffmpeg`。
  - 来源：T7 | 锚点：切割音轨 / “注意点”第 2 条
  - 原文：“需要有 ffmpeg 的执行权限 chmod +x /app/data/bin/ffmpeg”
  - 状态：已核实

- **主张**：切割音轨不支持 ape 格式，官方建议先把 ape 转成其他格式再切分。
  - 来源：T7 | 锚点：切割音轨 / “注意点”第 1 条
  - 原文：“ffmpeg 不支持 ape 音乐的操作，如需要切分 ape 音乐，可先将 ape 转换为其他格式。”
  - 状态：已核实

#### G. 数据丢失告警与备份建议（问题 7）

- **主张**：11 个分配页面中没有任何一页给出“请先备份音乐文件”的建议，也没有“操作不可逆”的告警。
  - 来源：T1–T11 | 锚点：逐页全文检索 备份/不可逆/丢失/风险
  - 原文：不适用（未命中）
  - 状态：已核实（作为“文档未说明”这一事实）

- **主张**：最接近数据安全的官方表述是 V2 基本设置的“写入元数据会影响做种”，提示改标签本体会破坏 BT 做种状态。
  - 来源：T11 | 锚点：基本设置 / 编号 1“本地音乐写入位置”
  - 原文：“写入元数据会影响做种”
  - 状态：已核实

- **主张**：V2 常见问题中有“删除文件夹功能”会同时删除音乐收藏中的音乐，以及“同步删除不存在的音乐”，属删除类操作提示。
  - 来源：T20 | 锚点：常见问题 / 第 6 条问答
  - 原文：“或着直接通过 操作台中的删除文件夹功能删除文件。该功能会同时删除音乐收藏中的音乐。”
  - 状态：已核实

- **主张**：后台刮削的文件转移与整理被官方定为必选项，常见问题明确回答“是的，必须要选择”，理由是保证监控是增量数据。
  - 来源：T20 | 锚点：常见问题 / 第 11 条问答
  - 原文：“A：是的，必须要选择，不然每次监控就不是增量数据”
  - 状态：已核实

- **主张**：后台刮削按官方教程会依据处理结果把文件转移到 `completed` 或 `failed` 目录，即原文件位置会被移动。
  - 来源：T15 | 锚点：后台刮削怎么玩 / “音乐文件整理（必选）”
  - 原文：“根据处理结果（成功或失败），将文件转移到相应的 `completed` 或 `failed` 目录中。”
  - 状态：已核实

#### H. V2 后台刮削的运作机制（V1 无对应页）

- **主张**：开启后台刮削后，后台每 3 分钟检查一次目标目录并执行自动刮削。
  - 来源：T10 | 锚点：后台刮削 / “开启后台刮削”段落
  - 原文：“后台会每3分钟检查 目标目录 进行自动刮削。”
  - 状态：已核实

- **主张**：后台刮削监听两个固定目录 `/app/download` 与 `/app/media/download`；前者需在部署时额外映射，后者只需在已映射的 /app/media 下新建 download 目录。
  - 来源：T10 | 锚点：后台刮削 / “后台刮削目录”及其两个代码块
  - 原文：“该目录需要自在部署docker应用时额外再映射一个目录到/app/download”
  - 状态：已核实

- **主张**：后台刮削的音乐预处理包含三项：声纹识别、乱码修复、繁体转简体。
  - 来源：T10 | 锚点：后台刮削 / “音乐预处理”
  - 原文：“支持声纹识别、乱码修复、繁体转简体”
  - 状态：已核实

- **主张**：官方教程进一步解释声纹识别的用途：对缺少艺术家或专辑元数据的音乐文件，用声纹识别尝试找到匹配信息。
  - 来源：T15 | 锚点：后台刮削怎么玩 / “音乐预处理”第 1 条
  - 原文：“对于缺少艺术家或专辑元数据的音乐文件，系统会使用声纹识别技术尝试找到匹配的信息。”
  - 状态：已核实

- **主张**：乱码修复会自动检测并修复文件名、艺术家、专辑名中的乱码；繁体转简体把所有繁体中文转成简体以保持一致。
  - 来源：T15 | 锚点：后台刮削怎么玩 / “音乐预处理”第 2、3 条
  - 原文：“系统会自动检测并修复文件名、艺术家、专辑名中的乱码问题。”
  - 状态：已核实

- **主张**：V2 名词解释把三种刮削定义为：手动刮削可自定义改元数据；自动刮削自动从音乐流媒体平台搜索元数据；后台刮削在固定目录下自动完成搜索、整理文件夹、重命名一系列操作。
  - 来源：T13 | 锚点：名词解释 / “手动刮削”“自动刮削”“后台刮削”词条
  - 原文：“固定的文件目录下，可自动从音乐流媒体平台搜索**元数据、整理文件夹、重命名**等一系列操作”
  - 状态：已核实

#### I. 变量语法（V1 与 V2 的能力差）

- **主张**：V1 对变量只说明“鼠标悬浮在标题 label 上可查看变量名称，点击即复制”，并举例 `${title}`/`${album}`，未给变量清单。
  - 来源：T2 | 锚点：批量修改 / “变量的使用”小节
  - 原文：“鼠标悬浮在标题的label上可以查看变量的名称，点击就会复制变量。”
  - 状态：已核实

- **主张**：V2 明确变量引擎基于 Mako，但仅解析 `${...}` 表达式，不支持完整 Mako 块语法。
  - 来源：T12 | 锚点：变量的使用说明 / 标题下首段
  - 原文：“当前项目基于 Mako 实现，**仅解析 `${...}` 表达式**，不支持完整 Mako 块语法。”
  - 状态：已核实

- **主张**：V2 变量清单含 `${counter}`（递增计数器）、`${null}`（空值）、`${first_artist_letter}`、`${file_suffix}`、`${language}`、`${guess_language}` 等 V1 手册完全未提及的变量。
  - 来源：T12 / T13 | 锚点：T12 “二、常用变量列表”；T13 “变量”词条
  - 原文：“| ${counter} | 计数器 |”
  - 状态：已核实

- **主张**：V2 支持条件与默认值写法，两种写法等价：`${title if title else "未知标题"}` 与简写 `${title or "未知标题"}`。
  - 来源：T12 | 锚点：变量的使用说明 / “六、条件判断（空值兜底）”
  - 原文：“${title if title else "未知标题"}”
  - 状态：已核实

- **主张**：V2 提供音轨号补零模板 `${tracknumber.zfill(2) + ". " if tracknumber else ""}`，并推荐用 zfill 而非 `{:02d}` 格式化，以兼容 `1/12` 这类特殊格式。
  - 来源：T12 | 锚点：变量的使用说明 / “九、注意事项”
  - 原文：“✅ 高兼容写法（适配 `1/12` 这类特殊格式，避免 `int` 报错）”
  - 状态：已核实

- **主张**：V2 明确列出两种不支持的写法：Mako 块语法（`% if ... % endif`）与 foobar2000 风格语法（`$if($num(...))`）。
  - 来源：T12 | 锚点：变量的使用说明 / “八、当前不支持的写法”
  - 原文：“2. **foobar2000 风格语法（不支持）**”
  - 状态：已核实

- **主张**：V2 官方教程演示用正则命名组重命名文件，例如 `(?P<tracknumber>\d+)\.(?P<title>\w+)` 解析 `01.夜曲.flac`。
  - 来源：T16 | 锚点：批量重命名文件名称 / “场景1”代码块
  - 原文：“(?P<tracknumber>\d+)\.(?P<title>\w+)”
  - 状态：已核实

- **主张**：V2 重命名时文件扩展名会自动沿用源文件扩展名，用户无需在模板中再写扩展名。
  - 来源：T16 | 锚点：批量重命名文件名称 / “场景2”变量使用示例
  - 原文：“文件扩展名会继续填充源文件的扩展名，所以你无需额外输入文件扩展名。”
  - 状态：已核实

#### J. 手动刮削的能力清单（V2 教程文章口径）

- **主张**：V2 教程文章列出手动刮削支持且均可批量执行的能力：重命名文件名、手动补充艺术家/专辑等元数据、导出歌词为 lrc、lrc 嵌入音乐、导出专辑封面、导入专辑封面。
  - 来源：T14 | 锚点：手动刮削能实现哪些功能？ / 项目符号列表
  - 原文：“下面功能均支持批量操作。”
  - 状态：已核实

- **主张**：手动刮削的前置动作被描述为“选择需要修改文件或文件目录”，即可自定义修改音乐元数据中的内容。
  - 来源：T14 | 锚点：手动刮削能实现哪些功能？ / 首段
  - 原文：“选择需要修改文件或文件目录，可自定义修改音乐元数据中的内容。”
  - 状态：已核实

- **主张**：V2 教程文章要求批量重命名前先确认文件元数据中已包含正确的艺术家信息，即元数据完整是重命名的前置条件。
  - 来源：T16 | 锚点：批量重命名文件名称 / 场景2 步骤 1“确保元数据完整”
  - 原文：“首先确认您的文件元数据中已经包含了正确的艺术家信息。”
  - 状态：已核实

### 本组矛盾与不一致

- **T8、T9 页面正文为空，与 T14/T13 对其功能的描述无法互相印证**：T8“手动刮削”、T9“自动刮削”两个 V2 功能页抓取成功但只有一级标题，无正文、无图片；而 T13 名词解释与 T14 教程文章却给出了这两个功能的定义与能力清单。三处口径关系未知。
  - T8 原文：“# 手动刮削”（其后再无内容）
  - T13 原文：“本项目中的功能，选择需要修改文件或文件目录，可自动从音乐流媒体平台搜索**元数据**实行**刮削**操作”

- **T2 与 T3 对“批量”一词的用法冲突**：V1 的“批量修改”被定义为手动填写共有元数据，V2 名词解释却把“批量”能力归给自动刮削；两版术语未被统一。
  - T2 原文：“勾选多个文件或文件夹进行批量修改文件中相同的元数据（注意是手动填写）”
  - T13 原文：“自动刮削 … 选择需要修改文件或文件目录，可自动从音乐流媒体平台搜索元数据实行刮削操作”

- **“V2 包含 V1 所有功能”的说法与 V2 页面缺失不一致**：T18/T19 声称 V2 具有 V1 全部功能，但 V2 手册中不存在“切割音轨”“拆分文件名称”“简繁体转换”的独立页面，无法从文档核实这三项。
  - T18 原文：“**V2 版本具有** [**V1 版本**]()**的所有功能**”
  - V2 llms.txt 页面树中检索不到 切割音轨/拆分文件名称 对应条目（未命中）

- **简繁体转换在两版中的形态不一致**：V1 有独立页面（T5）但正文只有一张截图、无任何文字步骤；V2 未设独立页，仅把它作为后台刮削的预处理项之一。
  - T5 原文：页面仅含 “# 简繁体转换” 与一个 `<figure>` 截图，无文字
  - T10 原文：“支持声纹识别、乱码修复、繁体转简体”

- **后台刮削的“整理/转移文件”在 T10 与 T20 中的强制性表述强度不同**：T10 只把它列为并列功能项，T20 明确回答“必选”并说明理由。
  - T10 原文：“**音乐自动刮削**”
  - T20 原文：“A：是的，必须要选择，不然每次监控就不是增量数据，数据会越积累越多”

- **T4 整理文件夹的措辞存在两处笔误，引用时须保留原样**：正文写“会更加音乐的元数据”，按上下文应为“会根据”，但页面未给分组字段名，无法据此确定分组键。
  - T4 原文：“选择多级目录，会更加音乐的元数据进行整理分组文件。”

### 未取到的信息

- **T8「V2 手动刮削」与 T9「V2 自动刮削」的正文内容**：两页 `.md` 与 HTML 均只有标题，`figcaption`/`files.gitbook` 命中数为 0（HTML 中的“刮削”21 次全部来自侧边导航）。已确认不是抓取失败，而是页面无实体内容 → 业务内容 未取到。
- **标签源 / 提供方的具体名单**：两版手册全文扫描 网易、QQ音乐、酷狗、酷我、咪咕、MusicBrainz、AcoustID、Spotify、Deezer、iTunes、Last.fm 命中数为 0，只有“标签源”“音乐流媒体平台”“插件”等泛称 → 具体 provider 未取到。
- **整理文件夹的分组键到底是哪个元数据字段**：T4 只写“以元数据中的值”，未列字段名，也未给默认分组规则 → 未取到。
- **整理文件夹遇到同名文件的处理策略**（覆盖 / 自动重命名 / 跳过）：T4 全文无相关文字 → 未取到。
- **写标签时是否在原文件上原地修改、是否生成副本**：所有页面均未使用“原地/覆盖/副本/备份”类描述，只能从 T11 的“写入元数据”推出会改到文件本体 → 明确结论未取到，仅可标 [推断] 为“原地改写原文件”。
- **操作可否撤销**（V1 全部页面）：V1 无任何回退说明；只有 V2 的 T19 提到元数据版本管理支持一键回退，且未说明覆盖哪些操作、是否有时间限制 → V1 撤销能力未取到。
- **官方是否建议备份音乐文件**：11 个分配页面均无备份建议或不可逆告警，无法引用任何“请先备份”原文 → 未取到。
- **切割音轨的完整操作步骤**：T7 只讲 ffmpeg 的安装与放置，未写切割时在界面上选什么、CUE 与音频如何配对、输出目录在哪 → 未取到。
- **切割音轨对整轨原文件的处理**（保留 / 删除）：T7 未提及 → 未取到。
- **手动修改标签“保存信息”的具体落盘目标**（写文件还是写数据库）：T1 第 6 步只有一句“完成一次音乐刮削”，未说明 → 未取到。
- **简繁体转换的实际操作方式**：T5 正文无文字，只有截图 → 未取到。
- **自动批量修改的完整界面步骤**：T3 只有两张说明模式的文字，页面其余内容为截图 → 除宽松/严格模式外未取到。
- **V1 变量的完整清单**：T2 只说可悬浮查看并复制变量名，未列清单 → 未取到（V2 清单见 T12/T13，不可回填到 V1）。


---

## 常见问题、激活、升级与排错（组前缀 `F`）


## P2 素材 — 常见问题、激活、升级与排错

### 来源表
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| F1 | 常见问题（FAQ，14 组问答） | https://xiers-organization.gitbook.io/music-tag-web-v2/chang-jian-wen-ti.md | 官方文档 | 2026-09-14 |
| F2 | 激活码激活失败、无响应 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/ji-huo-ma-ji-huo-shi-bai-wu-xiang-ying.md | 官方文档 | 2026-09-14 |
| F3 | 忘记登录密码怎么办？ | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/wang-ji-deng-lu-mi-ma-zen-me-ban.md | 官方文档 | 2026-09-14 |
| F4 | 怎么更新/升级 版本呢？ | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/zen-me-geng-xin-sheng-ji-ban-ben-ne.md | 官方文档 | 2026-09-14 |
| F5 | 批量重命名文件名称 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/pi-liang-zhong-ming-ming-wen-jian-ming-cheng.md | 官方文档 | 2026-09-14 |
| F6 | 多目录独立挂载的方式 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/duo-mu-lu-du-li-gua-zai-de-fang-shi.md | 官方文档 | 2026-09-14 |
| F7 | 手动刮削能实现哪些功能？ | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/shou-dong-gua-xiao-neng-shi-xian-na-xie-gong-neng.md | 官方文档 | 2026-09-14 |
| F8 | 容器自动更新 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md | 官方文档 | 2026-09-14 |
| F9 | Mysql 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu.md | 官方文档 | 2026-09-14 |
| F10 | 外置Redis服务 | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md | 官方文档 | 2026-09-14 |
| F11 | 快速开始（V1/V2 端口与启动差异） | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md | 官方文档 | 2026-09-14 |
| F12 | Issues 列表（按评论数倒序，共 643 条） | https://api.github.com/search/issues?q=repo:xhongc/music-tag-web+is:issue&sort=comments&order=desc | 项目仓库 | 2026-09-14 |
| F13 | Issues 关键词检索（激活/登录/封面/redis） | https://api.github.com/search/issues?q=repo:xhongc/music-tag-web+is:issue | 项目仓库 | 2026-09-14 |
| F14 | 各 issue 评论区（作者回复与用户回复） | https://github.com/xhongc/music-tag-web/issues/{编号} | 项目仓库（含社区实践） | 2026-09-14 |

---

### 主张 → 来源映射

#### A. 激活码（问题 1）

- **主张**：激活码通过爱发电「发电」后私信发放；爱发电不可用时，可加作者微信（charlesnowed）购买激活码。
  - 来源：F1 | 锚点：常见问题 / Q3「怎么获得激活码呢？」
  - 原文："爱发电中<https://ifdian.net/a/music-tag-web> 发电后，会私信发你激活码。当爱发电进不去时，可添加作者微信（charlesnowed）购买激活码。"
  - 状态：已核实

- **主张**：官方页面未给出激活码的价格、发电档位或最低金额；仅有「发电」「购买」两种表述。
  - 来源：F1 | 锚点：常见问题 / Q3
  - 原文："发电后，会私信发你激活码"
  - 状态：已核实（缺失本身已核实，具体金额为 未知）

- **主张**：未激活的表现是进入后仍是 V1 界面；官方给出的动作是输入激活码完成激活。
  - 来源：F1 | 锚点：常见问题 / Q2「怎么进来还是V1啊？」
  - 原文："点击 V1 按钮输入激活码激活。"
  - 状态：已核实

- **主张**：6 次上限指同一激活码「重新激活」的次数上限，官方说明目的是限制频繁激活，可联系作者清空激活信息。
  - 来源：F1 | 锚点：常见问题 / Q10
  - 原文："重新激活有 6 次上限，为了限制频繁激活。（可联系作者清空激活信息）"
  - 状态：已核实

- **主张**：只要 `/app/data` 未删除，重新部署或换机部署会自动生效，无需重新激活；删除 `/app/data` 则需用激活码重新激活。
  - 来源：F1 | 锚点：常见问题 / Q10
  - 原文："A：/app/data 配置没删除，重新部署自动生效 ，/app/data 删除 ， 可以用激活码重新激活"
  - 状态：已核实

- **主张**：同一激活码在另一台机器激活后，上一台机器会失效下线（单点绑定）。
  - 来源：F1 | 锚点：常见问题 / Q10
  - 原文："另一台机器激活后，上一台机器就会失效下线了"
  - 状态：已核实

- **主张**：激活后无任何提示无响应，官方归因于容器内网络不通、无法访问激活服务器，建议改 host 网络模式。
  - 来源：F2 | 锚点：情况 1
  - 原文："激活时需向激活服务器发送认证验证，容器内网络不通导致无响应"
  - 状态：已核实

- **主张**：host 模式会占用 8001、8002、9001 端口，启动失败需查看端口占用情况。
  - 来源：F2 | 锚点：情况 1 解决方案
  - 原文："需要占用 8001、8002、9001 端口，启动失败查看端口占用情况"
  - 状态：已核实

- **主张**：提示「请矫正服务时间，验证超时！」的官方解法是校准服务器时间为北京时间，误差不超过 1 分钟。
  - 来源：F2 | 锚点：情况 2
  - 原文："服务器（NAS）上的时间和北京时间误差不要超过 1 分钟"
  - 状态：已核实（F1 Q13 表述一致："不要相差超过一分钟！"）

- **主张**：提示「激活码已被激活」的原因是重复多次激活超限 6 次，官方解法是找开发者重置次数。
  - 来源：F2 | 锚点：情况 3
  - 原文："重复多次激活，超限 6 次"
  - 状态：已核实

#### B. 忘记密码（问题 2）

- **主张**：官方唯一的密码找回办法是进入 Docker 容器终端执行 Django 命令改密，用户名可替换。
  - 来源：F3 | 锚点：第一步：重置管理员密码 / 第 2-3 步
  - 原文："python manage.py changepassword admin"
  - 状态：已核实

- **主张**：官方文档未提供网页端「忘记密码」自助重置入口，流程要求在容器内执行命令。
  - 来源：F3 | 锚点：全文（仅三条步骤）
  - 原文："首先，您需要进入项目的Docker容器内。"
  - 状态：已核实（缺失本身已核实）

#### C. 升级（问题 3）

- **主张**：官方给出 3 种升级方式：docker pull 后重建容器、docker-compose pull + up -d、watchtower 一次性更新。
  - 来源：F4 | 锚点：全文标题 1/2/3
  - 原文："提供3种方式进行更新"
  - 状态：已核实

- **主张**：docker pull 方式需先停止并删除旧容器，再用新镜像按快速开始命令重新部署。
  - 来源：F4 | 锚点：1. docker pull 方式 / 步骤二
  - 原文："docker stop my-music-tag-web" / "docker rm my-music-tag-web"
  - 状态：已核实

- **主张**：官方明确警告 `docker-compose down -v` 会连同卷一起删除，并提醒确认数据已挂载到持久化存储以防丢失。
  - 来源：F4 | 锚点：2. 使用 Docker Compose 更新
  - 原文："若要连同卷一起删除，请添加 -v 选项" 及 "确保所有重要数据都已正确挂载到持久化存储上，防止数据丢失。"
  - 状态：已核实

- **主张**：Web 端内置自动更新的前提是首次部署时挂载 `/var/run/docker.sock`，否则会报 Docker 客户端初始化失败。
  - 来源：F8 | 锚点：0. 重要：挂载 Docker Socket / 「没有挂载会怎样？」
  - 原文："Docker客户端初始化失败" / "无法连接到 Docker daemon" / "更新按钮点击后没有反应"
  - 状态：已核实

- **主张**：自动更新官方声明会保留所有数据和配置，并要求首次安装即正确配置数据卷，更新后数据不丢失。
  - 来源：F8 | 锚点：什么是自动更新？列表 / 2. 确保数据持久化
  - 原文："保留你的所有数据和配置" / "这样更新后你的数据不会丢失"
  - 状态：已核实

- **主张**：官方升级文档使用 `xhongc/music_tag_web:2.0.1` 作为版本号示例，示例版本不代表最新版本。
  - 来源：F4 | 锚点：步骤一：拉取新版本镜像
  - 原文："假设我们想要更新到版本 2.0.1，那么命令如下：docker pull xhong/music_tag_web:2.0.1"
  - 状态：已核实（注意原文镜像名为 `xhong/music_tag_web`，与 F11 的 `xhongc/music_tag_web` 不一致，见矛盾节）

- **主张**：V1 升级到 V2 的官方要求是：容器内端口为 8002，并去掉 `command /start` 启动命令。
  - 来源：F1 | 锚点：常见问题 / Q12
  - 原文："需要确保你部署时后容器内端口是 8002，和去掉了 command /start 命令"
  - 状态：已核实（F11 表述一致）

#### D. FAQ 问答对（问题 4，逐条独立）

- **主张**：FAQ 第 1 条——专辑封面/艺术家图裂开且音乐无法播放时，官方建议修改文件夹权限为 Everyone，并确认访问的是 8002 端口。
  - 来源：F1 | 锚点：常见问题 / 第 1 条
  - 原文："修改文件夹权限，设置为Everyone。" / "ps. 确定配置访问的是 8002 端口"
  - 状态：已核实

- **主张**：FAQ 第 4 条——输入激活码没有反应时，官方建议确保容器能访问外部网络与激活服务器，可改网络模式为 host。
  - 来源：F1 | 锚点：常见问题 / 第 4 条
  - 原文："确保容器里能访问到外部的网络，能访问到激活服务器，可以修改网络模式为 host试试。"
  - 状态：已核实

- **主张**：FAQ 第 5 条——首页歌曲数为 0 时，需在操作台勾选歌曲目录并执行「导入收藏」，等待后台导入。
  - 来源：F1 | 锚点：常见问题 / 第 5 条
  - 原文："在操作台中勾选想要导入的歌曲目录-导入收藏，等待后台导入即可。"
  - 状态：已核实

- **主张**：FAQ 第 6 条——音乐收藏一直 loading，官方归因于 subsonic 密码未设置或已更改，需设置后重新登录再刷新页面。
  - 来源：F1 | 锚点：常见问题 / 第 6 条
  - 原文："更改过或未设置subsonic 的密码需要设置一次，需要重新再登录一次，后再刷新音乐收藏页面。"
  - 状态：已核实

- **主张**：FAQ 第 7 条——后台刮削不生效或删除收藏不生效时，官方建议在「其他设置」中停止所有后台任务后等待重新执行。
  - 来源：F1 | 锚点：常见问题 / 第 7 条
  - 原文："其他设置-停止所有后台任务，等待重新执行。"
  - 状态：已核实

- **主张**：FAQ 第 8 条——搜索刮削提示「暂无歌曲信息」时，官方建议确认容器可访问网络，可改 host 网络模式。
  - 来源：F1 | 锚点：常见问题 / 第 8 条
  - 原文："确认容器内可以访问网络，可以修改网络模式为 host试试。"
  - 状态：已核实

- **主张**：FAQ 第 9 条——`/admin` 报 403 无法访问，官方归因于框架安全机制限制反代地址，局域网地址可进入。
  - 来源：F1 | 锚点：常见问题 / 第 9 条
  - 原文："受限制框架安全机制，反代的地址无法进入，局域网地址可以。"
  - 状态：已核实

- **主张**：FAQ 第 11 条——后台刮削的「转移文件/整理文件」为必选项，官方理由是保证监控目录是增量数据，避免数据越积越多。
  - 来源：F1 | 锚点：常见问题 / 第 11 条
  - 原文："是的，必须要选择，不然每次监控就不是增量数据，数据会越积累越多"
  - 状态：已核实

- **主张**：FAQ 第 13 条——激活失败、验证超时的官方解法是把容器内时间校正为北京时间，误差不超过一分钟。
  - 来源：F1 | 锚点：常见问题 / 第 13 条
  - 原文："容器内的时间校正为北京时间，不要相差超过一分钟！"
  - 状态：已核实

- **主张**：FAQ 第 14 条——出现 Database is locked 时，官方归因于 Sqlite 并发读写的独占锁机制，建议切换到 mysql 数据库。
  - 来源：F1 | 锚点：常见问题 / 第 14 条
  - 原文："Sqlite 数据库并发读写**独占锁**机制，会锁定整个数据库，可以切换到 mysql 数据库有更好体验。"
  - 状态：已核实

- **主张**：FAQ 第 10 条同时覆盖跨机部署与 6 次重新激活上限，是激活相关最完整的一条官方说明。
  - 来源：F1 | 锚点：常见问题 / 第 10 条（整条）
  - 原文："购买激活码后，我重新部署容器或在另一台机器部署是否可以呢？"
  - 状态：已核实

- **主张**：FAQ 第 2、3、12 条共同构成「激活 → 获取激活码 → V1 升 V2」的最小链路，均为一句话式回答，无展开步骤。
  - 来源：F1 | 锚点：常见问题 / 第 2、3、12 条
  - 原文："点击 V1 按钮输入激活码激活。"
  - 状态：[推断]（「最小链路」为归纳，非原文表述）

- **主张**：MySQL 方案在官方文档中的定位就是解决 sqlite database is locked，需通过环境变量 MYSQL_HOST/PASSWORD/DB_NAME/USER/PORT 接入。
  - 来源：F9 | 锚点：页面导语 + docker-compose 环境变量段
  - 原文："本项目默认采用Sqlite数据库，sqlite 在并发写入时容易出现sqlite database is locked"
  - 状态：已核实

- **主张**：外置 Redis 不是必需项，容器自身会启动一个 redis；如使用外置需配置 REDIS_HOST、REDIS_PORT（默认 6379）、REDIS_PASSWORD。
  - 来源：F10 | 锚点：页面导语 + 方法一
  - 原文："容器本身就会启动一个 redis，如果你不需要**外置**的 redis，可以不进行此项的配置。"
  - 状态：已核实

- **主张**：手动刮削支持批量重命名文件名、补全艺术家/专辑元数据、导出与嵌入 lrc 歌词、导出与导入专辑封面。
  - 来源：F7 | 锚点：功能列表（共 6 项）
  - 原文："下面功能均支持批量操作。"
  - 状态：已核实

- **主张**：批量去除文件名音轨号可用正则 `(?P<tracknumber>\d+)\.(?P<filename>\w+)` 只保留标题作为文件名。
  - 来源：F5 | 锚点：场景1 / 第二个正则
  - 原文："我们只需要改变正则表达式，就能实现去掉音轨号，只保留《夜曲》 作为文件名。"
  - 状态：已核实

- **主张**：按「艺术家-音乐名」重命名用变量 `${artist}-${title}`，扩展名自动沿用源文件，无需手写。
  - 来源：F5 | 锚点：场景2 / 变量使用示例
  - 原文："文件扩展名会继续填充源文件的扩展名，所以你无需额外输入文件扩展名。"
  - 状态：已核实

- **主张**：多目录独立挂载靠 volumes 多行映射实现，示例为本地目录映射到 `/app/media/Pop` 等分类子目录。
  - 来源：F6 | 锚点：2. 修改 docker-compose.yml
  - 原文："- /path/to/your/pop_music:/app/media/Pop"
  - 状态：已核实

- **主张**：多目录挂载的两条官方注意事项为：路径错误会导致容器读不到音乐文件；新增或移除音乐库后必须重启容器才生效。
  - 来源：F6 | 锚点：注意事项 1、2
  - 原文："新增或移除音乐库后，需要重启容器才能生效"
  - 状态：已核实

- **主张**：F6 正文存在自相矛盾：配置步骤把容器路径写成 `/app/media/Pop`，而「容器内访问」一节却写成 `/music/Pop`。
  - 来源：F6 | 锚点：2. 修改 docker-compose.yml vs 容器内访问
  - 原文："- /path/to/your/pop_music:/app/media/Pop" 与 "`/music/Pop`：对应本地流行音乐库"
  - 状态：已核实（原文两组路径并存）

#### E. Issues 中的高频故障类别与处置（问题 5）

- **主张**：登录失败/鉴权「身份认证信息未提供」是最高频故障簇：`#81`（38 评论，默认密码进不去）、`#360`（20）、`#351`（13）等。
  - 来源：F12、F13 | 锚点：issue #81 / #360 / #351
  - 原文："輸入用戶名和密碼後…顯示兩個右上角alert：標題：查询失败！ 內容：身份认证信息未提供。"
  - 状态：已核实（官方回复见下条）

- **主张**：作者（xhongc）对登录失败给出的官方排查清单为四条：日志是否有进程一直重启、redis 连接是否正常、内存是否足够、host 模式是否端口冲突。
  - 来源：F14 | 锚点：#360 作者回复
  - 原文："无法登录问题排查： 1. 查看日志是否有进程在一直重启启动 2. 检查 redis 配置连接是否正常 3. 检查内存分配是否足够"
  - 状态：已核实（属官方回复）

- **主张**：作者在同一 issue 中追加过两种与上面清单不同的建议：删除 `/app/data` 下数据库重启，以及更换或升级浏览器。
  - 来源：F14 | 锚点：#360 作者后续回复
  - 原文："把/app/data 中的 db 数据库删掉，在重启一下试试呢" / "尝试换浏览器登录"
  - 状态：已核实（属官方回复，但口径前后不一致）

- **主张**：用户侧反馈与官方清单冲突：有用户报告 host 网络登录失败而 bridge 正常，作者回应可能是端口冲突。
  - 来源：F14 | 锚点：#360 用户 swatx2 评论
  - 原文："我用host网络也是一样，默认账号密码无法登陆，换成bridge网络没问题"
  - 状态：已核实（属用户猜测/用户实测，非官方结论）

- **主张**：升级后容器反复重启、CPU 占用飙升是第二高频簇（`#377`，23 评论），作者先让回退 2.3.8，后宣布修复。
  - 来源：F14 | 锚点：#377 作者回复
  - 原文："不是，先用 2.3.8 版本，我在看看" → "已经修复了，重新拉一下新版本吧" → "2.4.2 修复了"
  - 状态：已核实（属官方回复）

- **主张**：`#377` 中多数用户属同类复现（looperww、taxuew、LEO8210、horseytr、xiaopanjiaoshou 等），提示该回归跨 amd64/arm 平台。
  - 来源：F14 | 锚点：#377 用户评论
  - 原文："一样的问题，更新完就gg了，CPU占用率飙升而且打不开"
  - 状态：已核实（用户报告；「跨平台」为 [推断]）

- **主张**：升级后专辑与艺术家封面 404（`#546`，23 评论），作者先排查 attachment 目录，最终建议重新导入收藏。
  - 来源：F14 | 锚点：#546 作者回复
  - 原文："检查是否删除 attaments 目录" → "这个啊，算了，你重新导入收藏"
  - 状态：已核实（属官方回复，未给出根因）

- **主张**：`#546` 的故障现象是 `/rest/getCoverArt/` 接口返回 404，而映射目录内图片文件确实存在。
  - 来源：F14 | 锚点：#546 用户 bjzhili 评论
  - 原文："状态代码 404 Not Found 远程地址 10.10.9.19:8002"
  - 状态：已核实（用户自测数据）

- **主张**：V2 部署后服务报错且资源占用高（`#198`，16 评论），作者称 V2 需要 600 多 MB 内存，但真正根因由用户自行定位为未挂载 `/app/data`。
  - 来源：F14 | 锚点：#198 作者与用户 zoverdoser 评论
  - 原文："更多的内存试试，v2 要占用 600 多" / "app/data 没有挂载" / "挂载上app/data 之后可以正常启动了"
  - 状态：已核实（前半为官方回复，根因为用户自解）

- **主张**：内网 Redis 连接不上（`#397`，15 评论）属独立故障簇，用户表示容器内可 telnet 通 redis 但后台日志持续报错。
  - 来源：F12、F13 | 锚点：issue #397
  - 原文："配置好redis但无法连接上，后台日志一直报错，在容器中能telnet通对应的redis服务"
  - 状态：待核实（评论区未取到，见未取到节）

- **主张**：文件名乱码导致无法打开与重命名报错（`#33`，28 评论），作者判定为文件名编码问题，用户最终用 convmv 由 GB2312 转 UTF-8 解决。
  - 来源：F14 | 锚点：#33 用户 pubg-Eddie 结帖评论
  - 原文："windows文件名称编码默认是GB2312，linux默认是UTF-8，通过convmv即可进行修改。"
  - 状态：已核实（作者前期回复为「文件名称编码问题」，最终解法为用户自解）

- **主张**：`#33` 中作者多次提出「修改文件名后要刷新一下」「勾选是批量操作，单个文件要点名称进编辑页」，属于操作方式误解而非缺陷。
  - 来源：F14 | 锚点：#33 作者回复
  - 原文："勾选的时候是 批量操作 ，你要操作单个文件的话 点选名称就可以进去 编辑页面修改"
  - 状态：已核实（属官方回复）

- **主张**：Web 页勾选歌曲时自动连带勾选大量歌曲（`#479`，25 评论，镜像 2.5.8 / V2），属列表选择器缺陷类问题。
  - 来源：F12 | 锚点：issue #479
  - 原文："勾选第一首歌《unity-the fat rat》下方许多歌曲也被自动勾选了"
  - 状态：待核实（评论区未取到）

- **主张**：专辑封面修改后在第三方音乐软件不生效（`#257`，22 评论）与手动上传封面在 Navidrome 不显示（`#145`，10 评论）构成封面写入簇。
  - 来源：F13 | 锚点：issue #257 / #145
  - 原文："专辑封面修改后在音乐软件上未发生变化"
  - 状态：待核实（评论区未取到）

- **主张**：Subsonic API 覆盖不全导致第三方客户端异常（`#510`，18 评论），用户点名缺少 getIndexes、getStarred、getLyricsBySongId。
  - 来源：F12 | 锚点：issue #510
  - 原文："目前发现不支持getIndexes、getStarred、getLyricsBySongId。"
  - 状态：待核实（评论区未取到）

- **主张**：音乐收藏播放报「不支持播放格式或者音乐文件不存在」（`#559`，15 评论，镜像 2.6.6 / V2），用户已排除格式因素。
  - 来源：F12 | 锚点：issue #559
  - 原文："刚开始以为是格式不对，后来专门找了MP3格式的也还是不行"
  - 状态：待核实（评论区未取到）

- **主张**：V2 导入收藏在 NFS 后端报 Operation not permitted（`#637`，11 评论，镜像 2.7.4），用户判断卡在改 ownership 步骤。
  - 来源：F13 | 锚点：issue #637
  - 原文："保存到数据库失败: [Errno 1] Operation not permitted: '/app/media/attachments/f0/76/75/小城谣.webp'"
  - 状态：待核实（评论区未取到）

- **主张**：FLAC 元数据异常导致「加载文件失败」（`#263`，13 评论）与浮点参数转换失败（`#551`，8 评论）构成 FLAC 元数据兼容簇。
  - 来源：F12、F13 | 锚点：issue #263 / #551
  - 原文："加载文件失败, 请检查文件的元数据是否损坏"
  - 状态：待核实（评论区未取到）

- **主张**：刮削匹配不准（宽松模式）与指定专辑名仍匹配到别的作品（`#40`、`#339`、`#415`）构成刮削准确性簇，多为功能请求而非缺陷。
  - 来源：F12、F13 | 锚点：issue #40 / #339 / #415
  - 原文："在刮削的时候指定了 专辑名称 还是会刮削到别的"
  - 状态：待核实（评论区未取到）

- **主张**：`#34`（24 评论）同时包含 ID3v1 中文乱码与多艺术家支持两项诉求，与 `#30` 的 MP3 专辑类型无法保存同属标签写入兼容簇。
  - 来源：F12 | 锚点：issue #34 / #30
  - 原文："修改后id3v1的汉字全部为乱码。2.很多歌曲是多艺术家的，建议增加多艺术家支持。"
  - 状态：待核实（评论区未取到）

- **主张**：激活相关 issue 的数量（检索「激活」命中 14 条）明显少于登录与封面类，且多为「已被激活」这一类的次数超限问题。
  - 来源：F13 | 锚点：检索「激活」结果；issue #191 / #597 / #639
  - 原文："V1输入激活码显示错误，已被激活" / "激活码激活失败，提示已被激活"
  - 状态：已核实（检索计数为 API 返回结果）

- **主张**：用户曾请求把激活码写入环境变量或数据库以简化激活（`#631`），官方是否采纳未知。
  - 来源：F13 | 锚点：issue #631
  - 原文："v2版本能不能将激活码写入到环境环境变量或者数据库中呢？"
  - 状态：待核实（评论区未取到）

---

### 本组矛盾与不一致

- **host 网络模式：官方推荐 vs 用户实测相反。** F1 Q4/Q8 与 F2 情况 1 均建议改 host 模式解决激活与刮削的网络问题；但 F14 `#360` 中用户 swatx2 称 "我用host网络也是一样，默认账号密码无法登陆，换成bridge网络没问题"，作者仅回应 "可能有端口冲突"，未撤回 host 建议。F2 自身也承认 host 会占用 8001、8002、9001 三个端口。→ 两套网络建议并存，未收敛。

- **登录失败根因：同一 issue 内作者给出三套不同口径。** F14 `#360` 中作者先给四条排查清单（进程重启 / redis / 内存 / 端口冲突），随后改为 "把/app/data 中的 db 数据库删掉，在重启一下试试呢"，最后又建议 "尝试换浏览器登录" / "或者更新谷歌浏览器版本"。用户 Nitsuya 反馈删库重启后 "WebUI登录依旧是这错误"，问题未见闭环。

- **升级后封面丢失的处置结论不一致。** F8 官方声明自动更新 "保留你的所有数据和配置"；F14 `#546` 中用户删旧镜像拉新镜像后封面全部 404，作者未定位根因，结论是 "你重新导入收藏"。声明与实测结果之间存在缺口。

- **镜像仓库名不一致。** F4 升级示例写 `docker pull xhong/music_tag_web:2.0.1`，F11 快速开始写 `xhongc/music_tag_web:latest`，F9/F10 也用 `xhongc/...`。同一官方站内两种命名并存，未说明是否为旧名或笔误。

- **F6 挂载路径自相矛盾。** 配置段写容器内为 `/app/media/Pop`，同页「容器内访问」段却写 `/music/Pop`，同页两组路径互斥。

- **V2 版本号在 issue 中跨度大且无官方映射表。** F14 出现 2.3.8（回退版）、2.4.2（作者称修复回归）、2.5.8、2.6.6、2.7.4 等多个版本；F4 示例停在 2.0.1。官方站内没有版本变更记录页，无法交叉验证哪个版本引入了哪次故障。

- **默认密码问题在 FAQ 中无对应条目。** `#81`（38 评论，全仓最高）为 "后台管理用默认密码进不去"，但 F1 FAQ 14 条中没有「默认账号密码是多少/进不去怎么办」的问答；F3 只覆盖忘记密码后的命令行改密。

---

### 未取到的信息

- **激活码价格与发电档位**：F1 Q3 只有「发电」「购买」字样，未给金额、档位或最低门槛；三处官方页面均无价格。→ 未知。
- **重置 6 次激活上限的成本与耗时**：F1 Q10 与 F2 情况 3 只说「可联系作者清空激活信息」「找开发者进行重置次数」，未说明是否收费、需要什么凭证、多久处理。→ 未取到。
- **激活码与账号/机器的绑定粒度**：F1 Q10 说另一台机器激活后上一台失效，但未说明是绑定硬件、IP 还是仅绑定最后一次激活记录。→ 未取到。
- **官方版本变更记录 / 变更日志**：GitBook 站点树（llms.txt）中无 changelog 或 release notes 页面，无法核对各故障所对应的修复版本。→ 未取到。
- **Docker Hub 镜像 tag 列表**：`hub.docker.com` 在本机不可达（超时），F11 指向的 tags 页面内容无法抓取。→ 未取到。
- **`#81`（38 评论）评论区内容**：GitHub REST API 触发未认证速率限制（core 剩余 0，约 44 分钟后重置），且 issue 页 HTML 不再服务端渲染评论。仅取到标题与正文。→ 未取到。
- **`#397`（redis）、`#24`（映射目录不显示文件）、`#637`（NFS 导入报错）评论区内容**：同因速率限制未取到，故这几条只到标题/正文层级，未标注解决状态。→ 未取到。
- **`#479`、`#510`、`#559`、`#257`、`#145`、`#263`、`#551`、`#40`、`#339`、`#415`、`#34`、`#30`、`#631` 的评论区与解决状态**：仅取到标题与正文，无法区分官方回复与用户猜测。→ 未取到。
- **官方对「Database is locked」以外的数据库故障处置**：F9 只说明切换到 MySQL 的方案，未给出已 lock 状态下的应急恢复步骤。→ 未取到。
- **忘记密码是否影响 Subsonic 用户密码**：F3 只覆盖管理员登录密码，FAQ Q6 提到 subsonic 密码需另行设置，两者关系未说明。→ 未取到。


---

## 播放侧功能与生态集成（组前缀 `P`）


## P2 素材 — 播放侧功能与生态集成

### 来源表
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| P1 | 音乐收藏与播放 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/yin-yue-shou-cang-yu-bo-fang.md | 官方 | 2026-09-14 |
| P2 | 小爱音箱 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/xiao-ai-yin-xiang.md | 官方 | 2026-09-14 |
| P3 | 网盘音乐 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/wang-pan-yin-yue.md | 官方 | 2026-09-14 |
| P4 | 智能歌单 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/zhi-neng-ge-dan.md | 官方 | 2026-09-14 |
| P5 | 音乐去重 | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/yin-yue-qu-zhong.md | 官方 | 2026-09-14 |
| P6 | Subsonic客户端 | https://xiers-organization.gitbook.io/music-tag-web-v2/subsonic-ke-hu-duan.md | 官方 | 2026-09-14 |
| P7 | 刮削艺术家并被 navidrome 识别 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/gua-xiao-yi-shu-jia-bing-bei-navidrome-shi-bie.md | 官方 | 2026-09-14 |
| P8 | 飞牛私有云论坛帖 4152：music-tag 刮削过后 navidrome有些还是识别不出来 | https://club.fnnas.com/forum.php?mod=viewthread&tid=4152 | 社区实践 | 2026-09-14 |
| P9 | 博客园：Docker部署Navidrome+MusicTagWeb搭建私人音乐库 | https://www.cnblogs.com/ivoink/articles/22696323 | 社区实践 | 2026-09-14 |
| P10 | Music Tag Web V2 llms.txt（页面索引） | https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt | 官方 | 2026-09-14 |
| P11 | Music Tag Web（V1）llms.txt（页面索引） | https://xiers-organization.gitbook.io/music-tag-web/llms.txt | 官方 | 2026-09-14 |

### 主张 → 来源映射

- **主张**：Q1 项目自带 Subsonic 兼容服务端，无需另装服务端；登录 host 为「站点 ip:8002」，凭据在后台管理的 subsonic 用户中查看与修改。
  - 来源：P1 | 锚点：页首正文 + 第 4、5 条
  - 原文："Open Subsonic 协议的播放服务器。登录的 host 是站点 ip:8002, 账号密码在后台管理里subsonic 用户中查看并修改。"
  - 状态：已核实

- **主张**：Subsonic 密码的存储与修改位置：admin/后台的 subsonic 用户中，「修改 api token 即是密码」，改后需重新登录并刷新页面。
  - 来源：P1 | 锚点：第 5 条「subsonic 修改密码」
  - 原文："admin/后台中 subsonic 用户中，修改 api token 即是密码。"
  - 状态：已核实

- **主张**：官方声明「支持所有 subsonic 的客户端」，并在 P6 给出跨平台/Android/iOS/Web/桌面五类客户端清单；P6 明确不需要其他服务端。
  - 来源：P1、P6 | 锚点：P1 第 4 条与其客户端列表；P6 页首与全页清单
  - 原文：P6 "Music Tag Web 提供音乐服务器，就不需要其他的服务端了，可以直接用下列中的客户端连接听歌了"
  - 状态：已核实

- **主张**：音乐收藏需先导入：在操作台勾选目录后「导入收藏」，等待导入完成才会在音乐收藏中展示；文件侧删除后可用「其他设置-删除不存在收藏」同步清理。
  - 来源：P1 | 锚点：第 1、6 条
  - 原文："在操作台中，勾选想要导入的目录，导入收藏，等待导入后可在音乐收藏中展示。"
  - 状态：已核实

- **主张**：Q3 小爱音箱前置条件是小米账号（须填「小米 ID，非手机号码」）、设备型号/名称、关键字、本机内网地址与端口（用部署命令的端口），并需测试连接。
  - 来源：P2 | 锚点：第 1、3、4 条
  - 原文："小米账号：为小米 ID ，非手机号码" / "内网地址是本项目的内网地址，端口是部署命令的端口。"
  - 状态：已核实

- **主张**：小爱音箱官方测试通过型号为 LX06、L16A、LX5A、L17A、S12；L05B 只能播放 mp3 格式。
  - 来源：P2 | 锚点：型号段落
  - 原文："测试通过的型号 LX06，L16A，LX5A ，L17A，S12。" / "只能播放mp3 格式的型号：L05B"
  - 状态：已核实

- **主张**：Q3 网盘音乐「直连模式」前置条件是 alist：填 Alist Url、根目录地址、alist 用户名与密码；根目录映射到本项目的 /app/webdav。
  - 来源：P3 | 锚点：## 直连模式 及其设置项
  - 原文："直接连接 alist api，对网盘音乐进行刮削和入库。"
  - 状态：已核实

- **主张**：直连模式下刮削【不会】修改网盘音乐文件的元数据；本地挂载模式则需额外映射卷、并在基本设置中把 webdav 写入位置勾选数据库后再导入收藏。
  - 来源：P3 | 锚点：直连模式引用块 + ## 本地挂载 第 1–4 步
  - 原文："注意：刮削操作不会修改网盘音乐文件的元数据。"
  - 状态：已核实

- **主张**：Q3 智能歌单功能位于「音乐收藏-智能歌单」，作用是「根据满足条件快速从音乐库中创建歌单列表」，即其前置条件只是音乐库/收藏中已有内容，无需账号或插件。
  - 来源：P4 | 锚点：页首与正文
  - 原文："根据满足条件快速从音乐库中创建歌单列表"
  - 状态：已核实（页内未列出可用条件字段，见「未取到」）

- **主张**：Q3 音乐去重入口为「操作台-勾选目录-重复文件检查」，不会自动删除文件，结果需自行到操作记录中查看并手动删除。无需账号或插件。
  - 来源：P5 | 锚点：页首说明 + 第 1、3 步
  - 原文："查找出重复的文件 不会自动删除您的文件，可以到操作记录中查看重复文件进一步删除操作。"
  - 状态：已核实

- **主张**：Q2 Navidrome 集成页的前提是音乐已导入音乐收藏；操作为「系统设置-其他设置-刮削艺术家」，完成后可在操作记录查看刮削详情。
  - 来源：P7 | 锚点：**前提条件：** 与第 1 步「设置艺术家封面抓取」
  - 原文："前提条件： 确保您的音乐已导入到音乐收藏中。"
  - 状态：已核实

- **主张**：Q2 该页称在 `/app/media/music/王以太/演.说.家/人间天堂.flac` 这类结构下，系统会在 `/王以太/` 目录自动生成 `artist.jpg`，且"NaviDrome 自动识别"该文件用于艺术家页展示。
  - 来源：P7 | 锚点：第 2 步「艺术家页面展示封面」与第 3 步「封面文件识别」
  - 原文："`artist.jpg` 文件将被 NaviDrome 自动识别并用于艺术家页面的展示。"
  - 状态：已核实

- **主张**：该页要求目录结构必须是 `/艺术家/ /专辑/ 音乐文件`，「以保证 NaviDrome 能够准确地识别和展示艺术家及其作品的信息」。
  - 来源：P7 | 锚点：**总结：**
  - 原文："为了确保艺术家封面能被正确显示，请务必按照以下目录结构组织您的音乐文件"
  - 状态：已核实

- **社区实践（P8）**：Navidrome 专辑封面取自歌曲文件夹内的 `cover.jpg`；在 Music Tag Web 中须把「导出图片」开关打开，保存音乐信息时才会生成该 cover.jpg。
  - 来源：P8 | 锚点：2024-12-14 evo2004 回复楼层
  - 原文："我发现navidrome显示的专辑封面是取得歌曲文件夹里面的cover.jpg，用music-tag刮削后，要把“导出图片”这个设置为开，保存音乐信息就会自动生成一张cover.jpg。"
  - 状态：已核实（仅代表该帖用户经验，非官方）

- **社区实践（P8）**：有用户转述 Navidrome 的取图优先级配置默认值，用以解释识别顺序，属社区转述而非 Music Tag Web 官方文档。
  - 来源：P8 | 锚点：2025-3-28 飘过记忆的 楼层
  - 原文："默认值为 ，表示：CoverArtPrioritycover.*, folder.*, front.*, embedded, external"
  - 状态：已核实（仅代表该帖用户转述，非官方）

- **社区实践（P8）**：另有用户给出图片体积与分辨率经验值，称图片过大或分辨率过高时 Navidrome 有时不识别。
  - 来源：P8 | 锚点：2025-3-28 19:40 飘过记忆的 楼层
  - 原文："有情提示 图片别大于80K 不信你可以试一下" / "补充下 分辨 800-550 左右合适 高了有时候不识别"
  - 状态：待核实（社区经验值，官方文档未给出此类限制）

- **社区实践（P9）**：该文给出 Navidrome + Music Tag Web 同 compose 部署样例：两容器挂载同一音乐目录，MTW 映射 `8002:8002`、音乐挂 `/app/media`、数据挂 `/app/data`，镜像 `xhongc/music_tag_web:latest`。
  - 来源：P9 | 锚点：正文 compose 文件
  - 原文："- \"8002:8002\" # 前端访问端口，可自行修改" / "- /vol1/1001/06_Music:/app/media # 挂载和Navidrome相同的音乐目录，直接编辑标签"
  - 状态：已核实（社区实践；端口与官方 8002 一致）

- **社区实践（P9）**：作者把 MTW 设为 `unless-stopped` 以便「等需要添加歌曲再手动打开容器」，作为老旧低性能 NAS 上的省资源做法。
  - 来源：P9 | 锚点：「这样部署为什么会适合老旧设备？」
  - 原文："在MusicTagWeb上面，启动模式是 unless-stopped ，也就是可以随时手动停止"
  - 状态：已核实（社区实践，属作者个人取舍）

- **主张**：Q5 本组涉及的播放/生态功能（音乐收藏与播放/Subsonic 服务端、Subsonic 客户端、小爱音箱、网盘音乐、智能歌单、音乐去重）在 V1 手册页面索引中没有任何对应页面。
  - 来源：P10 对比 P11 | 锚点：P11 全部 10 条页面（项目介绍、快速开始、手动修改标签、批量修改、自动批量修改、整理文件夹、简繁体转换、拆分文件名称、切割音轨、V2 版本）
  - 原文：P11 索引中无上述任一主题条目；P11「V2 版本」条目描述为"是集合音乐标签刮削和音乐播放一体的个人音乐库解决方案。"
  - 状态：[推断]（判定方法＝逐个比对两份 llms.txt 页面索引；索引缺页仅能证明 V1 手册未收录，不等于 V1 代码无此能力）

### 本组矛盾与不一致

- **官方成功口径 vs 社区故障反馈（P7 vs P8）**：P7 把艺术家封面被 Navidrome 识别描述为可复现的实验结论；P8 帖标题与楼主称"部分有些还是识别不出来"，手动与自动刮削都试过。两者不直接互斥（P7 讲 artist.jpg，P8 讲 cover.jpg），但并列时需说明是两类不同封面文件。
  - P7 原文："本实验演示在music tag web 中批量刮削艺术家封面，并成功被 navidrome 识别到"
  - P8 原文："music-tag 刮削过后 navidrome 部分有些还是识别不出来 手动和自动刮削都试过了"
- **客户端清单不一致（P1 vs P6）**：同一官方文档内，"跨平台"一行列出的客户端不同——P1 只列「音流」，P6 列出「箭头音乐、音流」。
  - P1 原文："跨平**台：**音流"
  - P6 原文："跨平**台：箭头音乐、**音流"
- **同一页内路径拼写不一致（P3 内部）**：正文明写挂载到 `/app/weddav`（多一个 d），而同一页的映射示例写 `/app/webdav`。属文档笔误，需按 `/app/webdav` 理解。
  - P3 原文（正文）："将网盘挂载本地/app/weddav 目录"；P3 原文（映射）："/path/to/your/webdavmusic:/app/webdav:rw"

### 未取到的信息

- 官方来源未给出 Navidrome 的默认监听端口（P9 社区 compose 使用 `4533:4533`，但 P1–P7 均未提及该端口，故不作为官方事实）。
- Subsonic 用户的默认用户名与默认密码具体值：官方仅说明"在后台管理里subsonic 用户中查看并修改"，未给出默认值。
- Music Tag Web V2 的具体版本号或发布日期：本次抓取的 P1–P7、P10 页面均未出现版本号。仅 P11 索引中另有 V1 侧"绿联部署""飞牛云fnos部署（fnos版本：0.8.24）"等条目提到 fnos 版本，与本组主题无关。
- 智能歌单"满足条件"具体支持哪些字段/操作符：P4 全页仅有标题与一句说明，未列出条件清单（V2 另有 `jiao-cheng-wen-zhang/zhi-neng-ge-dan-de-jin-jie-wan-fa.md` 页面不在本组分配范围，未抓取）。
- 网盘音乐支持哪些具体网盘：P3 只说明经 alist 接入，未列举网盘类型清单。
- 小爱音箱在测试通过型号之外机型的行为：官方仅提示"可能是该型号的音箱不支持这个功能"，未给出完整兼容列表。
- 官方对封面图片体积/分辨率是否有限制：P1–P7 未提及；仅 P8 社区用户给出 80K 与 800x550 经验值。


---

## 飞牛 fnOS 部署（截图读取）（组前缀 `O`）


## P2 素材 — 飞牛 fnOS 部署（截图恢复）

### 页面文字（可直接读取的部分）
| S-ID | 标题 | URL | 层级 | 抓取日期 |
| --- | --- | --- | --- | --- |
| O1 | 飞牛云fnos部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md | 官方文档 | 2026-09-14 |

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

### 截图清单
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

### 截图恢复出的步骤与字段

#### 路线一：容器部署（截图 fnos-01 → fnos-07）

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

#### 路线二：Compose 部署（截图 fnos-08 → fnos-11）

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

#### 对六条待确认报告的回答

1. **要在 Docker 界面搜索的镜像** = `xhongc/music_tag_web`（下划线）。页面文字与 fnos-01.png 一致；**不是**应用商店（fnOS「应用商店」在本页完全没有出现，全程走的是 Docker 应用）。— 已确认
2. **容器端口** = `8002`。在 fnos-05.png（端口设置）与 fnos-06.png（确认信息）各出现一次，本地端口同为 8002。— 已确认，与页面文字 `访问8002端口` 互相印证
3. **卷映射** = `/vol1/1000/music → /app/media`（读写）与 `/vol1/1000/mtw_config → /app/data`（读写）。两条路线都一致，Compose YAML 亦同。— 已确认
4. **环境变量 / 网络模式** = **未取到**。fnos-01 至 fnos-11 全部截图中没有出现任何环境变量输入区，也没有网络模式（bridge/host/macvlan）选择项；「高级设置」页只截了端口设置与存储位置两个分区。— 未取到
5. **V2 激活步骤是否在本页** = 仅以**页面正文文字**出现一句 `左上角V1标签点击激活V2版本`；**没有任何截图展示该 V1 标签或激活对话框**。无法从截图确认激活入口的准确位置与外观。— 文字有，截图未取到
6. **fnOS 版本** = `0.8.24`（页面正文文字 `fnos版本：0.8.24`）。截图内不含版本号。— 已确认（文字来源）

### 页面确实没有提供的信息

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

### 本组发现的内部不一致（供 P4/P5 注意）

- **容器部署路线的卷数量自相矛盾**：`高级设置`（fnos-05.png）配置了 **2 条**映射（music→media、mtw_config→data），但紧接着的 `确认信息`（fnos-06.png）汇总表里**只剩 1 条**（music→media）。这是截图本身的差异，不是读取误差；对比之下 Compose 路线（fnos-11.png）明确带 2 条卷。**若照容器路线走，务必确认 `/app/data` 是否真的挂上了**，因为 V2 的配置/数据库落在 `/app/data`。
- **两条路线产生不同容器名**：容器部署为 `music_tag_web`（下划线），Compose 部署为 `music-tag-web`（连字符）。后续写笔记时不要混用。
- **`路径` 字段的前导斜杠不一致**：fnos-11.png 中 Compose 的「路径」填的是 `vol1/1000/mtw_config`（无前导 `/`），而同页 YAML 卷里写的是 `/vol1/1000/mtw_config`（有前导 `/`）。


