# 阶段 2：批量更新计划（run: update-xiaoya-fnos-alist）

## 2.0 更新目标

把「小雅 fnOS 单容器部署」整套笔记的部署主线，从**已停止维护**的 monlor 镜像换成**持续维护**的 `xiaoyaDev/xiaoya-alist`（DDSRem 整合脚本），部署方式改用其 README 给出的一键菜单脚本。章节结构（1 开篇定位 → 7 运维与收尾）保持不变。

| 项目 | 旧（现笔记） | 新（本次改写） | 依据 |
| --- | --- | --- | --- |
| 部署项目 | `monlor/docker-xiaoya`（最后提交 2025-03-27） | `xiaoyaDev/xiaoya-alist`（最后提交 2026-10-06） | 两仓库提交史 |
| 一键命令 | monlor `install.sh` | `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"` → 菜单 `1 1` | `sources/01_raw_githubusercontent_com.md:39,75` |

## 2.1 跨章统一替换项（G 清单）

同一件事在多篇出现，按此表统一口径，避免各章改法打架。

| # | 维度 | 旧（monlor） | 新（xiaoyaDev / DDSRem） | 依据 |
| --- | --- | --- | --- | --- |
| G1 | 维护方 | 社区维护者 monlor | 社区整合脚本项目 `xiaoyaDev/xiaoya-alist`（作者 DDSRem） | README |
| G2 | 一键命令 | `curl .../monlor/docker-xiaoya/main/install.sh` | `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"`，菜单选 **`1 1`（安装 小雅Alist）** | `README:39`、`:75` |
| G3 | 容器镜像 | `ghcr.io/monlor/xiaoya-alist`（社区镜像） | `xiaoyaliu/alist:latest`（**小雅官方镜像**；host 网络改 `xiaoyaliu/alist:hostmode`） | `all_in_one.sh:1373,1376` |
| G4 | 端口 | 宿主 `5677` → 容器 `5678`；`5345`/`5346` | 宿主 `5678` → 容器 `80`；`2345:2345`、`2346:2346`、`2347:2347` | `all_in_one.sh:1377` |
| G5 | 配置目录 | `/vol2/1000/docker2/xiaoya/data` 挂容器 `/data` | 默认 `/etc/xiaoya`，挂容器 `/data`（其下 `data/` 再挂 `/www/data`） | `all_in_one.sh:156,1392` |
| G6 | 凭据注入 | 环境变量三件套 | 安装时**交互式**写入 `${CONFIG_DIR}/` 下的 `mytoken.txt`、`myopentoken.txt`、`temp_transfer_folder_id.txt`、`quark_cookie.txt`、`115_cookie.txt`、`uc_cookie.txt` | `all_in_one.sh:569,628,1204起` |
| G7 | 单容器形态 | `EMBY_ENABLED=false` + `JELLYFIN_ENABLED=false` | 菜单**只选 `1 1`**，不装全家桶（没有 env 开关） | `README:75` |
| G8 | WebDAV | `guest` / `guest_Api789` / `/dav` | 路径 `/dav`；**开了「强制登入」→ 用户名固定 `dav` + 你自己设的密码**；未开强制登入 → `guest` / `guest_Api789` | `all_in_one.sh:1302,1401,1403`；`01_hub_docker_com.md:18` |
| G9 | 更新 | 重跑 monlor `install.sh` | 菜单 **`1 2`（更新 小雅Alist）** | `README:120` |
| G10 | 卸载 | — | 菜单 **`1 3`（卸载 小雅Alist）** | `README:132` |
| G11 | 就绪判定 | 「获取设置失败」+ 等 1~5 分钟 | 脚本**内置等待**：轮询容器日志直到出现 `success load storage: [/©️`（60s 起，600s 超时告警） | `all_in_one.sh:202,204` |
| G12 | 术语校正 | 把现用镜像笼统说成「社区/官方」 | `xiaoyaDev/xiaoya-alist` 是**社区整合脚本（不是官方）**；**官方**指的是镜像 `xiaoyaliu/alist`（作者 xiaoyaLiu，`alist.xiaoya.pro`） | `01_hub_docker_com.md` + README |

> **G8 是本次最需要讲清的一点**：`dav` 与 `guest` 的历史混用，根源是「**路径** `/dav`」与「**强制登入用户名** `dav`」两回事。旧笔记上一轮已用「实战反证」把用户名定为 `guest`——那只对**未开强制登入**成立。新脚本默认开强制登入，故第 3/4/7 章须改成上面这个两分支写法。

## 2.2 逐篇动作

| id | 文件 | 动作 | 主要改动 |
| --- | --- | --- | --- |
| ch04 | `chapters/04_部署实战.md` | **update（重写）** | 整章换主线：4.1 改为「为什么用 xiaoyaDev 一键脚本」（替换 monlor 五行表）；4.2 改为菜单 `1 1` 部署全程（含 G2–G8 要点、配置目录、凭据交互、端口）；4.3 自检改为脚本内置就绪判定 + WebDAV 两分支；章名与 frontmatter title 同步改 |
| ch03 | `chapters/03_动手前准备.md` | update | 三张清单换源：目录 `/etc/xiaoya`、端口 `5678/2345/2346/2347`、凭据文件名（G5/G4/G6）；§3.5 compose 片段替换为「一键脚本 + 可选手写 compose（官方镜像）」；WebDAV 两分支（G8） |
| ch07 | `chapters/07_运维与收尾.md` | update | §7.3 更新口径改菜单 `1 2`（G9）；补卸载 `1 3`（G10）；§7.4 资源推荐表换为脚本/官方镜像口径；§7.6 未决项删除 monlor 镜像名 |
| ch01 | `chapters/01_开篇定位.md` | update | 组件与「纯净版」描述换到 xiaoyaDev 语境（G1/G12）；术语校正：整合脚本 vs 官方镜像 |
| ch02 | `chapters/02_选型对比.md` | update | 路线 E/F 组成换为「DDSRem 全家桶菜单 vs 只装 `1 1`」（G7）；资源推荐表换源；Jellyfin 弃用/风险提示按 README:181 表述 |
| ch05 | `chapters/05_前端接入.md` | update（轻） | 仅改 monlor 相关引文与措辞：阿里云盘限速、转存 115（`ALIYUN_TO_115` → 脚本的 `ali2115.txt`/`settings_ali2115`）、会员相关注脚换源；前端工具（MediaWarp/SmartStrm/fntv-proxy）主体不动 |
| ch06 | `chapters/06_避坑清单.md` | update（轻） | 把 `AUTO_CLEAR_ENABLED` 提法改为脚本菜单口径（`2 9 1 1` 清理 mp4 元数据）；补一条「端口 5678/2347」与「强制登入」相关坑 |
| overview | `output/小雅 fnOS 单容器部署（总览）.md` | update | 读前须知把 monlor 镜像/项目换成 xiaoyaDev 一键脚本；**不在 `chapters/`，须在 `output/` 与 vault 两处手改** |

无 `skip`、无 `needs-review`。

## 2.3 批次编排（batch_size = 3）

| 批次 | 文件 | 理由 |
| --- | --- | --- |
| **批 1（锚点）** | ch04 → ch03 → ch07 | 这三篇是「部署主线」，monlor 密度最高，且互相引用（目录/端口/凭据/更新）。先定调，后续章节照它对齐 |
| **批 2（叙事）** | ch01 → ch02 → overview | 开篇定位、选型对比、总览都是「怎么讲这件事」，依赖批 1 定下的口径 |
| **批 3（收口）** | ch05 → ch06 | 前端接入改动轻、避坑清单靠后，最后统一收口 |

每批完成后：`publish_copies.py --apply --only <xx>` 同步 `output/` 与 vault 副本；全部完成后 `assemble_final.py --apply` 重建 `final_note.md`。

## 2.4 覆盖风险

| # | 风险 | 说明 | 处置 |
| --- | --- | --- | --- |
| R1 | **端口冲突** | 宿主端口由 `5677` 变 `5678`，并新增 `2347`。老笔记的 fnOS 端口/防火墙/路由器转发规则会失效 | 第 3 章端口清单标注「旧笔记用 5677，新版用 5678」，第 6 章加坑 |
| R2 | **配置目录冲突** | `/vol2/1000/docker2/xiaoya/data` → `/etc/xiaoya`。已按旧笔记部署过的读者会被误导 | 第 3、7 章明写「脚本默认 `/etc/xiaoya`，可在安装时改」 |
| R3 | **WebDAV 凭据口径变更** | 见 G8 两分支 | 第 3/4/7 章统一按 G8 写，并解释 `dav`/`guest` 的历史混淆 |
| R4 | **截图与新界面不符** | `assets/04 部署实战/*.png` 两张是 **monlor compose/环境变量**界面，新路线是**终端菜单** | **需用户确认**（见 2.5） |
| R5 | **`chapters/` 无 frontmatter** | 章名/frontmatter title 在发布件里，改标题须用 `publish_copies.py --title <xx> "<新标题>"` | 批 1 处理 ch04 时一并改标题 |
| R6 | **旧引文出处失效** | `sources/p2/monlor-*.md`、`sources/p3/monlor-env/*`、`sources/forum/tid-9690.md` 是 monlor 语境来源 | 引用改挂 `sources/01_raw_githubusercontent_com.md`、`sources/xiaoyaDev/all_in_one.sh`、`sources/01_hub_docker_com.md`；确实只属 monlor 的行移入「更新记录」备案 |

## 2.5 需用户确认项

1. **截图怎么办（R4）** —— 新路线是终端菜单，旧两张 monlor 界面截图对不上：
   - (a) 保留截图，加一句「界面为旧版 compose 示意」；
   - (b) 直接删掉两张图；
   - (c) 你之后自己补新截图，我先把图注写好占位。
2. **章名** —— ch04 拟由「第 4 章 部署实战——单容器小雅（monlor 镜像）」改为「**第 4 章 部署实战——单容器小雅（一键脚本）**」。
3. **`ali2115` 转存 115 的深度** —— 第 5 章只在正文顺带提，不展开成教程（维持主线不扩为全家桶）。

## 2.6 验收

- 全库 `rg -n "monlor|ghcr.io/monlor|EMBY_ENABLED|JELLYFIN_ENABLED"` 仅命中 `更新记录` 与 `sources/`。
- 每章「引文对照」表逐条可回源；新增引文取 `sources/01_raw_githubusercontent_com.md` / `sources/xiaoyaDev/all_in_one.sh`。
- `.claude/scripts/check-md-structure.py` 与引文检查通过。
- `publish_copies.py --check` 与 `assemble_final.py --check` 无差异。
