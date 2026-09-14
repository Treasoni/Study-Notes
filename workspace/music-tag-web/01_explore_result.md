# 01 探测结果 — 如何使用 Music Tag Web

- **主题**: 如何使用 Music Tag Web（自托管音乐标签编辑器）
- **项目**: `xhongc/music-tag-web` · 默认分支 `dev_1.0`
- **阶段**: P1 探测式收集
- **检索日期**: 2026-09-14
- **探测方式**: 3 个独立 lens 并行探测（部署配置 / 功能操作 / 排错生态），去重后合并

---

## 一、一手核验结论（本轮已回源逐字确认）

以下 3 条由父进程**直接 curl 原文**核验，不是子 agent 转述，可直接作为 P2 的既定事实，无需重复核实：

| # | 结论 | 原文（逐字） | 来源 |
| --- | --- | --- | --- |
| F1 | V1 与 V2 的唯一实质差异是**端口**和**是否要 `command: /start`** | "与V1 版本的区别，容器内的端口是 8002，和不需要 command /start 命令" / V1："容器内的端口是 8001。" "需要使用 `command /start` 命令来启动服务。" / V2："**容器端口**: V2 版本中的容器监听端口为 8002。" "**无需启动命令**: 不再需要使用 `command /start` 命令来启动服务。" | [V2 手册·快速开始](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md) |
| F2 | 镜像名 `xhongc/music_tag_web:latest`；**国内网络有阿里云镜像** | "镜像名称 `xhongc/music_tag_web:latest`" / "阿里云镜像名称：`registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest`" | 同上 |
| F3 | V2 Compose 是**三个卷**，比 `docker run` 示例多一个 `/app/download` | 见下方 YAML；"/path/to/your/download 替换为你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录" | [V2 手册·Docker Compose 部署](https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md) |

> [!warning] 已确认的坑：README 与官方手册不一致
> `docker run` 示例里**只有两个卷**（`/app/media`、`/app/data`），而 Compose 官方配置有**三个卷**。README 的 `--restart=always` 与手册的 `--restart=unless-stopped` 也不一致。笔记必须以**手册**为准，并显式说明第三个卷的作用。

F3 原文 YAML（逐字）：

```yaml
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
      - /path/to/your/download:/app/download
    restart: always
```

F2 官方 `docker run`（逐字）：

```bash
docker run -d -p 8002:8002 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --name=music-tag-web --restart=unless-stopped xhongc/music_tag_web:latest
```

其他同页已核验细节：访问 `http://127.0.0.1:8002`；默认账号 `admin/admin`；反向代理进后台报 **csrf** 错误时改用局域网地址访问；V2 需要**激活码**（"点击 V1 标签，按照提示输入 V2 激活码以完成激活"），激活报错时先校正服务器时间为北京时间。

---

## 二、官方文档全貌（来自 GitBook `llms.txt` 索引）

V2 手册 `llms.txt` 与 V1 手册 `llms.txt` 提供了完整页面树，是 P2 的**权威骨架**，不必再靠搜索拼凑。

### V2 手册（README 称"当前推荐"）

| 分组 | 页面 |
| --- | --- |
| 起步 | 项目介绍、快速开始、Docker部署、Docker Compose 部署 |
| **NAS 部署** | **群晖部署**、**1panel部署**、**绿联部署**、**飞牛云 fnos 部署**、**极空间部署** |
| 进阶配置 | Mysql 部署、外置 Redis 服务、自定义服务端口、容器自动更新 |
| 功能描述 | 变量的使用说明、MCP、自动刮削、手动刮削、音乐收藏与播放、后台刮削、基本设置、小爱音箱、网盘音乐、智能歌单、音乐去重 |
| 教程文章 | 激活码激活失败无响应、刮削艺术家并被 navidrome 识别、批量重命名文件名称、忘记登录密码、手动刮削能实现哪些功能、怎么更新/升级版本、智能歌单进阶玩法、批量删除源数据中水印、多目录独立挂载的方式 |
| 其他 | 名词解释、常见问题（FAQ）、Subsonic 客户端（棉花音乐/箭头音乐/sonixd/音流/Web App PWA） |

### V1 手册（结构 = 经典"标签编辑"主线）

项目介绍、快速开始、手动修改标签、批量修改、自动批量修改、整理文件夹、简繁体转换、拆分文件名称、切割音轨、V2 版本

> [!tip] 关键判断
> V1 手册的目录顺序**本身就是一条现成的操作主线**：加载文件 → 手动改 → 批量改 → 自动刮削 → 整理文件夹 → 拆名 → 切轨。P2 可直接沿用这条顺序组织正文。
> V2 手册则把项目从"标签编辑器"扩成了"**音乐标签刮削 + 音乐播放一体的个人音乐库方案**"（自带 Subsonic 服务端）。

---

## 三、去重后的候选来源表

按 canonical URL 去重；来源层级：官方一手 / 项目仓库 / 社区实践 / 第三方二手。

| # | 标题 | URL | 层级 | 相关性 | 评分 |
| --- | --- | --- | --- | --- | --- |
| S1 | V2 手册·快速开始 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md | 官方一手 | V1/V2 差异 + 镜像说明（含阿里云） | 5 |
| S2 | V2 手册·Docker 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md | 官方一手 | 可照抄 `docker run` + 访问/改密/激活步骤 | 5 |
| S3 | V2 手册·Docker Compose 部署 | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md | 官方一手 | 三卷 Compose 全文 | 5 |
| S4 | V2 手册·常见问题 FAQ | https://xiers-organization.gitbook.io/music-tag-web-v2/chang-jian-wen-ti | 官方一手 | 新手卡点官方答案（8002、403、host 网络、mysql、激活 6 次上限） | 5 |
| S5 | V2 手册·刮削艺术家并被 navidrome 识别 | https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/gua-xiao-yi-shu-jia-bing-bei-navidrome-shi-bie | 官方一手 | 与 Navidrome 联动的官方依据（`artist.jpg` 自动识别） | 5 |
| S6 | V2 手册·NAS 部署组（群晖/1panel/绿联/飞牛/极空间） | https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/qun-hui-bu-shu 等 5 页 | 官方一手 | 直接对应已确认的"NAS 差异小节" | 5 |
| S7 | V2 手册·进阶配置组（Mysql/Redis/自定义端口/自动更新） | https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu 等 4 页 | 官方一手 | sqlite `database is locked`、host 网络端口冲突 | 4 |
| S8 | V2 手册·功能描述组（自动/手动/后台刮削、设置、小爱、网盘、歌单、去重） | https://xiers-organization.gitbook.io/music-tag-web-v2/gong-neng-miao-shu/... | 官方一手 | V2 播放侧功能，决定"要不要写宽" | 4 |
| S9 | V1 手册（全站） | https://xiers-organization.gitbook.io/music-tag-web/ | 官方一手 | 标签编辑主线的章节顺序 | 5 |
| S10 | 仓库 README（dev_1.0） | https://github.com/xhongc/music-tag-web/blob/dev_1.0/README.md | 项目仓库 | V1/V2 并存、卷挂载；**SEO 文案，仅作交叉验证** | 3 |
| S11 | 仓库界面截图 `img_1`–`img_19` | https://github.com/xhongc/music-tag-web/tree/dev_1.0 | 项目仓库 | 唯一成体系 UI 参考（`templates/` 仅空 SPA 壳） | 4 |
| S12 | 官方在线演示实例 | http://117.72.222.188:8002/#/ | 官方一手 | 实测可达，可对照界面走通主线（admin/admin） | 4 |
| S13 | GitHub Issues 聚类 | https://github.com/xhongc/music-tag-web/issues?q=is%3Aissue+sort%3Acomments-desc | 项目仓库 | 6 类高频失败：默认密码/#81、升级 2.6.6 封面全挂/#546、改名报错/#33、映射目录不显示/#24、Redis 连不上/#397、勾选错乱/#479（**待回源**） | 4 |
| S14 | 飞牛 fnOS 论坛·刮削后 navidrome 识别不出 | https://club.fnnas.com/forum.php?mod=viewthread&tid=4152 | 社区实践 | NAS 侧真实排错串（"导出图片"开关 → `cover.jpg`；Navidrome `CoverArtPriority`） | 4 |
| S15 | 博客·Navidrome + MusicTagWeb 搭建私人音乐库 | https://www.cnblogs.com/ivoink/articles/22696323 | 社区实践 | 挂载曲库 + 刮削在真实个人曲库中的衔接 | 3 |
| S16 | Docker Hub·`xhongc/music_tag_web` tags | https://hub.docker.com/repository/docker/xhongc/music_tag_web/tags | 官方一手 | **未取到**（本环境 hub.docker.com 四次超时、WebFetch 被拦） | 3 |

---

## 四、覆盖缺口（P2 必须处理）

| 缺口 | 现状 | P2 处置 |
| --- | --- | --- |
| Docker Hub 实际 tag 与最后推送时间 | 本环境不可达 | 改走阿里云镜像页或第三方 tag 站；**取不到就在笔记中不写具体版本号**，只写 `latest` + 官方查询链接 |
| V2 激活码机制 | 只知"需要激活码""有 6 次上限" | 回源 FAQ 与《激活码激活失败》页，确认免费/收费与重置方式——**直接影响用户预期，必须写清** |
| 版本号与升级路径 | 只见 issue 提到 2.6.6、镜像 2.4.3 | 回源《怎么更新/升级版本》页；不猜测当前版本号 |
| 截图与功能的对应关系 | `img_1`–`img_19` 未逐张核对 | P2 只引用官方手册内已配文的图，不凭编号臆断 |
| 社区教程质量 | 大量互相抄袭 README，已剔除 | 仅保留 S14、S15 两篇有实拍/实证的 |

---

## 五、P2 预计范围

- **主骨架**: V2 手册（S1–S8，约 16–18 页）+ V1 手册（S9，约 9 页），均以 `.md` 后缀直取正文
- **交叉验证**: README（S10）、Issues 聚类（S13）
- **社区补充**: S14、S15（标注为社区实践，不与官方口径混写）
- **预计核心来源**: 3–5 个（按用户选定的方向裁剪，不整站搬运）
- **产出**: `02_deep_research.md` — 含 scope、来源表、claim/来源映射、矛盾点、实操指引、开放问题、下游交接

---

## 六、方向菜单（待用户选择）

用户已确认：**笔记类型=实战/操作指南**、**深度=上手**、**基础=有 Docker 基础未用过本项目**、**正文主线=通用 Docker Compose 为主 + NAS 差异小节**、**输出=项目 output**。

在此基础上，还需选定**覆盖范围**：

### 方向 A — 标签刮削主线（窄而深）
只写"把混乱曲库整理干净"这条线：部署 → 挂载 → 手动改标签 → 批量改 → 自动刮削 → 整理文件夹 → 拆名 → 切轨 → 繁简转换。
- 优点：与 V1 手册顺序一一对应，主线极清晰，篇幅可控
- 缺点：完全略过 V2 的音乐库/播放能力

### 方向 B — 标签 + 音乐库全貌（宽）
A 的全部，再加 V2 播放侧：Subsonic 服务端与客户端、小爱音箱、网盘音乐、智能歌单、音乐去重。
- 优点：覆盖 V2 的真实能力边界
- 缺点：主题从"标签编辑器"漂移成"个人音乐库方案"，篇幅约翻倍

### 方向 C — 部署与排错优先（运维向）
以部署（Docker/Compose/NAS 五平台）+ 进阶配置（Mysql/Redis/自定义端口/自动更新）+ FAQ 排错为骨架，标签操作压成一章速览。
- 优点：上手最快，踩坑最少
- 缺点：与"如何使用"的原始诉求相比，功能面偏薄

### 方向 D — 折中主线（**推荐**）
以 **A 为主线**，把 B 的播放侧、C 的进阶配置与 FAQ 全部收进 **「进阶与排错」附录章节**，正文主线保持单一。
- 优点：主线清晰 + 不丢信息，符合"上手"深度的合理篇幅
- 缺点：需要明确区分"正文主线"与"附录"，大纲阶段要多花一点结构设计

---

## 七、下一步

1. 用户从 **A / B / C / D** 中选定方向（或提出调整）
2. 确认 P1 素材质量 → 阶段 1 标记完成
3. 进入 **P2 深度收集**，按选定方向裁剪来源，回源核实第四节列出的 5 处缺口
