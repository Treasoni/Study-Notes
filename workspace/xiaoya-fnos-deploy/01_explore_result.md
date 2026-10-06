# 01 探测结果（P1）— fnOS 部署纯净版小雅（单容器）

> **本文件是中间产物**：引文与数值请回 `sources/` 按行号核对。本文件只列来源记录与方向判断，**不含逐字引文、不含未回源的数字**。

- 主题：在 fnOS（飞牛 OS）中部署纯净版小雅（单容器）——飞牛影视能否替代 Emby，以及单容器部署步骤
- 运行：`xiaoya-fnos-deploy` ｜ 阶段：P1 探测式收集
- 探测透镜：A 单容器定位与官方部署路径 ｜ B 飞牛影视 vs Emby 作前端 ｜ C fnOS 落地与踩坑
- 抓取工具：`crawl4ai`（`.claude/skills/research-collector/scripts/crawl.sh`）。本环境 `curl`/`WebFetch` 被封禁，全部抓取走 crawl4ai。

---

## 一、去重后的来源清单（按 canonical URL）

`evidence_form`：`fetched` = 正文已落盘可逐行核对；`snippet-only` = 仅见搜索引擎摘要，**P2 须先抓取才可当证据**。

| # | 标题 | URL | tier | evidence | 日期 | 快照路径 | 分 |
|---|---|---|---|---|---|---|---|
| S1 | xiaoyaliu/alist 官方镜像页 | https://hub.docker.com/r/xiaoyaliu/alist | official | **fetched** | unknown | `sources/01_hub_docker_com.md` | 5 |
| S2 | xiaoyaDev/xiaoya-alist README（main.sh 功能列表） | https://raw.githubusercontent.com/xiaoyaDev/xiaoya-alist/master/README.md | official | **fetched** | unknown | `sources/01_raw_githubusercontent_com.md` | 5 |
| S3 | 小雅Alist部署教程【解决应用中心版本无数据】 | https://club.fnnas.com/forum.php?mod=viewthread&tid=9690 | community | **fetched** | 2024-12-31 | `sources/forum/tid-9690.md` | 5 |
| S4 | 我把 xiaoyaemby 刮削好的 strm 放到飞牛影音 | https://club.fnnas.com/forum.php?mod=viewthread&tid=73955 | community | **fetched** | 2026-09-29（推算） | `sources/forum/tid-73955.md` | 5 |
| S5 | SmartStrm 快速部署（项目官方文档） | https://smartstrm.github.io/guide/deploy | official | **fetched** | unknown | `sources/01_smartstrm_github_io.md` | 5 |
| S6 | xiaoyaDev/xiaoyahelper（xiaoyakeeper 来源） | https://github.com/xiaoyaDev/xiaoyahelper | official | **fetched** | unknown | `sources/01_github_com.md` | 5 |
| S7 | AkimioJR/MediaWarp（飞牛影视中间件） | https://github.com/AkimioJR/MediaWarp | official | **fetched** | 2026-10-01 | `sources/lens-b/mediawarp/01_github_com.md` | 4 |
| S8 | jimboo7339/fntv-proxy（飞牛影视 302 代理） | https://github.com/jimboo7339/fntv-proxy | official | **fetched** | 2026-07-06 | `sources/lens-b/fntvproxy/01_github_com.md` | 4 |
| S9 | 飞牛影视 strm 实战教程 | https://club.fnnas.com/forum.php?mod=viewthread&tid=57134 | community | snippet-only | unknown | — | 4 |
| S10 | 【已解决】飞牛影视+Alist小雅刮削后无影视文件 | https://club.fnnas.com/forum.php?mod=viewthread&tid=40446 | community | snippet-only | unknown | — | 4 |
| S11 | 小雅安装后飞牛影视扫描会转存到个人阿里网盘 | https://club.fnnas.com/forum.php?mod=viewthread&tid=6046 | community | snippet-only | unknown | — | 4 |
| S12 | 用飞牛影视连接小雅，可行吗？可行，又不太行（知乎） | https://zhuanlan.zhihu.com/p/2063793058689421981 | community | snippet-only | unknown | — | 4 |
| S13 | monlor 项目维护者站点（docker-xiaoya） | https://www.monlor.com/archives/144/ | reputable | snippet-only | unknown | — | 3 |
| S14 | newzone.top 运维笔记：小雅 Alist 部署 | https://newzone.top/services/dockers-on-nas/xiaoya.html | reputable | snippet-only | unknown | — | 3 |
| S15 | 官方页面指向的 Notion 配置指南 | https://www.notion.so/xiaoyaliu/xiaoya-docker-69404af849504fa5bcf9f2dd5ecaa75f | official | 未抓取 | unknown | — | 待评 |

> 说明：阶段 0 规划器的一次探测（搜索结果摘要）与上表重叠，已并入；未新增独立记录。

---

## 二、三透镜的观察（描述性；不构成结论）

### 透镜 A —「纯净版 / 单容器」定位与官方路径
- 官方单容器入口是 `xiaoyaliu/alist` 镜像（S1）；官方编排脚本 `main.sh` 的功能表把「安装小雅 Alist」与「Emby 全家桶」列为**不同菜单项**（S2），兼容性表列出 fnOS ✅（S2）。
- **「纯净版（单容器）」不是官方术语**：S1、S2 均未出现该词。官方语义接近「只装小雅 Alist / 只跑一个容器」，社区俗称另有其词。
- **存在至少三条并存的部署路线**（P2 需裁决推荐哪条）：
  1. 官方 `xiaoyaliu/alist` 镜像 + `/data` 下三个 `.txt` 凭据文件（S1 + 社区）；
  2. `ghcr.io/monlor/xiaoya-alist` 镜像 + 环境变量（`ALIYUN_TOKEN` 等）（S3、S13）；
  3. 社区手写 `xiaoyaliu/alist:latest` compose（S14）。
- WebDAV 账号在多来源一致指向 `guest / guest_Api789`（S1、S3）——**P2 需回源逐字确认**。

### 透镜 B — 飞牛影视 vs Emby 作前端
- **不必须 Emby**：社区路线含小雅网页端直接播、TVBox、WebDAV 播放器、STRM + 飞牛影视（S4、S7、S8）。
- **飞牛影视可作刮削+播放前端**，但机制与 Emby 全家桶不同：Emby 路线吃小雅现成元数据包；飞牛影视走自身网络刮削 / STRM（S4、S12）。
- **直接让小雅被飞牛影视扫描有云盘风控风险**，稳妥路线是先备好 STRM 再喂给飞牛影视（S10、S11、S12）。
- **外网可达性是已知坑**：飞牛原生 `/stream` 可能返回内网地址，蜂窝网络播不动；社区用 MediaWarp（媒体服务器类型选 FNTV）或 fntv-proxy 做 302 代理（S4、S7、S8）。

### 透镜 C — fnOS 落地与踩坑
- **应用中心版小雅**：社区一致称「装上无数据、需卸载改用 Docker 重装」（S3）；**「是否已官方下架/停更」未获官方公告，属推断**。
- **STRM 生成路径**：SmartStrm 有官方部署文档、含 fnOS 应用中心装法与 Docker Compose（S5）；飞牛论坛有实操帖（S9）。
- **清理转存缓存**：`xiaoyakeeper` 官方来源为 `xiaoyaDev/xiaoyahelper`（S6），含定时/实时清理模式与自定义时间。
- **应用中心 vs 手动部署**：S5（SmartStrm，仍在维护）称应用中心版仅滞后 1~2 版；S3 称小雅应用中心版事实不可用——**两者不可类推**（一个是维护中的第三方工具，一个是停更项目）。

---

## 三、未确认 / 待核实（P2 必须回源，不得作为结论）

1. **「纯净版」的官方语义**：非官方术语；需在正文里说明社区叫法，避免当成规范名词。
2. **三个 `/data` 凭据文件机制**（`mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt`）：**未在任何已抓官方来源出现**，仅社区教程；且 monlor 路线用环境变量、机制不同。
3. **`ghcr.io` 是否有「官方」小雅镜像**：未发现官方 `ghcr`；社区用的是 monlor 的 `ghcr.io/monlor/xiaoya-alist`。
4. **`xiaoya.host` 是否官方域**：未证；仅见于社区 STRM 链路描述。
5. **飞牛影视开始支持 STRM 的版本号**：来源冲突（0.9.1 / 0.9.3 / 更早说法）——须以实际版本实测，不写死。
6. **飞牛「应用中心」小雅是否已下架/停更**：仅社区推断，无官方公告。
7. **「半分钟产生几 T 临时文件」量级**：仅见搜索聚合摘要，无原始帖逐字印证——**该数字不得引用**；只可写「触发转存/风控、媒体库变空」的方向性结论（有 S10 等支撑）。
8. **官方 Notion 配置指南（S15）**：未抓取；单容器完整参数表可能在此，P2 需定向抓取。
9. **仍有 4 条关键来源为 snippet-only**：S9、S10、S11、S12 —— P2 必须先抓取正文再引用。

---

## 四、方向菜单（请选择 P2 方向）

**方向 1（推荐）— 部署主线 + 飞牛影视作前端，直接覆盖你的两问**
先回答选型：纯净版不必须 Emby，飞牛影视可替代但有前置条件（STRM + 302 代理 + 外网可达性）；再给单容器部署实操（应用中心 vs 手动 Docker 的取舍、镜像路线裁决、凭据配置、WebDAV/STRM 接入飞牛影视）。P2 需补齐：Notion 官方配置、镜像路线裁决、STRM 生成、风控与清理。

**方向 2 — 以「飞牛影视 vs Emby 选型对比」为主**
部署步骤压缩为附录。适合你更关心「到底用哪个前端」。

**方向 3 — 加一层「全家桶（Alist+Emby）对照」**
作为「为什么可以不用 Emby」的反衬，代价是篇幅变长。

**附加项（可勾选）**
- [ ] 纳入「云盘风控与转存缓存清理（xiaoyakeeper）」为独立小节
- [ ] 纳入「外网访问」小节（302 代理 / 内网穿透）
- [ ] 保留「应用中心版为何不可用」的排除过程（可作为避坑）

---

## 五、估计 P2 规模

- **必抓（snippet-only → fetched）**：S9、S10、S11、S12，加 S15（Notion）。
- **需回源逐字核对**：WebDAV 账号、端口清单、`main.sh` 菜单编号、SmartStrm 端口与目录、xiaoyakeeper 模式编号。
- **预计 2–3 个批量子代理**（≤3 并发），每组一簇来源；产出 `02_deep_research.md`。
- **下游影响**：本主题与 vault `流媒体与影音/` 已有 3 篇笔记（Strm/302、网盘取舍、硬解软解）强相关，大纲阶段应规划双链。

---

## 六、用户选择（待填）

- 方向：_____
- 附加项：_____
