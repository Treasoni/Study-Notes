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
