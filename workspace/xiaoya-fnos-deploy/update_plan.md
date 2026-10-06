# 更新计划：小雅 fnOS 单容器部署 · 第 5 章

- 更新日期：2026-10-06
- 目标笔记：`流媒体与影音/小雅 fnOS 单容器部署/05 前端接入.md`（vault，拆分笔记第 5 章）
- 上游源：`workspace/xiaoya-fnos-deploy/chapters/05_前端接入.md`
- destination_mode：`patch-in-place`（并同步 output/ 与 vault，无漂移）
- update_goal：回答用户新问题「**依旧用小雅的资源，但用夸克网盘会员**，该怎么办」
- 口径修正：初稿把答案写成「放弃小雅库、改挂自己的夸克库」；用户澄清后改为**先正面回答「小雅没有『把小雅资源播放到夸克』的开关」**，把「改挂自己的夸克库」降级为 5.6.5 的备选。

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | 5.1–5.5 全部结构、代码块、Callout、双链、既有引文对照第 1–27 行 |
| 新增 | 5.6「没有阿里云盘会员、只有夸克会员怎么办」（5.6.1–5.6.5）；本章小结新增 1 条；引文对照新增第 28–35 行；文末 `## 更新记录` |
| 改写 | 5.6 整节按修正口径重写（第 19–27 行引文对照沿用原行号，新增 28–35） |
| 删除 | 无 |
| 未处理 | 总览页章节目录第 5 条一句话说明未改（仍准确）；第 6 章未加 → 5.6 交叉指针 |

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 小雅必填阿里云盘账号 | `sources/01_club_fnnas_com.md:32` |
| 机理：转存进你自己的阿里云盘再播 | `sources/p3/z-addone/01_www_cnblogs_com.md:33` |
| 会员只影响限速（不付费即限速 / SVIP 仍 380kb/s） | `sources/p2/monlor-144.md:273`、`:279` |
| 夸克为 `QUARK_COOKIE` 非必填 | `sources/01_club_fnnas_com.md:32`、`:48` |
| 社区同问（帖中无正面回答） | `sources/01_club_fnnas_com.md:732` |
| 阿里转存 115 思路（`ALIYUN_TO_115`） | `sources/p3/monlor-env/01_raw_githubusercontent_com.md:19` |
| **小雅转战 115、须 115 会员** | `sources/p4/ycyc-2878.md:13` |
| **`ali2115.txt` 加速阿里资源到 115** | `sources/p4/ycyc-2878.md:19` |
| **没有 115 会员就放弃 / 限速到 100k** | `sources/forum/tid-21673.md:11`、`:13` |
| **「小雅夸克玩法」= 挂自己的夸克** | `sources/forum/tid-8385880.md:26` |
| **实测填夸克 cookie 仍只有阿里直链** | `sources/forum/tid-8385880.md:30` |
| **115 转存「非115会员不支持」/ >5G 不支持** | `sources/forum/tid-8385880.md:32`、`:34` |
| 备选链路：夸克网盘 TV 驱动 | `sources/p2/tid-57134.md:32`；`sources/lens-b/fntvproxy/01_github_com.md:300` |
| 夸克 HLS 元数据坑 | `sources/lens-b/fntvproxy/01_github_com.md:241` |

---

# 追加更新计划：第 3 章（动手前准备）

- 更新日期：2026-10-06
- 目标笔记：`流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（vault，拆分笔记第 3 章）
- 上游源：`workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md`
- destination_mode：`patch-in-place`（并同步 output/ 与 vault，无漂移）
- update_goal：补 3.3 缺失的「三件套**怎么拿**」（原文只有文件名 + 放置位置）

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | 3.1 / 3.2 / 3.4 / 3.5；3.3 既有四表与 Callout；引文对照 1–22 行 |
| 新增 | 3.3 内「那么这三样怎么拿到？」段；引文对照 23–29 行；`## 更新记录` |
| 改写 / 删除 | 无 |

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 三步拿法（解码站 / `request.html` 扫码 / 资源盘建夹取 folder id） | `sources/p3/gnz48/01_www_cnblogs_com.md:26-31` |
| 「获取方式」对照表 + 「先转存小雅分享」提醒 | `sources/p3/z-addone/01_www_cnblogs_com.md:21-25` |
| 论坛楼主答复 = `request.html` | `sources/01_club_fnnas_com.md:904` |
| `ALIYUN_TOKEN` 第二天失效（单条用户反馈） | `sources/01_club_fnnas_com.md:157` |

---

# 追加更新计划：第 3 章（动手前准备）· 扫码法（方案 A）

- 更新日期：2026-10-06
- 目标笔记：`流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（vault，拆分笔记第 3 章）
- 上游源：`workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md`
- destination_mode：`patch-in-place`（并同步 output/ 与 vault，无漂移）
- update_goal：用户「还是不会操作，有更简单详细的方法吗？」→ 把**手机扫码（方案 A）**写进 3.3，旧的 F12 + 解码站法降为备选

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | 3.1 / 3.2 / 3.4 / 3.5；3.3 前部四表；引文对照 1–29 行 |
| 改写 | 3.3「怎么拿」引言 + 三步表第 1 行（F12 → 扫码）；`[!tip]` 末句；`[!warning]` 由两条扩为三条 |
| 新增 | 3.3「近期教程扫码流程细化」段；`[!note]` 位数差异；引文对照 30–37 行；本章小结 1 条；`## 更新记录` 1 行 |
| 删除 | 无 |

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 32 位 token / OpenToken 用手机 App 扫码 | `sources/p5/slarker/01_wiki_slarker_me.md:29`、`:30` |
| 旧「复制网页代码」法已失效（接口变更） | `sources/p5/wsisp/01_www_wsisp_com.md:17` |
| 扫码五步流程 | `sources/p5/wsisp/01_www_wsisp_com.md:21-25` |
| token 有效期 2~3 个月 / 扫码须二次确认 | `sources/p5/wsisp/01_www_wsisp_com.md:11` |

---

# 追加更新计划：第 3 章（动手前准备）· 3.3 补「夸克 cookie 怎么拿」

- 更新日期：2026-10-06
- 目标笔记：`流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备.md`（vault，拆分笔记第 3 章）
- 上游源：`workspace/xiaoya-fnos-deploy/chapters/03_动手前准备.md`
- destination_mode：`patch-in-place`（并同步 output/ 与 vault，无漂移）
- update_goal：用户「夸克网盘 cookie 如何的」→「放入」；补 3.3 缺失的夸克 cookie **获取方式**

## Stale Map

| 处理 | 内容 |
| --- | --- |
| 保留 | 3.1 / 3.2 / 3.4 / 3.5；3.3 前部四表；引文对照 1–37 行 |
| 新增 | 3.3「夸克 cookie 怎么拿」段 + `[!warning]` 两个坑；引文对照 38–40 行；本章小结 1 处补充；`## 更新记录` 1 行 |
| 改写 / 删除 | 无 |

## 依据（新增内容全部回源）

| 论点 | 出处 |
| --- | --- |
| 夸克 cookie 拿法（F12 → 网络 → 带 `Cookie` 参数的请求） | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:47` |
| 必须用 Chrome（Firefox 停在访客态） | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:63` |
| `__puus` 约 3 小时过期、过期后下载 403 | `sources/gh/alist-9596.md:11` |
| 「填了不出效果」现场反馈 | `sources/forum/tid-8385880.md:30` |
